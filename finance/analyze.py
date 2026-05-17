"""Финансовый агент: пошаговый анализ компании через локальный Ollama.

Принцип:
    1. На каждой фазе (0-6) читаем SKILL.md и шаблон артефакта.
    2. Передаём модели: системный промпт (из Modelfile) + skill + предыдущие
       артефакты + ввод пользователя.
    3. Сохраняем ответ модели как артефакт фазы.
    4. Спрашиваем «принять и идти дальше / переделать / выйти».
    5. Состояние сессии хранится в .session.json, можно --resume.

Пример:
    python finance/analyze.py --ticker AAPL
    python finance/analyze.py --ticker AAPL --resume
    python finance/analyze.py --ticker AAPL --phase 2  # начать сразу с фазы

Замечания:
    - Web search не используется. Свежие данные (отчёты, новости) пользователь
      приносит в чат вручную в фазах 1 и 4. Все выводы помечаются как cutoff.
    - Для tool-call варианта (yfinance, pandas-ta) см. README.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

PHASES: list[tuple[str, str, str]] = [
    # (id, имя скилла, имя артефакта)
    ("0", "00-scoping", "00-scope.md"),
    ("1", "01-company-context", "01-context.md"),
    ("2", "02-fundamental", "02-fundamental.md"),
    ("3", "03-technical", "03-technical.md"),
    ("4", "04-sentiment-macro", "04-sentiment.md"),
    ("5", "05-synthesis", "05-synthesis.md"),
    ("6", "06-verdict", "06-verdict.md"),
]


@dataclass
class Session:
    ticker: str
    date: str
    workdir: Path
    completed_phases: list[str] = field(default_factory=list)
    artifacts: dict[str, str] = field(default_factory=dict)  # phase_id -> relative path

    @property
    def state_path(self) -> Path:
        return self.workdir / ".session.json"

    def save(self) -> None:
        data = {
            "ticker": self.ticker,
            "date": self.date,
            "completed_phases": self.completed_phases,
            "artifacts": self.artifacts,
        }
        self.state_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    @classmethod
    def load(cls, workdir: Path) -> "Session":
        data = json.loads((workdir / ".session.json").read_text(encoding="utf-8"))
        return cls(
            ticker=data["ticker"],
            date=data["date"],
            workdir=workdir,
            completed_phases=data["completed_phases"],
            artifacts=data["artifacts"],
        )


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def read_skill(skills_dir: Path, skill_name: str) -> str:
    """Читает SKILL.md фазы вместе с frontmatter."""
    skill_path = skills_dir / skill_name / "SKILL.md"
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill не найден: {skill_path}")
    return skill_path.read_text(encoding="utf-8")


def read_template(skills_dir: Path, artifact_name: str) -> str:
    """Шаблон артефакта (если есть)."""
    template_path = skills_dir / "shared" / "templates" / artifact_name
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return ""


def read_artifact(workdir: Path, artifact_name: str) -> str:
    """Содержимое уже созданного артефакта."""
    path = workdir / artifact_name
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def build_messages(
    *,
    skill_md: str,
    template: str,
    previous_artifacts: list[tuple[str, str]],
    user_input: str,
    phase_artifact_name: str,
) -> list[dict[str, str]]:
    """Собирает messages для /api/chat.

    Системный промпт уже зашит в Modelfile. Здесь — content для текущей фазы.
    """
    parts: list[str] = []
    parts.append(f"# Активная фаза: {phase_artifact_name}\n")
    parts.append("## SKILL.md этой фазы\n")
    parts.append(skill_md)
    if template:
        parts.append("\n## Шаблон артефакта\n")
        parts.append("Заполни этот шаблон. Не меняй структуру, только содержимое.\n")
        parts.append("```markdown\n" + template + "\n```")
    if previous_artifacts:
        parts.append("\n## Артефакты предыдущих фаз\n")
        for name, body in previous_artifacts:
            parts.append(f"### {name}\n\n```markdown\n{body}\n```")
    parts.append("\n## Ввод пользователя\n")
    parts.append(user_input or "(пользователь не передал дополнительного ввода)")
    parts.append(
        "\n## Задача\n"
        "Выполни инструкции SKILL.md. Если данных недостаточно — задай "
        "ОДИН уточняющий вопрос пользователю (и больше ничего). "
        "Если данных достаточно — заполни шаблон артефакта целиком в виде "
        "одного markdown-блока без обвязки. "
        "Не выходи за рамки текущей фазы."
    )
    return [{"role": "user", "content": "\n".join(parts)}]


def call_ollama(
    client: httpx.Client,
    host: str,
    model: str,
    messages: list[dict[str, str]],
    options: dict[str, Any],
) -> str:
    url = host.rstrip("/") + "/api/chat"
    payload = {
        "model": model,
        "stream": False,
        "messages": messages,
        "options": options,
    }
    resp = client.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["message"]["content"].strip()


def extract_markdown_block(text: str) -> str:
    """Если модель обернула ответ в ```markdown ... ``` — снимаем обёртку."""
    stripped = text.strip()
    if stripped.startswith("```"):
        first_nl = stripped.find("\n")
        if first_nl != -1 and stripped.rstrip().endswith("```"):
            return stripped[first_nl + 1 : stripped.rfind("```")].strip()
    return stripped


def run_phase(
    *,
    session: Session,
    phase_id: str,
    skill_name: str,
    artifact_name: str,
    config: dict[str, Any],
    skills_dir: Path,
    client: httpx.Client,
) -> bool:
    """Возвращает True, если фаза завершена и подтверждена пользователем."""
    console.rule(f"[bold]Фаза {phase_id} — {skill_name}[/bold]")

    skill_md = read_skill(skills_dir, skill_name)
    template = read_template(skills_dir, artifact_name)

    previous: list[tuple[str, str]] = []
    for prev_id, _, prev_artifact in PHASES:
        if prev_id == phase_id:
            break
        body = read_artifact(session.workdir, prev_artifact)
        if body:
            previous.append((prev_artifact, body))

    user_input = ""
    while True:
        console.print(
            Panel.fit(
                "Введите дополнительный контекст для фазы (вставьте свежие новости, "
                "отчёт, ссылки и т.п.). Пустая строка — продолжить без ввода. "
                "Закончите ввод одинокой строкой с одним символом '.'",
                title="Ввод",
            )
        )
        lines: list[str] = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line.strip() == ".":
                break
            lines.append(line)
        user_input = "\n".join(lines).strip()

        messages = build_messages(
            skill_md=skill_md,
            template=template,
            previous_artifacts=previous,
            user_input=user_input,
            phase_artifact_name=artifact_name,
        )

        console.print("[dim]Запрос к модели…[/dim]")
        reply = call_ollama(
            client,
            host=config["host"],
            model=config["model"],
            messages=messages,
            options=config.get("options", {}),
        )

        console.print(Panel(Markdown(reply), title=f"Ответ модели — {artifact_name}"))

        action = Prompt.ask(
            "Действие",
            choices=["save", "retry", "skip", "quit"],
            default="save",
        )

        if action == "save":
            body = extract_markdown_block(reply)
            artifact_path = session.workdir / artifact_name
            artifact_path.write_text(body + "\n", encoding="utf-8")
            session.completed_phases.append(phase_id)
            session.artifacts[phase_id] = artifact_name
            session.save()
            console.print(f"[green]Сохранено: {artifact_path}[/green]")
            return True
        if action == "retry":
            console.print("[yellow]Повторяем фазу. Уточните ввод.[/yellow]")
            continue
        if action == "skip":
            console.print("[yellow]Пропускаем фазу (не рекомендуется).[/yellow]")
            return False
        if action == "quit":
            console.print("[red]Сессия прервана. Можно продолжить через --resume.[/red]")
            sys.exit(0)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Финансовый агент: пошаговый анализ компании через Ollama."
    )
    parser.add_argument("--ticker", required=False, help="Тикер компании, например AAPL.")
    parser.add_argument("--config", type=Path, default=Path("finance/config.yaml"),
                        help="Путь к config.yaml.")
    parser.add_argument("--model", help="Имя модели в Ollama (переопределяет config).")
    parser.add_argument("--host", help="URL Ollama (переопределяет config).")
    parser.add_argument("--resume", action="store_true",
                        help="Продолжить последнюю сессию для тикера.")
    parser.add_argument("--phase", help="Начать с фазы N (0-6), пропустив предыдущие.")
    parser.add_argument("--date", help="Дата сессии (по умолчанию сегодня, YYYY-MM-DD).")
    args = parser.parse_args()

    config: dict[str, Any] = {
        "model": "finance-agent",
        "host": "http://localhost:11434",
        "research_dir": "docs/research",
        "skills_dir": ".claude/skills/financial-analysis",
        "request_timeout": 600,
        "options": {},
    }
    config.update(load_config(args.config))
    if args.model:
        config["model"] = args.model
    if args.host:
        config["host"] = args.host

    skills_dir = Path(config["skills_dir"])
    if not skills_dir.exists():
        console.print(f"[red]Skills dir не найден: {skills_dir}[/red]")
        return 1

    if not args.ticker:
        console.print("[red]--ticker обязателен.[/red]")
        return 1

    date = args.date or dt.date.today().isoformat()
    workdir = Path(config["research_dir"]) / args.ticker.upper() / date
    workdir.mkdir(parents=True, exist_ok=True)

    if args.resume and (workdir / ".session.json").exists():
        session = Session.load(workdir)
        console.print(f"[green]Возобновляем сессию: {session.workdir}[/green]")
    else:
        session = Session(ticker=args.ticker.upper(), date=date, workdir=workdir)
        session.save()
        console.print(f"[green]Новая сессия: {session.workdir}[/green]")

    start_idx = 0
    if args.phase:
        ids = [p[0] for p in PHASES]
        if args.phase not in ids:
            console.print(f"[red]Фаза {args.phase} не существует.[/red]")
            return 1
        start_idx = ids.index(args.phase)
    elif args.resume and session.completed_phases:
        last_done = session.completed_phases[-1]
        ids = [p[0] for p in PHASES]
        start_idx = ids.index(last_done) + 1

    with httpx.Client(timeout=config["request_timeout"]) as client:
        for idx, (phase_id, skill_name, artifact_name) in enumerate(PHASES):
            if idx < start_idx:
                continue
            if phase_id in session.completed_phases and not args.phase:
                continue
            ok = run_phase(
                session=session,
                phase_id=phase_id,
                skill_name=skill_name,
                artifact_name=artifact_name,
                config=config,
                skills_dir=skills_dir,
                client=client,
            )
            if not ok and phase_id != "6":
                cont = Prompt.ask(
                    f"Фаза {phase_id} не подтверждена. Продолжить со следующей?",
                    choices=["yes", "no"],
                    default="no",
                )
                if cont == "no":
                    return 0

    console.rule("[bold green]Готово[/bold green]")
    console.print(f"Артефакты: {session.workdir}")
    console.print("Финал — 06-verdict.md. Disclaimer: не индивидуальная рекомендация.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

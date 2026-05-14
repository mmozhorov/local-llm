"""Пакетный перевод книги через локальный Ollama API.

Принцип:
    1. Читаем входной .txt в UTF-8.
    2. Делим на куски по границам абзацев (двойной перевод строки), стараясь не превышать
       --chunk-chars символов.
    3. Каждый кусок отправляем в Ollama через /api/chat и пишем перевод в выходной файл.
    4. Состояние сохраняем в <output>.progress.json — при повторном запуске можно --resume.

Пример:
    python translate_book.py --input book.txt --output book.ru.txt --model translator-qwen
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import httpx
from tqdm import tqdm


@dataclass
class Chunk:
    index: int
    text: str


def split_into_chunks(text: str, max_chars: int) -> list[Chunk]:
    """Бьём текст на куски по двойному переводу строки, не превышая max_chars."""
    paragraphs = [p for p in text.split("\n\n")]
    chunks: list[str] = []
    buf: list[str] = []
    buf_len = 0

    for para in paragraphs:
        # +2 на разделитель "\n\n"
        para_len = len(para) + 2
        if buf and buf_len + para_len > max_chars:
            chunks.append("\n\n".join(buf))
            buf = [para]
            buf_len = para_len
        else:
            buf.append(para)
            buf_len += para_len

    if buf:
        chunks.append("\n\n".join(buf))

    # Если один абзац длиннее max_chars — режем по строкам.
    refined: list[str] = []
    for c in chunks:
        if len(c) <= max_chars:
            refined.append(c)
            continue
        lines = c.split("\n")
        sub: list[str] = []
        sub_len = 0
        for line in lines:
            ln = len(line) + 1
            if sub and sub_len + ln > max_chars:
                refined.append("\n".join(sub))
                sub = [line]
                sub_len = ln
            else:
                sub.append(line)
                sub_len += ln
        if sub:
            refined.append("\n".join(sub))

    return [Chunk(i, t) for i, t in enumerate(refined)]


def translate_chunk(client: httpx.Client, host: str, model: str, text: str) -> str:
    """Один запрос к /api/chat. Возвращает перевод без обвязки."""
    url = host.rstrip("/") + "/api/chat"
    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": text,
            }
        ],
        "options": {
            # Параметры из Modelfile уже выставлены, но дублируем на случай чистой модели.
            "temperature": 0.3,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
        },
    }
    resp = client.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["message"]["content"].strip()


def load_progress(path: Path) -> dict:
    if not path.exists():
        return {"done": [], "outputs": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_progress(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Перевод книги через локальную Ollama.")
    parser.add_argument("--input", required=True, type=Path, help="Путь к исходному .txt (UTF-8).")
    parser.add_argument("--output", required=True, type=Path, help="Куда писать перевод.")
    parser.add_argument("--model", default="translator-qwen", help="Имя модели в Ollama.")
    parser.add_argument("--host", default="http://localhost:11434", help="Базовый URL Ollama.")
    parser.add_argument("--chunk-chars", type=int, default=4000, help="Максимум символов в одном куске.")
    parser.add_argument("--request-timeout", type=float, default=600.0, help="Таймаут запроса, секунд.")
    parser.add_argument("--resume", action="store_true", help="Продолжить с последнего сохранённого куска.")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Не найден входной файл: {args.input}", file=sys.stderr)
        return 1

    src = args.input.read_text(encoding="utf-8")
    chunks = split_into_chunks(src, args.chunk_chars)
    print(f"Куска для перевода: {len(chunks)} (всего {len(src)} символов).")

    progress_path = args.output.with_suffix(args.output.suffix + ".progress.json")
    state = load_progress(progress_path) if args.resume else {"done": [], "outputs": {}}
    done = set(state["done"])

    args.output.parent.mkdir(parents=True, exist_ok=True)

    with httpx.Client(timeout=args.request_timeout) as client:
        for ch in tqdm(chunks, desc="Перевод", unit="chunk"):
            if ch.index in done:
                continue
            translated = translate_chunk(client, args.host, args.model, ch.text)
            state["outputs"][str(ch.index)] = translated
            state["done"].append(ch.index)
            done.add(ch.index)
            save_progress(progress_path, state)

    ordered = [state["outputs"][str(i)] for i in range(len(chunks))]
    args.output.write_text("\n\n".join(ordered) + "\n", encoding="utf-8")
    print(f"Готово: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Финансовый агент: как готовить и запускать

Инструкция для **Claude Code** (CLI / VS Code / JetBrains / Web). Описывает, как
собрать репозиторий под анализ компании, как запустить агента в двух режимах —
через Claude Code skills и через локальный Ollama — и как читать результаты.

> Методологический документ: `docs/financial-agent.md`. Этот файл — про
> «как нажать кнопки», а не про «что и почему».

---

## 0. Что уже есть в репо

```
.claude/skills/financial-analysis/      # superpowers-style skills (7 фаз + shared)
├── SKILL.md                            # роутер
├── 00-scoping/SKILL.md
├── 01-company-context/SKILL.md
├── 02-fundamental/SKILL.md
├── 03-technical/SKILL.md
├── 04-sentiment-macro/SKILL.md
├── 05-synthesis/SKILL.md
├── 06-verdict/SKILL.md
└── shared/
    ├── data-sources.md
    ├── anti-patterns.md
    ├── self-review.md
    └── templates/                      # шаблоны артефактов

modelfiles/finance-agent.Modelfile      # Ollama Modelfile (Qwen2.5 14B)
finance/
├── analyze.py                          # CLI-конвейер для локального Ollama
├── config.example.yaml
└── requirements.txt
docs/financial-agent.md                 # best practices (методология)
docs/claude-code-finance-howto.md       # этот файл
```

Артефакты анализа складываются в `docs/research/<TICKER>/<YYYY-MM-DD>/` —
эта папка в `.gitignore`, не утечёт в репо.

---

## 1. Два режима работы

| Режим | Когда выбирать | Web search | Стоимость |
|---|---|---|---|
| **A. Claude Code** | Облачные модели Anthropic, есть интернет, нужна свежая информация | Да (WebSearch / Exa MCP) | Платные токены |
| **B. Локальный Ollama** | Офлайн, приватные данные, своё железо | Нет (без MCP) | 0 после установки |

Можно комбинировать: на свежих фазах (1, 4) — Claude Code с web search,
на фундаменте и синтезе — локальный Qwen.

---

## 2. Режим A — Claude Code (рекомендуется)

### 2.1 Что нужно

- Claude Code установлен (CLI или IDE-расширение).
- Репо `local-llm` открыт как рабочая директория.
- Доступ к интернету для web search и WebFetch.

### 2.2 Как Claude Code находит skills

Claude Code автоматически подтягивает скиллы из `.claude/skills/`, если они там
лежат. Никаких отдельных команд не нужно. Достаточно стартовать сессию
в корне репо.

Проверка: в начале сессии скажи в чате *«какие skills у тебя доступны?»* —
агент должен перечислить `financial-analysis` (и его суб-скиллы).

### 2.3 Запуск анализа

В чате просто пишешь:

```
Проведи анализ AAPL по протоколу financial-analysis.
```

или

```
Хочу разобраться, стоит ли держать NVDA на горизонте 12 месяцев.
```

Дальше агент сам:

1. Активирует `financial-analysis/SKILL.md` (роутер).
2. Перейдёт к фазе 0 (`00-scoping`), задаст один вопрос за раз про горизонт,
   валюту, бенчмарк, риск-профиль.
3. Создаст `docs/research/AAPL/<сегодня>/00-scope.md` и попросит подтверждение.
4. Пройдёт фазы 1–6 в порядке, между фазами — короткий чекпоинт.
5. Финал — `06-verdict.md` с тезисом, action plan, мониторингом.

### 2.4 Если Claude Code не подхватил skills

Иногда (особенно в новой версии или при custom-конфиге) скиллы нужно
явно «представить»:

```
Прочитай .claude/skills/financial-analysis/SKILL.md и следуй ему буквально.
Тикер: AAPL.
```

После этого агент уйдёт по протоколу.

### 2.5 Подсказки

- Если хочешь **только TA** или **только фундамент** — скажи:
  *«Сделай только фазу 2 для AAPL, scope: 1 год, USD, S&P 500 бенчмарк»*.
  Агент создаст scope-файл с принятыми дефолтами и сделает только нужную фазу.
- Если на середине анализа просишь *«не уверен, надо ли»* — агент должен
  **остаться в текущей фазе**, не перепрыгивая к verdict. Если перепрыгнул —
  это нарушение HARD-GATE, напомни:
  > «Helo, HARD-GATE. Фаза 2 ещё не завершена. Сначала её, потом synthesis.»
- Web search активируй явно, если агент его игнорирует:
  *«Используй WebSearch и WebFetch для свежих данных в фазах 1 и 4»*.

### 2.6 Подключение MCP для финансовых данных (опционально)

Если хочешь, чтобы агент сам тянул цены и отчётность:

- **yfinance MCP server** или **FMP MCP server** — для programmatic доступа
  к ценам и financials.
- **Exa MCP** — лучший web search для finance research (свежесть, фильтр по
  доменам типа SEC).

Настройка — через `~/.claude/settings.json` или через `/mcp` команду Claude Code.

---

## 3. Режим B — Локальный Ollama (Qwen2.5 14B)

### 3.1 Что нужно

- Ollama установлен (см. `scripts/windows/install.ps1` или
  `scripts/macos/install.sh`).
- Минимум 12 ГБ VRAM (Windows + RTX 3060) или 24 ГБ unified memory (MacBook M-серии).
- Python 3.10+.

### 3.2 Сборка образа `finance-agent`

#### Windows

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\windows\pull-models.ps1
```

Скрипт скачает Qwen2.5 14B и соберёт три образа: `translator-qwen`,
`translator-nemo`, **`finance-agent`**.

#### macOS

```bash
bash scripts/macos/pull-models.sh
```

То же самое.

#### Только finance-agent (вручную)

```bash
ollama create finance-agent -f modelfiles/finance-agent.Modelfile
ollama list   # проверка
ollama run finance-agent "Скажи коротко, как ты будешь анализировать AAPL."
```

### 3.3 Установка Python-конвейера

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r finance/requirements.txt
cp finance/config.example.yaml finance/config.yaml
# (опционально) поправь model/host/research_dir
```

### 3.4 Запуск анализа

```bash
python finance/analyze.py --ticker AAPL
```

Что произойдёт:

1. Создаётся папка `docs/research/AAPL/<сегодня>/` и `.session.json` в ней.
2. Конвейер по очереди для фаз 0–6:
   - Читает `SKILL.md` фазы.
   - Подкладывает шаблон артефакта.
   - Подкладывает артефакты предыдущих фаз.
   - Просит у тебя ввод (свежие новости, отчёт, ссылки).
     Заверши ввод одной строкой с точкой `.` на отдельной строке.
   - Отправляет всё это в Qwen, печатает ответ.
   - Спрашивает: `save / retry / skip / quit`.
3. Финал — `06-verdict.md`.

### 3.5 Полезные флаги

| Флаг | Что |
|---|---|
| `--resume` | Продолжить последнюю сессию (по тикеру и `--date`) |
| `--phase 2` | Начать с фазы 2 (пропустив 0–1; полезно, если уже есть scope) |
| `--date 2026-05-17` | Использовать конкретную дату (для resume старой сессии) |
| `--model finance-agent` | Переопределить модель |
| `--host http://192.168.1.50:11434` | Удалённый Ollama (например, на десктопе) |

### 3.6 Важные ограничения локального режима

- **Нет web search.** Свежие данные приносишь сам в чат: вставляешь
  выдержки из отчёта, новости, sell-side комментарии. Без этого фазы 1 и 4
  работают на знаниях модели (с явным cutoff).
- **Нет tool calling** (по умолчанию). Если хочешь, чтобы агент сам считал DCF
  по числам из `yfinance` — это отдельная доработка (см. §5).
- **Контекст 24k**. На фазе 5–6 в промпте лежат шесть предыдущих артефактов;
  если суммарно > ~20k символов, агент может «забывать» начало. При OOM
  уменьши `num_ctx` в Modelfile до 16384 и пересобери образ.
- **Скорость.** Qwen 14B Q4_K_M на RTX 3060: 20–30 ток/с в начале, 8–12 ток/с
  ближе к 8k. Одна фаза занимает 1–3 минуты ответа модели.

---

## 4. Гибридный подход (рекомендуется на практике)

Самое продуктивное — комбинировать:

1. **Фазы 0, 1, 4** (нужна свежесть) — в Claude Code с web search.
2. **Фазы 2, 3, 5, 6** (вычисления, синтез) — локальный Ollama,
   приватность, бесплатно.

Чтобы перенести артефакты из Claude Code в локальный режим:

```bash
# Claude Code сохранит файлы в ту же папку docs/research/AAPL/<дата>/
# Просто запускаешь Ollama-конвейер с --resume:
python finance/analyze.py --ticker AAPL --resume --phase 2
```

И наоборот: если начал локально, потом дошёл до синтеза и нужен web check —
открой папку в Claude Code и попроси:

> «Я провёл локальный анализ AAPL по протоколу financial-analysis.
> Артефакты в `docs/research/AAPL/2026-05-17/`. Сделай свежий sentiment
> check (фаза 4) с web search и согласуй с моим synthesis.»

---

## 5. Расширения (необязательно)

### 5.1 Tool calling через `yfinance`

Хочешь, чтобы агент сам тянул цены и финансовые показатели — есть два пути:

**a) Через Claude Code MCP-сервер.** Поставь yfinance-mcp или fmp-mcp,
агент сам вызовет `get_quote` / `get_financials`.

**b) Через локальный pre-fetch.** Добавь скрипт `finance/fetch.py`,
который через `yfinance` тянет данные и кладёт в `<TICKER>/_data.json`.
Эту папку конвейер сам подкинет в контекст фазы 2.

Пример pre-fetch (можно дописать самостоятельно):

```python
import yfinance as yf
import json
from pathlib import Path

t = yf.Ticker("AAPL")
data = {
    "info": t.info,
    "financials": t.financials.to_dict(),
    "balance": t.balance_sheet.to_dict(),
    "cashflow": t.cashflow.to_dict(),
    "history_1y": t.history(period="1y")["Close"].to_dict(),
}
Path("docs/research/AAPL").mkdir(parents=True, exist_ok=True)
Path("docs/research/AAPL/_data.json").write_text(json.dumps(data, default=str, indent=2))
```

### 5.2 Технический анализ через `pandas-ta`

В фазе 3 удобно прикладывать к сообщению модели предварительно посчитанные
индикаторы. Минимальный сниппет:

```python
import yfinance as yf
import pandas_ta as ta

df = yf.download("AAPL", period="1y")
df["RSI14"] = ta.rsi(df["Close"], 14)
df["EMA20"] = ta.ema(df["Close"], 20)
df["EMA50"] = ta.ema(df["Close"], 50)
df["EMA200"] = ta.ema(df["Close"], 200)
df["ATR14"] = ta.atr(df["High"], df["Low"], df["Close"], 14)
print(df.tail(30).to_markdown())
```

Вывод вставляешь в чат на фазе 3 — модель использует его как «evidence».

### 5.3 Параллельный анализ нескольких тикеров

Если нужно сравнение, делаешь отдельные сессии для каждого тикера, а потом
финальный compare-step:

> «Сравни тезисы AAPL, MSFT, GOOGL из их `06-verdict.md`.
> Кого взять, кого избежать, какой риск-параметр у каждого.»

Это уже за пределами `financial-analysis` skill — обычный analytics-чат.

---

## 6. Чек-лист первого запуска

После клонирования репо:

- [ ] `python --version` ≥ 3.10
- [ ] `ollama --version` (если идём в режим B)
- [ ] Запустил `pull-models.ps1` / `pull-models.sh` или собрал `finance-agent` вручную
- [ ] `ollama list` показывает `finance-agent:latest`
- [ ] `pip install -r finance/requirements.txt`
- [ ] `cp finance/config.example.yaml finance/config.yaml`
- [ ] `python finance/analyze.py --ticker TEST` — конвейер стартует, открывается
      ввод фазы 0
- [ ] В Claude Code: `.claude/skills/financial-analysis/SKILL.md` виден агентом
      («какие skills у тебя есть?»)
- [ ] Тестовый прогон на знакомом тикере (AAPL / SBER) — посмотреть, что
      артефакты складываются в `docs/research/<TICKER>/<сегодня>/`

---

## 7. Траблшутинг

| Симптом | Причина | Что делать |
|---|---|---|
| `model 'finance-agent' not found` | Образ не собран | `ollama create finance-agent -f modelfiles/finance-agent.Modelfile` |
| `CUDA error: out of memory` | num_ctx 24576 не лезет в 12 ГБ | Поменяй `num_ctx 16384` в Modelfile, пересобери образ |
| Модель отвечает на английском | Системный промпт перебивается | В первом сообщении явно: «отвечай на русском» |
| Модель пропускает фазы | Контекст переполнился | Уменьши количество предыдущих артефактов в build_messages, либо разбей сессию на части |
| `httpx.ReadTimeout` | Долгий ответ | Увеличь `request_timeout` в `config.yaml` до 1200 |
| Claude Code не видит skills | Запущен не из корня репо | Открой папку `local-llm` как workspace, рестарт сессии |
| Артефакты не сохраняются | Нет прав на `docs/research/` | Создай папку вручную, проверь `ls -la docs/` |

---

## 8. Что дальше

- Прочитай `docs/financial-agent.md` целиком — там вся методология и
  обоснования. Без неё агент — просто шаблон.
- Запусти первый анализ на компании, которую хорошо знаешь, и сверь вывод
  агента со своим мнением. Калибровка процесса важнее, чем «вау, оно работает».
- Через 1-3 месяца открой `06-verdict.md` и сверь сценарии с тем,
  что реально произошло. Это единственный способ понять, насколько процесс полезен.

Disclaimer: ничего из этого — не инвестиционная рекомендация.

# Локальная LLM для перевода книг

Готовый набор скриптов, Modelfile-ов и Python-утилит, чтобы быстро поднять локальную LLM на одной из двух машин и переводить книги с английского на русский:

| Машина | OS | Память | GPU |
|---|---|---|---|
| Десктоп | Windows 11 | 32 ГБ DDR5 + 12 ГБ VRAM | RTX 3060, i7-14700F |
| Ноутбук | macOS | 24 ГБ unified | MacBook Pro M4 (Apple Silicon, Metal) |

Стек одинаковый для обеих:

- **Ollama** — рантайм для GGUF, OpenAI-совместимый API, CUDA на Windows и Metal на macOS из коробки.
- **Qwen2.5 14B Instruct (Q4_K_M)** — основная модель: сильна в русском, помещается и в 12 ГБ VRAM, и в 24 ГБ unified.
- **Mistral Nemo 12B Instruct (Q4_K_M)** — запасной вариант: контекст 128k, удобно для длинных глав.
- **XTTS-v2 (Coqui)** — озвучка с клонированием голоса по 10-секундному сэмплу.
- Python-скрипт `translate/translate_book.py` — нарезает книгу на куски и переводит через локальный API.
- Python-скрипт `audio/tts_book.py` — превращает переведённый `.txt` в `.m4b` с разметкой глав.

## Структура

```
.
├── README.md
├── scripts/
│   ├── windows/
│   │   ├── install.ps1
│   │   ├── pull-models.ps1
│   │   └── start-api.ps1
│   └── macos/
│       ├── install.sh
│       ├── pull-models.sh
│       └── start-api.sh
├── modelfiles/
│   ├── translator-qwen.Modelfile
│   ├── translator-nemo.Modelfile
│   └── finance-agent.Modelfile
├── translate/
│   ├── requirements.txt
│   ├── translate_book.py
│   └── config.example.yaml
├── audio/
│   ├── requirements.txt
│   ├── tts_book.py
│   ├── preprocess.py
│   ├── config.example.yaml
│   └── voices/.gitkeep
├── finance/
│   ├── analyze.py
│   ├── config.example.yaml
│   └── requirements.txt
├── docs/
│   ├── financial-agent.md
│   └── claude-code-finance-howto.md
├── .claude/skills/financial-analysis/
└── .gitignore
```

Modelfile-ы платформонезависимые — одинаково собираются и на Windows, и на macOS.

---

## Windows (i7-14700F, 32 ГБ, RTX 3060 12 ГБ)

1. Откройте **PowerShell от имени администратора** в корне репозитория и разрешите выполнение скриптов в сессии:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

2. Поставьте Ollama и убедитесь, что 3060 видна:

   ```powershell
   .\scripts\windows\install.ps1
   ```

3. Скачайте модели и соберите «переводческие» образы:

   ```powershell
   .\scripts\windows\pull-models.ps1
   ```

4. (Опционально) Запустите API руками — обычно достаточно фонового сервиса:

   ```powershell
   .\scripts\windows\start-api.ps1
   ```

### Подсказки по производительности

- План электропитания — **«Высокая производительность»**, иначе p-ядра 14700F троттлят на длинных генерациях.
- 3060 12 ГБ — впритык: закрывайте браузер/игры, иначе VRAM заняется и упадёт скорость.
- Ожидаемая скорость на Qwen2.5 14B Q4_K_M: **20–30 ток/с** на пустом контексте, **8–12 ток/с** ближе к 8k.
- Если ловите `CUDA error: out of memory` — уменьшите `num_ctx` в `modelfiles/translator-qwen.Modelfile` до `4096` и пересоберите образ: `ollama create translator-qwen -f modelfiles\translator-qwen.Modelfile`.

---

## macOS (MacBook Pro M4, 24 ГБ unified)

1. Откройте Terminal в корне репозитория.

2. Поставьте Ollama (через Homebrew или .dmg вручную):

   ```bash
   bash scripts/macos/install.sh
   ```

3. Скачайте модели и соберите образы:

   ```bash
   bash scripts/macos/pull-models.sh
   ```

4. (Опционально) Запустите сервер руками, если не хватает того, что подняла .app:

   ```bash
   bash scripts/macos/start-api.sh
   ```

### Подсказки по производительности

- На Apple Silicon GPU использует общую с CPU память; по умолчанию macOS даёт ~75% RAM. На 24 ГБ это около 18 ГБ — хватает на Qwen2.5 14B Q4_K_M с большим контекстом.
- Если хотите выжать максимум контекста или запускать модель крупнее 14B — поднимите `wired`-лимит:

  ```bash
  sudo sysctl iogpu.wired_limit_mb=20480   # 20 ГБ под GPU
  ```

  Сбрасывается после перезагрузки; чтобы навсегда — пропишите строку в `/etc/sysctl.conf`.
- Скорость на M4 c Qwen2.5 14B Q4_K_M: **порядка 12–18 ток/с**, на маленьких контекстах быстрее.
- Mac удобнее под более жирные кванты: можно поставить `qwen2.5:14b-instruct-q5_K_M` (~10 ГБ) — качество чуть выше.

---

## Перевод книги

Установка зависимостей (одинаковая для обеих ОС, только активация venv разная):

```bash
# macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r translate/requirements.txt
```

```powershell
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r translate\requirements.txt
```

Запуск:

```bash
python translate/translate_book.py \
    --input  ~/books/book.txt \
    --output ~/books/book.ru.txt \
    --model  translator-qwen
```

Особенности скрипта:

- Режет текст по границам абзацев (двойной перевод строки), стараясь уложиться в `--chunk-chars` (по умолчанию 4000 символов).
- После каждого куска сохраняет прогресс в `<output>.progress.json` — при разрыве свяжите запуск через `--resume`.
- Использует `/api/chat`, поэтому уважает системный промпт из Modelfile.

## Озвучка (XTTS-v2)

Превращаем переведённый `.txt` в `.m4b` (или `.mp3`) с клонированием голоса диктора.

> **Лицензия.** XTTS-v2 распространяется под Coqui Public Model License — **только некоммерческое использование**. Для личной аудиокниги «послушать по дороге» — ок, в продакшн или на продажу — нет.

### Подготовка окружения

XTTS-v2 хочет **Python 3.10 или 3.11** (на 3.12 ломаются зависимости) и ffmpeg.

```bash
# macOS
brew install ffmpeg python@3.11
/opt/homebrew/bin/python3.11 -m venv .venv-audio
source .venv-audio/bin/activate
pip install -r audio/requirements.txt
```

```powershell
# Windows
winget install Gyan.FFmpeg
winget install Python.Python.3.11
py -3.11 -m venv .venv-audio
.\.venv-audio\Scripts\Activate.ps1
pip install -r audio\requirements.txt
# Поверх — torch с CUDA (иначе будет CPU-only):
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
```

### Подготовка сэмпла голоса

XTTS клонирует голос по референсной записи. Положите файл в `audio/voices/`:

- один говорящий, без музыки и шумов;
- **6–30 секунд** (оптимум 10–20);
- mono, 24 кГц, 16-bit PCM `.wav`;
- живой говор, разная интонация (не монотонное чтение).

Привести готовую запись к нужному формату:

```bash
ffmpeg -i source.mp3 -ac 1 -ar 24000 -sample_fmt s16 audio/voices/narrator.wav
```

### Запуск

```bash
python audio/tts_book.py \
    --input  book.ru.txt \
    --output book.ru.m4b \
    --voice  audio/voices/narrator.wav \
    --accent
```

Что делает скрипт:

- ищет в тексте строки вида `Глава 1` / `Chapter I` и режет книгу на главы; на выходе `.m4b` с метаданными глав (плеер покажет «12 / 24», можно прыгать);
- разворачивает числа в слова, аббревиатуры (`т.е.`, `г.` и т. п.), приводит тире/кавычки;
- если установлен `ruaccent` и передан `--accent` — расставляет ударения, чтобы XTTS не путал «за́мок/замо́к»;
- кеширует каждое предложение в `book.ru.m4b.cache/` по SHA-сэмпла и текста — упало посередине, перезапустите команду без потерь.

### Сколько это занимает

Оценка для книги ~80k слов (≈10 часов аудио):

- **3060 12 ГБ**: ~3–4 часа реального времени.
- **M4 24 ГБ (MPS)**: ~6–8 часов.
- CPU (`--no-gpu`): сутки и больше, не делайте так.

### Грабли

- Первый запуск тянет модель XTTS-v2 (~2 ГБ) и просит подтвердить лицензию через `COQUI_TOS_AGREED=1`. На неинтерактивной машине задайте переменную: `set COQUI_TOS_AGREED=1` / `export COQUI_TOS_AGREED=1`.
- На длинных предложениях (>240 символов) XTTS склонна «зажёвывать» концовку — поэтому `preprocess.py` режет на чанки <240 символов. Не увеличивайте `--chunk-chars` сверх 280–300.
- Ударения от `ruaccent` не на 100% правильные — для важных имён добавьте `+` вручную: `Бара́баш`.

## Подключение IDE / чат-клиентов

Ollama сразу даёт OpenAI-совместимый эндпоинт:

```
Base URL:  http://localhost:11434/v1
API key:   ollama          (любая непустая строка)
Model:     translator-qwen
```

Этого достаточно для Continue, Cursor, Open WebUI, Raycast AI и т. п.

## Под капотом: настройки в Modelfile

```text
PARAMETER num_ctx 8192
PARAMETER num_gpu 99
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
```

- `num_ctx 8192` — окно контекста; на 12 ГБ VRAM это около 7–8 ГБ суммарно вместе с моделью.
- `num_gpu 99` — оффлоадить все слои на ускоритель (Ollama сама уменьшит, если не влезет).
- Низкая температура и `repeat_penalty 1.1` — стабильный перевод без зацикливаний на длинных текстах.

Mac-пользователи без оглядки на VRAM могут увеличить `num_ctx` до `16384` и пересобрать образ:

```bash
ollama create translator-qwen -f modelfiles/translator-qwen.Modelfile
```

## Финансовый агент (бонус)

Помимо перевода, в репо лежит протокол **финансового агента** для пошагового
анализа публичной компании (фундамент + техника + сентимент) в стиле workflow
`obra/superpowers`:

- `modelfiles/finance-agent.Modelfile` — образ Ollama (Qwen2.5 14B).
- `.claude/skills/financial-analysis/` — 7 фазовых skill-файлов + shared.
- `finance/analyze.py` — Python-конвейер по фазам через локальный Ollama API.
- `docs/financial-agent.md` — методология и best practices.
- `docs/claude-code-finance-howto.md` — инструкция «как готовить и запускать»
  (Claude Code + локальный Ollama, два режима + гибрид).

Быстрый старт после `pull-models.{ps1,sh}`:

```bash
pip install -r finance/requirements.txt
cp finance/config.example.yaml finance/config.yaml
python finance/analyze.py --ticker AAPL
```

Подробности — в `docs/claude-code-finance-howto.md`.

## Известные грабли

- **Windows / winget**: после установки Ollama закройте и заново откройте PowerShell — иначе `ollama` не находится в текущей сессии.
- **Windows / антивирус**: Защитник Windows может тормозить первый запуск — добавьте `%LOCALAPPDATA%\Programs\Ollama` в исключения.
- **macOS / Gatekeeper**: при первом запуске .app может ругаться — System Settings → Privacy & Security → «Open Anyway».
- **macOS / память**: если `ollama` падает с `failed to allocate` — закройте Chrome/Slack и проверьте, что свободно хотя бы 14 ГБ под Qwen 14B.

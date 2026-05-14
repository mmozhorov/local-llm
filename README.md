# Локальная LLM на Windows (i7-14700F, 32 ГБ ОЗУ, RTX 3060 12 ГБ)

Готовый набор скриптов и конфигов, чтобы быстро поднять локальную LLM на Windows-машине с указанным железом и использовать её для перевода книг с английского на русский.

Стек:

- **Ollama** — рантайм для GGUF-моделей с CUDA-ускорением и OpenAI-совместимым API.
- **Qwen2.5 14B Instruct (Q4_K_M)** — основная модель: сильна в русском и в художественном переводе, помещается в 12 ГБ VRAM.
- **Mistral Nemo 12B Instruct (Q4_K_M)** — запасной вариант: контекст 128k, удобно для длинных глав.
- Python-скрипт `translate/translate_book.py` — нарезает книгу на куски и переводит через локальный API.

## Что в репозитории

```
.
├── README.md
├── scripts/
│   ├── install.ps1         # ставит Ollama и проверяет CUDA / NVIDIA-драйвер
│   ├── pull-models.ps1     # скачивает базовые модели и собирает Modelfile-варианты
│   └── start-api.ps1       # запускает Ollama-сервер с нужными параметрами
├── modelfiles/
│   ├── translator-qwen.Modelfile
│   └── translator-nemo.Modelfile
├── translate/
│   ├── requirements.txt
│   ├── translate_book.py   # CLI: txt -> txt (с разбивкой по абзацам)
│   └── config.example.yaml
└── .gitignore
```

## Быстрый старт

1. Откройте **PowerShell от имени администратора** в корне репозитория.

2. Разрешите выполнение скриптов в этой сессии:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

3. Установите Ollama и проверьте, что видеокарта видна:

   ```powershell
   .\scripts\install.ps1
   ```

   Скрипт:
   - проверит наличие NVIDIA-драйвера и `nvidia-smi`;
   - установит Ollama через `winget` (если не установлен);
   - проверит, что сервис `ollama` запускается и видит CUDA.

4. Скачайте модели и создайте «переводческие» варианты с системным промптом:

   ```powershell
   .\scripts\pull-models.ps1
   ```

   По умолчанию тянутся:
   - `qwen2.5:14b-instruct-q4_K_M` (~9 ГБ) — основная;
   - `mistral-nemo:12b-instruct-2407-q4_K_M` (~7 ГБ) — для длинного контекста.

   Из них собираются образы `translator-qwen` и `translator-nemo` с готовым системным промптом для перевода.

5. Запустите API (если он ещё не работает фоновым сервисом):

   ```powershell
   .\scripts\start-api.ps1
   ```

   Ollama слушает `http://localhost:11434`. OpenAI-совместимый эндпоинт: `http://localhost:11434/v1`.

6. Установите Python-зависимости и переведите книгу:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r translate\requirements.txt

   python translate\translate_book.py `
       --input "C:\books\book.txt" `
       --output "C:\books\book.ru.txt" `
       --model translator-qwen
   ```

## Под капотом: настройки под 12 ГБ VRAM

В `modelfiles/translator-qwen.Modelfile`:

- `num_ctx 8192` — окно контекста на инференс (около 7–8 ГБ суммарной VRAM с моделью);
- `num_gpu 99` — оффлоадить все слои на GPU (Ollama сам ограничит, если не влезет);
- `temperature 0.3`, `top_p 0.9` — низкая «креативность», чтобы перевод был стабильным;
- `repeat_penalty 1.1` — гасит зацикливания на длинных текстах.

Если модель не помещается — уменьшите `num_ctx` до `4096` или возьмите `qwen2.5:7b-instruct-q5_K_M`.

## Проверка вручную

```powershell
curl http://localhost:11434/api/generate -d '{
  \"model\": \"translator-qwen\",
  \"prompt\": \"Translate to Russian: The quick brown fox jumps over the lazy dog.\",
  \"stream\": false
}'
```

Или через OpenAI-совместимый эндпоинт (подходит для Continue, Open WebUI, Cursor и т. п.):

```
Base URL:  http://localhost:11434/v1
API key:   ollama          (любая непустая строка)
Model:     translator-qwen
```

## Подсказки по производительности

- На 14700F поставьте план электропитания **«Высокая производительность»**, иначе p-ядра троттлят при долгих генерациях.
- Закройте браузер / игры: 3060 12 ГБ — впритык, любая занятая VRAM портит скорость.
- Скорость на Qwen2.5 14B Q4_K_M ожидается порядка **20–30 ток/с** на пустом контексте и падает к **8–12 ток/с** к 8k.
- Для длинных книг гоняйте перевод **батчами по главам**: `translate_book.py` уже умеет резюмировать с контрольной точки (`--resume`).

## Известные грабли

- `winget` иногда ставит Ollama без перезагрузки PATH — закройте и заново откройте PowerShell.
- Если `ollama run` пишет `CUDA error: out of memory`, уменьшите `num_ctx` в Modelfile и пересоздайте образ: `ollama create translator-qwen -f modelfiles\translator-qwen.Modelfile`.
- Антивирус (особенно Защитник Windows) может тормозить первый запуск — добавьте папку `%LOCALAPPDATA%\Programs\Ollama` в исключения.

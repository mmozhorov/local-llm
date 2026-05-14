#!/usr/bin/env bash
# Ставит Ollama на macOS и проверяет, что хватит памяти под выбранную модель.
# Запускать: bash scripts/macos/install.sh

set -euo pipefail

section() { printf "\n\033[1;36m=== %s ===\033[0m\n" "$1"; }

section "Проверка платформы"
if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "Этот скрипт для macOS. Для Windows используйте scripts/windows/install.ps1." >&2
    exit 1
fi

arch="$(uname -m)"
echo "Архитектура: $arch"
if [[ "$arch" != "arm64" ]]; then
    echo "Предупреждение: Apple Silicon (arm64) не обнаружен. На Intel-Mac Ollama тоже работает, но без Metal-ускорения." >&2
fi

section "Объём оперативной памяти"
mem_bytes="$(sysctl -n hw.memsize)"
mem_gb=$(( mem_bytes / 1024 / 1024 / 1024 ))
echo "Всего памяти: ${mem_gb} ГБ"
if (( mem_gb < 16 )); then
    echo "Меньше 16 ГБ — для 14B моделей не хватит. Возьмите 7-8B в Q4_K_M." >&2
fi

section "Установка Ollama"
if command -v ollama >/dev/null 2>&1; then
    echo "Ollama уже установлена: $(command -v ollama)"
else
    if command -v brew >/dev/null 2>&1; then
        echo "Ставлю через Homebrew..."
        brew install --cask ollama
    else
        echo "Homebrew не найден. Скачайте .dmg вручную: https://ollama.com/download/mac" >&2
        echo "Либо поставьте brew: https://brew.sh" >&2
        exit 1
    fi
fi

section "Версия Ollama"
ollama --version

section "Подсказка"
cat <<'EOF'
Дальше: bash scripts/macos/pull-models.sh

На M-чипах Ollama использует Metal автоматически — никаких драйверов ставить не нужно.
Если будете гонять модели крупнее 14B, имеет смысл поднять лимит «wired» памяти
для GPU (по умолчанию ~75% RAM):

    sudo sysctl iogpu.wired_limit_mb=20480   # пример: 20 ГБ на 24-гиговой машине

Это значение сбрасывается после перезагрузки; для постоянного эффекта добавьте
строку в /etc/sysctl.conf (создайте файл, если его нет).
EOF

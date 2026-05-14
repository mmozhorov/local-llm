#!/usr/bin/env bash
# Запускает Ollama-сервер на 0.0.0.0:11434.
# Обычно на macOS .app сама стартует фоновый сервис — этот скрипт нужен,
# если хотите слушать LAN или поменять параметры окружения.

set -euo pipefail

export OLLAMA_HOST="${OLLAMA_HOST:-0.0.0.0:11434}"
export OLLAMA_KEEP_ALIVE="${OLLAMA_KEEP_ALIVE:-30m}"
export OLLAMA_NUM_PARALLEL="${OLLAMA_NUM_PARALLEL:-1}"

printf "\033[1;36mСтарт Ollama на %s. Ctrl+C — остановить.\033[0m\n" "$OLLAMA_HOST"
exec ollama serve

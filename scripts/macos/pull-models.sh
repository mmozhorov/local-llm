#!/usr/bin/env bash
# Скачивает базовые модели и собирает «переводческие» образы из Modelfile-ов.

set -euo pipefail

section() { printf "\n\033[1;36m=== %s ===\033[0m\n" "$1"; }

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd -- "${script_dir}/../.." && pwd)"

base_models=(
    "qwen2.5:14b-instruct-q4_K_M"
    "mistral-nemo:12b-instruct-2407-q4_K_M"
)

for m in "${base_models[@]}"; do
    section "Скачиваю $m"
    ollama pull "$m"
done

# name -> modelfile path (относительно repo_root)
custom=(
    "translator-qwen:modelfiles/translator-qwen.Modelfile"
    "translator-nemo:modelfiles/translator-nemo.Modelfile"
    "finance-agent:modelfiles/finance-agent.Modelfile"
)

for entry in "${custom[@]}"; do
    name="${entry%%:*}"
    rel="${entry#*:}"
    path="${repo_root}/${rel}"
    if [[ ! -f "$path" ]]; then
        echo "Не найден $path, пропускаю $name." >&2
        continue
    fi
    section "Собираю образ $name из $rel"
    ollama create "$name" -f "$path"
done

section "Итоговый список моделей"
ollama list

section "Готово"
echo "Проверка:"
echo "  ollama run translator-qwen \"Translate to Russian: Hello, world!\""

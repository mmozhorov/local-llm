<#
.SYNOPSIS
  Скачивает базовые модели и собирает «переводческие» варианты из Modelfile-ов.
#>

$ErrorActionPreference = 'Stop'

function Write-Section($msg) {
    Write-Host ""
    Write-Host "=== $msg ===" -ForegroundColor Cyan
}

# Скрипт лежит в scripts/windows/, поэтому корень репозитория — на два уровня выше.
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

$baseModels = @(
    "qwen2.5:14b-instruct-q4_K_M",
    "mistral-nemo:12b-instruct-2407-q4_K_M"
)

foreach ($m in $baseModels) {
    Write-Section "Скачиваю $m"
    & ollama pull $m
}

$customModels = @(
    @{ Name = "translator-qwen"; File = "modelfiles\translator-qwen.Modelfile" },
    @{ Name = "translator-nemo"; File = "modelfiles\translator-nemo.Modelfile" },
    @{ Name = "finance-agent"; File = "modelfiles\finance-agent.Modelfile" }
)

foreach ($cm in $customModels) {
    $path = Join-Path $repoRoot $cm.File
    if (-not (Test-Path $path)) {
        Write-Warning "Не найден $path, пропускаю $($cm.Name)."
        continue
    }
    Write-Section "Собираю образ $($cm.Name) из $($cm.File)"
    & ollama create $cm.Name -f $path
}

Write-Section "Итоговый список моделей"
& ollama list

Write-Section "Готово"
Write-Host "Проверка: ollama run translator-qwen ""Translate to Russian: Hello, world!""" -ForegroundColor Green

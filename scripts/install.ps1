<#
.SYNOPSIS
  Устанавливает Ollama и проверяет, что NVIDIA-драйвер и CUDA доступны.

.DESCRIPTION
  Запускать в PowerShell от имени администратора.
  Поведение:
    1. Проверяет nvidia-smi и пишет версию драйвера.
    2. Если ollama не найден — ставит через winget.
    3. Запускает `ollama --version` и `ollama list`, чтобы убедиться, что сервис стартовал.
#>

$ErrorActionPreference = 'Stop'

function Write-Section($msg) {
    Write-Host ""
    Write-Host "=== $msg ===" -ForegroundColor Cyan
}

Write-Section "Проверка NVIDIA-драйвера"
$nvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if (-not $nvidiaSmi) {
    Write-Warning "nvidia-smi не найден. Установите свежий драйвер NVIDIA (Game Ready или Studio) с https://www.nvidia.com/Download/index.aspx и перезапустите PowerShell."
    exit 1
}
& nvidia-smi | Select-Object -First 15
Write-Host "OK: видеокарта определилась." -ForegroundColor Green

Write-Section "Проверка наличия Ollama"
$ollama = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollama) {
    Write-Host "Ollama не найдена. Ставлю через winget..."
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        Write-Error "winget не найден. Установите App Installer из Microsoft Store или скачайте Ollama вручную: https://ollama.com/download/windows"
        exit 1
    }
    winget install --id Ollama.Ollama --source winget --accept-package-agreements --accept-source-agreements
    Write-Host "Установка завершена. Если ollama не находится в этой сессии — закройте и заново откройте PowerShell." -ForegroundColor Yellow
} else {
    Write-Host "Ollama уже установлена: $($ollama.Source)"
}

Write-Section "Версия Ollama"
& ollama --version

Write-Section "Список моделей (пусто — это нормально на первом запуске)"
try {
    & ollama list
} catch {
    Write-Warning "Не удалось получить список моделей. Возможно, сервис ещё не успел запуститься — подождите пару секунд и попробуйте ещё раз."
}

Write-Section "Готово"
Write-Host "Следующий шаг: .\scripts\pull-models.ps1" -ForegroundColor Green

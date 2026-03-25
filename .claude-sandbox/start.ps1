# start.ps1 — startet die Claude Code Sandbox
# Kein API-Key nötig — Login läuft via Claude.ai (Pro/Max Account)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "🔨  Building sandbox image (nur beim ersten Mal langsam)..." -ForegroundColor Cyan
docker compose build

Write-Host "▶️   Starte Claude Code Sandbox..." -ForegroundColor Cyan
Write-Host "   Beim ersten Mal: URL im Browser öffnen und mit Claude.ai einloggen." -ForegroundColor Yellow
docker compose run --rm claude

# start.ps1 — VolTRE Sandbox launcher
# Kein API-Key nötig — Login läuft via Claude.ai (Pro/Max Account)
#
# Model: the container is a long-running service (PID 1 = tail -f /dev/null), so
# quitting Claude no longer stops it — VSCode can stay attached. Claude sessions
# are launched on demand via `docker exec`, resuming the last conversation.

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$containerName = "voltre-sandbox"

$state = docker inspect --format='{{.State.Status}}' $containerName 2>$null

if ($LASTEXITCODE -ne 0) {
    # Container doesn't exist yet — build image and start it detached
    Write-Host "🔨  Building VolTRE Sandbox image (nur beim ersten Mal langsam)..." -ForegroundColor Cyan
    docker compose build
    Write-Host "🚀  Starting VolTRE Sandbox service..." -ForegroundColor Yellow
    Write-Host "   Beim ersten Mal: URL im Browser öffnen und mit Claude.ai einloggen." -ForegroundColor Yellow
    docker compose up -d
} elseif ($state -ne "running") {
    # Container exists but is stopped — start it (service stays up in background)
    Write-Host "▶️   Resuming VolTRE Sandbox service..." -ForegroundColor Cyan
    docker start $containerName | Out-Null
} else {
    Write-Host "🔗  Sandbox already running." -ForegroundColor Cyan
}

# Attach a Claude session inside the running container.
# `--continue` resumes the most recent conversation in /workspace; on the very
# first run (no history yet) it falls back to a fresh session.
# After /exit you land in the container shell — the container keeps running.
Write-Host "💬  Opening Claude session (resuming last conversation)..." -ForegroundColor Green
docker exec -it $containerName su -s /bin/sh claude -c `
    "claude --continue --dangerously-skip-permissions || claude --dangerously-skip-permissions; exec /bin/sh"

# VolTRE Sandbox

A Docker-based sandbox for running Claude Code against this repo safely.

## Quick Start

From the `.claude-sandbox/` folder in PowerShell:

```powershell
.\start.ps1
```

The script handles all three states automatically:

| Container state | What happens |
|----------------|--------------|
| Doesn't exist | Builds image + creates `voltre-sandbox` (slow first time) |
| Stopped | Resumes the existing container (`docker start -ai`) |
| Running | Opens a new Claude session inside it (`docker exec`) |

## What it does

- Mounts the repo root into `/workspace` inside the container
- Runs Claude Code as a non-root user (`claude`) with `--dangerously-skip-permissions`
- Blocks `git push` via a pre-push hook (so Claude can't push to remote)
- Persists Claude's memory, settings, and conversation state between sessions (see below)

## Persistent State

Claude's home directory (`/home/claude/.claude`) is stored in a named Docker volume called `voltre-claude-sandbox_claude-home`. The container itself is named `voltre-sandbox` and is never auto-deleted, so:

- Memory, project notes, and settings survive container restarts
- You can stop/restart freely without losing Claude's context
- The auth token is refreshed from your host `~/.claude.json` on every start

**To wipe Claude's state and start fresh:**
```powershell
docker rm voltre-sandbox
docker volume rm voltre-claude-sandbox_claude-home
```
The next `.\start.ps1` will rebuild and re-initialize from your host credentials.

## VSCode Attachment

With the container running, attach in VSCode via:
- **Remote Explorer** → **Dev Containers** → `voltre-sandbox` → *Attach to Container*

The container stays alive between Claude sessions, so VSCode can remain attached.

## Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Image definition: Python 3.12, Node 20, Claude Code |
| `docker-compose.yml` | Volume mounts, named volume for persistent state |
| `entrypoint.sh` | Copies credentials, installs push hook, launches Claude |
| `start.ps1` | PowerShell launcher — run this to start the sandbox |

## Rebuilding the image

If you change `Dockerfile`, remove the container and rebuild:
```powershell
docker rm voltre-sandbox
docker compose build
.\start.ps1
```

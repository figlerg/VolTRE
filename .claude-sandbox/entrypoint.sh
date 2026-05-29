#!/bin/sh

cleanup() {
    rm -f /workspace/.git/hooks/pre-push
    echo "🧹  Git push hook removed"
}
trap cleanup EXIT INT TERM

# On first run: copy full .claude config from host to initialize the volume
if [ ! -f /home/claude/.claude/.initialized ]; then
    cp -r /host-claude/. /home/claude/.claude/
    touch /home/claude/.claude/.initialized
    chown -R claude:claude /home/claude/.claude
    echo "✅  First run: credentials + config copied from host"
else
    # On subsequent runs: only refresh the auth token, leave memory intact
    cp /host-claude.json /home/claude/.claude.json 2>/dev/null || true
    chown claude:claude /home/claude/.claude.json 2>/dev/null || true
    echo "✅  Auth token refreshed (state preserved from last session)"
fi

# Hook kopieren
if [ -d "/workspace/.git/hooks" ]; then
    cp /home/claude/.git-templates/hooks/pre-push /workspace/.git/hooks/pre-push
    chmod +x /workspace/.git/hooks/pre-push
    echo "✅  Git push hook installed — pushes are disabled"
else
    echo "⚠️   No .git directory found at /workspace."
fi

# Falls Argument übergeben (z.B. /bin/sh), direkt ausführen
if [ $# -gt 0 ]; then
    echo "🐚  Starting shell as user 'claude'..."
    exec su -s /bin/sh claude -c "$*"
fi

# No args: keep the container alive as a long-running service so VSCode can stay
# attached and Claude sessions are launched on demand via `docker exec`.
# Quitting a Claude session no longer kills the container.
echo "🟢  Sandbox is up and will stay running."
echo "   Launch Claude with start.ps1, or:"
echo "   docker exec -it voltre-sandbox su -s /bin/sh claude -c 'claude --continue'"
# Keep the EXIT/INT/TERM trap active (so the host's pre-push hook is cleaned up
# on `docker stop`) by waiting on a background sleep instead of exec'ing it.
tail -f /dev/null &
wait $!

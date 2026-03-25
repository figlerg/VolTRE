#!/bin/sh

# Hook beim Container-Exit wieder entfernen (Host bleibt sauber)
cleanup() {
    rm -f /workspace/.git/hooks/pre-push
    echo "🧹  Git push hook removed"
}
trap cleanup EXIT INT TERM

# Hook kopieren als root
if [ -d "/workspace/.git/hooks" ]; then
    cp /home/claude/.git-templates/hooks/pre-push /workspace/.git/hooks/pre-push
    chmod +x /workspace/.git/hooks/pre-push
    echo "✅  Git push hook installed — pushes are disabled"
else
    echo "⚠️   No .git directory found at /workspace."
fi

echo "🚀  Starting Claude Code (no-confirm mode) as user 'claude'..."
echo "   (Nach /exit landest du in der Container-Shell)"

# Claude Code starten, danach Shell offen lassen
su -s /bin/sh claude -c "claude --dangerously-skip-permissions; exec /bin/sh"

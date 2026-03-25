#!/bin/sh

cleanup() {
    rm -f /workspace/.git/hooks/pre-push
    echo "🧹  Git push hook removed"
}
trap cleanup EXIT INT TERM

# Credentials vom Host in beschreibbaren Ort kopieren
cp -r /host-claude /home/claude/.claude
cp /host-claude.json /home/claude/.claude.json
chown -R claude:claude /home/claude/.claude
chown claude:claude /home/claude/.claude.json
echo "✅  Credentials kopiert"

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

echo "🚀  Starting Claude Code as user 'claude'..."
echo "   (Nach /exit landest du in der Container-Shell)"
su -s /bin/sh claude -c "claude --dangerously-skip-permissions; exec /bin/sh"

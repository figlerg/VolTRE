FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    git curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code globally
RUN npm install -g @anthropic-ai/claude-code

# Create non-root user (required for --dangerously-skip-permissions)
RUN useradd -m -s /bin/sh claude

# Pre-push hook + git config
RUN mkdir -p /home/claude/.git-templates/hooks && \
    printf '#!/bin/sh\necho "❌  git push is disabled in this sandbox"\nexit 1\n' \
    > /home/claude/.git-templates/hooks/pre-push && \
    chmod +x /home/claude/.git-templates/hooks/pre-push && \
    chown -R claude:claude /home/claude && \
    git config --system init.templateDir /home/claude/.git-templates && \
    git config --system user.email "sandbox@local" && \
    git config --system user.name "Claude Sandbox"

WORKDIR /workspace

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

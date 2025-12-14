# Devcontainer Setup Guide

A complete devcontainer configuration for full-stack development with persistent user data, VS Code extensions caching, and self-healing configuration.

**Last Updated:** 2025-12-13
**Status:** ✅ Validated and Working

---

## Features

- **Python 3.12** with uv package manager
- **Node.js 20** with npm
- **Playwright** with Chromium, Firefox, and WebKit browsers
- **Docker-outside-of-Docker** for container orchestration
- **Claude Code** AI assistant integration
- **Persistent user data** across container rebuilds
- **VS Code extension caching** for faster rebuilds
- **Self-healing symlinks** for VS Code server directories

---

## Architecture

### Volume Strategy

Uses **2 Docker volumes** organized by security sensitivity:

| Volume | Purpose | Contents |
|--------|---------|----------|
| `devcontainer-{project}-vscode` | VS Code tooling (low sensitivity) | Extensions, server cache for both stable and insiders |
| `devcontainer-{project}-user-data` | User data (high sensitivity) | Claude auth, config, bash history |

### Directory Layout

```
/home/vscode/
├── .vscode/                  # Volume mount (tooling)
│   ├── stable/               # VS Code stable server data
│   └── insiders/             # VS Code Insiders server data
├── .vscode-server -> .vscode/stable      # Symlink (created by on-create.sh)
├── .vscode-server-insiders -> .vscode/insiders  # Symlink
├── .persist/                 # Volume mount (user data)
│   ├── claude/               # Claude Code credentials
│   ├── config/               # User configuration
│   └── bash/                 # Bash history
├── .claude -> .persist/claude      # Symlink (created by post-create.sh)
├── .config -> .persist/config      # Symlink
└── .bash_history -> .persist/bash/.bash_history  # Symlink
```

---

## Files

### devcontainer.json

```json
{
  "name": "project-name",
  "image": "mcr.microsoft.com/devcontainers/base:bookworm",
  "features": {
    "ghcr.io/devcontainers/features/docker-outside-of-docker:1": {
      "moby": false,
      "installDockerCompose": true,
      "version": "latest",
      "dockerCompose": "v2"
    },
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20",
      "nodeGypDependencies": true
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.12",
      "installTools": true
    },
    "ghcr.io/va-h/devcontainers-features/uv:1": {
      "version": "latest"
    },
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/anthropics/devcontainer-features/claude-code:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "charliermarsh.ruff",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-playwright.playwright",
        "bradlc.vscode-tailwindcss",
        "tamasfe.even-better-toml",
        "redhat.vscode-yaml",
        "yoavbls.pretty-ts-errors",
        "usernamehw.errorlens",
        "EditorConfig.EditorConfig"
      ],
      "settings": {
        "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
        "python.terminal.activateEnvironment": true,
        "python.testing.pytestEnabled": true,
        "[python]": {
          "editor.defaultFormatter": "charliermarsh.ruff",
          "editor.formatOnSave": true,
          "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
          }
        },
        "[typescript]": {
          "editor.defaultFormatter": "esbenp.prettier-vscode",
          "editor.formatOnSave": true
        },
        "[typescriptreact]": {
          "editor.defaultFormatter": "esbenp.prettier-vscode",
          "editor.formatOnSave": true
        }
      }
    }
  },
  "mounts": [
    "source=devcontainer-project-name-vscode,target=/home/vscode/.vscode,type=volume",
    "source=devcontainer-project-name-user-data,target=/home/vscode/.persist,type=volume"
  ],
  "forwardPorts": [8080, 5173, 8000],
  "portsAttributes": {
    "8080": { "label": "Application", "onAutoForward": "notify" },
    "5173": { "label": "Vite Dev Server", "onAutoForward": "silent" },
    "8000": { "label": "FastAPI Backend", "onAutoForward": "silent" }
  },
  "postCreateCommand": "bash .devcontainer/post-create.sh",
  "remoteUser": "vscode",
  "containerEnv": {
    "PLAYWRIGHT_BROWSERS_PATH": "/home/vscode/.cache/ms-playwright"
  },
  "runArgs": [
    "--init",
    "--shm-size=2gb",
    "--name=devcontainer-project-name"
  ],
  "onCreateCommand": "bash .devcontainer/on-create.sh",
  "initializeCommand": "docker run --rm -v devcontainer-project-name-vscode:/data1 -v devcontainer-project-name-user-data:/data2 alpine sh -c 'mkdir -p /data1/stable /data1/insiders && chown -R 1000:1000 /data1 /data2'"
}
```

### on-create.sh

Runs **before** VS Code server starts. Sets up symlinks for VS Code server directories with self-healing logic.

```bash
#!/bin/bash
# on-create.sh - Runs BEFORE VS Code server starts
# Sets up symlinks for VS Code server directories to persistent volume storage

set -e

echo "=== Setting up VS Code server symlinks ==="

# Function to handle migration and symlink creation
setup_vscode_symlink() {
    local edition="$1"  # "stable" or "insiders"
    local suffix=""
    [ "$edition" = "insiders" ] && suffix="-insiders"

    local dir="$HOME/.vscode-server${suffix}"
    local target="$HOME/.vscode/${edition}"

    # Ensure target directory exists in volume
    mkdir -p "$target"

    # Check if real directory exists (not a symlink)
    if [ -d "$dir" ] && [ ! -L "$dir" ]; then
        # Calculate size of orphaned data
        local size=$(du -sh "$dir" 2>/dev/null | cut -f1 || echo "unknown")

        echo ""
        echo "╔════════════════════════════════════════════════════════════════════╗"
        echo "║  WARNING: Orphaned VS Code server directory detected!              ║"
        echo "╠════════════════════════════════════════════════════════════════════╣"
        echo "║  Location: $dir"
        echo "║  Size: $size"
        echo "║                                                                    ║"
        echo "║  This data was written outside persistent storage and would be    ║"
        echo "║  lost on container rebuild. Migrating to persistent volume...     ║"
        echo "╚════════════════════════════════════════════════════════════════════╝"
        echo ""

        # Migrate contents to volume
        echo "Migrating $dir -> $target ..."
        cp -a "$dir"/. "$target"/ 2>/dev/null || true
        rm -rf "$dir"

        echo "Migration complete."
        echo ""
    fi

    # Remove any existing symlink or empty directory
    rm -rf "$dir" 2>/dev/null || true

    # Create symlink
    ln -sfn "$target" "$dir"
    echo "Symlinked: $dir -> $target"
}

# Set up both VS Code editions
setup_vscode_symlink "stable"
setup_vscode_symlink "insiders"

echo ""
echo "VS Code server symlinks configured."
```

### post-create.sh

Runs **after** container creation. Sets up user data symlinks and installs dependencies.

```bash
#!/bin/bash
set -e

echo "=== Dev Container Setup ==="

# uv is now installed via devcontainer feature
export PATH="$HOME/.local/bin:$PATH"

# Set up symlinks for persistent user data
# These point to the mounted ~/.persist volume which contains sensitive data
echo "Setting up persistent user data symlinks..."
ln -sfn ~/.persist/claude ~/.claude
ln -sfn ~/.persist/config ~/.config
mkdir -p ~/.persist/bash
ln -sf ~/.persist/bash/.bash_history ~/.bash_history

# Install Playwright system dependencies
# Using Playwright's built-in dependency installer (knows exactly what's needed)
echo "Installing Playwright browser dependencies..."
sudo env PATH="$PATH" npx playwright install-deps

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Install Playwright browsers
echo "Installing Playwright browsers..."
npx playwright install chromium firefox webkit

# Initialize backend project if it doesn't exist
if [ ! -d "backend/.venv" ]; then
    echo "Initializing backend project..."
    cd backend

    # Install dependencies using uv
    uv sync

    echo "Backend initialized with dependencies"
    cd ..
else
    echo "Backend already initialized, skipping..."
fi

# Create data directory if it doesn't exist
mkdir -p data

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Environment:"
echo "  Python: $(python3 --version)"
echo "  uv: $(uv --version)"
echo "  Node: $(node --version)"
echo "  Playwright: $(npx playwright --version)"
echo ""
echo "Available commands:"
echo "  npm run test:e2e        - Run Playwright E2E tests"
echo "  npm run test:e2e:ui     - Run tests with Playwright UI"
echo "  cd backend && pytest    - Run backend tests"
echo "  docker compose up       - Start the application"
echo ""
```

---

## Lifecycle Events

The devcontainer lifecycle runs in this order:

1. **initializeCommand** (runs on host, before container exists)
   - Creates volumes with correct permissions
   - Sets up directory structure inside volumes

2. **onCreateCommand** (runs in container, before VS Code starts)
   - Creates symlinks for `.vscode-server` → `.vscode/stable`
   - Creates symlinks for `.vscode-server-insiders` → `.vscode/insiders`
   - Self-heals if orphaned data is detected

3. **postCreateCommand** (runs after container fully created)
   - Sets up user data symlinks (claude, config, bash history)
   - Installs Playwright dependencies and browsers
   - Installs npm dependencies
   - Initializes backend Python environment

---

## What Persists Across Rebuilds

| Item | Persists? | Location |
|------|-----------|----------|
| VS Code extensions | ✅ | `.vscode/` volume |
| Extension settings | ✅ | `.vscode/` volume |
| Claude Code auth | ✅ | `.persist/claude/` |
| User config | ✅ | `.persist/config/` |
| Bash history | ✅ | `.persist/bash/` |
| Project files | ✅ | Workspace bind mount |
| Backend .venv | ✅ | Workspace (but may need recreation) |
| System packages | ❌ | Reinstalled on rebuild |
| Playwright browsers | ❌ | Reinstalled on rebuild |

---

## Maintenance

### View volumes

```bash
docker volume ls | grep devcontainer
```

### Reset user data (start fresh)

```bash
docker volume rm devcontainer-project-name-user-data
```

### Reset VS Code cache (force extension reinstall)

```bash
docker volume rm devcontainer-project-name-vscode
```

### Full reset

```bash
docker volume rm devcontainer-project-name-vscode devcontainer-project-name-user-data
```

---

## Naming Convention

All devcontainer assets use the `devcontainer-` prefix to distinguish from production app resources:

- **Container:** `devcontainer-{project-name}`
- **Volumes:** `devcontainer-{project-name}-vscode`, `devcontainer-{project-name}-user-data`

---

## Troubleshooting

### Problem: Configuration not applied after rebuild

**Cause:** Invalid JSON in devcontainer.json (comments like `// text` are not valid JSON)

**Fix:**
```bash
# Validate JSON syntax
cat .devcontainer/devcontainer.json | python3 -m json.tool > /dev/null && echo "Valid" || echo "Invalid"
```

Remove any `// comments` from the file. Use JSONC-aware editors but ensure the file is valid strict JSON.

### Problem: Backend venv has broken symlinks

**Cause:** Previous session used different Python version

**Fix:**
```bash
rm -rf backend/.venv
# Then rebuild container - post-create.sh will recreate it
```

### Problem: VS Code server data not persisting

**Cause:** Symlinks not created before VS Code started

**Fix:** Ensure `onCreateCommand` runs before `postCreateCommand`. Check that `on-create.sh` has execute permissions.

---

## Key Insights

1. **JSON vs JSONC:** VS Code's editor supports JSONC (JSON with Comments), but the devcontainer CLI uses a strict JSON parser. Never use `// comments` in devcontainer.json.

2. **Lifecycle order matters:** VS Code server directories must be symlinked in `onCreateCommand` (before VS Code starts), not `postCreateCommand`.

3. **Self-healing:** The `on-create.sh` script detects orphaned VS Code directories and migrates them to persistent storage, preventing data loss.

4. **Volume consolidation:** Using 2 volumes (tooling + user data) instead of 4+ volumes simplifies management and aligns with security boundaries.

5. **Named containers:** Using `runArgs` to name the container (`--name=devcontainer-project`) prevents confusion with production containers.

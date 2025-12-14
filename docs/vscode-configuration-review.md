# VS Code Configuration Review

**Date:** 2025-12-13
**Scope:** Container-level vs. Workspace-level settings
**Status:** Needs optimization

---

## 📊 Current Configuration Hierarchy

VS Code settings are applied in this order (lowest to highest priority):

1. **Default Settings** (VS Code built-in)
2. **User Settings** (global, not in repo)
3. **Remote Settings** (container-level) ← `.devcontainer/devcontainer.json`
4. **Workspace Settings** (project-level) ← `.vscode/settings.json`
5. **Folder Settings** (if multi-root workspace)

**Rule:** Workspace settings OVERRIDE container settings.

---

## 🔍 Current State Analysis

### **Container-Level Settings** (`.devcontainer/devcontainer.json`)

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss",
        "ms-playwright.playwright",
        "tamasfe.even-better-toml",
        "yoavbls.pretty-ts-errors"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "[python]": {
          "editor.defaultFormatter": "charliermarsh.ruff",
          "editor.formatOnSave": true
        },
        "[typescript]": {
          "editor.defaultFormatter": "esbenp.prettier-vscode",
          "editor.formatOnSave": true
        },
        "[typescriptreact]": {
          "editor.defaultFormatter": "esbenp.prettier-vscode",
          "editor.formatOnSave": true
        },
        "playwright.reuseBrowser": true,
        "playwright.showTrace": true
      }
    }
  }
}
```

**Purpose:** Settings that should apply to ALL team members in the container.

---

### **Workspace-Level Settings** (`.vscode/settings.json`)

```json
{
  "claudeCode.initialPermissionMode": "bypassPermissions"
}
```

**Purpose:** Project-specific settings that override container defaults.

---

## ⚠️ Issues Identified

### **Issue 1: Python Interpreter Path is Wrong**

**Current:**
```json
"python.defaultInterpreterPath": "/usr/local/bin/python"
```

**Problem:** Backend uses uv virtualenv at `backend/.venv/bin/python`

**Impact:**
- ❌ VS Code Python extension uses system Python (3.9.2)
- ❌ Pylance intellisense won't find installed packages
- ❌ Debugging won't work correctly
- ❌ Test discovery may fail

**Fix Needed:** Point to uv virtualenv

---

### **Issue 2: Missing Test Configuration**

**Current:** No pytest or Vitest configuration

**Impact:**
- ⚠️ VS Code Test Explorer may not discover backend tests
- ⚠️ Frontend unit tests not configured

**Fix Needed:** Add test discovery settings

---

### **Issue 3: Missing Recommended Extensions for Backend**

**Current:** Python extensions installed

**Missing:**
- `donjayamanne.python-environment-manager` (manage virtualenvs)
- `ms-python.debugpy` (debugging support)

---

### **Issue 4: No EditorConfig**

**Current:** Format-on-save configured per language

**Problem:** No unified indentation/line-ending rules

**Impact:**
- ⚠️ Mix of tabs/spaces possible
- ⚠️ Line ending conflicts (CRLF vs LF)

**Fix Needed:** Add `.editorconfig`

---

## ✅ Recommended Configuration

### **1. Container-Level Settings** (for ALL team members)

**What belongs here:**
- ✅ Extensions that everyone needs
- ✅ Language formatter defaults
- ✅ Linter configurations
- ✅ Test framework settings
- ✅ File associations

**What does NOT belong:**
- ❌ User-specific preferences (theme, font size)
- ❌ Machine-specific paths
- ❌ Personal keyboard shortcuts

---

### **2. Workspace-Level Settings** (project-specific overrides)

**What belongs here:**
- ✅ Python interpreter path (points to uv venv)
- ✅ Test discovery patterns
- ✅ Monorepo path mappings
- ✅ Project-specific exclusions

**What does NOT belong:**
- ❌ Duplicates of container settings
- ❌ User preferences

---

## 🎯 Proposed Changes

### **Updated `.devcontainer/devcontainer.json`**

<details>
<summary>Click to expand full configuration</summary>

```json
{
  "name": "rss-remastered",
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
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        // Python
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "charliermarsh.ruff",

        // JavaScript/TypeScript
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",

        // Testing
        "ms-playwright.playwright",

        // Styling
        "bradlc.vscode-tailwindcss",

        // Config files
        "tamasfe.even-better-toml",
        "redhat.vscode-yaml",

        // Developer experience
        "yoavbls.pretty-ts-errors",
        "usernamehw.errorlens",
        "EditorConfig.EditorConfig"
      ],
      "settings": {
        // Python Configuration
        "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
        "python.terminal.activateEnvironment": true,
        "python.testing.pytestEnabled": true,
        "python.testing.pytestArgs": [
          "tests"
        ],
        "python.testing.unittestEnabled": false,
        "python.testing.cwd": "${workspaceFolder}/backend",

        // Python Formatting (Ruff)
        "[python]": {
          "editor.defaultFormatter": "charliermarsh.ruff",
          "editor.formatOnSave": true,
          "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
          }
        },

        // TypeScript/JavaScript Formatting (Prettier)
        "[typescript]": {
          "editor.defaultFormatter": "esbenp.prettier-vscode",
          "editor.formatOnSave": true,
          "editor.codeActionsOnSave": {
            "source.fixAll.eslint": "explicit"
          }
        },
        "[typescriptreact]": {
          "editor.defaultFormatter": "esbenp.prettier-vscode",
          "editor.formatOnSave": true,
          "editor.codeActionsOnSave": {
            "source.fixAll.eslint": "explicit"
          }
        },
        "[javascript]": {
          "editor.defaultFormatter": "esbenp.prettier-vscode",
          "editor.formatOnSave": true
        },
        "[json]": {
          "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "[jsonc]": {
          "editor.defaultFormatter": "esbenp.prettier-vscode"
        },

        // Markdown
        "[markdown]": {
          "editor.formatOnSave": true,
          "editor.wordWrap": "on"
        },

        // Playwright Extension
        "playwright.reuseBrowser": true,
        "playwright.showTrace": true,

        // File Associations
        "files.associations": {
          "*.env.example": "properties",
          "*.env.local": "properties",
          "Dockerfile*": "dockerfile",
          "docker-compose*.yml": "yaml",
          "*.md": "markdown"
        },

        // Editor
        "editor.rulers": [80, 120],
        "editor.bracketPairColorization.enabled": true,
        "editor.guides.bracketPairs": true,
        "editor.suggestSelection": "first",
        "editor.tabSize": 2,
        "editor.insertSpaces": true,
        "editor.detectIndentation": false,

        // Files
        "files.trimTrailingWhitespace": true,
        "files.insertFinalNewline": true,
        "files.eol": "\n",
        "files.exclude": {
          "**/__pycache__": true,
          "**/.pytest_cache": true,
          "**/.ruff_cache": true,
          "**/node_modules": true,
          "**/.venv": true,
          "**/dist": true,
          "**/build": true
        },

        // Search
        "search.exclude": {
          "**/node_modules": true,
          "**/.venv": true,
          "**/dist": true,
          "**/build": true,
          "**/.pytest_cache": true,
          "**/playwright-report": true,
          "**/test-results": true
        },

        // Git
        "git.autofetch": true,
        "git.confirmSync": false,

        // Error Lens (if installed)
        "errorLens.enabledDiagnosticLevels": [
          "error",
          "warning"
        ]
      }
    }
  },
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
    "--shm-size=2gb"
  ]
}
```

</details>

---

### **Updated `.vscode/settings.json`**

```json
{
  // Claude Code
  "claudeCode.initialPermissionMode": "bypassPermissions",

  // Python - Override container default with correct venv path
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",

  // Testing - Workspace-specific paths
  "python.testing.cwd": "${workspaceFolder}/backend",

  // Monorepo-specific exclusions (if needed)
  "files.watcherExclude": {
    "**/backend/.venv/**": true,
    "**/node_modules/**": true
  }
}
```

---

### **New `.editorconfig`**

```ini
# EditorConfig for consistent coding styles
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.{js,ts,jsx,tsx,json,yml,yaml}]
indent_style = space
indent_size = 2

[*.py]
indent_style = space
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

---

### **New `.vscode/extensions.json` (Recommended Extensions)**

```json
{
  "recommendations": [
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
  "unwantedRecommendations": []
}
```

---

## 📋 Configuration Comparison

| Setting | Container | Workspace | Winner | Reason |
|---------|-----------|-----------|--------|--------|
| **Extensions** | ✅ All team extensions | ❌ None | Container | Team-wide |
| **Python Interpreter** | ❌ `/usr/local/bin/python` | ✅ `backend/.venv/bin/python` | Workspace | Project-specific |
| **Format on Save** | ✅ Per language | - | Container | Team standard |
| **Pytest Config** | ✅ Enabled | - | Container | Team-wide |
| **File Exclusions** | ✅ Common patterns | ✅ Project-specific | Both | Complementary |
| **Claude Config** | ❌ Not here | ✅ User preference | Workspace | User-specific |

---

## 🚀 Migration Plan

### **Step 1: Backup Current Settings**

```bash
cp .devcontainer/devcontainer.json .devcontainer/devcontainer.json.backup
cp .vscode/settings.json .vscode/settings.json.backup
```

---

### **Step 2: Update Container Settings**

Update `.devcontainer/devcontainer.json` with:
1. ✅ Correct Python interpreter path
2. ✅ Pytest configuration
3. ✅ Additional recommended extensions
4. ✅ File associations and exclusions
5. ✅ Editor defaults

---

### **Step 3: Minimize Workspace Settings**

Update `.vscode/settings.json` to only include:
1. ✅ Claude Code preferences (user-specific)
2. ✅ Any project-specific overrides

---

### **Step 4: Add EditorConfig**

Create `.editorconfig` for cross-editor consistency.

---

### **Step 5: Add Recommended Extensions**

Create `.vscode/extensions.json` to prompt teammates to install required extensions.

---

### **Step 6: Test**

```bash
# 1. Rebuild container
# Command Palette → "Dev Containers: Rebuild Container"

# 2. Verify Python interpreter
# Command Palette → "Python: Select Interpreter"
# Should show: backend/.venv/bin/python

# 3. Verify test discovery
# Test Explorer should show backend pytest tests

# 4. Verify formatting
# Edit .py file → Save → Should auto-format with Ruff
# Edit .ts file → Save → Should auto-format with Prettier
```

---

## 🎯 Best Practices

### **Container Settings Should:**
- ✅ Define team-wide standards
- ✅ Install all required extensions
- ✅ Configure formatters and linters
- ✅ Set up test frameworks
- ✅ Define file associations

### **Workspace Settings Should:**
- ✅ Override container paths when needed
- ✅ Add project-specific exclusions
- ✅ Configure monorepo mappings
- ✅ Store user preferences (Claude, themes, etc.)

### **Never Put in Either:**
- ❌ API keys or secrets
- ❌ Absolute machine-specific paths
- ❌ User-specific preferences that vary per developer

---

## 📊 Summary

**Current State:**
- ⚠️ Python interpreter path incorrect
- ⚠️ Missing test configuration
- ⚠️ No EditorConfig
- ⚠️ Workspace settings underutilized

**After Migration:**
- ✅ Python interpreter points to uv venv
- ✅ Pytest auto-discovered
- ✅ Consistent formatting via EditorConfig
- ✅ Clear separation of concerns
- ✅ Recommended extensions for team

**Impact:**
- ✅ Better intellisense (correct Python packages)
- ✅ Test discovery works automatically
- ✅ Consistent code style across team
- ✅ Faster onboarding for new developers

---

## 🔗 Reference

**VS Code Settings Precedence:**
1. Default Settings
2. User Settings (global)
3. Remote/Container Settings ← `.devcontainer/devcontainer.json`
4. Workspace Settings ← `.vscode/settings.json`
5. Folder Settings (multi-root only)

**Documentation:**
- [VS Code Settings](https://code.visualstudio.com/docs/getstarted/settings)
- [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [EditorConfig](https://editorconfig.org/)

---

**Next Step:** Review proposed changes and approve migration?

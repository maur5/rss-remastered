# Devcontainer Persistence Guide

**Problem:** Container rebuilds wipe out:
- ❌ Claude Code login/authentication
- ❌ Claude Code settings
- ❌ Conversation history
- ❌ Bash history
- ❌ Git configuration
- ❌ Extension state

**Solution:** Use Docker volumes to persist data across rebuilds.

---

## 📚 Standard Patterns for Persistence

### **Pattern 1: Named Volumes** (Recommended)
- Persist specific directories using Docker named volumes
- Survives container rebuilds
- Managed by Docker

### **Pattern 2: Bind Mounts**
- Mount host directories into container
- Files stored on host machine
- Survives everything (rebuilds, container deletion)

### **Pattern 3: Workspace Storage**
- Store in `/workspaces/<project>/` (already persisted)
- Good for project-specific data
- Not ideal for user settings

---

## 🎯 Solution for Claude Code + VS Code State

### **What to Persist:**

1. **VS Code Server Extensions** (`~/.vscode-server/`)
   - Extension installations
   - Extension state and configuration
   - **Size:** 100-500MB

2. **User Configuration** (`~/.config/`)
   - Claude Code authentication tokens
   - VS Code user settings
   - **Size:** <10MB

3. **Bash History** (`~/.bash_history`)
   - Command history
   - **Size:** <1MB

4. **Git Configuration** (`~/.gitconfig`)
   - Git user settings
   - **Size:** <1KB

---

## ✅ Implementation

### **Step 1: Add Mounts to devcontainer.json**

Add the `mounts` property to persist critical directories:

```json
{
  "name": "rss-remastered",
  "image": "mcr.microsoft.com/devcontainers/base:bookworm",

  // ... features ...

  "mounts": [
    // VS Code Server extensions and state
    "source=rss-remastered-vscode-server,target=/home/vscode/.vscode-server,type=volume",

    // User config (Claude Code auth, settings)
    "source=rss-remastered-config,target=/home/vscode/.config,type=volume",

    // Bash history
    "source=rss-remastered-bashhistory,target=/home/vscode/.bash_history,type=volume",

    // Git config
    "source=rss-remastered-gitconfig,target=/home/vscode/.gitconfig,type=volume"
  ],

  // ... rest of config ...
}
```

---

### **Step 2: Understanding Named Volumes**

**Volume Naming Convention:**
```
{project-name}-{purpose}
```

**Examples:**
- `rss-remastered-vscode-server` - VS Code extensions
- `rss-remastered-config` - User configuration
- `rss-remastered-bashhistory` - Command history

**Location:**
- Volumes are stored by Docker on the host
- Not in your project directory
- Managed by Docker CLI

---

### **Step 3: Verify Volumes**

After rebuild, check volumes exist:

```bash
# List Docker volumes
docker volume ls | grep rss-remastered

# Expected output:
# local     rss-remastered-bashhistory
# local     rss-remastered-config
# local     rss-remastered-gitconfig
# local     rss-remastered-vscode-server

# Inspect a volume
docker volume inspect rss-remastered-config
```

---

## 🎯 Specific Solutions

### **Problem 1: Claude Code Re-Login**

**Where Claude stores auth:**
- Authentication tokens: `~/.config/`
- VS Code extension state: `~/.vscode-server/extensions/`

**Solution:**
```json
"mounts": [
  "source=rss-remastered-config,target=/home/vscode/.config,type=volume",
  "source=rss-remastered-vscode-server,target=/home/vscode/.vscode-server,type=volume"
]
```

**Result:**
- ✅ Stay logged in across rebuilds
- ✅ Extension settings preserved

---

### **Problem 2: Conversation History Loss**

**Claude Code Conversation Storage:**
- Likely in: `~/.config/Code/User/globalStorage/`
- Or: `~/.vscode-server/data/User/globalStorage/`

**Solution:** Same as Problem 1 - persist `~/.config/` and `~/.vscode-server/`

**Result:**
- ✅ Conversation history preserved
- ✅ All extension data persists

---

### **Problem 3: Bash History Lost**

**Solution:**
```json
"mounts": [
  "source=rss-remastered-bashhistory,target=/home/vscode/.bash_history,type=volume"
]
```

**Result:**
- ✅ Command history survives rebuilds
- ✅ Up arrow shows previous commands

---

### **Problem 4: Git Config Reset**

**Solution:**
```json
"mounts": [
  "source=rss-remastered-gitconfig,target=/home/vscode/.gitconfig,type=volume"
]
```

**Alternative:** Use `postCreateCommand` to set git config automatically:

```bash
# .devcontainer/post-create.sh
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

**Recommendation:** Use mount for persistence + post-create as fallback.

---

## ⚠️ Important Caveats

### **Caveat 1: Volumes Persist EVERYTHING**

**Problem:** Corrupted config can survive rebuilds

**Solution:**
```bash
# Nuclear option: Delete volumes to start fresh
docker volume rm rss-remastered-config
docker volume rm rss-remastered-vscode-server

# Then rebuild container
```

---

### **Caveat 2: Extension Updates May Not Apply**

**Problem:** If extensions are cached in volume, updates won't apply

**Solution:**
```json
// In devcontainer.json, force extension reinstall
"updateContentCommand": "code --install-extension ms-python.python --force"
```

Or delete volume manually when you want fresh extensions.

---

### **Caveat 3: Multi-Project Conflicts**

**Problem:** If you use same volume names in multiple projects, they'll share data

**Solution:** Use unique names per project (already doing this with `rss-remastered-` prefix)

---

### **Caveat 4: GitHub Codespaces Incompatibility**

**Problem:** Named volumes don't work well in Codespaces

**Solution for Codespaces:**
```json
// Store in workspace instead
"mounts": [
  "source=${localWorkspaceFolder}/.devcontainer/.persistent-config,target=/home/vscode/.config,type=bind"
]
```

Then add `.devcontainer/.persistent-config/` to `.gitignore`.

---

## 📊 Comparison: Mount Types

| Type | Survives Rebuild | Survives Delete | Where Stored | Use Case |
|------|------------------|-----------------|--------------|----------|
| **Named Volume** | ✅ Yes | ✅ Yes (until manually deleted) | Docker managed | User settings, caches |
| **Bind Mount** | ✅ Yes | ✅ Yes | Host filesystem | Shared configs |
| **tmpfs** | ❌ No | ❌ No | RAM | Temp data |

**Recommendation:** Use **named volumes** for devcontainers (Docker manages cleanup)

---

## 🚀 Complete Configuration

### **Updated `.devcontainer/devcontainer.json`**

```json
{
  "name": "rss-remastered",
  "image": "mcr.microsoft.com/devcontainers/base:bookworm",

  "features": {
    // ... existing features ...
  },

  "mounts": [
    // Persist VS Code Server (extensions, state)
    "source=rss-remastered-vscode-server,target=/home/vscode/.vscode-server,type=volume",

    // Persist user config (Claude Code auth, settings)
    "source=rss-remastered-config,target=/home/vscode/.config,type=volume",

    // Persist bash history
    "source=rss-remastered-bashhistory,target=/home/vscode/.bash_history,type=volume"
  ],

  "customizations": {
    // ... existing customizations ...
  },

  "forwardPorts": [8080, 5173, 8000],
  "portsAttributes": {
    // ... existing port attributes ...
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

---

## 🔍 Verification After Rebuild

### **1. Check Volumes Created**

```bash
docker volume ls | grep rss-remastered
```

**Expected:**
```
local     rss-remastered-bashhistory
local     rss-remastered-config
local     rss-remastered-vscode-server
```

---

### **2. Check Claude Code Still Logged In**

1. Open VS Code
2. Command Palette → "Claude Code: Chat"
3. Should NOT prompt for login ✅

---

### **3. Check Bash History Persists**

```bash
# In terminal, press ↑ arrow
# Should show previous commands ✅
```

---

### **4. Check VS Code Extensions Installed**

```bash
code --list-extensions
```

Should show all extensions WITHOUT reinstalling.

---

## 🧹 Maintenance

### **Clean Up Unused Volumes**

```bash
# List all volumes
docker volume ls

# Remove specific volume (if corrupted)
docker volume rm rss-remastered-config

# Remove all unused volumes (CAUTION!)
docker volume prune
```

---

### **Backup Volumes** (Optional)

```bash
# Backup a volume
docker run --rm \
  -v rss-remastered-config:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/config-backup.tar.gz /data

# Restore a volume
docker run --rm \
  -v rss-remastered-config:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/config-backup.tar.gz -C /
```

---

## 🎯 Recommended Setup for Your Project

### **Minimal (Just Claude Code Persistence):**
```json
"mounts": [
  "source=rss-remastered-vscode-server,target=/home/vscode/.vscode-server,type=volume",
  "source=rss-remastered-config,target=/home/vscode/.config,type=volume"
]
```

### **Standard (Includes Bash History):**
```json
"mounts": [
  "source=rss-remastered-vscode-server,target=/home/vscode/.vscode-server,type=volume",
  "source=rss-remastered-config,target=/home/vscode/.config,type=volume",
  "source=rss-remastered-bashhistory,target=/home/vscode/.bash_history,type=volume"
]
```

### **Complete (All User Data):**
```json
"mounts": [
  "source=rss-remastered-vscode-server,target=/home/vscode/.vscode-server,type=volume",
  "source=rss-remastered-config,target=/home/vscode/.config,type=volume",
  "source=rss-remastered-bashhistory,target=/home/vscode/.bash_history,type=volume",
  "source=rss-remastered-gitconfig,target=/home/vscode/.gitconfig,type=volume",
  "source=rss-remastered-cache,target=/home/vscode/.cache,type=volume"
]
```

**Recommendation:** Use **Standard** setup.

---

## 📚 Additional Resources

- [VS Code: Persist bash history](https://code.visualstudio.com/remote/advancedcontainers/persist-bash-history)
- [VS Code: Dev Container Tips and Tricks](https://code.visualstudio.com/docs/devcontainers/tips-and-tricks)
- [Advanced Dev Container Configuration](https://www.daytona.io/dotfiles/advanced-configuration-techniques-for-dev-container)
- [Docker Data Persistence Guide](https://ricky-lim.github.io/blog/to-mount-or-to-volume-a-guide-to-docker-data-persistence/)

---

## ✅ Summary

**Before:**
- ❌ Claude Code re-login required
- ❌ Settings reset on rebuild
- ❌ Conversation history lost
- ❌ Bash history gone

**After (with mounts):**
- ✅ Stay logged in to Claude Code
- ✅ Settings preserved
- ✅ Conversation history persists
- ✅ Bash history survives
- ✅ Extensions don't reinstall

**Trade-off:**
- ⚠️ Volumes consume disk space
- ⚠️ Need manual cleanup if corrupted
- ⚠️ Extension updates may not auto-apply

**Recommendation:** Accept the trade-off - the productivity gain far outweighs the minor maintenance cost.

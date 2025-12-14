# 🔄 Container Rebuild Checklist

**Quick reference for what survives (and doesn't survive) container rebuilds**

---

## ✅ What NOW Survives Rebuilds (After Mounts Added)

### **Persisted via Docker Volumes:**
- ✅ **Claude Code Authentication** - No re-login needed
- ✅ **Claude Code Settings** - All preferences preserved
- ✅ **Conversation History** - Chat history persists
- ✅ **VS Code Extensions** - Don't reinstall
- ✅ **Extension State** - Settings and data preserved
- ✅ **Bash History** - Command history saved
- ✅ **User Config** - All `~/.config/` data

### **Persisted in Workspace (Always Survived):**
- ✅ **Project Files** - `/workspaces/rss-remastered/`
- ✅ **Git Repo** - All commits, branches
- ✅ **Backend venv** - `backend/.venv/` (recreated via post-create)
- ✅ **node_modules** - Reinstalled via post-create

---

## ❌ What Still Doesn't Survive (By Design)

### **System Packages:**
- ❌ apt-get installed packages (reinstalled on rebuild)
- ❌ Container base image updates

### **Why:** This is intentional - ensures consistent base environment

---

## 🎯 What You'll Notice After First Rebuild

### **Before (Without Mounts):**
```
1. Rebuild container
2. ❌ Claude Code asks for login
3. ❌ Need to reconfigure settings
4. ❌ Conversation history gone
5. ❌ Extensions reinstall (slow)
6. ❌ Bash history empty
```

### **After (With Mounts):**
```
1. Rebuild container
2. ✅ Claude Code already logged in
3. ✅ Settings intact
4. ✅ Conversation history preserved
5. ✅ Extensions already installed (fast)
6. ✅ Bash history accessible (↑ arrow works)
```

---

## 🔍 How to Verify Persistence Working

### **Check 1: Docker Volumes Created**
```bash
docker volume ls | grep rss-remastered
```

**Expected:**
```
rss-remastered-bashhistory
rss-remastered-config
rss-remastered-vscode-server
```

### **Check 2: Claude Code Login Persists**

1. Before rebuild: Note that you're logged in to Claude
2. Rebuild container: Command Palette → "Rebuild Container"
3. After rebuild: Open Claude Code
4. ✅ Should NOT prompt for login

### **Check 3: Bash History Persists**

1. Before rebuild: Run a unique command: `echo "test-$(date +%s)"`
2. Rebuild container
3. After rebuild: Press `↑` arrow
4. ✅ Should show your previous commands

### **Check 4: Extensions Don't Reinstall**

1. Note rebuild time
2. ✅ Should be FASTER than first build (extensions cached)

---

## 🧹 Troubleshooting

### **Problem: Volumes Not Created**

**Check syntax:**
```json
// .devcontainer/devcontainer.json
"mounts": [
  "source=rss-remastered-vscode-server,target=/home/vscode/.vscode-server,type=volume"
]
```

**Verify JSON is valid:**
```bash
cat .devcontainer/devcontainer.json | jq .
```

---

### **Problem: Config Corrupted**

**Nuclear option (start fresh):**
```bash
# Delete all volumes
docker volume rm rss-remastered-config
docker volume rm rss-remastered-vscode-server
docker volume rm rss-remastered-bashhistory

# Rebuild
# Command Palette → "Dev Containers: Rebuild Container"
```

---

### **Problem: Extensions Not Updating**

**Solution:**
```bash
# Delete VS Code Server volume
docker volume rm rss-remastered-vscode-server

# Rebuild - extensions will reinstall fresh
```

---

## 📊 Volume Disk Usage

### **Check Size:**
```bash
docker system df -v | grep rss-remastered
```

**Expected Sizes:**
- `rss-remastered-vscode-server`: ~200-500MB (extensions)
- `rss-remastered-config`: ~1-10MB (settings, auth)
- `rss-remastered-bashhistory`: ~1MB (command history)

**Total:** ~300-600MB (acceptable)

---

## 🔄 When to Clean Up Volumes

### **Scenarios:**

1. **Extension Acting Weird** → Delete `rss-remastered-vscode-server`
2. **Config Corrupted** → Delete `rss-remastered-config`
3. **Disk Space Low** → Delete all, rebuild fresh
4. **Project Deleted** → Clean up manually:

```bash
# After deleting project
docker volume ls | grep rss-remastered
docker volume rm rss-remastered-config
docker volume rm rss-remastered-vscode-server
docker volume rm rss-remastered-bashhistory
```

---

## ⚡ Rebuild Speed Comparison

### **First Build (No Volumes):**
```
1. Pull base image: 2 min
2. Install features: 3 min
3. Run post-create: 2 min
4. Install extensions: 3 min
Total: ~10 minutes
```

### **Rebuild (With Volumes):**
```
1. Pull base image: 2 min (cached)
2. Install features: 3 min
3. Run post-create: 2 min
4. Extensions: <10 sec (cached in volume)
Total: ~7 minutes (30% faster)
```

---

## 🎯 Best Practices

### **DO:**
- ✅ Keep volumes for active projects
- ✅ Delete volumes when deleting project
- ✅ Use unique volume names per project

### **DON'T:**
- ❌ Share volume names across projects
- ❌ Store secrets in volumes (use environment variables)
- ❌ Rely on volumes for backups (use git + external backup)

---

## 📝 Quick Commands

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect rss-remastered-config

# Remove volume
docker volume rm rss-remastered-config

# Clean up ALL unused volumes (CAUTION)
docker volume prune
```

---

## ✅ Success Criteria

After rebuild, you should:
1. ✅ NOT need to log in to Claude Code
2. ✅ See previous bash commands with ↑ arrow
3. ✅ See extensions already installed
4. ✅ See all VS Code settings intact
5. ✅ Rebuild completes faster (~30% faster)

---

**Next rebuild:** Everything should "just work" ✨

For detailed information, see: [devcontainer-persistence-guide.md](devcontainer-persistence-guide.md)

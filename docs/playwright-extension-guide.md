# VS Code Playwright Extension Guide

**Extension:** `ms-playwright.playwright`
**Status:** ✅ Installed and configured
**Browser Location:** `/home/vscode/.cache/ms-playwright/`

---

## ✅ Current Configuration

Your devcontainer is already optimized for the Playwright extension:

```json
// .devcontainer/devcontainer.json
{
  "extensions": ["ms-playwright.playwright"],
  "settings": {
    "playwright.reuseBrowser": true,    // Keeps browser open between runs
    "playwright.showTrace": true        // Auto-shows trace viewer on failure
  },
  "containerEnv": {
    "PLAYWRIGHT_BROWSERS_PATH": "/home/vscode/.cache/ms-playwright"
  },
  "runArgs": ["--shm-size=2gb"]  // Required for browser stability
}
```

---

## 🎯 How to Use the Extension

### **1. Test Explorer (Primary Workflow)**

**Location:** VS Code sidebar → Testing icon (flask/beaker)

**Features:**
- ✅ Tree view of all test files and individual tests
- ✅ Run/Debug buttons on each test
- ✅ Real-time pass/fail status
- ✅ Browser selector (chromium/firefox/webkit)
- ✅ Run in headed/headless mode

**Quick Actions:**
- **Run Test:** Click ▶️ next to test name
- **Debug Test:** Click 🐛 next to test name
- **Run All:** Click ▶️ at top level
- **Run File:** Click ▶️ next to filename

---

### **2. Pick Locators (Codegen)**

**How to Use:**
1. Open any `.spec.ts` file
2. **Command Palette** (Cmd/Ctrl+Shift+P)
3. Type: `Playwright: Pick Locator`
4. Browser opens → Click element you want
5. Locator code copied to clipboard

**Example:**
```typescript
// Before: You need to find the selector
await page.click('???');

// After using Pick Locator:
await page.getByRole('button', { name: 'Subscribe' }).click();
```

---

### **3. Watch Mode (Auto-Run on Save)**

**Enable:**
1. Open Test Explorer
2. Click ⚙️ (settings gear)
3. Enable "Watch Mode"

**Behavior:**
- ✅ Auto-reruns tests when you save `.spec.ts` files
- ✅ Perfect for TDD workflow
- ✅ Shows results immediately

---

### **4. Trace Viewer (Visual Debugger)**

**Automatic on Failure:**
```typescript
// playwright.config.ts (already configured)
use: {
  trace: 'retain-on-failure',  // Auto-captures trace on failure
}
```

**When test fails:**
1. ❌ Test fails in Test Explorer
2. Click "Show trace" in output
3. Trace viewer opens with:
   - 🎬 Video recording of test
   - 📸 Screenshot at failure point
   - 🌳 DOM snapshot at each step
   - 🌐 Network requests
   - 📝 Console logs

**Manual Trace Viewing:**
```bash
npx playwright show-trace test-results/traces/trace.zip
```

---

### **5. Debug with Breakpoints**

**How:**
1. Set breakpoint in `.spec.ts` file (click line number)
2. Click 🐛 Debug button in Test Explorer
3. Browser pauses at breakpoint
4. Use VS Code debugger controls:
   - Step Over (F10)
   - Step Into (F11)
   - Continue (F5)
   - Inspect variables in Debug panel

**Example:**
```typescript
test('debug example', async ({ page }) => {
  await page.goto('/');

  // ⬅️ Set breakpoint here
  const title = await page.title();

  // Execution pauses, inspect `title` in Variables panel
  expect(title).toBe('Expected Title');
});
```

---

## 🔄 Extension vs. CLI Comparison

| Feature | Extension (UI Mode) | CLI (Headless) | Notes |
|---------|-------------------|----------------|-------|
| **Speed** | Slower (headed browser) | Faster (headless) | Extension shows browser visually |
| **Debugging** | ✅ Excellent | Limited | Extension has breakpoints + trace viewer |
| **CI/CD** | ❌ Not available | ✅ Required | CLI is what CI uses |
| **Trace Viewer** | ✅ Auto-opens | Manual | Extension more convenient |
| **Pick Locators** | ✅ Available | ❌ N/A | Extension only |
| **Watch Mode** | ✅ Built-in | Via `--ui` flag | Extension easier |

**Recommendation:**
- **Development:** Use extension (better DX)
- **CI/CD:** Use CLI (automated)
- **Pre-commit:** Run CLI occasionally to match CI environment

---

## ⚠️ Known Gaps & Mitigations

### **Gap 1: Extension Runs Headed, CI Runs Headless**

**Impact:** Different browser rendering behavior

**Mitigation:**
```bash
# Periodically test in headless mode (matches CI)
npm run test:e2e

# If tests pass in extension but fail in CI, debug with:
npx playwright test --headed  # Headed mode via CLI
```

---

### **Gap 2: Extension May Not Detect Config Changes Immediately**

**Impact:** Changes to `playwright.config.ts` not reflected

**Mitigation:**
1. **Command Palette:** `Playwright: Reload Tests`
2. Or restart VS Code

---

### **Gap 3: Extension Browser Cache**

**Impact:** Stale cached data affects tests

**Mitigation:**
```typescript
// Use in test setup to clear state
test.beforeEach(async ({ context }) => {
  await context.clearCookies();
  await context.clearPermissions();
});
```

---

### **Gap 4: Parallel Execution Differences**

**Impact:** Extension runs tests sequentially by default, CLI can run parallel

**Current Config:**
```typescript
// playwright.config.ts
fullyParallel: true,  // CLI runs parallel
workers: process.env.CI ? 1 : undefined,  // CI sequential, local parallel
```

**In Extension:**
- Tests run one at a time by default
- Can enable parallel via settings

---

## 🎯 Best Practices for Extension Use

### **1. Use Test Explorer as Your Primary Interface**

```
✅ DO: Run tests via Test Explorer
❌ DON'T: Run `npm test` manually during dev
```

**Why:** Test Explorer provides:
- Individual test execution
- Instant feedback
- Trace viewer integration
- Breakpoint debugging

---

### **2. Enable Trace on First Run**

```typescript
// playwright.config.ts (already set)
use: {
  trace: 'retain-on-failure',  // ✅ Good for debugging
  // trace: 'on',              // Only if you want trace on success too
}
```

**Why:** Automatic trace capture saves time when tests fail.

---

### **3. Use Pick Locators Instead of Browser DevTools**

```
✅ DO: Use "Pick Locator" command
❌ DON'T: Copy CSS selectors from DevTools
```

**Why:** Playwright locators are more resilient:
- `getByRole('button', { name: 'Submit' })` ← Resilient
- `button.btn-primary.mt-4` ← Brittle

---

### **4. Keep Browser Open Between Runs**

```json
// .devcontainer/devcontainer.json (already set)
"playwright.reuseBrowser": true  // ✅ Faster test iterations
```

**Why:** Browser stays open, tests run faster during dev.

---

### **5. Periodically Run Full Suite via CLI**

```bash
# Before committing code
npm run test:e2e

# Matches CI environment, catches parallel execution issues
```

---

## 🐛 Troubleshooting

### **Extension Not Detecting Tests**

**Symptoms:** Test Explorer shows "No tests found"

**Solutions:**
1. Check `playwright.config.ts` is valid
2. **Command Palette:** `Playwright: Reload Tests`
3. Restart VS Code
4. Verify `testDir` in config matches actual directory

---

### **Browser Won't Launch**

**Symptoms:** "Failed to launch browser"

**Solutions:**
```bash
# 1. Verify browsers installed
npx playwright install chromium --with-deps

# 2. Check shared memory size
docker inspect <container> | grep -i shm  # Should show 2gb

# 3. Check browser location
echo $PLAYWRIGHT_BROWSERS_PATH  # Should be /home/vscode/.cache/ms-playwright
```

---

### **Tests Pass in Extension, Fail in CI**

**Common Causes:**
1. **Timing:** Extension runs slower (headed), may hide race conditions
2. **State:** Extension may reuse browser state between runs
3. **Parallel:** CI runs tests in parallel, extension sequential

**Solution:**
```bash
# Test with CI settings locally
CI=true npm run test:e2e
```

---

### **Trace Viewer Not Opening**

**Symptoms:** Click "Show trace" does nothing

**Solutions:**
1. Verify trace was captured: `ls test-results/traces/`
2. Manually open: `npx playwright show-trace test-results/traces/<file>.zip`
3. Check `playwright.config.ts` has `trace: 'retain-on-failure'`

---

## 📚 Extension Commands

All available via **Command Palette** (Cmd/Ctrl+Shift+P):

| Command | Usage |
|---------|-------|
| `Playwright: Pick Locator` | Generate selectors by clicking elements |
| `Playwright: Record New Test` | Codegen mode - records actions as test code |
| `Playwright: Record at Cursor` | Continue recording from current position |
| `Playwright: Reload Tests` | Refresh Test Explorer |
| `Playwright: Show Trace Viewer` | Open trace for failed test |
| `Playwright: Install Browsers` | Re-install browsers if needed |

---

## 🚀 Recommended Workflow

**Daily Development:**

1. **Open Test Explorer** (sidebar)
2. **Find test** you're working on
3. **Click 🐛 Debug** to run with breakpoints
4. **Set breakpoints** in test code
5. **Use Pick Locator** to find selectors
6. **Watch Mode** enabled for auto-rerun
7. **Trace Viewer** auto-opens on failure

**Before Commit:**

```bash
# Run full suite in CI mode
npm run test:e2e

# Verify all tests pass
```

**CI/CD:**

```yaml
# .github/workflows/test.yml (future)
- run: npm run test:e2e
```

---

## ✅ Verification

Your setup is ready! Try this:

1. **Open Test Explorer** (sidebar → Testing icon)
2. You should see 3 test files:
   - ✅ health.spec.ts (3 tests)
   - ✅ subscriptions.spec.ts (9 tests)
   - ✅ error-recovery.spec.ts (5 tests)
3. **Click ▶️** next to any test
4. Browser opens and test runs
5. On failure, click "Show trace" to debug

---

## 📊 Summary

**Setup Status:** ✅ 100% Ready

**Extension Features Working:**
- ✅ Test Explorer UI
- ✅ Pick Locators
- ✅ Trace Viewer
- ✅ Debug with Breakpoints
- ✅ Watch Mode
- ✅ Browser installed (chromium)

**No Configuration Changes Needed** - Your setup is optimal!

**Gaps Mitigated:**
- ✅ `reuseBrowser: true` for faster dev
- ✅ `showTrace: true` for auto-debugging
- ✅ `PLAYWRIGHT_BROWSERS_PATH` set correctly
- ✅ `--shm-size=2gb` for browser stability

---

**You're ready to use the VS Code Playwright extension as your primary test runner!** 🎉

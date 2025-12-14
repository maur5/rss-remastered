# Test Environment Readiness Assessment
**Date:** 2025-12-13
**Project:** rss-remastered
**Phase:** Pre-Implementation (Phase 2 - Solutioning)

---

## Executive Summary

**Overall Readiness:** 🟡 **PARTIAL** (45% Ready)

**Status:** Your environment has a **solid E2E test foundation** with Playwright, but is **missing critical backend test infrastructure** and several recommended testing tools from the Test Design Report.

**Action Required:** Install missing dependencies before Epic 1 implementation begins.

---

## 1. Current Environment Status

### ✅ **READY - E2E Testing (Frontend)**

| Component | Status | Version | Notes |
|-----------|--------|---------|-------|
| **Node.js** | ✅ Installed | v24.12.0 | ✅ Modern LTS version |
| **npm** | ✅ Installed | 11.6.2 | ✅ Latest |
| **TypeScript** | ✅ Installed | 5.9.3 | ✅ Ready for test development |
| **Playwright** | ✅ Installed | 1.57.0 | ✅ Latest stable (target: 1.49+) |
| **@faker-js/faker** | ✅ Installed | 9.9.0 | ✅ Test data generation ready |
| **Custom Fixtures** | ✅ Created | - | ✅ subscriptionFactory, contentFactory, jobFactory |
| **Test Structure** | ✅ Scaffolded | - | ✅ tests/e2e/, tests/support/ |

**E2E Test Capability:** ✅ **FULLY READY**

**Example Test Execution:**
```bash
npm run test:e2e           # Run all E2E tests
npm run test:e2e:ui        # Playwright UI mode
npm run test:e2e:debug     # Debug mode
```

---

### ❌ **NOT READY - Backend Testing**

| Component | Status | Required For | Priority |
|-----------|--------|--------------|----------|
| **Python 3.11+** | ❌ Only 3.9.2 | Backend development | 🔴 CRITICAL |
| **uv** | ❌ Not installed | Python dependency mgmt | 🔴 CRITICAL |
| **backend/** directory | ❌ Not created | All backend tests | 🔴 CRITICAL |
| **pytest** | ❌ Not installed | Unit + integration tests | 🔴 CRITICAL |
| **pytest-asyncio** | ❌ Not installed | Async test support | 🔴 CRITICAL |
| **httpx** | ❌ Not installed | FastAPI test client | 🔴 CRITICAL |

**Backend Test Capability:** ❌ **NOT READY**

**Impact:** Cannot run backend unit/integration tests until Python environment is set up.

---

### ⚠️ **MISSING - Recommended Testing Tools**

From Test Design Report (TR-001 through TR-008):

#### Backend Tools (Python)
| Tool | Purpose | Test Report Reference | Status |
|------|---------|----------------------|--------|
| **pytest-benchmark** | API latency testing (NFR6) | TR-001 | ❌ Not installed |
| **freezegun** | Retry/backoff time testing | TR-005 | ❌ Not installed |
| **vcrpy** | HTTP recording for external APIs | TR-002 | ❌ Not installed |
| **pytest-vcr** | pytest integration for VCR | TR-002 | ❌ Not installed |
| **textstat** | AI quality metrics (Flesch score) | TR-004 | ❌ Not installed |
| **feedvalidator** | RSS 2.0 compliance (NFR15) | Section 2.3 | ❌ Not installed |

#### Frontend Tools (npm)
| Tool | Purpose | Test Report Reference | Status |
|------|---------|----------------------|--------|
| **@axe-core/playwright** | Accessibility testing (WCAG) | TR-007 | ❌ Not installed |
| **@lhci/cli** | Lighthouse CI (performance) | TR-001 | ❌ Not installed |
| **Vitest** | Frontend unit testing | Architecture | ❌ Not installed |
| **@testing-library/react** | React component testing | Architecture | ❌ Not installed |

---

## 2. Environment Setup Checklist

### Phase 1: Critical Infrastructure (Epic 1)

#### 🔴 **1.1 Python Environment Setup**

**Current:** Python 3.9.2 (below 3.11 requirement)
**Required:** Python 3.11+

```bash
# Check if Python 3.11+ available
python3.11 --version || python3.12 --version

# If not available, install via devcontainer rebuild or:
# Update .devcontainer/devcontainer.json to use Python 3.11+ base image
```

**Action:** Update devcontainer to Python 3.11+ base image

---

#### 🔴 **1.2 Install uv (Python Dependency Manager)**

**Required by:** Architecture specification, all backend development

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

**Expected Output:** `uv 0.x.x` (any recent version)

---

#### 🔴 **1.3 Initialize Backend Project**

**Status:** backend/ directory doesn't exist yet

```bash
# Create backend directory structure
mkdir -p backend/src backend/tests

# Initialize Python project with uv
cd backend
uv init

# Install core dependencies
uv add fastapi sqlalchemy[asyncio] alembic structlog pydantic-settings

# Install test dependencies
uv add --dev pytest pytest-asyncio httpx pytest-cov
```

---

### Phase 2: Performance & Quality Testing (Before Epic 3)

#### 🟡 **2.1 Backend Performance Tools**

**Purpose:** NFR validation (TR-001)

```bash
cd backend
uv add --dev pytest-benchmark
```

**Test:**
```bash
# Should work after installation
pytest --benchmark-only
```

---

#### 🟡 **2.2 External API Mocking Tools**

**Purpose:** Prevent flaky tests, reduce API costs (TR-002, TR-003)

```bash
cd backend
uv add --dev vcrpy pytest-vcr freezegun
```

**Test:**
```python
# tests/conftest.py
@pytest.fixture(scope="module")
def vcr_config():
    return {"record_mode": "once"}
```

---

#### 🟡 **2.3 AI Quality Testing Tools**

**Purpose:** AI transformation quality validation (TR-004)

```bash
cd backend
uv add --dev textstat
```

**Test:**
```python
import textstat
score = textstat.flesch_reading_ease("Test sentence.")
assert score > 60
```

---

#### 🟡 **2.4 RSS Compliance Testing**

**Purpose:** NFR15 validation

```bash
cd backend
uv add --dev feedvalidator
```

---

### Phase 3: Frontend Testing Enhancement (Before Epic 5)

#### 🟡 **3.1 Accessibility Testing**

**Purpose:** WCAG compliance (TR-007)

```bash
npm install --save-dev @axe-core/playwright
```

**Test:**
```typescript
import AxeBuilder from '@axe-core/playwright';

test('page is accessible', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

---

#### 🟡 **3.2 Performance Testing**

**Purpose:** Frontend NFR validation (TR-001)

```bash
npm install --save-dev @lhci/cli
```

**Config:**
```json
// .lighthouserc.json
{
  "ci": {
    "assert": {
      "assertions": {
        "first-contentful-paint": ["error", {"maxNumericValue": 3000}]
      }
    }
  }
}
```

---

#### 🟡 **3.3 Unit Testing Framework**

**Purpose:** Frontend component testing

```bash
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom
```

---

## 3. Docker Environment

### ✅ **Docker Available**

| Component | Status | Version |
|-----------|--------|---------|
| **Docker** | ✅ Installed | 29.1.2-2 |
| **docker-compose** | ⚠️ Check needed | - |

**Verify docker-compose:**
```bash
docker compose version
```

**Expected:** v2.x or higher

---

## 4. Playwright Browser Installation

### ⚠️ **Browsers Status**

**Current:** Browsers may not be installed (dry-run shows download URLs)

**Install all browsers:**
```bash
npx playwright install --with-deps
```

**Install specific browser for faster setup:**
```bash
npx playwright install chromium --with-deps
```

**Verify:**
```bash
npx playwright test --list
```

---

## 5. Test Execution Readiness

### Current Capabilities

| Test Type | Readiness | Executable Command | Status |
|-----------|-----------|-------------------|--------|
| **E2E Tests** | ✅ Ready | `npm run test:e2e` | ✅ Can run (but backend doesn't exist yet) |
| **Backend Unit Tests** | ❌ Not ready | `pytest` | ❌ No backend directory |
| **Backend Integration Tests** | ❌ Not ready | `pytest tests/integration` | ❌ No backend directory |
| **Performance Tests** | ❌ Not ready | `pytest --benchmark-only` | ❌ pytest-benchmark not installed |
| **Accessibility Tests** | ❌ Not ready | `npx playwright test --grep @a11y` | ❌ axe-core not installed |
| **Frontend Unit Tests** | ❌ Not ready | `npm test` | ❌ Vitest not configured |

---

## 6. Priority Action Plan

### 🔴 **IMMEDIATE (Before Epic 1 Development)**

**Goal:** Enable backend development and basic testing

1. **Update Python to 3.11+**
   ```bash
   # Update .devcontainer/devcontainer.json
   # Change: "image": "mcr.microsoft.com/devcontainers/python:3.11"
   # Rebuild container
   ```

2. **Install uv**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source ~/.bashrc  # or restart terminal
   ```

3. **Initialize backend project**
   ```bash
   mkdir -p backend/src backend/tests
   cd backend
   uv init
   uv add fastapi sqlalchemy[asyncio] alembic structlog pydantic-settings
   uv add --dev pytest pytest-asyncio httpx pytest-cov
   ```

4. **Verify backend tests work**
   ```bash
   cd backend
   pytest --version  # Should show pytest version
   ```

**Time Estimate:** 30-45 minutes

---

### 🟡 **HIGH PRIORITY (Before Epic 3)**

**Goal:** Enable external API testing and retry logic validation

5. **Install VCR and time-mocking tools**
   ```bash
   cd backend
   uv add --dev vcrpy pytest-vcr freezegun pytest-benchmark
   ```

6. **Install AI quality tools**
   ```bash
   uv add --dev textstat
   ```

7. **Install RSS validation**
   ```bash
   uv add --dev feedvalidator
   ```

**Time Estimate:** 10 minutes

---

### 🟡 **MEDIUM PRIORITY (Before Epic 5)**

**Goal:** Enable frontend quality testing

8. **Install accessibility testing**
   ```bash
   npm install --save-dev @axe-core/playwright
   ```

9. **Install performance testing**
   ```bash
   npm install --save-dev @lhci/cli
   ```

10. **Install frontend unit testing**
    ```bash
    npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom
    ```

**Time Estimate:** 15 minutes

---

## 7. Verification Commands

Once setup is complete, verify with these commands:

### Backend Verification
```bash
cd backend

# Check Python version
python --version  # Should be 3.11+

# Check uv
uv --version

# Check pytest
pytest --version

# List installed packages
uv pip list | grep -E "(pytest|httpx|sqlalchemy)"

# Run sample test
pytest --collect-only
```

### Frontend Verification
```bash
# Check Node
node --version  # ✅ Already v24.12.0

# Check Playwright
npx playwright --version  # ✅ Already 1.57.0

# List test dependencies
npm list --depth=0 | grep -E "(playwright|faker|axe|lhci|vitest)"

# Run E2E tests (will fail until backend exists)
npm run test:e2e -- --list
```

### Docker Verification
```bash
# Check Docker
docker --version  # ✅ Already 29.1.2-2

# Check docker-compose
docker compose version

# Test Docker build (once Dockerfile exists)
docker compose build
```

---

## 8. Complete Installation Script

**Quick setup script for all tools:**

```bash
#!/bin/bash
# setup-test-environment.sh

set -e

echo "🧪 Setting up rss-remastered test environment..."

# 1. Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11.0"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 3.11+ required (found: $PYTHON_VERSION)"
    echo "Please update .devcontainer/devcontainer.json to use Python 3.11+ base image"
    exit 1
fi

echo "✅ Python version OK: $PYTHON_VERSION"

# 2. Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.cargo/env
fi

echo "✅ uv installed: $(uv --version)"

# 3. Initialize backend if doesn't exist
if [ ! -d "backend" ]; then
    echo "🏗️  Initializing backend project..."
    mkdir -p backend/src backend/tests
    cd backend

    # Initialize project
    uv init --no-readme

    # Core dependencies
    uv add fastapi sqlalchemy[asyncio] alembic structlog pydantic-settings aiosqlite

    # Test dependencies
    uv add --dev pytest pytest-asyncio httpx pytest-cov \
        pytest-benchmark freezegun vcrpy pytest-vcr textstat feedvalidator

    cd ..
fi

echo "✅ Backend initialized"

# 4. Install frontend test tools
echo "📦 Installing frontend test dependencies..."
npm install --save-dev \
    @axe-core/playwright \
    @lhci/cli \
    vitest \
    @testing-library/react \
    @testing-library/jest-dom \
    jsdom

echo "✅ Frontend test tools installed"

# 5. Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
npx playwright install chromium --with-deps

echo "✅ Playwright browsers installed"

# 6. Verification
echo ""
echo "🎉 Test environment setup complete!"
echo ""
echo "Verification:"
echo "  Python: $(python3 --version)"
echo "  uv: $(uv --version)"
echo "  Node: $(node --version)"
echo "  npm: $(npm --version)"
echo "  Playwright: $(npx playwright --version)"
echo ""
echo "Next steps:"
echo "  1. Run backend tests: cd backend && pytest"
echo "  2. Run E2E tests: npm run test:e2e"
echo "  3. Start development: Follow Epic 1 stories"
```

**Usage:**
```bash
chmod +x setup-test-environment.sh
./setup-test-environment.sh
```

---

## 9. Summary & Recommendations

### Current State
- ✅ **E2E infrastructure ready** (Playwright, fixtures, test structure)
- ✅ **Docker available** for integration testing
- ✅ **Node.js modern LTS** version
- ❌ **Backend testing blocked** by Python version and missing uv
- ⚠️ **Quality tools missing** (performance, accessibility, AI testing)

### Recommended Action
**Execute the immediate action plan (Steps 1-4) BEFORE starting Epic 1 development.**

This will unblock:
- Backend project initialization
- Unit test development
- Integration test development
- Database migration testing

### Long-Term
Install remaining tools incrementally:
- **Before Epic 3:** VCR, freezegun, pytest-benchmark (Steps 5-7)
- **Before Epic 5:** axe-core, Lighthouse CI, Vitest (Steps 8-10)

---

## 10. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Python version too old (3.9 vs 3.11) | 🔴 **BLOCKER** | Update devcontainer immediately |
| uv not installed | 🔴 **BLOCKER** | Install before backend init |
| Missing performance tools | 🟡 **MODERATE** | Install before Epic 3 |
| Missing accessibility tools | 🟡 **MODERATE** | Install before Epic 5 |
| Playwright browsers not installed | 🟢 **LOW** | Quick install with `npx playwright install` |

---

**Test Environment Readiness: 45% → Target: 100%**

**Action Required:** Follow the Priority Action Plan to reach 100% readiness.

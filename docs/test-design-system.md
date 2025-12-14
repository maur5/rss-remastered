# System-Level Test Design

**Date:** 2025-12-13
**Author:** Mo (via TEA - Test Architect Agent)
**Status:** Draft
**Phase:** Solutioning (Phase 3 Gate Check)

---

## Executive Summary

This document provides a system-level testability review for rss-remastered, assessing the architecture's fitness for testing and defining the test strategy for implementation. The architecture demonstrates **excellent testability** with no blocking concerns.

---

## Testability Assessment

### Controllability: PASS

The architecture provides excellent controllability for testing:

| Capability | Architecture Support | Testability Impact |
|------------|---------------------|-------------------|
| **API seeding** | FastAPI endpoints (`POST /api/subscriptions`, etc.) | Test data injection via API |
| **Database control** | SQLAlchemy 2.0 async + SQLite | In-memory DB for test isolation |
| **Job queue** | In-process asyncio + SQLite job table | No external Redis dependency |
| **AI abstraction** | Provider protocol with NoOpProvider | Graceful degradation testing |
| **Configuration** | Pydantic Settings (env vars → YAML → DB) | Per-test environment configuration |
| **Factory support** | Domain-based modules | Clear boundaries for test factories |

**Evidence:**
- Architecture specifies domain-based structure (`subscriptions/`, `content/`, `transformations/`) enabling isolated test fixtures
- Job table schema includes `status`, `retries`, `error` fields for queue behavior assertions
- Layered configuration (`RSS_` prefix env vars) enables test-specific overrides

### Observability: PASS

The architecture provides clear observability for test validation:

| Capability | Architecture Support | Testability Impact |
|------------|---------------------|-------------------|
| **Structured logging** | structlog JSON output | Parseable log assertions |
| **Error codes** | `DOMAIN_ACTION_REASON` pattern | Assertion-friendly error checking |
| **Health endpoint** | `/api/health`, `/api/health/ready` | Service status validation |
| **Job status** | `status`, `created_at`, `completed_at`, `error` fields | Transformation pipeline visibility |
| **API responses** | Consistent error format with `detail`, `code`, `context` | Predictable error assertions |

**Evidence:**
- Error code pattern: `SUBSCRIPTION_CREATE_INVALID_URL`, `TRANSFORM_QUEUE_AI_UNAVAILABLE`
- Log format: `{"timestamp": "...", "level": "info", "event": "transformation_started", "job_id": 42}`
- HTTP status codes documented for all scenarios (200, 201, 204, 400, 401, 404, 409, 500)

### Reliability: PASS

The architecture supports reliable, deterministic testing:

| Capability | Architecture Support | Testability Impact |
|------------|---------------------|-------------------|
| **Test isolation** | Domain-based modules | Parallel-safe test execution |
| **Retry mechanism** | Exponential backoff (NFR13) | Retry logic unit testing |
| **Graceful degradation** | NoOpProvider for AI | AI-independent test execution |
| **Single container** | Docker single-container deployment | Simple CI environment setup |
| **Data persistence** | SQLite + Alembic migrations | Version-controlled schema testing |

**Evidence:**
- Architecture: "Each domain (subscriptions, transformations, feeds) gets its own module"
- NFR13: "Automatic retry with exponential backoff for transient failures"
- NoOpProvider: "Returns clear error when AI unconfigured"

---

## Architecturally Significant Requirements (ASRs)

Quality requirements that drive architecture decisions and require explicit test strategy:

### High-Priority ASRs (Score ≥6)

| ASR ID | Category | NFR | Requirement | Prob | Impact | Score | Mitigation |
|--------|----------|-----|-------------|------|--------|-------|------------|
| ASR-1 | PERF | NFR1 | System startup ≤30s | 2 | 3 | **6** | Container startup benchmark in CI |
| ASR-5 | REL | NFR8 | Network failure recovery | 2 | 3 | **6** | Mocked network failure E2E tests |
| ASR-6 | REL | NFR9 | Malformed feed handling | 3 | 2 | **6** | Edge-case feed input integration tests |

### Medium-Priority ASRs (Score 3-5)

| ASR ID | Category | NFR | Requirement | Prob | Impact | Score | Test Approach |
|--------|----------|-----|-------------|------|--------|-------|---------------|
| ASR-2 | PERF | NFR2 | 2GB RAM cap | 2 | 2 | 4 | Memory profiling in CI |
| ASR-3 | PERF | NFR3 | <3s UI initial load | 2 | 2 | 4 | Lighthouse CI gate |
| ASR-4 | PERF | NFR6 | <200ms API response | 2 | 2 | 4 | k6 API latency benchmarks |
| ASR-7 | REL | NFR10 | AI unavailability graceful | 2 | 2 | 4 | NoOpProvider integration tests |
| ASR-9 | INT | NFR15-16 | RSS 2.0 validator compliance | 2 | 2 | 4 | External validator in CI |
| ASR-10 | INT | NFR17-18 | *arr API spec adherence | 2 | 2 | 4 | Contract testing |

### Low-Priority ASRs (Score 1-2)

| ASR ID | Category | NFR | Requirement | Prob | Impact | Score | Test Approach |
|--------|----------|-----|-------------|------|--------|-------|---------------|
| ASR-8 | SEC | NFR22-23 | API key cryptographic security | 1 | 3 | 3 | Security audit, unit tests |

---

## Test Levels Strategy

Based on architecture (FastAPI + Vite + React SPA, SQLite, in-process job queue):

| Level | Target % | Scope | Rationale |
|-------|----------|-------|-----------|
| **Unit** | 50% | Business logic, validators, transformers | Fast feedback, high coverage of domain logic |
| **Integration** | 30% | API endpoints, database ops, job queue | Service boundary validation |
| **E2E** | 20% | Critical user journeys | User experience validation |

### Unit Test Scope

- **Backend (pytest + pytest-asyncio)**:
  - Transformation pipeline logic (`transformations/pipeline.py`)
  - AI provider abstraction (`ai/provider.py`, `ai/openai.py`, `ai/ollama.py`, `ai/noop.py`)
  - Feed parsing and validation (`content/aggregator.py`)
  - RSS generation (`feeds/rss_generator.py`)
  - Configuration parsing (`core/config.py`)
  - Error code generation (`*/exceptions.py`)

- **Frontend (Vitest)**:
  - TanStack Query hooks (`features/*/hooks.ts`)
  - Zustand store logic (`stores/ui.ts`)
  - Utility functions (`lib/utils.ts`)
  - API client (`lib/api.ts`)

### Integration Test Scope

- **Backend (pytest + httpx)**:
  - All API endpoints (`/api/subscriptions`, `/api/content`, `/api/transformations`, etc.)
  - Database operations (SQLAlchemy models, Alembic migrations)
  - Job queue behavior (job creation, status updates, retry logic)
  - Feed fetching and parsing (RSS, YouTube, podcast)
  - AI provider integration (OpenAI, Ollama, NoOp)

- **Frontend (Vitest + MSW)**:
  - API integration (mocked responses via MSW)
  - Component state management (TanStack Query + Zustand integration)

### E2E Test Scope

- **Playwright**:
  - **Marcus journey**: Subscribe → Aggregate → Transform → Consume
  - **Error recovery**: Feed failure → Status indicator → Retry → Success
  - **Sofia journey**: Plex library access, podcast feed consumption
  - **Health monitoring**: Dashboard health summary, feed status indicators

### Test Level Selection Rules

| Scenario | Test Level | Rationale |
|----------|------------|-----------|
| Transformation pipeline logic | Unit | Pure functions, fast feedback |
| AI provider switching | Unit + Integration | Logic (unit) + wiring (integration) |
| API endpoint contracts | Integration | Service boundary validation |
| Database CRUD operations | Integration | Data layer verification |
| Job queue processing | Integration | Async behavior validation |
| User subscription flow | E2E | Multi-page user journey |
| Error recovery UX | E2E | User-facing error handling |
| Feed health status | E2E | Real-time status display |

---

## NFR Testing Approach

### Security (NFR22-26)

| NFR | Test Type | Approach | Tool |
|-----|-----------|----------|------|
| NFR22 | Unit | API key generation uses `secrets.token_urlsafe()` | pytest |
| NFR23 | Unit | API key storage uses bcrypt/argon2 hashing | pytest |
| NFR24 | E2E | Unauthenticated access redirects to login | Playwright |
| NFR25 | Integration | Secrets not exposed in API responses or logs | pytest, log analysis |
| NFR26 | E2E | HTTPS works behind reverse proxy | Playwright |

**Security Test Examples:**
```python
# tests/core/test_api_keys.py
def test_api_key_generation_uses_cryptographic_random():
    key = generate_api_key()
    assert len(key) >= 32  # Sufficient entropy

def test_api_key_stored_hashed():
    key = generate_api_key()
    stored = store_api_key(key)
    assert key not in stored  # Not plaintext
    assert verify_api_key(key, stored)  # Verifiable
```

### Performance (NFR1-7)

| NFR | Test Type | Approach | Tool | Threshold |
|-----|-----------|----------|------|-----------|
| NFR1 | CI | Container startup time measurement | Docker + shell | ≤30s |
| NFR2 | CI | Memory profiling during transformation | pytest-memray | ≤2GB |
| NFR3 | CI | Frontend initial load | Lighthouse CI | ≤3s |
| NFR4 | E2E | Feed list render time | Playwright | ≤1s |
| NFR5 | Integration | Transformation queue acceptance | pytest | ≤500ms |
| NFR6 | Load | API endpoint latency | k6 | p95 ≤200ms |
| NFR7 | Integration | Podcast feed generation | pytest | ≤2s for 100 items |

**k6 Performance Test Example:**
```javascript
// tests/performance/api-latency.k6.js
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<200'],  // NFR6
  },
};

export default function () {
  const response = http.get(`${BASE_URL}/api/subscriptions`);
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
}
```

### Reliability (NFR8-14)

| NFR | Test Type | Approach | Tool |
|-----|-----------|----------|------|
| NFR8 | E2E | Mocked network failure, verify recovery | Playwright (route.abort) |
| NFR9 | Integration | Malformed feed input, verify no crash | pytest with edge-case feeds |
| NFR10 | Integration | AI unavailable, verify fallback behavior | pytest with NoOpProvider |
| NFR11 | Integration | Data persistence across restart | pytest with DB state verification |
| NFR12 | Integration | Failed transformation retry | pytest with job status tracking |
| NFR13 | Unit | Exponential backoff calculation | pytest |
| NFR14 | Integration | Error logging validation | pytest + log capture |

**Reliability Test Example:**
```typescript
// tests/e2e/reliability/network-failure.spec.ts
test('app recovers from network failure', async ({ page, context }) => {
  // Mock network failure
  await context.route('**/api/subscriptions', route => route.abort());

  await page.goto('/subscriptions');

  // Verify error message (not crash)
  await expect(page.getByText('Unable to load subscriptions')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Retry' })).toBeVisible();

  // Restore network
  await context.unroute('**/api/subscriptions');

  await page.getByRole('button', { name: 'Retry' }).click();

  // Verify recovery
  await expect(page.getByText('Unable to load')).not.toBeVisible();
});
```

### Maintainability

| Metric | Target | Enforcement | Tool |
|--------|--------|-------------|------|
| Test coverage (backend) | ≥80% | CI gate | pytest-cov |
| Test coverage (frontend) | ≥70% | CI gate | Vitest coverage |
| Code duplication | <5% | CI warning | jscpd |
| No critical vulnerabilities | 0 | CI gate | npm audit, pip-audit |
| Structured logging | Present | E2E validation | Playwright (trace-id header) |

---

## Test Environment Requirements

### Local Development

| Component | Configuration |
|-----------|---------------|
| Database | SQLite in-memory (`sqlite+aiosqlite:///:memory:`) |
| AI Provider | NoOpProvider (no external dependency) |
| External feeds | Mocked via httpx mock transport |
| Frontend | Vite dev server with MSW |

### CI Environment

| Component | Configuration |
|-----------|---------------|
| Container | Docker with real yt-dlp/FFmpeg |
| Database | SQLite file (persistent for test run) |
| AI Provider | NoOpProvider OR Ollama container |
| External feeds | Mocked OR real test feeds |
| Browser | Playwright browsers (Chromium default) |

### Staging Environment

| Component | Configuration |
|-----------|---------------|
| Container | Production-like Docker image |
| Database | SQLite (representative data volume) |
| AI Provider | Ollama with real model |
| External feeds | Real YouTube/RSS/podcast feeds |
| Browser | Full browser matrix |

---

## Testability Concerns

### No Blocking Concerns

The architecture demonstrates excellent testability with no issues that would block implementation or require architectural changes.

### Minor Concerns (Address in Sprint 0)

| Concern | Impact | Recommendation |
|---------|--------|----------------|
| PWA service worker testing | Low | Configure Playwright for service worker interception |
| YouTube rate limiting | Low | Validate yt-dlp backoff behavior in integration tests |
| Real-time status updates | Low | Polling for MVP; SSE tests when implemented |

---

## Recommendations for Sprint 0

### 1. Initialize Test Framework (`*framework` workflow)

- **Playwright** for E2E with `@seontechnologies/playwright-utils` (config: `tea_use_playwright_utils: true`)
- **pytest + pytest-asyncio + httpx** for backend
- **Vitest** for frontend
- **MSW** for frontend API mocking

### 2. Set Up CI Pipeline (`*ci` workflow)

```yaml
# Recommended CI jobs
jobs:
  unit-tests:
    - pytest backend/tests/unit
    - npm run test:unit (Vitest)

  integration-tests:
    - pytest backend/tests/integration

  e2e-tests:
    - npx playwright test

  performance-tests:
    - k6 run tests/performance/*.k6.js (on merge to main)

  coverage-gate:
    - pytest --cov=src --cov-fail-under=80
    - npm run test:coverage (--coverage.thresholds.lines=70)
```

### 3. Create Test Data Factories

```python
# backend/tests/factories/subscription.py
def create_subscription(**overrides):
    defaults = {
        "name": faker.company(),
        "url": faker.url(),
        "source_type": random.choice(["youtube_channel", "rss_feed", "podcast"]),
        "polling_interval_minutes": 60,
        "status": "active",
    }
    return {**defaults, **overrides}

# backend/tests/factories/job.py
def create_job(**overrides):
    defaults = {
        "task_name": "transform_content",
        "payload": json.dumps({"content_id": faker.uuid4()}),
        "status": "pending",
        "priority": 1,
        "retries": 0,
    }
    return {**defaults, **overrides}
```

### 4. Establish Baseline Tests

**Critical paths to cover in Sprint 0:**

1. **Health check**: `GET /api/health` returns 200
2. **Subscription CRUD**: Create, read, update, delete subscription
3. **Content aggregation**: Fetch and store content from feed
4. **Transformation queue**: Enqueue and process transformation job
5. **Error handling**: API returns proper error codes and messages

---

## Quality Gate Criteria

For solutioning gate check, this test design validates:

- [x] **Controllability** assessed (PASS)
- [x] **Observability** assessed (PASS)
- [x] **Reliability** assessed (PASS)
- [x] **ASRs identified** (3 high-risk, 7 medium-risk)
- [x] **Test levels strategy** defined (50/30/20 split)
- [x] **NFR testing approach** documented
- [x] **Test environment requirements** specified
- [x] **No blocking testability concerns** identified
- [x] **Sprint 0 recommendations** provided

---

## Next Steps

1. **Review this document** with the team
2. **Approve for implementation** (solutioning gate)
3. **Run `*framework` workflow** to initialize test infrastructure
4. **Run `*ci` workflow** to scaffold CI/CD pipeline
5. **Begin Epic 1** with test-first approach

---

**Generated by**: BMad TEA Agent - Test Architect Module
**Workflow**: `.bmad/bmm/testarch/test-design` (System-Level Mode)
**Version**: 4.0 (BMad v6)

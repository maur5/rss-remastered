# rss-remastered E2E Tests

Production-ready Playwright test framework for rss-remastered.

## Quick Start

```bash
# Install dependencies
npm install

# Install Playwright browsers
npx playwright install

# Run tests
npm run test:e2e

# Run tests with UI
npm run test:e2e:ui

# Run tests in headed mode
npm run test:e2e:headed
```

## Prerequisites

1. **Node.js 20+** (see `.nvmrc`)
2. **Application running** at `http://localhost:8080` (or configure `BASE_URL`)

```bash
# Start the application
docker-compose up

# Or for development
cd backend && uv run uvicorn src.main:app --reload --port 8000
cd frontend && npm run dev
```

## Directory Structure

```
tests/
├── e2e/                          # E2E test files
│   ├── health.spec.ts           # Health check tests
│   ├── subscriptions.spec.ts    # Subscription management tests
│   └── error-recovery.spec.ts   # Error handling tests
├── support/                      # Test infrastructure
│   ├── fixtures/                # Playwright fixtures
│   │   ├── index.ts            # Merged fixtures (import this!)
│   │   ├── custom-fixtures.ts  # Project-specific fixtures
│   │   └── factories/          # Data factories
│   │       ├── subscription-factory.ts
│   │       ├── content-factory.ts
│   │       └── job-factory.ts
│   ├── helpers/                 # Utility functions
│   └── page-objects/           # Page object models
└── README.md
```

## Writing Tests

### Import from Merged Fixtures

Always import `test` and `expect` from the merged fixtures:

```typescript
import { test, expect } from '../support/fixtures';

test('my test', async ({ page, subscriptionFactory }) => {
  // All fixtures available
});
```

### Available Fixtures

| Fixture | Description |
|---------|-------------|
| `page` | Playwright page object |
| `request` | API request context |
| `subscriptionFactory` | Create/cleanup subscriptions |
| `contentFactory` | Create/cleanup content items |
| `jobFactory` | Create/cleanup transformation jobs |

### Using Data Factories

Factories create test data via API and automatically clean up after each test:

```typescript
test('subscription test', async ({ subscriptionFactory }) => {
  // Create subscription (auto-cleanup on test end)
  const subscription = await subscriptionFactory.createYouTubeChannel({
    name: 'My Channel',
  });

  expect(subscription.id).toBeTruthy();
  // Cleanup happens automatically!
});
```

### Factory Methods

**SubscriptionFactory:**
- `create(overrides)` - Generic subscription
- `createYouTubeChannel(overrides)` - YouTube channel
- `createRssFeed(overrides)` - RSS feed
- `createPodcast(overrides)` - Podcast

**ContentFactory:**
- `create(overrides)` - Generic content (requires `subscription_id`)
- `createVideo(subscriptionId, overrides)` - Video content
- `createArticle(subscriptionId, overrides)` - Article content
- `createPodcastEpisode(subscriptionId, overrides)` - Podcast episode

**JobFactory:**
- `create(overrides)` - Generic job
- `createTransformationJob(contentId, overrides)` - Transformation job
- `createFeedFetchJob(subscriptionId, overrides)` - Feed fetch job
- `waitForStatus(jobId, status, timeout)` - Wait for job completion

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
BASE_URL=http://localhost:8080    # Application URL
API_URL=http://localhost:8080/api # API base URL
```

### Playwright Config

Key settings in `playwright.config.ts`:

| Setting | Value | Rationale |
|---------|-------|-----------|
| `timeout` | 60s | Full test execution |
| `actionTimeout` | 15s | Click, fill, etc. |
| `navigationTimeout` | 30s | Page navigation |
| `expect.timeout` | 15s | Assertions |
| `retries` | 2 (CI) | Handle flakiness in CI |

### Browser Projects

- `chromium` - Desktop Chrome (default)
- `firefox` - Desktop Firefox
- `webkit` - Desktop Safari
- `mobile-chrome` - Mobile Chrome (Pixel 5)

## Running Tests

```bash
# All tests
npm run test:e2e

# Specific file
npm run test:e2e -- tests/e2e/subscriptions.spec.ts

# Specific test
npm run test:e2e -- -g "can create a YouTube channel"

# With UI (interactive)
npm run test:e2e:ui

# Headed mode
npm run test:e2e:headed

# Specific browser
npm run test:e2e -- --project=firefox

# Debug mode
npm run test:e2e:debug
```

## Test Results

After running tests:

- **HTML Report**: `test-results/html/index.html`
- **JUnit XML**: `test-results/junit.xml` (for CI)
- **Screenshots/Videos**: `test-results/` (failures only)
- **Traces**: `test-results/` (failures only)

View HTML report:
```bash
npx playwright show-report test-results/html
```

## Best Practices

### 1. Use `data-testid` Selectors

```html
<button data-testid="add-subscription">Add</button>
```

```typescript
await page.getByTestId('add-subscription').click();
```

### 2. Network-First Testing

Intercept network calls BEFORE navigation:

```typescript
test('network-first pattern', async ({ page }) => {
  // Setup interception BEFORE navigate
  const responsePromise = page.waitForResponse('**/api/subscriptions');

  await page.goto('/subscriptions');

  // Wait for actual response
  const response = await responsePromise;
  expect(response.ok()).toBeTruthy();
});
```

### 3. No Hard Waits

```typescript
// BAD
await page.waitForTimeout(3000);

// GOOD
await page.waitForResponse('**/api/data');
await expect(page.getByText('Loaded')).toBeVisible();
```

### 4. Test Isolation

Each test should be independent. Use factories for data setup:

```typescript
// Each test gets fresh data
test('test 1', async ({ subscriptionFactory }) => {
  const sub = await subscriptionFactory.create();
  // Auto-cleaned after test
});

test('test 2', async ({ subscriptionFactory }) => {
  const sub = await subscriptionFactory.create();
  // Different data, no conflicts
});
```

### 5. Keep Tests Under 300 Lines

Split large tests into focused scenarios.

## CI Integration

Tests run automatically in CI via GitHub Actions:

```yaml
- name: Run E2E Tests
  run: npm run test:e2e
  env:
    BASE_URL: http://localhost:8080
```

### Parallelization

- Local: Runs in parallel (all workers)
- CI: Runs sequentially (`workers: 1`) for stability

## Playwright Utils Integration

This project uses `@seontechnologies/playwright-utils` for enhanced fixtures:

```typescript
// After installing: npm install -D @seontechnologies/playwright-utils

// Uncomment in tests/support/fixtures/index.ts:
import { test as apiRequestFixture } from '@seontechnologies/playwright-utils/api-request/fixtures';
import { test as recurseFixture } from '@seontechnologies/playwright-utils/recurse/fixtures';
```

Provides:
- `apiRequest` - Typed HTTP client with schema validation
- `recurse` - Polling utility for async conditions
- `interceptNetworkCall` - Network spy/stub
- `log` - Test report logging

## Troubleshooting

### Tests fail with "Page not found"

Ensure the application is running:
```bash
docker-compose up
# or
curl http://localhost:8080/api/health
```

### Tests are flaky

1. Check for hard waits (`waitForTimeout`)
2. Add network interception before navigation
3. Use deterministic assertions

### Cleanup not working

Factories require API endpoints:
- `DELETE /api/subscriptions/:id`
- `DELETE /api/content/:id`
- `POST /api/jobs/:id/cancel`

## Knowledge Base References

- Test quality standards: `.bmad/bmm/testarch/knowledge/test-quality.md`
- Fixture patterns: `.bmad/bmm/testarch/knowledge/fixture-architecture.md`
- Network-first testing: `.bmad/bmm/testarch/knowledge/network-first.md`
- Data factories: `.bmad/bmm/testarch/knowledge/data-factories.md`

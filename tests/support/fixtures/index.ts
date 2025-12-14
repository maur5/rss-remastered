/**
 * Merged Fixtures for rss-remastered E2E Tests
 *
 * Combines @seontechnologies/playwright-utils with custom project fixtures.
 * Import { test, expect } from this file in all test files.
 *
 * Usage:
 *   import { test, expect } from '../support/fixtures';
 *
 *   test('my test', async ({ page, apiRequest, subscriptionFactory }) => {
 *     // All fixtures available
 *   });
 */
import { mergeTests } from '@playwright/test';

// Playwright Utils fixtures (uncomment after npm install)
// import { test as apiRequestFixture } from '@seontechnologies/playwright-utils/api-request/fixtures';
// import { test as recurseFixture } from '@seontechnologies/playwright-utils/recurse/fixtures';
// import { test as networkErrorMonitorFixture } from '@seontechnologies/playwright-utils/network-error-monitor/fixtures';

// Custom project fixtures
import { test as customFixtures } from './custom-fixtures';

// Merge all fixtures into single test object
// When playwright-utils is installed, add: apiRequestFixture, recurseFixture, networkErrorMonitorFixture
export const test = mergeTests(customFixtures);

export { expect } from '@playwright/test';

/**
 * Error Recovery Tests
 *
 * Tests for NFR8, NFR9, NFR10: Graceful degradation and error handling.
 * Validates the application handles failures without crashing.
 */
import { test, expect } from '../support/fixtures';

test.describe('Error Recovery', () => {
  test('app remains functional when API returns 500 error', async ({ page, context }) => {
    // Mock API failure
    await context.route('**/api/subscriptions', (route) => {
      route.fulfill({
        status: 500,
        body: JSON.stringify({ error: 'Internal Server Error' }),
      });
    });

    await page.goto('/subscriptions');

    // User sees error message (not crash or blank page)
    await expect(page.getByText(/unable to load|error|failed/i)).toBeVisible();

    // Retry button should be available
    await expect(page.getByRole('button', { name: /retry/i })).toBeVisible();

    // Navigation still works
    await page.getByRole('link', { name: /home|dashboard/i }).click();
    await expect(page).toHaveURL(/\/(dashboard)?$/);
  });

  test('app handles network disconnection gracefully', async ({ page, context }) => {
    await page.goto('/dashboard');

    // Simulate offline mode
    await context.setOffline(true);

    // Trigger action requiring network
    const refreshButton = page.getByRole('button', { name: /refresh|reload/i });
    if (await refreshButton.isVisible()) {
      await refreshButton.click();

      // User sees offline indicator
      await expect(page.getByText(/offline|no connection|network error/i)).toBeVisible();
    }

    // Reconnect
    await context.setOffline(false);
  });

  test('handles malformed API response gracefully', async ({ page, context }) => {
    // Mock malformed JSON response
    await context.route('**/api/subscriptions', (route) => {
      route.fulfill({
        status: 200,
        body: 'not valid json',
        contentType: 'application/json',
      });
    });

    await page.goto('/subscriptions');

    // App should handle parse error gracefully
    await expect(page.getByText(/error|failed|unable/i)).toBeVisible();
  });

  test('displays actionable error messages', async ({ page, context }) => {
    // Mock specific error
    await context.route('**/api/subscriptions', (route) => {
      route.fulfill({
        status: 400,
        body: JSON.stringify({
          detail: 'Invalid subscription URL format',
          code: 'SUBSCRIPTION_CREATE_INVALID_URL',
        }),
      });
    });

    await page.goto('/subscriptions/new');

    // Try to submit invalid data
    await page.getByLabel(/url/i).fill('not-a-valid-url');
    await page.getByRole('button', { name: /save|submit|add/i }).click();

    // Error message should be user-friendly
    const errorMessage = page.getByRole('alert');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText(/invalid|url|format/i);
  });

  test('retry mechanism works after transient failure', async ({ page, context }) => {
    let attemptCount = 0;

    // Mock transient failure (fail first 2 times, succeed on 3rd)
    await context.route('**/api/subscriptions', (route) => {
      attemptCount++;
      if (attemptCount < 3) {
        route.fulfill({
          status: 503,
          body: JSON.stringify({ error: 'Service Unavailable' }),
        });
      } else {
        route.fulfill({
          status: 200,
          body: JSON.stringify([]),
        });
      }
    });

    await page.goto('/subscriptions');

    // First attempt fails
    await expect(page.getByText(/error|unable|failed/i)).toBeVisible();

    // Click retry
    await page.getByRole('button', { name: /retry/i }).click();

    // May need another retry
    if (await page.getByRole('button', { name: /retry/i }).isVisible()) {
      await page.getByRole('button', { name: /retry/i }).click();
    }

    // Eventually succeeds - error message disappears
    await expect(page.getByText(/error|unable|failed/i)).not.toBeVisible({ timeout: 5000 });
  });
});

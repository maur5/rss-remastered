/**
 * Health Check Tests
 *
 * Verifies the application health endpoint is working correctly.
 * This is the first test to run - validates basic connectivity.
 */
import { test, expect } from '../support/fixtures';

test.describe('Health Check', () => {
  test('API health endpoint returns healthy status', async ({ request }) => {
    const response = await request.get('/api/health');

    expect(response.status()).toBe(200);

    const health = await response.json();
    expect(health).toHaveProperty('status', 'healthy');
  });

  test('API health endpoint includes service details', async ({ request }) => {
    const response = await request.get('/api/health');

    expect(response.ok()).toBeTruthy();

    const health = await response.json();
    expect(health).toHaveProperty('timestamp');

    // If services are monitored, verify they're reported
    if (health.services) {
      expect(health.services).toHaveProperty('database');
    }
  });

  test('homepage loads successfully', async ({ page }) => {
    await page.goto('/');

    // Wait for the app to hydrate
    await expect(page.locator('body')).toBeVisible();

    // Basic smoke test - page should have content
    const pageContent = await page.content();
    expect(pageContent.length).toBeGreaterThan(100);
  });
});

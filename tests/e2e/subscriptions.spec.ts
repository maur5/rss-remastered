/**
 * Subscription Management Tests
 *
 * Tests for FR1-FR9: Subscription CRUD operations.
 * Uses the subscriptionFactory fixture for data setup and cleanup.
 */
import { test, expect } from '../support/fixtures';

test.describe('Subscription Management', () => {
  test.describe('API Operations', () => {
    test('can create a YouTube channel subscription via API', async ({ request, subscriptionFactory }) => {
      const subscription = await subscriptionFactory.createYouTubeChannel({
        name: 'Test YouTube Channel',
      });

      expect(subscription.id).toBeTruthy();
      expect(subscription.name).toBe('Test YouTube Channel');
      expect(subscription.source_type).toBe('youtube_channel');
      expect(subscription.status).toBe('active');

      // Verify it was persisted
      const response = await request.get(`/api/subscriptions/${subscription.id}`);
      expect(response.status()).toBe(200);

      const fetched = await response.json();
      expect(fetched.id).toBe(subscription.id);
    });

    test('can create an RSS feed subscription via API', async ({ subscriptionFactory }) => {
      const subscription = await subscriptionFactory.createRssFeed({
        name: 'Test RSS Feed',
        polling_interval_minutes: 30,
      });

      expect(subscription.source_type).toBe('rss_feed');
      expect(subscription.polling_interval_minutes).toBe(30);
    });

    test('can create a podcast subscription via API', async ({ subscriptionFactory }) => {
      const subscription = await subscriptionFactory.createPodcast({
        name: 'Test Podcast',
        tags: ['tech', 'news'],
      });

      expect(subscription.source_type).toBe('podcast');
      expect(subscription.tags).toContain('tech');
      expect(subscription.tags).toContain('news');
    });

    test('can list all subscriptions', async ({ request, subscriptionFactory }) => {
      // Create multiple subscriptions
      await subscriptionFactory.createYouTubeChannel({ name: 'Channel 1' });
      await subscriptionFactory.createRssFeed({ name: 'Feed 1' });
      await subscriptionFactory.createPodcast({ name: 'Podcast 1' });

      const response = await request.get('/api/subscriptions');
      expect(response.status()).toBe(200);

      const subscriptions = await response.json();
      expect(subscriptions.length).toBeGreaterThanOrEqual(3);
    });

    test('can update subscription settings', async ({ request, subscriptionFactory }) => {
      const subscription = await subscriptionFactory.createRssFeed({
        name: 'Original Name',
        polling_interval_minutes: 60,
      });

      const response = await request.patch(`/api/subscriptions/${subscription.id}`, {
        data: {
          name: 'Updated Name',
          polling_interval_minutes: 120,
        },
      });

      expect(response.status()).toBe(200);

      const updated = await response.json();
      expect(updated.name).toBe('Updated Name');
      expect(updated.polling_interval_minutes).toBe(120);
    });

    test('can delete a subscription', async ({ request, subscriptionFactory }) => {
      const subscription = await subscriptionFactory.createRssFeed();

      const deleteResponse = await request.delete(`/api/subscriptions/${subscription.id}`);
      expect(deleteResponse.status()).toBe(204);

      // Verify deletion
      const getResponse = await request.get(`/api/subscriptions/${subscription.id}`);
      expect(getResponse.status()).toBe(404);
    });
  });

  test.describe('UI Operations', () => {
    test('can view subscription list in UI', async ({ page, subscriptionFactory }) => {
      // Create test data via API
      const subscription = await subscriptionFactory.createYouTubeChannel({
        name: 'E2E Test Channel',
      });

      // Navigate to subscriptions page
      await page.goto('/subscriptions');

      // Verify subscription appears in list
      await expect(page.getByText('E2E Test Channel')).toBeVisible();
    });

    test('can add subscription via UI form', async ({ page }) => {
      await page.goto('/subscriptions');

      // Click add button
      await page.getByRole('button', { name: /add subscription/i }).click();

      // Fill form
      await page.getByLabel(/url/i).fill('https://www.youtube.com/channel/UCtest123');
      await page.getByLabel(/name/i).fill('UI Test Channel');

      // Submit
      await page.getByRole('button', { name: /save|submit|add/i }).click();

      // Verify success message or redirect
      await expect(page.getByText(/created|added|success/i)).toBeVisible();
    });

    test('displays subscription health status', async ({ page, subscriptionFactory }) => {
      const subscription = await subscriptionFactory.createRssFeed({
        name: 'Health Status Test',
      });

      await page.goto('/subscriptions');

      // Find subscription card
      const subscriptionCard = page.locator(`[data-subscription-id="${subscription.id}"]`);

      // Verify health indicator is present
      await expect(subscriptionCard.locator('[data-testid="health-status"]')).toBeVisible();
    });
  });
});

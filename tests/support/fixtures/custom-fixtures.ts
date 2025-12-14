/**
 * Custom Fixtures for rss-remastered
 *
 * Project-specific fixtures that integrate with the application's API.
 * All fixtures include auto-cleanup via the use() pattern.
 */
import { test as base, APIRequestContext } from '@playwright/test';
import { SubscriptionFactory } from './factories/subscription-factory';
import { ContentFactory } from './factories/content-factory';
import { JobFactory } from './factories/job-factory';

type CustomFixtures = {
  /** Factory for creating and cleaning up subscriptions */
  subscriptionFactory: SubscriptionFactory;
  /** Factory for creating and cleaning up content items */
  contentFactory: ContentFactory;
  /** Factory for creating and cleaning up transformation jobs */
  jobFactory: JobFactory;
  /** API request context pre-configured with base URL */
  apiContext: APIRequestContext;
};

export const test = base.extend<CustomFixtures>({
  // API context fixture - provides pre-configured request context
  apiContext: async ({ request }, use) => {
    await use(request);
  },

  // Subscription factory with auto-cleanup
  subscriptionFactory: async ({ apiContext }, use) => {
    const factory = new SubscriptionFactory(apiContext);
    await use(factory);
    await factory.cleanup();
  },

  // Content factory with auto-cleanup
  contentFactory: async ({ apiContext }, use) => {
    const factory = new ContentFactory(apiContext);
    await use(factory);
    await factory.cleanup();
  },

  // Job factory with auto-cleanup
  jobFactory: async ({ apiContext }, use) => {
    const factory = new JobFactory(apiContext);
    await use(factory);
    await factory.cleanup();
  },
});

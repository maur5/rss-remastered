/**
 * Subscription Factory
 *
 * Creates test subscriptions via API with auto-cleanup.
 * Uses faker for unique data to enable parallel test execution.
 */
import { APIRequestContext } from '@playwright/test';
import { faker } from '@faker-js/faker';

export type SourceType = 'youtube_channel' | 'rss_feed' | 'podcast';

export type Subscription = {
  id: string;
  name: string;
  url: string;
  source_type: SourceType;
  icon_url: string | null;
  polling_interval_minutes: number;
  status: 'active' | 'paused' | 'error';
  tags: string[];
  created_at: string;
  updated_at: string;
};

export type CreateSubscriptionInput = Partial<{
  name: string;
  url: string;
  source_type: SourceType;
  icon_url: string | null;
  polling_interval_minutes: number;
  tags: string[];
}>;

export class SubscriptionFactory {
  private createdIds: string[] = [];
  private baseUrl: string;

  constructor(private request: APIRequestContext) {
    this.baseUrl = process.env.API_URL || 'http://localhost:8080/api';
  }

  /**
   * Create a subscription with optional overrides
   */
  async create(overrides: CreateSubscriptionInput = {}): Promise<Subscription> {
    const sourceType = overrides.source_type || faker.helpers.arrayElement(['youtube_channel', 'rss_feed', 'podcast']);

    const defaults: CreateSubscriptionInput = {
      name: faker.company.name(),
      url: this.generateUrlForType(sourceType),
      source_type: sourceType,
      icon_url: faker.image.url(),
      polling_interval_minutes: 60,
      tags: [faker.word.noun()],
    };

    const data = { ...defaults, ...overrides };

    const response = await this.request.post(`${this.baseUrl}/subscriptions`, {
      data,
    });

    if (!response.ok()) {
      const error = await response.text();
      throw new Error(`Failed to create subscription: ${response.status()} ${error}`);
    }

    const subscription = (await response.json()) as Subscription;
    this.createdIds.push(subscription.id);
    return subscription;
  }

  /**
   * Create a YouTube channel subscription
   */
  async createYouTubeChannel(overrides: CreateSubscriptionInput = {}): Promise<Subscription> {
    return this.create({
      source_type: 'youtube_channel',
      url: `https://www.youtube.com/channel/${faker.string.alphanumeric(24)}`,
      ...overrides,
    });
  }

  /**
   * Create an RSS feed subscription
   */
  async createRssFeed(overrides: CreateSubscriptionInput = {}): Promise<Subscription> {
    return this.create({
      source_type: 'rss_feed',
      url: `https://${faker.internet.domainName()}/feed.xml`,
      ...overrides,
    });
  }

  /**
   * Create a podcast subscription
   */
  async createPodcast(overrides: CreateSubscriptionInput = {}): Promise<Subscription> {
    return this.create({
      source_type: 'podcast',
      url: `https://${faker.internet.domainName()}/podcast.xml`,
      ...overrides,
    });
  }

  /**
   * Clean up all created subscriptions
   */
  async cleanup(): Promise<void> {
    for (const id of this.createdIds) {
      try {
        await this.request.delete(`${this.baseUrl}/subscriptions/${id}`);
      } catch {
        // Ignore cleanup errors (resource may already be deleted)
      }
    }
    this.createdIds = [];
  }

  private generateUrlForType(sourceType: SourceType): string {
    switch (sourceType) {
      case 'youtube_channel':
        return `https://www.youtube.com/channel/${faker.string.alphanumeric(24)}`;
      case 'rss_feed':
        return `https://${faker.internet.domainName()}/feed.xml`;
      case 'podcast':
        return `https://${faker.internet.domainName()}/podcast.xml`;
    }
  }
}

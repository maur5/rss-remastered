/**
 * Content Factory
 *
 * Creates test content items via API with auto-cleanup.
 * Requires a subscription to exist first.
 */
import { APIRequestContext } from '@playwright/test';
import { faker } from '@faker-js/faker';

export type ContentType = 'video' | 'article' | 'podcast_episode';

export type ContentItem = {
  id: string;
  subscription_id: string;
  external_id: string;
  title: string;
  description: string;
  url: string;
  content_type: ContentType;
  published_at: string;
  duration_seconds: number | null;
  thumbnail_url: string | null;
  is_read: boolean;
  created_at: string;
};

export type CreateContentInput = Partial<{
  subscription_id: string;
  external_id: string;
  title: string;
  description: string;
  url: string;
  content_type: ContentType;
  published_at: string;
  duration_seconds: number | null;
  thumbnail_url: string | null;
}>;

export class ContentFactory {
  private createdIds: string[] = [];
  private baseUrl: string;

  constructor(private request: APIRequestContext) {
    this.baseUrl = process.env.API_URL || 'http://localhost:8080/api';
  }

  /**
   * Create a content item with optional overrides
   */
  async create(overrides: CreateContentInput = {}): Promise<ContentItem> {
    if (!overrides.subscription_id) {
      throw new Error('subscription_id is required to create content');
    }

    const contentType = overrides.content_type || faker.helpers.arrayElement(['video', 'article', 'podcast_episode']);

    const defaults: CreateContentInput = {
      external_id: faker.string.alphanumeric(11),
      title: faker.lorem.sentence(),
      description: faker.lorem.paragraph(),
      url: `https://example.com/content/${faker.string.alphanumeric(10)}`,
      content_type: contentType,
      published_at: faker.date.recent().toISOString(),
      duration_seconds: contentType === 'article' ? null : faker.number.int({ min: 60, max: 7200 }),
      thumbnail_url: faker.image.url(),
    };

    const data = { ...defaults, ...overrides };

    const response = await this.request.post(`${this.baseUrl}/content`, {
      data,
    });

    if (!response.ok()) {
      const error = await response.text();
      throw new Error(`Failed to create content: ${response.status()} ${error}`);
    }

    const content = (await response.json()) as ContentItem;
    this.createdIds.push(content.id);
    return content;
  }

  /**
   * Create a video content item
   */
  async createVideo(subscriptionId: string, overrides: CreateContentInput = {}): Promise<ContentItem> {
    return this.create({
      subscription_id: subscriptionId,
      content_type: 'video',
      duration_seconds: faker.number.int({ min: 300, max: 3600 }),
      ...overrides,
    });
  }

  /**
   * Create an article content item
   */
  async createArticle(subscriptionId: string, overrides: CreateContentInput = {}): Promise<ContentItem> {
    return this.create({
      subscription_id: subscriptionId,
      content_type: 'article',
      duration_seconds: null,
      ...overrides,
    });
  }

  /**
   * Create a podcast episode content item
   */
  async createPodcastEpisode(subscriptionId: string, overrides: CreateContentInput = {}): Promise<ContentItem> {
    return this.create({
      subscription_id: subscriptionId,
      content_type: 'podcast_episode',
      duration_seconds: faker.number.int({ min: 600, max: 7200 }),
      ...overrides,
    });
  }

  /**
   * Clean up all created content items
   */
  async cleanup(): Promise<void> {
    for (const id of this.createdIds) {
      try {
        await this.request.delete(`${this.baseUrl}/content/${id}`);
      } catch {
        // Ignore cleanup errors
      }
    }
    this.createdIds = [];
  }
}

/**
 * Job Factory
 *
 * Creates test transformation jobs via API with auto-cleanup.
 * Used for testing the transformation pipeline.
 */
import { APIRequestContext } from '@playwright/test';
import { faker } from '@faker-js/faker';

export type JobStatus = 'pending' | 'running' | 'completed' | 'failed';

export type Job = {
  id: string;
  task_name: string;
  payload: Record<string, unknown>;
  status: JobStatus;
  priority: number;
  retries: number;
  max_retries: number;
  error: string | null;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
};

export type CreateJobInput = Partial<{
  task_name: string;
  payload: Record<string, unknown>;
  priority: number;
  max_retries: number;
}>;

export class JobFactory {
  private createdIds: string[] = [];
  private baseUrl: string;

  constructor(private request: APIRequestContext) {
    this.baseUrl = process.env.API_URL || 'http://localhost:8080/api';
  }

  /**
   * Create a job with optional overrides
   */
  async create(overrides: CreateJobInput = {}): Promise<Job> {
    const defaults: CreateJobInput = {
      task_name: 'transform_content',
      payload: {
        content_id: faker.string.uuid(),
        transformation_type: 'subtitle_to_article',
      },
      priority: 1,
      max_retries: 3,
    };

    const data = { ...defaults, ...overrides };

    const response = await this.request.post(`${this.baseUrl}/jobs`, {
      data,
    });

    if (!response.ok()) {
      const error = await response.text();
      throw new Error(`Failed to create job: ${response.status()} ${error}`);
    }

    const job = (await response.json()) as Job;
    this.createdIds.push(job.id);
    return job;
  }

  /**
   * Create a transformation job for specific content
   */
  async createTransformationJob(contentId: string, overrides: CreateJobInput = {}): Promise<Job> {
    return this.create({
      task_name: 'transform_content',
      payload: {
        content_id: contentId,
        transformation_type: 'subtitle_to_article',
      },
      ...overrides,
    });
  }

  /**
   * Create a feed fetch job
   */
  async createFeedFetchJob(subscriptionId: string, overrides: CreateJobInput = {}): Promise<Job> {
    return this.create({
      task_name: 'fetch_feed',
      payload: {
        subscription_id: subscriptionId,
      },
      ...overrides,
    });
  }

  /**
   * Wait for a job to reach a specific status
   */
  async waitForStatus(jobId: string, targetStatus: JobStatus, timeoutMs: number = 30000): Promise<Job> {
    const startTime = Date.now();

    while (Date.now() - startTime < timeoutMs) {
      const response = await this.request.get(`${this.baseUrl}/jobs/${jobId}`);
      if (!response.ok()) {
        throw new Error(`Failed to get job: ${response.status()}`);
      }

      const job = (await response.json()) as Job;
      if (job.status === targetStatus) {
        return job;
      }

      // Wait 500ms before polling again
      await new Promise((resolve) => setTimeout(resolve, 500));
    }

    throw new Error(`Job ${jobId} did not reach status ${targetStatus} within ${timeoutMs}ms`);
  }

  /**
   * Clean up all created jobs (cancel pending jobs)
   */
  async cleanup(): Promise<void> {
    for (const id of this.createdIds) {
      try {
        // Try to cancel the job first
        await this.request.post(`${this.baseUrl}/jobs/${id}/cancel`);
      } catch {
        // Ignore errors (job may have completed)
      }
    }
    this.createdIds = [];
  }
}

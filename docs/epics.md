---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - docs/prd.md
  - docs/architecture.md
  - docs/ux-design-specification.md
---

# rss-remastered - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for rss-remastered, decomposing the requirements from the PRD, UX Design, and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

**Subscription Management (FR1-FR9)**
- FR1: Users can add YouTube channel subscriptions by URL or channel ID
- FR2: Users can add RSS feed subscriptions by URL
- FR3: Users can add podcast feed subscriptions by URL
- FR4: Users can import multiple subscriptions via OPML file upload
- FR5: Users can view all active subscriptions with current status
- FR6: Users can edit subscription settings (name, tags, polling frequency)
- FR7: Users can delete subscriptions
- FR8: Users can organize subscriptions into user-defined categories/tags
- FR9: Users can export subscriptions as OPML file

**Content Aggregation (FR10-FR18)**
- FR10: System can fetch new content from YouTube channels automatically
- FR11: System can fetch new content from RSS feeds automatically
- FR12: System can fetch new content from podcast feeds automatically
- FR13: System can store content metadata (title, description, date, source, duration)
- FR14: Users can view aggregated content in chronological order (newest first)
- FR15: Users can filter content by subscription, category, or content type
- FR16: Users can search content by title or description
- FR17: Users can mark content as read/unread
- FR18: System can track content consumption state across sessions

**Content Transformation (FR19-FR27)**
- FR19: Users can request subtitle-to-article transformation for video content
- FR20: System can extract subtitles from YouTube videos (via available captions)
- FR21: System can transform subtitles into readable article format using AI transposition
- FR22: System can remove verbal artifacts (um, uh, repetition) from transformed content
- FR23: System can convert visual references to verbal descriptions in transformed content
- FR24: Users can view transformation status (queued, processing, complete, failed)
- FR25: Users can access completed transformations for consumption
- FR26: System can queue multiple transformation requests
- FR27: System can process transformations on-demand or via scheduled batch

**Content Serving - Web UI (FR28-FR33)**
- FR28: Users can access web interface for subscription and content management
- FR29: Users can read transformed articles in web interface
- FR30: Users can navigate content via responsive mobile-friendly interface
- FR31: Users can install web app to device home screen (PWA)
- FR32: Users can toggle between dark and light themes
- FR33: System can remember user's theme preference

**Content Serving - Podcast Feeds (FR34-FR37)**
- FR34: System can generate valid RSS 2.0 podcast feeds with iTunes extensions
- FR35: Users can access generated podcast feed URLs for use in podcatcher apps
- FR36: System can include episode metadata (title, description, duration, artwork) in feeds
- FR37: Podcatcher apps can fetch and play content from generated feeds

**Content Serving - Media Server Integration (FR38-FR40)**
- FR38: System can serve media files in Plex-compatible format
- FR39: System can serve media files in Jellyfin-compatible format
- FR40: Users can organize content into per-user libraries (e.g., "Sofia's Feeds")

**Integration - *arr Stack (FR41-FR45)**
- FR41: System can read from Sonarr API to understand existing media library
- FR42: System can read from Radarr API to understand existing media library
- FR43: External services can authenticate via API key
- FR44: External services can retrieve content metadata via API
- FR45: External services can retrieve subscription status via API

**System Health & Monitoring (FR46-FR51)**
- FR46: System can display feed health status (healthy, rate-limited, failing)
- FR47: System can display detailed error information for failed feed fetches
- FR48: Users can manually retry failed feed fetches
- FR49: System can automatically retry failed fetches with backoff
- FR50: System can display transformation queue status and progress
- FR51: System can display system health summary (uptime, queue depth, error rate)

**Configuration & Settings (FR52-FR58)**
- FR52: Users can generate API keys for external service access
- FR53: Users can revoke API keys
- FR54: Users can configure AI provider settings (local vs remote, model selection)
- FR55: Users can configure transformation quality preferences
- FR56: System can operate with AI features disabled (graceful degradation)
- FR57: Administrators can configure system via YAML configuration file
- FR58: System can auto-generate required keys (VAPID) on first run

**Notifications - Opportunistic (FR59-FR61)**
- FR59: Users can opt-in to push notifications for transformation completion
- FR60: Users can opt-in to push notifications for feed health alerts
- FR61: System can deliver notifications via Web Push API

### Non-Functional Requirements

**Performance (NFR1-NFR7)**
- NFR1: System startup completes within 30 seconds from container start to serving content
- NFR2: MVP operates within 2GB RAM without GPU requirement
- NFR3: Web UI initial load completes within 3 seconds on broadband connection
- NFR4: Feed list and content views render within 1 second after initial load
- NFR5: Transformation queue accepts new requests within 500ms
- NFR6: API endpoints respond within 200ms for CRUD operations
- NFR7: Podcast feed generation completes within 2 seconds for feeds under 100 items

**Reliability (NFR8-NFR14)**
- NFR8: System recovers gracefully from network failures without data loss
- NFR9: Malformed feed input does not crash system or corrupt other data
- NFR10: AI provider unavailability does not prevent core functionality (graceful degradation)
- NFR11: System preserves subscription and content data across restarts
- NFR12: Failed transformations can be retried without manual intervention
- NFR13: Automatic retry with exponential backoff for transient failures
- NFR14: System logs errors in structured format for debugging

**Integration Compatibility (NFR15-NFR21)**
- NFR15: Generated podcast feeds pass standard RSS 2.0 validators
- NFR16: Generated podcast feeds include required iTunes podcast extensions
- NFR17: Sonarr API integration follows documented Sonarr API specification
- NFR18: Radarr API integration follows documented Radarr API specification
- NFR19: Plex media serving follows Plex media server compatibility requirements
- NFR20: Jellyfin media serving follows Jellyfin compatibility requirements
- NFR21: OPML import/export follows OPML 2.0 specification

**Security (NFR22-NFR26)**
- NFR22: API keys use cryptographically secure random generation
- NFR23: API keys are stored hashed, not in plaintext
- NFR24: All API endpoints require authentication (no anonymous access to data)
- NFR25: Configuration files with secrets are not logged or exposed via API
- NFR26: HTTPS supported for all web traffic (user-configurable)

**Usability & Accessibility (NFR27-NFR31)**
- NFR27: Web UI functions on mobile devices (320px minimum width)
- NFR28: Touch targets meet 44x44px minimum for mobile usability
- NFR29: UI provides sufficient color contrast for readability (WCAG AA for text)
- NFR30: Error messages are human-readable and actionable
- NFR31: System state is always visible (no silent failures or mystery states)

**Deployment & Operations (NFR32-NFR36)**
- NFR32: Single `docker-compose up` deploys fully functional system
- NFR33: Configuration via environment variables and/or YAML file
- NFR34: Logs output in structured JSON format for log aggregation
- NFR35: System operates correctly behind reverse proxy (configurable base URL)
- NFR36: Data directory is configurable for Docker volume mounting

### Additional Requirements

**From Architecture - Project Initialization:**
- Initialize backend with FastAPI domain-based structure using uv
- Initialize frontend with Vite + React + TypeScript + shadcn/ui + Tailwind CSS v4
- Configure SQLAlchemy 2.0 with async support and Alembic migrations
- Set up in-process asyncio job queue with SQLite persistence
- Configure structlog for JSON logging
- Implement Pydantic Settings for layered configuration (env vars → YAML → DB → defaults)
- Create Docker single-container deployment with docker-compose.yml

**From Architecture - AI Integration:**
- Implement AI provider abstraction with OpenAI and Ollama support
- Support OpenAI-compatible endpoints via configurable base_url
- Implement NoOpProvider for graceful degradation when AI unavailable
- AI configuration via YAML and environment variables

**From Architecture - Implementation Patterns:**
- Follow naming conventions: snake_case for API/DB, PascalCase for components
- Use error code pattern: DOMAIN_ACTION_REASON
- Implement domain-based backend structure with router/schemas/models/service/exceptions per domain
- Implement feature-based frontend structure with components/features/stores/lib

**From UX - Component Requirements:**
- Implement StatusBadge component with traffic-light status indicators
- Implement SubscriptionCard component with health status and quick actions
- Implement TransformationProgress component with step-by-step progress
- Implement ErrorAlert component with categorized errors and recovery actions
- Implement HealthBanner component for system-wide status

**From UX - Layout Requirements:**
- Three-panel layout: collapsible sidebar (240px→64px) + main content + dismissable context panel (340px)
- Dark theme default with system preference detection
- Keyboard shortcuts for panel toggles ([ and ])
- State persistence to localStorage for panel collapse states

**From UX - Accessibility Requirements:**
- WCAG 2.1 AA compliance target
- Minimum touch targets 44x44px (mobile) / 36x36px (desktop)
- Keyboard navigation with visible focus indicators
- Screen reader support with ARIA labels and live regions
- prefers-reduced-motion support for animations

### FR Coverage Map

| FR | Epic | Description |
|----|------|-------------|
| FR1 | Epic 2 | Add YouTube subscriptions |
| FR2 | Epic 2 | Add RSS feed subscriptions |
| FR3 | Epic 2 | Add podcast subscriptions |
| FR4 | Epic 2 | OPML import |
| FR5 | Epic 2 | View subscriptions with status |
| FR6 | Epic 2 | Edit subscription settings |
| FR7 | Epic 2 | Delete subscriptions |
| FR8 | Epic 2 | Organize with tags |
| FR9 | Epic 2 | OPML export |
| FR10 | Epic 3 | Auto-fetch YouTube content |
| FR11 | Epic 3 | Auto-fetch RSS content |
| FR12 | Epic 3 | Auto-fetch podcast content |
| FR13 | Epic 3 | Store content metadata |
| FR14 | Epic 3 | Chronological content view |
| FR15 | Epic 3 | Filter content |
| FR16 | Epic 3 | Search content |
| FR17 | Epic 3 | Mark read/unread |
| FR18 | Epic 3 | Track consumption state |
| FR19 | Epic 4 | Request transformation |
| FR20 | Epic 4 | Extract subtitles |
| FR21 | Epic 4 | AI transposition |
| FR22 | Epic 4 | Remove verbal artifacts |
| FR23 | Epic 4 | Convert visual references |
| FR24 | Epic 4 | View transformation status |
| FR25 | Epic 4 | Access transformed content |
| FR26 | Epic 4 | Queue transformations |
| FR27 | Epic 4 | On-demand/scheduled transforms |
| FR28 | Epic 5 | Web interface |
| FR29 | Epic 5 | Article reader |
| FR30 | Epic 5 | Mobile-friendly interface |
| FR31 | Epic 5 | PWA installable |
| FR32 | Epic 5 | Theme toggle |
| FR33 | Epic 5 | Remember theme |
| FR34 | Epic 6 | Generate podcast feeds |
| FR35 | Epic 6 | Podcast feed URLs |
| FR36 | Epic 6 | Episode metadata |
| FR37 | Epic 6 | Podcatcher compatibility |
| FR38 | Epic 6 | Plex serving |
| FR39 | Epic 6 | Jellyfin serving |
| FR40 | Epic 6 | Per-user libraries |
| FR41 | Epic 6 | Sonarr API read |
| FR42 | Epic 6 | Radarr API read |
| FR43 | Epic 6 | API key auth |
| FR44 | Epic 6 | Content metadata API |
| FR45 | Epic 6 | Subscription status API |
| FR46 | Epic 3 | Feed health status |
| FR47 | Epic 3 | Error details |
| FR48 | Epic 3 | Manual retry |
| FR49 | Epic 3 | Auto-retry with backoff |
| FR50 | Epic 4 | Queue status/progress |
| FR51 | Epic 5 | System health summary |
| FR52 | Epic 7 | Generate API keys |
| FR53 | Epic 7 | Revoke API keys |
| FR54 | Epic 4 | AI provider settings |
| FR55 | Epic 4 | Transform quality prefs |
| FR56 | Epic 4 | Graceful AI degradation |
| FR57 | Epic 7 | YAML config |
| FR58 | Epic 7 | Auto-gen VAPID keys |
| FR59 | Epic 7 | Notification opt-in (transform) |
| FR60 | Epic 7 | Notification opt-in (health) |
| FR61 | Epic 7 | Web Push delivery |

## Epic List

### Epic 1: Project Foundation & Core Infrastructure
Developers can run the application locally and have a working foundation for all subsequent development. A running Docker container with FastAPI backend, React frontend shell, database, and basic health endpoint - ready for feature development.

**FRs covered:** Foundation for all FRs (infrastructure per Architecture requirements)
**NFRs addressed:** NFR1, NFR2, NFR32, NFR33, NFR34, NFR35, NFR36

### Epic 2: Subscription Management
Users can subscribe to content sources and manage their subscriptions. Marcus can add YouTube channels, RSS feeds, and podcasts to his system, organize them with tags, and import/export via OPML.

**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8, FR9
**NFRs addressed:** NFR6, NFR21, NFR24

### Epic 3: Content Aggregation & Feed Health
Users can view aggregated content from their subscriptions with clear health visibility. Marcus sees a chronological feed of all content from his subscriptions, can filter and search, and always knows if a feed is healthy or having issues.

**FRs covered:** FR10, FR11, FR12, FR13, FR14, FR15, FR16, FR17, FR18, FR46, FR47, FR48, FR49
**NFRs addressed:** NFR4, NFR8, NFR9, NFR13, NFR14

### Epic 4: Content Transformation Pipeline
Users can transform content across formats using intelligent AI transposition. Marcus can request subtitle-to-article transformation, see progress as it happens, and access quality transformed content.

**FRs covered:** FR19, FR20, FR21, FR22, FR23, FR24, FR25, FR26, FR27, FR50, FR54, FR55, FR56
**NFRs addressed:** NFR5, NFR10, NFR12

### Epic 5: Web Application & PWA
Users can manage their system through a polished, responsive web interface. Marcus accesses a dark-mode dashboard, reads transformed articles, installs as PWA, and has full system visibility.

**FRs covered:** FR28, FR29, FR30, FR31, FR32, FR33, FR51
**NFRs addressed:** NFR3, NFR27, NFR28, NFR29, NFR30, NFR31

### Epic 6: Content Delivery & Integrations
Users can consume content through their preferred apps (Plex, podcast apps, *arr stack). Sofia's transformed content appears in Plex, Marcus's podcast feed works in any podcatcher, and the system integrates with existing *arr stack.

**FRs covered:** FR34, FR35, FR36, FR37, FR38, FR39, FR40, FR41, FR42, FR43, FR44, FR45
**NFRs addressed:** NFR7, NFR15, NFR16, NFR17, NFR18, NFR19, NFR20

### Epic 7: API Security & Notifications
Users have secure API access and optional push notifications. Marcus generates API keys for external integrations, system is secure, and users can opt-in to notifications.

**FRs covered:** FR52, FR53, FR57, FR58, FR59, FR60, FR61
**NFRs addressed:** NFR22, NFR23, NFR24, NFR25, NFR26

---

## Epic 1: Project Foundation & Core Infrastructure

Developers can run the application locally and have a working foundation for all subsequent development.

### Story 1.1: Initialize Backend Project Structure

**As a** developer,
**I want** a FastAPI backend project with domain-based module structure,
**So that** I have a consistent foundation for implementing all backend features.

**Acceptance Criteria:**

**Given** a fresh clone of the repository
**When** I run `cd backend && uv sync`
**Then** all Python dependencies are installed from pyproject.toml
**And** the project structure matches the Architecture specification:
- `backend/src/core/` with config.py, database.py, dependencies.py, exceptions.py, logging.py
- `backend/src/subscriptions/` empty module skeleton with __init__.py
- `backend/src/content/` empty module skeleton
- `backend/src/transformations/` empty module skeleton
- `backend/src/feeds/` empty module skeleton
- `backend/src/integrations/` empty module skeleton
- `backend/src/jobs/` empty module skeleton
- `backend/src/ai/` empty module skeleton
- `backend/src/health/` with router.py and service.py
- `backend/src/main.py` FastAPI app entry point

**Given** the backend is installed
**When** I run `uv run uvicorn src.main:app --reload`
**Then** the FastAPI server starts on port 8000
**And** `GET /api/health` returns `{"status": "healthy"}`

---

### Story 1.2: Initialize Frontend Project Structure

**As a** developer,
**I want** a Vite + React + TypeScript frontend with shadcn/ui configured,
**So that** I have a consistent foundation for implementing all frontend features.

**Acceptance Criteria:**

**Given** a fresh clone of the repository
**When** I run `cd frontend && npm install`
**Then** all dependencies are installed including React 18+, TypeScript, Tailwind CSS v4
**And** shadcn/ui is initialized with components.json configured
**And** the project structure includes:
- `frontend/src/components/ui/` for shadcn/ui base components
- `frontend/src/components/app/` empty directory for app components
- `frontend/src/features/` empty directory for feature modules
- `frontend/src/stores/ui.ts` Zustand store skeleton
- `frontend/src/lib/api.ts`, `query.ts`, `utils.ts` utility files
- `frontend/src/App.tsx` and `main.tsx` entry points

**Given** the frontend is installed
**When** I run `npm run dev`
**Then** the Vite dev server starts
**And** the app displays a placeholder heading with dark theme applied
**And** `@/` path aliases resolve correctly in imports

---

### Story 1.3: Configure Database and Migrations

**As a** developer,
**I want** SQLAlchemy 2.0 async setup with Alembic migrations,
**So that** I can create and migrate database schemas for all features.

**Acceptance Criteria:**

**Given** the backend project from Story 1.1
**When** I run `uv run alembic upgrade head`
**Then** the SQLite database is created at the configured path (default: `data/rss.db`)
**And** the `alembic_version` table exists tracking migration state

**Given** `core/database.py` exists
**Then** it provides:
- `async_engine` configured for SQLite with aiosqlite
- `AsyncSessionLocal` session factory
- `get_db` dependency for FastAPI routes
- `Base` declarative base class for all models

**Given** the environment variable `RSS_DATABASE_URL` is set
**When** the application starts
**Then** it uses the configured database URL instead of the default

---

### Story 1.4: Configure Structured Logging

**As a** developer,
**I want** structlog configured for JSON output,
**So that** all application logs are structured and parseable by log aggregation tools.

**Acceptance Criteria:**

**Given** the backend application starts
**When** any log statement is executed
**Then** logs are output in JSON format to stdout containing:
- `timestamp` in ISO 8601 format
- `level` (debug, info, warning, error)
- `event` describing what happened
- Additional context fields as key-value pairs

**Given** `RSS_LOG_LEVEL=debug` environment variable is set
**When** the application starts
**Then** debug-level logs are included in output

**Given** `RSS_LOG_FORMAT=console` environment variable is set
**When** the application starts
**Then** logs use human-readable colored format for development

---

### Story 1.5: Configure Pydantic Settings

**As a** developer,
**I want** a layered configuration system using Pydantic Settings,
**So that** all app configuration follows a consistent pattern with environment variable overrides.

**Acceptance Criteria:**

**Given** `core/config.py` exists
**Then** it exports a `Settings` class with typed configuration fields:
- `database_url: str` (default: `sqlite+aiosqlite:///data/rss.db`)
- `log_level: str` (default: `info`)
- `log_format: str` (default: `json`)
- `base_url: str` (default: empty string for reverse proxy support)
- `data_dir: Path` (default: `data/`)

**Given** environment variables with `RSS_` prefix exist
**When** the application loads configuration
**Then** environment variables override YAML file values
**And** YAML file values override defaults
**And** nested settings use double underscore (e.g., `RSS_AI__PROVIDER`)

**Given** an invalid configuration value is provided
**When** the application starts
**Then** a clear validation error message is displayed
**And** the application fails to start

---

### Story 1.6: Docker Single-Container Deployment

**As a** self-hoster,
**I want** to run rss-remastered with a single `docker-compose up` command,
**So that** I can deploy the complete application with minimal configuration.

**Acceptance Criteria:**

**Given** Docker and Docker Compose are installed
**When** I run `docker-compose up --build`
**Then** a single container is built containing both backend and frontend
**And** the frontend is built to static files and served by FastAPI
**And** the application is accessible at `http://localhost:8080`

**Given** the container is running
**When** I access `GET /api/health`
**Then** the response is `{"status": "healthy"}`

**Given** the docker-compose.yml file
**Then** it includes:
- Volume mount for `./data:/app/data` (persistent storage)
- Optional volume mount for `./config.yaml:/app/config.yaml:ro`
- Port mapping `8080:8000`
- Environment variable pass-through

**Given** the container starts
**Then** startup completes within 30 seconds (NFR1)
**And** memory usage stays under 2GB (NFR2)

---

## Epic 2: Subscription Management

Users can subscribe to content sources and manage their subscriptions. Marcus can add YouTube channels, RSS feeds, and podcasts to his system, organize them with tags, and import/export via OPML.

### Story 2.1: Create Subscription Data Model

**As a** developer,
**I want** a Subscription database model and API schemas,
**So that** subscriptions can be persisted and validated.

**Acceptance Criteria:**

**Given** the database is initialized
**When** the migration for subscriptions runs
**Then** a `subscriptions` table is created with columns:
- `id` (UUID primary key)
- `name` (string, required)
- `url` (string, required, unique)
- `source_type` (enum: youtube_channel, rss_feed, podcast)
- `icon_url` (string, nullable)
- `polling_interval_minutes` (integer, default 60)
- `status` (enum: active, paused, error)
- `error_message` (string, nullable)
- `last_fetched_at` (datetime, nullable)
- `created_at` (datetime)
- `updated_at` (datetime)

**Given** the subscriptions module exists
**Then** it includes Pydantic schemas for:
- `SubscriptionCreate` (input validation)
- `SubscriptionUpdate` (partial update)
- `SubscriptionResponse` (API output)
- `SubscriptionListResponse` (paginated list)

---

### Story 2.2: Add YouTube Channel Subscription

**As a** power user (Marcus),
**I want** to add a YouTube channel subscription by URL or channel ID,
**So that** I can track new content from my favorite YouTube creators.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I POST to `/api/subscriptions` with:
```json
{
  "url": "https://www.youtube.com/channel/UC...",
  "source_type": "youtube_channel"
}
```
**Then** the system extracts the channel ID from the URL
**And** fetches channel metadata (name, icon) from YouTube
**And** creates a subscription record
**And** returns the subscription with status 201

**Given** I provide a channel ID directly (e.g., `UC...`)
**When** I POST to `/api/subscriptions`
**Then** the system accepts the ID without URL parsing

**Given** I provide an invalid YouTube URL or channel ID
**When** I POST to `/api/subscriptions`
**Then** the system returns 400 with error `SUBSCRIPTION_CREATE_INVALID_URL`

**Given** a subscription for this channel already exists
**When** I POST to `/api/subscriptions`
**Then** the system returns 409 with error `SUBSCRIPTION_CREATE_DUPLICATE`

---

### Story 2.3: Add RSS Feed Subscription

**As a** power user (Marcus),
**I want** to add an RSS feed subscription by URL,
**So that** I can aggregate content from blogs and news sites.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I POST to `/api/subscriptions` with:
```json
{
  "url": "https://example.com/feed.xml",
  "source_type": "rss_feed"
}
```
**Then** the system fetches and parses the RSS feed
**And** extracts feed metadata (title, description, icon)
**And** creates a subscription record
**And** returns the subscription with status 201

**Given** the URL returns invalid RSS/Atom XML
**When** I POST to `/api/subscriptions`
**Then** the system returns 400 with error `SUBSCRIPTION_CREATE_INVALID_FEED`
**And** includes details about the parse error

**Given** the URL is unreachable
**When** I POST to `/api/subscriptions`
**Then** the system returns 400 with error `SUBSCRIPTION_CREATE_FETCH_FAILED`

---

### Story 2.4: Add Podcast Feed Subscription

**As a** power user (Marcus),
**I want** to add a podcast feed subscription by URL,
**So that** I can track new episodes from my favorite podcasts.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I POST to `/api/subscriptions` with:
```json
{
  "url": "https://example.com/podcast.xml",
  "source_type": "podcast"
}
```
**Then** the system fetches and parses the podcast RSS feed
**And** extracts podcast metadata (title, description, artwork, author)
**And** validates iTunes podcast extensions are present
**And** creates a subscription record
**And** returns the subscription with status 201

**Given** the feed is valid RSS but not a podcast feed
**When** I POST to `/api/subscriptions`
**Then** the system returns 400 with error `SUBSCRIPTION_CREATE_NOT_PODCAST`
**And** suggests using `rss_feed` source_type instead

---

### Story 2.5: View All Subscriptions

**As a** power user (Marcus),
**I want** to view all my subscriptions with their current status,
**So that** I can see what I'm subscribed to and their health.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I GET `/api/subscriptions`
**Then** the system returns a paginated list of subscriptions
**And** each subscription includes: id, name, url, source_type, icon_url, status, last_fetched_at

**Given** I provide query parameter `?status=error`
**When** I GET `/api/subscriptions`
**Then** only subscriptions with error status are returned

**Given** I provide query parameter `?source_type=youtube_channel`
**When** I GET `/api/subscriptions`
**Then** only YouTube channel subscriptions are returned

**Given** I provide query parameter `?tag=tech`
**When** I GET `/api/subscriptions`
**Then** only subscriptions with the "tech" tag are returned

**Given** the API responds
**Then** the response completes within 200ms (NFR6)

---

### Story 2.6: Edit Subscription Settings

**As a** power user (Marcus),
**I want** to edit subscription settings like name, tags, and polling frequency,
**So that** I can customize how subscriptions behave.

**Acceptance Criteria:**

**Given** I am authenticated and a subscription exists
**When** I PATCH `/api/subscriptions/{id}` with:
```json
{
  "name": "Custom Name",
  "polling_interval_minutes": 30
}
```
**Then** the subscription is updated with the new values
**And** only provided fields are changed
**And** the updated subscription is returned

**Given** I try to update the URL
**When** I PATCH `/api/subscriptions/{id}`
**Then** the system returns 400 with error `SUBSCRIPTION_UPDATE_URL_IMMUTABLE`

**Given** the subscription does not exist
**When** I PATCH `/api/subscriptions/{id}`
**Then** the system returns 404 with error `SUBSCRIPTION_NOT_FOUND`

---

### Story 2.7: Delete Subscription

**As a** power user (Marcus),
**I want** to delete a subscription,
**So that** I can remove sources I no longer want to follow.

**Acceptance Criteria:**

**Given** I am authenticated and a subscription exists
**When** I DELETE `/api/subscriptions/{id}`
**Then** the subscription is soft-deleted (marked as deleted, not removed)
**And** the system returns 204 No Content

**Given** the subscription has associated content items
**When** I DELETE `/api/subscriptions/{id}`
**Then** the subscription is deleted
**And** associated content items are preserved but marked as orphaned

**Given** I provide query parameter `?hard=true`
**When** I DELETE `/api/subscriptions/{id}`
**Then** the subscription and all associated content are permanently deleted

---

### Story 2.8: Tag Management for Subscriptions

**As a** power user (Marcus),
**I want** to organize subscriptions with user-defined tags,
**So that** I can group and filter related subscriptions.

**Acceptance Criteria:**

**Given** the database is initialized
**When** the migration for tags runs
**Then** a `tags` table is created with: id, name, color
**And** a `subscription_tags` junction table is created

**Given** I am authenticated
**When** I POST `/api/tags` with `{"name": "tech", "color": "#3b82f6"}`
**Then** a new tag is created and returned

**Given** I am authenticated and tags exist
**When** I PATCH `/api/subscriptions/{id}` with `{"tags": ["tech", "news"]}`
**Then** the subscription is associated with the specified tags
**And** tags that don't exist are created automatically

**Given** I GET `/api/tags`
**Then** all tags are returned with subscription count for each

---

### Story 2.9: OPML Import

**As a** power user (Marcus),
**I want** to import subscriptions from an OPML file,
**So that** I can migrate from other RSS readers quickly.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I POST `/api/subscriptions/import` with an OPML file
**Then** the system parses the OPML 2.0 format
**And** creates subscriptions for each feed entry
**And** preserves folder structure as tags
**And** returns a summary: created, skipped (duplicates), failed

**Given** the OPML contains 50 feeds
**When** I import the file
**Then** subscriptions are created in batch
**And** duplicates are skipped without error
**And** the response includes details for each feed

**Given** the OPML file is malformed
**When** I POST `/api/subscriptions/import`
**Then** the system returns 400 with error `SUBSCRIPTION_IMPORT_INVALID_OPML`

---

### Story 2.10: OPML Export

**As a** power user (Marcus),
**I want** to export my subscriptions as an OPML file,
**So that** I can backup or migrate to other RSS readers.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I GET `/api/subscriptions/export`
**Then** the system generates a valid OPML 2.0 file
**And** includes all active subscriptions
**And** preserves tags as OPML folders/categories
**And** returns with Content-Type `application/xml`
**And** includes Content-Disposition header for download

**Given** subscriptions have tags
**When** I export
**Then** the OPML organizes feeds into outline elements by tag

---

## Epic 3: Content Aggregation & Feed Health

Users can view aggregated content from their subscriptions with clear health visibility. Marcus sees a chronological feed of all content from his subscriptions, can filter and search, and always knows if a feed is healthy or having issues.

### Story 3.1: Create Content Item Data Model

**As a** developer,
**I want** a ContentItem database model and API schemas,
**So that** fetched content can be persisted and queried.

**Acceptance Criteria:**

**Given** the database is initialized
**When** the migration for content items runs
**Then** a `content_items` table is created with columns:
- `id` (UUID primary key)
- `subscription_id` (UUID foreign key to subscriptions)
- `external_id` (string, unique per subscription - e.g., video ID, article GUID)
- `title` (string, required)
- `description` (text, nullable)
- `url` (string, required)
- `thumbnail_url` (string, nullable)
- `published_at` (datetime, required)
- `duration_seconds` (integer, nullable - for video/audio)
- `content_type` (enum: video, article, podcast_episode)
- `is_read` (boolean, default false)
- `created_at` (datetime)
- `updated_at` (datetime)

**Given** the content module exists
**Then** it includes Pydantic schemas for:
- `ContentItemResponse` (API output)
- `ContentItemListResponse` (paginated list with total count)

---

### Story 3.2: Implement Background Job Queue

**As a** developer,
**I want** an in-process async job queue with SQLite persistence,
**So that** background tasks like feed fetching can run reliably.

**Acceptance Criteria:**

**Given** the database is initialized
**When** the migration for jobs runs
**Then** a `jobs` table is created with columns:
- `id` (UUID primary key)
- `job_type` (string, e.g., "fetch_subscription", "transform_content")
- `payload` (JSON)
- `status` (enum: pending, running, completed, failed)
- `result` (JSON, nullable)
- `error_message` (text, nullable)
- `attempts` (integer, default 0)
- `max_attempts` (integer, default 3)
- `scheduled_at` (datetime)
- `started_at` (datetime, nullable)
- `completed_at` (datetime, nullable)
- `created_at` (datetime)

**Given** the jobs module exists
**Then** it provides:
- `enqueue_job(job_type, payload, scheduled_at)` function
- `JobRunner` class that processes pending jobs
- Automatic retry with exponential backoff for failed jobs
- Job status updates via database

**Given** the application starts
**Then** the job runner starts processing pending jobs in the background

---

### Story 3.3: Fetch YouTube Channel Content

**As a** power user (Marcus),
**I want** the system to automatically fetch new videos from my YouTube subscriptions,
**So that** I see new content without manual refresh.

**Acceptance Criteria:**

**Given** a YouTube channel subscription exists
**When** the scheduled fetch job runs
**Then** the system fetches the channel's RSS feed from YouTube
**And** parses video metadata (title, description, thumbnail, published date, duration)
**And** creates ContentItem records for new videos
**And** skips videos that already exist (by external_id)
**And** updates the subscription's `last_fetched_at` timestamp

**Given** the fetch encounters a rate limit
**When** the job fails
**Then** the subscription status is set to "error"
**And** the error message indicates rate limiting
**And** the job is rescheduled with exponential backoff

**Given** the fetch succeeds
**Then** the subscription status is set to "active"
**And** any previous error message is cleared

---

### Story 3.4: Fetch RSS Feed Content

**As a** power user (Marcus),
**I want** the system to automatically fetch new articles from my RSS subscriptions,
**So that** I see new content from blogs and news sites.

**Acceptance Criteria:**

**Given** an RSS feed subscription exists
**When** the scheduled fetch job runs
**Then** the system fetches and parses the RSS/Atom feed
**And** extracts article metadata (title, description, link, published date)
**And** creates ContentItem records for new articles
**And** handles both RSS 2.0 and Atom feed formats
**And** updates the subscription's `last_fetched_at` timestamp

**Given** the feed XML is malformed
**When** the job fails
**Then** the subscription status is set to "error"
**And** the error message includes parse error details
**And** the system logs the error for debugging (NFR14)

---

### Story 3.5: Fetch Podcast Episode Content

**As a** power user (Marcus),
**I want** the system to automatically fetch new episodes from my podcast subscriptions,
**So that** I see new podcast content.

**Acceptance Criteria:**

**Given** a podcast subscription exists
**When** the scheduled fetch job runs
**Then** the system fetches and parses the podcast RSS feed
**And** extracts episode metadata (title, description, audio URL, duration, episode artwork)
**And** creates ContentItem records for new episodes
**And** stores audio enclosure URL for later transformation
**And** updates the subscription's `last_fetched_at` timestamp

**Given** the podcast has iTunes-specific metadata
**Then** the system extracts: episode number, season, explicit flag, episode type

---

### Story 3.6: View Aggregated Content Feed

**As a** power user (Marcus),
**I want** to view all content from my subscriptions in chronological order,
**So that** I see the most recent content first with nothing buried.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I GET `/api/content`
**Then** the system returns a paginated list of content items
**And** items are sorted by `published_at` descending (newest first)
**And** each item includes: id, title, description, url, thumbnail_url, published_at, content_type, is_read, subscription (name, icon)

**Given** I provide query parameter `?limit=50&offset=0`
**When** I GET `/api/content`
**Then** the first 50 items are returned with total count

**Given** content is rendered
**Then** the response completes within 1 second (NFR4)

---

### Story 3.7: Filter Content by Subscription and Type

**As a** power user (Marcus),
**I want** to filter content by subscription, category, or content type,
**So that** I can focus on specific content sources.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I GET `/api/content?subscription_id={uuid}`
**Then** only content from the specified subscription is returned

**Given** I am authenticated
**When** I GET `/api/content?content_type=video`
**Then** only video content items are returned

**Given** I am authenticated
**When** I GET `/api/content?tag=tech`
**Then** only content from subscriptions with the "tech" tag is returned

**Given** I combine multiple filters
**When** I GET `/api/content?content_type=video&tag=tech`
**Then** filters are applied with AND logic

---

### Story 3.8: Search Content

**As a** power user (Marcus),
**I want** to search content by title or description,
**So that** I can find specific content I'm looking for.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I GET `/api/content?search=kubernetes`
**Then** content items matching "kubernetes" in title or description are returned
**And** search is case-insensitive
**And** results are still sorted by published_at descending

**Given** no content matches the search term
**When** I GET `/api/content?search=nonexistent`
**Then** an empty list is returned with total count 0

**Given** the search query is very broad
**Then** results are paginated to prevent performance issues

---

### Story 3.9: Mark Content as Read/Unread

**As a** power user (Marcus),
**I want** to mark content as read or unread,
**So that** I can track what I've consumed.

**Acceptance Criteria:**

**Given** I am authenticated and a content item exists
**When** I PATCH `/api/content/{id}` with `{"is_read": true}`
**Then** the content item is marked as read
**And** the updated item is returned

**Given** I want to mark multiple items as read
**When** I POST `/api/content/batch` with `{"ids": [...], "is_read": true}`
**Then** all specified items are marked as read
**And** a summary is returned with count of updated items

**Given** I filter by `?is_read=false`
**When** I GET `/api/content`
**Then** only unread content items are returned

---

### Story 3.10: Display Feed Health Status

**As a** power user (Marcus),
**I want** to see the health status of each subscription,
**So that** I know immediately if a feed is having issues.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I GET `/api/subscriptions`
**Then** each subscription includes:
- `status` (active, paused, error)
- `error_message` (if status is error)
- `last_fetched_at` (timestamp of last successful fetch)
- `next_fetch_at` (scheduled next fetch time)

**Given** a subscription has status "error"
**When** I view the subscription
**Then** the error message explains what went wrong in human-readable terms (NFR30)

**Given** I GET `/api/health/feeds`
**Then** a summary is returned with counts: healthy, warning (stale), error

---

### Story 3.11: Manual Feed Retry

**As a** power user (Marcus),
**I want** to manually retry a failed feed fetch,
**So that** I can recover from transient errors without waiting.

**Acceptance Criteria:**

**Given** I am authenticated and a subscription has status "error"
**When** I POST `/api/subscriptions/{id}/retry`
**Then** a new fetch job is enqueued immediately
**And** the subscription status is set to "active" (optimistic)
**And** the response indicates the job was queued

**Given** the retry job completes successfully
**Then** the subscription status remains "active"
**And** new content items are created

**Given** the retry job fails
**Then** the subscription status is set back to "error"
**And** the error message is updated with the new failure reason

---

### Story 3.12: Automatic Retry with Backoff

**As a** power user (Marcus),
**I want** failed feeds to automatically retry with exponential backoff,
**So that** transient errors resolve without my intervention.

**Acceptance Criteria:**

**Given** a fetch job fails
**When** the job has not exceeded max_attempts
**Then** a new job is scheduled with exponential backoff:
- Attempt 1 failure: retry in 5 minutes
- Attempt 2 failure: retry in 15 minutes
- Attempt 3 failure: retry in 60 minutes
**And** the subscription status shows "error" with retry scheduled

**Given** a fetch job has exceeded max_attempts
**Then** no more automatic retries are scheduled
**And** the subscription requires manual intervention

**Given** automatic retry succeeds
**Then** the subscription status is set to "active"
**And** normal polling schedule resumes

---

## Epic 4: Content Transformation Pipeline

Users can transform content across formats using intelligent AI transposition. Marcus can request subtitle-to-article transformation, see progress as it happens, and access quality transformed content.

### Story 4.1: Create Transformation Data Model

**As a** developer,
**I want** a Transformation database model and API schemas,
**So that** transformation requests can be tracked and managed.

**Acceptance Criteria:**

**Given** the database is initialized
**When** the migration for transformations runs
**Then** a `transformations` table is created with columns:
- `id` (UUID primary key)
- `content_item_id` (UUID foreign key to content_items)
- `input_format` (enum: video, audio, article)
- `output_format` (enum: article, audio, summary)
- `status` (enum: queued, processing, completed, failed)
- `progress_percent` (integer, 0-100)
- `current_step` (string, nullable - e.g., "Extracting audio...")
- `result_url` (string, nullable - path to transformed content)
- `quality_score` (float, nullable - confidence metric)
- `error_message` (text, nullable)
- `started_at` (datetime, nullable)
- `completed_at` (datetime, nullable)
- `created_at` (datetime)

**Given** the transformations module exists
**Then** it includes Pydantic schemas for:
- `TransformationRequest` (input)
- `TransformationResponse` (API output with progress)
- `TransformationListResponse` (queue view)

---

### Story 4.2: Configure AI Provider Abstraction

**As a** developer,
**I want** an AI provider abstraction supporting OpenAI and Ollama,
**So that** transformation can use different AI backends.

**Acceptance Criteria:**

**Given** the ai module exists
**Then** it provides an `AIProvider` abstract base class with:
- `async def complete(prompt: str, max_tokens: int) -> str`
- `async def is_available() -> bool`

**Given** `RSS_AI__PROVIDER=openai` is configured
**When** the application starts
**Then** the OpenAI provider is initialized with `RSS_AI__API_KEY`
**And** it supports `RSS_AI__BASE_URL` for OpenAI-compatible endpoints

**Given** `RSS_AI__PROVIDER=ollama` is configured
**When** the application starts
**Then** the Ollama provider is initialized with `RSS_AI__OLLAMA_HOST`
**And** it uses the model specified in `RSS_AI__MODEL`

**Given** `RSS_AI__PROVIDER=none` or AI is unavailable
**When** transformation is requested
**Then** the NoOpProvider returns graceful error
**And** the system continues operating without AI features (NFR10)

---

### Story 4.3: Extract YouTube Subtitles

**As a** power user (Marcus),
**I want** the system to extract subtitles from YouTube videos,
**So that** they can be transformed into readable articles.

**Acceptance Criteria:**

**Given** a video content item exists from a YouTube subscription
**When** a transformation is requested
**Then** the system attempts to fetch available captions from YouTube
**And** prefers manual captions over auto-generated
**And** downloads the caption text with timestamps

**Given** captions are available in multiple languages
**When** extracting subtitles
**Then** the system prefers English captions
**And** falls back to other languages if English unavailable

**Given** no captions are available for the video
**When** extraction is attempted
**Then** the transformation fails with error `TRANSFORM_NO_CAPTIONS`
**And** the error message suggests the video has no subtitles

---

### Story 4.4: Request On-Demand Transformation

**As a** power user (Marcus),
**I want** to request transformation for specific content,
**So that** I can convert content to my preferred format.

**Acceptance Criteria:**

**Given** I am authenticated and a content item exists
**When** I POST `/api/transformations` with:
```json
{
  "content_item_id": "uuid",
  "output_format": "article"
}
```
**Then** a transformation record is created with status "queued"
**And** a transformation job is enqueued
**And** the transformation is returned with queue position
**And** the request completes within 500ms (NFR5)

**Given** a transformation for this content/format already exists
**When** I POST `/api/transformations`
**Then** the existing transformation is returned
**And** no duplicate is created

**Given** the content type cannot be transformed to the requested format
**When** I POST `/api/transformations`
**Then** the system returns 400 with error `TRANSFORM_INVALID_FORMAT`

---

### Story 4.5: AI-Powered Subtitle to Article Transformation

**As a** power user (Marcus),
**I want** subtitles transformed into readable articles using AI,
**So that** I can read video content as text.

**Acceptance Criteria:**

**Given** a transformation job is processing with subtitles extracted
**When** the AI transformation step runs
**Then** the AI provider receives a prompt to:
- Convert spoken language to written prose
- Remove verbal artifacts (um, uh, like, you know)
- Add paragraph breaks at topic changes
- Preserve the original meaning and key points

**Given** the transformation completes
**Then** the result is stored as markdown
**And** the transformation status is set to "completed"
**And** the quality_score is set based on AI confidence

**Given** the AI provider fails
**When** the transformation is processing
**Then** the job is retried according to retry policy (NFR12)
**And** the error is logged with context

---

### Story 4.6: Clean Verbal Artifacts

**As a** power user (Marcus),
**I want** verbal artifacts removed from transformed content,
**So that** the text reads naturally as written prose.

**Acceptance Criteria:**

**Given** subtitle text is being transformed
**When** the cleaning step runs
**Then** the following are removed or corrected:
- Filler words: "um", "uh", "like", "you know", "right"
- False starts: "I was going to- I mean"
- Repetitions: "very very important" → "very important"
- Speaker interruptions and overlaps

**Given** the original has intentional emphasis through repetition
**Then** the context is preserved appropriately

**Given** the cleaning produces significantly shorter text
**Then** this is logged as a quality indicator

---

### Story 4.7: Convert Visual References to Verbal Descriptions

**As a** power user (Marcus),
**I want** visual references converted to verbal descriptions,
**So that** transformed articles make sense without the video.

**Acceptance Criteria:**

**Given** subtitle text contains visual references like "as you can see here"
**When** the AI transformation runs
**Then** the prompt instructs the AI to:
- Identify visual references
- Replace with contextual descriptions where possible
- Flag unclear references that need removal
- Maintain coherent narrative flow

**Given** a timestamp reference like "at 5:32"
**When** transformation runs
**Then** the timestamp is either contextualized or removed

---

### Story 4.8: View Transformation Queue and Progress

**As a** power user (Marcus),
**I want** to see transformation queue status and progress,
**So that** I know when my transformations will complete.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I GET `/api/transformations`
**Then** a list of my transformations is returned
**And** each includes: id, content_item title, status, progress_percent, current_step, created_at

**Given** transformations exist in various states
**When** I GET `/api/transformations?status=processing`
**Then** only processing transformations are returned

**Given** a transformation is processing
**When** I GET `/api/transformations/{id}`
**Then** current progress is returned including:
- `progress_percent` (0-100)
- `current_step` (e.g., "Cleaning artifacts...")
- Estimated time remaining (if calculable)

---

### Story 4.9: Access Completed Transformations

**As a** power user (Marcus),
**I want** to access completed transformed content,
**So that** I can consume it in my preferred format.

**Acceptance Criteria:**

**Given** a transformation has status "completed"
**When** I GET `/api/transformations/{id}`
**Then** the response includes `result_url` pointing to the content

**Given** I access the `result_url`
**Then** the transformed content is served with appropriate Content-Type
**And** article transformations are served as markdown or HTML

**Given** a transformation failed
**When** I GET `/api/transformations/{id}`
**Then** the response includes error_message explaining the failure
**And** the error is human-readable and actionable

---

### Story 4.10: Transformation Progress Notifications

**As a** developer,
**I want** transformation progress to be tracked in real-time,
**So that** the UI can show meaningful progress updates.

**Acceptance Criteria:**

**Given** a transformation is processing
**When** each step completes
**Then** the transformation record is updated with:
- `progress_percent` incremented
- `current_step` updated to next step name

**Given** the transformation steps are:
1. Extracting subtitles (0-20%)
2. Cleaning transcript (20-40%)
3. AI transformation (40-80%)
4. Post-processing (80-100%)
**Then** progress is updated at each transition

**Given** the frontend polls for progress
**Then** updates are visible within 2 seconds of step completion

---

### Story 4.11: Configure Transformation Quality Preferences

**As a** power user (Marcus),
**I want** to configure transformation quality preferences,
**So that** I can balance quality vs. speed.

**Acceptance Criteria:**

**Given** I access settings
**When** I configure transformation preferences
**Then** I can set:
- AI model preference (if multiple available)
- Detail level (summary, standard, detailed)
- Language preference for output

**Given** `RSS_AI__QUALITY=fast` is configured
**Then** transformations use faster but lower-quality settings

**Given** `RSS_AI__QUALITY=quality` is configured
**Then** transformations use slower but higher-quality settings

---

### Story 4.12: Graceful Degradation Without AI

**As a** power user (Marcus),
**I want** the system to work even if AI is unavailable,
**So that** core functionality isn't dependent on AI providers.

**Acceptance Criteria:**

**Given** the AI provider is unavailable or not configured
**When** I request a transformation
**Then** the system returns an error indicating AI is required
**And** the error suggests configuring an AI provider

**Given** the AI provider becomes unavailable mid-transformation
**When** the transformation job fails
**Then** it is queued for retry
**And** the transformation status shows "queued" with retry information

**Given** AI is unavailable
**Then** all non-AI features continue working:
- Subscriptions management
- Content aggregation
- Feed health monitoring

---

## Epic 5: Web Application & PWA

Users can manage their system through a polished, responsive web interface. Marcus accesses a dark-mode dashboard, reads transformed articles, installs as PWA, and has full system visibility.

### Story 5.1: Implement App Shell and Layout

**As a** power user (Marcus),
**I want** a responsive application shell with navigation,
**So that** I can navigate between different views efficiently.

**Acceptance Criteria:**

**Given** I access the web application
**Then** the app shell renders with:
- Collapsible sidebar (240px expanded, 64px collapsed)
- Header with health banner
- Main content area
- Dismissable context panel (340px)

**Given** I press `[` on keyboard
**Then** the sidebar toggles between expanded and collapsed states

**Given** I press `]` on keyboard
**Then** the context panel toggles visibility

**Given** I collapse or expand panels
**Then** the state is persisted to localStorage
**And** restored on next visit

**Given** I view on mobile (< 768px)
**Then** sidebar becomes a hamburger menu
**And** context panel becomes a bottom sheet

---

### Story 5.2: Implement Dashboard View

**As a** power user (Marcus),
**I want** a dashboard showing system health at a glance,
**So that** I can quickly verify everything is working.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I navigate to the dashboard (`/`)
**Then** I see:
- Health banner showing system status (healthy/degraded/unhealthy)
- Stats grid with: total subscriptions, active feeds, error count, queue depth
- Recent content items (last 5)
- Active transformations (if any)

**Given** all feeds are healthy
**Then** the health banner shows "All systems healthy" in success green

**Given** some feeds have errors
**Then** the health banner shows count of issues in warning amber
**And** clicking the banner navigates to error details

**Given** the dashboard loads
**Then** it completes within 3 seconds (NFR3)

---

### Story 5.3: Implement Subscriptions List View

**As a** power user (Marcus),
**I want** a view showing all my subscriptions,
**So that** I can manage my content sources.

**Acceptance Criteria:**

**Given** I navigate to `/subscriptions`
**Then** I see a grid of SubscriptionCard components
**And** each card shows: icon, name, status badge, item count, last fetched time

**Given** I hover over a subscription card
**Then** action buttons appear: Transform, Edit, Delete

**Given** I click "Add Subscription" button
**Then** a modal opens for adding new subscriptions

**Given** I filter by tag or status
**Then** the subscription list updates immediately
**And** URL query params update for shareable links

---

### Story 5.4: Implement Add Subscription Modal

**As a** power user (Marcus),
**I want** a modal for adding new subscriptions,
**So that** I can subscribe to new content sources.

**Acceptance Criteria:**

**Given** I open the add subscription modal
**Then** I see:
- URL input field with paste detection
- Source type selector (auto-detected from URL)
- Preview section (populated after URL validation)
- Tag selector/creator
- Polling frequency selector

**Given** I paste a valid YouTube channel URL
**Then** the system auto-detects source type
**And** fetches and displays channel preview (name, icon, recent videos)

**Given** I paste an invalid URL
**Then** an inline error message appears
**And** the save button remains disabled

**Given** I click "Save"
**Then** the subscription is created
**And** the modal closes
**And** the subscription appears in the list

---

### Story 5.5: Implement Content Feed View

**As a** power user (Marcus),
**I want** a view showing aggregated content,
**So that** I can browse all my content in one place.

**Acceptance Criteria:**

**Given** I navigate to `/content`
**Then** I see a chronological list of content items
**And** each item shows: thumbnail, title, source, published date, content type badge

**Given** I scroll to the bottom
**Then** more content loads automatically (infinite scroll)

**Given** I click on a content item
**Then** a detail view opens showing full description and actions

**Given** I click "Transform" on a video item
**Then** a transformation request is initiated
**And** I see confirmation with queue position

---

### Story 5.6: Implement Article Reader View

**As a** power user (Marcus),
**I want** to read transformed articles in the web interface,
**So that** I can consume content directly in the app.

**Acceptance Criteria:**

**Given** I have a completed article transformation
**When** I click to view the transformed content
**Then** I see a clean reading view with:
- Article title
- Source link to original content
- Formatted markdown content
- Reading time estimate

**Given** I am reading an article
**Then** the typography is optimized for reading
**And** dark mode is respected
**And** code blocks (if any) are syntax highlighted

**Given** I click "Back" or press Escape
**Then** I return to the previous view

---

### Story 5.7: Implement Theme Toggle

**As a** power user (Marcus),
**I want** to toggle between dark and light themes,
**So that** I can use my preferred visual style.

**Acceptance Criteria:**

**Given** I access the application
**Then** dark theme is applied by default
**And** the system respects `prefers-color-scheme` media query

**Given** I click the theme toggle in settings/header
**Then** the theme switches between dark and light
**And** all components update their colors accordingly
**And** the preference is saved to localStorage

**Given** I have previously set a theme preference
**When** I return to the application
**Then** my preference is restored

---

### Story 5.8: Implement System Health Dashboard

**As a** power user (Marcus),
**I want** a detailed system health view,
**So that** I can diagnose and resolve issues.

**Acceptance Criteria:**

**Given** I navigate to `/health` or click the health banner
**Then** I see:
- Overall system status
- Feed health breakdown (healthy, warning, error counts)
- List of feeds with issues, sorted by severity
- Transformation queue status
- System resource usage (if available)

**Given** a feed has errors
**Then** I see the ErrorAlert component with:
- Error type and message
- Affected subscription
- Timestamp
- Retry button

**Given** I click "Retry" on an error
**Then** a retry job is queued
**And** the UI shows optimistic update

---

### Story 5.9: Implement Queue View in Context Panel

**As a** power user (Marcus),
**I want** to see the transformation queue in the context panel,
**So that** I always know what's processing.

**Acceptance Criteria:**

**Given** the context panel is visible
**Then** I see tabs for "Queue" and "Activity"

**Given** I view the Queue tab
**Then** I see TransformationProgress components for each item
**And** processing items show progress bar and current step
**And** queued items show queue position

**Given** a transformation completes
**Then** it moves from Queue to Activity
**And** a toast notification appears

**Given** I click on a queue item
**Then** I see full details including content info and timestamps

---

### Story 5.10: Implement PWA Support

**As a** power user (Marcus),
**I want** to install the app to my device home screen,
**So that** I can access it like a native app.

**Acceptance Criteria:**

**Given** I visit the web application
**Then** a web app manifest is served at `/manifest.json`
**And** it includes: name, short_name, icons, start_url, display: standalone, theme_color

**Given** a service worker is registered
**Then** static assets are cached for offline access
**And** the app shows cached content when offline

**Given** I click "Install" or use browser's install option
**Then** the app is added to my home screen
**And** it opens in standalone mode without browser chrome

**Given** the app is installed
**Then** the icon appears on my device home screen with the app icon

---

### Story 5.11: Implement Responsive Mobile Experience

**As a** power user (Marcus),
**I want** the app to work well on mobile devices,
**So that** I can check status on my phone.

**Acceptance Criteria:**

**Given** I view the app on mobile (< 768px)
**Then** the layout adapts:
- Single column layout
- Bottom navigation bar (Dashboard, Subscriptions, Content, Settings)
- Sidebar becomes hamburger menu
- Context panel becomes full-screen sheet

**Given** I tap on interactive elements
**Then** touch targets are at least 44x44px (NFR28)

**Given** I use the app on a 320px wide screen
**Then** all content remains usable (NFR27)

---

### Story 5.12: Implement Accessibility Features

**As a** user with accessibility needs,
**I want** the app to be accessible,
**So that** I can use it with assistive technologies.

**Acceptance Criteria:**

**Given** I navigate using keyboard only
**Then** all interactive elements are focusable via Tab
**And** focus indicators are clearly visible (2px accent ring)
**And** skip links allow jumping to main content

**Given** I use a screen reader
**Then** all interactive elements have appropriate ARIA labels
**And** dynamic content updates are announced via live regions
**And** page structure uses semantic HTML landmarks

**Given** I have `prefers-reduced-motion` enabled
**Then** animations are minimized or disabled

**Given** I run automated accessibility tests
**Then** the app passes WCAG 2.1 AA criteria (NFR29)

---

## Epic 6: Content Delivery & Integrations

Users can consume content through their preferred apps (Plex, podcast apps, *arr stack). Sofia's transformed content appears in Plex, Marcus's podcast feed works in any podcatcher, and the system integrates with existing *arr stack.

**MVP Scope Note:** Stories 6.1-6.3 (podcast feed generation) are deferred to v1.1 pending TTS implementation (per PRD v1.1). MVP focuses on Plex/Jellyfin integration and *arr stack support using text-transformed content.

### Story 6.1: Generate RSS 2.0 Podcast Feeds **[DEFERRED TO v1.1]**

**As a** power user (Marcus),
**I want** the system to generate valid podcast feeds,
**So that** I can subscribe to transformed content in any podcast app.

**Deferred Rationale:** Podcast feeds require audio enclosures. MVP delivers subtitle→article transformation (text-to-text). Audio transformation (TTS) is planned for v1.1 per PRD.

**Acceptance Criteria:**

**Given** transformed audio content exists
**When** I GET `/api/feeds/podcast/{feed_id}`
**Then** a valid RSS 2.0 feed is returned with:
- Channel metadata (title, description, link, image)
- iTunes namespace extensions (itunes:author, itunes:category, etc.)
- Episode items with enclosure URLs to audio files

**Given** a podcatcher requests the feed
**Then** the feed passes RSS 2.0 validation (NFR15)
**And** the feed includes required iTunes podcast extensions (NFR16)

**Given** I generate a feed
**Then** the response completes within 2 seconds for feeds under 100 items (NFR7)

---

### Story 6.2: Create Personal Podcast Feed URLs **[DEFERRED TO v1.1]**

**As a** power user (Marcus),
**I want** to get podcast feed URLs for use in my podcast apps,
**So that** Sofia and I can subscribe in Pocket Casts or Overcast.

**Deferred Rationale:** Depends on Story 6.1. Podcast feed URLs require audio content generation capability planned for v1.1.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I GET `/api/feeds/podcast`
**Then** I see a list of available podcast feeds including:
- All-content feed (everything transformed to audio)
- Per-subscription feeds
- Per-tag feeds

**Given** a feed URL
**When** I copy it to a podcatcher app
**Then** the app can subscribe and receive new episodes

**Given** I want a private feed URL
**When** I generate a feed URL
**Then** it includes a secure token for authentication
**And** the token can be regenerated if compromised

---

### Story 6.3: Include Episode Metadata in Feeds **[DEFERRED TO v1.1]**

**As a** household consumer (Sofia),
**I want** podcast episodes to have proper metadata,
**So that** they display correctly in my podcast app.

**Deferred Rationale:** Depends on Story 6.1. Episode metadata enhancement is contingent on podcast feed generation capability in v1.1.

**Acceptance Criteria:**

**Given** an episode in the podcast feed
**Then** it includes:
- Title from original content
- Description/show notes
- Duration in HH:MM:SS format
- Episode artwork (thumbnail from original)
- Publication date
- Enclosure with audio URL, type, and length

**Given** the original content is a YouTube video
**Then** the episode shows the video thumbnail as artwork
**And** the description includes link to original video

---

### Story 6.4: Serve Media Files for Plex

**As a** household consumer (Sofia),
**I want** transformed content to appear in Plex,
**So that** I can watch/listen on my TV.

**Acceptance Criteria:**

**Given** transformed content exists
**When** the media is organized in the Plex library path
**Then** files follow Plex naming conventions:
- Audio: `{show}/{show} - S01E{n} - {title}.mp3`
- Or podcast-style: `{show}/{title}.mp3`

**Given** Plex scans the library
**Then** content is recognized and indexed correctly
**And** metadata is populated from accompanying .nfo files or embedded tags

**Given** I configure a Plex library path
**Then** transformed content is automatically copied/symlinked there

---

### Story 6.5: Serve Media Files for Jellyfin

**As a** household consumer (Sofia),
**I want** transformed content to appear in Jellyfin,
**So that** I can use my preferred media server.

**Acceptance Criteria:**

**Given** transformed content exists
**When** the media is organized in the Jellyfin library path
**Then** files follow Jellyfin-compatible naming conventions

**Given** Jellyfin scans the library
**Then** content is recognized and indexed correctly (NFR20)

**Given** I configure a Jellyfin library path
**Then** transformed content is automatically organized there

---

### Story 6.6: Organize Content into Per-User Libraries

**As a** power user (Marcus),
**I want** to organize content into per-user libraries,
**So that** Sofia has her own clean library without seeing everything.

**Acceptance Criteria:**

**Given** I create a library configuration
**When** I POST `/api/libraries` with:
```json
{
  "name": "Sofia's Feeds",
  "subscriptions": ["uuid1", "uuid2"],
  "output_path": "/media/sofia-feeds"
}
```
**Then** a library is created
**And** transformed content from those subscriptions goes to that path

**Given** content is transformed for a subscription in multiple libraries
**Then** it is copied/symlinked to each library path

**Given** Sofia opens Plex
**Then** she only sees content in her assigned library

---

### Story 6.7: Sonarr API Integration - Read

**As a** power user (Marcus),
**I want** to read my Sonarr library,
**So that** I can understand what TV content I already have.

**Acceptance Criteria:**

**Given** Sonarr connection is configured
**When** I GET `/api/integrations/sonarr/series`
**Then** the system proxies to Sonarr API and returns series list
**And** the API follows Sonarr specification (NFR17)

**Given** I configure Sonarr connection
**Then** I provide: URL, API key
**And** the connection is tested on save

**Given** Sonarr is unreachable
**Then** the integration gracefully degrades
**And** an error message explains the issue

---

### Story 6.8: Radarr API Integration - Read

**As a** power user (Marcus),
**I want** to read my Radarr library,
**So that** I can understand what movie content I already have.

**Acceptance Criteria:**

**Given** Radarr connection is configured
**When** I GET `/api/integrations/radarr/movies`
**Then** the system proxies to Radarr API and returns movie list
**And** the API follows Radarr specification (NFR18)

**Given** I configure Radarr connection
**Then** I provide: URL, API key
**And** the connection is tested on save

---

### Story 6.9: External API Authentication

**As a** developer (Jordan),
**I want** to authenticate to the RSS-Remastered API,
**So that** I can build automations against it.

**Acceptance Criteria:**

**Given** I have an API key
**When** I make API requests with `Authorization: Bearer {key}` header
**Then** the request is authenticated

**Given** I make a request without authentication
**Then** 401 Unauthorized is returned (NFR24)

**Given** I make a request with an invalid key
**Then** 401 Unauthorized is returned
**And** the error message is generic (doesn't reveal if key exists)

---

### Story 6.10: Content Metadata API

**As a** developer (Jordan),
**I want** to retrieve content metadata via API,
**So that** I can build integrations and dashboards.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I GET `/api/content`
**Then** I receive content items with full metadata

**Given** I GET `/api/content/{id}`
**Then** I receive detailed content item including transformation status

**Given** I want specific fields only
**When** I GET `/api/content?fields=id,title,status`
**Then** only requested fields are returned

---

### Story 6.11: Subscription Status API

**As a** developer (Jordan),
**I want** to retrieve subscription status via API,
**So that** I can monitor feed health programmatically.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I GET `/api/subscriptions`
**Then** I receive subscriptions with status information

**Given** I GET `/api/subscriptions/{id}/health`
**Then** I receive detailed health information:
- Current status
- Last successful fetch
- Error history
- Next scheduled fetch

**Given** I GET `/api/health`
**Then** I receive overall system health summary suitable for monitoring

---

### Story 6.12: Webhook Notifications for Integrations

**As a** developer (Jordan),
**I want** webhook notifications for events,
**So that** I can trigger external automations.

**Acceptance Criteria:**

**Given** I configure a webhook endpoint
**When** I POST `/api/webhooks` with:
```json
{
  "url": "https://my-service.com/webhook",
  "events": ["transformation.completed", "feed.error"]
}
```
**Then** a webhook subscription is created

**Given** a subscribed event occurs
**Then** a POST request is sent to the webhook URL
**And** the payload includes event type, timestamp, and relevant data

**Given** the webhook endpoint is unreachable
**Then** retries are attempted with backoff
**And** persistent failures are logged

---

## Epic 7: API Security & Notifications

Users have secure API access and optional push notifications. Marcus generates API keys for external integrations, system is secure, and users can opt-in to notifications.

### Story 7.1: API Key Generation

**As a** power user (Marcus),
**I want** to generate API keys for external access,
**So that** I can integrate with external services securely.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I POST `/api/settings/api-keys` with `{"name": "Home Assistant"}`
**Then** an API key is generated using cryptographically secure randomness (NFR22)
**And** the key is displayed once (it won't be shown again)
**And** the key is stored as a hash (NFR23)
**And** the response includes: id, name, created_at, last_used_at, prefix (first 8 chars)

**Given** the key is generated
**Then** it uses at least 32 bytes of entropy
**And** the raw key is never logged or stored

---

### Story 7.2: API Key Management

**As a** power user (Marcus),
**I want** to view and revoke API keys,
**So that** I can manage access to my system.

**Acceptance Criteria:**

**Given** I am authenticated
**When** I GET `/api/settings/api-keys`
**Then** I see a list of API keys with: id, name, prefix, created_at, last_used_at
**And** the full key value is NOT returned

**Given** I want to revoke a key
**When** I DELETE `/api/settings/api-keys/{id}`
**Then** the key is immediately invalidated
**And** requests using that key return 401

**Given** I want to regenerate a key
**When** I POST `/api/settings/api-keys/{id}/regenerate`
**Then** a new key is generated with the same name
**And** the old key is invalidated
**And** the new key is displayed once

---

### Story 7.3: YAML Configuration File Support

**As a** self-hoster,
**I want** to configure the system via a YAML file,
**So that** I can manage configuration as code.

**Acceptance Criteria:**

**Given** a `config.yaml` file exists in the config directory
**When** the application starts
**Then** settings are loaded from the YAML file
**And** environment variables override YAML values
**And** the file is watched for changes (optional hot reload)

**Given** the YAML file contains:
```yaml
ai:
  provider: ollama
  model: llama3
subscriptions:
  default_polling_interval: 30
```
**Then** these settings are applied to the application

**Given** the YAML contains secrets
**Then** secrets are NOT logged or exposed via API (NFR25)

---

### Story 7.4: Auto-Generate VAPID Keys

**As a** self-hoster,
**I want** VAPID keys auto-generated on first run,
**So that** push notifications work without manual setup.

**Acceptance Criteria:**

**Given** the application starts for the first time
**When** no VAPID keys exist
**Then** VAPID public/private key pair is generated
**And** keys are stored securely in the data directory
**And** a log message indicates keys were generated

**Given** VAPID keys already exist
**When** the application starts
**Then** existing keys are loaded
**And** no new keys are generated

**Given** I want to regenerate keys
**When** I delete the existing key file and restart
**Then** new keys are generated
**And** existing push subscriptions are invalidated

---

### Story 7.5: Push Notification Subscription

**As a** power user (Marcus),
**I want** to subscribe to push notifications,
**So that** I can receive alerts on my devices.

**Acceptance Criteria:**

**Given** I am authenticated and have granted notification permission
**When** I POST `/api/notifications/subscribe` with push subscription data
**Then** the subscription is stored
**And** the endpoint is associated with my session

**Given** I have multiple devices
**When** I subscribe from each device
**Then** each subscription is stored separately
**And** notifications are sent to all subscribed devices

**Given** I want to unsubscribe
**When** I DELETE `/api/notifications/subscribe`
**Then** the subscription is removed
**And** no more notifications are sent to that endpoint

---

### Story 7.6: Transformation Completion Notifications

**As a** power user (Marcus),
**I want** to receive notifications when transformations complete,
**So that** I know when my content is ready.

**Acceptance Criteria:**

**Given** I have opted in to transformation notifications
**When** a transformation completes successfully
**Then** a push notification is sent with:
- Title: "Transformation Complete"
- Body: Content title
- Action: Link to view transformed content

**Given** a transformation fails
**When** I have opted in to notifications
**Then** a push notification is sent with:
- Title: "Transformation Failed"
- Body: Content title and brief error
- Action: Link to retry or view details

**Given** I have not opted in
**Then** no notifications are sent

---

### Story 7.7: Feed Health Alert Notifications

**As a** power user (Marcus),
**I want** to receive notifications when feeds have issues,
**So that** I can address problems promptly.

**Acceptance Criteria:**

**Given** I have opted in to health notifications
**When** a feed enters error state
**Then** a push notification is sent with:
- Title: "Feed Health Alert"
- Body: Subscription name and error summary
- Action: Link to health dashboard

**Given** multiple feeds fail simultaneously
**Then** notifications are batched into a summary
**And** the summary indicates count of affected feeds

**Given** a feed recovers from error state
**When** I have health notifications enabled
**Then** an optional recovery notification is sent

---

### Story 7.8: Notification Preferences

**As a** power user (Marcus),
**I want** to configure notification preferences,
**So that** I only receive notifications I care about.

**Acceptance Criteria:**

**Given** I access notification settings
**Then** I can configure:
- Enable/disable transformation notifications
- Enable/disable health alert notifications
- Quiet hours (no notifications during specified times)
- Notification frequency (immediate, batched hourly, daily digest)

**Given** I save notification preferences
**Then** they are persisted and applied immediately

**Given** quiet hours are configured
**When** an event occurs during quiet hours
**Then** the notification is queued for after quiet hours

---

### Story 7.9: HTTPS Support

**As a** self-hoster,
**I want** HTTPS support for secure communication,
**So that** my data is encrypted in transit.

**Acceptance Criteria:**

**Given** I configure `RSS_HTTPS_ENABLED=true`
**When** the application starts
**Then** it serves over HTTPS using provided certificate files

**Given** `RSS_HTTPS_CERT` and `RSS_HTTPS_KEY` are configured
**Then** the application uses these files for TLS

**Given** I use a reverse proxy for HTTPS termination
**When** `RSS_TRUST_PROXY=true` is set
**Then** the application trusts X-Forwarded headers
**And** generates correct URLs with HTTPS scheme

---

### Story 7.10: Security Headers

**As a** security-conscious user,
**I want** appropriate security headers on all responses,
**So that** the application follows security best practices.

**Acceptance Criteria:**

**Given** any HTTP response is returned
**Then** it includes security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`

**Given** the application serves the web UI
**Then** Content-Security-Policy header is included
**And** it restricts script sources appropriately

---

### Story 7.11: Rate Limiting for API

**As a** system operator,
**I want** rate limiting on API endpoints,
**So that** the system is protected from abuse.

**Acceptance Criteria:**

**Given** an API client makes requests
**When** they exceed 100 requests per minute
**Then** subsequent requests receive 429 Too Many Requests
**And** the response includes Retry-After header

**Given** rate limiting is triggered
**Then** the event is logged
**And** legitimate traffic from other clients is unaffected

**Given** I want to adjust rate limits
**Then** limits are configurable via settings

---

### Story 7.12: Audit Logging

**As a** security-conscious user,
**I want** security-relevant events logged,
**So that** I can review access and changes.

**Acceptance Criteria:**

**Given** a security-relevant event occurs
**Then** it is logged with:
- Timestamp
- Event type
- Actor (API key ID or session)
- Resource affected
- Outcome (success/failure)

**Given** security events include:
- API key creation/deletion
- Failed authentication attempts
- Settings changes
- Subscription modifications
**Then** each event type is logged appropriately

**Given** I review audit logs
**Then** sensitive data (API keys, passwords) is NOT included in logs

---

## Summary

**Total Epics:** 7
**Total Stories:** 76
**Stories in MVP:** 73
**Stories Deferred to v1.1:** 3 (Epic 6 Stories 6.1-6.3)

### MVP Scope

The MVP delivers complete subtitle→article transformation functionality across 7 epics with 73 stories. The system provides:

- Complete RSS aggregation and subscription management
- Intelligent text-to-text AI transformation (subtitle→article)
- Plex/Jellyfin media server integration
- *arr stack compatibility (Sonarr/Radarr)
- Full web UI with PWA support
- API security and notifications

### Deferred to v1.1

**Epic 6 Stories 6.1-6.3:** Podcast feed generation requiring audio transformation (TTS) per PRD v1.1 roadmap. These stories depend on article→audio capability planned for the next version.

### Implementation Readiness

This epic breakdown has been validated for implementation readiness. See [Implementation Readiness Report](implementation-readiness-report-2025-12-14.md) for detailed assessment.
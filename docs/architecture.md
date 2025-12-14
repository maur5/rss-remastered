---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - docs/prd.md
  - docs/ux-design-specification.md
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2025-12-13'
project_name: 'rss-remastered'
user_name: 'Mo'
date: '2025-12-13'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**

The PRD defines 58 functional requirements across 9 categories:

| Category | FR Range | Key Capabilities |
|----------|----------|------------------|
| Subscription Management | FR1-9 | YouTube/RSS/podcast subscriptions, OPML import/export, tagging |
| Content Aggregation | FR10-18 | Auto-fetch, metadata storage, chronological feed, search, read state |
| Content Transformation | FR19-27 | Subtitle extraction, AI transposition, queue management, on-demand/scheduled |
| Web UI Serving | FR28-33 | Responsive PWA, article reader, dark/light themes |
| Podcast Feed Generation | FR34-37 | RSS 2.0 + iTunes extensions, podcatcher compatibility |
| Media Server Integration | FR38-40 | Plex/Jellyfin serving, per-user libraries |
| *arr Stack Integration | FR41-45 | Sonarr/Radarr API read, API key auth |
| System Health | FR46-51 | Feed health display, error details, retry, queue status |
| Configuration | FR52-58 | API keys, AI provider settings, YAML config, VAPID auto-gen |

**Architecturally significant requirements:**
- **FR19-27**: Transformation pipeline is the core differentiator - requires robust queue, progress tracking, and failure handling
- **FR38-40**: Multi-destination serving (Plex, Jellyfin, podcast feeds) requires abstracted delivery layer
- **FR41-45**: *arr API compatibility constrains API design patterns
- **FR56**: Graceful degradation without AI - transformation is enhancement, not dependency

**Non-Functional Requirements:**

36 NFRs define the quality attributes:

| Category | Key Constraints |
|----------|-----------------|
| **Performance** | 30s startup, 2GB RAM cap, <3s initial load, <200ms API response |
| **Reliability** | Network failure recovery, malformed input handling, auto-retry with backoff |
| **Integration** | RSS 2.0 validator compliance, Sonarr/Radarr API spec adherence, OPML 2.0 |
| **Security** | Cryptographically secure API keys, hashed storage, authenticated endpoints |
| **Usability** | 44x44px touch targets, WCAG AA contrast, human-readable errors |
| **Deployment** | Single docker-compose command, reverse proxy support, JSON logging |

**Scale & Complexity:**

- **Primary domain:** Full-stack Web Application with Media Processing Pipeline
- **Complexity level:** Medium (AI enhancement layer, no regulatory overhead)
- **Estimated architectural components:** 8-12 major modules

### UX Architectural Implications

From the UX specification:

| UX Requirement | Architectural Implication |
|----------------|--------------------------|
| Real-time transformation progress | Event-driven status updates (polling → SSE) |
| Collapsible panels with state persistence | Client-side state management + localStorage |
| PWA installability | Service worker, manifest.json, HTTPS |
| Multi-channel delivery (Web, Plex, podcatcher) | Abstracted content serving layer |
| "Calm technology" error handling | Structured error types with recovery actions |
| WCAG 2.1 AA compliance | Semantic HTML, ARIA, keyboard navigation |

### Technical Constraints & Dependencies

**Explicit Constraints (from PRD):**
- Python 3.11+ backend with FastAPI
- Modern JS/TS SPA frontend (framework TBD)
- SQLite for MVP (PostgreSQL path for scale)
- Single Docker container deployment
- YAML configuration, JSON API format
- uv for dependency management

**External Dependencies:**
- yt-dlp for YouTube content extraction
- FFmpeg for media processing
- AI provider (local or remote) for intelligent transposition

### Cross-Cutting Concerns Identified

| Concern | Affected Components | Architectural Strategy |
|---------|--------------------|-----------------------|
| **Queue Management** | Transformation, aggregation, delivery | Shared task queue with priority and status |
| **Error Handling** | All external integrations | Categorized errors with recovery actions |
| **Authentication** | API, Web UI, *arr integration | API key-based, session management for UI |
| **Rate Limiting** | YouTube fetching, AI providers | Delegated to libraries + internal throttling |
| **Real-time Status** | Dashboard, transformation progress, health | Event bus pattern (polling MVP → SSE growth) |
| **Graceful Degradation** | AI features, external services | Feature flags, fallback behaviors |
| **Logging & Observability** | All components | Structured JSON logging, health endpoints |

## Starter Template Evaluation

### Primary Technology Domains

- **Backend:** Python 3.11+ with FastAPI (no starter template - clean start)
- **Frontend:** Vite + React + TypeScript SPA with shadcn/ui

### Starter Options Considered

**Frontend Options Evaluated:**

| Option | Pros | Cons | Fit |
|--------|------|------|-----|
| **Vite + React + TS** | Simple, fast, static output | Manual router/data-fetching setup | ✅ Best fit |
| Next.js | SSR, file-based routing, image optimization | Overkill for self-hosted SPA, complex build output | ❌ Over-engineered |
| Create React App | Familiar | Deprecated, slow, no longer recommended | ❌ Outdated |

**Backend Options Evaluated:**

| Option | Pros | Cons | Fit |
|--------|------|------|-----|
| **FastAPI from scratch** | Full control, no inherited opinions | Manual setup | ✅ Best fit |
| FastAPI starter templates | Quick start | Often opinionated, may not fit monolith-first | ❌ Adds constraints |

### Selected Approach

**Frontend: Vite + React + TypeScript + shadcn/ui + Tailwind CSS v4**

**Rationale:**
- Pure SPA is sufficient - no SSR/SEO needs for self-hosted admin dashboard
- Static build output trivially served by FastAPI
- Excellent shadcn/ui support with Tailwind v4
- Simpler mental model than Next.js for API-first architecture
- Fast HMR development experience

**Next.js Trade-off Analysis:**

Next.js features not needed for this project:
- SSR/SSG - No public pages, no SEO requirements
- API Routes - FastAPI serves all API endpoints
- Edge middleware - Single container deployment
- Image optimization - Minimal image needs (feed icons only)

Manual additions required with Vite (trivial):
- `react-router-dom` for routing
- TanStack Query for data fetching/caching

**Initialization Commands:**

```bash
# Create Vite React TypeScript project
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install

# Install Tailwind CSS v4 with Vite plugin
npm install tailwindcss @tailwindcss/vite

# Initialize shadcn/ui
npx shadcn@latest init
```

**Backend: FastAPI from scratch with domain-based structure**

**Rationale:**
- Monolith-first architecture benefits from domain-based module structure
- No starter template baggage - structure emerges from requirements
- Follows Netflix Dispatch pattern recommended by community
- Clean separation: each domain (subscriptions, transformations, feeds) gets its own module

**Project Structure Pattern:**

```
src/
├── subscriptions/
│   ├── router.py
│   ├── schemas.py
│   ├── models.py
│   ├── service.py
│   └── exceptions.py
├── transformations/
│   ├── router.py
│   ├── schemas.py
│   ├── models.py
│   ├── service.py
│   ├── pipeline.py
│   └── exceptions.py
├── feeds/
│   ├── router.py
│   ├── schemas.py
│   └── service.py
├── core/
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   └── exceptions.py
└── main.py
```

### Architectural Decisions Established by Stack

**Language & Runtime:**
- Frontend: TypeScript (strict mode)
- Backend: Python 3.11+ with type hints

**Styling Solution:**
- Tailwind CSS v4 with @tailwindcss/vite plugin
- shadcn/ui component library (copy-paste architecture)
- CSS custom properties for theming

**Build Tooling:**
- Frontend: Vite (esbuild for dev, Rollup for prod)
- Backend: uv for dependency management

**Testing Framework:**
- Frontend: Vitest (Vite-native, Jest-compatible API)
- Backend: pytest + pytest-asyncio + httpx

**Code Organization:**
- Frontend: Feature-based folders with shadcn/ui components in `src/components/ui/`
- Backend: Domain-based modules (subscriptions, transformations, feeds, core)

**Development Experience:**
- Vite HMR for frontend
- FastAPI auto-reload for backend
- Path aliases (`@/` for frontend imports)

**Note:** Project initialization using these commands should be the first implementation story.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Database layer and ORM choice
- Background task processing strategy
- Configuration management approach

**Important Decisions (Shape Architecture):**
- AI provider abstraction
- Frontend state management
- Logging strategy

**Deferred Decisions (Post-MVP):**
- Additional AI providers beyond OpenAI/Ollama
- SSE for real-time updates (polling for MVP)
- PostgreSQL migration (SQLite sufficient for MVP)

### Data Architecture

**ORM:** SQLAlchemy 2.0 with async support
- Explicit separation of DB models and Pydantic schemas
- Type-safe queries with modern 2.0 syntax
- Well-documented patterns for AI agent implementation

**Migrations:** Alembic
- Auto-generation from model changes
- Version-controlled migration history
- Clear path to PostgreSQL when needed

**Database:** SQLite (MVP) → PostgreSQL (scale)
- Single file, zero configuration for MVP
- Sufficient for household-scale usage
- Migration path documented but not premature

### Background Task Processing

**Approach:** In-process asyncio + SQLite job table

**Rationale:**
- No external dependencies (Redis not required)
- Jobs persist across restarts via database
- Single container deployment preserved
- Sufficient throughput for target scale

**Job Table Schema:**
```python
class Job(Base):
    id: Mapped[int]
    task_name: Mapped[str]          # e.g., "transform_content"
    payload: Mapped[str]            # JSON arguments
    status: Mapped[str]             # pending/running/completed/failed
    priority: Mapped[int]           # Queue ordering
    created_at: Mapped[datetime]
    started_at: Mapped[datetime | None]
    completed_at: Mapped[datetime | None]
    error: Mapped[str | None]
    retries: Mapped[int]
```

**Scale Path:** If Redis needed later, migrate to ARQ with minimal code changes.

### AI Provider Integration

**Native Support:**
- **OpenAI SDK** - Covers OpenAI, Azure OpenAI, and OpenAI-compatible endpoints
- **Ollama** - Local model support via direct HTTP API

**Configuration:**
```python
class AIConfig:
    provider: Literal["openai", "ollama", "none"]
    base_url: str | None      # Override for OpenAI-compatible endpoints
    model: str
    api_key: str | None
```

**Extensibility:** Users wanting other providers (Anthropic, Gemini) can:
1. Wait for native support
2. Run LiteLLM as sidecar, point `base_url` at it

**Graceful Degradation:** `NoOpProvider` returns clear error when AI unconfigured.

### Frontend Architecture

**State Management:**
- **TanStack Query** - Server state (subscriptions, transformations, queue)
- **Zustand** - UI state (sidebar collapsed, panel visibility, theme)

**Rationale:**
- TanStack Query handles caching, refetching, optimistic updates
- Zustand is minimal (~1KB) for localStorage-backed UI preferences
- Clean separation of concerns

**Data Fetching Pattern:**
```typescript
// Server state via TanStack Query
const { data: subscriptions } = useQuery({
  queryKey: ['subscriptions'],
  queryFn: () => api.getSubscriptions()
})

// UI state via Zustand (persisted to localStorage)
const { sidebarCollapsed, toggleSidebar } = useUIStore()
```

### Logging & Observability

**Library:** structlog

**Output Strategy:**
- JSON format to stdout/stderr (production)
- Human-readable format (development)
- Docker captures logs natively
- Compatible with `docker compose logs`

**Log Levels:** DEBUG, INFO, WARNING, ERROR
**Structured Fields:** timestamp, level, event, context (request_id, user_id, etc.)

**Example Output:**
```json
{"timestamp": "2025-12-13T10:30:00Z", "level": "info", "event": "transformation_started", "job_id": 42, "content_id": 123}
```

### Configuration Management

**Library:** Pydantic Settings

**Priority Order (highest wins):**
1. Environment variables (`RSS_` prefix)
2. YAML config file (bind-mounted)
3. Database (user preferences from Web UI)
4. Defaults

**Config Categories:**

| Category | Source | Examples |
|----------|--------|----------|
| **System config** | Env vars, YAML | AI provider, database path, log level |
| **User preferences** | Web UI → DB | Theme, sidebar state, notifications |
| **Application data** | Web UI → DB | Subscriptions, transform rules |

**Example Configuration:**
```yaml
# config.yaml (bind-mounted into container)
ai:
  provider: ollama
  base_url: http://host.docker.internal:11434
  model: llama3.2

logging:
  level: info
  format: json
```

```bash
# docker-compose.yml - env vars override YAML
environment:
  - RSS_AI__PROVIDER=openai
  - RSS_AI__API_KEY=sk-...
```

### Decision Impact Analysis

**Implementation Sequence:**
1. Project scaffolding (Vite + FastAPI)
2. Database setup (SQLAlchemy + Alembic)
3. Configuration system (Pydantic Settings)
4. Job queue infrastructure
5. Core domain modules
6. AI provider abstraction
7. Frontend shell with state management

**Cross-Component Dependencies:**
- Job queue depends on database
- AI providers depend on configuration
- Frontend state depends on API contracts
- Logging is cross-cutting (inject early)

## Implementation Patterns & Consistency Rules

These patterns ensure AI agents writing code for different parts of the system produce compatible, consistent output.

### Naming Patterns

**Database Naming (SQLAlchemy):**

| Element | Convention | Example |
|---------|------------|---------|
| Tables | snake_case, plural | `subscriptions`, `content_items`, `jobs` |
| Columns | snake_case | `created_at`, `feed_url`, `is_active` |
| Foreign keys | `{table_singular}_id` | `subscription_id`, `content_item_id` |
| Indexes | `ix_{table}_{column}` | `ix_subscriptions_url` |
| Constraints | `{type}_{table}_{columns}` | `uq_subscriptions_url`, `fk_content_items_subscription_id` |

**API Naming (FastAPI):**

| Element | Convention | Example |
|---------|------------|---------|
| Endpoints | lowercase, hyphens, plural | `/api/subscriptions`, `/api/content-items` |
| Path params | snake_case | `/subscriptions/{subscription_id}` |
| Query params | snake_case | `?feed_type=youtube&is_active=true` |
| JSON fields | snake_case | `{ "created_at": "...", "feed_url": "..." }` |

**Frontend Code Naming:**

| Element | Convention | Example |
|---------|------------|---------|
| Components | PascalCase | `SubscriptionCard`, `TransformQueue` |
| Component files | PascalCase.tsx | `SubscriptionCard.tsx` |
| Hooks | camelCase, use prefix | `useSubscriptions`, `useUIStore` |
| Functions | camelCase | `getSubscriptions()`, `formatDate()` |
| Variables | camelCase | `const feedUrl`, `let isLoading` |
| Constants | SCREAMING_SNAKE_CASE | `const API_BASE_URL`, `const MAX_RETRIES` |

### API Response Patterns

**Success Responses:**
- Return data directly (no wrapper)
- Use appropriate HTTP status codes
- Include pagination in headers when needed

```python
# GET /api/subscriptions - returns list directly
[{"id": 1, "name": "Tech News", "url": "..."}, ...]

# GET /api/subscriptions/1 - returns object directly
{"id": 1, "name": "Tech News", "url": "..."}

# POST /api/subscriptions - returns created object
# Status: 201 Created
{"id": 2, "name": "New Feed", "url": "..."}

# DELETE /api/subscriptions/1
# Status: 204 No Content
```

**Error Responses:**
```python
{
  "detail": "Human-readable message for UI display",
  "code": "DOMAIN_ACTION_REASON",
  "context": {"field": "url", "value": "invalid"}  # optional
}
```

**Error Code Pattern:** `DOMAIN_ACTION_REASON`
- `SUBSCRIPTION_CREATE_INVALID_URL`
- `SUBSCRIPTION_CREATE_DUPLICATE`
- `TRANSFORM_QUEUE_AI_UNAVAILABLE`
- `AUTH_API_KEY_INVALID`
- `AUTH_API_KEY_MISSING`

**HTTP Status Codes:**

| Code | Usage |
|------|-------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Validation error, bad request |
| 401 | Unauthorized (missing/invalid auth) |
| 404 | Resource not found |
| 409 | Conflict (duplicate, state conflict) |
| 500 | Server error |

### Data Format Patterns

**Date/Time:**
- API: ISO 8601 strings, always UTC (`"2025-12-13T10:30:00Z"`)
- Database: UTC timestamps
- Frontend: Display in user's timezone, store references as UTC

**Booleans:**
- JSON: `true`/`false` (never `1`/`0` or strings)
- Query params: `?is_active=true` (string, parsed by FastAPI)

**Nulls:**
- Omit null fields from responses when possible
- Use `None` in Python, `null` in JSON, `undefined` in TypeScript for optional fields

### Project Structure Patterns

**Backend Structure:**
```
backend/
├── src/
│   ├── subscriptions/
│   │   ├── __init__.py
│   │   ├── router.py      # FastAPI routes
│   │   ├── schemas.py     # Pydantic models (API)
│   │   ├── models.py      # SQLAlchemy models (DB)
│   │   ├── service.py     # Business logic
│   │   └── exceptions.py  # Domain exceptions
│   ├── transformations/
│   ├── feeds/
│   ├── jobs/              # Background job system
│   ├── ai/                # AI provider abstraction
│   ├── core/
│   │   ├── config.py      # Pydantic Settings
│   │   ├── database.py    # SQLAlchemy setup
│   │   ├── dependencies.py # FastAPI dependencies
│   │   └── exceptions.py  # Base exceptions
│   └── main.py
├── tests/
│   ├── subscriptions/
│   │   ├── test_router.py
│   │   └── test_service.py
│   ├── conftest.py        # Shared fixtures
│   └── ...
├── alembic/
│   └── versions/
├── pyproject.toml
└── alembic.ini
```

**Frontend Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/            # shadcn/ui components
│   │   └── app/           # App-specific composed components
│   ├── features/
│   │   ├── subscriptions/
│   │   │   ├── SubscriptionList.tsx
│   │   │   ├── SubscriptionCard.tsx
│   │   │   ├── hooks.ts   # useSubscriptions, etc.
│   │   │   └── api.ts     # API calls for this feature
│   │   ├── transformations/
│   │   └── dashboard/
│   ├── stores/            # Zustand stores
│   │   └── ui.ts          # useUIStore
│   ├── lib/
│   │   ├── api.ts         # API client setup
│   │   └── utils.ts       # Shared utilities
│   ├── App.tsx
│   └── main.tsx
├── tests/
│   └── ...
├── index.html
├── vite.config.ts
├── tailwind.config.ts
└── package.json
```

**Import Aliases:**
```typescript
// vite.config.ts / tsconfig.json
"@/components/*" → "src/components/*"
"@/features/*"   → "src/features/*"
"@/stores/*"     → "src/stores/*"
"@/lib/*"        → "src/lib/*"
```

### Error Handling Patterns

**Backend Exception Hierarchy:**
```python
# core/exceptions.py
class AppException(Exception):
    """Base for all application exceptions"""
    code: str
    status_code: int = 400

class NotFoundError(AppException):
    status_code = 404

class ValidationError(AppException):
    status_code = 400

class ConflictError(AppException):
    status_code = 409

# subscriptions/exceptions.py
class SubscriptionNotFoundError(NotFoundError):
    code = "SUBSCRIPTION_NOT_FOUND"

class SubscriptionDuplicateError(ConflictError):
    code = "SUBSCRIPTION_CREATE_DUPLICATE"
```

**Frontend Error Handling:**
```typescript
// TanStack Query handles errors automatically
const { error } = useQuery({...})

// Display using error.code for i18n or error.detail for direct display
if (error) {
  toast.error(error.detail)
}
```

### Testing Patterns

**Backend Tests:**
- Location: `tests/` directory mirroring `src/`
- Framework: pytest + pytest-asyncio + httpx
- Fixtures: Shared in `conftest.py`

```python
# tests/subscriptions/test_router.py
async def test_create_subscription(client: AsyncClient, db: AsyncSession):
    response = await client.post("/api/subscriptions", json={...})
    assert response.status_code == 201
```

**Frontend Tests:**
- Location: `tests/` or co-located `*.test.tsx`
- Framework: Vitest + React Testing Library

### Enforcement Guidelines

**All AI Agents MUST:**
1. Follow naming conventions exactly as specified
2. Use the error response format with proper codes
3. Place files in the correct directory structure
4. Use snake_case for all API JSON fields
5. Return appropriate HTTP status codes
6. Include type hints (Python) and TypeScript types

**Pattern Verification:**
- Linting catches naming violations (ESLint, Ruff)
- Type checking catches schema mismatches
- Integration tests verify API contracts

## Project Structure & Boundaries

### Complete Project Directory Structure

```
rss-remastered/
├── README.md
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .gitignore
├── config.example.yaml
│
├── backend/
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py              # Pydantic Settings
│   │   │   ├── database.py            # SQLAlchemy async setup
│   │   │   ├── dependencies.py        # FastAPI dependencies
│   │   │   ├── exceptions.py          # Base exception classes
│   │   │   └── logging.py             # structlog configuration
│   │   │
│   │   ├── subscriptions/
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # /api/subscriptions endpoints
│   │   │   ├── schemas.py             # Pydantic models
│   │   │   ├── models.py              # SQLAlchemy models
│   │   │   ├── service.py             # Business logic
│   │   │   └── exceptions.py
│   │   │
│   │   ├── content/
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # /api/content endpoints
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   ├── service.py
│   │   │   ├── aggregator.py          # Feed fetching logic
│   │   │   └── exceptions.py
│   │   │
│   │   ├── transformations/
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # /api/transformations endpoints
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   ├── service.py
│   │   │   ├── pipeline.py            # Transformation orchestration
│   │   │   ├── extractors/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── youtube.py         # yt-dlp integration
│   │   │   │   └── subtitles.py       # Subtitle extraction
│   │   │   └── exceptions.py
│   │   │
│   │   ├── feeds/
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # /api/feeds, /feeds/podcast.xml
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   ├── rss_generator.py       # RSS 2.0 + iTunes generation
│   │   │   └── exceptions.py
│   │   │
│   │   ├── integrations/
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # /api/integrations endpoints
│   │   │   ├── schemas.py
│   │   │   ├── plex.py                # Plex integration
│   │   │   ├── jellyfin.py            # Jellyfin integration
│   │   │   ├── arr.py                 # Sonarr/Radarr integration
│   │   │   └── exceptions.py
│   │   │
│   │   ├── jobs/
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # /api/jobs endpoints (queue status)
│   │   │   ├── schemas.py
│   │   │   ├── models.py              # Job table
│   │   │   ├── service.py
│   │   │   ├── worker.py              # Background job worker
│   │   │   ├── tasks.py               # Task definitions
│   │   │   └── exceptions.py
│   │   │
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── provider.py            # AIProvider protocol
│   │   │   ├── openai.py              # OpenAI implementation
│   │   │   ├── ollama.py              # Ollama implementation
│   │   │   ├── noop.py                # No-op for graceful degradation
│   │   │   └── exceptions.py
│   │   │
│   │   └── health/
│   │       ├── __init__.py
│   │       ├── router.py              # /api/health, /api/health/ready
│   │       └── service.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py                # Shared fixtures
│       ├── subscriptions/
│       │   ├── test_router.py
│       │   └── test_service.py
│       ├── content/
│       ├── transformations/
│       ├── jobs/
│       └── ai/
│
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── components.json                # shadcn/ui config
│   ├── index.html
│   │
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── index.css                  # Tailwind imports
│   │   │
│   │   ├── components/
│   │   │   ├── ui/                    # shadcn/ui components
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   └── ...
│   │   │   └── app/                   # App-level composed components
│   │   │       ├── Sidebar.tsx
│   │   │       ├── Header.tsx
│   │   │       ├── ContextPanel.tsx
│   │   │       └── Layout.tsx
│   │   │
│   │   ├── features/
│   │   │   ├── dashboard/
│   │   │   │   ├── Dashboard.tsx
│   │   │   │   ├── StatsCard.tsx
│   │   │   │   └── hooks.ts
│   │   │   ├── subscriptions/
│   │   │   │   ├── SubscriptionList.tsx
│   │   │   │   ├── SubscriptionCard.tsx
│   │   │   │   ├── AddSubscriptionForm.tsx
│   │   │   │   ├── hooks.ts
│   │   │   │   └── api.ts
│   │   │   ├── content/
│   │   │   │   ├── ContentFeed.tsx
│   │   │   │   ├── ContentCard.tsx
│   │   │   │   ├── ArticleReader.tsx
│   │   │   │   ├── hooks.ts
│   │   │   │   └── api.ts
│   │   │   ├── transformations/
│   │   │   │   ├── TransformQueue.tsx
│   │   │   │   ├── TransformCard.tsx
│   │   │   │   ├── hooks.ts
│   │   │   │   └── api.ts
│   │   │   └── settings/
│   │   │       ├── Settings.tsx
│   │   │       ├── AISettings.tsx
│   │   │       ├── IntegrationSettings.tsx
│   │   │       └── api.ts
│   │   │
│   │   ├── stores/
│   │   │   └── ui.ts                  # useUIStore (Zustand)
│   │   │
│   │   └── lib/
│   │       ├── api.ts                 # API client (fetch wrapper)
│   │       ├── query.ts               # TanStack Query setup
│   │       └── utils.ts               # Shared utilities
│   │
│   ├── tests/
│   │   └── ...
│   │
│   └── public/
│       ├── manifest.json              # PWA manifest
│       └── icons/
│
└── data/                              # Bind-mounted volume
    ├── rss.db                         # SQLite database
    ├── media/                         # Transformed content
    └── config.yaml                    # User configuration
```

### Architectural Boundaries

**API Boundaries:**

| Boundary | Endpoint Pattern | Auth | Purpose |
|----------|------------------|------|---------|
| Public feeds | `/feeds/*` | None | RSS readers, podcatchers |
| Web UI API | `/api/*` | Session cookie | Frontend SPA |
| *arr integration | `/api/*` | API key header | Sonarr/Radarr |
| Health checks | `/api/health/*` | None | Container orchestration |
| Static assets | `/assets/*`, `/` | None | Frontend bundle |

**Data Boundaries:**

| Domain | Tables | Responsibility |
|--------|--------|----------------|
| Subscriptions | `subscriptions`, `tags`, `subscription_tags` | Feed source management |
| Content | `content_items` | Aggregated content storage |
| Transformations | `transformations` | Transform results and metadata |
| Jobs | `jobs` | Background task state |
| Settings | `user_preferences`, `integration_configs` | User and system configuration |

**Service Boundaries:**

| Module | External Dependencies | Owns |
|--------|----------------------|------|
| `subscriptions/` | None | Subscription CRUD |
| `content/` | External RSS/YouTube feeds | Content aggregation |
| `transformations/` | `ai/`, `jobs/` | Transform pipeline |
| `feeds/` | None | RSS generation |
| `integrations/` | Plex, Jellyfin, *arr APIs | External service sync |
| `jobs/` | None | Task queue management |
| `ai/` | OpenAI, Ollama | AI abstraction |

### Requirements to Structure Mapping

**PRD Category → Implementation Location:**

| PRD Category | Backend Module | Frontend Feature | Database Tables |
|--------------|----------------|------------------|-----------------|
| FR1-9: Subscription Management | `subscriptions/` | `features/subscriptions/` | `subscriptions`, `tags` |
| FR10-18: Content Aggregation | `content/` | `features/content/` | `content_items` |
| FR19-27: Content Transformation | `transformations/`, `ai/`, `jobs/` | `features/transformations/` | `transformations`, `jobs` |
| FR28-33: Web UI Serving | `main.py` | Entire frontend | - |
| FR34-37: Podcast Feed Generation | `feeds/` | - | - |
| FR38-40: Media Server Integration | `integrations/` | `features/settings/` | `integration_configs` |
| FR41-45: *arr Stack Integration | `integrations/` | `features/settings/` | `integration_configs` |
| FR46-51: System Health | `health/`, `jobs/` | `features/dashboard/` | `jobs` |
| FR52-58: Configuration | `core/config.py` | `features/settings/` | `user_preferences` |

### Integration Points

**Internal Communication:**

```
Frontend (React) ──HTTP/JSON──▶ FastAPI ──async──▶ SQLAlchemy ──▶ SQLite
                                   │
                                   ├──▶ Job Worker (asyncio)
                                   │
                                   └──▶ AI Provider (OpenAI/Ollama)
```

**External Integrations:**

| Integration | Protocol | Direction | Module |
|-------------|----------|-----------|--------|
| YouTube | HTTPS (yt-dlp) | Outbound | `transformations/extractors/youtube.py` |
| RSS Feeds | HTTPS | Outbound | `content/aggregator.py` |
| OpenAI | HTTPS | Outbound | `ai/openai.py` |
| Ollama | HTTP | Outbound | `ai/ollama.py` |
| Plex | HTTPS | Outbound | `integrations/plex.py` |
| Jellyfin | HTTPS | Outbound | `integrations/jellyfin.py` |
| Sonarr/Radarr | HTTP | Inbound | `integrations/arr.py` |

### Data Flow

**Content Transformation Flow:**

```
1. User clicks "Transform" on content item
2. Frontend POST /api/transformations
3. Backend creates Job record (status: pending)
4. Returns job_id immediately (202 Accepted)
5. Job Worker picks up job
6. Worker calls AI provider
7. Worker updates Job (status: completed)
8. Frontend polls /api/jobs/{id} for status
9. Frontend fetches transformed content
```

**Feed Aggregation Flow:**

```
1. Scheduler triggers aggregation (or manual refresh)
2. For each subscription:
   a. Fetch feed URL
   b. Parse RSS/YouTube content
   c. Deduplicate against existing content
   d. Insert new content_items
3. Log results, update subscription.last_fetched
```

### Development Workflow Integration

**Development Server:**

```bash
# Terminal 1: Backend
cd backend && uv run uvicorn src.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev  # Vite dev server on :5173

# Frontend proxies /api/* to backend
```

**Production Build:**

```bash
# Frontend builds to static files
cd frontend && npm run build  # Output: frontend/dist/

# Backend serves static files from frontend/dist/
# Single container runs FastAPI serving both API and static
```

**Docker Deployment:**

```yaml
# docker-compose.yml
services:
  rss-remastered:
    build: .
    ports:
      - "8080:8000"
    volumes:
      - ./data:/app/data          # Persistent storage
      - ./config.yaml:/app/config.yaml:ro
    environment:
      - RSS_LOG_LEVEL=info
```

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**
All technology decisions work together without conflicts:
- FastAPI + SQLAlchemy 2.0 (async) + Pydantic: Native integration via Pydantic v2
- Vite + React + TanStack Query + Zustand: Standard modern React stack
- structlog + Docker stdout: Native logging without additional infrastructure
- In-process asyncio + SQLite job table: No external dependencies, single container preserved

**Pattern Consistency:**
- Naming conventions (snake_case API, PascalCase components) align across stack
- Domain-based backend structure matches feature-based frontend organization
- Error handling patterns consistent: domain exceptions → HTTP errors → frontend toasts
- All imports use established alias patterns (`@/` prefix)

**Structure Alignment:**
- Project structure directly supports all architectural decisions
- Module boundaries match data ownership boundaries
- Integration points clearly defined between modules
- Test structure mirrors source structure in both backend and frontend

### Requirements Coverage Validation ✅

**Functional Requirements Coverage:**

| FR Category | Architectural Support | Implementation Location |
|-------------|----------------------|------------------------|
| FR1-9: Subscriptions | ✅ Full | `subscriptions/` module |
| FR10-18: Aggregation | ✅ Full | `content/` module + job worker |
| FR19-27: Transformation | ✅ Full | `transformations/` + `ai/` + `jobs/` |
| FR28-33: Web UI | ✅ Full | Frontend SPA + FastAPI static serving |
| FR34-37: Podcast Feeds | ✅ Full | `feeds/` module |
| FR38-40: Media Server | ✅ Full | `integrations/` module |
| FR41-45: *arr Stack | ✅ Full | `integrations/arr.py` |
| FR46-51: System Health | ✅ Full | `health/` + `jobs/` modules |
| FR52-58: Configuration | ✅ Full | `core/config.py` + layered config |

**Non-Functional Requirements Coverage:**

| NFR Category | Architectural Support |
|--------------|----------------------|
| Performance (30s startup, 2GB RAM) | ✅ SQLite + in-process async supports constraints |
| Reliability (retry, backoff) | ✅ Job table with retry count and error tracking |
| Integration compliance | ✅ RSS 2.0 generator, *arr API patterns documented |
| Security (API keys, hashed) | ✅ Pydantic Settings + secure storage patterns |
| Usability (WCAG AA) | ✅ shadcn/ui provides accessible defaults |
| Deployment (single compose) | ✅ Single container architecture preserved |

### Implementation Readiness Validation ✅

**Decision Completeness:**
- All critical technology choices documented with specific versions
- Implementation patterns comprehensive with concrete examples
- Consistency rules clearly stated for AI agent enforcement
- Error code patterns provide template for all new error types

**Structure Completeness:**
- Complete directory tree with all files specified
- Module boundaries clearly defined
- Integration points mapped with protocols and directions
- Configuration file locations and formats documented

**Pattern Completeness:**
- Naming conventions cover database, API, and code
- API response/error formats fully specified
- Testing patterns established for both stacks
- Data flow diagrams document transformation and aggregation pipelines

### Gap Analysis Results

**Critical Gaps:** None identified

**Important Gaps (address in implementation):**
- PWA service worker implementation details (defer to story-level)
- Rate limiting configuration for external APIs (can use library defaults)
- Metrics/observability beyond logging (defer post-MVP)

**Nice-to-Have Gaps (future enhancement):**
- OpenAPI schema customization documentation
- Performance benchmarking targets
- Disaster recovery procedures

### Architecture Completeness Checklist

**✅ Requirements Analysis**
- [x] Project context thoroughly analyzed (58 FRs, 36 NFRs)
- [x] Scale and complexity assessed (medium complexity, household scale)
- [x] Technical constraints identified (Python 3.11+, SQLite MVP, Docker single container)
- [x] Cross-cutting concerns mapped (queue, auth, error handling, logging)

**✅ Architectural Decisions**
- [x] Critical decisions documented with versions (SQLAlchemy 2.0, Vite 6.x, etc.)
- [x] Technology stack fully specified (FastAPI + React + shadcn/ui)
- [x] Integration patterns defined (OpenAI/Ollama, Plex/Jellyfin, *arr)
- [x] Performance considerations addressed (in-process async, SQLite)

**✅ Implementation Patterns**
- [x] Naming conventions established (snake_case API, PascalCase components)
- [x] Structure patterns defined (domain-based backend, feature-based frontend)
- [x] Communication patterns specified (HTTP/JSON, error codes)
- [x] Process patterns documented (job queue, transformation pipeline)

**✅ Project Structure**
- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** High

The architecture provides clear, unambiguous guidance for AI agents to implement features consistently. Technology choices are compatible, patterns are comprehensive, and all requirements have architectural support.

**Key Strengths:**
- Single container deployment simplifies operations
- In-process job queue eliminates Redis dependency
- Layered configuration provides flexibility without complexity
- Domain-based structure enables parallel development
- Clear separation between API, UI, and background processing

**Areas for Future Enhancement:**
- SSE for real-time updates (polling sufficient for MVP)
- PostgreSQL migration path (documented but not implemented)
- Additional AI providers beyond OpenAI/Ollama
- Horizontal scaling patterns (not needed at target scale)

### Implementation Handoff

**AI Agent Guidelines:**
- Follow all architectural decisions exactly as documented
- Use implementation patterns consistently across all components
- Respect project structure and module boundaries
- Use error codes from the established pattern (`DOMAIN_ACTION_REASON`)
- Refer to this document for all architectural questions

**First Implementation Priority:**
Initialize project structure using documented commands:
1. Create backend with `uv init` and domain module skeleton
2. Create frontend with `npm create vite@latest` + shadcn/ui
3. Configure Dockerfile and docker-compose.yml
4. Establish database with Alembic initial migration

## Architecture Completion Summary

### Workflow Completion

**Architecture Decision Workflow:** COMPLETED
**Total Steps Completed:** 8
**Date Completed:** 2025-12-13
**Document Location:** docs/architecture.md

### Final Architecture Deliverables

**Complete Architecture Document**
- All architectural decisions documented with specific versions
- Implementation patterns ensuring AI agent consistency
- Complete project structure with all files and directories
- Requirements to architecture mapping
- Validation confirming coherence and completeness

**Implementation Ready Foundation**
- 15+ architectural decisions made (database, auth, API, frontend, infrastructure)
- 25+ implementation patterns defined (naming, structure, API, error handling)
- 8 architectural domains specified (subscriptions, content, transformations, feeds, integrations, jobs, ai, health)
- 58 functional requirements + 36 non-functional requirements fully supported

**AI Agent Implementation Guide**
- Technology stack with verified versions
- Consistency rules that prevent implementation conflicts
- Project structure with clear boundaries
- Integration patterns and communication standards

### Implementation Handoff

**For AI Agents:**
This architecture document is your complete guide for implementing rss-remastered. Follow all decisions, patterns, and structures exactly as documented.

**First Implementation Priority:**
```bash
# Backend initialization
cd backend && uv init
# Frontend initialization
npm create vite@latest frontend -- --template react-ts
npx shadcn@latest init
```

**Development Sequence:**
1. Initialize project using documented starter template
2. Set up development environment per architecture
3. Implement core architectural foundations (database, config, logging)
4. Build features following established patterns
5. Maintain consistency with documented rules

### Quality Assurance Checklist

**Architecture Coherence**
- [x] All decisions work together without conflicts
- [x] Technology choices are compatible
- [x] Patterns support the architectural decisions
- [x] Structure aligns with all choices

**Requirements Coverage**
- [x] All functional requirements are supported
- [x] All non-functional requirements are addressed
- [x] Cross-cutting concerns are handled
- [x] Integration points are defined

**Implementation Readiness**
- [x] Decisions are specific and actionable
- [x] Patterns prevent agent conflicts
- [x] Structure is complete and unambiguous
- [x] Examples are provided for clarity

### Project Success Factors

**Clear Decision Framework**
Every technology choice was made collaboratively with clear rationale, ensuring all stakeholders understand the architectural direction.

**Consistency Guarantee**
Implementation patterns and rules ensure that multiple AI agents will produce compatible, consistent code that works together seamlessly.

**Complete Coverage**
All project requirements are architecturally supported, with clear mapping from business needs to technical implementation.

**Solid Foundation**
The chosen stack (FastAPI + Vite + React + shadcn/ui) provides a production-ready foundation following current best practices.

---

**Architecture Status:** READY FOR IMPLEMENTATION

**Next Phase:** Begin implementation using the architectural decisions and patterns documented herein.

**Document Maintenance:** Update this architecture when major technical decisions are made during implementation.

---
project_name: 'rss-remastered'
user_name: 'Mo'
date: '2025-12-13'
sections_completed: ['technology_stack', 'language_rules', 'framework_rules', 'testing_rules', 'code_quality', 'workflow_rules', 'critical_rules']
status: 'complete'
rule_count: 45
optimized_for_llm: true
source: 'architecture.md'
---

# Project Context for AI Agents

_Critical rules and patterns for implementing rss-remastered. Focus on unobvious details that prevent implementation mistakes._

---

## Technology Stack & Versions

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Runtime |
| FastAPI | latest | Web framework |
| SQLAlchemy | 2.0 (async) | ORM |
| Alembic | latest | Migrations |
| SQLite | - | Database (MVP) |
| Pydantic | v2 | Validation + Settings |
| structlog | latest | Logging |
| uv | latest | Package management |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.x | UI framework |
| TypeScript | strict mode | Type safety |
| Vite | 6.x | Build tool |
| Tailwind CSS | 4.x | Styling |
| shadcn/ui | latest | Component library |
| TanStack Query | latest | Server state |
| Zustand | latest | Client state |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| Docker | Single container deployment |
| yt-dlp | YouTube extraction |
| FFmpeg | Media processing |

---

## Critical Implementation Rules

### Python/FastAPI Rules

**SQLAlchemy 2.0 Async Patterns:**
- ALWAYS use `async def` for database operations
- Use `AsyncSession` from `sqlalchemy.ext.asyncio`
- Use `Mapped[Type]` for column annotations, NOT `Column(Type)`
- Use `select()` syntax, NOT legacy `query()` syntax

```python
# CORRECT - SQLAlchemy 2.0 async
async def get_subscription(db: AsyncSession, id: int) -> Subscription | None:
    result = await db.execute(select(Subscription).where(Subscription.id == id))
    return result.scalar_one_or_none()

# WRONG - Legacy pattern
def get_subscription(db: Session, id: int):
    return db.query(Subscription).filter(Subscription.id == id).first()
```

**Pydantic v2 Patterns:**
- Use `model_validator` NOT `root_validator`
- Use `field_validator` NOT `validator`
- Use `ConfigDict` NOT inner `class Config`
- Use `model_dump()` NOT `dict()`

**FastAPI Router Patterns:**
- One router per domain module in `router.py`
- Inject dependencies via `Depends()`
- Return Pydantic schemas, not SQLAlchemy models
- Use `status_code=` parameter for non-200 responses

### TypeScript/React Rules

**Strict Mode Requirements:**
- NO `any` types - use `unknown` and narrow
- NO implicit returns in functions
- ALL function parameters must be typed
- Use discriminated unions for state

**TanStack Query Patterns:**
- ALL server data via `useQuery` / `useMutation`
- Query keys follow pattern: `['domain', 'action', params]`
- Mutations invalidate related queries on success
- Handle loading/error states explicitly

```typescript
// CORRECT - TanStack Query pattern
const { data, isLoading, error } = useQuery({
  queryKey: ['subscriptions', 'list'],
  queryFn: () => api.getSubscriptions()
})

// WRONG - Direct fetch in component
const [data, setData] = useState()
useEffect(() => { fetch(...).then(setData) }, [])
```

**Zustand Patterns:**
- UI-only state (sidebar, theme, panels)
- Persist to localStorage via middleware
- Keep stores minimal - server state in TanStack Query

**Import Aliases:**
```typescript
// Use path aliases
import { Button } from '@/components/ui/button'
import { useSubscriptions } from '@/features/subscriptions/hooks'

// NOT relative imports across features
import { Button } from '../../../components/ui/button'
```

---

## API Contract Rules

### JSON Field Naming
- **ALL JSON fields use `snake_case`** - backend AND frontend
- Frontend converts at API boundary if needed
- Database columns match JSON field names

```json
// CORRECT
{ "subscription_id": 1, "feed_url": "...", "created_at": "..." }

// WRONG
{ "subscriptionId": 1, "feedUrl": "...", "createdAt": "..." }
```

### Response Patterns

**Success - Return data directly:**
```python
# GET /api/subscriptions
[{"id": 1, "name": "..."}]  # List directly

# GET /api/subscriptions/1
{"id": 1, "name": "..."}    # Object directly

# POST /api/subscriptions (201 Created)
{"id": 2, "name": "..."}    # Created object

# DELETE /api/subscriptions/1 (204 No Content)
# Empty response
```

**Errors - Structured format:**
```python
{
  "detail": "Human-readable message",
  "code": "DOMAIN_ACTION_REASON",
  "context": {"field": "url"}  # optional
}
```

**Error Code Pattern:** `DOMAIN_ACTION_REASON`
- `SUBSCRIPTION_CREATE_INVALID_URL`
- `SUBSCRIPTION_CREATE_DUPLICATE`
- `TRANSFORM_QUEUE_AI_UNAVAILABLE`
- `AUTH_API_KEY_INVALID`

### HTTP Status Codes
| Code | Usage |
|------|-------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Validation error |
| 401 | Unauthorized |
| 404 | Not found |
| 409 | Conflict (duplicate) |
| 500 | Server error |

---

## Testing Rules

### Backend (pytest)
- Tests in `backend/tests/` mirroring `src/` structure
- Use `pytest-asyncio` for async tests
- Use `httpx.AsyncClient` for API tests
- Fixtures in `conftest.py`

```python
# CORRECT - Async test pattern
@pytest.mark.asyncio
async def test_create_subscription(client: AsyncClient, db: AsyncSession):
    response = await client.post("/api/subscriptions", json={...})
    assert response.status_code == 201
```

### Frontend (Vitest)
- Tests in `frontend/tests/` or co-located `*.test.tsx`
- Use React Testing Library
- Mock API calls with MSW or vi.mock

### Test Naming
- `test_<action>_<condition>_<expected_result>`
- Example: `test_create_subscription_duplicate_url_returns_409`

---

## Project Structure Rules

### Backend Domain Modules
Each domain (`subscriptions/`, `content/`, etc.) contains:
```
domain/
├── __init__.py
├── router.py      # FastAPI routes
├── schemas.py     # Pydantic models (API)
├── models.py      # SQLAlchemy models (DB)
├── service.py     # Business logic
└── exceptions.py  # Domain exceptions
```

**Service Layer Pattern:**
- Routers call services, NOT direct DB access
- Services contain business logic
- Services raise domain exceptions
- Exception handler converts to HTTP responses

### Frontend Feature Modules
Each feature (`features/subscriptions/`, etc.) contains:
```
feature/
├── FeatureComponent.tsx
├── hooks.ts       # useQuery/useMutation hooks
└── api.ts         # API client functions
```

### File Naming
| Type | Convention | Example |
|------|------------|---------|
| Python modules | snake_case | `subscription_service.py` |
| React components | PascalCase | `SubscriptionCard.tsx` |
| Hooks | camelCase | `useSubscriptions.ts` |
| Tests | snake_case | `test_router.py` |

---

## Database Rules

### Naming Conventions
| Element | Convention | Example |
|---------|------------|---------|
| Tables | snake_case, plural | `subscriptions`, `content_items` |
| Columns | snake_case | `created_at`, `feed_url` |
| Foreign keys | `{table_singular}_id` | `subscription_id` |
| Indexes | `ix_{table}_{column}` | `ix_subscriptions_url` |

### Migration Rules
- ALWAYS create migration for schema changes
- NEVER modify existing migrations
- Test migrations forward AND backward
- Command: `alembic revision --autogenerate -m "description"`

---

## Background Jobs Rules

**Job Queue Pattern:**
- Jobs stored in `jobs` table (SQLite)
- Worker runs in-process via asyncio
- NO Redis/Celery - single container constraint

**Job Status Flow:**
`pending` → `running` → `completed` | `failed`

**Creating Jobs:**
```python
job = Job(
    task_name="transform_content",
    payload=json.dumps({"content_id": 123}),
    status="pending",
    priority=1
)
await db.add(job)
await db.commit()
```

---

## Configuration Rules

**Priority Order (highest wins):**
1. Environment variables (`RSS_` prefix)
2. YAML config file
3. Database (user preferences)
4. Defaults

**Environment Variable Pattern:**
```bash
RSS_AI__PROVIDER=openai     # Nested: ai.provider
RSS_AI__API_KEY=sk-...      # Nested: ai.api_key
RSS_LOG_LEVEL=debug         # Top-level: log_level
```

---

## Critical Don't-Miss Rules

### NEVER Do This
- `any` types in TypeScript
- Synchronous database calls in FastAPI
- Direct state mutation (use immutable patterns)
- API responses with camelCase JSON
- Wrapper objects around API responses
- `query()` syntax with SQLAlchemy 2.0
- External dependencies like Redis/Celery

### ALWAYS Do This
- Type hints on ALL Python functions
- Explicit error handling with domain exceptions
- snake_case for ALL JSON fields
- Async patterns for database operations
- Domain-based module organization
- Service layer between router and database

### Security Rules
- API keys stored hashed in database
- Secrets via environment variables only
- No credentials in YAML config
- Validate all external input via Pydantic

---

## AI Provider Rules

**Supported Providers:**
- `openai` - OpenAI API (also Azure, compatible endpoints)
- `ollama` - Local models
- `none` - Graceful degradation

**OpenAI-Compatible Pattern:**
```python
# Point base_url at any OpenAI-compatible endpoint
AIConfig(
    provider="openai",
    base_url="http://localhost:8080/v1",  # LocalAI, LiteLLM, etc.
    model="gpt-4"
)
```

**Graceful Degradation:**
- If AI unconfigured, `NoOpProvider` returns clear error
- Transformation features disabled, not broken
- User sees "AI not configured" message

---

## Logging Rules

**Use structlog with JSON output:**
```python
import structlog
log = structlog.get_logger()

log.info("transformation_started", job_id=42, content_id=123)
```

**Output to stdout/stderr only:**
- Docker captures logs natively
- Works with `docker compose logs`
- No file-based logging

**Log Levels:**
- `DEBUG`: Development details
- `INFO`: Normal operations
- `WARNING`: Recoverable issues
- `ERROR`: Failures requiring attention

---

_Last updated: 2025-12-13_
_Source: docs/architecture.md_

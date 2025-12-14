# Story 1.5: Configure Pydantic Settings

Status: Ready for Review

## Story

As a **developer**,
I want **a layered configuration system using Pydantic Settings**,
So that **all app configuration follows a consistent pattern with environment variable overrides**.

## Acceptance Criteria

1. **Given** `core/config.py` exists
   **Then** it exports a `Settings` class with typed configuration fields:
   - `database_url: str` (default: `sqlite+aiosqlite:///data/rss.db`)
   - `log_level: str` (default: `info`)
   - `log_format: str` (default: `json`)
   - `base_url: str` (default: empty string for reverse proxy support)
   - `data_dir: Path` (default: `data/`)

2. **Given** environment variables with `RSS_` prefix exist
   **When** the application loads configuration
   **Then** environment variables override YAML file values
   **And** YAML file values override defaults
   **And** nested settings use double underscore (e.g., `RSS_AI__PROVIDER`)

3. **Given** an invalid configuration value is provided
   **When** the application starts
   **Then** a clear validation error message is displayed
   **And** the application fails to start

## Tasks / Subtasks

- [x] Task 1: Implement Settings class with Pydantic Settings (AC: #1, #2, #3)
  - [x] Create Settings class extending BaseSettings
  - [x] Configure `RSS_` prefix for environment variables
  - [x] Add all required typed fields with defaults
  - [x] Enable nested model support with `__` separator
  - [x] Configure YAML file loading from `config.yaml` or `data/config.yaml`

- [x] Task 2: Implement configuration priority/layering (AC: #2)
  - [x] Implement settings_customise_sources for priority ordering
  - [x] Priority: env vars (highest) → YAML → defaults (lowest)
  - [x] Add YAML file settings source using pydantic-settings-yaml or custom loader

- [x] Task 3: Implement nested settings for future AI configuration (AC: #2)
  - [x] Create AISettings nested model (provider, base_url, model, api_key placeholders)
  - [x] Create LoggingSettings nested model (level, format)
  - [x] Ensure double-underscore env var parsing works correctly

- [x] Task 4: Add configuration validation with clear error messages (AC: #3)
  - [x] Add validators for log_level (must be debug/info/warning/error)
  - [x] Add validators for log_format (must be json/console)
  - [x] Add validators for database_url (must be valid SQLAlchemy URL)
  - [x] Implement startup validation that fails fast with clear errors

- [x] Task 5: Integrate settings into existing modules (AC: #1)
  - [x] Update `core/database.py` to use Settings.database_url
  - [x] Update `core/logging.py` to use Settings.log_level and Settings.log_format
  - [x] Create singleton settings instance with `@lru_cache` or module-level
  - [x] Update `main.py` to initialize settings at startup

- [x] Task 6: Add unit tests for configuration system
  - [x] Test default values
  - [x] Test environment variable overrides
  - [x] Test YAML file loading
  - [x] Test validation error messages
  - [x] Test nested settings parsing

## Dev Notes

### Architecture Requirements

From `docs/architecture.md`:

**Configuration Management Pattern:**
```python
# Priority Order (highest wins):
# 1. Environment variables (RSS_ prefix)
# 2. YAML config file (bind-mounted)
# 3. Database (user preferences - future)
# 4. Defaults
```

**Required Config Categories:**
| Category | Source | Examples |
|----------|--------|----------|
| System config | Env vars, YAML | AI provider, database path, log level |
| User preferences | Web UI → DB | Theme, sidebar state, notifications (future) |
| Application data | Web UI → DB | Subscriptions, transform rules (future) |

**Example YAML Configuration:**
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

**Example Environment Override:**
```bash
# docker-compose.yml - env vars override YAML
environment:
  - RSS_AI__PROVIDER=openai
  - RSS_AI__API_KEY=sk-...
  - RSS_LOG_LEVEL=debug
```

### Technical Implementation Details

**Pydantic Settings v2 Pattern:**
```python
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RSS_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    database_url: str = "sqlite+aiosqlite:///data/rss.db"
    log_level: str = "info"
    log_format: str = "json"
    base_url: str = ""
    data_dir: Path = Path("data")
```

**YAML Loading Options:**
1. **Option A - pydantic-settings-yaml**: `pip install pydantic-settings-yaml`
2. **Option B - Custom source**: Use `settings_customise_sources` with PyYAML

**Singleton Pattern:**
```python
from functools import lru_cache

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### Existing Code Integration Points

**`core/database.py` (line 25-35):**
Currently uses `os.environ.get("RSS_DATABASE_URL", default_url)`.
Update to: `get_settings().database_url`

**`core/logging.py` (line 22-38):**
Currently uses `os.getenv("RSS_LOG_LEVEL", "info")` and `os.getenv("RSS_LOG_FORMAT", "json")`.
Update to: `get_settings().log_level` and `get_settings().log_format`

### Project Structure Notes

**File locations per architecture:**
- `backend/src/core/config.py` - Main Settings class (currently placeholder)
- `config.yaml` or `data/config.yaml` - YAML configuration file location
- `.env.example` - Document all `RSS_*` environment variables

**Dependencies to add to `pyproject.toml`:**
```toml
dependencies = [
    "pydantic-settings>=2.0.0",
    "pyyaml>=6.0",
]
```

### Validation Rules

| Field | Valid Values | Error Code Pattern |
|-------|--------------|-------------------|
| log_level | debug, info, warning, error | CONFIG_INVALID_LOG_LEVEL |
| log_format | json, console | CONFIG_INVALID_LOG_FORMAT |
| database_url | Valid SQLAlchemy async URL | CONFIG_INVALID_DATABASE_URL |
| data_dir | Valid directory path | CONFIG_INVALID_DATA_DIR |

### Testing Strategy

**Test files:**
- `backend/tests/core/test_config.py`

**Test scenarios:**
1. Default values when no env/yaml present
2. Environment variable override precedence
3. YAML file loading when present
4. Nested settings with `__` separator
5. Validation errors for invalid values
6. Missing optional fields don't error
7. Integration with database.py and logging.py

### References

- [Source: docs/architecture.md#Configuration-Management] - Configuration priority order
- [Source: docs/architecture.md#Core-Architectural-Decisions] - Pydantic Settings decision
- [Source: docs/epics.md#Story-1.5] - Original story requirements
- [Source: backend/src/core/database.py] - Current env var usage to replace
- [Source: backend/src/core/logging.py] - Current env var usage to replace

## Dev Agent Record

### Context Reference

<!-- Story 1-5: Pydantic Settings Configuration -->

### Agent Model Used

Claude Opus 4.5 (claude-opus-4-5-20251101)

### Debug Log References

No debug issues encountered during implementation.

### Completion Notes List

**Implementation Summary:**
- Created comprehensive `Settings` class in `backend/src/core/config.py` with:
  - All required typed fields with defaults matching AC #1
  - RSS_ prefix for environment variables
  - `__` delimiter for nested settings (RSS_AI__PROVIDER, etc.)
  - Custom `YamlConfigSettingsSource` for YAML config file loading
  - `settings_customise_sources` method implementing priority: env vars → YAML → defaults

- Created nested settings models:
  - `AISettings`: provider (openai/ollama/none), base_url, model, api_key
  - `LoggingSettings`: level, format

- Added validators with clear error codes:
  - `CONFIG_INVALID_LOG_LEVEL` for invalid log levels
  - `CONFIG_INVALID_LOG_FORMAT` for invalid log formats
  - `CONFIG_INVALID_DATABASE_URL` for invalid database URLs
  - `CONFIG_INVALID_DATA_DIR` for invalid data directory paths

- Implemented `validate_settings_on_startup()` for fail-fast startup validation

- Updated existing modules:
  - `database.py`: Uses `get_settings().database_url`
  - `logging.py`: Uses `get_settings().log_level` and `get_settings().log_format`
  - `main.py`: Calls `validate_settings_on_startup()` at startup, logs config details

- Created 40 comprehensive tests covering:
  - Default values (7 tests)
  - Environment variable overrides (5 tests)
  - Nested settings env vars (5 tests)
  - YAML config loading (3 tests)
  - Validation errors (6 tests)
  - Nested settings models (5 tests)
  - Settings caching and startup validation (4 tests)
  - Integration tests (3 tests)

- Updated existing tests to work with new Settings-based configuration
- All 75 tests pass with no regressions

### Change Log

- 2025-12-14: Initial implementation of Pydantic Settings configuration system
  - Added pyyaml dependency to pyproject.toml
  - Implemented Settings class with layered configuration
  - Created AISettings and LoggingSettings nested models
  - Added validators with clear error codes
  - Integrated settings into database.py, logging.py, and main.py
  - Created comprehensive test suite (40 new tests)
  - Updated existing tests for compatibility
  - Created config.example.yaml and updated .env.example

### File List

- backend/src/core/config.py (modified - full Settings implementation)
- backend/src/core/database.py (modified - uses get_settings().database_url)
- backend/src/core/logging.py (modified - uses get_settings() for log config)
- backend/src/main.py (modified - validates settings at startup)
- backend/pyproject.toml (modified - added pyyaml>=6.0)
- backend/tests/core/__init__.py (created)
- backend/tests/core/test_config.py (created - 40 unit tests)
- backend/tests/test_database.py (modified - updated for new Settings API)
- backend/tests/test_logging.py (modified - added settings cache clearing)
- config.example.yaml (created - example YAML configuration)
- .env.example (modified - documented all RSS_* environment variables)

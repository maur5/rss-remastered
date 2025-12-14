# Test Design Report - rss-remastered
## System-Level Testability Review (Phase 2 - Solutioning)

**Date:** 2025-12-13
**Architect:** Murat (Master Test Architect)
**Project Phase:** Solutioning (Pre-Implementation Readiness Gate)
**Mode:** System-Level Mode

---

## Executive Summary

**Overall Testability Score:** 8.5/10 ✅
**Implementation Readiness:** CONDITIONAL PASS ⚠️
**Recommendation:** Proceed to Phase 3 (Implementation) with **mandatory** mitigation of 4 high-priority test risks during Epic 3 and Epic 4.

### Key Findings

✅ **Strengths:**
- Domain-based architecture enables isolated unit testing
- Async-first patterns are highly testable with modern Python tools
- Existing Playwright E2E framework with custom fixtures demonstrates test-first culture
- AI provider abstraction perfectly designed for test isolation

⚠️ **Moderate Risks** (4 identified):
- NFR performance testing strategy undefined (TR-001)
- External integration testing lacks mocking strategy (TR-002, TR-003)
- AI transformation quality validation missing (TR-004)
- Retry/backoff logic testing patterns undefined (TR-005)

🔴 **High Risks** (2 identified):
- Media pipeline testability challenges (TR-008)
- PWA offline behavior testing complexity (TR-006)

---

## 1. Architecture Testability Analysis

### 1.1 Testability Characteristics

#### ✅ Domain Modularity
**Score: 10/10**

Your domain-based backend structure provides excellent test isolation:

```
backend/src/
├── subscriptions/     # Isolated domain
├── transformations/   # Isolated domain
├── content/           # Isolated domain
├── feeds/             # Isolated domain
└── integrations/      # Isolated domain
```

**Impact on Testing:**
- Each domain can be tested in complete isolation
- Clear boundaries enable parallel test development
- Mocking dependencies between domains is straightforward
- Unit test coverage can reach 90%+ per domain

**Test Pattern:**
```python
# tests/subscriptions/test_service.py
async def test_create_subscription_isolated(db_session):
    """Test subscription creation without touching other domains"""
    service = SubscriptionService(db_session)
    subscription = await service.create_subscription({
        "name": "Test Feed",
        "url": "https://example.com/feed.xml",
        "source_type": "rss_feed"
    })
    assert subscription.id is not None
```

---

#### ✅ Async-First Architecture
**Score: 9/10**

SQLAlchemy 2.0 async + FastAPI async patterns are battle-tested and highly testable:

**Test Tools:**
- `pytest-asyncio` for async test execution
- `httpx.AsyncClient` for FastAPI testing
- `asyncio` primitives for concurrency testing

**Example:**
```python
@pytest.mark.asyncio
async def test_concurrent_subscription_fetch(client: AsyncClient):
    """Test parallel feed fetching doesn't cause race conditions"""
    urls = [f"https://feed{i}.example.com" for i in range(10)]

    tasks = [
        client.post("/api/subscriptions", json={"url": url})
        for url in urls
    ]

    responses = await asyncio.gather(*tasks)
    assert all(r.status_code == 201 for r in responses)
```

---

#### ✅ AI Provider Abstraction
**Score: 10/10**

The `AIProvider` protocol with `NoOpProvider` fallback is **exemplary testability design**:

```python
# ai/provider.py
class AIProvider(Protocol):
    async def complete(self, prompt: str, max_tokens: int) -> str: ...
    async def is_available(self) -> bool: ...

# ai/noop.py
class NoOpProvider(AIProvider):
    async def complete(self, prompt: str, max_tokens: int) -> str:
        raise AIUnavailableError("No AI provider configured")
```

**Test Pattern:**
```python
class MockAIProvider(AIProvider):
    async def complete(self, prompt: str, max_tokens: int) -> str:
        return "Mocked AI response for testing"

    async def is_available(self) -> bool:
        return True

@pytest.fixture
def ai_provider():
    return MockAIProvider()

async def test_transformation_with_mock_ai(ai_provider):
    """Test transformation logic without calling real AI API"""
    result = await transform_service.subtitle_to_article(
        subtitles="Test subtitle text",
        ai_provider=ai_provider
    )
    assert result.status == "completed"
```

---

#### ✅ In-Process Job Queue
**Score: 9/10**

SQLite-backed job queue is **deterministic and testable**:

**Advantages:**
- No external Redis dependency = faster, simpler tests
- Job state persisted in database = easy to inspect and assert
- Synchronous job execution available for tests

**Test Pattern:**
```python
async def test_job_execution_synchronously(db_session):
    """Test job processing without background worker"""
    job = await jobs_service.enqueue_job(
        "transform_content",
        {"content_id": 123}
    )

    # Execute synchronously in test
    await jobs_service.execute_job(job.id)

    # Assert state changes
    job = await jobs_service.get_job(job.id)
    assert job.status == "completed"
```

---

### 1.2 Testability Weaknesses

#### ⚠️ External Integration Coupling
**Score: 6/10**

Your architecture depends on **8 external integrations** without a clear mocking strategy:

| Integration | Protocol | Test Challenge |
|-------------|----------|----------------|
| YouTube (yt-dlp) | HTTPS | Rate limiting, video availability |
| RSS feeds | HTTPS | Network flakiness, malformed feeds |
| OpenAI API | HTTPS | API costs, quota limits |
| Ollama | HTTP | Local service dependency |
| Plex API | HTTPS | Test instance required |
| Jellyfin API | HTTPS | Test instance required |
| Sonarr API | HTTP | Mock *arr instance needed |
| Radarr API | HTTP | Mock *arr instance needed |

**Current PRD Statement:**
> "Real yt-dlp + FFmpeg - No mocking media, that's where bugs hide"

**Risk:**
- ✅ Philosophy is correct (integration bugs are real)
- ❌ Implementation is impractical (slow, flaky, expensive tests)

**Mitigation Required:** Implement **layered testing strategy** (see Risk TR-002).

---

## 2. NFR Testability Assessment

### 2.1 Performance NFRs (NFR1-NFR7)

| NFR | Target | Testability | Mitigation Required |
|-----|--------|-------------|---------------------|
| NFR1: Startup time | <30s | ⚠️ No automation | Add Docker startup benchmark |
| NFR2: Memory usage | <2GB | ⚠️ No automation | Add `docker stats` validation |
| NFR3: UI load time | <3s | ⚠️ No automation | Add Lighthouse CI |
| NFR4: Feed rendering | <1s | ⚠️ No automation | Add Playwright timing assertions |
| NFR5: Queue response | <500ms | ⚠️ No automation | Add pytest-benchmark |
| NFR6: API latency | <200ms | ⚠️ No automation | Add pytest-benchmark |
| NFR7: Podcast generation | <2s for 100 items | ⚠️ No automation | Add pytest-benchmark |

**Risk TR-001: NFR Performance Targets Not Validated**

**Impact:** High
**Likelihood:** High

**Problem:** Without automated performance validation, you risk:
- Shipping code that violates NFRs
- Discovering performance issues only in production
- Regression when dependencies update

**Mitigation Strategy:**

```yaml
Performance Test Framework:

Backend (pytest-benchmark):
  Setup:
    pip install pytest-benchmark

  Tests:
    # tests/performance/test_api_latency.py
    def test_subscription_list_latency(benchmark, client):
        """NFR6: API responds within 200ms"""
        response = benchmark(lambda: client.get("/api/subscriptions"))
        assert benchmark.stats.mean < 0.2  # 200ms

    def test_podcast_feed_generation(benchmark, db_session):
        """NFR7: Podcast feed <2s for 100 items"""
        setup_test_items(db_session, count=100)
        response = benchmark(lambda: generate_podcast_feed())
        assert benchmark.stats.mean < 2.0

Frontend (Lighthouse CI):
  Setup:
    npm install --save-dev @lhci/cli

  Config (.lighthouserc.json):
    {
      "ci": {
        "collect": {
          "url": ["http://localhost:8080"],
          "numberOfRuns": 3
        },
        "assert": {
          "assertions": {
            "first-contentful-paint": ["error", {"maxNumericValue": 3000}],
            "interactive": ["error", {"maxNumericValue": 3000}]
          }
        }
      }
    }

Container Performance (Docker):
  # .github/workflows/nfr-validation.yml
  - name: Validate NFR1 (Startup) and NFR2 (Memory)
    run: |
      START=$(date +%s)
      docker-compose up -d
      docker-compose exec app curl --retry 10 --retry-delay 3 http://localhost:8000/api/health
      END=$(date +%s)
      STARTUP_TIME=$((END - START))

      # NFR1: Startup <30s
      if [ $STARTUP_TIME -gt 30 ]; then
        echo "FAIL: Startup took ${STARTUP_TIME}s (max: 30s)"
        exit 1
      fi

      # NFR2: Memory <2GB
      MEMORY=$(docker stats --no-stream --format "{{.MemUsage}}" app | awk '{print $1}')
      if [[ "$MEMORY" =~ "GiB" ]] && [ "${MEMORY%GiB}" -gt 2 ]; then
        echo "FAIL: Memory usage ${MEMORY} (max: 2GB)"
        exit 1
      fi
```

**Priority:** 🔴 **CRITICAL** - Implement during Epic 1 (Project Foundation)

---

### 2.2 Reliability NFRs (NFR8-NFR14)

| NFR | Testability | Status |
|-----|-------------|--------|
| NFR8: Network failure recovery | ✅ Testable with `pytest-httpx` mock failures | READY |
| NFR9: Malformed feed handling | ✅ Testable with fixture malformed feeds | READY |
| NFR10: AI unavailability graceful degradation | ✅ Testable with `NoOpProvider` | READY |
| NFR11: Data persistence across restarts | ✅ Testable with SQLite + container restart | READY |
| NFR12: Failed transformation retry | ⚠️ Requires retry testing pattern | **NEEDS MITIGATION** |
| NFR13: Exponential backoff | ⚠️ Requires time-based testing | **NEEDS MITIGATION** |
| NFR14: Structured logging | ✅ Testable with `structlog` test utilities | READY |

**Risk TR-005: Retry/Backoff Logic Not Tested**

**Impact:** Critical (if bugs ship)
**Likelihood:** Medium

**Problem:** Exponential backoff logic is notoriously difficult to test. Common bugs:
- Infinite retry loops
- Incorrect backoff multipliers
- Race conditions in retry state
- Max attempts not respected

**Mitigation Strategy:**

```python
# Install time-mocking library
pip install freezegun

# tests/jobs/test_retry_backoff.py
import freezegun
from datetime import datetime, timedelta

@freezegun.freeze_time("2025-12-13 10:00:00")
async def test_exponential_backoff_schedule():
    """
    NFR13: Verify retry backoff intervals.

    Expected schedule per PRD:
    - Attempt 1 failure → retry in 5 min
    - Attempt 2 failure → retry in 15 min
    - Attempt 3 failure → retry in 60 min
    - Attempt 4 → no more retries (max 3)
    """
    job = await jobs_service.create_job(
        "fetch_subscription",
        {"subscription_id": "test-123"}
    )

    # Simulate first failure
    await jobs_service.fail_job(job.id, error="Rate limited")

    # Assert retry scheduled for +5 minutes
    job = await jobs_service.get_job(job.id)
    assert job.status == "pending"
    assert job.attempts == 1
    assert job.next_retry_at == datetime(2025, 12, 13, 10, 5)

    # Fast-forward to retry time
    with freezegun.freeze_time("2025-12-13 10:05:00"):
        await jobs_service.retry_job(job.id)
        await jobs_service.fail_job(job.id, error="Rate limited")

        # Assert retry scheduled for +15 minutes from original time
        job = await jobs_service.get_job(job.id)
        assert job.attempts == 2
        assert job.next_retry_at == datetime(2025, 12, 13, 10, 20)

    # Fast-forward to second retry
    with freezegun.freeze_time("2025-12-13 10:20:00"):
        await jobs_service.retry_job(job.id)
        await jobs_service.fail_job(job.id, error="Rate limited")

        # Assert retry scheduled for +60 minutes
        job = await jobs_service.get_job(job.id)
        assert job.attempts == 3
        assert job.next_retry_at == datetime(2025, 12, 13, 11, 20)

    # Fast-forward to third retry
    with freezegun.freeze_time("2025-12-13 11:20:00"):
        await jobs_service.retry_job(job.id)
        await jobs_service.fail_job(job.id, error="Rate limited")

        # Assert NO MORE RETRIES scheduled
        job = await jobs_service.get_job(job.id)
        assert job.status == "failed"
        assert job.attempts == 3  # Max attempts reached
        assert job.next_retry_at is None


async def test_retry_infinite_loop_prevention():
    """
    NFR13: Ensure retry logic cannot create infinite loops.
    """
    job = await jobs_service.create_job("test_task", {})

    # Simulate 100 failures
    for i in range(100):
        await jobs_service.fail_job(job.id, error="Test failure")

    # Assert job is permanently failed after max attempts
    job = await jobs_service.get_job(job.id)
    assert job.status == "failed"
    assert job.attempts <= 3  # Never exceeds max
    assert "max attempts" in job.error_message.lower()
```

**Priority:** 🔴 **CRITICAL** - Implement during Epic 3 (Content Aggregation)

---

### 2.3 Integration Compatibility NFRs (NFR15-NFR21)

| NFR | Target | Testability | Automation |
|-----|--------|-------------|------------|
| NFR15: RSS 2.0 validator compliance | Pass feedvalidator.org | ✅ Testable | `feedvalidator` library |
| NFR16: iTunes podcast extensions | Required tags present | ✅ Testable | XML parsing assertions |
| NFR17: Sonarr API spec compliance | Match documented endpoints | ⚠️ Manual | Contract testing recommended |
| NFR18: Radarr API spec compliance | Match documented endpoints | ⚠️ Manual | Contract testing recommended |
| NFR19: Plex media serving compatibility | Plex recognizes files | ⚠️ Manual | Smoke tests only |
| NFR20: Jellyfin compatibility | Jellyfin recognizes files | ⚠️ Manual | Smoke tests only |
| NFR21: OPML 2.0 compliance | Valid OPML structure | ✅ Testable | XML schema validation |

**Test Pattern for NFR15 (RSS Validation):**

```python
# tests/feeds/test_rss_compliance.py
from feedvalidator import validateString

async def test_generated_podcast_feed_is_valid_rss(feeds_service):
    """NFR15: Generated feeds pass RSS 2.0 validation"""
    feed_xml = await feeds_service.generate_podcast_feed(feed_id="test")

    # Validate against RSS 2.0 spec
    events = validateString(feed_xml)

    # Assert no errors (warnings are acceptable)
    errors = [e for e in events if e.get('level') == 'error']
    assert len(errors) == 0, f"RSS validation errors: {errors}"


async def test_podcast_feed_includes_itunes_extensions(feeds_service):
    """NFR16: Podcast feeds include required iTunes tags"""
    feed_xml = await feeds_service.generate_podcast_feed(feed_id="test")

    import xml.etree.ElementTree as ET
    root = ET.fromstring(feed_xml)

    # Assert iTunes namespace present
    assert 'http://www.itunes.com/dtds/podcast-1.0.dtd' in root.attrib

    # Assert required iTunes tags
    channel = root.find('channel')
    assert channel.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}author') is not None
    assert channel.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}category') is not None
```

---

## 3. Test Strategy Completeness

### 3.1 Current Test Coverage

✅ **Well-Covered:**
- API contract testing (Playwright fixtures + httpx)
- Database migration testing (Alembic ready)
- UI component structure (Vitest + React Testing Library mentioned)
- Custom E2E fixtures (subscription, content, job factories)

⚠️ **Gaps Identified:**

| Gap | Impact | Epic Affected | Priority |
|-----|--------|---------------|----------|
| NFR performance benchmarks | Miss targets in prod | Epic 1 | 🔴 CRITICAL |
| External integration mocking | Flaky CI, API costs | Epic 3, 4 | 🔴 CRITICAL |
| AI quality regression testing | Silent degradation | Epic 4 | 🔴 CRITICAL |
| Retry/backoff logic testing | Production retry storms | Epic 3 | 🔴 CRITICAL |
| Media pipeline test strategy | Slow tests, CI bloat | Epic 4 | 🟡 HIGH |
| PWA offline behavior testing | PWA not functional | Epic 5 | 🟡 HIGH |
| Accessibility automation | WCAG violations ship | Epic 5 | 🟡 HIGH |
| Security testing (OWASP) | Vulnerabilities ship | Epic 7 | 🟢 MEDIUM |

---

### 3.2 Test Pyramid Recommendation

```
         /\
        /  \       E2E (Playwright)
       /10% \      - Full user journeys (FR1-FR61)
      /------\     - Real browser + real backend
     /        \    - Marcus, Sofia, Jordan user stories
    /  Integ  \   Integration Tests (pytest + VCR.py)
   /    20%    \   - API contracts
  /------------\   - External service contract testing (VCR)
 /              \  - Database integration (Alembic migrations)
/      Unit      \ Unit Tests (pytest + Vitest)
/      70%       \ - Business logic isolation
/________________\ - Domain service tests
                   - Component tests (React)

Cross-Cutting Test Layers:
├── Performance: pytest-benchmark + Lighthouse CI (NFR1-7)
├── Accessibility: axe-core in E2E (NFR27-31)
├── Security: OWASP ZAP baseline scan (NFR22-26)
├── Contract: VCR.py for external APIs
└── NFR Validation: Custom assertions per requirement
```

---

### 3.3 Epic-Level Test Strategy

#### Epic 1: Project Foundation ✅
**Testability: 9/10**

**Test Focus:**
- Docker build reproducibility
- Configuration layering (env → YAML → DB → defaults)
- Database migrations (Alembic up/down)
- Health endpoint availability

**Key Tests:**
```python
# tests/core/test_config.py
def test_config_priority_order(monkeypatch):
    """Env vars override YAML override DB override defaults"""
    monkeypatch.setenv("RSS_AI__PROVIDER", "openai")
    config = Settings(_yaml_path="fixtures/config.yaml")
    assert config.ai.provider == "openai"  # Env wins

# tests/core/test_database.py
async def test_alembic_upgrade_downgrade():
    """Migrations are reversible"""
    alembic_upgrade("head")
    alembic_downgrade("base")
    alembic_upgrade("head")  # Should succeed
```

**Gaps:** NFR1/NFR2 performance validation → **Add Docker startup benchmark**

---

#### Epic 2: Subscription Management ✅
**Testability: 9/10**

**Test Focus:**
- CRUD operations (FR1-FR9)
- OPML import/export (NFR21)
- Tag management
- Duplicate detection

**Key Tests:**
```python
# Already scaffolded in tests/e2e/subscriptions.spec.ts
# Need to add:

async def test_opml_import_malformed_xml():
    """NFR9: Malformed OPML doesn't crash system"""
    malformed_opml = "<opml><bad></xml>"
    response = await client.post("/api/subscriptions/import", files={"file": malformed_opml})
    assert response.status_code == 400
    assert response.json()["code"] == "SUBSCRIPTION_IMPORT_INVALID_OPML"
```

**Gaps:** OPML parsing edge cases → **Add fuzzing tests**

---

#### Epic 3: Content Aggregation ⚠️
**Testability: 7/10**

**Test Focus:**
- Feed fetching (FR10-FR12)
- Deduplication logic
- Feed health monitoring (FR46-FR49)
- Automatic retry with backoff (NFR13)

**Critical Gap: External Integration Mocking**

**Risk TR-002: YouTube/RSS Flaky Tests**

**Impact:** High
**Likelihood:** High

**Problem:**
- Real YouTube fetches will hit rate limits
- Real RSS feeds can go offline
- Network I/O makes tests slow and flaky

**Mitigation: VCR.py HTTP Recording**

```bash
# Install VCR
pip install vcrpy pytest-vcr
```

```python
# conftest.py
import pytest

@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization", "api-key"],
        "record_mode": "once",  # Record on first run, replay thereafter
        "match_on": ["uri", "method"],
    }

# tests/content/test_aggregator.py
@pytest.mark.vcr
async def test_fetch_youtube_channel():
    """
    FR10: Fetch YouTube content.

    First run: Records real HTTP interaction to cassette.
    Subsequent runs: Replay from cassette (fast, deterministic).
    """
    aggregator = ContentAggregator()
    items = await aggregator.fetch_youtube_channel("UC_test_channel")

    assert len(items) > 0
    assert items[0].title is not None

# VCR cassette stored in: tests/fixtures/vcr_cassettes/test_fetch_youtube_channel.yaml
```

**Test Strategy:**
```
Unit Tests (70%):
  - Mock all external HTTP calls with pytest-mock
  - Test error handling for each failure mode
  - Test deduplication logic

Integration Tests (20%):
  - VCR.py cassettes for real API contract validation
  - Record once, replay in CI (fast + deterministic)
  - Detect API contract breakage

E2E Tests (10%):
  - Real YouTube fetch (1 Creative Commons video)
  - Run ONLY on merge to main or nightly
```

**Priority:** 🔴 **CRITICAL** - Implement before Epic 3 development

---

#### Epic 4: Transformation Pipeline ⚠️
**Testability: 6/10 - LOWEST SCORE**

**Test Focus:**
- Subtitle extraction (FR20)
- AI transposition (FR21-FR23)
- Queue management (FR24-FR27)
- Quality validation (PRD quality bar)

**Critical Gaps:**

##### Gap 1: AI Quality Regression Testing

**Risk TR-004: AI Quality Degradation**

**Impact:** High
**Likelihood:** Medium

**Problem:**
AI transposition quality can silently degrade when:
- Prompts are modified
- AI models are updated
- Input edge cases aren't covered

**PRD Quality Bar:**
- Flesch reading ease score > 60
- No timestamp artifacts
- Proper paragraph structure
- No verbal artifacts (um, uh, like)

**Mitigation Strategy:**

```bash
# Install quality analysis tools
pip install textstat
```

```python
# tests/transformations/test_quality.py
import textstat
import re

def assert_article_quality(text: str, baseline: str = None):
    """
    Comprehensive quality validation for transformed articles.

    Checks:
    1. Flesch reading ease >= 60 (readable by general audience)
    2. No verbal artifacts
    3. No visual references
    4. Proper paragraph structure (>= 3 paragraphs)
    5. Optional: Similarity to known-good baseline
    """
    # Flesch reading ease
    flesch_score = textstat.flesch_reading_ease(text)
    assert flesch_score >= 60, f"Flesch score {flesch_score} < 60 (hard to read)"

    # No verbal artifacts
    verbal_artifacts = re.findall(r'\b(um|uh|like|you know|right)\b', text, re.I)
    assert len(verbal_artifacts) == 0, f"Found verbal artifacts: {verbal_artifacts}"

    # No visual references
    visual_refs = re.findall(r'(as you can see|on screen|this video)', text, re.I)
    assert len(visual_refs) == 0, f"Found visual references: {visual_refs}"

    # Paragraph structure
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    assert len(paragraphs) >= 3, f"Only {len(paragraphs)} paragraphs (expected >=3)"

    # Optional: Baseline similarity check for regression detection
    if baseline:
        from difflib import SequenceMatcher
        similarity = SequenceMatcher(None, text, baseline).ratio()
        assert similarity > 0.85, f"Output diverged from baseline (similarity: {similarity})"


async def test_subtitle_transformation_quality():
    """
    FR21-23: AI transformation produces quality articles.

    Uses fixture:
    - tests/fixtures/ai_transformations/youtube_subtitles_sample.vtt
    - tests/fixtures/ai_transformations/expected_output_baseline.md
    """
    subtitles = load_fixture("youtube_subtitles_sample.vtt")
    baseline = load_fixture("expected_output_baseline.md")

    result = await transformation_service.subtitle_to_article(
        subtitles,
        ai_provider=get_real_ai_provider()  # Or mock for unit tests
    )

    assert_article_quality(result.text, baseline=baseline)


async def test_verbal_artifact_removal():
    """FR22: Verbal artifacts are removed"""
    input_text = "Um, so like, you know, this is, uh, really important, right?"

    result = await transformation_service.clean_verbal_artifacts(input_text)

    assert "um" not in result.lower()
    assert "uh" not in result.lower()
    assert "like" not in result.lower()  # When used as filler


async def test_visual_reference_conversion():
    """FR23: Visual references converted to verbal descriptions"""
    input_text = "As you can see here on the screen, the button is red."

    result = await transformation_service.convert_visual_references(
        input_text,
        ai_provider=get_ai_provider()
    )

    assert "as you can see" not in result.lower()
    assert "on the screen" not in result.lower()
    # Should describe what was shown instead
```

**Baseline Fixture Strategy:**
```
tests/fixtures/ai_transformations/
├── youtube_subtitles_sample.vtt        # Input
├── expected_output_baseline.md         # Known-good output
├── youtube_subtitles_with_artifacts.vtt
├── expected_cleaned_baseline.md
└── README.md                            # How to update baselines
```

**Priority:** 🔴 **CRITICAL** - Implement before Epic 4 development

---

##### Gap 2: Media Pipeline Test Strategy

**Risk TR-008: Media Pipeline Tests Too Slow**

**Impact:** Medium (developer experience)
**Likelihood:** High

**Problem:**
Your PRD states: "Real yt-dlp + FFmpeg - No mocking media"

This creates:
- Slow tests (downloading real videos)
- Brittle tests (video availability, rate limits)
- CI bloat (media storage in artifacts)

**Mitigation: Layered Testing Strategy**

```
Layer 1: Unit Tests (70%) - FAST
  Mock yt-dlp responses
  Use fixture subtitle files
  Test parsing logic only

Layer 2: Integration Tests (20%) - MEDIUM
  Use VCR.py to record yt-dlp HTTP interactions
  Store small test videos (~1MB) in fixtures/
  Test full pipeline with recorded data

Layer 3: E2E Smoke Tests (10%) - SLOW
  Download 1 real YouTube video (Creative Commons)
  Run full transformation pipeline
  Verify end-to-end quality
  Run ONLY on merge to main (not every PR)
```

**Implementation:**

```python
# tests/transformations/test_extraction_unit.py (FAST)
async def test_subtitle_extraction_from_vtt_file():
    """Unit test: Parse VTT file without yt-dlp"""
    vtt_content = load_fixture("youtube_subtitles_sample.vtt")

    extractor = SubtitleExtractor()
    subtitles = extractor.parse_vtt(vtt_content)

    assert len(subtitles) > 0
    assert subtitles[0].text is not None


# tests/transformations/test_extraction_integration.py (MEDIUM)
@pytest.mark.vcr
async def test_youtube_subtitle_extraction_with_vcr():
    """Integration test: yt-dlp interaction recorded to cassette"""
    extractor = YouTubeExtractor()

    # First run: Records real yt-dlp HTTP calls
    # Subsequent runs: Replays from cassette (fast)
    subtitles = await extractor.extract_subtitles("dQw4w9WgXcQ")

    assert subtitles is not None


# tests/transformations/test_pipeline_e2e.py (SLOW)
@pytest.mark.slow
@pytest.mark.skipif(not os.getenv("RUN_SLOW_TESTS"), reason="Slow E2E test")
async def test_full_transformation_pipeline_real_video():
    """
    E2E smoke test: Real YouTube video transformation.

    Uses Creative Commons licensed test video.
    Runs ONLY on merge to main or when RUN_SLOW_TESTS=1.
    """
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Short CC video

    transformation = await transformation_service.transform_video_to_article(
        video_url,
        ai_provider=get_real_ai_provider()
    )

    assert transformation.status == "completed"
    assert_article_quality(transformation.result_text)


# pytest.ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
```

**CI Configuration:**
```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - run: pytest -m "not slow" --cov

  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests/integration --vcr-record=none

  e2e-slow-tests:
    # Only run on merge to main or nightly
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: RUN_SLOW_TESTS=1 pytest -m slow
```

**Priority:** 🟡 **HIGH** - Implement during Epic 4 development

---

#### Epic 5: Web App & PWA ⚠️
**Testability: 7/10**

**Test Focus:**
- Responsive layout (NFR27-28)
- Accessibility (NFR29-31)
- PWA installability (FR31)
- Theme toggle (FR32-33)
- Offline behavior

**Critical Gaps:**

##### Gap 1: PWA Offline Behavior Testing

**Risk TR-006: PWA Not Functional Offline**

**Impact:** Medium
**Likelihood:** Medium

**Problem:**
PWA offline behavior is complex to test:
- Service worker registration
- Cache storage strategies
- Network interception
- Install prompt triggering

**Mitigation: Playwright PWA Testing**

```typescript
// tests/e2e/pwa.spec.ts
import { test, expect } from '@playwright/test';

test('PWA offline shell loads after installation', async ({ page, context }) => {
  // 1. Load app and wait for service worker registration
  await page.goto('/');
  await page.waitForFunction(() => navigator.serviceWorker.ready);

  // 2. Verify service worker is registered
  const swRegistration = await page.evaluate(() =>
    navigator.serviceWorker.getRegistration()
  );
  expect(swRegistration).toBeTruthy();

  // 3. Cache should be populated after first load
  const cacheNames = await page.evaluate(async () =>
    await caches.keys()
  );
  expect(cacheNames.length).toBeGreaterThan(0);

  // 4. Go offline
  await context.setOffline(true);

  // 5. Reload - cached shell should load
  await page.reload();

  // 6. Verify critical UI elements are visible
  await expect(page.getByRole('navigation')).toBeVisible();
  await expect(page.getByRole('main')).toBeVisible();

  // 7. Verify graceful API failure messaging
  await expect(page.getByText(/offline|no connection/i)).toBeVisible();

  // 8. Go back online
  await context.setOffline(false);
  await page.reload();

  // 9. Verify full functionality restored
  await expect(page.getByText(/offline/i)).not.toBeVisible();
});


test('PWA install prompt can be triggered', async ({ page }) => {
  await page.goto('/');

  // Mock beforeinstallprompt event
  await page.evaluate(() => {
    const event = new Event('beforeinstallprompt');
    (event as any).prompt = () => Promise.resolve();
    (event as any).userChoice = Promise.resolve({ outcome: 'accepted' });
    window.dispatchEvent(event);
  });

  // Verify install button appears
  await expect(page.getByRole('button', { name: /install|add to home/i })).toBeVisible();
});
```

**Priority:** 🟡 **HIGH** - Implement during Epic 5 development

---

##### Gap 2: Accessibility Testing Automation

**Risk TR-007: WCAG Violations Ship to Production**

**Impact:** Medium
**Likelihood:** Medium

**NFRs:**
- NFR29: WCAG 2.1 AA color contrast
- NFR30: Human-readable errors
- NFR31: No silent failures

**Mitigation: axe-core Integration**

```bash
npm install --save-dev @axe-core/playwright
```

```typescript
// tests/e2e/accessibility.spec.ts
import { test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('dashboard page is accessible', async ({ page }) => {
  await page.goto('/');

  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});

test('subscription form is accessible', async ({ page }) => {
  await page.goto('/subscriptions');
  await page.getByRole('button', { name: /add subscription/i }).click();

  const results = await new AxeBuilder({ page })
    .include('[role="dialog"]')  // Modal only
    .analyze();

  expect(results.violations).toEqual([]);
});

test('keyboard navigation works throughout app', async ({ page }) => {
  await page.goto('/');

  // Tab through interactive elements
  await page.keyboard.press('Tab');
  await expect(page.locator(':focus')).toBeVisible();

  // Verify focus indicators
  const focusedElement = page.locator(':focus');
  const outlineWidth = await focusedElement.evaluate(el =>
    window.getComputedStyle(el).outlineWidth
  );
  expect(parseFloat(outlineWidth)).toBeGreaterThan(1);  // Visible focus ring
});
```

**CI Integration:**
```yaml
# .github/workflows/accessibility.yml
name: Accessibility Tests

on: [push, pull_request]

jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - run: npm ci
      - run: npx playwright test --grep @a11y

      - name: Upload a11y report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: accessibility-report
          path: test-results/
```

**Priority:** 🟡 **HIGH** - Implement during Epic 5 development

---

#### Epic 6: Content Delivery & Integrations ✅
**Testability: 8/10**

**Test Focus:**
- RSS 2.0 compliance (NFR15-16)
- Plex/Jellyfin compatibility (NFR19-20)
- *arr API integration (NFR17-18)

**Test Strategy:**
```python
# tests/feeds/test_podcast_compliance.py
from feedvalidator import validateString

async def test_podcast_feed_rss_compliance():
    """NFR15: Generated podcast feeds pass RSS 2.0 validation"""
    feed_xml = await feeds_service.generate_podcast_feed("test-feed")

    events = validateString(feed_xml)
    errors = [e for e in events if e.get('level') == 'error']

    assert len(errors) == 0

# tests/integrations/test_plex.py
@pytest.mark.smoke
async def test_plex_recognizes_media_files():
    """NFR19: Plex can index generated media"""
    # This is a SMOKE TEST - requires real Plex instance
    # Run only in dedicated test environment
    pass  # Manual verification for MVP
```

**Gaps:** Plex/Jellyfin compatibility requires manual smoke testing (acceptable for MVP)

---

#### Epic 7: API Security & Notifications ✅
**Testability: 9/10**

**Test Focus:**
- API key generation (NFR22-23)
- Secure storage (NFR23)
- Push notifications (FR59-61)
- HTTPS support (NFR26)

**Test Strategy:**
```python
# tests/security/test_api_keys.py
import secrets

async def test_api_key_generation_is_cryptographically_secure():
    """NFR22: API keys use cryptographically secure randomness"""
    key1 = await api_key_service.generate_key()
    key2 = await api_key_service.generate_key()

    # Keys are unique
    assert key1 != key2

    # Keys have sufficient entropy (>=32 bytes)
    assert len(secrets.token_urlsafe(32)) <= len(key1)


async def test_api_keys_stored_hashed():
    """NFR23: API keys stored as hashes, not plaintext"""
    raw_key = await api_key_service.generate_key()

    # Fetch from database
    stored_key = await db.execute(
        select(APIKey).where(APIKey.key_prefix == raw_key[:8])
    )

    # Raw key should NOT appear in database
    assert stored_key.key_hash != raw_key
    assert len(stored_key.key_hash) > 32  # Hash length
```

**Gaps:** None - security testing strategy is sound

---

## 4. Risk Register & Mitigation Roadmap

| Risk ID | Risk Description | Impact | Likelihood | Epic | Mitigation Priority | Owner |
|---------|------------------|--------|------------|------|---------------------|-------|
| **TR-001** | NFR performance targets not validated in CI | High | High | Epic 1 | 🔴 **CRITICAL** | Foundation |
| **TR-002** | YouTube rate limiting breaks CI | High | Medium | Epic 3 | 🔴 **CRITICAL** | Aggregation |
| **TR-003** | OpenAI API costs spiral in tests | Medium | High | Epic 4 | 🔴 **CRITICAL** | Transformation |
| **TR-004** | AI quality silently degrades over time | High | Medium | Epic 4 | 🔴 **CRITICAL** | Transformation |
| **TR-005** | Retry logic causes infinite loops in production | Critical | Low | Epic 3 | 🔴 **CRITICAL** | Aggregation |
| **TR-006** | PWA doesn't work offline despite FR31 | Medium | Medium | Epic 5 | 🟡 **HIGH** | Web App |
| **TR-007** | WCAG violations ship to production | Medium | Medium | Epic 5 | 🟡 **HIGH** | Web App |
| **TR-008** | Media pipeline tests too slow for TDD | Low | High | Epic 4 | 🟡 **HIGH** | Transformation |

---

### Mitigation Roadmap

#### Phase 1: Before Epic 1 Completion (Foundation)
- [ ] Add pytest-benchmark for API latency testing (NFR6)
- [ ] Add Docker startup time validation (NFR1)
- [ ] Add memory usage monitoring (NFR2)
- [ ] Add Lighthouse CI for frontend performance (NFR3-4)

#### Phase 2: Before Epic 3 Development (Aggregation)
- [ ] Implement VCR.py for external API recording
- [ ] Add freezegun for retry/backoff time-based testing
- [ ] Create fixture strategy for malformed feeds
- [ ] Add contract tests for RSS/YouTube APIs

#### Phase 3: Before Epic 4 Development (Transformation)
- [ ] Create AI quality baseline fixtures
- [ ] Implement textstat quality assertions
- [ ] Add layered media pipeline test strategy
- [ ] Mock AI providers by default, real API optional

#### Phase 4: During Epic 5 Development (Web App)
- [ ] Add axe-core accessibility testing
- [ ] Implement PWA offline behavior tests
- [ ] Add Playwright network interception
- [ ] Validate keyboard navigation

---

## 5. Quality Gate Decision

### Implementation Readiness Assessment

**Architecture Testability:** ✅ 8.5/10
**Test Framework Readiness:** ✅ Playwright + pytest scaffolded
**Critical Risks Identified:** ⚠️ 4 critical, 2 high
**Mitigation Plan:** ✅ Clear action items per epic

---

### **DECISION: CONDITIONAL PASS** ⚠️

**Recommendation:** **Proceed to Phase 3 (Implementation)** with the following **mandatory conditions:**

#### 🔴 **Blocking Conditions (Must Complete Before Epic Completion):**

**Epic 1 (Foundation):**
- [ ] Implement NFR performance validation (TR-001)
  - pytest-benchmark for API latency
  - Docker startup time measurement
  - Memory usage monitoring
  - Lighthouse CI for frontend

**Epic 3 (Aggregation):**
- [ ] Implement VCR.py HTTP recording (TR-002)
- [ ] Implement retry/backoff time-based testing (TR-005)

**Epic 4 (Transformation):**
- [ ] Implement AI quality baseline testing (TR-004)
- [ ] Implement layered media pipeline testing (TR-008)
- [ ] Mock OpenAI by default to prevent cost spirals (TR-003)

**Epic 5 (Web App):**
- [ ] Implement PWA offline behavior tests (TR-006)
- [ ] Implement accessibility automation with axe-core (TR-007)

---

### Why Conditional vs. Full Pass?

**Strengths:**
- ✅ Solid architectural foundation
- ✅ Test framework already in place
- ✅ Good test-first culture demonstrated

**Concerns:**
- ⚠️ 4 critical risks could create **significant technical debt** if not addressed early
- ⚠️ NFR validation gaps risk shipping non-compliant code
- ⚠️ External integration testing strategy undefined

**Why Proceed Anyway:**
- All identified risks have **clear, well-established mitigation patterns**
- Mitigations can be implemented **incrementally per epic**
- Blocking implementation for test infrastructure would delay user value
- Team has demonstrated test-first mindset (Playwright fixtures already built)

---

## 6. Implementation Handoff

### For Development Team

**Test-First Development Checklist:**

When implementing each story, ensure:
- [ ] Unit tests written BEFORE implementation
- [ ] Integration tests added for external dependencies
- [ ] E2E test covers user journey (if UI story)
- [ ] NFR assertions added where applicable
- [ ] Performance benchmarks added for critical paths
- [ ] Accessibility checks for new UI components
- [ ] Security tests for authentication/authorization changes

**Test Execution Strategy:**

```bash
# Fast feedback loop (run on every commit)
pytest -m "not slow" --cov
npm test

# Full test suite (run before PR)
pytest --cov
npx playwright test

# Performance validation (run on PR merge)
pytest tests/performance --benchmark-only
npm run lighthouse-ci

# E2E smoke tests (run on merge to main)
RUN_SLOW_TESTS=1 pytest -m slow
npx playwright test --project=chromium
```

---

### Test Data Management

**Fixture Organization:**
```
tests/fixtures/
├── youtube/
│   ├── subtitles_sample.vtt
│   ├── metadata_sample.json
│   └── test_video_short.mp4 (1MB)
├── rss/
│   ├── valid_feed.xml
│   ├── malformed_feed.xml
│   └── podcast_feed_with_itunes.xml
├── ai_baselines/
│   ├── subtitle_input_sample.vtt
│   └── expected_article_baseline.md
└── vcr_cassettes/
    ├── youtube_fetch.yaml
    └── openai_completion.yaml
```

---

### CI/CD Pipeline

**Recommended GitHub Actions Workflow:**

```yaml
name: CI

on: [push, pull_request]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install -r requirements-test.txt
      - run: pytest -m "not slow" --cov --cov-report=xml
      - uses: codecov/codecov-action@v3

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm test -- --coverage
      - run: npm run lint

  test-e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker-compose up -d
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: test-results/

  test-performance:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests/performance --benchmark-only
      - run: npm run lighthouse-ci

  test-accessibility:
    runs-on: ubuntu-latest
    steps:
      - run: npx playwright test --grep @a11y

  test-nfr-validation:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: docker-compose up -d
      - run: ./scripts/validate-nfr.sh  # Startup time, memory usage
```

---

## 7. Next Steps

### Immediate Actions (Before Development Starts)

1. **Install test dependencies:**
   ```bash
   # Backend
   cd backend
   uv add --dev pytest-benchmark freezegun vcrpy pytest-vcr textstat

   # Frontend
   cd frontend
   npm install --save-dev @axe-core/playwright @lhci/cli
   ```

2. **Create test fixture directories:**
   ```bash
   mkdir -p tests/fixtures/{youtube,rss,ai_baselines,vcr_cassettes}
   ```

3. **Configure VCR.py:**
   ```python
   # tests/conftest.py
   @pytest.fixture(scope="module")
   def vcr_config():
       return {
           "filter_headers": ["authorization", "api-key"],
           "record_mode": "once",
       }
   ```

4. **Add performance test placeholders:**
   ```python
   # tests/performance/test_api.py
   def test_subscription_list_latency(benchmark, client):
       """NFR6: API responds <200ms"""
       response = benchmark(lambda: client.get("/api/subscriptions"))
       assert benchmark.stats.mean < 0.2
   ```

---

### Per-Epic Test Implementation

**Epic 1:** Focus on NFR1/NFR2 validation
**Epic 3:** Implement VCR.py + retry testing
**Epic 4:** Add AI quality baselines + media pipeline layers
**Epic 5:** Integrate axe-core + PWA offline tests

---

## 8. Conclusion

Your architecture demonstrates **strong testability fundamentals**, with a domain-based structure that enables isolated testing and an existing E2E framework showing test-first culture.

The identified risks are **real but manageable** - all have well-established mitigation patterns in the testing community. The key is to **implement mitigations early** (Epic 1-4) rather than accumulating technical debt.

**Final Assessment:** **PROCEED TO IMPLEMENTATION** with vigilance on the 4 critical test risks.

---

**Test Architect Sign-Off:**
Murat - Master Test Architect
Date: 2025-12-13

---

**Appendix: Tool References**

| Tool | Purpose | Documentation |
|------|---------|---------------|
| pytest-benchmark | API latency testing | https://pytest-benchmark.readthedocs.io/ |
| freezegun | Time-based testing | https://github.com/spulec/freezegun |
| vcrpy | HTTP recording | https://vcrpy.readthedocs.io/ |
| textstat | Text readability metrics | https://github.com/textstat/textstat |
| axe-core | Accessibility testing | https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright |
| Lighthouse CI | Performance auditing | https://github.com/GoogleChrome/lighthouse-ci |
| feedvalidator | RSS validation | https://github.com/w3c/feedvalidator |

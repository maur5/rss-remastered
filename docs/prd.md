---
stepsCompleted: [1, 2, 3, 4, 6, 7, 8, 9, 10, 11]
inputDocuments:
  - docs/analysis/brainstorming-session-2025-12-13.md
documentCounts:
  briefs: 0
  research: 0
  brainstorming: 1
  projectDocs: 0
workflowType: 'prd'
lastStep: 11
completedAt: '2025-12-13'
project_name: 'rss-remastered'
user_name: 'Mo'
date: '2025-12-13'
---

# Product Requirements Document - rss-remastered

**Author:** Mo
**Date:** 2025-12-13

## Executive Summary

RSS-Remastered restores **subscription sovereignty** - you declare what you want, consumed when published, in whatever format fits your life. Under the hood, it's a really smart transcoder with optional AI features. But what it *means* is taking back control from algorithmic feeds that bury what you asked for and serve what *they* want you to see.

**The Experience:** Your morning commute becomes an audio digest of exactly what you subscribed to - YouTube videos become podcasts that make sense without visuals, articles become narrated conversations. Nothing buried, nothing missed. Switch from video at your desk to audio in your car, pick up exactly where you left off, with the content intelligently adapted rather than crudely converted.

**Target Audience:** Power users already running *arr stack (Sonarr, Radarr, Prowlarr) who want to extend their self-hosted media ecosystem. These users understand Docker, manage multiple services, and value owning their consumption pipeline. Newcomers to self-hosting are welcome but not the primary design target for v1.

**Deployment Story:** Single container, single compose entry, full capability from day one. The "monolith-first, modular-inside, decouple-later" architecture respects the cognitive load of the self-hosting crowd - no orchestration complexity required to get started.

### What Makes This Special

**On-demand transformation enables everything.** Unlike tools that pre-compute and serve static output, RSS-Remastered transforms at the moment of consumption. This isn't just efficient (subscribe to 100 channels, consume 20% = 80% wasted compute avoided) - it enables live adjustability. Pre-computed locks you in. On-demand means infinite versions, real-time parameter changes, and responsive steering.

**The killer AI feature:** Intelligent transposition - not crude conversion, but content *refactored* to make sense in the target format.

**v1 Scope:**
- YouTube → Audio: Visual references automatically described verbally
- Article → Audio: TTS with proper pacing and natural narration

**v2+ Scope (out of scope for v1):**
- Article → Visual presentation (lean-back reading)
- Cross-format summarization and briefings
- Companion conversation features

**Core without AI, enhanced with AI.** The pipeline works without AI: aggregation, serving, basic conversion. AI is the enhancement layer - intelligent transposition, companion features, preference learning. Graceful degradation ensures no one is locked out based on their hardware.

## Project Classification

**Technical Type:** Web Application + API Backend
**Domain:** General (Consumer/Prosumer Media Tooling)
**Complexity:** Medium (AI enhancement layer, no regulatory overhead)
**Project Context:** Greenfield - new project
**Target Persona:** Self-hosting power users with existing *arr stack
**Architecture:** Monolith-first, modular-inside, decouple-later
**Deployment:** Single Docker container with Docker Compose support

Integrates with existing *arr stack ecosystem (Sonarr, Radarr, Prowlarr) and serves content via Plex/Jellyfin, podcast feeds, and web UI.

## Success Criteria

### User Success

- **Subscription sovereignty achieved:** 100% of subscribed content delivered without algorithmic filtering or suppression
- **Format fluidity realized:** Users consume same content across 2+ formats without manual intervention
- **Intelligent adaptation quality:** AI-transposed content meets concrete quality bar:
  - Proper paragraph structure (no wall of text)
  - No timestamp artifacts or speaker label noise (unless contextually relevant)
  - Flesch reading ease score > 60 (readable by general audience)
  - Passes "would I read this?" test
- **Session continuity:** Resume position preserved across format switches and devices
- **Zero content missed:** "Nothing buried, nothing missed" - subscriptions delivered as published

### Business Success

- **Personal daily driver:** Creator dogfooding RSS-Remastered as primary media consumption tool from Week 1
- **Community traction (6-month targets):**
  - >100 GitHub stars
  - >10 forks
  - >5 external issues or PRs from community members
- **Ecosystem adoption:** Recognition/adoption within *arr stack community (Reddit mentions, blog posts, integration requests)
- **Contributor growth:** External contributors submitting PRs and extending functionality

### North Star

> RSS-Remastered becomes the reference implementation for **subscription sovereignty** - other projects adopt the framing, the philosophy spreads beyond this single tool. Success isn't just adoption, it's starting a conversation about taking back control from algorithmic feeds.

### Technical Success

- **One-command deployment:** Single `docker-compose up` to fully working system
- **Low resource floor:** MVP runs on 2GB RAM, no GPU required
- **Fast startup:** < 30 seconds from container start to serving content
- **Integration compatibility:** Valid Sonarr/Radarr API integration, compliant podcast RSS feeds, Plex-compatible media serving
- **Graceful degradation:** Handles network failures, malformed feeds, missing content without crashes

### Measurable Outcomes

| Timeframe | Success Indicator |
|-----------|-------------------|
| **Week 1** | Creator dogfooding daily; subscribing to and ingesting content from 3+ source types |
| **Month 1** | Daily personal use with subtitle → article transformation working reliably |
| **Month 3** | Community feedback incorporated, first post-MVP feature shipped |
| **Month 6** | >100 stars, >10 forks, >5 community contributions; companion features in development |

## Product Scope

### MVP - Minimum Viable Product (v1.0)

- Subscribe to YouTube channels, RSS feeds, podcast feeds
- Ingest and store content metadata
- Subtitle → Article intelligent transformation (text-to-text AI transposition)
- Serve via web UI and generated podcast/RSS feeds
- Single Docker container deployment
- **Integration with *arr stack APIs (read direction):** RSS-Remastered reads FROM Sonarr/Radarr to understand existing media library
- Plex/Jellyfin compatible media serving

### Growth Features (Post-MVP)

**v1.1 - Audio Output:**
- Article → Audio (TTS with natural pacing)
- Voice customization options

**v1.2 - Audio Input:**
- Audio → Text (Whisper transcription for content without subtitles)
- Quality chain: Bazarr subs → Manual captions → Auto-captions → Transcribe

*Note: v1.1 and v1.2 are independent tracks - can ship in either order based on user demand and implementation readiness.*

**v1.x - Integration Expansion:**
- *arr stack integration (write direction): RSS-Remastered appears AS a source to Sonarr/Radarr

### Vision (v2+)

- **Companion features:** Conversational selection ("What's interesting?"), content Q&A, cross-source synthesis
- **Cross-media companion:** Browser extension providing live fact-checks and context while consuming content anywhere
- **Video transformations:** Full video-in/video-out processing
- **Live steering:** Adjust transformation parameters mid-stream
- **Preference learning:** Multi-signal learning from behavior, imports, and conversation

## User Journeys

### Journey 1: Marcus Chen - The *arr Stack Power User

Marcus is a software engineer who's been running Sonarr, Radarr, and Prowlarr on his home server for three years. He loves the control - no streaming service can cancel his favorite show or bury it in their algorithm. But there's a gap in his setup: YouTube subscriptions and podcasts still live in walled gardens. He subscribes to 47 YouTube channels - tech reviewers, cooking shows, educational content - but YouTube's "Recommended" feed shows him rage-bait instead of the channels he actually subscribed to.

One evening, while catching up on his favorite tech channel, Marcus realizes he's been "missing" uploads for weeks - YouTube just... didn't show them. That's the last straw. He posts on r/selfhosted: "Is there a Sonarr-like tool for YouTube subscriptions?" Someone replies with a link to RSS-Remastered and the tagline "subscription sovereignty for the *arr stack." Marcus clicks, sees the README, and recognizes the philosophy immediately. This is what he's been looking for.

Setup takes 15 minutes. He adds his docker-compose entry, imports his YouTube subscriptions via OPML, and connects it to his existing Sonarr/Radarr APIs. The web UI shows a clean chronological feed - everything he subscribed to, nothing he didn't. No algorithm. No recommendations. Just his content.

The "aha" moment comes a week later. Marcus has a long commute and usually listens to podcasts. He discovers that RSS-Remastered transformed a 45-minute YouTube video essay into a clean article - proper paragraphs, no "um"s, no "as you can see on screen." He reads it during lunch instead of watching. Same content, different format, his choice.

Six months later, Marcus's RSS-Remastered instance is the hub of his media consumption. He hasn't opened YouTube's app in months - everything flows through his system. When friends complain about the algorithm, he just smiles and shares his setup guide.

### Journey 2: Marcus Chen - Edge Case (Error Recovery)

A few weeks into using RSS-Remastered, Marcus adds a new tech channel he discovered. The next day, he notices episodes aren't appearing in his feed. Instead of mystery or silent failure, the web UI shows a clear status indicator: **"Feed rate-limited by YouTube, retrying in 2 hours"** with a timestamp and a manual "Retry Now" button.

Marcus clicks into the subscription details and sees a history: successful fetches, the rate-limit event, scheduled retry. He understands exactly what's happening. He hits "Retry Now," the fetch succeeds, and the missing episodes appear.

Later, he adds an obscure podcast with a malformed RSS feed. The UI flags it immediately: **"Feed parsing failed - invalid XML at line 47"** with an option to report the issue or try an alternative parser. Marcus copies the error, opens a GitHub issue on the podcast's repo, and moves on. No guessing, no debugging, no frustration.

The key insight: RSS-Remastered treats errors as **expected states** with clear communication, not failures to hide. Marcus always knows what's happening and what he can do about it.

### Journey 3: Sofia Chen - The Household Consumer

Sofia is Marcus's partner. She's not technical - Docker is just "that thing Marcus runs in the basement." But she loves cooking shows, true crime podcasts, and keeping up with a few YouTubers. She doesn't care HOW the content gets to her, she just wants it to work.

One Saturday morning, Marcus mentions he added her favorite cooking channel to "his media thing." Sofia is skeptical but opens Plex on her iPad. There's a new library called "Sofia's Feeds" with a familiar thumbnail - it's the latest episode from her favorite chef. She watches it on the couch. Works fine. No different from before, except... she notices she hasn't seen an ad in 20 minutes.

The real win comes during her evening run. Sofia usually listens to a true crime podcast, but she's caught up on episodes. Marcus had mentioned something about "articles becoming audio." She finds a long-form article from her favorite newsletter in her podcast app - the same app she uses for everything else. It's being read aloud with decent narration. She finishes her run actually looking forward to the next piece.

Sofia never logs into RSS-Remastered's web UI. She doesn't know what Docker is. But her content shows up in Plex and her podcast app, organized by her preferences, without her ever fighting an algorithm. To her, it's just "Marcus's thing" that somehow makes streaming work better.

*Design Note: Sofia's journey assumes Marcus manages subscriptions for her. Future consideration: simple "add subscription" interface accessible to household members without exposing system complexity.*

### Journey 4: Jordan Park - The Integration Builder

Jordan is a developer who runs a personal automation stack - n8n workflows, Home Assistant, a bunch of custom scripts. They discover RSS-Remastered through a Reddit post and immediately see the potential: not just for consuming content, but for building on top of it.

Jordan's first project: a "morning briefing" workflow. They want an audio summary of overnight content from their subscribed feeds, ready to play when their alarm goes off. They dig into RSS-Remastered's API docs and find clean endpoints for subscription management, content retrieval, and transformation requests.

Within a weekend, Jordan has a working prototype. Their n8n workflow triggers at 5:30 AM, queries RSS-Remastered for new content since last night, requests article transformations for the top 5 items by their custom priority score, and queues the results for their morning routine. By the time they're making coffee, their speaker is reading a personalized news digest.

The breakthrough comes when Jordan shares their workflow on GitHub. Other RSS-Remastered users fork it, adapt it, improve it. Someone builds a Home Assistant integration. Someone else creates a Raycast plugin. Jordan's simple automation becomes the seed of a small ecosystem.

Jordan eventually becomes a contributor to RSS-Remastered itself, submitting PRs to improve the API based on patterns they've discovered from their automation work.

### Journey Requirements Summary

| Journey | Capabilities Revealed |
|---------|----------------------|
| **Marcus (Power User)** | OPML import, subscription management, chronological feed, web UI, *arr integration, format transformation (video→article) |
| **Marcus (Edge Case)** | Error visibility, status indicators, retry mechanisms, feed health monitoring, clear failure communication |
| **Sofia (Household)** | Plex library integration, podcast feed generation, per-user content organization, invisible complexity |
| **Jordan (API Consumer)** | RESTful API, content retrieval endpoints, transformation request API, webhook/trigger support, API documentation |

### API Scope Clarification

| Scope | Capabilities | Target User |
|-------|-------------|-------------|
| **MVP API** | *arr integration endpoints, basic content retrieval, subscription CRUD | Marcus (power user automation) |
| **Growth API (v1.x+)** | Full transformation API, webhooks, batch operations, advanced queries | Jordan (integration builders) |

*Note: Don't over-engineer the API for MVP. Marcus and Sofia don't need it. Jordan can wait for v1.x.*

### Discovery & Adoption Requirements

The "how Marcus finds RSS-Remastered" moment surfaces a non-code requirement:

- **README and landing page must communicate the vision instantly**
- Tagline should resonate with *arr stack users: "subscription sovereignty"
- Philosophy should be front-and-center, not buried in features
- Setup instructions visible within 30 seconds of landing

## Innovation & Novel Patterns

### Detected Innovation Areas

**Subscription Sovereignty Philosophy**
RSS-Remastered isn't just a tool - it's a statement. The "subscription sovereignty" framing positions this as a movement against algorithmic control. Unlike aggregators that simply collect feeds, RSS-Remastered actively restores user agency over what they consume and when.

**Flexible Transformation Timing**
The architecture supports multiple transformation paradigms:
- **On-demand**: Transform at moment of consumption (efficient for low-consumption-rate subscriptions)
- **Scheduled batch**: Pre-process during off-peak hours for immediate availability
- **Smart pre-warming**: Predictive transformation based on consumption patterns

This flexibility acknowledges that "on-demand" isn't always optimal - sometimes users want content ready immediately.

**Intelligent Transposition**
Not crude format conversion, but content "refactored" to make sense in the target format. Visual references become verbal descriptions, timestamps become natural transitions. The AI doesn't just convert - it adapts.

**AI Sovereignty**
Users control their AI stack: local models, remote providers, or hybrid approaches. No vendor lock-in, no forced cloud dependencies. The product works without AI and enhances with AI - graceful degradation is a feature, not a fallback.

### Agent Protocol Ecosystem

**Companion Interface Innovation**
Rather than building custom companion UIs (browser extensions, chat interfaces), RSS-Remastered can expose capabilities via emerging agent protocols:

| Protocol | Owner | Maturity | RSS-Remastered Fit |
|----------|-------|----------|-------------------|
| **MCP** (Model Context Protocol) | Anthropic | Production-ready | Primary target - expose as MCP server |
| **A2A** (Agent-to-Agent) | Google/Linux Foundation | Emerging | Monitor for multi-agent orchestration |
| **ACP** (Agent Communication Protocol) | IBM/BeeAI | Emerging | Monitor for enterprise scenarios |

**Strategic Approach:**
1. RSS-Remastered exposes its **own MCP server** - standalone, no external dependencies
2. Users connect via Claude Desktop, custom clients, or their preferred MCP-compatible tools
3. Optional integration with external *arr MCPs **only after maturity analysis** - no reliance on unmaintained community projects
4. Users can manually compose their own MCP stack if desired

This positions RSS-Remastered as potentially the **reference MCP interface** for the self-hosted media ecosystem - not by depending on others, but by being the reliable, well-maintained option.

### Validation Approach

- **MCP Compatibility**: Test against Claude Desktop as reference MCP client
- **Protocol Compliance**: Ensure clean MCP server implementation per spec
- **Integration Testing**: Validate transformation requests via MCP work correctly
- **Graceful Fallback**: Verify full functionality without any MCP client connected

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Agent protocol ecosystem fragmentation | MCP-first with abstraction layer for future protocols |
| External *arr MCP dependency | Standalone-first; no integration until maturity proven |
| Protocol immaturity | Core product works without agent protocols; they're enhancement layer |
| Community project abandonment | RSS-Remastered owns its own MCP implementation completely |

## Web Application + API Technical Requirements

### Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Backend** | Python 3.11+ | Creator preference; strong media ecosystem (yt-dlp, FFmpeg); async-capable |
| **Web Framework** | FastAPI | Modern async Python, auto-generated OpenAPI docs, SSE support, excellent DX |
| **Frontend** | Modern JS/TS SPA | React/Vue/Svelte/SolidJS (TBD at architecture phase) |
| **Dependency Mgmt** | uv | Fast (Rust-based), modern, lock files, from Astral (ruff team) |
| **Config Format** | YAML | Human-readable, familiar to self-hosters, Docker-native |
| **API Format** | JSON | Standard M2M communication |
| **Feed Format** | RSS 2.0 + iTunes extensions | Podcast industry standard |
| **Project Config** | pyproject.toml | PEP 621 single source of truth |

### Testing Strategy

| Component | Tool | Approach |
|-----------|------|----------|
| **Unit/Integration** | pytest + pytest-asyncio | Async-first testing |
| **API Testing** | httpx | Async test client for FastAPI |
| **Coverage** | pytest-cov | Track coverage metrics |
| **Media Pipeline** | Real yt-dlp + FFmpeg | No mocking media - that's where bugs hide |
| **CI Environment** | Docker-based | Reproducible test environment with real dependencies |

### Authentication Model

**API Keys** - Matching *arr ecosystem patterns:
- Simple bearer token authentication for service-to-service
- Generated via web UI or CLI
- VAPID keys auto-generated on first run for Web Push
- Scoped permissions optional (read-only vs read-write) for growth phase

### Database Strategy

| Scale | Database | When to Migrate |
|-------|----------|-----------------|
| **MVP/Household** | SQLite | Sufficient for single-user, handles household fine |
| **Multi-user/Heavy** | PostgreSQL | Consider at ~10 concurrent writers or multi-instance |

*Don't prematurely migrate. SQLite is not a limitation for target use case.*

### Browser Support

**Modern browsers only** (last 2 versions):
- Chrome, Firefox, Safari, Edge (desktop)
- Chrome Mobile, Safari Mobile (iOS/Android)
- No IE11 or legacy support

### Mobile Strategy (PWA)

**Progressive Web App as mobile path:**
- **Responsive design**: Mobile-first CSS, touch-friendly (44x44px min tap targets)
- **Gesture support**: Swipe actions for common operations (mark read, queue transformation)
- **Installable**: Add-to-homescreen capability (manifest.json)
- **Push notifications**: Web Push API with contextual permission prompts (not on first visit)
- **Offline shell**: Service worker caches UI shell for instant load; content requires network

**Notification Use Cases:**

| Notification | Trigger |
|--------------|---------|
| New content available | Subscribed feed has new items |
| Transformation complete | Requested article/audio ready |
| Feed health alert | Subscription failing repeatedly |

### Theme & Visual Design

- **Dark mode default**: Matches self-hoster dashboard aesthetic
- **System preference detection**: Respects `prefers-color-scheme`
- **Manual override**: Toggle in settings for explicit user control
- **Dark-first CSS architecture**: Build dark theme first, light as alternate

### Real-time Updates

| Phase | Technology | Use Case |
|-------|------------|----------|
| **MVP** | Polling | Transformation status, feed refresh |
| **Growth** | Server-Sent Events (SSE) | Live notifications, simpler than WebSockets |
| **Future** | WebSockets | If bidirectional communication needed |

### Rate Limiting Strategy

**Delegate external, manage internal:**

| Concern | Approach |
|---------|----------|
| YouTube rate limits | Delegated to yt-dlp (built-in rate limiting) |
| RSS feed polling | RSS-Remastered manages respectful polling intervals |
| Concurrent transformations | Internal queue with configurable parallelism |
| API abuse | Not a concern for self-hosted deployment |

### Feed Generation Requirements

**Podcast Feed Compliance:**
- RSS 2.0 with iTunes podcast extensions
- Valid XML that passes podcast validator tools
- Enclosure URLs that resolve correctly for podcatchers
- Episode metadata (title, description, duration, artwork) properly populated

### API Surface (MVP)

| Endpoint Category | Purpose |
|------------------|---------|
| `/subscriptions` | CRUD for feed subscriptions |
| `/content` | List/retrieve content items |
| `/feeds` | Generated podcast/RSS feeds |
| `/status` | System health, transformation queue status |
| `/*arr` | Sonarr/Radarr API compatibility endpoints |

*Full API specification deferred to Architecture phase.*

### Implementation Considerations

- **Containerization**: Single Dockerfile, multi-stage build for small image
- **Lock file**: `uv.lock` committed to repo for reproducible builds
- **Media Storage**: Local filesystem with configurable paths (Docker volume friendly)
- **Logging**: Structured JSON logs for easy parsing (Loki/Grafana compatible)

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Problem-Solving MVP
- Solve the core aggregation problem with one killer transformation (subtitle → article)
- Deliver Marcus's complete journey and Sofia's consumption experience
- Prove the "subscription sovereignty" concept works

**Resource Requirements:** Solo developer with focused effort (creator dogfooding from Week 1)

**Internal Milestones:**
- **MVP Core** (Week 1): Dogfood-ready - subscribe, aggregate, transform, consume
- **MVP Polish** (v1.0): Release-ready - PWA complete, error UX polished, ready for r/selfhosted

### MVP Feature Set (Phase 1)

**Core User Journeys Supported:**
- Marcus (Power User): Full journey - subscribe, aggregate, transform, consume
- Marcus (Edge Case): Error visibility and recovery flows
- Sofia (Household): Plex/podcast consumption (managed by Marcus)

**Must-Have Capabilities:**

| Category | Features |
|----------|----------|
| **Subscriptions** | YouTube channels, RSS feeds, podcast feeds via OPML import |
| **Aggregation** | Chronological feed, no algorithmic filtering |
| **Transformation** | Subtitle → Article (text-to-text AI transposition) |
| **Serving** | Web UI, podcast RSS feeds, Plex/Jellyfin compatible |
| **Integration** | *arr stack API (read direction) |
| **Infrastructure** | Single Docker container, SQLite, YAML config |
| **Web App** | Responsive PWA, dark mode default, touch-friendly |
| **Error Handling** | Clear status indicators, retry mechanisms, feed health monitoring |

**Opportunistic MVP (Include if <2 days effort):**

| Feature | Criteria | Deferral Point |
|---------|----------|----------------|
| PWA Push Notifications | Natural fit during PWA setup | If >2 days effort → v1.0.1 |
| Swipe gestures | Falls into place with mobile CSS | If complex → v1.0.1 |

**Explicitly Out of MVP:**
- TTS (Article → Audio) - v1.1
- Whisper transcription - v1.2
- *arr write integration - v1.x
- MCP server - v1.x
- Jordan's full API (webhooks, batch operations) - v1.x

### Post-MVP Features

**Phase 2: v1.1 - Audio Output**
- Article → Audio (TTS with natural pacing)
- Voice customization options
- Audio player in web UI

**Phase 2: v1.2 - Audio Input**
- Audio → Text (Whisper transcription)
- Quality chain: Bazarr subs → Manual captions → Auto-captions → Transcribe
- Handles content without existing subtitles

*v1.1 and v1.2 are independent tracks - ship in either order based on demand.*

**Phase 3: v1.x - Platform Expansion**
- *arr stack integration (write direction) - appear AS a source
- Full transformation API for Jordan's use case
- Webhooks and batch operations
- MCP server for companion interface
- SSE for real-time updates

**Phase 4: v2+ - Vision Features**
- Companion features (conversational selection, Q&A)
- Cross-source synthesis and briefings
- Video transformations
- Live steering (adjust parameters mid-stream)
- Preference learning

### Risk Mitigation Strategy

| Risk Category | Risk | Mitigation |
|---------------|------|------------|
| **Technical** | AI transposition quality varies | Concrete quality bar (Flesch >60, no artifacts); manual review samples |
| **Technical** | YouTube API/scraping instability | Delegate to yt-dlp which handles this; graceful degradation |
| **Technical** | PWA complexity creep | Opportunistic scope - defer if >2 days |
| **Market** | *arr community doesn't adopt | Dogfood immediately; iterate based on real usage |
| **Market** | "Subscription sovereignty" doesn't resonate | Focus on concrete value (format flexibility) if philosophy doesn't land |
| **Resource** | Solo developer bandwidth | Lean MVP; opportunistic features; ship early, iterate |

### Scope Decision Log

| Decision | Rationale |
|----------|-----------|
| Subtitle → Article as MVP transformation | Lowest technical risk, highest "aha" potential |
| PWA notifications opportunistic | Build if easy, defer if rabbit hole |
| Internal milestone split (Core vs Polish) | Enables Week 1 dogfood without blocking on polish |
| Jordan's API deferred to v1.x | Marcus and Sofia don't need it; keep MVP lean |
| Deferred features = marketing moments | Re-announce on v1.1, v1.2 releases |

## Functional Requirements

### Subscription Management

- **FR1**: Users can add YouTube channel subscriptions by URL or channel ID
- **FR2**: Users can add RSS feed subscriptions by URL
- **FR3**: Users can add podcast feed subscriptions by URL
- **FR4**: Users can import multiple subscriptions via OPML file upload
- **FR5**: Users can view all active subscriptions with current status
- **FR6**: Users can edit subscription settings (name, tags, polling frequency)
- **FR7**: Users can delete subscriptions
- **FR8**: Users can organize subscriptions into user-defined categories/tags
- **FR9**: Users can export subscriptions as OPML file

### Content Aggregation

- **FR10**: System can fetch new content from YouTube channels automatically
- **FR11**: System can fetch new content from RSS feeds automatically
- **FR12**: System can fetch new content from podcast feeds automatically
- **FR13**: System can store content metadata (title, description, date, source, duration)
- **FR14**: Users can view aggregated content in chronological order (newest first)
- **FR15**: Users can filter content by subscription, category, or content type
- **FR16**: Users can search content by title or description
- **FR17**: Users can mark content as read/unread
- **FR18**: System can track content consumption state across sessions

### Content Transformation

- **FR19**: Users can request subtitle-to-article transformation for video content
- **FR20**: System can extract subtitles from YouTube videos (via available captions)
- **FR21**: System can transform subtitles into readable article format using AI transposition
- **FR22**: System can remove verbal artifacts (um, uh, repetition) from transformed content
- **FR23**: System can convert visual references to verbal descriptions in transformed content
- **FR24**: Users can view transformation status (queued, processing, complete, failed)
- **FR25**: Users can access completed transformations for consumption
- **FR26**: System can queue multiple transformation requests
- **FR27**: System can process transformations on-demand or via scheduled batch

### Content Serving - Web UI

- **FR28**: Users can access web interface for subscription and content management
- **FR29**: Users can read transformed articles in web interface
- **FR30**: Users can navigate content via responsive mobile-friendly interface
- **FR31**: Users can install web app to device home screen (PWA)
- **FR32**: Users can toggle between dark and light themes
- **FR33**: System can remember user's theme preference

### Content Serving - Podcast Feeds

- **FR34**: System can generate valid RSS 2.0 podcast feeds with iTunes extensions
- **FR35**: Users can access generated podcast feed URLs for use in podcatcher apps
- **FR36**: System can include episode metadata (title, description, duration, artwork) in feeds
- **FR37**: Podcatcher apps can fetch and play content from generated feeds

### Content Serving - Media Server Integration

- **FR38**: System can serve media files in Plex-compatible format
- **FR39**: System can serve media files in Jellyfin-compatible format
- **FR40**: Users can organize content into per-user libraries (e.g., "Sofia's Feeds")

### Integration - *arr Stack

- **FR41**: System can read from Sonarr API to understand existing media library
- **FR42**: System can read from Radarr API to understand existing media library
- **FR43**: External services can authenticate via API key
- **FR44**: External services can retrieve content metadata via API
- **FR45**: External services can retrieve subscription status via API

### System Health & Monitoring

- **FR46**: System can display feed health status (healthy, rate-limited, failing)
- **FR47**: System can display detailed error information for failed feed fetches
- **FR48**: Users can manually retry failed feed fetches
- **FR49**: System can automatically retry failed fetches with backoff
- **FR50**: System can display transformation queue status and progress
- **FR51**: System can display system health summary (uptime, queue depth, error rate)

### Configuration & Settings

- **FR52**: Users can generate API keys for external service access
- **FR53**: Users can revoke API keys
- **FR54**: Users can configure AI provider settings (local vs remote, model selection)
- **FR55**: Users can configure transformation quality preferences
- **FR56**: System can operate with AI features disabled (graceful degradation)
- **FR57**: Administrators can configure system via YAML configuration file
- **FR58**: System can auto-generate required keys (VAPID) on first run

### Notifications (Opportunistic)

- **FR59**: Users can opt-in to push notifications for transformation completion
- **FR60**: Users can opt-in to push notifications for feed health alerts
- **FR61**: System can deliver notifications via Web Push API

## Non-Functional Requirements

### Performance

- **NFR1**: System startup completes within 30 seconds from container start to serving content
- **NFR2**: MVP operates within 2GB RAM without GPU requirement
- **NFR3**: Web UI initial load completes within 3 seconds on broadband connection
- **NFR4**: Feed list and content views render within 1 second after initial load
- **NFR5**: Transformation queue accepts new requests within 500ms
- **NFR6**: API endpoints respond within 200ms for CRUD operations
- **NFR7**: Podcast feed generation completes within 2 seconds for feeds under 100 items

### Reliability

- **NFR8**: System recovers gracefully from network failures without data loss
- **NFR9**: Malformed feed input does not crash system or corrupt other data
- **NFR10**: AI provider unavailability does not prevent core functionality (graceful degradation)
- **NFR11**: System preserves subscription and content data across restarts
- **NFR12**: Failed transformations can be retried without manual intervention
- **NFR13**: Automatic retry with exponential backoff for transient failures
- **NFR14**: System logs errors in structured format for debugging

### Integration Compatibility

- **NFR15**: Generated podcast feeds pass standard RSS 2.0 validators
- **NFR16**: Generated podcast feeds include required iTunes podcast extensions
- **NFR17**: Sonarr API integration follows documented Sonarr API specification
- **NFR18**: Radarr API integration follows documented Radarr API specification
- **NFR19**: Plex media serving follows Plex media server compatibility requirements
- **NFR20**: Jellyfin media serving follows Jellyfin compatibility requirements
- **NFR21**: OPML import/export follows OPML 2.0 specification

### Security

- **NFR22**: API keys use cryptographically secure random generation
- **NFR23**: API keys are stored hashed, not in plaintext
- **NFR24**: All API endpoints require authentication (no anonymous access to data)
- **NFR25**: Configuration files with secrets are not logged or exposed via API
- **NFR26**: HTTPS supported for all web traffic (user-configurable)

### Usability & Accessibility

- **NFR27**: Web UI functions on mobile devices (320px minimum width)
- **NFR28**: Touch targets meet 44x44px minimum for mobile usability
- **NFR29**: UI provides sufficient color contrast for readability (WCAG AA for text)
- **NFR30**: Error messages are human-readable and actionable
- **NFR31**: System state is always visible (no silent failures or mystery states)

### Deployment & Operations

- **NFR32**: Single `docker-compose up` deploys fully functional system
- **NFR33**: Configuration via environment variables and/or YAML file
- **NFR34**: Logs output in structured JSON format for log aggregation
- **NFR35**: System operates correctly behind reverse proxy (configurable base URL)
- **NFR36**: Data directory is configurable for Docker volume mounting


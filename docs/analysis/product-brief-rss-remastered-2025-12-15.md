---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments:
  - docs/analysis/brainstorming-session-2025-12-13.md
  - docs/prd.md
workflowType: 'product-brief'
lastStep: 6
completedAt: '2025-12-15'
project_name: 'rss-remastered'
user_name: 'Mo'
date: '2025-12-15'
---

# Product Brief: rss-remastered

**Date:** 2025-12-15
**Author:** Mo

---

## Executive Summary

RSS-Remastered restores **subscription sovereignty** - enabling users to consume exactly what they subscribed to, when they want, in whatever format fits their life. Under the hood, it's an intelligent content transcoder with optional AI features. What it *means* is taking back control from algorithmic feeds that bury subscribed content and serve platform-chosen recommendations instead.

**The Problem:** Major platforms suppress content users explicitly subscribed to in favor of algorithmic recommendations. YouTube, social media feeds, and aggregators decide what users see and when - not the subscription choices users make. Power users running self-hosted media stacks (*arr ecosystem) have sovereignty over movies and TV, but not over their YouTube subscriptions, podcasts, and RSS feeds.

**The Solution:** Self-hosted content aggregation with intelligent on-demand transformation. RSS-Remastered aggregates subscriptions (YouTube, RSS, podcasts), serves them chronologically without algorithmic filtering, and transforms content between formats intelligently - not crude conversion, but content *refactored* to make sense in the target format.

**Target Audience:** Self-hosting power users already running *arr stack (Sonarr, Radarr, Prowlarr) who understand Docker, manage multiple services, and value owning their consumption pipeline. These users want to extend their self-hosted media sovereignty to all their subscriptions.

**Deployment:** Single Docker container, single compose entry, full capability from day one. The "monolith-first, modular-inside, decouple-later" architecture respects the cognitive load of the self-hosting crowd - no orchestration complexity required.

**Traction Goal:** Community adoption within *arr ecosystem - GitHub stars, forks, integration discussions - with creator dogfooding from Week 1 as validation.

---

## Core Vision

### Problem Statement

Algorithmic feeds have broken the subscription contract. Users subscribe to creators, channels, and sources they want to follow - but platforms decide what actually gets shown. Content gets buried, missed, or never surfaces despite explicit subscription choices. The algorithm optimizes for platform goals (engagement, ad revenue), not user intent.

For self-hosting power users who've achieved media sovereignty through *arr stack tools, this gap is particularly frustrating. They control their movie and TV libraries completely, but YouTube subscriptions, podcasts, and RSS feeds remain trapped in algorithmic walled gardens.

### Problem Impact

**For Individual Users:**
- Subscribed content never surfaces (YouTube's "Recommended" buries actual subscriptions)
- No control over consumption format (can't read a video essay, can't listen to an article)
- Algorithmic manipulation replaces user agency
- Fragmented consumption across multiple platforms and apps

**For Self-Hosting Community:**
- Philosophical gap in their self-hosted ecosystem (media controlled, subscriptions not)
- No "Sonarr for YouTube subscriptions" equivalent
- Forced reliance on platforms that don't respect user choices

### Why Existing Solutions Fall Short

**RSS Readers:** Aggregate feeds but don't handle YouTube subscriptions well, no format transformation, limited serving options

**YouTube Alternatives (NewPipe, Invidious):** Solve the YouTube-specific problem but don't unify across sources (podcasts, RSS, video)

**Media Servers (Plex, Jellyfin):** Serve media you already have, but don't aggregate or transform subscription content

**Feed Aggregators:** Focus on reading articles, miss the format fluidity (video → audio, article → audio) that modern consumption demands

**None provide:**
- Unified aggregation across YouTube, RSS, and podcasts
- Intelligent format transformation (content adapted, not crudely converted)
- Self-hosted deployment matching *arr stack patterns
- "Subscription sovereignty" as a core philosophy

### Proposed Solution

RSS-Remastered is a self-hosted content aggregation and transformation platform that restores subscription sovereignty:

**Core Capabilities:**
1. **Unified Aggregation:** Subscribe to YouTube channels, RSS feeds, and podcasts in one place
2. **Chronological Serving:** View all subscribed content in pure chronological order - no algorithm
3. **Intelligent Transformation:** On-demand content adaptation between formats
   - YouTube video → readable article (AI-enhanced: visual refs become verbal descriptions)
   - Article → natural audio narration (post-MVP)
   - Subtitle quality chain: manual captions → auto-captions → Whisper transcription
4. **Multi-Format Delivery:** Web UI, podcast feeds, Plex/Jellyfin integration - consume how you want
5. **Ecosystem Integration:** Reads from Sonarr/Radarr APIs, follows *arr patterns

**Technical Foundation:**
- Python 3.11+ backend (FastAPI, SQLAlchemy 2.0 async, SQLite)
- React 19 + TypeScript frontend (Vite, Tailwind, shadcn/ui)
- Single Docker container deployment
- AI-optional architecture (core works without AI, enhanced with AI)

**Deployment Philosophy:** Monolith-first, modular-inside, decouple-later - respects self-hoster cognitive load

### Key Differentiators

**1. Subscription Sovereignty as Philosophy**
Not just a feature set - a statement against algorithmic control. RSS-Remastered frames the problem politically: users deserve to receive what they subscribed to, without platform interference.

**2. On-Demand Transformation**
Unlike tools that pre-compute all transformations (wasteful, inflexible), RSS-Remastered transforms at consumption time:
- Efficiency: Subscribe to 100 channels, consume 20% = 80% compute saved
- Flexibility: Infinite format variations, real-time parameter adjustments
- Live steering: Adjust transformation mid-stream (future)

**3. Intelligent Transposition, Not Crude Conversion**
AI doesn't just convert formats - it *refactors content* to make sense in the target format:
- Visual references become verbal descriptions
- Timestamps removed, natural paragraph flow added
- Verbal artifacts cleaned (um, uh, repetition)
- Flesch reading ease >60 (quality bar)

**4. *arr Stack Native**
Designed for the self-hosting community from day one:
- Single container deployment (no orchestration complexity)
- API key auth matching *arr patterns
- Reads Sonarr/Radarr APIs
- Docker Compose native
- Philosophy aligns with *arr ecosystem values

**5. AI Sovereignty**
Users control their AI stack: local models, remote providers, or hybrid. Graceful degradation ensures core functionality without AI. No vendor lock-in, no forced cloud dependencies.

**6. Format Fluidity**
Switch from video at desk → audio in car, pick up where you left off. Session continuity across formats and devices. Content adapts to your life, not the other way around.

---

## Target Users

### Primary User: The *arr Stack Power User

**Profile:** Marcus Chen represents the core target - software engineers and technical enthusiasts already running self-hosted media stacks (Sonarr, Radarr, Prowlarr). These users:
- Understand Docker and container orchestration
- Manage multiple self-hosted services
- Value ownership and control over their media consumption
- Subscribe to 40+ YouTube channels, multiple podcasts, and RSS feeds
- Frustrated by algorithmic suppression of subscribed content

**Pain Point:** Has achieved media sovereignty for movies/TV through *arr stack, but YouTube subscriptions and podcasts remain in algorithmic walled gardens. YouTube's "Recommended" feed buries actual subscriptions.

**Success Criteria:**
- One-command deployment (`docker-compose up`)
- OPML import of existing subscriptions
- Chronological feed with zero algorithmic filtering
- Format transformation (video → article for commute reading)
- Integration with existing *arr APIs
- Complete control over consumption pipeline

**Value Realization:** Week 1 dogfooding - managing all subscriptions through RSS-Remastered, never opening YouTube app again

### Secondary User: The Household Consumer

**Profile:** Sofia Chen represents the non-technical household member who benefits from managed setup:
- Not technical (Docker is "Marcus's thing in the basement")
- Consumes via familiar interfaces (Plex, podcast apps)
- Wants content to "just work" without complexity
- Values ad-free, algorithm-free experience

**Use Case:** Content appears in Plex library or podcast app, managed by primary user. Complexity remains invisible - just better streaming without ads or algorithmic manipulation.

**Success Criteria:**
- Zero configuration required
- Content consumption identical to existing workflows
- Reliable, invisible operation

### Tertiary User: The Integration Builder

**Profile:** Jordan Park represents the developer/automator community (post-MVP focus):
- Runs personal automation stacks (n8n, Home Assistant)
- Looks for API-first tools to build upon
- Creates workflows, extensions, and integrations
- Shares automation patterns with community

**Use Case:** Build "morning briefing" automation - query RSS-Remastered API for overnight content, transform top items, queue for breakfast listening. Eventually becomes contributor to core project.

**Success Criteria (v1.x+):**
- Clean REST API with OpenAPI docs
- Webhook support for automation triggers
- Batch operation endpoints
- API-first design philosophy

---

## Success Metrics

### User Success Indicators

**Subscription Sovereignty Achieved:**
- 100% of subscribed content delivered without algorithmic filtering
- No content missed or buried by platform algorithms
- User controls what they see and when

**Format Fluidity Realized:**
- Users consume same content across 2+ formats without manual intervention
- Session continuity preserved across format switches and devices
- Seamless transition (video at desk → audio in car)

**Quality Bar for AI Transposition:**
- Proper paragraph structure (no wall of text)
- No timestamp artifacts or speaker label noise
- Flesch reading ease score > 60 (general audience readability)
- Passes "would I read this?" test

### Business Success Metrics

**Community Traction (6-month targets):**
- \>100 GitHub stars
- \>10 forks
- \>5 external issues or PRs from community members
- Recognition within *arr stack community (Reddit mentions, blog posts, integration requests)

**Dogfooding Validation:**
- Creator using RSS-Remastered as primary media consumption tool from Week 1
- Daily personal use validates product-market fit

**Contributor Growth:**
- External contributors submitting PRs
- Community extending functionality
- Integration ecosystem emerging (n8n workflows, Home Assistant, Raycast plugins)

### Technical Success Criteria

**Deployment Simplicity:**
- One-command deployment: Single `docker-compose up` to fully working system
- < 30 seconds from container start to serving content

**Resource Efficiency:**
- MVP runs on 2GB RAM, no GPU required
- Low resource floor enables broad adoption

**Integration Compatibility:**
- Valid Sonarr/Radarr API integration
- Compliant podcast RSS feeds (RSS 2.0 + iTunes extensions)
- Plex/Jellyfin compatible media serving

**Reliability:**
- Graceful degradation on network failures, malformed feeds, missing content
- No crashes or data corruption
- Clear error states and recovery paths

### North Star

> RSS-Remastered becomes the reference implementation for **subscription sovereignty** - other projects adopt the framing, the philosophy spreads beyond this single tool. Success isn't just adoption, it's starting a conversation about taking back control from algorithmic feeds.

---

## Product Scope

### MVP (v1.0) - Problem-Solving Core

**Strategy:** Solve the core aggregation problem with one killer transformation (subtitle → article). Deliver Marcus's complete journey and Sofia's consumption experience. Prove "subscription sovereignty" works.

**Must-Have Capabilities:**

| Category | Features |
|----------|----------|
| **Subscriptions** | YouTube channels, RSS feeds, podcast feeds; OPML import/export |
| **Aggregation** | Chronological feed, no algorithmic filtering; full-text search; read state tracking |
| **Transformation** | Subtitle → Article (AI-enhanced text-to-text transposition); queue management; on-demand processing |
| **Serving** | Responsive PWA web UI; podcast RSS feed generation; Plex/Jellyfin compatible serving |
| **Integration** | *arr stack API (read direction); API key authentication |
| **Infrastructure** | Single Docker container; SQLite database; YAML configuration |
| **Error Handling** | Clear status indicators; retry mechanisms; feed health monitoring |

**Explicitly Out of MVP:**
- TTS (Article → Audio) - deferred to v1.1
- Whisper transcription (Audio → Text) - deferred to v1.2
- *arr write integration - deferred to v1.x
- MCP server for companion features - deferred to v1.x
- Full transformation API with webhooks - deferred to v1.x

### Post-MVP Roadmap

**v1.1 - Audio Output:**
- Article → Audio (TTS with natural pacing)
- Voice customization options
- Audio player in web UI

**v1.2 - Audio Input:**
- Audio → Text (Whisper transcription)
- Quality chain: Bazarr subs → Manual captions → Auto-captions → Transcribe
- Handles content without existing subtitles

*Note: v1.1 and v1.2 are independent - ship in either order based on demand*

**v1.x - Platform Expansion:**
- *arr stack integration (write direction) - appear AS a source
- Full transformation API for Jordan's automation use case
- Webhooks and batch operations
- MCP server for companion interface
- SSE for real-time updates

**v2+ - Vision Features:**
- Companion features (conversational selection, Q&A, cross-source synthesis)
- Video transformations (full video processing)
- Live steering (adjust parameters mid-stream)
- Preference learning (multi-signal behavior analysis)

---

## Technology Foundation

### Architecture Approach

**Monolith-First Philosophy:** Start with single container deployment, modular internal structure, decouple later when scale demands it. Respects self-hoster cognitive load - no orchestration complexity required for MVP.

### Stack Selection

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Backend** | Python 3.11+ with FastAPI | Creator preference; strong media ecosystem (yt-dlp, FFmpeg); async-capable; auto-generated OpenAPI docs |
| **Frontend** | React 19 + TypeScript (strict) | Modern UI framework; strong typing; large ecosystem |
| **Build Tools** | Vite 6.x, Tailwind CSS 4.x, shadcn/ui | Fast builds; utility-first CSS; high-quality component library |
| **Database** | SQLite (MVP), PostgreSQL (future) | Sufficient for household use; migrate at ~10 concurrent writers |
| **Package Mgmt** | uv | Fast (Rust-based), modern, lock files; from Astral (ruff team) |
| **Deployment** | Docker (single container) | Self-hoster standard; simple orchestration |

### Integration Points

**Media Tools:**
- yt-dlp for YouTube extraction (handles rate limiting, scraping instability)
- FFmpeg for media processing

**External Services:**
- Sonarr/Radarr API (read direction)
- Plex/Jellyfin media serving
- Podcast RSS 2.0 + iTunes extensions

**AI Providers:**
- Local models (Ollama, llama.cpp)
- Remote providers (OpenAI, Anthropic, others)
- Hybrid approaches supported
- Graceful degradation without AI

---

## Risk Mitigation

| Risk Category | Risk | Mitigation Strategy |
|---------------|------|---------------------|
| **Technical** | AI transposition quality varies | Concrete quality bar (Flesch >60, no artifacts); manual review samples; iterate based on real usage |
| **Technical** | YouTube API/scraping instability | Delegate to yt-dlp (built-in handling); graceful degradation with clear error states |
| **Technical** | PWA complexity creep | Opportunistic scope - defer if >2 days effort; ship basic first |
| **Market** | *arr community doesn't adopt | Dogfood immediately (Week 1); iterate based on creator's real usage; validate product-market fit before broad release |
| **Market** | "Subscription sovereignty" doesn't resonate | Focus on concrete value (format flexibility, chronological feed) if philosophy doesn't land; let results speak |
| **Resource** | Solo developer bandwidth | Lean MVP scope; opportunistic features only; ship early and iterate; community contributions post-launch |
| **Integration** | Agent protocol ecosystem fragmentation | MCP-first with abstraction layer; deferred to v1.x; standalone functionality doesn't depend on protocols |

---

## Strategic Positioning

### Market Opportunity

**Gap in Self-Hosting Ecosystem:** The *arr stack has achieved media sovereignty for movies and TV, but no equivalent exists for subscription content (YouTube, podcasts, RSS). RSS-Remastered fills this philosophical and practical gap.

**Emerging Trend - Algorithm Fatigue:** Growing user frustration with algorithmic feeds burying subscribed content. Power users seeking alternatives. Self-hosting movement gaining momentum.

**Format Fluidity Demand:** Modern consumption patterns require flexibility - read during lunch, listen during commute, watch at desk. Existing tools lock users into single formats.

### Competitive Advantages

1. **Philosophy-First:** "Subscription sovereignty" isn't just marketing - it's the core principle that drives every design decision
2. ***arr Native:** Built for the self-hosting community with their patterns, not adapted from SaaS
3. **On-Demand Architecture:** Transforms at consumption time, enabling flexibility impossible with pre-computed approaches
4. **AI Optional:** Core functionality works without AI; AI enhances but doesn't gate features
5. **Single Container:** Respects cognitive load - no Kubernetes, no microservices complexity for MVP

### Go-to-Market

**Launch Strategy:**
- r/selfhosted post with clear value proposition
- *arr community forums and Discord channels
- GitHub as primary distribution (Docker Hub for images)
- Dogfooding from Week 1 validates real-world usage

**Community Building:**
- Open source from day one (license TBD)
- Clear contribution guidelines
- API-first design enables ecosystem
- Integration builders (Jordan's segment) become advocates

**Success Indicators:**
- Community contributions emerge organically
- Integration patterns shared (n8n workflows, Home Assistant configs)
- "How I set up RSS-Remastered" blog posts appear
- Feature requests align with core vision

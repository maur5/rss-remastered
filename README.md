# RSS-Remastered

**Restore subscription sovereignty.** Take back control from algorithmic feeds and consume what you subscribed to, when you want, in the format that fits your life.

## What Is This?

RSS-Remastered is a self-hosted content aggregation and transformation platform. Under the hood, it's a smart transcoder with optional AI features. What it *means* is:

- YouTube videos become podcasts that make sense without visuals
- Articles become narrated conversations with proper pacing
- Your morning commute becomes an audio digest of exactly what you subscribed to
- Switch from video at your desk to audio in your car, pick up exactly where you left off

**Nothing buried. Nothing missed. Content intelligently adapted, not crudely converted.**

## Status

🚧 **Early Development** - Currently in implementation phase (Phase 3)

- ✅ Planning complete (PRD, UX Design)
- ✅ Architecture designed
- ✅ Test framework designed
- 🚧 Active development of backend and frontend

## Quick Start

_Coming soon - Docker Compose deployment with single-command setup_

## Architecture

**Monolith-first, modular-inside, decouple-later approach**

- **Backend:** Python 3.11+ with FastAPI, SQLAlchemy 2.0 (async), SQLite
- **Frontend:** React 19.x + TypeScript (strict), Vite 6.x, Tailwind CSS 4.x, shadcn/ui
- **Deployment:** Single Docker container for MVP

See [docs/architecture.md](docs/architecture.md) for detailed architecture decisions.

## Key Features (v1)

### Subscription Management
- YouTube channels, RSS feeds, and podcast subscriptions
- OPML import/export for easy migration
- Tag-based organization

### Content Aggregation
- Automatic content fetching and metadata storage
- Unified chronological feed across all sources
- Full-text search and read state tracking

### Intelligent Transformation
- **YouTube → Audio:** Visual references automatically described verbally (AI-enhanced)
- **Article → Audio:** Natural TTS narration with proper pacing
- On-demand transformation (no wasted compute on unwatched content)
- Queue management with progress tracking

### Delivery Options
- Responsive PWA web interface
- Podcast feed generation (RSS 2.0 + iTunes extensions)
- Plex/Jellyfin integration for media server users

### *arr Stack Integration
- Read Sonarr/Radarr subscriptions
- API key authentication

## Documentation

Project documentation lives in the [docs/](docs/) directory:

- [PRD](docs/prd.md) - Complete product requirements
- [Architecture](docs/architecture.md) - Architecture decisions and patterns
- [UX Design](docs/ux-design-specification.md) - User experience specification
- [Project Context](docs/project_context.md) - Critical rules for AI-assisted development
- [Test Design](docs/test-design-system.md) - Testing strategy and approach

See [docs/README.md](docs/README.md) for complete documentation navigation.

## Target Audience

**Primary:** Power users already running *arr stack (Sonarr, Radarr, Prowlarr) who want to extend their self-hosted media ecosystem.

These users:
- Understand Docker and container orchestration
- Manage multiple self-hosted services
- Value owning their consumption pipeline
- Prefer single-container deployments

**Welcome but not primary:** Newcomers to self-hosting (v1 focuses on *arr stack users)

## Development Setup

### Prerequisites

- **Backend:** Python 3.11+, uv package manager
- **Frontend:** Node.js (see `.nvmrc`), npm
- **Infrastructure:** Docker, Docker Compose
- **Media Tools:** yt-dlp, FFmpeg

### Backend Setup

```bash
cd backend
uv sync                    # Install dependencies
uv run alembic upgrade head # Run migrations
uv run uvicorn app.main:app --reload # Start dev server
```

### Frontend Setup

```bash
cd frontend
npm install                # Install dependencies
npm run dev                # Start dev server
```

### Testing

```bash
# E2E tests (Playwright)
npm run test:e2e
npm run test:e2e:ui        # Interactive UI mode

# Backend tests
cd backend
uv run pytest
```

See [docs/test-design-system.md](docs/test-design-system.md) for complete testing approach.

## Project Structure

```
rss-remastered/
├── backend/               # Python FastAPI backend
│   ├── src/              # Source code
│   ├── tests/            # Backend tests
│   └── alembic/          # Database migrations
├── frontend/             # React TypeScript frontend
│   ├── src/              # Source code
│   └── public/           # Static assets
├── docs/                 # Project documentation
├── tests/                # E2E tests (Playwright)
├── scripts/              # Development and deployment scripts
└── .devcontainer/        # VS Code Dev Container configuration
```

## Contributing

This project uses the [BMAD Method](https://github.com/your-bmad-link) for development workflow:

1. Requirements captured in PRD
2. Architecture decisions documented
3. Epics and stories drive implementation
4. Test-first approach with comprehensive coverage

See [docs/implementation-readiness-report-2025-12-14.md](docs/implementation-readiness-report-2025-12-14.md) for current project status.

## License

_License TBD_

## Why Build This?

Algorithmic feeds bury what you asked for and serve what *they* want you to see. RSS-Remastered returns control to you:

- You declare what you want to subscribe to
- Content is consumed when published, not when an algorithm decides
- Format adapts to your life (commute = audio, desk = video)
- Your data stays on your hardware

**Subscription sovereignty, restored.**

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [shadcn/ui](https://ui.shadcn.com/) - Component library
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube extraction
- [BMAD](https://github.com/your-bmad-link) - Development methodology

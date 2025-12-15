# Documentation Hub

Welcome to the RSS-Remastered documentation. This guide helps you navigate all project documentation organized by purpose and phase.

## Quick Navigation

| What You Need | Where to Go |
|---------------|-------------|
| **Understand the product vision** | [Product Requirements (PRD)](#product-requirements) |
| **Understand the system design** | [Architecture](#architecture-and-design) |
| **Implement features** | [Project Context](#developer-guides) → [Epics & Stories](#implementation) |
| **Write tests** | [Test Design](#testing-documentation) |
| **Setup environment** | [Environment Setup](#environment-and-configuration) |
| **Track sprint progress** | [Sprint Artifacts](#implementation) |

## Core Documentation

### Product Requirements

The source of truth for what we're building and why.

- **[prd.md](prd.md)** - Complete Product Requirements Document
  - Executive summary and vision
  - User stories and use cases
  - 58 functional requirements across 9 categories
  - 36 non-functional requirements
  - Success metrics and release criteria

**Start here** to understand the product vision and requirements.

### Architecture and Design

Technical decisions, patterns, and system design.

- **[architecture.md](architecture.md)** - Architecture Decision Document
  - Technology stack decisions (FastAPI, React, SQLite)
  - System architecture patterns (monolith-first approach)
  - Data models and relationships
  - Integration patterns (*arr stack, media servers)
  - Deployment architecture (single container)
  - Security and performance considerations

- **[ux-design-specification.md](ux-design-specification.md)** - User Experience Specification
  - Visual design system (Tailwind CSS 4.x + shadcn/ui)
  - Responsive layout patterns
  - User flows and wireframes
  - Interaction patterns
  - Accessibility requirements

**Read these** to understand how the system is designed.

### Developer Guides

Critical information for implementing features correctly.

- **[project_context.md](project_context.md)** - Project Context for AI Agents
  - Technology stack versions
  - Language and framework rules
  - Testing requirements
  - Code quality standards
  - Critical implementation rules (45 rules total)

**Reference this constantly** during implementation to avoid common mistakes.

## Testing Documentation

Comprehensive testing strategy and tools.

- **[test-design-system.md](test-design-system.md)** - Test Design System
  - Testing philosophy and strategy
  - Test pyramid approach
  - Framework choices (Pytest, Vitest, Playwright)
  - Coverage requirements
  - CI/CD integration

- **[test-design-report.md](test-design-report.md)** - Test Design Report
  - Detailed test scenarios
  - Risk assessment
  - Test environment configuration
  - Readiness validation

- **[test-environment-readiness.md](test-environment-readiness.md)** - Test Environment Readiness Report
  - Environment validation results
  - Tool configuration verification
  - Infrastructure readiness

**Follow these** to ensure comprehensive test coverage.

## Implementation

Sprint artifacts and development progress.

### Sprint Artifacts

Active development stories with implementation details:

- **[sprint-artifacts/1-1-initialize-backend-project-structure.md](sprint-artifacts/1-1-initialize-backend-project-structure.md)** - Backend scaffolding ✅
- **[sprint-artifacts/1-2-initialize-frontend-project-structure.md](sprint-artifacts/1-2-initialize-frontend-project-structure.md)** - Frontend scaffolding ✅
- **[sprint-artifacts/1-5-configure-pydantic-settings.md](sprint-artifacts/1-5-configure-pydantic-settings.md)** - Pydantic settings configuration ✅

### Epics and Stories

- **[epics.md](epics.md)** - Complete epic and story breakdown
  - Epic 1: Core Infrastructure Setup (MVP Foundation)
  - Epic 2: Subscription Management
  - Epic 3: Content Aggregation Engine
  - Epic 4-9: Additional epics with user stories

**Check sprint-artifacts/** for active development tasks and implementation notes.

## Project Management

Planning and readiness validation.

- **[implementation-readiness-report-2025-12-14.md](implementation-readiness-report-2025-12-14.md)** - Implementation Readiness Report
  - Requirements → Architecture → Stories validation
  - Gap analysis and risk assessment
  - Readiness score: 92/100 (READY TO IMPLEMENT)
  - Recommendations for implementation

- **[bmm-workflow-status.yaml](bmm-workflow-status.yaml)** - BMAD Method workflow status
  - Current phase: Implementation (Phase 3)
  - Completed workflows: PRD, UX Design, Architecture, Test Design
  - Next steps: Sprint planning

**Review these** to understand project status and readiness.

## Environment and Configuration

Setup guides and configuration references.

- **[devcontainer-setup.md](devcontainer-setup.md)** - Dev Container setup guide
- **[devcontainer-persistence-guide.md](devcontainer-persistence-guide.md)** - Persistent storage patterns
- **[environment-setup-complete.md](environment-setup-complete.md)** - Environment validation
- **[vscode-configuration-review.md](vscode-configuration-review.md)** - VS Code settings
- **[playwright-extension-guide.md](playwright-extension-guide.md)** - Playwright test tooling

**Reference these** for development environment setup.

## Development Tools

Guides for development workflow tools.

- **[claude-hooks-reference.md](claude-hooks-reference.md)** - Claude Code hooks configuration
- **[bmad-subagent-quickstart.md](bmad-subagent-quickstart.md)** - BMAD subagent quick reference
- **[bmad-subagent-orchestration.md](bmad-subagent-orchestration.md)** - Advanced BMAD orchestration patterns

**Use these** to work effectively with AI-assisted development tools.

## Analysis and Research

Background research and brainstorming sessions.

- **[analysis/brainstorming-session-2025-12-13.md](analysis/brainstorming-session-2025-12-13.md)** - Initial brainstorming session
  - Product vision exploration
  - Feature ideation
  - Technical approach discussions

**Review these** for context on product decisions.

## Documentation Standards

All documentation in this project follows:

- **CommonMark specification** (strict compliance)
- **Task-oriented structure** (what you can accomplish)
- **Active voice, present tense**
- **Mermaid diagrams** for visual explanations
- **No time estimates** (focus on steps, not duration)

See [BMAD documentation standards](../.bmad/bmm/data/documentation-standards.md) for complete guidelines.

## How to Use This Documentation

### I'm new to the project
1. Read [prd.md](prd.md) - Understand what we're building
2. Read [architecture.md](architecture.md) - Understand how it's designed
3. Review [project_context.md](project_context.md) - Learn critical implementation rules
4. Check [implementation-readiness-report-2025-12-14.md](implementation-readiness-report-2025-12-14.md) - See current status

### I'm implementing a feature
1. Find your story in [epics.md](epics.md) or [sprint-artifacts/](sprint-artifacts/)
2. Reference [project_context.md](project_context.md) for implementation rules
3. Check [architecture.md](architecture.md) for relevant patterns
4. Review [test-design-system.md](test-design-system.md) for testing approach

### I'm debugging an issue
1. Check [environment-setup-complete.md](environment-setup-complete.md) for environment validation
2. Review [test-environment-readiness.md](test-environment-readiness.md) for test tool status
3. Reference [architecture.md](architecture.md) for system design context

### I'm writing tests
1. Read [test-design-system.md](test-design-system.md) for strategy
2. Check [test-design-report.md](test-design-report.md) for scenarios
3. Reference [project_context.md](project_context.md) for testing rules (Rule 15-23)

## Contributing to Documentation

When adding or updating documentation:

1. **Follow CommonMark strictly** - Use ATX-style headers, fenced code blocks, consistent list markers
2. **No time estimates** - Focus on steps and dependencies, not duration
3. **Task-oriented writing** - Answer "how do I..." questions
4. **Include examples** - Show concrete usage where helpful
5. **Link between docs** - Use relative paths like `[architecture](architecture.md)`
6. **Update this README** - Add new docs to the appropriate section

## Questions?

- Check the relevant section above
- Search within specific docs (all are CommonMark-formatted)
- Review [prd.md](prd.md) for requirements context
- Check [architecture.md](architecture.md) for design decisions
- Consult [project_context.md](project_context.md) for implementation rules

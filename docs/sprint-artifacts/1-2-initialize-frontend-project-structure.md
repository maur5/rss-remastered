# Story 1.2: Initialize Frontend Project Structure

**Epic:** 1 - Project Foundation & Core Infrastructure
**Status:** Complete
**Story ID:** 1.2

---

## Story

**As a** developer,
**I want** a Vite + React + TypeScript frontend with shadcn/ui configured,
**So that** I have a consistent foundation for implementing all frontend features.

---

## Acceptance Criteria

### AC1: Project Dependencies Installed

**Given** a fresh clone of the repository
**When** I run `cd frontend && npm install`
**Then** all dependencies are installed from package.json
**And** the project structure matches the Architecture specification

### AC2: Technology Stack Configured

**Given** the frontend is installed
**Then** the project includes:
- React 19.x with TypeScript strict mode
- Vite 6.x as build tool with @tailwindcss/vite plugin
- Tailwind CSS 4.x with CSS-first configuration (no tailwind.config.js)
- shadcn/ui initialized with components.json configured
- TanStack Query v5 for server state management
- Zustand for client state management

### AC3: Project Structure Created

**Given** the frontend is installed
**Then** the project structure includes:
- `frontend/src/components/ui/` for shadcn/ui base components (button added as verification)
- `frontend/src/components/app/` empty directory for app-level components
- `frontend/src/features/` empty directory for feature modules
- `frontend/src/stores/ui.ts` Zustand store skeleton for UI state
- `frontend/src/lib/api.ts` API client foundation
- `frontend/src/lib/query.ts` TanStack Query configuration
- `frontend/src/lib/utils.ts` shadcn/ui cn() utility
- `frontend/src/App.tsx` main application component
- `frontend/src/main.tsx` application entry point
- `frontend/src/index.css` Tailwind CSS imports

### AC4: Development Server Working

**Given** the frontend is installed
**When** I run `npm run dev`
**Then** the Vite dev server starts on port 5173
**And** the app displays a placeholder heading confirming setup
**And** dark theme is applied by default
**And** hot module replacement (HMR) works correctly

### AC5: Path Aliases Configured

**Given** the frontend is installed
**When** I create an import using `@/` prefix
**Then** the import resolves correctly to `src/` directory
**And** TypeScript recognizes the alias without errors

---

## Tasks / Subtasks

**Task 1: Initialize Vite + React + TypeScript project** (AC: #1, #2)
- [x] Create frontend directory
- [x] Run `npm create vite@latest . -- --template react-ts`
- [x] Verify package.json has React 19.x and TypeScript
- [x] Configure TypeScript strict mode in tsconfig.json
- [x] Run `npm install` to verify dependencies

**Task 2: Configure Tailwind CSS 4.x** (AC: #2)
- [x] Install Tailwind CSS 4: `npm install tailwindcss @tailwindcss/vite`
- [x] Add @tailwindcss/vite plugin to vite.config.ts
- [x] Create/update src/index.css with `@import "tailwindcss";`
- [x] Configure dark theme as default via CSS
- [x] Verify Tailwind classes work in App.tsx

**Task 3: Configure path aliases** (AC: #5)
- [x] Update vite.config.ts with resolve.alias for "@" → "./src"
- [x] Install @types/node for path module
- [x] Update tsconfig.json with paths configuration
- [x] Verify imports using @/ prefix work

**Task 4: Initialize shadcn/ui** (AC: #2, #3)
- [x] Run `npx shadcn@latest init`
- [x] Select New York style, Zinc base color, CSS variables
- [x] Verify components.json created correctly
- [x] Add Button component: `npx shadcn@latest add button`
- [x] Verify component installed in src/components/ui/

**Task 5: Install and configure TanStack Query** (AC: #2)
- [x] Install TanStack Query: `npm install @tanstack/react-query`
- [x] Create src/lib/query.ts with QueryClient configuration
- [x] Wrap App in QueryClientProvider in main.tsx
- [x] Configure default options (staleTime, retry, etc.)

**Task 6: Install and configure Zustand** (AC: #2, #3)
- [x] Install Zustand: `npm install zustand`
- [x] Create src/stores/ui.ts with UI state store skeleton
- [x] Include sidebar collapse state and theme preference
- [x] Configure localStorage persistence middleware

**Task 7: Create project structure and utility files** (AC: #3)
- [x] Create src/components/app/ directory
- [x] Create src/features/ directory
- [x] Create src/lib/api.ts with API client foundation
- [x] Create src/lib/utils.ts with cn() utility (shadcn creates this)
- [x] Verify all directories exist with proper structure

**Task 8: Create application entry point** (AC: #3, #4)
- [x] Update src/main.tsx with providers (QueryClient)
- [x] Update src/App.tsx with placeholder content
- [x] Apply dark theme class to root element
- [x] Import and display shadcn Button to verify setup

**Task 9: Verify dev server and HMR** (AC: #4)
- [x] Run `npm run dev`
- [x] Verify server starts on port 5173
- [x] Verify app loads with dark theme
- [x] Test hot reload by modifying App.tsx
- [x] Verify changes reflect without manual refresh

---

## Dev Notes

### Critical Architecture Patterns

**From [project_context.md](../project_context.md#L85-L125):**

TypeScript/React strict mode requirements:
- NO `any` types - use `unknown` and narrow
- NO implicit returns in functions
- ALL function parameters must be typed
- Use discriminated unions for state

TanStack Query patterns:
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

Zustand patterns:
- UI-only state (sidebar, theme, panels)
- Persist to localStorage via middleware
- Keep stores minimal - server state in TanStack Query

Import aliases:
```typescript
// Use path aliases
import { Button } from '@/components/ui/button'
import { useSubscriptions } from '@/features/subscriptions/hooks'

// NOT relative imports across features
import { Button } from '../../../components/ui/button'
```

### Technology Stack Requirements

**From [project_context.md](../project_context.md#L33-L42):**

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.x | UI framework |
| TypeScript | strict mode | Type safety |
| Vite | 6.x | Build tool |
| Tailwind CSS | 4.x | Styling |
| shadcn/ui | latest | Component library |
| TanStack Query | latest (v5) | Server state |
| Zustand | latest | Client state |

### API Contract Rules

**From [project_context.md](../project_context.md#L128-L141):**

**JSON Field Naming:**
- **ALL JSON fields use `snake_case`** - backend AND frontend
- Frontend converts at API boundary if needed
- Database columns match JSON field names

```json
// CORRECT
{ "subscription_id": 1, "feed_url": "...", "created_at": "..." }

// WRONG
{ "subscriptionId": 1, "feedUrl": "...", "createdAt": "..." }
```

### Frontend Feature Module Structure

**From [project_context.md](../project_context.md#L237-L244):**

Each feature (`features/subscriptions/`, etc.) will contain:
```
feature/
├── FeatureComponent.tsx
├── hooks.ts       # useQuery/useMutation hooks
└── api.ts         # API client functions
```

### File Naming Conventions

**From [project_context.md](../project_context.md#L246-L252):**

| Type | Convention | Example |
|------|------------|---------|
| React components | PascalCase | `SubscriptionCard.tsx` |
| Hooks | camelCase | `useSubscriptions.ts` |
| Stores | camelCase | `ui.ts` |
| Utilities | camelCase | `utils.ts` |

---

## Technical Requirements

### React 19.x Features Available

**From web research (react.dev):**

React 19 key features to leverage:
- Server Components support (use `'use client'` directive when needed)
- `use` API for reading promises and context conditionally
- New hooks: `useActionState`, `useFormStatus`, `useOptimistic`
- Document metadata support (`<title>`, `<meta>` in components)
- Concurrent rendering enabled by default

**Note:** For this MVP, focus on client-side React patterns. Server Components are available but not required for initial setup.

### Vite 6.x Configuration

**From web research (vite.dev):**

Vite 6 with React + TypeScript:
```bash
npm create vite@latest frontend -- --template react-ts
```

Key configuration for vite.config.ts:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### Tailwind CSS 4.x Configuration

**From web research (tailwindcss.com):**

**CRITICAL:** Tailwind CSS 4 uses CSS-first configuration - NO tailwind.config.js needed!

Installation:
```bash
npm install tailwindcss @tailwindcss/vite
```

CSS file (src/index.css):
```css
@import "tailwindcss";

@theme {
  /* Custom theme variables go here */
  --color-primary: oklch(0.7 0.15 180);
}
```

**Browser Compatibility:** Tailwind CSS v4.0 requires Safari 16.4+, Chrome 111+, Firefox 128+.

### shadcn/ui Setup

**From web research (ui.shadcn.com):**

After Vite + Tailwind setup:
```bash
npx shadcn@latest init
```

Configuration prompts:
- Style: New York
- Base color: Zinc (matches dark-first design)
- CSS variables: Yes

This creates:
- `components.json` - shadcn/ui configuration
- `src/lib/utils.ts` - cn() utility function
- `src/components/ui/` - component directory

Add initial component to verify:
```bash
npx shadcn@latest add button
```

**React 19 Note:** When using React 19, some packages may require `--force` flag due to peer dependency resolution.

### TanStack Query v5 Setup

**From web research (tanstack.com):**

Installation:
```bash
npm install @tanstack/react-query
```

Query client configuration (src/lib/query.ts):
```typescript
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})
```

Provider setup (main.tsx):
```typescript
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from '@/lib/query'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <QueryClientProvider client={queryClient}>
    <App />
  </QueryClientProvider>
)
```

**v5 Changes:**
- `isLoading` renamed to `isPending`
- `cacheTime` renamed to `gcTime`
- Dedicated suspense hooks: `useSuspenseQuery`

### Zustand Setup

**From web research (zustand.docs.pmnd.rs):**

Installation:
```bash
npm install zustand
```

UI store skeleton (src/stores/ui.ts):
```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface UIState {
  sidebarCollapsed: boolean
  contextPanelOpen: boolean
  theme: 'dark' | 'light' | 'system'
  toggleSidebar: () => void
  toggleContextPanel: () => void
  setTheme: (theme: 'dark' | 'light' | 'system') => void
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      contextPanelOpen: true,
      theme: 'dark',
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      toggleContextPanel: () => set((state) => ({ contextPanelOpen: !state.contextPanelOpen })),
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'rss-ui-storage',
    }
  )
)
```

**Key Pattern:** Zustand for UI state only. Server state (subscriptions, content, etc.) goes through TanStack Query.

---

## UX Design Integration

### Design System Foundation

**From [ux-design-specification.md](../ux-design-specification.md):**

Visual foundation:
- Dark theme as default (user preference: dark-first)
- Teal accent color for primary actions
- shadcn/ui + Tailwind CSS for consistent components
- System preference detection for theme

Three-panel layout (future stories):
- Left sidebar: 240px expanded, 64px collapsed
- Main content: flexible width
- Right context panel: 340px, dismissable

### Accessibility Requirements

**From [ux-design-specification.md](../ux-design-specification.md):**

WCAG 2.1 AA compliance target:
- Minimum touch targets: 44x44px mobile, 36x36px desktop
- Keyboard navigation with visible focus indicators
- Screen reader support with ARIA labels
- prefers-reduced-motion support

---

## Project Structure Reference

### Complete Frontend Structure (Target)

**From [architecture.md](../architecture.md):**

```
frontend/
├── package.json               # Project config (THIS STORY)
├── package-lock.json          # Lock file (THIS STORY)
├── vite.config.ts             # Vite configuration (THIS STORY)
├── tsconfig.json              # TypeScript config (THIS STORY)
├── tsconfig.node.json         # Node TypeScript config (THIS STORY)
├── components.json            # shadcn/ui config (THIS STORY)
├── index.html                 # HTML entry point (THIS STORY)
├── src/
│   ├── main.tsx               # React entry point (THIS STORY)
│   ├── App.tsx                # Main app component (THIS STORY)
│   ├── index.css              # Global styles + Tailwind (THIS STORY)
│   ├── components/
│   │   ├── ui/                # shadcn/ui components (THIS STORY - button)
│   │   │   └── button.tsx     # Verification component
│   │   └── app/               # App components (THIS STORY - empty)
│   ├── features/              # Feature modules (THIS STORY - empty)
│   ├── stores/
│   │   └── ui.ts              # UI state store (THIS STORY)
│   └── lib/
│       ├── api.ts             # API client (THIS STORY - skeleton)
│       ├── query.ts           # TanStack Query config (THIS STORY)
│       └── utils.ts           # Utilities (THIS STORY - shadcn creates)
└── tests/                     # Test directory (future stories)
```

---

## Testing Requirements

### Manual Testing Checklist

For this story, manual testing is sufficient:

1. **Project initialization:**
   - [ ] `cd frontend && npm install` completes without errors
   - [ ] All dependencies installed
   - [ ] package-lock.json created

2. **TypeScript configuration:**
   - [ ] `npm run build` completes without type errors
   - [ ] Strict mode enabled (no implicit any)
   - [ ] Path aliases resolve correctly

3. **Tailwind CSS 4:**
   - [ ] Tailwind classes apply correctly (test with `bg-zinc-900`)
   - [ ] Dark theme applied by default
   - [ ] No tailwind.config.js file (CSS-first approach)

4. **shadcn/ui:**
   - [ ] components.json exists with correct configuration
   - [ ] Button component renders correctly
   - [ ] Component uses Tailwind classes

5. **TanStack Query:**
   - [ ] QueryClientProvider wraps app
   - [ ] No console errors about missing provider

6. **Zustand:**
   - [ ] UI store created
   - [ ] State persists to localStorage

7. **Development server:**
   - [ ] `npm run dev` starts on port 5173
   - [ ] App loads in browser
   - [ ] Dark theme visible
   - [ ] HMR works (modify text, see instant update)

8. **Path aliases:**
   - [ ] Import using `@/components/ui/button` works
   - [ ] TypeScript shows no import errors

---

## Library & Framework Requirements

### Package.json Dependencies

**Required dependencies:**
```json
{
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@tanstack/react-query": "^5.0.0",
    "zustand": "^5.0.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "lucide-react": "^0.400.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@types/node": "^20.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "~5.6.0",
    "vite": "^6.0.0",
    "tailwindcss": "^4.0.0",
    "@tailwindcss/vite": "^4.0.0"
  }
}
```

**Note:** Exact versions will be determined at install time. Use latest stable versions.

---

## Previous Story Intelligence

### Story 1.1 Patterns to Follow

**From [1-1-initialize-backend-project-structure.md](./1-1-initialize-backend-project-structure.md):**

1. **Story structure:** Follow same comprehensive format with AC mapping
2. **Stub file pattern:** Create skeleton files with clear "implemented in Story X" comments
3. **Health check pattern:** Frontend should eventually call backend `/api/health`
4. **Development server:** Backend runs on 8000, frontend on 5173 (CORS configured)
5. **Code review:** Expect similar review process with issues to fix

### Integration with Backend

**From Story 1.1:**
- Backend CORS configured for `localhost:5173`
- API base URL will be `http://localhost:8000/api`
- Health endpoint available at `/api/health` for testing

---

## Git Intelligence Summary

### Branch Strategy

**Required branch:** `story/1-2-init-frontend`

**Commands:**
```bash
git checkout -b story/1-2-init-frontend dev
# ... implement story ...
git checkout dev && git merge --no-ff story/1-2-init-frontend
```

### Commit Checkpoints

1. **After project initialization:** `[story] 1-2: Initialize Vite + React + TypeScript project`
2. **After Tailwind + shadcn:** `[story] 1-2: Configure Tailwind CSS 4 and shadcn/ui`
3. **After TanStack + Zustand:** `[story] 1-2: Add TanStack Query and Zustand`
4. **After verification:** `[story] 1-2: Complete - frontend project structure initialized`

---

## Latest Technical Information Summary

### React 19 (December 2024 - Current)
- Server Components available (use `'use client'` for client components)
- New `use` API for promises and context
- New hooks: `useActionState`, `useFormStatus`, `useOptimistic`
- Concurrent rendering by default
- Document metadata support in components

### Vite 6 (Current)
- Native ES modules for fast dev server
- React + TypeScript template: `react-ts`
- First-party Tailwind plugin: `@tailwindcss/vite`
- Automatic content detection
- SWC for fast compilation

### Tailwind CSS 4 (January 2025 - Current)
- **CSS-first configuration** - NO tailwind.config.js needed
- Use `@import "tailwindcss";` in CSS
- Configure theme via `@theme` directive in CSS
- Up to 5x faster full builds, 100x faster incremental
- First-party Vite plugin for tight integration
- Automatic source detection

### shadcn/ui (Current)
- Works with Tailwind CSS 4
- `npx shadcn@latest init` for setup
- Components installed to src/components/ui/
- Uses CSS variables for theming
- May need `--force` flag with React 19

### TanStack Query v5 (Current)
- Requires React 18+ (works with React 19)
- `isPending` replaces `isLoading`
- `gcTime` replaces `cacheTime`
- Dedicated suspense hooks available
- ~20% smaller than v4

### Zustand (Current)
- No provider needed (just import and use)
- Persist middleware for localStorage
- Works seamlessly with TanStack Query
- Use for UI-only state

---

## Story Completion Checklist

**Story Definition:**
- [x] User story clearly stated
- [x] Acceptance criteria defined with Given/When/Then
- [x] Tasks broken down with AC mapping

**Technical Context:**
- [x] Architecture patterns documented
- [x] Technology stack with versions specified
- [x] Naming conventions established
- [x] API contract rules defined

**Implementation Guidance:**
- [x] File structure requirements documented
- [x] Code organization patterns specified
- [x] Development workflow documented
- [x] Latest technical research included

**Quality Context:**
- [x] Manual testing checklist
- [x] Integration points identified
- [x] Previous story patterns referenced

---

## Developer Quick Start

1. **Create branch:**
   ```bash
   git checkout -b story/1-2-init-frontend dev
   ```

2. **Initialize project:**
   ```bash
   mkdir frontend && cd frontend
   npm create vite@latest . -- --template react-ts
   npm install
   ```

3. **Add Tailwind CSS 4:**
   ```bash
   npm install tailwindcss @tailwindcss/vite
   ```
   Update vite.config.ts and src/index.css

4. **Configure path aliases:**
   Update vite.config.ts and tsconfig.json

5. **Initialize shadcn/ui:**
   ```bash
   npx shadcn@latest init
   npx shadcn@latest add button
   ```

6. **Add state management:**
   ```bash
   npm install @tanstack/react-query zustand
   ```
   Create lib/query.ts and stores/ui.ts

7. **Verify setup:**
   ```bash
   npm run dev
   ```
   Open http://localhost:5173

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-12-14 | Story drafted from epics and architecture | SM Agent (Bob) |
| 2025-12-14 | Implementation complete - all tasks done | Dev Agent (Amelia/Sonnet) |
| 2025-12-14 | Code review complete - 7 issues found and fixed | Dev Agent (Amelia/Opus) |

---

**Story Status:** Complete

# SM Parallel Epic Execution Workflow

_Documentation for the SM agent's `*parallel-epic` workflow that orchestrates BMAD sprint delivery using Claude Code subagents._

---

## Quick Start

```
/bmad:bmm:agents:sm

*parallel-epic
```

This invokes the SM (Scrum Master) agent and triggers the parallel epic execution workflow, which:
1. Reads sprint-status.yaml to identify stories in the target epic
2. Groups stories into dependency waves
3. For each story: creates → validates → implements → reviews → merges
4. Updates sprint-status.yaml as stories complete

**Workflow Location:** `.bmad/bmm/workflows/4-implementation/parallel-epic-execution/`

---

## How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  SM ORCHESTRATOR (Bob / Opus or Sonnet)                     │
│  - Reads sprint-status.yaml                                 │
│  - Analyzes story dependencies, plans waves                 │
│  - Dispatches parallel subagents per wave                   │
│  - Reviews results at checkpoints                           │
│  - OWNS all merges and sprint-status.yaml updates           │
└─────────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
   ┌─────────────┐                 ┌─────────────┐
   │ DEV AGENT   │                 │ DEV AGENT   │
   │ (Sonnet)    │ ──────────────► │ (Opus)      │
   │             │                 │             │
   │ /dev-story  │                 │ /code-review│
   │ implements  │                 │ validates   │
   └─────────────┘                 └─────────────┘
```

### Execution Phases

**Phase 1: Preparation**
1. **Load Context** - Read sprint-status.yaml, project_context.md, dependency analysis
2. **Dependency Analysis** - Map story dependencies, group into waves
3. **Verify Prerequisites** - Confirm story files exist and are ready-for-dev

**Phase 2: Execution (Per Wave)**

For each story in wave (parallel where no dependencies exist):

1. **Story Preparation** (if status = `drafted`)
   - Dispatch Create-Story subagent (Sonnet) to flesh out tasks, ACs, technical details
   - Dispatch Validate-Story subagent (Opus) to verify completeness, flag gaps
   - If validation verdict = `needs-revision` → fix and re-validate
   - If validation verdict = `needs-discussion` → escalate to user
   - Mark story `ready-for-dev` in story file footer

2. **Implementation** (if status = `ready-for-dev`)
   - SM creates story branch: `git checkout -b story/{branch} dev`
   - Dispatch Dev-Story subagent (Sonnet)
   - Dev executes tasks in order, commits at logical checkpoints
   - Returns structured result

3. **Code Review Gate**
   - Dispatch Code-Review subagent (Opus)
   - Finds 3-10 specific issues
   - Fixes issues directly
   - Returns verdict (approved/needs-rework)

4. **Merge and Update** - SM orchestrator owns all merges:
   - `git checkout dev && git pull`
   - `git merge --no-ff story/{branch}`
   - Update sprint-status.yaml (single story)
   - Push to origin
   - Delete story branch

5. **Wave Completion** - When all stories in wave complete, proceed to next wave

**Phase 3: Completion**
1. **Final Verification** - All tests pass, build succeeds
2. **Update Epic Status** - Mark epic done in sprint-status.yaml
3. **Generate Execution Log** - Document the parallel execution results

---

## Design Principles

### 1. Dual-Model Review Pattern

| Phase | Model | Rationale |
|-------|-------|-----------|
| **Generation** (create-story, dev-story) | Sonnet | Fast, cost-effective, excellent workflow following |
| **Validation** (validate-story, code-review) | Opus | Deeper reasoning, catches gaps Sonnet misses |

This mirrors BMAD's official guidance:
- Sonnet: "excellent workflow following, coding, reasoning"
- Opus: "maximum context, complex planning"

**Important:** Haiku is NOT recommended for BMM workflows.

### 2. YOLO Through Generation, Checkpoint at Review

Don't over-analyze between steps. Let subagents run autonomously, then validate at review gates.

```
Dev (Sonnet)     Dev (Opus)
implements  ───► reviews
   │                │
   └── YOLO ────────┴── CHECKPOINT (analyze here)
```

### 3. Subagent Autonomy

Subagents cannot ask interactive questions. They must:
- Make reasonable decisions based on provided context
- Document decisions in commits/output
- Return structured results for orchestrator review
- Flag blockers rather than stopping silently

### 4. Serial Story Pipeline

Stories flow through a serial pipeline rather than batching phases:

```
drafted → Create (Sonnet) → Validate (Opus) → ready-for-dev → Implement (Sonnet) → Review (Opus) → done
```

**Why serial over batched:**
- Simpler orchestration - one state machine per story
- Faster first delivery - Story A done while batched approach still preparing
- Natural feedback loop - lessons from Story A inform Story B
- Easier recovery - if Story B fails, A is already shipped

### 5. Git Responsibility Separation

Git operations are split between SM orchestrator and Dev subagents:

| Operation | Owner | When |
|-----------|-------|------|
| Branch creation | SM | Before dispatching Dev subagent |
| Commits | Dev | At logical checkpoints during implementation |
| Merge to dev | SM | After code review approval |
| Push to origin | SM | After successful merge |
| Branch deletion | SM | After push succeeds |

**Why this split:**
- SM has full visibility into sprint state and can coordinate branches across parallel stories
- Dev focuses purely on implementation without git state management
- Single point of control for remote operations prevents race conditions
- If Dev fails mid-implementation, SM can easily clean up

**Note:** The Git Workflow Rules section in `project_context.md` is commented out. This orchestration doc is the source of truth for subagent git workflow.

### 6. Native BMAD Invocation

Subagents use native BMAD agent loading rather than custom prompts:

| Aspect | Custom Prompts | Native BMAD |
|--------|----------------|-------------|
| Persona source | Duplicated in prompt | Single source (agent file) |
| Workflow logic | Duplicated in prompt | Single source (workflow file) |
| Maintenance | Update in multiple places | Update once, propagates |
| Consistency | May drift from interactive | Always matches interactive |
| Prompt size | Large (~200 lines each) | Tiny (2-3 lines) |

### 7. Parallel Execution with Worktrees and CLI Subprocesses

Claude Code Task tool subagents share the same filesystem and git repository. This creates branch contention when multiple stories execute simultaneously. The solution is **1:1 mapping of subagent to Claude CLI instance**, each in its own worktree.

**Architecture:**

```
SM Orchestrator (this Claude Code instance)
│
├─ 1. Read sprint-status.yaml, determine pipeline per story by status
│     - backlog:      create → validate → implement → review
│     - drafted:      validate → implement → review
│     - ready-for-dev: implement → review
│     - done:         SKIP
│
├─ 2. Batch-create worktrees (one per non-done story in wave)
│
├─ 3. Issue PARALLEL Bash tool calls (one per story, all in single message)
│     Each Bash call runs the appropriate pipeline chained with &&
│
├─ 4. SM waits for all parallel calls to return
│
├─ 5. SM merges completed stories to dev (sequential)
│
└─ 6. SM cleans up worktrees
```

**Validated Pattern (tested 2025-12-14):**

```bash
# Step 1: SM batch-creates worktrees
git worktree add /tmp/wt-story-1-3 -b story/1-3-setup-database dev
git worktree add /tmp/wt-story-1-4 -b story/1-4-create-api dev
git worktree add /tmp/wt-story-1-5 -b story/1-5-add-auth dev
```

```
# Step 2: SM issues parallel Bash tool calls (in single message)
# Pipeline length depends on story status - all calls execute CONCURRENTLY

# For backlog stories (no story file yet) - full pipeline:
Bash({ command: "cd /tmp/wt-story-1-5 && claude --dangerously-skip-permissions -p '/bmad:bmm:agents:sm

*create-story 1-5 #yolo' && claude --dangerously-skip-permissions -p '/bmad:bmm:agents:sm

*validate-create-story 1-5 #yolo' && claude --dangerously-skip-permissions -p '/bmad:bmm:agents:dev

*develop-story 1-5 #yolo' && claude --dangerously-skip-permissions -p '/bmad:bmm:agents:dev

*code-review 1-5 #yolo'", timeout: 600000 })

# For drafted stories (story file exists, needs validation):
Bash({ command: "cd /tmp/wt-story-1-6 && claude --dangerously-skip-permissions -p '/bmad:bmm:agents:sm

*validate-create-story 1-6 #yolo' && claude --dangerously-skip-permissions -p '/bmad:bmm:agents:dev

*develop-story 1-6 #yolo' && claude --dangerously-skip-permissions -p '/bmad:bmm:agents:dev

*code-review 1-6 #yolo'", timeout: 600000 })

# For ready-for-dev stories (validated, ready to implement):
Bash({ command: "cd /tmp/wt-story-1-7 && claude --dangerously-skip-permissions -p '/bmad:bmm:agents:dev

*develop-story 1-7 #yolo' && claude --dangerously-skip-permissions -p '/bmad:bmm:agents:dev

*code-review 1-7 #yolo'", timeout: 600000 })

# Stories with status=done are skipped entirely
```

**Key Insight:** Parallel Bash tool calls in a single message run concurrently. Each story runs its pipeline (length based on status) chained with `&&`. SM waits for all to complete, then merges sequentially.

**Why This Works:**

| Aspect | Behavior |
|--------|----------|
| Concurrency | Multiple Bash calls in one message execute in parallel |
| Serial Pipeline | Each story completes its full lifecycle before SM merges |
| Isolation | Each CLI runs in its own worktree (separate filesystem, branch) |
| Fail-fast | `&&` chaining stops pipeline if any step fails |
| Git safety | No checkout conflicts - each worktree has its own branch |

**Progress Visibility (Optional):**

While waiting for parallel calls, SM can poll worktree git logs:

```bash
for wt in /tmp/wt-story-*; do echo "=== $wt ===" && git -C $wt log --oneline -5; done
```

**Cleanup after merge:**

```bash
git worktree remove /tmp/wt-story-1-3
git branch -d story/1-3-setup-database  # Local branch
git push origin --delete story/1-3-setup-database  # Remote branch
```

---

## Subagent Reference

### YOLO Mode

From `.bmad/core/tasks/workflow.xml`:

```xml
<execution-modes>
  <mode name="normal">Full user interaction and confirmation of EVERY step</mode>
  <mode name="yolo">Skip all confirmations and elicitation, minimize prompts and
    try to produce all of the workflow automatically by simulating the remaining
    discussions with a simulated expert user</mode>
</execution-modes>
```

The `#yolo` suffix triggers autonomous execution without interactive prompts.

### Story ID Format

Workflows accept story IDs in multiple formats (from `create-story/instructions.xml`):

| Format | Example | Notes |
|--------|---------|-------|
| Dash notation | `1-3` | Epic 1, Story 3 |
| Dot notation | `1.3` | Epic 1, Story 3 |
| Natural language | `epic 1 story 3` | Verbose but clear |
| Full key | `1-3-setup-database` | With kebab-case title |

The workflow parses these into `{{epic_num}}`, `{{story_num}}`, and `{{story_key}}` variables.

### Subagent Invocations

#### Create-Story (Sonnet) → SM Agent

```
/bmad:bmm:agents:sm

*create-story 1-3 #yolo
```

**Agent:** Bob (Scrum Master)
**Workflow:** `.bmad/bmm/workflows/4-implementation/create-story/workflow.yaml`

#### Validate-Story (Opus) → SM Agent

```
/bmad:bmm:agents:sm

*validate-create-story 1-3 #yolo
```

**Agent:** Bob (Scrum Master)
**Purpose:** Adversarial validation before marking ready-for-dev

#### Dev-Story (Sonnet) → Dev Agent

```
/bmad:bmm:agents:dev

*develop-story 1-3 #yolo
```

**Agent:** Amelia (Developer)
**Workflow:** `.bmad/bmm/workflows/4-implementation/dev-story/workflow.yaml`

#### Code-Review (Opus) → Dev Agent

```
/bmad:bmm:agents:dev

*code-review 1-3 #yolo
```

**Agent:** Amelia (Developer)
**Workflow:** `.bmad/bmm/workflows/4-implementation/code-review/workflow.yaml`

### Model Selection Summary

| Task | Recommended Model | Rationale |
|------|-------------------|-----------|
| Create-Story | Sonnet | Workflow following, task extraction, structured output |
| Validate-Story | Opus | Adversarial review, catch gaps before implementation |
| Dev-Story (implementation) | Sonnet | Code generation, workflow adherence |
| Code-Review | Opus | Adversarial review, deeper reasoning |
| Status updates | Sonnet | Straightforward file operations |
| SM Orchestration | Opus | Coordination, decision-making, escalation judgment |

---

## Orchestrator Checklists

### Before Dispatching Story Pipeline

- [ ] Identified stories for wave from sprint-status.yaml
- [ ] Story status determines pipeline (backlog/drafted/ready-for-dev → different pipelines, done → skip)
- [ ] Worktrees created for each non-done story in wave
- [ ] Project context is up to date

### After Story Pipeline Returns

- [ ] Exit code is 0 (pipeline completed successfully)
- [ ] If non-zero: check which step failed (create/validate/implement/review)
- [ ] Review git log in worktree for commits made
- [ ] Note any issues for manual review if needed

### Finalization

- [ ] Update story file changelog
- [ ] Merge story branch to dev (--no-ff)
- [ ] Delete story branch
- [ ] Push to origin
- [ ] Update sprint-status.yaml if not already done

---

## Handling Edge Cases

### Subagent Returns `blocked`

1. Read the blocker description
2. Determine if you (orchestrator) can resolve it
3. If yes: provide guidance and re-dispatch
4. If no: escalate to user with context

### Subagent Returns `partial`

1. Review what was completed vs. remaining
2. Determine if partial work is committable
3. Either re-dispatch with narrower scope or escalate

### Code Review Returns `needs-rework`

1. Review the issues found
2. If issues are fixable by another subagent dispatch, do so
3. If issues require architectural discussion, escalate to user

### Interactive Prompts in Subagents

Some tools (like `npx shadcn@latest init`) have interactive prompts. Subagents should:
- Use non-interactive flags where available
- Accept defaults when prompts can't be avoided
- Document any unexpected prompt responses

---

## Lessons Learned

### From Story 1-2 (Frontend Init)

1. **Dual-model pattern works** - Sonnet implemented, Opus found 7 real issues
2. **Git workflow followed** - Subagents correctly created branches and committed
3. **Self-healing** - Opus fixed issues it found, didn't just report them
4. **Autonomy succeeded** - No human intervention needed during execution
5. **Root .gitignore patterns** - May need `git add -f` for paths matching ignore patterns

### Common Issues to Watch

- Story file footer may not update (fix manually or in finalization)
- Checkpoint files may cause branch switch conflicts (stash if needed)
- Some npm packages need `--force` with React 19

---

## Supporting BMAD Changes

The following changes were made to `.bmad/` to support this workflow:

### SM Agent Menu Addition

**File:** `.bmad/bmm/agents/sm.md`

Added `*parallel-epic` menu item to SM agent:

```xml
<item cmd="*parallel-epic" workflow="{project-root}/.bmad/bmm/workflows/4-implementation/parallel-epic-execution/workflow.yaml">
  Execute entire epic with parallel subagents (Sonnet implements, Opus reviews, SM merges)
</item>
```

### Git Workflow in project_context.md

**File:** `docs/project_context.md`

The Git Workflow Rules section is commented out in project_context.md. This orchestration document is the authoritative source for git workflow in subagent mode. The comment header explains how to restore interactive rules if needed:

```markdown
<!-- COMMENTED OUT: Git Workflow Rules are handled by SM orchestrator in subagent model.
     See docs/bmad-subagent-orchestration.md for git responsibilities:
     - SM owns: branch creation, merging, pushing, branch deletion
     - Dev owns: commits only (logical checkpoints within branch)
     Restore these rules if returning to interactive human-driven sessions.
-->
```

### Agent Customization Files

**Files:** `.bmad/_cfg/agents/bmm-*.customize.yaml`

Agent customization files contain notes pointing to this orchestration doc for git workflow guidance. No critical action overrides are needed since:
- Git operations are handled by SM orchestrator, not individual agents
- Dev agents only need to commit (which they do naturally during implementation)
- Other agents treat project_context.md as their guide for coding standards

### Parallel Epic Execution Workflow

**Location:** `.bmad/bmm/workflows/4-implementation/parallel-epic-execution/`

New workflow files created:
- `workflow.yaml` - Workflow configuration
- `instructions.xml` - Orchestration instructions
- `checklist.md` - Validation checklist

### Future Refactoring (When BMAD Build Fixed)

The `*parallel-epic` menu item was added directly to `sm.md` because `npx bmad-method build` is broken in v6.0.0-alpha.16 ([Issue #1129](https://github.com/bmad-code-org/BMAD-METHOD/issues/1129)).

When the build command is fixed, migrate to the proper customization pattern:

1. Move menu item to `.bmad/_cfg/agents/bmm-sm.customize.yaml`:
   ```yaml
   menu:
     - trigger: parallel-epic
       workflow: "{project-root}/.bmad/bmm/workflows/4-implementation/parallel-epic-execution/workflow.yaml"
       description: Execute entire epic with parallel subagents (Sonnet implements, Opus reviews, SM merges)
   ```

2. Remove the `*parallel-epic` item from `.bmad/bmm/agents/sm.md`

3. Run `npx bmad-method build sm` to apply

This ensures BMAD updates won't overwrite the customization.

---

## Version History

| Date | Change | Author |
|------|--------|--------|
| 2025-12-14 | Status-based pipeline: backlog (4 steps), drafted (3), ready-for-dev (2), done (skip) | Winston |
| 2025-12-14 | Simplify to plain Bash - remove SDK wrapper, use && chaining for serial pipeline per story | Winston |
| 2025-12-14 | Add worktree isolation pattern for parallel execution | Winston |
| 2025-12-14 | Simplify git responsibilities: SM owns all git ops except commits | Winston |
| 2025-12-14 | Replace custom prompts with native BMAD agent/workflow invocation using #yolo mode | Winston |
| 2025-12-14 | Add serial story pipeline (create → validate → implement → review) | Winston |
| 2025-12-14 | Initial documentation based on Story 1-2 execution | BMad Master |

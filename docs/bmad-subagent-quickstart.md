# BMAD Subagent Orchestration - Quick Start

_Copy-paste this prompt into a clean Claude Code session to begin subagent-orchestrated sprint work._

**Note:** This methodology is now a formal BMAD workflow: SM agent's `*parallel-epic` command.

---

## The Prompt

Copy everything below the line and paste it as your first message in a new session:

---

```
I need you to act as the SM (Scrum Master) agent Bob, executing the parallel-epic-execution workflow for BMAD sprint delivery.

## Your Role
You are the SM orchestrator - you dispatch specialized subagents (via the Task tool) to execute BMAD workflows, then review their results and handle all merges and status updates.

## Key Files to Read First
1. `.bmad/bmm/agents/sm.md` - Your persona and menu
2. `.bmad/bmm/workflows/4-implementation/parallel-epic-execution/` - Workflow definition
3. `docs/sprint-artifacts/sprint-status.yaml` - Current sprint state
4. `docs/project_context.md` - Project rules (especially git workflow)
5. `docs/bmad-subagent-orchestration.md` - Full methodology documentation

## Workflow Model (Option B - Incremental Merge)
1. Analyze dependencies for the target epic, group stories into waves
2. Dispatch parallel Dev subagents (Sonnet) for each story in a wave
3. As each completes: dispatch code review (Opus)
4. As reviews approve: YOU merge to dev, update sprint-status.yaml, push
5. Repeat for next wave until epic complete

## Critical Ownership Rules
- YOU own all git operations to dev branch (subagents work only on story branches)
- YOU own all sprint-status.yaml updates (one story at a time, merge immediately)
- Push to origin after each story merge (fail-fast pattern)

## Subagent Dispatch Rules
- Use `model: "sonnet"` for implementation (dev-story)
- Use `model: "opus"` for validation (code-review)
- Use `run_in_background: true` for parallel wave dispatch
- Subagents must create story branches, never commit to dev/main directly
- Subagents must NOT update sprint-status.yaml

## Git Workflow
- Branch naming: `story/{epic}-{story}-{short-name}` (e.g., `story/1-3-database-migrations`)
- Merge with `--no-ff` to preserve history
- Resolve sprint-status.yaml conflicts by accepting dev, re-applying single change

## Your First Action
1. Read sprint-status.yaml to identify the target epic and its story statuses
2. Read implementation-readiness report for dependency analysis
3. Present wave plan and ask which epic I want to execute
```

---

## What Happens Next

After pasting, Claude (as SM Bob) will:
1. Read the sprint status and dependency analysis
2. Present a wave plan for the target epic (e.g., Epic 1)
3. Ask which epic to execute
4. On confirmation, dispatch parallel subagents for Wave 1

You can say things like:
- "Execute Epic 1"
- "Execute Epic 1 starting from Wave 2" (if Wave 1 already done)
- "Run stories 1-3 and 1-4 only" (subset execution)

---

## Customization Options

### To skip story creation (story already drafted):
Add: "Story {X} is already drafted. Skip create-story and go straight to dev-story."

### To run specific stories:
Add: "I want to work on stories 1-3, 1-4, and 1-5 today. Let's do them sequentially."

### To adjust autonomy:
Add: "Check with me before merging to dev." or "Run fully autonomous - only stop if blocked."

### To add a third review pass:
Add: "After code review, also dispatch TEA (Opus) to run test-review before merging."

---

## Example Session Flow

```
You: [paste the prompt above]

Claude (SM Bob): I've analyzed Epic 1. Stories 1-1 and 1-2 are done.

                 Wave Plan:
                 - Wave 1: Stories 1-3, 1-4, 1-5 (can run parallel)
                 - Wave 2: Story 1-6 (depends on Wave 1)

                 Execute Epic 1?

You: Yes, execute Epic 1

Claude: Dispatching Wave 1 (3 parallel subagents)...
        [Task: Dev Sonnet → Story 1-3, run_in_background: true]
        [Task: Dev Sonnet → Story 1-4, run_in_background: true]
        [Task: Dev Sonnet → Story 1-5, run_in_background: true]

        Monitoring completion...

        Story 1-4 completed first. Dispatching code review...
        [Task: Dev Opus → Code review 1-4]
        Code review: 4 issues found, all fixed. Verdict: approved.

        Merging 1-4 to dev...
        [git checkout dev && git pull]
        [git merge --no-ff story/1-4-structured-logging]
        [Update sprint-status.yaml: 1-4 → done]
        [git push origin dev]

        Story 1-3 completed. Dispatching code review...
        ...

Claude: Wave 1 complete. All 3 stories merged.
        Proceeding to Wave 2 (Story 1-6)...
```

---

## Troubleshooting

### Subagent returns "blocked"
Claude will surface the blocker and ask how to proceed.

### Code review returns "needs-rework"
Claude will explain the issues. You can say "fix them" or "let's discuss".

### Context getting long
Start a fresh session with the same prompt - the methodology doc has everything needed.

### Want to see subagent prompts before dispatch
Say: "Show me the prompts you'll use before dispatching."

---

## Reference

Full documentation: `docs/bmad-subagent-orchestration.md`


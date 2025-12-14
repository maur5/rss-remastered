# Parallel Epic Execution - Validation Checklist

## Pre-Execution Validation

### Epic Readiness
- [ ] Epic number specified and valid
- [ ] Epic exists in sprint-status.yaml
- [ ] Stories identified with their current status (backlog/drafted/ready-for-dev/done)

### Git State
- [ ] Currently on dev branch
- [ ] Working directory is clean (no uncommitted changes)
- [ ] Dev branch is up to date with origin/dev

### Context Loaded
- [ ] project_context.md available
- [ ] sprint-status.yaml current state captured
- [ ] Implementation readiness report reviewed (if exists)

## Wave Planning Validation

### Dependency Analysis
- [ ] All story dependencies within epic identified
- [ ] Stories correctly grouped into waves
- [ ] No circular dependencies detected
- [ ] Wave 1 contains only stories with no internal dependencies

### Resource Allocation
- [ ] max_parallel_stories not exceeded in any wave (default: 3)
- [ ] Stories in same wave have no dependencies on each other

## Execution Validation (Per Wave)

### Worktree Setup
- [ ] Worktree created for each story: /tmp/wt-story-{id}
- [ ] Branch created in worktree: story/{branch-name}

### Pipeline Dispatch
- [ ] Parallel Bash calls issued (one per story, all in single message)
- [ ] Pipeline determined by status:
  - backlog: create → validate → implement → review
  - drafted: validate → implement → review
  - ready-for-dev: implement → review
  - done: skip entirely
- [ ] All calls use --dangerously-skip-permissions flag
- [ ] Timeout set appropriately (600000ms = 10 min)

### Pipeline Results
- [ ] Exit code 0 = pipeline succeeded
- [ ] Exit code non-zero = check which step failed
- [ ] Git log in worktree shows commits made

### Merge Process (Sequential)
- [ ] Dev branch pulled before each merge
- [ ] Merge performed with --no-ff flag
- [ ] sprint-status.yaml updated for this story only
- [ ] Changes pushed to origin immediately
- [ ] Worktree removed
- [ ] Story branch deleted locally and remotely

## Post-Wave Validation

### Test Suite
- [ ] Tests pass on dev branch (if configured)
- [ ] No regressions introduced by merged stories

### Status Tracking
- [ ] All completed stories marked done in sprint-status.yaml
- [ ] Blocked stories documented with reasons

## Epic Completion Validation

### Final State
- [ ] All epic stories show status: done
- [ ] Epic status updated to done in sprint-status.yaml

### Cleanup
- [ ] All worktrees removed
- [ ] All story branches deleted
- [ ] No orphaned branches remaining
- [ ] Git state clean on dev

## Error Scenarios

### Pipeline Failures
- [ ] Non-zero exit code logged with story ID
- [ ] Other parallel stories unaffected
- [ ] User notified of blocked stories

### Merge Conflicts
- [ ] sprint-status.yaml conflicts: accept dev, re-apply single change
- [ ] Code conflicts: HALT and report to user

### Test Failures on Dev
- [ ] Wave execution halted
- [ ] User notified with failure details

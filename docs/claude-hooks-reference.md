# Claude Code Hooks Reference

This document describes the custom Claude Code hooks configured for this project.

## Overview

The Session Checkpoint System preserves BMAD agent state across context compaction, ensuring:
1. Agent personas reload automatically after compaction
2. Workflow context and pending steps are preserved
3. Non-BMAD sessions are unaffected (hooks stay silent)

## Configuration

**Location:** `.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [{ "type": "command", "command": ".claude/hooks/session-start.sh" }]
      },
      {
        "matcher": "compact",
        "hooks": [{ "type": "command", "command": ".claude/hooks/session-resume.sh" }]
      }
    ]
  }
}
```

## Hooks

### session-start.sh

**Trigger:** New session startup

**Purpose:**
- Creates `.claude/checkpoints/` directory if needed
- Exposes `SESSION_ID` environment variable to Claude

**Location:** `.claude/hooks/session-start.sh`

### session-resume.sh

**Trigger:** After context compaction (auto or manual)

**Purpose:**
- Checks for checkpoint file at `.claude/checkpoints/{SESSION_ID}.md`
- If checkpoint exists:
  - Injects agent activation prompt directly (no slash command needed)
  - Displays checkpoint context (current state, pending steps)
- If no checkpoint: exits silently (non-BMAD session)

**Location:** `.claude/hooks/session-resume.sh`

## Checkpoint System

### File Structure

```
.claude/
├── settings.json          # Hook configuration
├── settings.local.json    # Permissions (gitignored)
├── hooks/
│   ├── session-start.sh   # Startup hook
│   └── session-resume.sh  # Post-compaction hook
├── checkpoints/
│   └── {session_id}.md    # Per-session checkpoint files
└── commands/
    └── bmad/              # BMAD slash commands
```

### Checkpoint Format

```markdown
# Session Checkpoint
_Updated: 2025-12-14T10:30:00_

## Resume
**Agent:** pm
**Context:** Implementing story 1-2-health-endpoint via dev-story workflow

## Current State
- **Story:** 1-2-health-endpoint
- **Phase:** dev (in progress)
- **Branch:** story/1-2-health-endpoint

## Pending Steps
1. Complete health endpoint implementation
2. Write tests per acceptance criteria
3. Run code-review workflow for validation
4. Update sprint-status.yaml
5. Commit with [story] prefix

## Notes
Working on task 3 of 5 in the story file.
```

### When Checkpoints Are Written

Agents should write/update checkpoints:
- At every status file update (workflow, sprint, story)
- Before long-running operations
- When switching workflow phases
- Proactively when context feels heavy

This is **agent discipline** defined in `docs/project_context.md`.

## Behavior Matrix

| Scenario | Checkpoint Exists? | Hook Behavior |
|----------|-------------------|---------------|
| BMAD session (agent wrote checkpoint) | Yes | Full agent reload + context display |
| BMAD session (forgot to checkpoint) | No | Silent (discipline failure) |
| Non-BMAD session | No | Silent (no interference) |

## How It Works

### Normal BMAD Session Flow

1. **Session starts** → `session-start.sh` runs
   - Creates checkpoints directory
   - Writes `SESSION_ID` to env file

2. **Agent works** → Agent writes checkpoint at status updates
   - File: `.claude/checkpoints/{SESSION_ID}.md`

3. **Compaction happens** → `session-resume.sh` runs
   - Finds checkpoint file
   - Outputs agent activation prompt directly
   - Displays checkpoint contents

4. **Agent resumes** → Claude sees activation prompt
   - Loads agent file
   - Reads checkpoint context
   - Continues from pending steps

### Non-BMAD Session Flow

1. **Session starts** → `session-start.sh` runs (same as above)
2. **User works** → No checkpoint written (no agent rules)
3. **Compaction happens** → `session-resume.sh` runs
   - No checkpoint found
   - Exits silently (exit code 0)
4. **Session continues** → Claude's natural summary takes over

## Agent Activation Injection

Instead of asking Claude to run a slash command, the hook outputs the activation prompt directly:

```
You must fully embody this agent's persona and follow all activation instructions exactly as specified. NEVER break character until given an exit command.

<agent-activation CRITICAL="TRUE">
1. LOAD the FULL agent file from .bmad/bmm/agents/{AGENT}.md
2. READ its entire contents - this contains the complete agent persona, menu, and instructions
3. Execute ALL activation steps exactly as written in the agent file
4. Follow the agent's persona and menu system precisely
5. Stay in character throughout the session
</agent-activation>
```

This is the same content the `/bmad:bmm:agents:{agent}` slash command would deliver, but injected directly without requiring tool invocation.

## Troubleshooting

### Checkpoint not being read after compaction

1. Verify checkpoint file exists: `ls .claude/checkpoints/`
2. Check SESSION_ID matches: `echo $SESSION_ID`
3. Verify hook is configured: check `.claude/settings.json`

### Agent not reloading

1. Verify agent name in checkpoint matches file: `.bmad/bmm/agents/{agent}.md`
2. Check hook script is executable: `ls -la .claude/hooks/`

### Hooks not running

1. Verify `.claude/settings.json` exists and is valid JSON
2. Check hook scripts are executable: `chmod +x .claude/hooks/*.sh`

## Maintenance

### Checkpoint Cleanup

Checkpoints persist indefinitely. Manual cleanup if needed:

```bash
# Remove all checkpoints
rm -rf .claude/checkpoints/*.md

# Remove checkpoints older than 30 days
find .claude/checkpoints -name "*.md" -mtime +30 -delete
```

### Future Considerations

- **SessionEnd hook:** Could auto-delete checkpoint on graceful session end
- **Age-based cleanup:** Could add to session-start.sh if accumulation becomes an issue
- **Workflow state:** Could expand checkpoint to track mid-workflow step numbers

## Related Documentation

- `docs/project_context.md` - Agent rules including checkpoint discipline
- `.bmad/bmm/agents/*.md` - BMAD agent definitions
- `.claude/commands/bmad/` - BMAD slash commands

---

_Last updated: 2025-12-14_

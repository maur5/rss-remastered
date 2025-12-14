#!/bin/bash
# session-resume.sh - Runs after context compaction
#
# Purpose:
# - If checkpoint exists: inject agent activation prompt + show context
# - If no checkpoint: stay silent (non-BMAD session, don't interfere)
#
# Part of the Session Checkpoint System for BMAD agent continuity.
# See: docs/claude-hooks-reference.md

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)

CHECKPOINT_FILE="$CLAUDE_PROJECT_DIR/.claude/checkpoints/${SESSION_ID}.md"

# No checkpoint = not a BMAD session, exit silently
[ ! -f "$CHECKPOINT_FILE" ] && exit 0

# Extract agent name from checkpoint
AGENT=$(grep -E "^\*\*Agent:\*\*" "$CHECKPOINT_FILE" | sed 's/\*\*Agent:\*\* //')

echo "══════════════════════════════════════════════════════════════"
echo " SESSION RESUMED AFTER CONTEXT COMPACTION"
echo "══════════════════════════════════════════════════════════════"
echo ""

# Inject agent activation if agent found
if [ -n "$AGENT" ]; then
  AGENT_FILE="$CLAUDE_PROJECT_DIR/.bmad/bmm/agents/${AGENT}.md"

  if [ -f "$AGENT_FILE" ]; then
    echo "Reloading agent: $AGENT"
    echo ""
    echo "You must fully embody this agent's persona and follow all activation instructions exactly as specified. NEVER break character until given an exit command."
    echo ""
    echo "<agent-activation CRITICAL=\"TRUE\">"
    echo "1. LOAD the FULL agent file from .bmad/bmm/agents/${AGENT}.md"
    echo "2. READ its entire contents - this contains the complete agent persona, menu, and instructions"
    echo "3. Execute ALL activation steps exactly as written in the agent file"
    echo "4. Follow the agent's persona and menu system precisely"
    echo "5. Stay in character throughout the session"
    echo "</agent-activation>"
    echo ""
  else
    echo "Warning: Agent file not found: .bmad/bmm/agents/${AGENT}.md"
    echo "You may need to manually reload the agent."
    echo ""
  fi
fi

echo "══════════════════════════════════════════════════════════════"
echo " CHECKPOINT CONTEXT"
echo "══════════════════════════════════════════════════════════════"
echo ""
cat "$CHECKPOINT_FILE"
echo ""
echo "══════════════════════════════════════════════════════════════"
echo " Continue from Pending Steps after agent activation completes."
echo "══════════════════════════════════════════════════════════════"

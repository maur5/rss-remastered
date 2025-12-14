#!/bin/bash
# session-start.sh - Runs on new session startup
#
# Purpose:
# - Creates checkpoints directory if needed
# - Exposes SESSION_ID to Claude via env file
#
# Part of the Session Checkpoint System for BMAD agent continuity.
# See: docs/claude-hooks-reference.md

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)

# Write session ID to env file so Claude can access it
if [ -n "$SESSION_ID" ] && [ -n "$CLAUDE_ENV_FILE" ]; then
  echo "SESSION_ID=$SESSION_ID" >> "$CLAUDE_ENV_FILE"
fi

# Ensure checkpoints directory exists
mkdir -p "$CLAUDE_PROJECT_DIR/.claude/checkpoints"

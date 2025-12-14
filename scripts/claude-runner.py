#!/usr/bin/env python3
"""
Claude Agent SDK wrapper with streaming progress output.

Usage:
    python claude-runner.py --story-id 1-3 --cwd /tmp/wt-story-1-3 --prompt "..."

Output format (stdout):
    [1-3] > Starting...
    [1-3] @ Edit: backend/src/main.py
    [1-3] @ Bash: npm test
    [1-3] * Complete
"""

import argparse
import asyncio
import sys
import os
from datetime import datetime

try:
    from claude_code_sdk import query, ClaudeCodeOptions
    from claude_code_sdk.types import (
        AssistantMessage,
        ResultMessage,
        SystemMessage,
        UserMessage,
        ToolUseBlock,
        TextBlock,
    )
except ImportError:
    print("Error: claude-code-sdk not installed. Run: pip install claude-code-sdk", file=sys.stderr)
    sys.exit(1)


LOG_FILE = None

def log(story_id: str, icon: str, message: str):
    """Print a prefixed log line and optionally write to file."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{story_id}] {icon} {message}"
    print(line, flush=True)

    # Also write to log file if configured
    if LOG_FILE:
        with open(LOG_FILE, 'a') as f:
            f.write(f"{timestamp} {line}\n")


async def run_agent(story_id: str, cwd: str, prompt: str, accept_permissions: bool = True):
    """Run a Claude agent with streaming output."""

    log(story_id, ">", "Starting...")

    options = ClaudeCodeOptions(
        cwd=cwd,
        permission_mode="acceptEdits" if accept_permissions else "default",
    )

    tool_count = 0
    last_tool = None

    try:
        async for message in query(prompt=prompt, options=options):
            # Handle AssistantMessage (contains tool use and text)
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, ToolUseBlock):
                        tool_name = block.name
                        tool_count += 1

                        # Extract brief info based on tool type
                        tool_input = block.input or {}
                        detail = ""

                        if tool_name == 'Edit':
                            detail = tool_input.get('file_path', '').split('/')[-1]
                        elif tool_name == 'Write':
                            detail = tool_input.get('file_path', '').split('/')[-1]
                        elif tool_name == 'Read':
                            detail = tool_input.get('file_path', '').split('/')[-1]
                        elif tool_name == 'Bash':
                            cmd = tool_input.get('command', '')[:40]
                            detail = cmd + ('...' if len(tool_input.get('command', '')) > 40 else '')
                        elif tool_name == 'Grep':
                            detail = tool_input.get('pattern', '')[:30]
                        elif tool_name == 'Glob':
                            detail = tool_input.get('pattern', '')[:30]

                        # Avoid duplicate logs for same tool
                        tool_key = f"{tool_name}:{detail}"
                        if tool_key != last_tool:
                            log(story_id, "@", f"{tool_name}: {detail}" if detail else tool_name)
                            last_tool = tool_key

            # Handle ResultMessage
            elif isinstance(message, ResultMessage):
                subtype = message.subtype
                if subtype == 'success':
                    log(story_id, "*", f"Complete ({tool_count} tool calls)")
                else:
                    log(story_id, "!", f"Finished: {subtype}")

    except Exception as e:
        log(story_id, "X", f"Error: {str(e)[:50]}")
        return 1

    return 0


def main():
    global LOG_FILE

    parser = argparse.ArgumentParser(description="Claude Agent SDK wrapper with streaming progress")
    parser.add_argument('--story-id', '-s', required=True, help="Story identifier for log prefix")
    parser.add_argument('--cwd', '-c', default='.', help="Working directory for the agent")
    parser.add_argument('--prompt', '-p', required=True, help="Prompt to send to the agent")
    parser.add_argument('--no-accept', action='store_true', help="Don't auto-accept permissions")
    parser.add_argument('--log-file', '-l', help="Also write progress to this file")

    args = parser.parse_args()

    # Set global log file
    if args.log_file:
        LOG_FILE = args.log_file

    # Verify cwd exists
    if not os.path.isdir(args.cwd):
        print(f"Error: Directory does not exist: {args.cwd}", file=sys.stderr)
        sys.exit(1)

    exit_code = asyncio.run(run_agent(
        story_id=args.story_id,
        cwd=args.cwd,
        prompt=args.prompt,
        accept_permissions=not args.no_accept
    ))

    sys.exit(exit_code)


if __name__ == '__main__':
    main()

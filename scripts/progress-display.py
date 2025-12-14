#!/usr/bin/env python3
"""
Progress bar display for parallel epic execution.
Parses the shared log file and renders visual progress bars.

Usage:
    python progress-display.py --log-file /tmp/epic-progress.log --stories "1-3,1-4,1-5"
"""

import argparse
import time
import sys
import os
from collections import defaultdict
from datetime import datetime

# Progress estimation based on typical tool patterns
TOOL_WEIGHTS = {
    'Read': 1,
    'Grep': 1,
    'Glob': 1,
    'Edit': 3,
    'Write': 3,
    'Bash': 5,
    'Task': 8,
}

# Typical story complexity (estimated tool calls)
ESTIMATED_TOOLS_PER_STORY = 25


def parse_log_line(line):
    """Parse a log line like: 14:32:01 [1-3] @ Edit: filename.py"""
    parts = line.strip().split(']', 1)
    if len(parts) != 2:
        return None

    prefix = parts[0]
    rest = parts[1].strip()

    # Extract story ID
    if '[' not in prefix:
        return None
    story_id = prefix.split('[')[-1]

    # Parse icon and message
    if not rest:
        return None
    icon = rest[0]
    message = rest[1:].strip() if len(rest) > 1 else ""

    return {
        'story_id': story_id,
        'icon': icon,
        'message': message
    }


def render_progress_bar(progress, width=30):
    """Render a progress bar like [████████░░░░░░░░░░░░]"""
    filled = int(progress * width)
    empty = width - filled
    return f"[{'█' * filled}{'░' * empty}]"


def clear_screen():
    """Clear terminal screen."""
    print('\033[2J\033[H', end='')


def render_dashboard(stories_state, elapsed_seconds, total_tools, total_files):
    """Render the full progress dashboard."""
    clear_screen()

    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║           PARALLEL EPIC EXECUTION - Live Progress                ║")
    print("╠══════════════════════════════════════════════════════════════════╣")
    print()

    for story_id, state in sorted(stories_state.items()):
        status = state.get('status', 'pending')
        tool_count = state.get('tool_count', 0)
        last_tool = state.get('last_tool', '')

        if status == 'complete':
            bar = render_progress_bar(1.0)
            suffix = f"✓ Complete ({tool_count} tools)"
        elif status == 'error':
            bar = render_progress_bar(state.get('progress', 0))
            suffix = f"✗ Error"
        else:
            progress = min(tool_count / ESTIMATED_TOOLS_PER_STORY, 0.95)
            bar = render_progress_bar(progress)
            pct = int(progress * 100)
            suffix = f"{pct}%  @ {last_tool}" if last_tool else f"{pct}%"

        name = state.get('name', story_id)
        print(f"  Story {story_id}: {name[:30]}")
        print(f"  {bar} {suffix}")
        print()

    print("╚══════════════════════════════════════════════════════════════════╝")

    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    print(f"  Elapsed: {minutes:02d}:{seconds:02d}  |  Tool Calls: {total_tools}  |  Files Changed: {total_files}")
    print()
    sys.stdout.flush()


def monitor_progress(log_file, story_ids, poll_interval=2):
    """Monitor log file and render progress dashboard."""
    stories_state = {
        sid: {'status': 'pending', 'tool_count': 0, 'last_tool': '', 'name': f'Story {sid}'}
        for sid in story_ids
    }

    start_time = time.time()
    last_position = 0
    total_tools = 0
    files_changed = set()

    try:
        while True:
            # Read new lines from log file
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    f.seek(last_position)
                    new_lines = f.readlines()
                    last_position = f.tell()

                for line in new_lines:
                    parsed = parse_log_line(line)
                    if not parsed:
                        continue

                    story_id = parsed['story_id']
                    icon = parsed['icon']
                    message = parsed['message']

                    if story_id not in stories_state:
                        continue

                    state = stories_state[story_id]

                    if icon == '>':
                        state['status'] = 'running'
                    elif icon == '@':
                        state['status'] = 'running'
                        state['tool_count'] += 1
                        state['last_tool'] = message[:40]
                        total_tools += 1

                        # Track file changes
                        if message.startswith(('Edit:', 'Write:')):
                            filename = message.split(':', 1)[1].strip()
                            files_changed.add(filename)
                    elif icon == '*':
                        state['status'] = 'complete'
                    elif icon == '!':
                        state['status'] = 'finished'
                    elif icon == 'X':
                        state['status'] = 'error'

            # Render dashboard
            elapsed = int(time.time() - start_time)
            render_dashboard(stories_state, elapsed, total_tools, len(files_changed))

            # Check if all complete
            all_done = all(
                s['status'] in ('complete', 'finished', 'error')
                for s in stories_state.values()
            )
            if all_done:
                print("┌──────────────────────────────────────────────────────────────────┐")
                print("│  ✓ ALL STORIES COMPLETE                                          │")
                print("└──────────────────────────────────────────────────────────────────┘")
                break

            time.sleep(poll_interval)

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")


def main():
    parser = argparse.ArgumentParser(description="Progress bar display for parallel epic execution")
    parser.add_argument('--log-file', '-l', required=True, help="Shared log file to monitor")
    parser.add_argument('--stories', '-s', required=True, help="Comma-separated story IDs")
    parser.add_argument('--poll', '-p', type=int, default=2, help="Poll interval in seconds")

    args = parser.parse_args()
    story_ids = [s.strip() for s in args.stories.split(',')]

    monitor_progress(args.log_file, story_ids, args.poll)


if __name__ == '__main__':
    main()

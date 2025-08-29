import argparse
import datetime

def get_formatted_date():
    """Returns the current date in YYYY-MM-DD format."""
    return datetime.datetime.now().strftime("%Y-%m-%d")

def format_activity_log(task_description, date):
    """Formats the log entry for ACTIVITY.md."""
    return f"""
---
## ACT-??? (TBD): {task_description}

**Date:** {date}
**Status:** 🚧 In Progress
**Assignee:** Jules

### Objective
(To be filled in)

### Outcome
- (To be filled in)

### Related Documents
- (To be filled in)
"""

def format_session_log(task_description, date):
    """Formats the log entry for SESSION_LOG.md."""
    return f"""
---
## LOG-ENTRY: {date}

**Task:** {task_description}
**Finding:** (To be filled in)
**Outcome:** (To be filled in)
"""

def format_current_state(task_description, date):
    """Formats the content for CURRENT_STATE.md."""
    return f"""
# Project State as of {date}

**Status:** Live Document

## 1. Session Summary & Accomplishments

- **Current Task:** {task_description}

## 2. Known Issues & Blockers

(To be filled in)

## 3. Pending Work: Next Immediate Steps

(To be filled in)
"""

def update_log_file(file_path, content, mode='a'):
    """Appends or overwrites a log file with new content."""
    try:
        with open(file_path, mode) as f:
            f.write(content)
        print(f"Successfully updated {file_path}")
    except IOError as e:
        print(f"Error updating {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Automate logging of work tasks.")
    parser.add_argument("--task", required=True, help="A clear, concise summary of the action taken.")
    args = parser.parse_args()

    task = args.task
    date = get_formatted_date()

    # For ACTIVITY.md and SESSION_LOG.md, we read the existing content and prepend the new entry.
    # This keeps the logs in reverse chronological order.

    # Update ACTIVITY.md
    activity_entry = format_activity_log(task, date)
    try:
        with open("project/logs/ACTIVITY.md", "r+") as f:
            original_content = f.read()
            f.seek(0)
            f.write(activity_entry.strip() + "\n\n" + original_content)
        print("Successfully updated project/logs/ACTIVITY.md")
    except IOError as e:
        print(f"Error updating project/logs/ACTIVITY.md: {e}")


    # Update SESSION_LOG.md
    session_entry = format_session_log(task, date)
    try:
        with open("project/logs/SESSION_LOG.md", "r+") as f:
            original_content = f.read()
            f.seek(0)
            f.write(session_entry.strip() + "\n\n" + original_content)
        print("Successfully updated project/logs/SESSION_LOG.md")
    except IOError as e:
        print(f"Error updating project/logs/SESSION_LOG.md: {e}")

    # Overwrite CURRENT_STATE.md
    state_content = format_current_state(task, date)
    update_log_file("project/logs/CURRENT_STATE.md", state_content.strip() + "\n", mode='w')


if __name__ == "__main__":
    main()

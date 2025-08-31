import argparse
import datetime
import textwrap

def get_formatted_date():
    """Returns the current date in YYYY-MM-DD format."""
    return datetime.datetime.now().strftime("%Y-%m-%d")

def format_activity_log(description):
    """Formats the log entry for ACTIVITY.md."""
    # ACT-??? is a placeholder for a proper ticket number if one exists.
    return textwrap.dedent(f"""
    ---
    ## ACT-???: {description}

    **Date:** {get_formatted_date()}
    **Status:** ✅ Done
    **Assignee:** Jules

    ### Outcome
    - (To be filled in manually)
    """)

def format_session_log(summary):
    """Formats the log entry for SESSION_LOG.md."""
    return textwrap.dedent(f"""
    ---
    ## Session Report: {get_formatted_date()}

    **Summary:** {summary}
    **Findings:**
    - (To be filled in manually)
    """)

def format_current_state(summary):
    """Formats the content for CURRENT_STATE.md."""
    return textwrap.dedent(f"""
    # Project State as of {get_formatted_date()}

    **Status:** Live Document

    ## 1. Session Summary & Accomplishments
    {summary}

    ## 2. Known Issues & Blockers
    - None

    ## 3. Pending Work: Next Immediate Steps
    - (To be filled in manually)
    """)

def prepend_to_file(file_path, content):
    """Prepends new content to the beginning of a file."""
    try:
        with open(file_path, "r+") as f:
            original_content = f.read()
            f.seek(0)
            f.write(content.strip() + "\n\n" + original_content)
        print(f"Successfully updated {file_path}")
    except IOError as e:
        print(f"Error updating {file_path}: {e}")

def write_to_file(file_path, content):
    """Writes content to a file, overwriting existing content."""
    try:
        with open(file_path, "w") as f:
            f.write(content.strip() + "\n")
        print(f"Successfully updated {file_path}")
    except IOError as e:
        print(f"Error updating {file_path}: {e}")


def main():
    """
    Main function to parse commit message and update log files.
    This script is intended to be used as a pre-commit hook.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath", help="Path to the commit message file.")
    args = parser.parse_args()

    try:
        with open(args.commit_msg_filepath, "r") as f:
            commit_message = f.read().strip()
    except IOError as e:
        print(f"Error reading commit message file: {e}", file=sys.stderr)
        sys.exit(1)

    # Ignore merge commits and other automated messages
    if not commit_message or commit_message.startswith("Merge"):
        print("Ignoring merge commit or empty message.")
        sys.exit(0)

    lines = commit_message.split('\n')
    activity_summary = lines[0]
    session_summary = commit_message
    state_summary = activity_summary # Use the first line for state as well

    # --- Update ACTIVITY.md ---
    activity_entry = format_activity_log(activity_summary)
    prepend_to_file("project/logs/ACTIVITY.md", activity_entry)

    # --- Update SESSION_LOG.md ---
    session_entry = format_session_log(session_summary)
    prepend_to_file("project/logs/SESSION_LOG.md", session_entry)

    # --- Overwrite CURRENT_STATE.md ---
    state_content = format_current_state(state_summary)
    write_to_file("project/logs/CURRENT_STATE.md", state_content)


if __name__ == "__main__":
    main()

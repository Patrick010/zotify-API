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

    ### Objective
    (To be filled in manually)

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
    parser = argparse.ArgumentParser(
        description="Automate logging of work tasks to the project's 'Trinity' logs.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--activity",
        required=True,
        help="A short, granular description of the specific task completed (for ACTIVITY.md)."
    )
    parser.add_argument(
        "--session",
        required=True,
        help="A higher-level summary of the session's outcome (for SESSION_LOG.md)."
    )
    parser.add_argument(
        "--state",
        required=True,
        help="A brief, one-sentence summary of the project's current state (for CURRENT_STATE.md)."
    )
    args = parser.parse_args()

    # --- Update ACTIVITY.md ---
    activity_entry = format_activity_log(args.activity)
    prepend_to_file("project/logs/ACTIVITY.md", activity_entry)

    # --- Update SESSION_LOG.md ---
    session_entry = format_session_log(args.session)
    prepend_to_file("project/logs/SESSION_LOG.md", session_entry)

    # --- Overwrite CURRENT_STATE.md ---
    state_content = format_current_state(args.state)
    write_to_file("project/logs/CURRENT_STATE.md", state_content)


if __name__ == "__main__":
    main()

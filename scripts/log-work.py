import argparse
import datetime
import re
import textwrap

def get_formatted_date():
    """Returns the current date in YYYY-MM-DD format."""
    return datetime.datetime.now().strftime("%Y-%m-%d")

def get_next_act_number(file_path="project/logs/ACTIVITY.md"):
    """Finds the latest ACT-XXX number in the activity log and returns the next number."""
    try:
        with open(file_path, "r") as f:
            content = f.read()
        act_numbers = re.findall(r"## ACT-(\d+):", content)
        if not act_numbers:
            return 1
        return max([int(n) for n in act_numbers]) + 1
    except FileNotFoundError:
        return 1

def format_activity_log(act_number, summary, objective, outcome, files=None):
    """Formats the log entry for ACTIVITY.md."""
    related_docs_section = ""
    if files:
        file_list = "\n".join([f"    - `{f}`" for f in files])
        related_docs_section = textwrap.dedent(f"""
        ### Related Documents
{file_list}
        """).strip()

    return textwrap.dedent(f"""
    ---
    ## ACT-{act_number:03d}: {summary}

    **Date:** {get_formatted_date()}
    **Status:** ✅ Done
    **Assignee:** Jules

    ### Objective
    {objective}

    ### Outcome
    {outcome}
    {related_docs_section}
    """).strip()

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
        description="Automate logging of work tasks to project/logs/ACTIVITY.md.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--summary",
        required=True,
        help="A one-line summary of the task, used as the entry title."
    )
    parser.add_argument(
        "--objective",
        required=True,
        help="A description of the task's objective."
    )
    parser.add_argument(
        "--outcome",
        required=True,
        help="A multi-line description of the outcome. Use '\\n' for new lines."
    )
    parser.add_argument(
        "--files",
        nargs='*',
        help="An optional list of file paths related to the activity."
    )
    args = parser.parse_args()

    # Determine the next ACT number
    act_number = get_next_act_number()

    # Format the new entry
    activity_entry = format_activity_log(act_number, args.summary, args.objective, args.outcome, args.files)

    # Prepend the new entry to the activity log
    prepend_to_file("project/logs/ACTIVITY.md", activity_entry)


if __name__ == "__main__":
    main()

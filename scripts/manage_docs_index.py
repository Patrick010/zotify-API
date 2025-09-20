import os
import re
import argparse
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
DOC_DIRS_TO_INDEX = ["api/docs", "snitch/docs", "Gonk/GonkUI/docs"]
DOCS_QUALITY_INDEX = PROJECT_ROOT / "api/docs/DOCS_QUALITY_INDEX.md"

# --- Main Functions ---

def get_all_markdown_files():
    """Scans the doc directories and returns a list of all .md files."""
    md_files = []
    for directory in DOC_DIRS_TO_INDEX:
        for root, _, files in os.walk(PROJECT_ROOT / directory):
            for file in files:
                if file.endswith(".md"):
                    # Store the path relative to the project root
                    md_files.append(Path(root) / file)
    return md_files

def get_indexed_docs():
    """Parses the DOCS_QUALITY_INDEX.md to find which files are already indexed."""
    indexed = set()
    if not DOCS_QUALITY_INDEX.is_file():
        return indexed

    with open(DOCS_QUALITY_INDEX, "r", encoding="utf-8") as f:
        # Skip header and separator
        f.readline()
        f.readline()
        for line in f:
            if not line.strip():
                continue
            try:
                # Path is in the second column
                path = line.split("|")[2].strip()
                indexed.add(path)
            except IndexError:
                continue
    return indexed

def add_to_docs_quality_index(doc_path):
    """Appends a new entry for a markdown file to the quality index."""
    # Use the filename as the module name for simplicity
    module_name = doc_path.stem.replace("_", " ").title()
    # Get path relative to project root
    relative_path = doc_path.relative_to(PROJECT_ROOT).as_posix()
    entry = f"| {module_name} | {relative_path} | X |\n"

    with open(DOCS_QUALITY_INDEX, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  - Added '{relative_path}' to {DOCS_QUALITY_INDEX.name}")

def main():
    """Main function to manage the documentation quality index."""
    parser = argparse.ArgumentParser(description="Manage the documentation quality index.")
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run the script to find and add missing markdown files to the index."
    )
    args = parser.parse_args()

    if not args.run:
        print("This script populates the DOCS_QUALITY_INDEX.md file.")
        print("Run with the --run flag to execute.")
        return

    print("--- Starting Docs Quality Indexer ---")

    all_md_files = get_all_markdown_files()
    indexed_docs = get_indexed_docs()

    new_entries_added = 0

    for md_path in all_md_files:
        relative_path_str = md_path.relative_to(PROJECT_ROOT).as_posix()
        if relative_path_str not in indexed_docs:
            new_entries_added += 1
            print(f"\nFound un-indexed doc file: {relative_path_str}")
            add_to_docs_quality_index(md_path)

    if new_entries_added == 0:
        print("\nNo new markdown files to index. Everything is up to date.")
    else:
        print(f"\nSuccessfully added {new_entries_added} new file(s) to the index.")

    print("--- Indexer Finished ---")

if __name__ == "__main__":
    main()

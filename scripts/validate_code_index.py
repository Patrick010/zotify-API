import os
from pathlib import Path
import sys

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
CODE_INDEX_PATH = PROJECT_ROOT / "api/docs/CODE_FILE_INDEX.md"
DIRS_TO_SCAN = [
    PROJECT_ROOT / "api/src/zotify_api",
    PROJECT_ROOT / "scripts",
    PROJECT_ROOT / "api/tests",
    PROJECT_ROOT / "Gonk",
    PROJECT_ROOT / "snitch",
]
FILE_EXTENSIONS = {".py", ".go", ".js"}


def get_indexed_files(index_path: Path) -> set[str]:
    """Parses the code index markdown file and returns a set of file paths."""
    if not index_path.exists():
        print(f"Error: Code index file not found at {index_path}", file=sys.stderr)
        sys.exit(1)

    indexed_files = set()
    with open(index_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip().startswith("|"):
                continue
            if "---" in line or "Path" in line:
                continue

            parts = [p.strip().strip("`") for p in line.split("|")]
            if len(parts) > 1 and parts[1]:
                # Convert to relative path from project root
                indexed_files.add(parts[1])
    return indexed_files


def get_actual_files(directories: list[Path], extensions: set[str]) -> set[str]:
    """Walks the given directories and returns a set of actual file paths."""
    actual_files = set()
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if Path(file).suffix in extensions:
                    full_path = Path(root) / file
                    # Make path relative to project root for comparison
                    relative_path = str(full_path.relative_to(PROJECT_ROOT))
                    actual_files.add(relative_path)
    return actual_files


def main() -> int:
    """Main function to compare indexed files vs. actual files."""
    print("--- Running Code File Index Validator ---")
    indexed_files = get_indexed_files(CODE_INDEX_PATH)
    actual_files = get_actual_files(DIRS_TO_SCAN, FILE_EXTENSIONS)

    # Ignore __init__.py files as they are for packaging, not standalone code logic
    actual_files = {f for f in actual_files if not f.endswith("__init__.py")}
    indexed_files = {f for f in indexed_files if not f.endswith("__init__.py")}

    unindexed_files = actual_files - indexed_files
    stale_index_entries = indexed_files - actual_files

    if not unindexed_files and not stale_index_entries:
        print("✅ Success: Code file index is up-to-date.")
        return 0

    if unindexed_files:
        print("\n❌ Error: The following code files are present in the repository but not in the index:", file=sys.stderr)
        for file in sorted(list(unindexed_files)):
            print(f"- {file}", file=sys.stderr)

    if stale_index_entries:
        print("\n❌ Error: The following files are in the index but do not exist in the repository:", file=sys.stderr)
        for file in sorted(list(stale_index_entries)):
            print(f"- {file}", file=sys.stderr)

    print("\nPlease update api/docs/CODE_FILE_INDEX.md to match the repository.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

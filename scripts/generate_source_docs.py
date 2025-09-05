import os
import re
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_DIRS = ["api/src", "snitch", "gonk-testUI", "scripts"]
SOURCE_EXTENSIONS = [".py", ".go", ".js"]
DOC_DIR = PROJECT_ROOT / "api/docs/reference/source"
MASTER_INDEX = PROJECT_ROOT / "api/docs/MASTER_INDEX.md"
DOCS_QUALITY_INDEX = PROJECT_ROOT / "api/docs/DOCS_QUALITY_INDEX.md"

STUB_TEMPLATE = """
# {module_name}

## 1. Role / Purpose
- (To be filled in)

## 2. Key Functions
- (To be filled in)

## 3. Place within Project Architecture
- (To be filled in)

## 4. Code Examples
```
// (Add code examples here)
```

## 5. Dependencies
- (To be filled in)
"""

def get_all_source_files():
    """Scans the source directories and returns a list of all source files."""
    source_files = []
    for directory in SOURCE_DIRS:
        for root, _, files in os.walk(PROJECT_ROOT / directory):
            for file in files:
                if any(file.endswith(ext) for ext in SOURCE_EXTENSIONS):
                    source_files.append(Path(root) / file)
    return source_files

def get_documented_files():
    """Parses the MASTER_INDEX.md to find which source files are already documented."""
    documented = set()
    if not MASTER_INDEX.is_file():
        return documented

    with open(MASTER_INDEX, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find links like (reference/source/CRUD.py.md)
    matches = re.findall(r"\(reference/source/([^)]+\.md)\)", content)
    for match in matches:
        documented.add(match)
    return documented

def create_stub_file(module_name, doc_path):
    """Creates a new markdown stub file for a source module."""
    content = STUB_TEMPLATE.format(module_name=module_name)
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"  - Created stub file: {doc_path.relative_to(PROJECT_ROOT)}")

def add_to_master_index(module_name, doc_filename):
    """Appends a new entry to the MASTER_INDEX.md file."""
    # Format the module name for the link text, e.g., "CRUD.py" -> "CRUD Module"
    link_text = module_name.replace('.py', '').replace('.go', '').replace('.js', '').replace('_', ' ').title() + " Module"
    entry = f"* [{link_text}](reference/source/{doc_filename})\n"

    with open(MASTER_INDEX, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  - Added '{link_text}' to {MASTER_INDEX.name}")

def add_to_docs_quality_index(module_name, doc_filename):
    """Appends a new entry to the DOCS_QUALITY_INDEX.md file."""
    # Format the module name, e.g., "CRUD.py" -> "CRUD"
    module_text = module_name.replace('.py', '').replace('.go', '').replace('.js', '').title()
    entry = f"| {module_text} | {doc_filename} | X |\n"

    with open(DOCS_QUALITY_INDEX, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  - Added '{module_text}' to {DOCS_QUALITY_INDEX.name}")

def main():
    """Main function to generate documentation stubs."""
    print("--- Starting Source Documentation Stub Generator ---")

    if not DOC_DIR.exists():
        print(f"Creating documentation directory: {DOC_DIR}")
        DOC_DIR.mkdir(parents=True)

    source_files = get_all_source_files()
    documented_files = get_documented_files()

    new_stubs_created = 0

    for src_path in source_files:
        # Generate the expected doc filename, e.g., "crud.py" -> "CRUD.py.md"
        doc_filename = src_path.name.upper() + ".md"

        if doc_filename not in documented_files:
            new_stubs_created += 1
            print(f"\nFound undocumented source file: {src_path.name}")
            module_name = src_path.name
            doc_path = DOC_DIR / doc_filename

            create_stub_file(module_name, doc_path)
            add_to_master_index(module_name, doc_filename)
            add_to_docs_quality_index(module_name, doc_filename)

    if new_stubs_created == 0:
        print("\nNo new source files to document. Everything is up to date.")
    else:
        print(f"\nSuccessfully created {new_stubs_created} new documentation stub(s).")

    print("--- Stub Generator Finished ---")

if __name__ == "__main__":
    main()

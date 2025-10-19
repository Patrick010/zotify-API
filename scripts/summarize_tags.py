#!/usr/bin/env python3
"""
summarize_tags.py

Tag generator for repo_inventory_and_governance.py.
Generates meaningful tags from a text description (doc or code).
"""

import re

# Project-specific ID patterns
PROJECT_ID_PATTERNS = [
    r"\bapi-\d+\b",
    r"\bar-\d+\b",
    r"\bdoc-\d+\b",
    r"\bos-\d+\b",
]

# Special symbols to preserve
SPECIAL_SYMBOLS = {"*", "#", ":*"}

# Default number of tags to display in test runs
DEFAULT_TAG_COUNT = 15

def generate_tags_from_text(text: str) -> list[str]:
    """
    Generate tags from a given text string (description).
    """
    tags = []

    # Extract project IDs
    for pattern in PROJECT_ID_PATTERNS:
        tags.extend(re.findall(pattern, text))

    # Extract special symbols
    for sym in SPECIAL_SYMBOLS:
        if sym in text:
            tags.append(sym)

    # Extract words: letters, numbers, underscores, hyphens
    words = re.findall(r"\b[\w\-]+\b", text)
    tags.extend(words)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for t in tags:
        if t not in seen:
            deduped.append(t)
            seen.add(t)
    return deduped

extract_tags = generate_tags_from_text

def test_run():
    """
    Test run with example texts.
    """
    example_docs = [
        "This document specifies API endpoints for the Zotify service.",
        "Project guidelines for code reviews and documentation standards."
    ]
    example_code = [
        "def add(a, b): return a + b",
        "class ZotifyAPI: handles authentication and media download"
    ]
    for i, text in enumerate(example_docs + example_code):
        tags = generate_tags_from_text(text)
        print(f"\n--- TAGS for example {i+1} ---")
        print(tags[:DEFAULT_TAG_COUNT])

if __name__ == "__main__":
    test_run()


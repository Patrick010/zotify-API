import sys
from pathlib import Path
import os
import pytest
from unittest.mock import patch, MagicMock

# Add scripts directory to path to allow importing linter
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

import linter

@pytest.fixture
def temp_log_file(tmp_path):
    """Create a temporary log file for testing."""
    return tmp_path / "test_log.md"

def test_prepend_to_file_with_id(temp_log_file):
    """
    Verify that prepend_to_file correctly preserves the ID line.
    """
    # 1. Create initial file with an ID and some content
    initial_content = "<!-- ID: DOC-123 -->\n\n---\n\nOld entry."
    temp_log_file.write_text(initial_content, encoding="utf-8")

    # 2. Prepend a new entry
    new_entry = "---\n\nNew entry."
    linter.prepend_to_file(temp_log_file, new_entry)

    # 3. Verify the final content
    final_content = temp_log_file.read_text(encoding="utf-8")
    lines = [line.strip() for line in final_content.strip().split('\n') if line.strip()]

    assert "<!-- ID: DOC-123 -->" in lines[0]
    assert "---" in lines[1]
    assert "New entry." in lines[2]
    assert "---" in lines[3]
    assert "Old entry." in lines[4]

def test_prepend_to_file_without_id(temp_log_file):
    """
    Verify that prepend_to_file works correctly on a file without an ID.
    """
    # 1. Create initial file without an ID
    initial_content = "---\n\nOld entry."
    temp_log_file.write_text(initial_content, encoding="utf-8")

    # 2. Prepend a new entry
    new_entry = "---\n\nNew entry."
    linter.prepend_to_file(temp_log_file, new_entry)

    # 3. Verify the final content
    final_content = temp_log_file.read_text(encoding="utf-8")
    lines = [line.strip() for line in final_content.strip().split('\n') if line.strip()]

    assert "---" in lines[0]
    assert "New entry." in lines[1]

def test_file_content_rule_fail(tmp_path):
    """
    Verify that the file content rule correctly fails when an ID is not on the first line.
    """
    # 1. Create a mock rules file
    rules_content = """
file_content_rules:
  - name: "Enforce Document ID on First Line"
    include_paths: [".md"]
    must_start_with: "<!-- ID:"
    message: "ID must be on the first line."
"""
    rules_file = tmp_path / "doc-lint-rules.yml"
    rules_file.write_text(rules_content)

    # 2. Create a malformed markdown file
    md_content = "\n<!-- ID: BAD-ID -->"
    md_file = tmp_path / "bad_file.md"
    md_file.write_text(md_content)

    # 3. Patch the linter's rule path and run the check
    with patch('linter.DOC_LINT_RULES', rules_file):
        errors = linter.check_file_content_rules({str(md_file)})

    # 4. Assert that an error was returned
    assert len(errors) == 1
    assert "ID must be on the first line" in errors[0]

def test_prepend_to_new_file(temp_log_file):
    """
    Verify that prepend_to_file works correctly when the file doesn't exist yet.
    """
    # 1. Prepend an entry to a non-existent file
    new_entry = "---\n\nNew entry."
    linter.prepend_to_file(temp_log_file, new_entry)

    # 2. Verify the final content
    final_content = temp_log_file.read_text(encoding="utf-8")
    lines = [line.strip() for line in final_content.strip().split('\n') if line.strip()]

    assert "---" in lines[0]
    assert "New entry." in lines[1]

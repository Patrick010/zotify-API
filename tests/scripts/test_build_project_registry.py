#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for the build_project_registry script.
"""
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

# Ensure the script's parent directory is on the Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from scripts import build_project_registry


class TestBuildProjectRegistry(unittest.TestCase):
    """Tests for the build_project_registry script."""

    def setUp(self):
        self.tmpdir = TemporaryDirectory()
        self.repo_root = Path(self.tmpdir.name).resolve()

        self.project_dir = self.repo_root / "project"
        (self.project_dir / "reports").mkdir(parents=True, exist_ok=True)

        self.trace_index_path = self.project_dir / "reports" / "TRACE_INDEX.yml"
        self.registry_md_path = self.project_dir / "PROJECT_REGISTRY.md"

        scripts_dir = self.repo_root / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        self.extras_path = scripts_dir / "project_registry_extras.yml"
        self.output_json_path = scripts_dir / "project_registry.json"

        self.orphan_file_path = self.project_dir / "orphan_file.md"
        self.orphan_file_path.touch()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_end_to_end_logic(self):
        """Test the full registry generation logic from mock files."""
        trace_content = """
artifacts:
  - path: project/reports/report.md
    type: doc
    registered: true
    exists_on_disk: true
  - path: project/missing_doc.md
    type: doc
    registered: true
    exists_on_disk: false
  - path: api/docs/some_api_doc.md
    type: doc
    registered: true
  - path: api/docs/CODE_FILE_INDEX.md
    type: doc
    registered: true
"""
        self.trace_index_path.write_text(trace_content)
        (self.project_dir / "reports" / "report.md").touch()
        (self.repo_root / "api" / "docs").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "api" / "docs" / "CODE_FILE_INDEX.md").touch()

        legacy_md_content = "| [Old Report](./old_report.md) | An old report |"
        self.registry_md_path.write_text(legacy_md_content)
        (self.project_dir / "old_report.md").touch()

        extras_content = 'include:\n  - "docs/extra_doc.md"'
        self.extras_path.write_text(extras_content)

        registry = build_project_registry.build_registry(
            self.trace_index_path, self.registry_md_path, self.extras_path,
            self.output_json_path, self.project_dir, self.repo_root
        )

        status_map = {item["path"]: item["status"] for item in registry}
        self.assertEqual(status_map.get("project/reports/report.md"), "registered")
        self.assertEqual(status_map.get("project/missing_doc.md"), "missing")
        self.assertEqual(status_map.get("project/orphan_file.md"), "orphan")
        self.assertEqual(status_map.get("project/old_report.md"), "orphan")
        self.assertEqual(status_map.get("docs/extra_doc.md"), "missing")
        self.assertEqual(status_map.get("api/docs/CODE_FILE_INDEX.md"), "registered")

    def test_filtering_excludes_api_docs(self):
        """Verify that api/docs are excluded, except for CODE_FILE_INDEX.md."""
        trace_content = """
artifacts:
  - { path: project/reports/a.md, type: doc, registered: true }
  - { path: api/docs/b.md, type: doc, registered: true }
  - { path: api/docs/CODE_FILE_INDEX.md, type: doc, registered: true }
"""
        self.trace_index_path.write_text(trace_content)
        (self.project_dir / "reports" / "a.md").touch()
        (self.repo_root / "api" / "docs").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "api" / "docs" / "b.md").touch()
        (self.repo_root / "api" / "docs" / "CODE_FILE_INDEX.md").touch()

        registry = build_project_registry.build_registry(
            self.trace_index_path, self.registry_md_path, self.extras_path,
            self.output_json_path, self.project_dir, self.repo_root
        )

        paths = {item['path'] for item in registry}
        self.assertIn('project/reports/a.md', paths)
        self.assertIn('api/docs/CODE_FILE_INDEX.md', paths)
        self.assertNotIn('api/docs/b.md', paths)

    def test_legacy_entry_preservation(self):
        """Test that legacy entries from markdown are preserved correctly."""
        self.trace_index_path.write_text("artifacts: []")

        legacy_md_content = "| [My Legacy Doc](./legacy.md) | Some notes |"
        self.registry_md_path.write_text(legacy_md_content)

        registry = build_project_registry.build_registry(
            self.trace_index_path, self.registry_md_path, self.extras_path,
            self.output_json_path, self.project_dir, self.repo_root
        )

        legacy_entry = next((item for item in registry if item["status"] == "legacy"), None)
        self.assertIsNotNone(legacy_entry)
        self.assertEqual(legacy_entry["name"], "My Legacy Doc")
        self.assertEqual(legacy_entry["source"], "project/PROJECT_REGISTRY.md")

    def test_idempotency(self):
        """Test that files are not rewritten if content is unchanged."""
        self.trace_index_path.write_text("artifacts: []")
        self.registry_md_path.touch()

        build_project_registry.build_registry(
            self.trace_index_path, self.registry_md_path, self.extras_path,
            self.output_json_path, self.project_dir, self.repo_root
        )
        initial_mtime = self.output_json_path.stat().st_mtime

        build_project_registry.build_registry(
            self.trace_index_path, self.registry_md_path, self.extras_path,
            self.output_json_path, self.project_dir, self.repo_root
        )
        second_mtime = self.output_json_path.stat().st_mtime

        self.assertEqual(initial_mtime, second_mtime)


if __name__ == "__main__":
    unittest.main()
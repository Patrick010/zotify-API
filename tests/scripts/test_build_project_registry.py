# ID: TEST-002
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for the corrected build_project_registry script.
"""
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import os

# Ensure the script's parent directory is on the Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from scripts import build_project_registry


class TestCorrectedBuildProjectRegistry(unittest.TestCase):
    """Tests for the corrected build_project_registry script that uses TRACE_INDEX.yml for descriptions."""

    def setUp(self):
        self.tmpdir = TemporaryDirectory()
        self.repo_root = Path(self.tmpdir.name).resolve()

        # Set up the directory structure the script expects
        self.scripts_dir = self.repo_root / "scripts"
        self.scripts_dir.mkdir(parents=True, exist_ok=True)

        self.project_dir = self.repo_root / "project"
        self.reports_dir = self.project_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        # Set the paths for the script's constants
        build_project_registry.TRACE_INDEX_PATH = self.reports_dir / "TRACE_INDEX.yml"
        build_project_registry.OUTPUT_JSON = self.scripts_dir / "project_registry.json"
        build_project_registry.OUTPUT_MD = self.project_dir / "PROJECT_REGISTRY.md"

        # Create some dummy files to be referenced
        (self.project_dir / "proposals").mkdir(parents=True, exist_ok=True)
        (self.project_dir / "proposals" / "NEW_PROPOSAL.md").touch()
        (self.project_dir / "proposals" / "QA_GATE_IMPLEMENTATION_PLAN.md").touch()
        (self.repo_root / "api" / "docs").mkdir(parents=True, exist_ok=True)
        (self.repo_root / "api" / "docs" / "some_api_doc.md").touch() # This should be ignored

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_registry_generation_uses_trace_index_descriptions(self):
        """
        Test that the registry generation logic correctly pulls descriptions
        from the mock TRACE_INDEX.yml, not a hardcoded map.
        """
        trace_content = """
artifacts:
  - path: project/proposals/NEW_PROPOSAL.md
    meta:
      description: "This is the correct description from TRACE_INDEX."
  - path: project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md
    meta:
      description: "This is also the correct description."
  - path: api/docs/some_api_doc.md
    meta:
      description: "This description for a non-project file should be ignored."
  - path: project/proposals/MISSING_FILE.md
    meta:
      description: "A file that does not exist on disk"
"""
        build_project_registry.TRACE_INDEX_PATH.write_text(trace_content)

        # Run the main function of the script, patching sys.argv
        with unittest.mock.patch.object(sys, 'argv', ['build_project_registry.py', '--repo-root', str(self.repo_root)]):
            build_project_registry.main()

        # --- Validate JSON Output ---
        self.assertTrue(build_project_registry.OUTPUT_JSON.exists())
        with open(build_project_registry.OUTPUT_JSON, "r") as f:
            registry_data = json.load(f)

        self.assertEqual(len(registry_data), 4) # Two existing files, one missing, one ignored

        status_map = {item["path"]: item["status"] for item in registry_data}
        notes_map = {item["path"]: item["notes"] for item in registry_data}

        # Check that only project files are included
        self.assertIn("project/proposals/NEW_PROPOSAL.md", status_map)
        self.assertNotIn("api/docs/some_api_doc.md", status_map)

        # Check statuses
        self.assertEqual(status_map["project/proposals/NEW_PROPOSAL.md"], "registered")
        self.assertEqual(status_map["project/proposals/MISSING_FILE.md"], "missing")

        # Check that descriptions now come from the mock TRACE_INDEX.yml
        self.assertEqual(notes_map["project/proposals/NEW_PROPOSAL.md"], "This is the correct description from TRACE_INDEX.")
        self.assertEqual(notes_map["project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md"], "This is also the correct description.")

        # --- Validate Markdown Output ---
        self.assertTrue(build_project_registry.OUTPUT_MD.exists())
        md_content = build_project_registry.OUTPUT_MD.read_text()

        self.assertIn("`project/proposals/NEW_PROPOSAL.md`", md_content)
        self.assertIn("This is the correct description from TRACE_INDEX.", md_content)
        self.assertIn("`project/proposals/MISSING_FILE.md`", md_content)
        self.assertIn("| missing |", md_content)
        self.assertNotIn("api/docs/some_api_doc.md", md_content)

if __name__ == "__main__":
    unittest.main()
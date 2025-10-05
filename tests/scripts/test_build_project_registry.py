#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for the simplified build_project_registry script.
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


class TestSimplifiedBuildProjectRegistry(unittest.TestCase):
    """Tests for the new, simplified build_project_registry script."""

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

    def test_registry_generation_with_descriptions(self):
        """
        Test the full registry generation logic from a mock TRACE_INDEX.yml
        to ensure it correctly enriches entries with descriptions.
        """
        trace_content = """
artifacts:
  - path: project/proposals/NEW_PROPOSAL.md
    description: "Old placeholder description"
  - path: project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md
    description: "Another placeholder"
  - path: api/docs/some_api_doc.md
    description: "This should be ignored"
  - path: project/proposals/MISSING_FILE.md
    description: "A file that does not exist on disk"
"""
        build_project_registry.TRACE_INDEX_PATH.write_text(trace_content)

        # Run the main function of the script
        build_project_registry.main()

        # --- Validate JSON Output ---
        self.assertTrue(build_project_registry.OUTPUT_JSON.exists())
        with open(build_project_registry.OUTPUT_JSON, "r") as f:
            registry_data = json.load(f)

        self.assertEqual(len(registry_data), 3) # Two existing files, one missing

        status_map = {item["path"]: item["status"] for item in registry_data}
        desc_map = {item["path"]: item["description"] for item in registry_data}

        # Check that only project files are included
        self.assertIn("project/proposals/NEW_PROPOSAL.md", status_map)
        self.assertNotIn("api/docs/some_api_doc.md", status_map)

        # Check statuses
        self.assertEqual(status_map["project/proposals/NEW_PROPOSAL.md"], "registered")
        self.assertEqual(status_map["project/proposals/MISSING_FILE.md"], "missing")

        # Check that descriptions from METADATA_MAP are used
        self.assertEqual(desc_map["project/proposals/NEW_PROPOSAL.md"], "A template for creating new project proposals.")
        self.assertEqual(desc_map["project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md"], "A phased implementation plan for the new QA Gate system.")

        # --- Validate Markdown Output ---
        self.assertTrue(build_project_registry.OUTPUT_MD.exists())
        md_content = build_project_registry.OUTPUT_MD.read_text()

        self.assertIn("`project/proposals/NEW_PROPOSAL.md`", md_content)
        self.assertIn("A template for creating new project proposals.", md_content)
        self.assertIn("`project/proposals/MISSING_FILE.md`", md_content)
        self.assertIn("| missing |", md_content)
        self.assertNotIn("api/docs/some_api_doc.md", md_content)

if __name__ == "__main__":
    unittest.main()
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Unit tests for merge-config.py."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml

from importlib.util import spec_from_file_location, module_from_spec

# Import merge_config module
_spec = spec_from_file_location(
    "merge_config",
    str(Path(__file__).parent.parent / "merge-config.py"),
)
merge_config_mod = module_from_spec(_spec)
_spec.loader.exec_module(merge_config_mod)

extract_module_metadata = merge_config_mod.extract_module_metadata
merge_config = merge_config_mod.merge_config


SAMPLE_MODULE_YAML = {
    "code": "bmb",
    "name": "BMad Builder",
    "description": "Standard Skill Compliant Factory",
    "default_selected": False,
    "bmad_builder_output_folder": {
        "prompt": "Where should skills be saved?",
        "default": "_bmad-output/skills",
        "result": "{project-root}/{value}",
    },
    "bmad_builder_reports": {
        "prompt": "Output for reports?",
        "default": "_bmad-output/reports",
        "result": "{project-root}/{value}",
    },
}


class TestExtractModuleMetadata(unittest.TestCase):
    def test_extracts_metadata_fields(self):
        result = extract_module_metadata(SAMPLE_MODULE_YAML)
        self.assertEqual(result["name"], "BMad Builder")
        self.assertEqual(result["description"], "Standard Skill Compliant Factory")
        self.assertFalse(result["default_selected"])

    def test_excludes_variable_definitions(self):
        result = extract_module_metadata(SAMPLE_MODULE_YAML)
        self.assertNotIn("bmad_builder_output_folder", result)
        self.assertNotIn("bmad_builder_reports", result)
        self.assertNotIn("code", result)


class TestMergeConfig(unittest.TestCase):
    def test_fresh_install_with_core_and_module(self):
        answers = {
            "core": {
                "user_name": "Brian",
                "communication_language": "English",
            },
            "module": {
                "bmad_builder_output_folder": "_bmad-output/skills",
            },
        }
        result = merge_config({}, SAMPLE_MODULE_YAML, answers)

        self.assertEqual(result["core"]["user_name"], "Brian")
        self.assertEqual(result["bmb"]["name"], "BMad Builder")
        self.assertEqual(result["bmb"]["bmad_builder_output_folder"], "_bmad-output/skills")

    def test_update_preserves_core(self):
        existing = {
            "core": {"user_name": "Brian", "communication_language": "English"},
            "other_module": {"name": "Other"},
        }
        answers = {
            "module": {
                "bmad_builder_output_folder": "_bmad-output/skills",
            },
        }
        result = merge_config(existing, SAMPLE_MODULE_YAML, answers)

        # Core preserved
        self.assertEqual(result["core"]["user_name"], "Brian")
        # Other module preserved
        self.assertIn("other_module", result)
        # New module added
        self.assertIn("bmb", result)

    def test_anti_zombie_removes_existing_module(self):
        existing = {
            "core": {"user_name": "Brian"},
            "bmb": {
                "name": "BMad Builder",
                "old_variable": "should_be_removed",
                "bmad_builder_output_folder": "old/path",
            },
        }
        answers = {
            "module": {
                "bmad_builder_output_folder": "new/path",
            },
        }
        result = merge_config(existing, SAMPLE_MODULE_YAML, answers)

        # Old variable is gone
        self.assertNotIn("old_variable", result["bmb"])
        # New value is present
        self.assertEqual(result["bmb"]["bmad_builder_output_folder"], "new/path")
        # Metadata is fresh from module.yaml
        self.assertEqual(result["bmb"]["name"], "BMad Builder")

    def test_core_answers_override_existing(self):
        existing = {
            "core": {"user_name": "OldName", "communication_language": "Spanish"},
        }
        answers = {
            "core": {"user_name": "NewName", "communication_language": "English"},
            "module": {},
        }
        result = merge_config(existing, SAMPLE_MODULE_YAML, answers)

        self.assertEqual(result["core"]["user_name"], "NewName")
        self.assertEqual(result["core"]["communication_language"], "English")

    def test_no_core_answers_skips_core(self):
        existing = {
            "core": {"user_name": "Brian"},
        }
        answers = {
            "module": {"bmad_builder_output_folder": "path"},
        }
        result = merge_config(existing, SAMPLE_MODULE_YAML, answers)

        # Core unchanged
        self.assertEqual(result["core"]["user_name"], "Brian")

    def test_module_metadata_always_from_yaml(self):
        """Module metadata comes from module.yaml, not answers."""
        answers = {
            "module": {"bmad_builder_output_folder": "path"},
        }
        result = merge_config({}, SAMPLE_MODULE_YAML, answers)

        self.assertEqual(result["bmb"]["name"], "BMad Builder")
        self.assertEqual(result["bmb"]["description"], "Standard Skill Compliant Factory")
        self.assertFalse(result["bmb"]["default_selected"])


class TestEndToEnd(unittest.TestCase):
    def test_write_and_read_round_trip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "_bmad", "config.yaml")
            answers_path = os.path.join(tmpdir, "answers.json")
            module_path = os.path.join(tmpdir, "module.yaml")

            # Write module.yaml
            with open(module_path, "w") as f:
                yaml.dump(SAMPLE_MODULE_YAML, f)

            # Write answers
            answers = {
                "core": {"user_name": "Brian", "communication_language": "English"},
                "module": {"bmad_builder_output_folder": "_bmad-output/skills"},
            }
            with open(answers_path, "w") as f:
                json.dump(answers, f)

            # Run merge
            result = merge_config({}, SAMPLE_MODULE_YAML, answers)
            merge_config_mod.write_config(result, config_path)

            # Read back
            with open(config_path, "r") as f:
                written = yaml.safe_load(f)

            self.assertEqual(written["core"]["user_name"], "Brian")
            self.assertEqual(written["bmb"]["bmad_builder_output_folder"], "_bmad-output/skills")

    def test_update_round_trip(self):
        """Simulate install, then re-install with different values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "config.yaml")

            # First install
            answers1 = {
                "core": {"user_name": "Brian"},
                "module": {"bmad_builder_output_folder": "old/path"},
            }
            result1 = merge_config({}, SAMPLE_MODULE_YAML, answers1)
            merge_config_mod.write_config(result1, config_path)

            # Second install (update)
            existing = merge_config_mod.load_yaml_file(config_path)
            answers2 = {
                "module": {"bmad_builder_output_folder": "new/path"},
            }
            result2 = merge_config(existing, SAMPLE_MODULE_YAML, answers2)
            merge_config_mod.write_config(result2, config_path)

            # Verify
            with open(config_path, "r") as f:
                final = yaml.safe_load(f)

            self.assertEqual(final["core"]["user_name"], "Brian")
            self.assertEqual(final["bmb"]["bmad_builder_output_folder"], "new/path")


if __name__ == "__main__":
    unittest.main()

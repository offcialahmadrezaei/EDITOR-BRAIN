"""Validation tests for EDITOR BRAIN Edit Plan Schema v0.1.

Run from the repository root:
    python -m pip install -r requirements-dev.txt
    python -m unittest discover -s tests -v
"""

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "edit-plan.schema.json"
EXAMPLES_DIR = ROOT / "examples"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


class EditPlanSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load_json(SCHEMA_PATH)
        cls.validator = Draft202012Validator(cls.schema)

    def test_schema_is_valid(self):
        Draft202012Validator.check_schema(self.schema)

    def test_minimal_example_is_valid(self):
        plan = load_json(EXAMPLES_DIR / "minimal-edit-plan.json")
        errors = list(self.validator.iter_errors(plan))
        self.assertEqual(
            errors, [],
            msg="; ".join(error.message for error in errors)
        )

    def test_basic_video_edit_example_is_valid(self):
        plan = load_json(EXAMPLES_DIR / "basic-video-edit.json")
        errors = list(self.validator.iter_errors(plan))
        self.assertEqual(
            errors, [],
            msg="; ".join(error.message for error in errors)
        )

    def test_invalid_schema_version_is_rejected(self):
        plan = load_json(EXAMPLES_DIR / "minimal-edit-plan.json")
        plan["schema_version"] = "99.0"
        self.assertFalse(self.validator.is_valid(plan))

    def test_missing_required_output_is_rejected(self):
        plan = load_json(EXAMPLES_DIR / "minimal-edit-plan.json")
        del plan["output"]
        self.assertFalse(self.validator.is_valid(plan))

    def test_unknown_top_level_property_is_rejected(self):
        plan = load_json(EXAMPLES_DIR / "minimal-edit-plan.json")
        plan["unexpected_field"] = True
        self.assertFalse(self.validator.is_valid(plan))


if __name__ == "__main__":
    unittest.main()

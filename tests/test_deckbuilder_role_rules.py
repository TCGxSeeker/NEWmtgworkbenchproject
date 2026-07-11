from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mtg_workbench.deckbuilder.role_rules import (
    RoleRulesError,
    RoleRuleSet,
    load_role_rules,
    normalize_match_text,
    normalize_role_key,
)


ROLE_RULES_FIXTURE = Path("data/fixtures/roles/role_rules.example.yaml")


class RoleRulesTests(unittest.TestCase):
    def test_loads_role_rules_fixture(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)

        self.assertEqual(ruleset.schema_version, 1)
        self.assertEqual(ruleset.source, "role_rules_v0_example")
        self.assertEqual(len(ruleset.roles), 14)
        self.assertIsNotNone(ruleset.ui_visibility)
        self.assertIn("machine_evidence", ruleset.ui_visibility["output_fields"])

    def test_loads_initial_role_names(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        role_names = {role.canonical_role for role in ruleset.roles}

        self.assertIn("Land", role_names)
        self.assertIn("Ramp", role_names)
        self.assertIn("Draw", role_names)
        self.assertIn("Wincon", role_names)

    def test_get_role_accepts_role_id_or_canonical_name(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)

        self.assertEqual(ruleset.get_role("ramp").canonical_role, "Ramp")
        self.assertEqual(ruleset.get_role("Board   Wipe").role_id, "board_wipe")
        self.assertIsNone(ruleset.get_role("not a role"))

    def test_normalize_match_text_casefolds_trims_and_collapses_spaces(self) -> None:
        self.assertEqual(normalize_match_text("  Draw    A Card "), "draw a card")
        self.assertEqual(normalize_role_key("  Board   Wipe "), "board wipe")

    def test_from_dict_validates_schema_version(self) -> None:
        with self.assertRaises(RoleRulesError) as context:
            RoleRuleSet.from_dict(
                {
                    "schema_version": 999,
                    "evidence_score_bands": [{"score": 0, "meaning": "none"}],
                    "roles": [
                        {
                            "role_id": "ramp",
                            "canonical_role": "Ramp",
                            "evidence_rules": {"oracle_text_phrases": [{"phrase": "add", "score": 75}]},
                            "exclusion_rules": [],
                            "score_policy": {"combine": "highest_match", "default_score": 0, "max_score": 100},
                        }
                    ],
                }
            )

        self.assertIn("Unsupported role rules schema_version", str(context.exception))

    def test_from_dict_validates_duplicate_role_ids(self) -> None:
        role = {
            "role_id": "ramp",
            "canonical_role": "Ramp",
            "evidence_rules": {"oracle_text_phrases": [{"phrase": "add", "score": 75}]},
            "exclusion_rules": [],
            "score_policy": {"combine": "highest_match", "default_score": 0, "max_score": 100},
        }

        with self.assertRaises(RoleRulesError) as context:
            RoleRuleSet.from_dict(
                {
                    "schema_version": 1,
                    "evidence_score_bands": [{"score": 0, "meaning": "none"}],
                    "roles": [role, {**role, "canonical_role": "Mana"}],
                }
            )

        self.assertIn("Duplicate role_id", str(context.exception))

    def test_from_dict_validates_unsupported_score_policy(self) -> None:
        with self.assertRaises(RoleRulesError) as context:
            RoleRuleSet.from_dict(
                {
                    "schema_version": 1,
                    "evidence_score_bands": [{"score": 0, "meaning": "none"}],
                    "roles": [
                        {
                            "role_id": "draw",
                            "canonical_role": "Draw",
                            "evidence_rules": {"oracle_text_phrases": [{"phrase": "draw a card", "score": 75}]},
                            "exclusion_rules": [],
                            "score_policy": {"combine": "additive_capped", "default_score": 0, "max_score": 100},
                        }
                    ],
                }
            )

        self.assertIn("unsupported score_policy.combine", str(context.exception))

    def test_from_dict_validates_bad_score(self) -> None:
        with self.assertRaises(RoleRulesError) as context:
            RoleRuleSet.from_dict(
                {
                    "schema_version": 1,
                    "evidence_score_bands": [{"score": 0, "meaning": "none"}],
                    "roles": [
                        {
                            "role_id": "draw",
                            "canonical_role": "Draw",
                            "evidence_rules": {"oracle_text_phrases": [{"phrase": "draw a card", "score": 175}]},
                            "exclusion_rules": [],
                            "score_policy": {"combine": "highest_match", "default_score": 0, "max_score": 100},
                        }
                    ],
                }
            )

        self.assertIn("must be between 0 and 100", str(context.exception))

    def test_loader_reports_bad_yaml_shape(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bad_role_rules.yaml"
            path.write_text("roles:\n  ramp: bad\n", encoding="utf-8")

            with self.assertRaises(RoleRulesError):
                load_role_rules(path)


if __name__ == "__main__":
    unittest.main()

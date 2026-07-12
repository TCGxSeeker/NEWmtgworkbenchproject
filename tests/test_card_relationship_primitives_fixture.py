from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


FIXTURE_PATH = Path(
    "data/fixtures/relationships/"
    "card_relationship_primitives.example.json"
)

SNAKE_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


class CardRelationshipPrimitivesFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(
            FIXTURE_PATH.read_text(encoding="utf-8")
        )

    def test_schema_and_top_level_contract(self) -> None:
        self.assertEqual(
            self.payload["schema_version"],
            "card_relationship_primitives.v0",
        )

        self.assertEqual(
            set(self.payload),
            {
                "schema_version",
                "behavior_dimensions",
                "resources",
                "events",
                "relationship_types",
                "evidence_fields",
                "confidence_bands",
                "deferred_relationship_types",
                "non_goals",
            },
        )

    def test_vocabulary_lists_are_unique_snake_case(self) -> None:
        vocabulary_fields = (
            "behavior_dimensions",
            "resources",
            "events",
            "relationship_types",
            "evidence_fields",
            "deferred_relationship_types",
            "non_goals",
        )

        for field in vocabulary_fields:
            values = self.payload[field]

            self.assertTrue(values, field)
            self.assertEqual(len(values), len(set(values)), field)

            for value in values:
                self.assertRegex(value, SNAKE_CASE_PATTERN, field)

    def test_minimum_v0_relationship_types_are_locked(self) -> None:
        self.assertEqual(
            self.payload["relationship_types"],
            [
                "supplies",
                "triggers",
                "enables",
                "amplifies",
                "protects",
                "recurs",
                "conflicts_with",
            ],
        )

    def test_evidence_and_confidence_contract_is_locked(self) -> None:
        self.assertEqual(
            self.payload["evidence_fields"],
            [
                "source_entry_id",
                "target_entry_id",
                "relationship_type",
                "source_behavior",
                "target_behavior",
                "oracle_evidence",
                "conditions",
                "zones",
                "confidence_band",
                "derivation_rule",
            ],
        )

        self.assertEqual(
            self.payload["confidence_bands"],
            [0, 25, 50, 75, 100],
        )

    def test_deferred_and_forbidden_concepts_stay_out_of_v0(self) -> None:
        active = set(self.payload["relationship_types"])
        deferred = set(self.payload["deferred_relationship_types"])

        self.assertTrue(active.isdisjoint(deferred))

        self.assertEqual(
            deferred,
            {
                "redundant_with",
                "competes_with",
                "converts",
                "closes_with",
            },
        )

        required_non_goals = {
            "synergy_scoring",
            "deck_level_role_totals",
            "package_detection",
            "commander_analysis",
            "recommendations",
            "card_quality_judgments",
            "all_pairs_comparison",
            "hidden_inference",
        }

        self.assertTrue(
            required_non_goals.issubset(
                set(self.payload["non_goals"])
            )
        )


if __name__ == "__main__":
    unittest.main()

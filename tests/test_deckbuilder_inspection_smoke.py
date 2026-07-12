from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from mtg_workbench.deckbuilder.deck_inspection_report import (
    build_deck_inspection_report,
)
from mtg_workbench.deckbuilder.role_rules import load_role_rules
from mtg_workbench.deckbuilder.serialization import load_workspace


FIXTURE_DIR = Path("tests/fixtures/deckbuilder")
WORKSPACE_FIXTURE = FIXTURE_DIR / "inspection_smoke_workspace.mtgwdeck.json"
CARD_RECORDS_FIXTURE = FIXTURE_DIR / "inspection_smoke_card_records.json"
EXPECTED_FIXTURE = FIXTURE_DIR / "inspection_smoke_expected.json"
ROLE_RULES_FIXTURE = Path("data/fixtures/roles/role_rules.example.yaml")


def _all_keys(value: object) -> set[str]:
    keys: set[str] = set()

    if isinstance(value, dict):
        for key, item in value.items():
            keys.add(str(key))
            keys.update(_all_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_all_keys(item))

    return keys


class DeckInspectionFixtureSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.card_records = json.loads(
            CARD_RECORDS_FIXTURE.read_text(encoding="utf-8-sig")
        )
        cls.ruleset = load_role_rules(ROLE_RULES_FIXTURE)

    def _build_payload(self) -> tuple[object, dict]:
        workspace = load_workspace(WORKSPACE_FIXTURE)
        original_workspace = deepcopy(workspace)

        with patch.object(
            socket,
            "create_connection",
            side_effect=AssertionError("Smoke fixture must not use the network."),
        ):
            report = build_deck_inspection_report(
                workspace,
                card_records_by_name=self.card_records,
                ruleset=self.ruleset,
                include_card_role_evidence=True,
            )

        self.assertEqual(workspace, original_workspace)
        self.assertFalse(workspace.saved_state["is_dirty"])

        return workspace, report.to_dict()

    def test_end_to_end_report_matches_stable_expected_fixture(self) -> None:
        _, payload = self._build_payload()
        expected = json.loads(EXPECTED_FIXTURE.read_text(encoding="utf-8-sig"))

        self.assertEqual(payload, expected)

    def test_repeated_execution_is_deterministic(self) -> None:
        _, first = self._build_payload()
        _, second = self._build_payload()

        self.assertEqual(first, second)

    def test_smoke_contract_preserves_inspection_boundaries(self) -> None:
        _, payload = self._build_payload()

        self.assertEqual(
            payload["schema_version"],
            "deck_inspection_report.v0",
        )
        self.assertIn("skeleton_report", payload)
        self.assertIn("structural_warnings_report", payload)
        self.assertIn("card_fact_coverage", payload)
        self.assertIn("machine_evidence", payload)
        self.assertNotIn("debug_details", payload)

        coverage = payload["card_fact_coverage"]
        self.assertTrue(coverage["lookup_attempted"])
        self.assertGreater(coverage["found_count"], 0)
        self.assertGreater(coverage["missing_count"], 0)
        self.assertIn(
            "entry-smoke-missing",
            coverage["missing_entry_ids"],
        )

        found_ids = set(coverage["found_entry_ids"])
        role_report_entry_ids = {
            report["entry_id"]
            for report in payload["card_role_reports"]
        }
        self.assertTrue(role_report_entry_ids)
        self.assertTrue(role_report_entry_ids.issubset(found_ids))
        self.assertNotIn("entry-smoke-missing", role_report_entry_ids)

        keys = _all_keys(payload)
        forbidden_keys = {
            "deck_role_counts",
            "role_counts",
            "role_totals",
            "recommendations",
            "candidate_search",
            "add_scoring",
            "cut_scoring",
            "power_level",
            "deck_quality",
        }
        self.assertTrue(forbidden_keys.isdisjoint(keys))

        summary = payload["user_summary"].casefold()
        for forbidden_phrase in (
            "needs more ramp",
            "needs more draw",
            "should cut",
            "underpowered",
            "overpowered",
            "optimized",
        ):
            self.assertNotIn(forbidden_phrase, summary)


if __name__ == "__main__":
    unittest.main()

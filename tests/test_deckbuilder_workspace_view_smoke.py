from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from mtg_workbench.cli.main import main
from mtg_workbench.io.json_output import stable_json


FIXTURE_DIR = Path("tests/fixtures/deckbuilder")
WORKSPACE_FIXTURE = FIXTURE_DIR / "workspace_view_smoke_workspace.mtgwdeck.json"
CARD_RECORDS_FIXTURE = FIXTURE_DIR / "workspace_view_smoke_card_records.json"
EXPECTED_FIXTURE = FIXTURE_DIR / "workspace_view_smoke_expected.json"


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


class WorkspaceViewFixtureSmokeTests(unittest.TestCase):
    def test_cli_workspace_view_matches_stable_expected_fixture(self) -> None:
        expected = json.loads(EXPECTED_FIXTURE.read_text(encoding="utf-8-sig"))
        before_text = WORKSPACE_FIXTURE.read_text(encoding="utf-8")

        with patch.object(
            socket,
            "create_connection",
            side_effect=AssertionError("Workspace view smoke fixture must not use the network."),
        ):
            first_exit_code, first_output, first_errors = self._run_workspace_view()
            second_exit_code, second_output, second_errors = self._run_workspace_view()

        after_text = WORKSPACE_FIXTURE.read_text(encoding="utf-8")
        payload = json.loads(first_output)

        self.assertEqual(first_exit_code, 0, first_errors)
        self.assertEqual(second_exit_code, 0, second_errors)
        self.assertEqual(first_output, second_output)
        self.assertEqual(after_text, before_text)
        self.assertEqual(payload, expected)
        self.assertEqual(first_output, stable_json(expected) + "\n")

        self.assertEqual(payload["schema_version"], "deck_workspace_view_projection.v0")
        self.assertEqual(payload["group_by"], "color_identity")
        self.assertEqual(payload["sort_by"], "mana_value")
        self.assertEqual(payload["card_fact_lookup"]["found_count"], 3)
        self.assertEqual(payload["card_fact_lookup"]["missing_count"], 1)
        self.assertEqual(payload["card_fact_lookup"]["ambiguous_count"], 1)

        groups = {group["label"]: group for group in payload["groups"]}
        self.assertEqual(list(groups), ["Colorless", "U", "UG", "Missing Card Facts", "Ambiguous Card Facts"])
        self.assertEqual(groups["Colorless"]["entries"][0]["entry_id"], "entry-view-smoke-rock")
        self.assertEqual(groups["U"]["entries"][0]["entry_id"], "entry-view-smoke-draw")
        self.assertEqual(groups["UG"]["entries"][0]["entry_id"], "entry-view-smoke-commander")
        self.assertEqual(groups["Missing Card Facts"]["entries"][0]["entry_id"], "entry-view-smoke-missing")
        self.assertEqual(groups["Ambiguous Card Facts"]["entries"][0]["entry_id"], "entry-view-smoke-ambiguous")

        forbidden_keys = {
            "recommendations",
            "candidate_search",
            "add_scoring",
            "cut_scoring",
            "deck_role_counts",
            "role_totals",
            "power_level",
            "deck_quality",
            "strategic_analysis",
        }
        self.assertTrue(forbidden_keys.isdisjoint(_all_keys(payload)))

    def _run_workspace_view(self) -> tuple[int, str, str]:
        output = io.StringIO()
        errors = io.StringIO()

        with redirect_stdout(output), redirect_stderr(errors):
            exit_code = main(
                [
                    "workspace-view",
                    str(WORKSPACE_FIXTURE),
                    "--card-records",
                    str(CARD_RECORDS_FIXTURE),
                    "--group-by",
                    "color-identity",
                    "--sort-by",
                    "mana-value",
                ]
            )

        return exit_code, output.getvalue(), errors.getvalue()


if __name__ == "__main__":
    unittest.main()

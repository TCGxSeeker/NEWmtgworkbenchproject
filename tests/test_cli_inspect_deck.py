from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import unittest

from mtg_workbench.cli.main import main


FIXTURE_ROOT = Path(__file__).parent / "fixtures"
WORKSPACE_FIXTURE = FIXTURE_ROOT / "deckbuilder" / "inspection_smoke_workspace.mtgwdeck.json"
CARD_RECORDS_FIXTURE = FIXTURE_ROOT / "deckbuilder" / "inspection_smoke_card_records.json"
ROLE_RULES_FIXTURE = Path("data/fixtures/roles/role_rules.example.yaml")


class CliInspectDeckTests(unittest.TestCase):
    def test_inspect_deck_outputs_factual_report_without_card_source(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(["inspect-deck", str(WORKSPACE_FIXTURE)])

        self.assertEqual(exit_code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["schema_version"], "deck_inspection_report.v0")
        self.assertEqual(payload["deck_id"], "deck-inspection-smoke-v0")
        self.assertFalse(payload["card_fact_coverage"]["source_available"])
        self.assertFalse(payload["card_fact_coverage"]["lookup_attempted"])
        self.assertEqual(payload["card_role_reports"], [])
        self.assertNotIn("debug_details", payload)
        self.assertEqual(list(payload.keys()), sorted(payload.keys()))

    def test_inspect_deck_with_card_records_reports_lookup_coverage(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "inspect-deck",
                    str(WORKSPACE_FIXTURE),
                    "--card-records",
                    str(CARD_RECORDS_FIXTURE),
                ]
            )

        self.assertEqual(exit_code, 0)
        payload = json.loads(output.getvalue())
        coverage = payload["card_fact_coverage"]
        self.assertTrue(coverage["source_available"])
        self.assertTrue(coverage["lookup_attempted"])
        self.assertEqual(coverage["found_count"], 6)
        self.assertEqual(coverage["missing_count"], 1)
        self.assertEqual(coverage["ambiguous_count"], 0)
        self.assertEqual(coverage["missing_entry_ids"], ["entry-smoke-missing"])
        self.assertEqual(payload["machine_evidence"]["card_role_report_count"], 0)
        self.assertNotIn("deck_role_totals", payload)
        self.assertNotIn("recommendations", payload)

    def test_inspect_deck_can_include_card_level_role_evidence(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "inspect-deck",
                    str(WORKSPACE_FIXTURE),
                    "--card-records",
                    str(CARD_RECORDS_FIXTURE),
                    "--role-rules",
                    str(ROLE_RULES_FIXTURE),
                    "--include-role-evidence",
                ]
            )

        self.assertEqual(exit_code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["machine_evidence"]["card_role_report_count"], 6)
        self.assertEqual(len(payload["card_role_reports"]), 6)
        draw_report = next(
            report
            for report in payload["card_role_reports"]
            if report["entry_id"] == "entry-smoke-draw"
        )
        self.assertEqual(draw_report["role_report"]["best_match"]["role_id"], "draw")
        self.assertTrue(payload["machine_evidence"]["role_evidence_is_card_level_only"])

    def test_inspect_deck_requires_role_rules_for_role_evidence(self) -> None:
        output = io.StringIO()
        errors = io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            exit_code = main(
                [
                    "inspect-deck",
                    str(WORKSPACE_FIXTURE),
                    "--card-records",
                    str(CARD_RECORDS_FIXTURE),
                    "--include-role-evidence",
                ]
            )

        self.assertEqual(exit_code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("--role-rules is required", errors.getvalue())

    def test_inspect_deck_debug_output_is_explicit(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "inspect-deck",
                    str(WORKSPACE_FIXTURE),
                    "--card-records",
                    str(CARD_RECORDS_FIXTURE),
                    "--debug",
                ]
            )

        self.assertEqual(exit_code, 0)
        payload = json.loads(output.getvalue())
        self.assertIn("debug_details", payload)
        self.assertIn("card_lookup_results", payload["debug_details"])

    def test_inspect_deck_summary_only_outputs_compact_payload(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "inspect-deck",
                    str(WORKSPACE_FIXTURE),
                    "--card-records",
                    str(CARD_RECORDS_FIXTURE),
                    "--summary-only",
                ]
            )

        self.assertEqual(exit_code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["schema_version"], "deck_inspection_report.v0")
        self.assertEqual(payload["deck_id"], "deck-inspection-smoke-v0")
        self.assertEqual(payload["active_quantity_total"], 7)
        self.assertEqual(payload["structural_warning_count"], 3)
        self.assertEqual(payload["card_fact_coverage"]["found_count"], 6)
        self.assertEqual(payload["card_role_report_count"], 0)
        self.assertIn("user_summary", payload)
        self.assertNotIn("skeleton_report", payload)
        self.assertNotIn("structural_warnings_report", payload)
        self.assertNotIn("debug_details", payload)

    def test_inspect_deck_reports_missing_workspace_without_traceback(self) -> None:
        output = io.StringIO()
        errors = io.StringIO()

        with redirect_stdout(output), redirect_stderr(errors):
            exit_code = main(["inspect-deck", "missing.mtgwdeck.json"])

        self.assertEqual(exit_code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("workspace_path does not exist or is not a file", errors.getvalue())

    def test_inspect_deck_rejects_summary_only_with_debug(self) -> None:
        output = io.StringIO()
        errors = io.StringIO()

        with redirect_stdout(output), redirect_stderr(errors):
            exit_code = main(
                [
                    "inspect-deck",
                    str(WORKSPACE_FIXTURE),
                    "--summary-only",
                    "--debug",
                ]
            )

        self.assertEqual(exit_code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("--summary-only cannot be combined with --debug", errors.getvalue())


if __name__ == "__main__":
    unittest.main()

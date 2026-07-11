from pathlib import Path
import unittest

from mtg_workbench.deckbuilder.card_facts import CardFactsError
from mtg_workbench.deckbuilder.card_role_pipeline import (
    card_record_to_role_evidence_report,
    card_records_to_role_evidence_reports,
)
from mtg_workbench.deckbuilder.role_rules import load_role_rules


ROLE_RULES_FIXTURE = Path("data/fixtures/roles/role_rules.example.yaml")


class CardRoleEvidencePipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ruleset = load_role_rules(ROLE_RULES_FIXTURE)

    def test_single_draw_card_record_produces_draw_report(self) -> None:
        record = {"name": "Divination-ish", "oracle_text": "Draw two cards."}

        report = card_record_to_role_evidence_report(record, self.ruleset)

        self.assertIsNotNone(report.best_match)
        self.assertEqual(report.best_match.canonical_role, "Draw")
        self.assertEqual(report.card_name, "Divination-ish")

    def test_land_type_line_record_produces_land_match(self) -> None:
        record = {"name": "Test Island", "type_line": "Basic Land \u2014 Island"}

        report = card_record_to_role_evidence_report(record, self.ruleset)

        self.assertIsNotNone(report.best_match)
        self.assertEqual(report.best_match.canonical_role, "Land")

    def test_treasure_subtype_record_produces_ramp_match(self) -> None:
        record = {"name": "Treasure Token", "type_line": "Token Artifact \u2014 Treasure"}

        report = card_record_to_role_evidence_report(record, self.ruleset)

        self.assertIsNotNone(report.best_match)
        self.assertEqual(report.best_match.canonical_role, "Ramp")
        self.assertEqual(report.best_match.matched_field, "subtypes")

    def test_missing_name_raises_card_facts_error(self) -> None:
        with self.assertRaises(CardFactsError):
            card_record_to_role_evidence_report({"oracle_text": "Draw a card."}, self.ruleset)

    def test_include_unmatched_true_includes_unmatched_roles(self) -> None:
        report = card_record_to_role_evidence_report(
            {"name": "Blank Card"},
            self.ruleset,
            include_unmatched=True,
        )

        self.assertEqual(report.matched_role_count, 0)
        self.assertEqual(report.unmatched_role_count, len(self.ruleset.roles))

    def test_batch_helper_returns_tuple_of_reports_in_input_order(self) -> None:
        records = (
            {"name": "Draw Spell", "oracle_text": "Draw a card."},
            {"name": "Test Island", "type_line": "Basic Land \u2014 Island"},
        )

        reports = card_records_to_role_evidence_reports(records, self.ruleset)

        self.assertIsInstance(reports, tuple)
        self.assertEqual([report.card_name for report in reports], ["Draw Spell", "Test Island"])

    def test_two_faced_record_flows_through_pipeline(self) -> None:
        record = {
            "name": "Split Draw",
            "card_faces": [
                {"oracle_text": "Draw a card.", "type_line": "Instant"},
                {"oracle_text": "Scry 1.", "type_line": "Sorcery"},
            ],
        }

        report = card_record_to_role_evidence_report(record, self.ruleset)

        self.assertGreaterEqual(report.matched_role_count, 1)
        self.assertEqual(report.best_match.canonical_role, "Draw")

    def test_to_dict_keeps_summary_evidence_and_explanations_separated(self) -> None:
        record = {"name": "Draw Spell", "oracle_text": "Draw a card."}

        report = card_record_to_role_evidence_report(record, self.ruleset)
        payload = report.to_dict()

        self.assertIn("user_summary", payload)
        self.assertIn("machine_evidence", payload)
        self.assertIn("explanations", payload)
        self.assertNotIn("debug_details", payload["machine_evidence"][0])


if __name__ == "__main__":
    unittest.main()

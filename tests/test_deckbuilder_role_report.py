from pathlib import Path
import unittest

from mtg_workbench.deckbuilder.role_evidence import CardRoleFacts
from mtg_workbench.deckbuilder.role_report import build_role_evidence_report
from mtg_workbench.deckbuilder.role_rules import load_role_rules


ROLE_RULES_FIXTURE = Path("data/fixtures/roles/role_rules.example.yaml")


class RoleEvidenceReportTests(unittest.TestCase):
    def test_builds_report_for_matched_card(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        card = CardRoleFacts(card_name="Divination-ish", oracle_text="Draw two cards.")

        report = build_role_evidence_report(card, ruleset)

        self.assertEqual(report.schema_version, "role_evidence_report.v0")
        self.assertEqual(report.card_name, "Divination-ish")
        self.assertGreaterEqual(report.matched_role_count, 1)
        self.assertEqual(report.unmatched_role_count, 0)
        self.assertIsNotNone(report.best_match)
        self.assertEqual(report.best_match.role_id, "draw")
        self.assertIn("matched", report.user_summary)

    def test_builds_report_for_unmatched_card(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        card = CardRoleFacts(card_name="Blank Card", oracle_text="")

        report = build_role_evidence_report(card, ruleset)

        self.assertEqual(report.matched_role_count, 0)
        self.assertEqual(report.unmatched_role_count, 0)
        self.assertIsNone(report.best_match)
        self.assertIn("no role evidence matched", report.user_summary)

    def test_can_include_unmatched_roles_for_debug_or_advanced_views(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        card = CardRoleFacts(card_name="Blank Card", oracle_text="")

        report = build_role_evidence_report(card, ruleset, include_unmatched=True)

        self.assertEqual(report.matched_role_count, 0)
        self.assertEqual(report.unmatched_role_count, len(ruleset.roles))

    def test_to_dict_separates_summary_evidence_explanations_and_debug(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        card = CardRoleFacts(card_name="Draw Spell", oracle_text="Draw a card.")

        report = build_role_evidence_report(card, ruleset)
        payload = report.to_dict()

        self.assertEqual(payload["schema_version"], "role_evidence_report.v0")
        self.assertIn("user_summary", payload)
        self.assertIn("machine_evidence", payload)
        self.assertIn("explanations", payload)
        self.assertNotIn("debug_details", payload["machine_evidence"][0])

    def test_to_dict_can_include_debug_details(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        card = CardRoleFacts(card_name="Draw Spell", oracle_text="Draw a card.")

        report = build_role_evidence_report(card, ruleset)
        payload = report.to_dict(include_debug=True)

        self.assertIn("debug_details", payload["machine_evidence"][0])


if __name__ == "__main__":
    unittest.main()

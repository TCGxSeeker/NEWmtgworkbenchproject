from pathlib import Path
import unittest

from mtg_workbench.deckbuilder.role_evidence import (
    CardRoleFacts,
    match_all_role_evidence,
    match_role_evidence,
)
from mtg_workbench.deckbuilder.role_rules import load_role_rules


ROLE_RULES_FIXTURE = Path("data/fixtures/roles/role_rules.example.yaml")


class RoleEvidenceMatcherTests(unittest.TestCase):
    def test_matches_oracle_text_phrase_with_highest_score(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        role = ruleset.get_role("Draw")
        card = CardRoleFacts(card_name="Test Draw Spell", oracle_text="Draw two cards.")

        match = match_role_evidence(card, role)

        self.assertTrue(match.matched)
        self.assertEqual(match.role_id, "draw")
        self.assertEqual(match.score, 100)
        self.assertEqual(match.matched_field, "oracle_text")
        self.assertEqual(match.matched_value, "draw two cards")
        self.assertIn("Test Draw Spell", match.explanation)

    def test_matches_casefolded_whitespace_normalized_phrase(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        role = ruleset.get_role("draw")
        card = CardRoleFacts(card_name="Messy Text", oracle_text="  DRAW    A CARD. ")

        match = match_role_evidence(card, role)

        self.assertTrue(match.matched)
        self.assertEqual(match.score, 75)

    def test_matches_type_line_evidence(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        role = ruleset.get_role("Land")
        card = CardRoleFacts(card_name="Test Island", type_line="Basic Land — Island")

        match = match_role_evidence(card, role)

        self.assertTrue(match.matched)
        self.assertEqual(match.score, 100)
        self.assertEqual(match.matched_field, "type_line")

    def test_matches_subtype_evidence(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        role = ruleset.get_role("Ramp")
        card = CardRoleFacts(card_name="Test Treasure", subtypes=("Treasure",))

        match = match_role_evidence(card, role)

        self.assertTrue(match.matched)
        self.assertEqual(match.score, 50)
        self.assertEqual(match.matched_field, "subtypes")

    def test_exclusion_rule_blocks_match(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        role = ruleset.get_role("Draw")
        card = CardRoleFacts(
            card_name="Bad Group Hug",
            oracle_text="Draw a card. Each opponent draws a card.",
        )

        match = match_role_evidence(card, role)

        self.assertFalse(match.matched)
        self.assertEqual(match.score, 0)
        self.assertEqual(match.matched_field, "oracle_text")
        self.assertIn("Opponent-only draw", match.exclusion_reason)

    def test_mana_value_constraint_can_block_match(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        role = ruleset.get_role("Ramp")
        card = CardRoleFacts(
            card_name="Expensive Mana Thing",
            oracle_text="Add one mana of any color.",
            mana_value=7,
        )

        match = match_role_evidence(card, role)

        self.assertFalse(match.matched)
        self.assertEqual(match.score, 0)

    def test_match_all_role_evidence_returns_only_matches_by_default(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        card = CardRoleFacts(card_name="Simple Draw", oracle_text="Draw a card.")

        matches = match_all_role_evidence(card, ruleset)

        self.assertTrue(matches)
        self.assertTrue(all(match.matched for match in matches))
        self.assertIn("draw", {match.role_id for match in matches})

    def test_match_all_role_evidence_can_include_unmatched_roles(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        card = CardRoleFacts(card_name="Blank", oracle_text="")

        matches = match_all_role_evidence(card, ruleset, include_unmatched=True)

        self.assertEqual(len(matches), len(ruleset.roles))
        self.assertTrue(any(not match.matched for match in matches))


if __name__ == "__main__":
    unittest.main()

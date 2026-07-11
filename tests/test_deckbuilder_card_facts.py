from pathlib import Path
import unittest

from mtg_workbench.deckbuilder.card_facts import (
    CardFactsError,
    card_record_to_role_facts,
    records_to_role_facts,
)
from mtg_workbench.deckbuilder.role_report import build_role_evidence_report
from mtg_workbench.deckbuilder.role_rules import load_role_rules


ROLE_RULES_FIXTURE = Path("data/fixtures/roles/role_rules.example.yaml")


class CardFactsAdapterTests(unittest.TestCase):
    def test_simple_single_faced_record(self) -> None:
        facts = card_record_to_role_facts(
            {
                "name": "Example Draw",
                "oracle_text": "Draw a card.",
                "type_line": "Sorcery",
                "keywords": [],
                "mana_value": 2,
            }
        )

        self.assertEqual(facts.card_name, "Example Draw")
        self.assertEqual(facts.oracle_text, "Draw a card.")
        self.assertEqual(facts.type_line, "Sorcery")
        self.assertEqual(facts.keywords, ())
        self.assertEqual(facts.mana_value, 2)

    def test_missing_oracle_text_becomes_empty_string(self) -> None:
        facts = card_record_to_role_facts({"name": "Textless Card", "type_line": "Creature"})

        self.assertEqual(facts.oracle_text, "")

    def test_keywords_convert_to_tuple_of_strings(self) -> None:
        facts = card_record_to_role_facts(
            {
                "name": "Keyword Card",
                "keywords": ["Flying", "Vigilance"],
            }
        )

        self.assertEqual(facts.keywords, ("Flying", "Vigilance"))

    def test_mana_value_falls_back_to_cmc(self) -> None:
        facts = card_record_to_role_facts({"name": "Old Shape", "cmc": "3"})

        self.assertEqual(facts.mana_value, 3)

    def test_invalid_mana_value_becomes_none(self) -> None:
        facts = card_record_to_role_facts({"name": "Weird Value", "mana_value": "not a number"})

        self.assertIsNone(facts.mana_value)

    def test_subtypes_parse_from_type_line(self) -> None:
        treasure = card_record_to_role_facts({"name": "Treasure", "type_line": "Artifact \u2014 Treasure"})
        island = card_record_to_role_facts({"name": "Island", "type_line": "Basic Land \u2014 Island"})

        self.assertEqual(treasure.subtypes, ("Treasure",))
        self.assertEqual(island.subtypes, ("Island",))

    def test_card_faces_combine_oracle_text_and_type_line(self) -> None:
        facts = card_record_to_role_facts(
            {
                "name": "Two Face Card",
                "card_faces": [
                    {
                        "oracle_text": "Draw a card.",
                        "type_line": "Creature \u2014 Human",
                    },
                    {
                        "oracle_text": "Add one mana of any color.",
                        "type_line": "Sorcery \u2014 Adventure",
                    },
                ],
            }
        )

        self.assertEqual(facts.oracle_text, "Draw a card.\nAdd one mana of any color.")
        self.assertEqual(facts.type_line, "Creature \u2014 Human // Sorcery \u2014 Adventure")
        self.assertEqual(facts.subtypes, ("Human", "Adventure"))

    def test_missing_name_raises_clear_error(self) -> None:
        with self.assertRaises(CardFactsError) as context:
            card_record_to_role_facts({"oracle_text": "Draw a card."})

        self.assertIn("missing required name", str(context.exception))

    def test_adapter_output_feeds_role_evidence_report(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)
        facts = card_record_to_role_facts(
            {
                "name": "Draw Spell",
                "oracle_text": "Draw two cards.",
                "type_line": "Sorcery",
                "mana_value": 3,
            }
        )

        report = build_role_evidence_report(facts, ruleset)

        self.assertIsNotNone(report.best_match)
        self.assertEqual(report.best_match.role_id, "draw")

    def test_records_to_role_facts_returns_tuple(self) -> None:
        facts = records_to_role_facts(
            [
                {"name": "First", "oracle_text": "Draw a card."},
                {"name": "Second", "type_line": "Land"},
            ]
        )

        self.assertEqual([fact.card_name for fact in facts], ["First", "Second"])


if __name__ == "__main__":
    unittest.main()

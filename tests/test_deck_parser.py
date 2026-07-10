from pathlib import Path
import unittest

from mtg_workbench.decks.parser import parse_decklist


FIXTURE_ROOT = Path(__file__).parent / "fixtures"


class DeckParserTests(unittest.TestCase):
    def test_plain_text_parser_preserves_quantities_and_sections(self) -> None:
        raw_deck = parse_decklist(FIXTURE_ROOT / "decklists" / "plain_commander.txt")

        self.assertEqual(raw_deck.source_format, "plain_text")
        self.assertEqual(len(raw_deck.entries), 9)
        self.assertEqual(raw_deck.entries[0].section, "commander")
        self.assertEqual(raw_deck.entries[0].quantity, 1)
        self.assertEqual(raw_deck.entries[2].raw_name, "Basic Land Name")
        self.assertEqual(raw_deck.entries[2].quantity, 35)
        self.assertEqual(raw_deck.entries[-1].section, "maybeboard")

    def test_csv_parser_uses_category_to_detect_commander(self) -> None:
        raw_deck = parse_decklist(FIXTURE_ROOT / "decklists" / "csv_commander.csv")

        self.assertEqual(raw_deck.source_format, "csv")
        self.assertEqual(raw_deck.entries[0].section, "commander")
        self.assertEqual(raw_deck.entries[0].category, "Commander")
        self.assertEqual(raw_deck.entries[1].quantity, 35)
        self.assertEqual(raw_deck.entries[-1].section, "maybeboard")


if __name__ == "__main__":
    unittest.main()

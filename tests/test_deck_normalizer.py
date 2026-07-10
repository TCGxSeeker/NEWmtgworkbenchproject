from pathlib import Path
import unittest

from mtg_workbench.cards.catalog import CardCatalog
from mtg_workbench.decks.normalizer import normalize_deck
from mtg_workbench.decks.parser import parse_decklist


FIXTURE_ROOT = Path(__file__).parent / "fixtures"


class DeckNormalizerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = CardCatalog.from_json_file(FIXTURE_ROOT / "cards" / "tiny_cards.json")

    def test_plain_text_normalization_outputs_expected_groups(self) -> None:
        raw_deck = parse_decklist(FIXTURE_ROOT / "decklists" / "plain_commander.txt")
        parsed = normalize_deck(raw_deck, self.catalog)

        self.assertEqual([entry.name for entry in parsed.commanders], ["Example Commander"])
        self.assertEqual(parsed.mainboard[1].name, "Example Basic Land")
        self.assertEqual(parsed.mainboard[1].quantity, 35)
        self.assertEqual(parsed.mainboard[4].name, "Alias Target")
        self.assertEqual(parsed.mainboard[5].name, "Can't Stay Away")
        self.assertEqual([entry.raw_name for entry in parsed.unknown_cards], ["Unknown Mystery"])
        self.assertEqual([entry.name for entry in parsed.maybeboard], ["Maybe Card"])

    def test_duplicate_non_basic_warning_ignores_basic_lands(self) -> None:
        raw_deck = parse_decklist(FIXTURE_ROOT / "decklists" / "plain_commander.txt")
        parsed = normalize_deck(raw_deck, self.catalog)

        warning_codes = [warning.code for warning in parsed.warnings]
        self.assertEqual(warning_codes, ["duplicate_non_basic"])
        self.assertEqual(parsed.warnings[0].card_name, "Duplicate Nonbasic")
        self.assertEqual(parsed.warnings[0].quantity, 2)

    def test_csv_normalization_reports_unknowns_and_duplicates(self) -> None:
        raw_deck = parse_decklist(FIXTURE_ROOT / "decklists" / "csv_commander.csv")
        parsed = normalize_deck(raw_deck, self.catalog)

        self.assertEqual([entry.name for entry in parsed.commanders], ["Example Commander"])
        self.assertEqual([entry.raw_name for entry in parsed.unknown_cards], ["Unknown CSV Card"])
        self.assertEqual(len(parsed.warnings), 1)
        self.assertEqual(parsed.warnings[0].card_name, "Duplicate Nonbasic")
        self.assertEqual(parsed.warnings[0].quantity, 2)


if __name__ == "__main__":
    unittest.main()

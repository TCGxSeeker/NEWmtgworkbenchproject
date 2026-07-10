from pathlib import Path
import unittest

from mtg_workbench.cards.catalog import CardCatalog, normalize_lookup_key


FIXTURE_ROOT = Path(__file__).parent / "fixtures"


class CardCatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = CardCatalog.from_json_file(FIXTURE_ROOT / "cards" / "tiny_cards.json")

    def test_lookup_normalizes_case_and_repeated_spaces(self) -> None:
        card = self.catalog.find("  example   commander ")
        self.assertIsNotNone(card)
        self.assertEqual(card.name, "Example Commander")

    def test_lookup_supports_aliases(self) -> None:
        card = self.catalog.find("alias helper")
        self.assertIsNotNone(card)
        self.assertEqual(card.name, "Alias Target")

    def test_lookup_preserves_punctuation_sensitive_display_name(self) -> None:
        card = self.catalog.find("can't stay away")
        self.assertIsNotNone(card)
        self.assertEqual(card.name, "Can't Stay Away")

    def test_lookup_key_does_not_remove_punctuation(self) -> None:
        self.assertNotEqual(normalize_lookup_key("cant stay away"), normalize_lookup_key("can't stay away"))


if __name__ == "__main__":
    unittest.main()

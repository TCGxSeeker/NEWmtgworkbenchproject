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


    def test_card_record_preserves_stable_identity_fields(self) -> None:
        from mtg_workbench.cards.catalog import CardRecord

        card = CardRecord.from_dict(
            {
                "name": "Sol Ring",
                "aliases": [],
                "oracle_id": "oracle-sol-ring",
                "representative_scryfall_id": "printing-sol-ring",
            }
        )

        self.assertEqual(card.oracle_id, "oracle-sol-ring")
        self.assertEqual(
            card.representative_scryfall_id,
            "printing-sol-ring",
        )

    def test_catalog_preserves_all_alias_candidates(self) -> None:
        from mtg_workbench.cards.catalog import CardCatalog, CardRecord

        first = CardRecord.from_dict(
            {
                "name": "First Card",
                "aliases": ["Shared Alias"],
                "oracle_id": "oracle-first",
                "representative_scryfall_id": "printing-first",
            }
        )
        second = CardRecord.from_dict(
            {
                "name": "Second Card",
                "aliases": ["Shared Alias"],
                "oracle_id": "oracle-second",
                "representative_scryfall_id": "printing-second",
            }
        )

        catalog = CardCatalog([first, second])

        self.assertEqual(
            {card.oracle_id for card in catalog.find_all("shared alias")},
            {"oracle-first", "oracle-second"},
        )

    def test_catalog_find_rejects_alias_collision_across_oracle_ids(self) -> None:
        from mtg_workbench.cards.catalog import (
            CardCatalog,
            CardCatalogAmbiguityError,
            CardRecord,
        )

        first = CardRecord.from_dict(
            {
                "name": "First Card",
                "aliases": ["Shared Alias"],
                "oracle_id": "oracle-first",
            }
        )
        second = CardRecord.from_dict(
            {
                "name": "Second Card",
                "aliases": ["Shared Alias"],
                "oracle_id": "oracle-second",
            }
        )

        catalog = CardCatalog([first, second])

        with self.assertRaises(CardCatalogAmbiguityError):
            catalog.find("shared alias")

    def test_catalog_candidate_order_is_deterministic(self) -> None:
        from mtg_workbench.cards.catalog import CardCatalog, CardRecord

        first = CardRecord.from_dict(
            {
                "name": "First Card",
                "aliases": ["Shared Alias"],
                "oracle_id": "oracle-first",
            }
        )
        second = CardRecord.from_dict(
            {
                "name": "Second Card",
                "aliases": ["Shared Alias"],
                "oracle_id": "oracle-second",
            }
        )

        forward = CardCatalog([first, second]).find_all("shared alias")
        reverse = CardCatalog([second, first]).find_all("shared alias")

        self.assertEqual(
            [card.oracle_id for card in forward],
            [card.oracle_id for card in reverse],
        )


    def test_catalog_multiple_printings_of_one_oracle_identity_are_not_ambiguous(
        self,
    ) -> None:
        from mtg_workbench.cards.catalog import CardCatalog, CardRecord

        older_printing = CardRecord.from_dict(
            {
                "name": "Sol Ring",
                "oracle_id": "oracle-sol-ring",
                "representative_scryfall_id": "printing-z",
            }
        )
        default_printing = CardRecord.from_dict(
            {
                "name": "Sol Ring",
                "oracle_id": "oracle-sol-ring",
                "representative_scryfall_id": "printing-a",
            }
        )

        catalog = CardCatalog([older_printing, default_printing])

        found = catalog.find("Sol Ring")

        self.assertIsNotNone(found)
        self.assertEqual(found.oracle_id, "oracle-sol-ring")
        self.assertEqual(
            found.representative_scryfall_id,
            "printing-a",
        )
        self.assertEqual(len(catalog.find_all("Sol Ring")), 2)

    def test_catalog_multiple_no_oracle_printings_of_one_name_are_not_ambiguous(
        self,
    ) -> None:
        from mtg_workbench.cards.catalog import CardCatalog, CardRecord

        alternate_printing = CardRecord.from_dict(
            {
                "name": "Mystery Card",
                "representative_scryfall_id": "printing-z",
            }
        )
        default_printing = CardRecord.from_dict(
            {
                "name": "Mystery Card",
                "representative_scryfall_id": "printing-a",
            }
        )

        catalog = CardCatalog([alternate_printing, default_printing])

        found = catalog.find("Mystery Card")

        self.assertIsNotNone(found)
        self.assertIsNone(found.oracle_id)
        self.assertEqual(found.name, "Mystery Card")
        self.assertEqual(
            found.representative_scryfall_id,
            "printing-a",
        )
        self.assertEqual(len(catalog.find_all("Mystery Card")), 2)


if __name__ == "__main__":
    unittest.main()

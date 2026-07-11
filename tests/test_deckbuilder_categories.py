from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mtg_workbench.deckbuilder.categories import (
    CategoryTaxonomy,
    CategoryTaxonomyError,
    load_category_taxonomy,
    normalize_category_key,
)


FIXTURE_ROOT = Path(__file__).parent.parent / "data" / "fixtures" / "categories"
TAXONOMY_FIXTURE = FIXTURE_ROOT / "category_taxonomy.example.yaml"


class DeckbuilderCategoryTaxonomyTests(unittest.TestCase):
    def test_loads_tiny_category_taxonomy_fixture(self) -> None:
        taxonomy = load_category_taxonomy(TAXONOMY_FIXTURE)

        self.assertEqual(taxonomy.schema_version, 1)
        self.assertEqual(taxonomy.source, "category_taxonomy_v0_example")
        self.assertIn("Commander", taxonomy.canonical_categories)
        self.assertIn("Pet Card", taxonomy.canonical_categories)
        self.assertEqual(taxonomy.aliases["Card Advantage"], "Draw")

    def test_normalize_category_key_trims_casefolds_and_collapses_spaces(self) -> None:
        self.assertEqual(normalize_category_key("  Card    Advantage "), "card advantage")

    def test_normalizes_exact_canonical_category(self) -> None:
        taxonomy = load_category_taxonomy(TAXONOMY_FIXTURE)

        result = taxonomy.normalize("  board   wipe ")

        self.assertTrue(result.is_known)
        self.assertEqual(result.input_category, "  board   wipe ")
        self.assertEqual(result.normalized_category, "Board Wipe")
        self.assertEqual(result.category_origin, "normalized")

    def test_normalizes_alias_to_canonical_category(self) -> None:
        taxonomy = load_category_taxonomy(TAXONOMY_FIXTURE)

        result = taxonomy.normalize("mana   rock")

        self.assertTrue(result.is_known)
        self.assertEqual(result.normalized_category, "Ramp")

    def test_unknown_category_is_preserved_without_guessing(self) -> None:
        taxonomy = load_category_taxonomy(TAXONOMY_FIXTURE)

        result = taxonomy.normalize("Weird Personal Bucket")

        self.assertFalse(result.is_known)
        self.assertEqual(result.input_category, "Weird Personal Bucket")
        self.assertIsNone(result.normalized_category)
        self.assertEqual(result.category_origin, "unknown")

    def test_is_canonical_distinguishes_alias_from_canonical(self) -> None:
        taxonomy = load_category_taxonomy(TAXONOMY_FIXTURE)

        self.assertTrue(taxonomy.is_canonical("ramp"))
        self.assertFalse(taxonomy.is_canonical("Mana Rock"))

    def test_from_dict_validates_alias_targets(self) -> None:
        with self.assertRaises(CategoryTaxonomyError) as context:
            CategoryTaxonomy.from_dict(
                {
                    "schema_version": 1,
                    "canonical_categories": ["Ramp"],
                    "aliases": {"Card Draw": "Draw"},
                }
            )

        self.assertIn("points to unknown category", str(context.exception))

    def test_from_dict_rejects_duplicate_canonical_categories(self) -> None:
        with self.assertRaises(CategoryTaxonomyError) as context:
            CategoryTaxonomy.from_dict(
                {
                    "schema_version": 1,
                    "canonical_categories": ["Ramp", " ramp "],
                    "aliases": {},
                }
            )

        self.assertIn("Duplicate canonical category", str(context.exception))

    def test_loader_reports_bad_fixture_shape(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bad_taxonomy.yaml"
            path.write_text("canonical_categories:\n  Commander: bad\n", encoding="utf-8")

            with self.assertRaises(CategoryTaxonomyError):
                load_category_taxonomy(path)


if __name__ == "__main__":
    unittest.main()

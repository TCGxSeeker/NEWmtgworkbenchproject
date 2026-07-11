from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mtg_workbench.cards.catalog import CardCatalog
from mtg_workbench.deckbuilder.import_export import export_plain_text_decklist, import_plain_text_decklist
from mtg_workbench.deckbuilder.mutations import add_entry
from mtg_workbench.deckbuilder.models import DeckWorkspace
from mtg_workbench.deckbuilder.serialization import dumps_workspace, load_workspace, save_workspace


FIXTURE_ROOT = Path(__file__).parent / "fixtures"
DECKBUILDER_FIXTURES = FIXTURE_ROOT / "deckbuilder"
CARDS_FIXTURE = FIXTURE_ROOT / "cards" / "tiny_cards.json"
STAMP = "2026-07-10T03:00:00Z"


class DeckbuilderImportExportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = CardCatalog.from_json_file(CARDS_FIXTURE)

    def test_import_simple_lines_supports_1x_1_and_bare_name(self) -> None:
        text = (DECKBUILDER_FIXTURES / "simple_import.txt").read_text(encoding="utf-8")

        workspace = import_plain_text_decklist(
            text,
            catalog=self.catalog,
            name="Simple Import",
            deck_id="simple-import",
            source="simple_import.txt",
            updated_at=STAMP,
        )

        self.assertEqual(workspace.name, "Simple Import")
        self.assertEqual(workspace.metadata, {"import_origin": "plain_text", "source": "simple_import.txt"})
        self.assertEqual([entry.quantity for entry in workspace.mainboard], [1, 1, 1])
        self.assertEqual([entry.input_name for entry in workspace.mainboard], ["Arcane Helper", "Alias Helper", "Can't Stay Away"])
        self.assertEqual([entry.display_name for entry in workspace.mainboard], ["Arcane Helper", "Alias Target", "Can't Stay Away"])
        self.assertTrue(workspace.saved_state["is_dirty"])
        self.assertEqual(workspace.updated_at, STAMP)

    def test_import_commander_mainboard_and_maybeboard_sections(self) -> None:
        text = (DECKBUILDER_FIXTURES / "commander_import.txt").read_text(encoding="utf-8")

        workspace = import_plain_text_decklist(text, catalog=self.catalog, deck_id="sections", updated_at=STAMP)

        self.assertEqual([entry.display_name for entry in workspace.commanders], ["Example Commander"])
        self.assertEqual(workspace.commanders[0].quantity, 1)
        self.assertEqual(workspace.commanders[0].zone, "commander")
        self.assertEqual([entry.display_name for entry in workspace.mainboard], ["Arcane Helper"])
        self.assertEqual([entry.display_name for entry in workspace.maybeboard], ["Maybe Card"])

    def test_import_preserves_explicit_commander_quantity(self) -> None:
        workspace = import_plain_text_decklist(
            "Commander\n2x Example Commander\n",
            catalog=self.catalog,
            deck_id="commander-quantity",
            updated_at=STAMP,
        )

        self.assertEqual(workspace.commanders[0].quantity, 2)

    def test_import_treats_sideboard_as_maybeboard(self) -> None:
        workspace = import_plain_text_decklist(
            "Sideboard\n1x Maybe Card\n",
            catalog=self.catalog,
            deck_id="sideboard",
            updated_at=STAMP,
        )

        self.assertEqual(len(workspace.maybeboard), 1)
        self.assertEqual(workspace.maybeboard[0].display_name, "Maybe Card")

    def test_import_preserves_unknown_unresolved_cards(self) -> None:
        text = (DECKBUILDER_FIXTURES / "unresolved_import.txt").read_text(encoding="utf-8")

        workspace = import_plain_text_decklist(text, catalog=self.catalog, deck_id="unresolved", updated_at=STAMP)

        unknown_main = workspace.mainboard[0]
        unknown_maybe = workspace.maybeboard[0]
        self.assertEqual(unknown_main.input_name, "Unknown Mystery")
        self.assertIsNone(unknown_main.display_name)
        self.assertTrue(unknown_main.is_unresolved)
        self.assertEqual(unknown_maybe.input_name, "Mystery Maybe")
        self.assertIsNone(unknown_maybe.display_name)
        self.assertTrue(unknown_maybe.is_unresolved)

    def test_import_preserves_conservative_category_headers(self) -> None:
        text = (DECKBUILDER_FIXTURES / "categorized_import.txt").read_text(encoding="utf-8")

        workspace = import_plain_text_decklist(text, catalog=self.catalog, deck_id="categorized", updated_at=STAMP)

        self.assertEqual([entry.display_name for entry in workspace.mainboard], ["Arcane Helper", "Alias Target", "Example Basic Land"])
        self.assertEqual([entry.quantity for entry in workspace.mainboard], [1, 1, 35])
        self.assertEqual([entry.categories for entry in workspace.mainboard], [["Ramp"], ["Draw"], ["Lands"]])

    def test_export_workspace_to_plain_text_sections(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Export Test", deck_id="export-test")
        add_entry(workspace, "Example Commander", display_name="Example Commander", entry_id="commander", zone="commander", updated_at=STAMP)
        add_entry(workspace, "Arcane Helper", display_name="Arcane Helper", entry_id="main", quantity=2, updated_at=STAMP)
        add_entry(workspace, "Maybe Card", display_name="Maybe Card", entry_id="maybe", zone="maybeboard", updated_at=STAMP)

        exported = export_plain_text_decklist(workspace)

        self.assertEqual(
            exported,
            "Commander\n1x Example Commander\n\nMainboard\n2x Arcane Helper\n\nMaybeboard\n1x Maybe Card\n",
        )

    def test_export_unresolved_cards_use_input_name_fallback(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Export Unknown", deck_id="export-unknown")
        add_entry(workspace, "Unknown Mystery", entry_id="unknown", is_unresolved=True, updated_at=STAMP)

        exported = export_plain_text_decklist(workspace)

        self.assertIn("1x Unknown Mystery", exported)

    def test_import_export_preserves_card_names_and_quantities(self) -> None:
        text = (DECKBUILDER_FIXTURES / "unresolved_import.txt").read_text(encoding="utf-8")

        workspace = import_plain_text_decklist(text, catalog=self.catalog, deck_id="round-trip-text", updated_at=STAMP)
        exported = export_plain_text_decklist(workspace)

        self.assertIn("1x Example Commander", exported)
        self.assertIn("1x Unknown Mystery", exported)
        self.assertIn("1x Mystery Maybe", exported)

    def test_import_save_load_export_works_and_save_marks_clean(self) -> None:
        text = "Commander\nExample Commander\n\nMainboard\n2x Arcane Helper\n1x Unknown Mystery\n\nMaybeboard\nMaybe Card\n"
        expected = (DECKBUILDER_FIXTURES / "expected_export.txt").read_text(encoding="utf-8")
        workspace = import_plain_text_decklist(text, catalog=self.catalog, deck_id="save-load-export", updated_at=STAMP)
        self.assertTrue(workspace.saved_state["is_dirty"])

        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "save-load-export.mtgwdeck.json"
            save_workspace(workspace, path)
            self.assertFalse(workspace.saved_state["is_dirty"])
            loaded = load_workspace(path)

        self.assertFalse(loaded.saved_state["is_dirty"])
        self.assertEqual(export_plain_text_decklist(loaded), expected)

    def test_load_workspace_returns_clean_even_if_file_says_dirty(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Dirty File", deck_id="dirty-file")
        add_entry(workspace, "Arcane Helper", entry_id="dirty-card", updated_at=STAMP)
        self.assertTrue(workspace.saved_state["is_dirty"])

        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "dirty-file.mtgwdeck.json"
            path.write_text(dumps_workspace(workspace), encoding="utf-8")
            loaded = load_workspace(path)

        self.assertFalse(loaded.saved_state["is_dirty"])


if __name__ == "__main__":
    unittest.main()

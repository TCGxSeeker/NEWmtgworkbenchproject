from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mtg_workbench.cli.main import main
from mtg_workbench.deckbuilder.serialization import load_workspace


FIXTURE_ROOT = Path(__file__).parent / "fixtures"
DECKBUILDER_FIXTURES = FIXTURE_ROOT / "deckbuilder"
CARDS_FIXTURE = FIXTURE_ROOT / "cards" / "tiny_cards.json"
TAXONOMY_FIXTURE = Path("data/fixtures/categories/category_taxonomy.example.yaml")


class CliWorkspaceImportExportTests(unittest.TestCase):
    def test_workspace_import_writes_native_workspace_and_summary(self) -> None:
        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "cli-import.mtgwdeck.json"
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    [
                        "workspace-import",
                        str(DECKBUILDER_FIXTURES / "commander_import.txt"),
                        "--cards",
                        str(CARDS_FIXTURE),
                        "--name",
                        "CLI Import",
                        "--deck-id",
                        "cli-import",
                        "--output",
                        str(output_path),
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())
            payload = json.loads(output.getvalue())
            workspace = load_workspace(output_path)

        self.assertEqual(payload["command"], "workspace-import")
        self.assertEqual(list(payload.keys()), sorted(payload.keys()))
        self.assertEqual(payload["deck"]["deck_id"], "cli-import")
        self.assertEqual(payload["deck"]["active_quantity_total"], 2)
        self.assertFalse(payload["deck"]["is_dirty"])
        self.assertEqual(workspace.name, "CLI Import")
        self.assertEqual(workspace.deck_id, "cli-import")
        self.assertFalse(workspace.saved_state["is_dirty"])
        self.assertEqual(workspace.commanders[0].display_name, "Example Commander")
        self.assertEqual(workspace.mainboard[0].display_name, "Arcane Helper")
        self.assertEqual(workspace.maybeboard[0].display_name, "Maybe Card")

    def test_workspace_import_can_use_category_taxonomy(self) -> None:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "taxonomy_import.txt"
            output_path = Path(temp_dir) / "taxonomy-import.mtgwdeck.json"
            input_path.write_text("Main Deck\nCard Draw\n1x Arcane Helper\n", encoding="utf-8")
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    [
                        "workspace-import",
                        str(input_path),
                        "--cards",
                        str(CARDS_FIXTURE),
                        "--category-taxonomy",
                        str(TAXONOMY_FIXTURE),
                        "--output",
                        str(output_path),
                    ]
                )

            self.assertEqual(exit_code, 0)
            workspace = load_workspace(output_path)

        entry = workspace.mainboard[0]
        self.assertEqual(entry.categories, ["Draw"])
        self.assertEqual(entry.imported_category, "Card Draw")
        self.assertEqual(entry.normalized_category, "Draw")
        self.assertEqual(entry.generic_category_hint, "Draw")
        self.assertEqual(entry.category_origin, "normalized")

    def test_workspace_export_writes_plain_text_decklist_and_summary(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_path = Path(temp_dir) / "round-trip.mtgwdeck.json"
            export_path = Path(temp_dir) / "round-trip.txt"
            import_output = io.StringIO()
            export_output = io.StringIO()

            with redirect_stdout(import_output):
                import_exit_code = main(
                    [
                        "workspace-import",
                        str(DECKBUILDER_FIXTURES / "commander_import.txt"),
                        "--cards",
                        str(CARDS_FIXTURE),
                        "--name",
                        "Round Trip",
                        "--deck-id",
                        "round-trip",
                        "--output",
                        str(workspace_path),
                    ]
                )
            with redirect_stdout(export_output):
                export_exit_code = main(
                    [
                        "workspace-export",
                        str(workspace_path),
                        "--output",
                        str(export_path),
                    ]
                )

            exported = export_path.read_text(encoding="utf-8")
            payload = json.loads(export_output.getvalue())

        self.assertEqual(import_exit_code, 0)
        self.assertEqual(export_exit_code, 0)
        self.assertEqual(
            exported,
            "Commander\n1x Example Commander\n\n"
            "Mainboard\n1x Arcane Helper\n\n"
            "Maybeboard\n1x Maybe Card\n",
        )
        self.assertEqual(payload["command"], "workspace-export")
        self.assertEqual(payload["deck"]["deck_id"], "round-trip")
        self.assertEqual(payload["deck"]["quantity_totals"]["maybeboard"], 1)
        self.assertEqual(payload["line_count"], 8)

    def test_workspace_import_rejects_non_native_output_suffix(self) -> None:
        output = io.StringIO()
        errors = io.StringIO()

        with redirect_stdout(output), redirect_stderr(errors):
            exit_code = main(
                [
                    "workspace-import",
                    str(DECKBUILDER_FIXTURES / "commander_import.txt"),
                    "--output",
                    "deck.json",
                ]
            )

        self.assertEqual(exit_code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn(".mtgwdeck.json", errors.getvalue())

    def test_workspace_export_rejects_non_native_input_suffix(self) -> None:
        output = io.StringIO()
        errors = io.StringIO()

        with redirect_stdout(output), redirect_stderr(errors):
            exit_code = main(
                [
                    "workspace-export",
                    str(DECKBUILDER_FIXTURES / "simple_import.txt"),
                    "--output",
                    "decklist.txt",
                ]
            )

        self.assertEqual(exit_code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn(".mtgwdeck.json", errors.getvalue())


if __name__ == "__main__":
    unittest.main()

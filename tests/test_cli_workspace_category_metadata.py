from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mtg_workbench.cli.main import main
from mtg_workbench.deckbuilder.models import DeckWorkspace
from mtg_workbench.deckbuilder.mutations import add_entry
from mtg_workbench.deckbuilder.serialization import load_workspace, save_workspace


TAXONOMY_FIXTURE = (
    Path(__file__).parent.parent
    / "data"
    / "fixtures"
    / "categories"
    / "category_taxonomy.example.yaml"
)


def _workspace_with_metadata() -> DeckWorkspace:
    workspace = DeckWorkspace.create_empty(name="Category CLI", deck_id="category-cli")
    add_entry(
        workspace,
        "Arcane Helper",
        entry_id="category-card",
        categories=["Draw"],
        imported_category="Card Draw",
        normalized_category="Draw",
        generic_category_hint="Draw",
        deck_specific_primary_role="Engine Setup",
        secondary_tags=["setup"],
        category_origin="normalized",
        tags=["favorite"],
        notes="Original note",
    )
    return workspace


class CliWorkspaceCategoryMetadataTests(unittest.TestCase):
    def test_workspace_category_metadata_commands_preserve_grouping(self) -> None:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.mtgwdeck.json"
            imported_path = Path(temp_dir) / "imported.mtgwdeck.json"
            generic_path = Path(temp_dir) / "generic.mtgwdeck.json"
            origin_path = Path(temp_dir) / "origin.mtgwdeck.json"
            save_workspace(_workspace_with_metadata(), input_path)

            with redirect_stdout(io.StringIO()):
                imported_exit = main(
                    [
                        "workspace-set-imported-category",
                        str(input_path),
                        "category-card",
                        "--value",
                        "Personal Draw",
                        "--output",
                        str(imported_path),
                    ]
                )
            with redirect_stdout(io.StringIO()):
                generic_exit = main(
                    [
                        "workspace-set-generic-category-hint",
                        str(imported_path),
                        "category-card",
                        "--value",
                        "Selection",
                        "--output",
                        str(generic_path),
                    ]
                )
            output = io.StringIO()
            with redirect_stdout(output):
                origin_exit = main(
                    [
                        "workspace-set-category-origin",
                        str(generic_path),
                        "category-card",
                        "--value",
                        "user",
                        "--output",
                        str(origin_path),
                    ]
                )

            input_workspace = load_workspace(input_path)
            workspace = load_workspace(origin_path)
            entry = workspace.mainboard[0]
            payload = json.loads(output.getvalue())

        self.assertEqual(imported_exit, 0)
        self.assertEqual(generic_exit, 0)
        self.assertEqual(origin_exit, 0)
        self.assertEqual(input_workspace.mainboard[0].imported_category, "Card Draw")
        self.assertEqual(entry.categories, ["Draw"])
        self.assertEqual(entry.imported_category, "Personal Draw")
        self.assertEqual(entry.generic_category_hint, "Selection")
        self.assertEqual(entry.category_origin, "user")
        self.assertEqual(payload["command"], "workspace-set-category-origin")
        self.assertEqual(payload["entry"]["categories"], ["Draw"])
        self.assertEqual(payload["entry"]["category_origin"], "user")

    def test_workspace_set_normalized_category_can_validate_with_taxonomy(self) -> None:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.mtgwdeck.json"
            valid_path = Path(temp_dir) / "valid.mtgwdeck.json"
            invalid_path = Path(temp_dir) / "invalid.mtgwdeck.json"
            save_workspace(_workspace_with_metadata(), input_path)

            with redirect_stdout(io.StringIO()):
                valid_exit = main(
                    [
                        "workspace-set-normalized-category",
                        str(input_path),
                        "category-card",
                        "--value",
                        "Ramp",
                        "--category-taxonomy",
                        str(TAXONOMY_FIXTURE),
                        "--output",
                        str(valid_path),
                    ]
                )
            errors = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(errors):
                invalid_exit = main(
                    [
                        "workspace-set-normalized-category",
                        str(input_path),
                        "category-card",
                        "--value",
                        "Card Draw",
                        "--category-taxonomy",
                        str(TAXONOMY_FIXTURE),
                        "--output",
                        str(invalid_path),
                    ]
                )

            workspace = load_workspace(valid_path)

        self.assertEqual(valid_exit, 0)
        self.assertEqual(workspace.mainboard[0].normalized_category, "Ramp")
        self.assertEqual(invalid_exit, 2)
        self.assertFalse(invalid_path.exists())
        self.assertIn("normalized_category must be a canonical category", errors.getvalue())

    def test_secondary_tag_commands_and_clear_category_metadata(self) -> None:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.mtgwdeck.json"
            added_path = Path(temp_dir) / "added.mtgwdeck.json"
            removed_path = Path(temp_dir) / "removed.mtgwdeck.json"
            replaced_path = Path(temp_dir) / "replaced.mtgwdeck.json"
            cleared_path = Path(temp_dir) / "cleared.mtgwdeck.json"
            save_workspace(_workspace_with_metadata(), input_path)

            with redirect_stdout(io.StringIO()):
                add_exit = main(
                    [
                        "workspace-add-secondary-tag",
                        str(input_path),
                        "category-card",
                        "--tag",
                        "cantrip",
                        "--output",
                        str(added_path),
                    ]
                )
            with redirect_stdout(io.StringIO()):
                remove_exit = main(
                    [
                        "workspace-remove-secondary-tag",
                        str(added_path),
                        "category-card",
                        "--tag",
                        "setup",
                        "--output",
                        str(removed_path),
                    ]
                )
            with redirect_stdout(io.StringIO()):
                replace_exit = main(
                    [
                        "workspace-replace-secondary-tags",
                        str(removed_path),
                        "category-card",
                        "--tag",
                        "engine",
                        "--tag",
                        "engine",
                        "--tag",
                        "payoff",
                        "--output",
                        str(replaced_path),
                    ]
                )
            with redirect_stdout(io.StringIO()):
                clear_exit = main(
                    [
                        "workspace-clear-category-metadata",
                        str(replaced_path),
                        "category-card",
                        "--output",
                        str(cleared_path),
                    ]
                )

            replaced_entry = load_workspace(replaced_path).mainboard[0]
            cleared_entry = load_workspace(cleared_path).mainboard[0]

        self.assertEqual(add_exit, 0)
        self.assertEqual(remove_exit, 0)
        self.assertEqual(replace_exit, 0)
        self.assertEqual(clear_exit, 0)
        self.assertEqual(replaced_entry.secondary_tags, ["engine", "payoff"])
        self.assertEqual(cleared_entry.categories, ["Draw"])
        self.assertIsNone(cleared_entry.imported_category)
        self.assertIsNone(cleared_entry.normalized_category)
        self.assertIsNone(cleared_entry.generic_category_hint)
        self.assertIsNone(cleared_entry.deck_specific_primary_role)
        self.assertEqual(cleared_entry.secondary_tags, [])
        self.assertIsNone(cleared_entry.category_origin)

    def test_entry_annotation_commands_update_notes_and_tags(self) -> None:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.mtgwdeck.json"
            notes_path = Path(temp_dir) / "notes.mtgwdeck.json"
            tags_path = Path(temp_dir) / "tags.mtgwdeck.json"
            add_tags_path = Path(temp_dir) / "add-tags.mtgwdeck.json"
            remove_tags_path = Path(temp_dir) / "remove-tags.mtgwdeck.json"
            clear_notes_path = Path(temp_dir) / "clear-notes.mtgwdeck.json"
            save_workspace(_workspace_with_metadata(), input_path)

            with redirect_stdout(io.StringIO()):
                notes_exit = main(
                    [
                        "workspace-set-notes",
                        str(input_path),
                        "category-card",
                        "--value",
                        "Needs review",
                        "--output",
                        str(notes_path),
                    ]
                )
            with redirect_stdout(io.StringIO()):
                set_tags_exit = main(
                    [
                        "workspace-set-tags",
                        str(notes_path),
                        "category-card",
                        "--tag",
                        "fast",
                        "--tag",
                        "fast",
                        "--tag",
                        "review",
                        "--output",
                        str(tags_path),
                    ]
                )
            with redirect_stdout(io.StringIO()):
                add_tags_exit = main(
                    [
                        "workspace-add-tag",
                        str(tags_path),
                        "category-card",
                        "--tag",
                        "keep",
                        "--tag",
                        "fast",
                        "--output",
                        str(add_tags_path),
                    ]
                )
            with redirect_stdout(io.StringIO()):
                remove_tags_exit = main(
                    [
                        "workspace-remove-tag",
                        str(add_tags_path),
                        "category-card",
                        "--tag",
                        "review",
                        "--output",
                        str(remove_tags_path),
                    ]
                )
            with redirect_stdout(io.StringIO()):
                clear_notes_exit = main(
                    [
                        "workspace-set-notes",
                        str(remove_tags_path),
                        "category-card",
                        "--clear",
                        "--output",
                        str(clear_notes_path),
                    ]
                )

            workspace = load_workspace(clear_notes_path)
            entry = workspace.mainboard[0]

        self.assertEqual(notes_exit, 0)
        self.assertEqual(set_tags_exit, 0)
        self.assertEqual(add_tags_exit, 0)
        self.assertEqual(remove_tags_exit, 0)
        self.assertEqual(clear_notes_exit, 0)
        self.assertEqual(entry.tags, ["fast", "keep"])
        self.assertIsNone(entry.notes)

    def test_category_metadata_commands_require_native_output_suffix(self) -> None:
        errors = io.StringIO()

        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            exit_code = main(
                [
                    "workspace-set-imported-category",
                    "input.mtgwdeck.json",
                    "category-card",
                    "--value",
                    "Draw",
                    "--output",
                    "output.json",
                ]
            )

        self.assertEqual(exit_code, 2)
        self.assertIn("--output must end with .mtgwdeck.json", errors.getvalue())


if __name__ == "__main__":
    unittest.main()

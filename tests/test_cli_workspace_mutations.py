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


CARDS_FIXTURE = Path(__file__).parent / "fixtures" / "cards" / "tiny_cards.json"


class CliWorkspaceMutationTests(unittest.TestCase):
    def test_workspace_add_card_writes_output_without_mutating_input_file(self) -> None:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.mtgwdeck.json"
            output_path = Path(temp_dir) / "output.mtgwdeck.json"
            workspace = DeckWorkspace.create_empty(name="Mutation CLI", deck_id="mutation-cli")
            save_workspace(workspace, input_path)
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    [
                        "workspace-add-card",
                        str(input_path),
                        "Arcane Helper",
                        "--cards",
                        str(CARDS_FIXTURE),
                        "--entry-id",
                        "cli-add",
                        "--quantity",
                        "2",
                        "--category",
                        "Ramp",
                        "--tag",
                        "test",
                        "--output",
                        str(output_path),
                    ]
                )

            input_workspace = load_workspace(input_path)
            output_workspace = load_workspace(output_path)
            payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(input_workspace.mainboard, [])
        self.assertFalse(output_workspace.saved_state["is_dirty"])
        self.assertEqual(output_workspace.mainboard[0].entry_id, "cli-add")
        self.assertEqual(output_workspace.mainboard[0].display_name, "Arcane Helper")
        self.assertEqual(output_workspace.mainboard[0].quantity, 2)
        self.assertEqual(output_workspace.mainboard[0].categories, ["Ramp"])
        self.assertEqual(output_workspace.mainboard[0].tags, ["test"])
        self.assertEqual(payload["command"], "workspace-add-card")
        self.assertEqual(payload["entry"]["entry_id"], "cli-add")
        self.assertEqual(payload["entry"]["quantity"], 2)
        self.assertFalse(payload["deck"]["is_dirty"])

    def test_workspace_add_card_can_preserve_unresolved_entry(self) -> None:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.mtgwdeck.json"
            output_path = Path(temp_dir) / "output.mtgwdeck.json"
            save_workspace(DeckWorkspace.create_empty(name="Unknowns"), input_path)

            with redirect_stdout(io.StringIO()):
                exit_code = main(
                    [
                        "workspace-add-card",
                        str(input_path),
                        "Mystery Card",
                        "--entry-id",
                        "unknown",
                        "--unresolved",
                        "--output",
                        str(output_path),
                    ]
                )

            workspace = load_workspace(output_path)

        self.assertEqual(exit_code, 0)
        self.assertEqual(workspace.mainboard[0].input_name, "Mystery Card")
        self.assertIsNone(workspace.mainboard[0].display_name)
        self.assertTrue(workspace.mainboard[0].is_unresolved)

    def test_workspace_remove_entry_writes_removed_status(self) -> None:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.mtgwdeck.json"
            output_path = Path(temp_dir) / "output.mtgwdeck.json"
            workspace = DeckWorkspace.create_empty(name="Remove CLI")
            add_entry(workspace, "Arcane Helper", entry_id="remove-me")
            save_workspace(workspace, input_path)
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    [
                        "workspace-remove-entry",
                        str(input_path),
                        "remove-me",
                        "--output",
                        str(output_path),
                    ]
                )

            workspace = load_workspace(output_path)
            payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(workspace.mainboard, [])
        self.assertEqual(payload["entry"], {"entry_id": "remove-me", "status": "removed"})

    def test_workspace_quantity_commands_update_or_remove_entries(self) -> None:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.mtgwdeck.json"
            increased_path = Path(temp_dir) / "increased.mtgwdeck.json"
            decreased_path = Path(temp_dir) / "decreased.mtgwdeck.json"
            workspace = DeckWorkspace.create_empty(name="Quantity CLI")
            add_entry(workspace, "Arcane Helper", entry_id="qty", quantity=2)
            save_workspace(workspace, input_path)

            with redirect_stdout(io.StringIO()):
                increase_exit_code = main(
                    [
                        "workspace-increase-quantity",
                        str(input_path),
                        "qty",
                        "--amount",
                        "3",
                        "--output",
                        str(increased_path),
                    ]
                )
            with redirect_stdout(io.StringIO()):
                decrease_exit_code = main(
                    [
                        "workspace-decrease-quantity",
                        str(increased_path),
                        "qty",
                        "--amount",
                        "5",
                        "--output",
                        str(decreased_path),
                    ]
                )

            increased_workspace = load_workspace(increased_path)
            decreased_workspace = load_workspace(decreased_path)

        self.assertEqual(increase_exit_code, 0)
        self.assertEqual(decrease_exit_code, 0)
        self.assertEqual(increased_workspace.mainboard[0].quantity, 5)
        self.assertEqual(decreased_workspace.mainboard, [])

    def test_workspace_move_zone_and_set_commander(self) -> None:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.mtgwdeck.json"
            maybe_path = Path(temp_dir) / "maybe.mtgwdeck.json"
            commander_path = Path(temp_dir) / "commander.mtgwdeck.json"
            workspace = DeckWorkspace.create_empty(name="Zone CLI")
            add_entry(workspace, "Arcane Helper", entry_id="zone-card", quantity=4)
            save_workspace(workspace, input_path)

            with redirect_stdout(io.StringIO()):
                move_exit_code = main(
                    [
                        "workspace-move-zone",
                        str(input_path),
                        "zone-card",
                        "--zone",
                        "maybeboard",
                        "--output",
                        str(maybe_path),
                    ]
                )
            with redirect_stdout(io.StringIO()):
                commander_exit_code = main(
                    [
                        "workspace-set-commander",
                        str(maybe_path),
                        "zone-card",
                        "--output",
                        str(commander_path),
                    ]
                )

            maybe_workspace = load_workspace(maybe_path)
            commander_workspace = load_workspace(commander_path)

        self.assertEqual(move_exit_code, 0)
        self.assertEqual(commander_exit_code, 0)
        self.assertEqual(maybe_workspace.maybeboard[0].zone, "maybeboard")
        self.assertEqual(maybe_workspace.maybeboard[0].quantity, 4)
        self.assertEqual(commander_workspace.commanders[0].zone, "commander")
        self.assertEqual(commander_workspace.commanders[0].quantity, 1)

    def test_workspace_mutation_commands_require_native_output_suffix(self) -> None:
        output = io.StringIO()
        errors = io.StringIO()

        with redirect_stdout(output), redirect_stderr(errors):
            exit_code = main(
                [
                    "workspace-add-card",
                    "input.mtgwdeck.json",
                    "Arcane Helper",
                    "--output",
                    "output.json",
                ]
            )

        self.assertEqual(exit_code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("--output must end with .mtgwdeck.json", errors.getvalue())


if __name__ == "__main__":
    unittest.main()

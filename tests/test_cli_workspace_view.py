from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mtg_workbench.cli.main import main
from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace
from mtg_workbench.deckbuilder.serialization import save_workspace


def _entry(
    entry_id: str,
    name: str,
    *,
    quantity: int = 1,
    zone: str = "mainboard",
    categories: list[str] | None = None,
    tags: list[str] | None = None,
    is_unresolved: bool = False,
) -> DeckEntry:
    return DeckEntry(
        entry_id=entry_id,
        quantity=quantity,
        input_name=name,
        display_name=None if is_unresolved else name,
        zone=zone,
        categories=list(categories or []),
        tags=list(tags or []),
        is_unresolved=is_unresolved,
    )


def _workspace() -> DeckWorkspace:
    workspace = DeckWorkspace.create_empty(name="CLI View", deck_id="cli-view")
    workspace.commanders.append(_entry("commander", "Example Commander", zone="commander"))
    workspace.mainboard.append(
        _entry("ramp", "Arcane Helper", quantity=2, categories=["Ramp"], tags=["fast"])
    )
    workspace.mainboard.append(_entry("draw", "Brainstorm Tutor", categories=["Draw"]))
    workspace.maybeboard.append(
        _entry("maybe", "Maybe Mystery", zone="maybeboard", is_unresolved=True)
    )
    return workspace


class CliWorkspaceViewTests(unittest.TestCase):
    def test_workspace_view_prints_projection_without_mutating_file(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_path = Path(temp_dir) / "deck.mtgwdeck.json"
            save_workspace(_workspace(), workspace_path)
            before_text = workspace_path.read_text(encoding="utf-8")
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    [
                        "workspace-view",
                        str(workspace_path),
                        "--group-by",
                        "category",
                        "--sort-by",
                        "quantity",
                    ]
                )

            after_text = workspace_path.read_text(encoding="utf-8")
            payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(after_text, before_text)
        self.assertEqual(payload["schema_version"], "deck_workspace_view_projection.v0")
        self.assertEqual(payload["deck_id"], "cli-view")
        self.assertEqual(payload["group_by"], "category")
        self.assertEqual(payload["sort_by"], "quantity")
        self.assertEqual(payload["visible_entry_count"], 4)
        groups = {group["label"]: [entry["entry_id"] for entry in group["entries"]] for group in payload["groups"]}
        self.assertEqual(groups["Ramp"], ["ramp"])
        self.assertEqual(groups["Uncategorized"], ["commander", "maybe"])

    def test_workspace_view_supports_filter_and_zone_options(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_path = Path(temp_dir) / "deck.mtgwdeck.json"
            save_workspace(_workspace(), workspace_path)
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    [
                        "workspace-view",
                        str(workspace_path),
                        "--group-by",
                        "full deck",
                        "--filter",
                        "FAST",
                        "--zone",
                        "mainboard",
                    ]
                )

            payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["group_by"], "full_deck")
        self.assertEqual(payload["filter_text"], "fast")
        self.assertEqual(payload["visible_entry_count"], 1)
        self.assertEqual(payload["groups"][0]["entries"][0]["entry_id"], "ramp")

    def test_workspace_view_uses_local_card_records_for_type_and_mana_value(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_path = Path(temp_dir) / "deck.mtgwdeck.json"
            records_path = Path(temp_dir) / "records.json"
            save_workspace(_workspace(), workspace_path)
            records_path.write_text(
                json.dumps(
                    {
                        "Example Commander": {
                            "name": "Example Commander",
                            "type_line": "Legendary Creature \u2014 Human",
                            "mana_value": 3,
                        },
                        "Arcane Helper": {
                            "name": "Arcane Helper",
                            "type_line": "Artifact",
                            "mana_value": 2,
                        },
                        "Brainstorm Tutor": {
                            "name": "Brainstorm Tutor",
                            "type_line": "Sorcery",
                            "mana_value": 1,
                        },
                    }
                ),
                encoding="utf-8",
            )
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    [
                        "workspace-view",
                        str(workspace_path),
                        "--card-records",
                        str(records_path),
                        "--group-by",
                        "type",
                        "--sort-by",
                        "mana-value",
                    ]
                )

            payload = json.loads(output.getvalue())
            groups = {group["label"]: [entry["entry_id"] for entry in group["entries"]] for group in payload["groups"]}

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["group_by"], "type")
        self.assertEqual(payload["sort_by"], "mana_value")
        self.assertEqual(payload["card_fact_lookup"]["found_count"], 3)
        self.assertEqual(payload["card_fact_lookup"]["missing_count"], 1)
        self.assertEqual(groups["Creature"], ["commander"])
        self.assertEqual(groups["Artifact"], ["ramp"])
        self.assertEqual(groups["Sorcery"], ["draw"])
        self.assertEqual(groups["Missing Card Facts"], ["maybe"])

    def test_workspace_view_uses_local_card_records_for_color_identity(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_path = Path(temp_dir) / "deck.mtgwdeck.json"
            records_path = Path(temp_dir) / "records.json"
            save_workspace(_workspace(), workspace_path)
            records_path.write_text(
                json.dumps(
                    {
                        "Example Commander": {
                            "name": "Example Commander",
                            "colors": ["G"],
                            "color_identity": ["G", "U"],
                        },
                        "Arcane Helper": {
                            "name": "Arcane Helper",
                            "colors": ["G", "U"],
                            "color_identity": ["G", "U"],
                        },
                        "Brainstorm Tutor": {
                            "name": "Brainstorm Tutor",
                            "colors": ["U"],
                            "color_identity": ["U"],
                        },
                    }
                ),
                encoding="utf-8",
            )
            output = io.StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    [
                        "workspace-view",
                        str(workspace_path),
                        "--card-records",
                        str(records_path),
                        "--group-by",
                        "color identity",
                        "--sort-by",
                        "color-identity",
                    ]
                )

            payload = json.loads(output.getvalue())
            groups = {group["label"]: [entry["entry_id"] for entry in group["entries"]] for group in payload["groups"]}

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["group_by"], "color_identity")
        self.assertEqual(payload["sort_by"], "color_identity")
        self.assertEqual(groups["U"], ["draw"])
        self.assertEqual(groups["UG"], ["ramp", "commander"])
        self.assertEqual(groups["Missing Card Facts"], ["maybe"])

    def test_workspace_view_rejects_fact_backed_modes_without_local_card_source(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_path = Path(temp_dir) / "deck.mtgwdeck.json"
            save_workspace(_workspace(), workspace_path)
            errors = io.StringIO()

            with redirect_stdout(io.StringIO()), redirect_stderr(errors):
                exit_code = main(
                    [
                        "workspace-view",
                        str(workspace_path),
                        "--group-by",
                        "mana value",
                    ]
                )

        self.assertEqual(exit_code, 2)
        self.assertIn("require an explicit card_fact_lookup_report", errors.getvalue())

    def test_workspace_view_reports_invalid_projection_mode(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_path = Path(temp_dir) / "deck.mtgwdeck.json"
            save_workspace(_workspace(), workspace_path)
            errors = io.StringIO()

            with redirect_stdout(io.StringIO()), redirect_stderr(errors):
                exit_code = main(
                    [
                        "workspace-view",
                        str(workspace_path),
                        "--group-by",
                        "price",
                    ]
                )

        self.assertEqual(exit_code, 2)
        self.assertIn("Unsupported group_by", errors.getvalue())

    def test_workspace_view_requires_native_existing_file(self) -> None:
        errors = io.StringIO()

        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            suffix_exit_code = main(["workspace-view", "deck.json"])

        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            missing_exit_code = main(["workspace-view", "missing.mtgwdeck.json"])

        self.assertEqual(suffix_exit_code, 2)
        self.assertEqual(missing_exit_code, 2)
        self.assertIn("workspace_path must end with .mtgwdeck.json", errors.getvalue())
        self.assertIn("workspace_path does not exist or is not a file", errors.getvalue())


if __name__ == "__main__":
    unittest.main()

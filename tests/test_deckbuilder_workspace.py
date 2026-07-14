import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace
from mtg_workbench.deckbuilder.serialization import (
    dumps_workspace,
    is_native_workspace_path,
    load_workspace,
    loads_workspace,
    save_workspace,
)
from mtg_workbench.deckbuilder.validation import WorkspaceValidationError


FIXTURE_ROOT = Path(__file__).parent / "fixtures"
WORKSPACE_FIXTURE = FIXTURE_ROOT / "deckbuilder" / "sample_workspace.mtgwdeck.json"


class DeckbuilderWorkspaceTests(unittest.TestCase):
    def test_create_empty_workspace(self) -> None:
        workspace = DeckWorkspace.create_empty(
            name="New Commander Deck",
            deck_id="deck-empty",
            created_at="2026-07-10T00:00:00Z",
            tags=["draft"],
        )

        self.assertEqual(workspace.schema_version, 1)
        self.assertEqual(workspace.deck_id, "deck-empty")
        self.assertEqual(workspace.name, "New Commander Deck")
        self.assertEqual(workspace.format, "commander")
        self.assertEqual(workspace.tags, ["draft"])
        self.assertEqual(workspace.commanders, [])
        self.assertEqual(workspace.mainboard, [])
        self.assertEqual(workspace.maybeboard, [])
        self.assertEqual(workspace.saved_state, {"is_dirty": False})

    def test_serializing_and_loading_workspace_preserves_sections(self) -> None:
        workspace = load_workspace(WORKSPACE_FIXTURE)

        self.assertEqual(workspace.commanders[0].display_name, "Example Commander")
        self.assertEqual(workspace.commanders[0].zone, "commander")
        self.assertEqual(workspace.mainboard[0].display_name, "Example Ramp")
        self.assertEqual(workspace.mainboard[0].quantity, 2)
        self.assertEqual(workspace.mainboard[0].zone, "mainboard")
        self.assertEqual(workspace.maybeboard[0].display_name, "Maybe Card")
        self.assertEqual(workspace.maybeboard[0].zone, "maybeboard")

    def test_preserves_unknown_cards_and_entry_annotations(self) -> None:
        workspace = load_workspace(WORKSPACE_FIXTURE)
        unknown_entry = workspace.mainboard[1]

        self.assertEqual(unknown_entry.input_name, "Mystery Card")
        self.assertIsNone(unknown_entry.display_name)
        self.assertIsNone(unknown_entry.oracle_id)
        self.assertTrue(unknown_entry.is_unresolved)
        self.assertEqual(unknown_entry.categories, ["Unknown"])
        self.assertEqual(unknown_entry.tags, ["needs-review"])
        self.assertEqual(unknown_entry.notes, "Unknown card should be preserved.")

    def test_save_and_load_workspace_round_trip(self) -> None:
        workspace = load_workspace(WORKSPACE_FIXTURE)

        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "round-trip.mtgwdeck.json"
            save_workspace(workspace, path)
            loaded = load_workspace(path)

        self.assertEqual(loaded.to_dict(), workspace.to_dict())
        self.assertTrue(is_native_workspace_path("round-trip.mtgwdeck.json"))

    def test_stable_json_round_trip(self) -> None:
        workspace = load_workspace(WORKSPACE_FIXTURE)
        first = dumps_workspace(workspace)
        second = dumps_workspace(loads_workspace(first))

        self.assertEqual(first, second)
        self.assertEqual(list(json.loads(first).keys()), sorted(json.loads(first).keys()))

    def test_extra_fields_round_trip_without_loss(self) -> None:
        workspace = load_workspace(WORKSPACE_FIXTURE)
        payload = workspace.to_dict()
        payload["future_workspace_field"] = {"kept": True}
        payload["mainboard"][0]["future_entry_field"] = "keep me"

        loaded = loads_workspace(json.dumps(payload))
        round_tripped = loaded.to_dict()

        self.assertEqual(round_tripped["future_workspace_field"], {"kept": True})
        self.assertEqual(round_tripped["mainboard"][0]["future_entry_field"], "keep me")

    def test_model_objects_can_be_serialized_directly(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Manual Workspace", deck_id="deck-manual")
        workspace.commanders.append(
            DeckEntry(
                entry_id="entry-1",
                quantity=1,
                input_name="Manual Commander",
                display_name="Manual Commander",
                oracle_id="oracle-manual",
                selected_printing_id=None,
                zone="commander",
                categories=["Commander"],
                tags=["manual"],
                notes="Created in test.",
            )
        )

        loaded = loads_workspace(dumps_workspace(workspace))

        self.assertEqual(loaded.commanders[0].entry_id, "entry-1")
        self.assertEqual(loaded.commanders[0].categories, ["Commander"])
        self.assertEqual(loaded.commanders[0].tags, ["manual"])
        self.assertEqual(loaded.commanders[0].notes, "Created in test.")

    def test_entry_category_metadata_round_trips(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Category Metadata", deck_id="deck-category-metadata")
        workspace.mainboard.append(
            DeckEntry(
                entry_id="entry-category",
                quantity=1,
                input_name="Arcane Helper",
                display_name="Arcane Helper",
                zone="mainboard",
                categories=["Draw"],
                tags=["test"],
                imported_category="Card Draw",
                normalized_category="Draw",
                generic_category_hint="Draw",
                deck_specific_primary_role="Card Advantage",
                secondary_tags=["cantrip", "engine-support"],
                category_origin="normalized",
                notes="Preserve provenance.",
            )
        )

        loaded = loads_workspace(dumps_workspace(workspace))
        entry = loaded.mainboard[0]

        self.assertEqual(entry.imported_category, "Card Draw")
        self.assertEqual(entry.normalized_category, "Draw")
        self.assertEqual(entry.generic_category_hint, "Draw")
        self.assertEqual(entry.deck_specific_primary_role, "Card Advantage")
        self.assertEqual(entry.secondary_tags, ["cantrip", "engine-support"])
        self.assertEqual(entry.category_origin, "normalized")
        self.assertEqual(entry.notes, "Preserve provenance.")

    def test_malformed_json_reports_clear_error(self) -> None:
        with self.assertRaises(WorkspaceValidationError) as context:
            loads_workspace("{not valid json")

        self.assertIn("Malformed workspace JSON", str(context.exception))

    def test_missing_required_fields_report_clear_error(self) -> None:
        missing_required = FIXTURE_ROOT / "deckbuilder" / "missing_required_workspace.mtgwdeck.json"

        with self.assertRaises(WorkspaceValidationError) as context:
            load_workspace(missing_required)

        self.assertIn("Missing required workspace field: deck_id.", str(context.exception))

    def test_zone_mismatch_reports_clear_error(self) -> None:
        payload = load_workspace(WORKSPACE_FIXTURE).to_dict()
        payload["mainboard"][0]["zone"] = "maybeboard"

        with self.assertRaises(WorkspaceValidationError) as context:
            loads_workspace(json.dumps(payload))

        self.assertIn("mainboard[0].zone is 'maybeboard'", str(context.exception))

    def test_malformed_category_metadata_reports_clear_errors(self) -> None:
        payload = load_workspace(WORKSPACE_FIXTURE).to_dict()
        payload["mainboard"][0]["secondary_tags"] = ["valid", 123]
        payload["mainboard"][0]["category_origin"] = "invented"

        with self.assertRaises(WorkspaceValidationError) as context:
            loads_workspace(json.dumps(payload))

        self.assertIn("mainboard[0].secondary_tags[1] must be a string.", str(context.exception))
        self.assertIn("mainboard[0].category_origin must be one of", str(context.exception))


    def test_duplicate_entry_ids_inside_same_zone_are_rejected(self) -> None:
        payload = load_workspace(WORKSPACE_FIXTURE).to_dict()
        payload["mainboard"][1]["entry_id"] = payload["mainboard"][0]["entry_id"]

        with self.assertRaises(WorkspaceValidationError) as context:
            loads_workspace(json.dumps(payload))

        self.assertIn(
            "Duplicate entry_id",
            str(context.exception),
        )
        self.assertIn(
            payload["mainboard"][0]["entry_id"],
            str(context.exception),
        )

    def test_duplicate_entry_ids_across_zones_are_rejected(self) -> None:
        payload = load_workspace(WORKSPACE_FIXTURE).to_dict()
        payload["mainboard"][0]["entry_id"] = payload["commanders"][0]["entry_id"]

        with self.assertRaises(WorkspaceValidationError) as context:
            loads_workspace(json.dumps(payload))

        self.assertIn(
            "Duplicate entry_id",
            str(context.exception),
        )
        self.assertIn(
            payload["commanders"][0]["entry_id"],
            str(context.exception),
        )



    def test_failed_save_preserves_existing_file_and_dirty_state(self) -> None:
        workspace = load_workspace(WORKSPACE_FIXTURE)
        workspace.saved_state["is_dirty"] = True

        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "deck.mtgwdeck.json"
            path.write_text("original contents\n", encoding="utf-8")

            original_replace = Path.replace

            def fail_replace(self: Path, target: Path) -> Path:
                raise OSError("simulated replace failure")

            Path.replace = fail_replace
            try:
                with self.assertRaisesRegex(OSError, "simulated replace failure"):
                    save_workspace(workspace, path)
            finally:
                Path.replace = original_replace

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                "original contents\n",
            )
            self.assertTrue(workspace.saved_state["is_dirty"])
            self.assertFalse(path.with_name(f"{path.name}.tmp").exists())


if __name__ == "__main__":
    unittest.main()

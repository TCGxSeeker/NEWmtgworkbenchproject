import unittest

from mtg_workbench.deckbuilder.models import DeckWorkspace
from mtg_workbench.deckbuilder.mutations import (
    WorkspaceMutationError,
    add_entry,
    decrease_quantity,
    find_entry,
    increase_quantity,
    list_entries,
    move_category,
    move_zone,
    remove_entry,
    set_commander,
    update_notes,
    update_tags,
)
from mtg_workbench.deckbuilder.serialization import dumps_workspace, loads_workspace


STAMP_ONE = "2026-07-10T01:00:00Z"
STAMP_TWO = "2026-07-10T02:00:00Z"


def _workspace() -> DeckWorkspace:
    return DeckWorkspace.create_empty(name="Mutation Test Deck", deck_id="deck-mutations")


class DeckbuilderMutationTests(unittest.TestCase):
    def test_add_entry_to_mainboard_by_default(self) -> None:
        workspace = _workspace()

        returned = add_entry(
            workspace,
            "Example Ramp",
            display_name="Example Ramp",
            quantity=2,
            entry_id="main-1",
            categories=["Ramp"],
            tags=["test"],
            notes="Mainboard note.",
            updated_at=STAMP_ONE,
        )

        self.assertIs(returned, workspace)
        self.assertEqual(len(workspace.mainboard), 1)
        self.assertEqual(workspace.mainboard[0].zone, "mainboard")
        self.assertEqual(workspace.mainboard[0].quantity, 2)
        self.assertEqual(workspace.mainboard[0].categories, ["Ramp"])
        self.assertEqual(workspace.mainboard[0].tags, ["test"])
        self.assertEqual(workspace.mainboard[0].notes, "Mainboard note.")
        self.assertEqual(workspace.updated_at, STAMP_ONE)
        self.assertTrue(workspace.saved_state["is_dirty"])

    def test_add_entry_preserves_category_metadata(self) -> None:
        workspace = _workspace()

        add_entry(
            workspace,
            "Arcane Helper",
            display_name="Arcane Helper",
            entry_id="category-metadata",
            categories=["Draw"],
            imported_category="Card Draw",
            normalized_category="Draw",
            generic_category_hint="Draw",
            deck_specific_primary_role="Card Advantage",
            secondary_tags=["cantrip", "setup"],
            category_origin="normalized",
            updated_at=STAMP_ONE,
        )

        entry = workspace.mainboard[0]
        self.assertEqual(entry.imported_category, "Card Draw")
        self.assertEqual(entry.normalized_category, "Draw")
        self.assertEqual(entry.generic_category_hint, "Draw")
        self.assertEqual(entry.deck_specific_primary_role, "Card Advantage")
        self.assertEqual(entry.secondary_tags, ["cantrip", "setup"])
        self.assertEqual(entry.category_origin, "normalized")

    def test_add_entry_to_commander(self) -> None:
        workspace = _workspace()

        add_entry(
            workspace,
            "Example Commander",
            display_name="Example Commander",
            entry_id="commander-1",
            zone="commander",
            categories=["Commander"],
            updated_at=STAMP_ONE,
        )

        self.assertEqual(len(workspace.commanders), 1)
        self.assertEqual(workspace.commanders[0].entry_id, "commander-1")
        self.assertEqual(workspace.commanders[0].zone, "commander")

    def test_add_entry_to_maybeboard(self) -> None:
        workspace = _workspace()

        add_entry(
            workspace,
            "Maybe Card",
            display_name="Maybe Card",
            entry_id="maybe-1",
            zone="maybeboard",
            updated_at=STAMP_ONE,
        )

        self.assertEqual(len(workspace.maybeboard), 1)
        self.assertEqual(workspace.maybeboard[0].entry_id, "maybe-1")
        self.assertEqual(workspace.maybeboard[0].zone, "maybeboard")

    def test_generated_entry_id_when_missing(self) -> None:
        workspace = _workspace()

        add_entry(workspace, "Generated Id Card", updated_at=STAMP_ONE)

        self.assertEqual(len(workspace.mainboard), 1)
        self.assertTrue(workspace.mainboard[0].entry_id)

    def test_preserve_supplied_entry_id(self) -> None:
        workspace = _workspace()

        add_entry(workspace, "Supplied Id Card", entry_id="supplied-entry", updated_at=STAMP_ONE)

        self.assertEqual(workspace.mainboard[0].entry_id, "supplied-entry")

    def test_remove_entry_by_entry_id(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Remove Me", entry_id="remove-me", updated_at=STAMP_ONE)

        remove_entry(workspace, "remove-me", updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard, [])
        self.assertEqual(workspace.updated_at, STAMP_TWO)

    def test_remove_missing_entry_reports_clear_error(self) -> None:
        workspace = _workspace()

        with self.assertRaises(WorkspaceMutationError) as context:
            remove_entry(workspace, "missing-entry", updated_at=STAMP_ONE)

        self.assertIn("Entry not found: missing-entry.", str(context.exception))

    def test_increase_quantity(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Increase Me", entry_id="increase-me", quantity=1, updated_at=STAMP_ONE)

        increase_quantity(workspace, "increase-me", increment=3, updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard[0].quantity, 4)
        self.assertEqual(workspace.updated_at, STAMP_TWO)

    def test_increase_rejects_invalid_increment(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Increase Me", entry_id="increase-me", updated_at=STAMP_ONE)

        with self.assertRaises(WorkspaceMutationError) as context:
            increase_quantity(workspace, "increase-me", increment=0, updated_at=STAMP_TWO)

        self.assertIn("increment must be at least 1.", str(context.exception))

    def test_decrease_quantity(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Decrease Me", entry_id="decrease-me", quantity=4, updated_at=STAMP_ONE)

        decrease_quantity(workspace, "decrease-me", decrement=2, updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard[0].quantity, 2)

    def test_decrease_to_zero_removes_entry(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Remove By Decrease", entry_id="zero-me", quantity=2, updated_at=STAMP_ONE)

        decrease_quantity(workspace, "zero-me", decrement=2, updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard, [])

    def test_decrease_rejects_invalid_decrement(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Decrease Me", entry_id="decrease-me", updated_at=STAMP_ONE)

        with self.assertRaises(WorkspaceMutationError) as context:
            decrease_quantity(workspace, "decrease-me", decrement=-1, updated_at=STAMP_TWO)

        self.assertIn("decrement must be at least 1.", str(context.exception))

    def test_move_mainboard_entry_to_commander_sets_quantity_to_one(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Future Commander", entry_id="future-commander", quantity=4, updated_at=STAMP_ONE)

        move_zone(workspace, "future-commander", "commander", updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard, [])
        self.assertEqual(workspace.commanders[0].entry_id, "future-commander")
        self.assertEqual(workspace.commanders[0].zone, "commander")
        self.assertEqual(workspace.commanders[0].quantity, 1)

    def test_move_commander_entry_to_mainboard(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Commander", entry_id="commander", zone="commander", updated_at=STAMP_ONE)

        move_zone(workspace, "commander", "mainboard", updated_at=STAMP_TWO)

        self.assertEqual(workspace.commanders, [])
        self.assertEqual(workspace.mainboard[0].entry_id, "commander")
        self.assertEqual(workspace.mainboard[0].zone, "mainboard")

    def test_move_entry_to_maybeboard(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Maybe Later", entry_id="maybe-later", updated_at=STAMP_ONE)

        move_zone(workspace, "maybe-later", "maybeboard", updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard, [])
        self.assertEqual(workspace.maybeboard[0].entry_id, "maybe-later")
        self.assertEqual(workspace.maybeboard[0].zone, "maybeboard")

    def test_set_commander_convenience_helper(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Commander Helper", entry_id="helper", quantity=3, updated_at=STAMP_ONE)

        set_commander(workspace, "helper", updated_at=STAMP_TWO)

        self.assertEqual(workspace.commanders[0].entry_id, "helper")
        self.assertEqual(workspace.commanders[0].quantity, 1)

    def test_move_category_replaces_categories_and_preserves_tags_notes(self) -> None:
        workspace = _workspace()
        add_entry(
            workspace,
            "Category Card",
            entry_id="category-card",
            categories=["Old"],
            tags=["keep"],
            notes="Keep this.",
            updated_at=STAMP_ONE,
        )

        move_category(workspace, "category-card", ["Ramp", "Draw"], updated_at=STAMP_TWO)

        entry = workspace.mainboard[0]
        self.assertEqual(entry.categories, ["Ramp", "Draw"])
        self.assertEqual(entry.tags, ["keep"])
        self.assertEqual(entry.notes, "Keep this.")

    def test_update_tags_replaces_adds_and_removes_with_stable_order(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Tagged Card", entry_id="tagged", tags=["old"], updated_at=STAMP_ONE)

        update_tags(workspace, "tagged", tags=["new", "new", "keep"], updated_at=STAMP_TWO)
        update_tags(workspace, "tagged", add=["extra", "new"], remove=["keep"], updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard[0].tags, ["new", "extra"])

    def test_update_notes_sets_and_clears_notes(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Notes Card", entry_id="notes", updated_at=STAMP_ONE)

        update_notes(workspace, "notes", "New note.", updated_at=STAMP_TWO)
        self.assertEqual(workspace.mainboard[0].notes, "New note.")

        update_notes(workspace, "notes", None, updated_at=STAMP_TWO)
        self.assertIsNone(workspace.mainboard[0].notes)

    def test_mutation_updates_timestamp_and_marks_dirty(self) -> None:
        workspace = _workspace()
        self.assertFalse(workspace.saved_state["is_dirty"])

        add_entry(workspace, "Dirty Card", entry_id="dirty", updated_at=STAMP_ONE)

        self.assertEqual(workspace.updated_at, STAMP_ONE)
        self.assertTrue(workspace.saved_state["is_dirty"])

    def test_duplicate_add_merges_when_clearly_identical(self) -> None:
        workspace = _workspace()
        add_entry(
            workspace,
            "Example Ramp",
            display_name="Example Ramp",
            entry_id="ramp-a",
            quantity=1,
            oracle_id="oracle-ramp",
            selected_printing_id="printing-a",
            categories=["Ramp"],
            tags=["first"],
            foil=False,
            updated_at=STAMP_ONE,
        )

        add_entry(
            workspace,
            "Example Ramp",
            display_name="Example Ramp",
            entry_id="ramp-b",
            quantity=2,
            oracle_id="oracle-ramp",
            selected_printing_id="printing-a",
            categories=["Ramp"],
            tags=["second"],
            foil=False,
            updated_at=STAMP_TWO,
        )

        self.assertEqual(len(workspace.mainboard), 1)
        self.assertEqual(workspace.mainboard[0].entry_id, "ramp-a")
        self.assertEqual(workspace.mainboard[0].quantity, 3)
        self.assertEqual(workspace.mainboard[0].tags, ["first", "second"])

    def test_duplicate_add_creates_separate_entries_when_materially_different(self) -> None:
        workspace = _workspace()
        common_kwargs = {
            "input_name": "Flexible Card",
            "display_name": "Flexible Card",
            "oracle_id": "oracle-flex",
            "updated_at": STAMP_ONE,
        }

        add_entry(workspace, entry_id="base", categories=["Ramp"], selected_printing_id="p1", foil=False, **common_kwargs)
        add_entry(workspace, entry_id="different-category", categories=["Draw"], selected_printing_id="p1", foil=False, **common_kwargs)
        add_entry(workspace, entry_id="different-printing", categories=["Ramp"], selected_printing_id="p2", foil=False, **common_kwargs)
        add_entry(workspace, entry_id="different-foil", categories=["Ramp"], selected_printing_id="p1", foil=True, **common_kwargs)
        add_entry(workspace, entry_id="different-zone", zone="maybeboard", categories=["Ramp"], selected_printing_id="p1", foil=False, **common_kwargs)

        self.assertEqual(len(workspace.mainboard), 4)
        self.assertEqual(len(workspace.maybeboard), 1)
        self.assertEqual([entry.quantity for entry in list_entries(workspace)], [1, 1, 1, 1, 1])

    def test_duplicate_add_preserves_separate_entries_when_category_metadata_differs(self) -> None:
        workspace = _workspace()
        common_kwargs = {
            "input_name": "Flexible Card",
            "display_name": "Flexible Card",
            "oracle_id": "oracle-flex",
            "categories": ["Draw"],
            "selected_printing_id": "p1",
            "updated_at": STAMP_ONE,
        }

        add_entry(
            workspace,
            entry_id="alias-category",
            imported_category="Card Draw",
            normalized_category="Draw",
            category_origin="normalized",
            **common_kwargs,
        )
        add_entry(
            workspace,
            entry_id="canonical-category",
            imported_category="Draw",
            normalized_category="Draw",
            category_origin="normalized",
            **common_kwargs,
        )

        self.assertEqual(len(workspace.mainboard), 2)
        self.assertEqual([entry.entry_id for entry in workspace.mainboard], ["alias-category", "canonical-category"])

    def test_unresolved_entry_preservation_and_merge_policy(self) -> None:
        workspace = _workspace()

        add_entry(
            workspace,
            "Mystery Card",
            entry_id="mystery-a",
            categories=["Unknown"],
            tags=["needs-review"],
            notes="Keep unresolved.",
            is_unresolved=True,
            updated_at=STAMP_ONE,
        )
        add_entry(
            workspace,
            "  mystery   card ",
            entry_id="mystery-b",
            categories=["Unknown"],
            is_unresolved=True,
            updated_at=STAMP_TWO,
        )

        self.assertEqual(len(workspace.mainboard), 1)
        self.assertEqual(workspace.mainboard[0].entry_id, "mystery-a")
        self.assertEqual(workspace.mainboard[0].quantity, 2)
        self.assertTrue(workspace.mainboard[0].is_unresolved)
        self.assertEqual(workspace.mainboard[0].input_name, "Mystery Card")
        self.assertEqual(workspace.mainboard[0].tags, ["needs-review"])
        self.assertEqual(workspace.mainboard[0].notes, "Keep unresolved.")

    def test_native_workspace_round_trip_after_mutations(self) -> None:
        workspace = _workspace()
        add_entry(workspace, "Round Trip Card", entry_id="round-trip", updated_at=STAMP_ONE)
        update_tags(workspace, "round-trip", add=["saved"], updated_at=STAMP_TWO)

        loaded = loads_workspace(dumps_workspace(workspace))

        self.assertEqual(loaded.to_dict(), workspace.to_dict())

    def test_find_entry_returns_none_when_missing(self) -> None:
        self.assertIsNone(find_entry(_workspace(), "missing"))


if __name__ == "__main__":
    unittest.main()

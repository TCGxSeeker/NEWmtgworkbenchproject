from pathlib import Path
import unittest

from mtg_workbench.deckbuilder.categories import load_category_taxonomy
from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace
from mtg_workbench.deckbuilder.mutations import (
    WorkspaceMutationError,
    add_entry,
    add_secondary_tag,
    clear_category_metadata,
    decrease_quantity,
    find_entry,
    increase_quantity,
    list_entries,
    move_category,
    move_zone,
    remove_secondary_tag,
    remove_entry,
    replace_secondary_tags,
    set_commander,
    set_category_origin,
    set_deck_specific_primary_role,
    set_generic_category_hint,
    set_imported_category,
    set_normalized_category,
    update_notes,
    update_tags,
)
from mtg_workbench.deckbuilder.serialization import dumps_workspace, loads_workspace


STAMP_ONE = "2026-07-10T01:00:00Z"
STAMP_TWO = "2026-07-10T02:00:00Z"
TAXONOMY_FIXTURE = Path(__file__).parent.parent / "data" / "fixtures" / "categories" / "category_taxonomy.example.yaml"


def _workspace() -> DeckWorkspace:
    return DeckWorkspace.create_empty(name="Mutation Test Deck", deck_id="deck-mutations")


def _workspace_with_category_metadata_entry() -> DeckWorkspace:
    workspace = _workspace()
    add_entry(
        workspace,
        "Arcane Helper",
        display_name="Arcane Helper",
        entry_id="category-card",
        categories=["Draw"],
        imported_category="Card Draw",
        normalized_category="Draw",
        generic_category_hint="Draw",
        deck_specific_primary_role="Card Advantage",
        secondary_tags=["setup"],
        category_origin="normalized",
        updated_at=STAMP_ONE,
    )
    workspace.saved_state["is_dirty"] = False
    workspace.updated_at = STAMP_ONE
    return workspace


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

    def test_supplied_entry_id_is_trimmed(self) -> None:
        workspace = _workspace()

        add_entry(
            workspace,
            "Trimmed Id Card",
            entry_id="  supplied-entry  ",
            updated_at=STAMP_ONE,
        )

        self.assertEqual(workspace.mainboard[0].entry_id, "supplied-entry")

    def test_add_entry_rejects_non_string_supplied_entry_id(self) -> None:
        workspace = _workspace()

        with self.assertRaisesRegex(
            WorkspaceMutationError,
            "entry_id must be a non-empty string",
        ):
            add_entry(
                workspace,
                "Invalid Id Card",
                entry_id=123,
                updated_at=STAMP_ONE,
            )

        self.assertEqual(workspace.mainboard, [])

    def test_add_entry_rejects_blank_supplied_entry_id(self) -> None:
        workspace = _workspace()

        with self.assertRaisesRegex(
            WorkspaceMutationError,
            "entry_id must be a non-empty string",
        ):
            add_entry(
                workspace,
                "Blank Id Card",
                entry_id="   ",
                updated_at=STAMP_ONE,
            )

        self.assertEqual(workspace.mainboard, [])

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

    def test_set_imported_category_preserves_grouping_marks_dirty_and_updates_timestamp(self) -> None:
        workspace = _workspace_with_category_metadata_entry()

        returned = set_imported_category(workspace, "category-card", "Draw Spells", updated_at=STAMP_TWO)

        entry = workspace.mainboard[0]
        self.assertIs(returned, workspace)
        self.assertEqual(entry.imported_category, "Draw Spells")
        self.assertEqual(entry.categories, ["Draw"])
        self.assertTrue(workspace.saved_state["is_dirty"])
        self.assertEqual(workspace.updated_at, STAMP_TWO)

    def test_set_normalized_category_validates_with_taxonomy_when_supplied(self) -> None:
        workspace = _workspace_with_category_metadata_entry()
        taxonomy = load_category_taxonomy(TAXONOMY_FIXTURE)

        set_normalized_category(workspace, "category-card", "Ramp", category_taxonomy=taxonomy, updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard[0].normalized_category, "Ramp")
        self.assertEqual(workspace.mainboard[0].categories, ["Draw"])

        with self.assertRaises(WorkspaceMutationError) as context:
            set_normalized_category(workspace, "category-card", "Card Draw", category_taxonomy=taxonomy, updated_at=STAMP_TWO)

        self.assertIn("normalized_category must be a canonical category", str(context.exception))

    def test_set_normalized_category_without_taxonomy_preserves_value_without_guessing(self) -> None:
        workspace = _workspace_with_category_metadata_entry()

        set_normalized_category(workspace, "category-card", "Personal Bucket", updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard[0].normalized_category, "Personal Bucket")

    def test_set_generic_category_hint(self) -> None:
        workspace = _workspace_with_category_metadata_entry()

        set_generic_category_hint(workspace, "category-card", "Selection", updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard[0].generic_category_hint, "Selection")
        self.assertEqual(workspace.mainboard[0].categories, ["Draw"])

    def test_set_deck_specific_primary_role_placeholder(self) -> None:
        workspace = _workspace_with_category_metadata_entry()

        set_deck_specific_primary_role(workspace, "category-card", "Engine Setup", updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard[0].deck_specific_primary_role, "Engine Setup")
        self.assertEqual(workspace.mainboard[0].categories, ["Draw"])

    def test_set_category_origin_validates_known_origin(self) -> None:
        workspace = _workspace_with_category_metadata_entry()

        set_category_origin(workspace, "category-card", "user", updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard[0].category_origin, "user")

        with self.assertRaises(WorkspaceMutationError) as context:
            set_category_origin(workspace, "category-card", "invented", updated_at=STAMP_TWO)

        self.assertIn("category_origin must be one of", str(context.exception))

    def test_add_secondary_tag_with_stable_deduplication(self) -> None:
        workspace = _workspace_with_category_metadata_entry()

        add_secondary_tag(workspace, "category-card", "cantrip", updated_at=STAMP_TWO)
        add_secondary_tag(workspace, "category-card", "setup", updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard[0].secondary_tags, ["setup", "cantrip"])

    def test_remove_secondary_tag(self) -> None:
        workspace = _workspace_with_category_metadata_entry()
        replace_secondary_tags(workspace, "category-card", ["setup", "cantrip"], updated_at=STAMP_TWO)

        remove_secondary_tag(workspace, "category-card", "setup", updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard[0].secondary_tags, ["cantrip"])

    def test_replace_secondary_tags(self) -> None:
        workspace = _workspace_with_category_metadata_entry()

        replace_secondary_tags(workspace, "category-card", ["engine", "engine", "payoff"], updated_at=STAMP_TWO)

        self.assertEqual(workspace.mainboard[0].secondary_tags, ["engine", "payoff"])

    def test_clear_category_metadata_preserves_grouping_category(self) -> None:
        workspace = _workspace_with_category_metadata_entry()

        clear_category_metadata(workspace, "category-card", updated_at=STAMP_TWO)

        entry = workspace.mainboard[0]
        self.assertEqual(entry.categories, ["Draw"])
        self.assertIsNone(entry.imported_category)
        self.assertIsNone(entry.normalized_category)
        self.assertIsNone(entry.generic_category_hint)
        self.assertIsNone(entry.deck_specific_primary_role)
        self.assertEqual(entry.secondary_tags, [])
        self.assertIsNone(entry.category_origin)
        self.assertTrue(workspace.saved_state["is_dirty"])
        self.assertEqual(workspace.updated_at, STAMP_TWO)

    def test_category_metadata_helpers_raise_clear_error_for_missing_entry(self) -> None:
        with self.assertRaises(WorkspaceMutationError) as context:
            set_imported_category(_workspace(), "missing-entry", "Draw", updated_at=STAMP_TWO)

        self.assertIn("Entry not found: missing-entry.", str(context.exception))

    def test_category_metadata_helpers_reject_invalid_value_shapes(self) -> None:
        workspace = _workspace_with_category_metadata_entry()

        with self.assertRaises(WorkspaceMutationError) as context:
            replace_secondary_tags(workspace, "category-card", ["valid", 123], updated_at=STAMP_TWO)

        self.assertIn("secondary_tags must contain only strings.", str(context.exception))

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


    def test_add_entry_rejects_supplied_id_owned_by_different_entry(self) -> None:
        workspace = _workspace()
        add_entry(
            workspace,
            "First Card",
            display_name="First Card",
            entry_id="shared-id",
            updated_at=STAMP_ONE,
        )

        with self.assertRaises(WorkspaceMutationError) as context:
            add_entry(
                workspace,
                "Different Card",
                display_name="Different Card",
                entry_id="shared-id",
                updated_at=STAMP_TWO,
            )

        self.assertIn("entry_id already exists: shared-id.", str(context.exception))
        self.assertEqual(len(workspace.mainboard), 1)
        self.assertEqual(workspace.mainboard[0].display_name, "First Card")
        self.assertEqual(workspace.mainboard[0].quantity, 1)

    def test_merge_rejects_incoming_id_owned_by_another_entry(self) -> None:
        workspace = _workspace()
        add_entry(
            workspace,
            "Merge Target",
            display_name="Merge Target",
            entry_id="merge-target",
            oracle_id="oracle-target",
            selected_printing_id="printing-target",
            categories=["Ramp"],
            updated_at=STAMP_ONE,
        )
        add_entry(
            workspace,
            "Other Entry",
            display_name="Other Entry",
            entry_id="already-owned",
            oracle_id="oracle-other",
            selected_printing_id="printing-other",
            categories=["Utility"],
            updated_at=STAMP_ONE,
        )

        with self.assertRaises(WorkspaceMutationError) as context:
            add_entry(
                workspace,
                "Merge Target",
                display_name="Merge Target",
                entry_id="already-owned",
                oracle_id="oracle-target",
                selected_printing_id="printing-target",
                categories=["Ramp"],
                quantity=2,
                updated_at=STAMP_TWO,
            )

        self.assertIn("entry_id already exists: already-owned.", str(context.exception))
        self.assertEqual(len(workspace.mainboard), 2)
        self.assertEqual(find_entry(workspace, "merge-target").quantity, 1)
        self.assertEqual(find_entry(workspace, "already-owned").display_name, "Other Entry")

    def test_identical_merge_with_unused_incoming_id_preserves_existing_id(self) -> None:
        workspace = _workspace()
        add_entry(
            workspace,
            "Merge Card",
            display_name="Merge Card",
            entry_id="original-id",
            oracle_id="oracle-merge",
            selected_printing_id="printing-merge",
            categories=["Draw"],
            updated_at=STAMP_ONE,
        )

        add_entry(
            workspace,
            "Merge Card",
            display_name="Merge Card",
            entry_id="unused-incoming-id",
            oracle_id="oracle-merge",
            selected_printing_id="printing-merge",
            categories=["Draw"],
            quantity=2,
            updated_at=STAMP_TWO,
        )

        self.assertEqual(len(workspace.mainboard), 1)
        self.assertEqual(workspace.mainboard[0].entry_id, "original-id")
        self.assertEqual(workspace.mainboard[0].quantity, 3)
        self.assertIsNone(find_entry(workspace, "unused-incoming-id"))



    def test_find_entry_rejects_ambiguous_in_memory_entry_ids(self) -> None:
        workspace = _workspace()
        workspace.mainboard.append(
            DeckEntry(
                entry_id="duplicate-id",
                quantity=1,
                input_name="First Duplicate",
                display_name="First Duplicate",
                zone="mainboard",
            )
        )
        workspace.maybeboard.append(
            DeckEntry(
                entry_id="duplicate-id",
                quantity=1,
                input_name="Second Duplicate",
                display_name="Second Duplicate",
                zone="maybeboard",
            )
        )

        with self.assertRaises(WorkspaceMutationError) as context:
            find_entry(workspace, "duplicate-id")

        self.assertIn(
            "Multiple entries found for entry_id: duplicate-id.",
            str(context.exception),
        )

    def test_remove_entry_rejects_ambiguous_in_memory_entry_ids(self) -> None:
        workspace = _workspace()
        workspace.mainboard.append(
            DeckEntry(
                entry_id="duplicate-id",
                quantity=1,
                input_name="First Duplicate",
                display_name="First Duplicate",
                zone="mainboard",
            )
        )
        workspace.maybeboard.append(
            DeckEntry(
                entry_id="duplicate-id",
                quantity=1,
                input_name="Second Duplicate",
                display_name="Second Duplicate",
                zone="maybeboard",
            )
        )

        with self.assertRaises(WorkspaceMutationError) as context:
            remove_entry(workspace, "duplicate-id", updated_at=STAMP_TWO)

        self.assertIn(
            "Multiple entries found for entry_id: duplicate-id.",
            str(context.exception),
        )
        self.assertEqual(len(workspace.mainboard), 1)
        self.assertEqual(len(workspace.maybeboard), 1)

    def test_generated_entry_id_retries_after_collision(self) -> None:
        from unittest.mock import patch

        workspace = _workspace()
        add_entry(
            workspace,
            "Existing Card",
            display_name="Existing Card",
            entry_id="collision-id",
            updated_at=STAMP_ONE,
        )

        with patch(
            "mtg_workbench.deckbuilder.mutations.uuid4",
            side_effect=["collision-id", "fresh-id"],
        ):
            add_entry(
                workspace,
                "Generated Card",
                display_name="Generated Card",
                updated_at=STAMP_TWO,
            )

        generated = find_entry(workspace, "fresh-id")
        self.assertIsNotNone(generated)
        self.assertEqual(generated.display_name, "Generated Card")
        self.assertEqual(len(workspace.mainboard), 2)

if __name__ == "__main__":
    unittest.main()

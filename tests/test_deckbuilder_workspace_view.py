import json
import unittest

from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace
from mtg_workbench.deckbuilder.workspace_view import (
    GROUP_CATEGORY,
    GROUP_FULL_DECK,
    GROUP_ZONE,
    SORT_ALPHABET,
    SORT_CATEGORY,
    SORT_QUANTITY,
    SORT_ZONE,
    WorkspaceViewError,
    build_workspace_view_projection,
)


def _entry(
    entry_id: str,
    name: str,
    *,
    quantity: int = 1,
    zone: str = "mainboard",
    categories: list[str] | None = None,
    tags: list[str] | None = None,
    secondary_tags: list[str] | None = None,
    imported_category: str | None = None,
    normalized_category: str | None = None,
    generic_category_hint: str | None = None,
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
        secondary_tags=list(secondary_tags or []),
        imported_category=imported_category,
        normalized_category=normalized_category,
        generic_category_hint=generic_category_hint,
        is_unresolved=is_unresolved,
    )


def _workspace() -> DeckWorkspace:
    workspace = DeckWorkspace.create_empty(name="View Deck", deck_id="view-deck")
    workspace.commanders.append(
        _entry("commander", "Zed Commander", zone="commander", categories=["Commander"])
    )
    workspace.mainboard.append(
        _entry(
            "ramp",
            "Arcane Helper",
            quantity=2,
            categories=["Ramp"],
            tags=["fast"],
        )
    )
    workspace.mainboard.append(
        _entry(
            "draw",
            "Brainstorm Tutor",
            categories=["Draw", "Selection"],
            secondary_tags=["setup"],
            imported_category="Card Draw",
            normalized_category="Draw",
            generic_category_hint="Selection",
        )
    )
    workspace.mainboard.append(_entry("plain", "Plain Card"))
    workspace.maybeboard.append(
        _entry("maybe", "Maybe Mystery", zone="maybeboard", categories=["Ramp"], is_unresolved=True)
    )
    return workspace


class DeckWorkspaceViewProjectionTests(unittest.TestCase):
    def test_full_deck_projection_sorts_by_alphabet_and_serializes_stably(self) -> None:
        projection = build_workspace_view_projection(
            _workspace(),
            group_by=GROUP_FULL_DECK,
            sort_by=SORT_ALPHABET,
        )
        payload = projection.to_dict()

        self.assertEqual(projection.schema_version, "deck_workspace_view_projection.v0")
        self.assertEqual(projection.deck_id, "view-deck")
        self.assertEqual(projection.visible_entry_count, 5)
        self.assertEqual(projection.visible_quantity_total, 6)
        self.assertEqual([group.label for group in projection.groups], ["Full Deck"])
        self.assertEqual(
            [entry.entry_id for entry in projection.groups[0].entries],
            ["ramp", "draw", "maybe", "plain", "commander"],
        )
        self.assertIn("groups", payload)
        json.dumps(payload, sort_keys=True)

    def test_zone_grouping_uses_workspace_zone_order(self) -> None:
        projection = build_workspace_view_projection(
            _workspace(),
            group_by=GROUP_ZONE,
            sort_by=SORT_ZONE,
        )

        self.assertEqual(
            [(group.group_id, [entry.entry_id for entry in group.entries]) for group in projection.groups],
            [
                ("commander", ["commander"]),
                ("mainboard", ["ramp", "draw", "plain"]),
                ("maybeboard", ["maybe"]),
            ],
        )

    def test_category_grouping_allows_multiple_memberships(self) -> None:
        projection = build_workspace_view_projection(
            _workspace(),
            group_by=GROUP_CATEGORY,
            sort_by=SORT_CATEGORY,
        )

        groups = {group.label: [entry.entry_id for entry in group.entries] for group in projection.groups}

        self.assertEqual(list(groups), ["Commander", "Draw", "Ramp", "Selection", "Uncategorized"])
        self.assertEqual(groups["Draw"], ["draw"])
        self.assertEqual(groups["Ramp"], ["ramp", "maybe"])
        self.assertEqual(groups["Selection"], ["draw"])
        self.assertEqual(groups["Uncategorized"], ["plain"])
        self.assertEqual(projection.visible_entry_count, 5)
        self.assertEqual(projection.grouped_entry_count, 6)

    def test_quantity_sort_is_descending_with_alphabetical_tiebreaker(self) -> None:
        projection = build_workspace_view_projection(
            _workspace(),
            group_by=GROUP_FULL_DECK,
            sort_by=SORT_QUANTITY,
        )

        self.assertEqual(
            [entry.entry_id for entry in projection.groups[0].entries],
            ["ramp", "draw", "maybe", "plain", "commander"],
        )

    def test_filter_matches_current_workspace_text_fields(self) -> None:
        tag_projection = build_workspace_view_projection(_workspace(), filter_text="FAST")
        metadata_projection = build_workspace_view_projection(_workspace(), filter_text="card draw")
        unresolved_projection = build_workspace_view_projection(_workspace(), filter_text="mystery")

        self.assertEqual(tag_projection.visible_entry_count, 1)
        self.assertEqual(tag_projection.groups[0].entries[0].entry_id, "ramp")
        self.assertEqual(metadata_projection.visible_entry_count, 1)
        self.assertEqual(metadata_projection.groups[0].entries[0].entry_id, "draw")
        self.assertEqual(unresolved_projection.visible_entry_count, 1)
        self.assertEqual(unresolved_projection.groups[0].entries[0].entry_id, "maybe")

    def test_zone_filter_limits_visible_entries_without_mutating_workspace(self) -> None:
        workspace = _workspace()
        before = workspace.to_dict()

        projection = build_workspace_view_projection(
            workspace,
            group_by=GROUP_FULL_DECK,
            zones=("mainboard",),
        )

        self.assertEqual(projection.visible_entry_count, 3)
        self.assertEqual([entry.zone for entry in projection.groups[0].entries], ["mainboard"] * 3)
        self.assertEqual(workspace.to_dict(), before)

    def test_group_and_sort_modes_accept_readable_aliases(self) -> None:
        projection = build_workspace_view_projection(
            _workspace(),
            group_by="full deck",
            sort_by="quantity",
        )

        self.assertEqual(projection.group_by, GROUP_FULL_DECK)
        self.assertEqual(projection.sort_by, SORT_QUANTITY)

    def test_invalid_modes_and_zones_raise_clear_errors(self) -> None:
        with self.assertRaisesRegex(WorkspaceViewError, "Unsupported group_by"):
            build_workspace_view_projection(_workspace(), group_by="price")

        with self.assertRaisesRegex(WorkspaceViewError, "Unsupported sort_by"):
            build_workspace_view_projection(_workspace(), sort_by="mana_value")

        with self.assertRaisesRegex(WorkspaceViewError, "Invalid zone"):
            build_workspace_view_projection(_workspace(), zones=("sideboard",))

        with self.assertRaisesRegex(WorkspaceViewError, "zones must be an iterable"):
            build_workspace_view_projection(_workspace(), zones="mainboard")


if __name__ == "__main__":
    unittest.main()

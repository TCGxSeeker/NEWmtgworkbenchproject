import unittest

from mtg_workbench.deckbuilder.deck_skeleton_report import build_deck_skeleton_report
from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace


def _entry(
    entry_id: str,
    name: str,
    *,
    quantity: int = 1,
    zone: str = "mainboard",
    categories: list[str] | None = None,
    oracle_id: str | None = None,
    is_unresolved: bool = False,
) -> DeckEntry:
    return DeckEntry(
        entry_id=entry_id,
        quantity=quantity,
        input_name=name,
        display_name=None if is_unresolved else name,
        oracle_id=oracle_id,
        zone=zone,
        categories=list(categories or []),
        tags=[],
        is_unresolved=is_unresolved,
    )


class DeckSkeletonReportTests(unittest.TestCase):
    def test_empty_workspace_produces_stable_report(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Empty Deck", deck_id="deck-empty")

        report = build_deck_skeleton_report(workspace)
        payload = report.to_dict()

        self.assertEqual(report.schema_version, "deck_skeleton_report.v0")
        self.assertEqual(report.deck_id, "deck-empty")
        self.assertEqual(report.zone_entry_counts, {"commander": 0, "mainboard": 0, "maybeboard": 0})
        self.assertEqual(report.zone_quantity_totals, {"commander": 0, "mainboard": 0, "maybeboard": 0})
        self.assertEqual(report.active_quantity_total, 0)
        self.assertEqual(report.card_fact_lookup_status, "not_requested")
        self.assertIn("machine_evidence", payload)
        self.assertIn("mechanical_warnings", payload)

    def test_reports_zone_counts_quantities_and_commanders(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Counters Deck", deck_id="deck-counts")
        workspace.commanders.append(_entry("commander-1", "Example Commander", zone="commander"))
        workspace.mainboard.append(_entry("main-1", "Example Ramp", quantity=2, categories=["Ramp"]))
        workspace.maybeboard.append(_entry("maybe-1", "Maybe Card", zone="maybeboard"))

        report = build_deck_skeleton_report(workspace)

        self.assertEqual(report.zone_entry_counts["commander"], 1)
        self.assertEqual(report.zone_entry_counts["mainboard"], 1)
        self.assertEqual(report.zone_entry_counts["maybeboard"], 1)
        self.assertEqual(report.zone_quantity_totals["mainboard"], 2)
        self.assertEqual(report.active_quantity_total, 3)
        self.assertEqual(report.commander_names, ("Example Commander",))

    def test_active_category_counts_exclude_maybeboard(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Category Deck", deck_id="deck-categories")
        workspace.mainboard.append(_entry("main-1", "Draw Spell", quantity=2, categories=["Draw"]))
        workspace.mainboard.append(_entry("main-2", "No Category"))
        workspace.maybeboard.append(_entry("maybe-1", "Maybe Ramp", zone="maybeboard", categories=["Ramp"]))

        report = build_deck_skeleton_report(workspace)

        self.assertEqual(report.category_entry_counts, {"Draw": 1, "Uncategorized": 1})
        self.assertEqual(report.category_quantity_totals, {"Draw": 2, "Uncategorized": 1})

    def test_reports_unresolved_entries(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Unknown Deck", deck_id="deck-unknown")
        workspace.mainboard.append(_entry("unknown-1", "Mystery Card", is_unresolved=True))

        report = build_deck_skeleton_report(workspace)

        self.assertEqual(len(report.unresolved_entries), 1)
        self.assertEqual(report.unresolved_entries[0].input_name, "Mystery Card")

    def test_without_card_records_does_not_guess_missing_facts(self) -> None:
        workspace = DeckWorkspace.create_empty(name="No Facts Deck", deck_id="deck-no-facts")
        workspace.mainboard.append(_entry("sol-ring", "Sol Ring", quantity=2))

        report = build_deck_skeleton_report(workspace)

        self.assertEqual(report.card_fact_lookup_status, "not_requested")
        self.assertEqual(report.missing_card_fact_entries, ())
        self.assertEqual(report.duplicate_nonbasic_warnings, ())

    def test_with_card_records_reports_missing_facts(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Missing Facts Deck", deck_id="deck-missing-facts")
        workspace.mainboard.append(_entry("known-1", "Sol Ring"))
        workspace.mainboard.append(_entry("missing-1", "Mystery Card"))

        report = build_deck_skeleton_report(
            workspace,
            card_records_by_name={"Sol Ring": {"name": "Sol Ring", "type_line": "Artifact"}},
        )

        self.assertEqual(report.card_fact_lookup_status, "checked")
        self.assertEqual(len(report.missing_card_fact_entries), 1)
        self.assertEqual(report.missing_card_fact_entries[0].entry_id, "missing-1")

    def test_known_nonbasic_duplicate_warns(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Duplicate Deck", deck_id="deck-duplicates")
        workspace.mainboard.append(_entry("sol-ring", "Sol Ring", quantity=2, oracle_id="oracle-sol-ring"))

        report = build_deck_skeleton_report(
            workspace,
            card_records_by_name={"Sol Ring": {"name": "Sol Ring", "type_line": "Artifact"}},
        )

        self.assertEqual(len(report.duplicate_nonbasic_warnings), 1)
        warning = report.duplicate_nonbasic_warnings[0]
        self.assertEqual(warning.display_name, "Sol Ring")
        self.assertEqual(warning.quantity, 2)
        self.assertEqual(warning.entry_ids, ("sol-ring",))

    def test_basic_land_duplicate_does_not_warn(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Land Deck", deck_id="deck-lands")
        workspace.mainboard.append(_entry("island", "Island", quantity=35))

        report = build_deck_skeleton_report(
            workspace,
            card_records_by_name={"Island": {"name": "Island", "type_line": "Basic Land \u2014 Island"}},
        )

        self.assertEqual(report.duplicate_nonbasic_warnings, ())

    def test_duplicate_with_missing_card_facts_does_not_warn(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Unknown Duplicate", deck_id="deck-unknown-dupe")
        workspace.mainboard.append(_entry("unknown", "Mystery Card", quantity=2))

        report = build_deck_skeleton_report(workspace, card_records_by_name={})

        self.assertEqual(len(report.missing_card_fact_entries), 1)
        self.assertEqual(report.duplicate_nonbasic_warnings, ())

    def test_to_dict_keeps_summary_evidence_and_debug_separated(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Debug Deck", deck_id="deck-debug")
        workspace.mainboard.append(_entry("draw", "Draw Spell", categories=["Draw"]))

        payload = build_deck_skeleton_report(workspace).to_dict(include_debug=True)

        self.assertIn("user_summary", payload)
        self.assertIn("machine_evidence", payload)
        self.assertIn("mechanical_warnings", payload)
        self.assertIn("debug_details", payload)
        self.assertIn("entries", payload["debug_details"])


if __name__ == "__main__":
    unittest.main()

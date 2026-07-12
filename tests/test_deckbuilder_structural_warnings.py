import unittest

from mtg_workbench.deckbuilder.deck_skeleton_report import build_deck_skeleton_report
from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace
from mtg_workbench.deckbuilder.structural_warnings import build_structural_warnings_report


def _entry(
    entry_id: str,
    name: str,
    *,
    quantity: int = 1,
    zone: str = "mainboard",
    is_unresolved: bool = False,
) -> DeckEntry:
    return DeckEntry(
        entry_id=entry_id,
        quantity=quantity,
        input_name=name,
        display_name=None if is_unresolved else name,
        zone=zone,
        categories=[],
        tags=[],
        is_unresolved=is_unresolved,
    )


def _commander_workspace(active_mainboard_quantity: int = 99) -> DeckWorkspace:
    workspace = DeckWorkspace.create_empty(name="Warning Deck", deck_id="deck-warnings")
    workspace.commanders.append(_entry("commander", "Example Commander", zone="commander"))
    workspace.mainboard.append(_entry("main", "Main Deck Cards", quantity=active_mainboard_quantity))
    return workspace


class StructuralWarningsTests(unittest.TestCase):
    def test_no_warning_for_commander_shape_with_100_active_cards(self) -> None:
        skeleton = build_deck_skeleton_report(_commander_workspace())

        report = build_structural_warnings_report(skeleton)

        self.assertEqual(report.warning_count, 0)
        self.assertIn("no mechanical structural warnings", report.user_summary)

    def test_missing_commander_warning(self) -> None:
        workspace = DeckWorkspace.create_empty(name="No Commander", deck_id="deck-no-commander")
        workspace.mainboard.append(_entry("main", "Main Deck Cards", quantity=99))

        report = build_structural_warnings_report(build_deck_skeleton_report(workspace))

        self.assertIn("missing_commander", {warning.warning_id for warning in report.warnings})

    def test_commander_active_quantity_mismatch_warning(self) -> None:
        report = build_structural_warnings_report(
            build_deck_skeleton_report(_commander_workspace(active_mainboard_quantity=98))
        )

        warning = _find_warning(report, "commander_active_quantity_mismatch")
        self.assertEqual(warning.machine_evidence["expected_active_quantity"], 100)
        self.assertEqual(warning.machine_evidence["actual_active_quantity"], 99)

    def test_unresolved_entries_warning(self) -> None:
        workspace = _commander_workspace()
        workspace.mainboard.append(_entry("unknown", "Mystery Card", is_unresolved=True))

        report = build_structural_warnings_report(build_deck_skeleton_report(workspace))

        warning = _find_warning(report, "unresolved_entries")
        self.assertEqual(warning.machine_evidence["entry_ids"], ["unknown"])

    def test_missing_card_facts_warning_only_when_skeleton_checked_facts(self) -> None:
        workspace = _commander_workspace()

        report_without_lookup = build_structural_warnings_report(build_deck_skeleton_report(workspace))
        self.assertNotIn(
            "missing_card_facts",
            {warning.warning_id for warning in report_without_lookup.warnings},
        )

        report_with_lookup = build_structural_warnings_report(
            build_deck_skeleton_report(workspace, card_records_by_name={})
        )
        self.assertIn(
            "missing_card_facts",
            {warning.warning_id for warning in report_with_lookup.warnings},
        )

    def test_known_nonbasic_duplicate_warning_is_carried_from_skeleton(self) -> None:
        workspace = _commander_workspace(active_mainboard_quantity=1)
        workspace.mainboard.append(_entry("sol-ring", "Sol Ring", quantity=2))

        report = build_structural_warnings_report(
            build_deck_skeleton_report(
                workspace,
                card_records_by_name={"Sol Ring": {"name": "Sol Ring", "type_line": "Artifact"}},
            )
        )

        warning = _find_warning(report, "duplicate_known_nonbasic")
        self.assertEqual(warning.machine_evidence["display_name"], "Sol Ring")
        self.assertEqual(warning.machine_evidence["quantity"], 2)

    def test_missing_card_facts_do_not_create_duplicate_warning(self) -> None:
        workspace = _commander_workspace(active_mainboard_quantity=1)
        workspace.mainboard.append(_entry("mystery", "Mystery Card", quantity=2))

        report = build_structural_warnings_report(
            build_deck_skeleton_report(workspace, card_records_by_name={})
        )

        self.assertNotIn(
            "duplicate_known_nonbasic",
            {warning.warning_id for warning in report.warnings},
        )

    def test_to_dict_keeps_summary_warnings_and_debug_separated(self) -> None:
        report = build_structural_warnings_report(
            build_deck_skeleton_report(_commander_workspace(active_mainboard_quantity=98))
        )

        payload = report.to_dict(include_debug=True)

        self.assertIn("user_summary", payload)
        self.assertIn("warnings", payload)
        self.assertIn("debug_details", payload)
        self.assertIn("warning_ids", payload["debug_details"])


def _find_warning(report, warning_id):
    for warning in report.warnings:
        if warning.warning_id == warning_id:
            return warning
    raise AssertionError(f"Missing warning: {warning_id}")


if __name__ == "__main__":
    unittest.main()

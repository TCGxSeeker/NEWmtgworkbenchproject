from pathlib import Path
import unittest

from mtg_workbench.cards.catalog import CardCatalog, CardRecord
from mtg_workbench.deckbuilder.deck_inspection_report import (
    DeckInspectionReportError,
    build_deck_inspection_report,
)
from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace
from mtg_workbench.deckbuilder.role_rules import load_role_rules


ROLE_RULES_FIXTURE = Path("data/fixtures/roles/role_rules.example.yaml")


def _entry(
    entry_id: str,
    name: str,
    *,
    quantity: int = 1,
    zone: str = "mainboard",
    categories: list[str] | None = None,
    is_unresolved: bool = False,
) -> DeckEntry:
    return DeckEntry(
        entry_id=entry_id,
        quantity=quantity,
        input_name=name,
        display_name=None if is_unresolved else name,
        zone=zone,
        categories=list(categories or []),
        tags=[],
        is_unresolved=is_unresolved,
    )


def _workspace() -> DeckWorkspace:
    workspace = DeckWorkspace.create_empty(name="Inspection Deck", deck_id="inspection-deck")
    workspace.commanders.append(_entry("commander", "Example Commander", zone="commander"))
    workspace.mainboard.append(_entry("draw", "Draw Spell", categories=["Draw"]))
    workspace.mainboard.append(_entry("missing", "Mystery Card"))
    workspace.mainboard.append(_entry("ambiguous", "Shared Alias"))
    workspace.maybeboard.append(_entry("maybe", "Maybe Card", zone="maybeboard"))
    return workspace


def _card_records() -> list[dict[str, object]]:
    return [
        {
            "name": "Example Commander",
            "type_line": "Legendary Creature - Example",
            "oracle_text": "This fixture commander has no special role text.",
        },
        {
            "name": "Draw Spell",
            "type_line": "Sorcery",
            "oracle_text": "Draw two cards.",
        },
        {
            "name": "Maybe Card",
            "type_line": "Creature - Example",
            "oracle_text": "Maybe card text.",
        },
        {
            "name": "First Alias Card",
            "aliases": ["Shared Alias"],
            "type_line": "Creature - Example",
            "oracle_text": "First possible record.",
            "oracle_id": "oracle-first",
        },
        {
            "name": "Second Alias Card",
            "aliases": ["Shared Alias"],
            "type_line": "Creature - Example",
            "oracle_text": "Second possible record.",
            "oracle_id": "oracle-second",
        },
    ]


class DeckInspectionReportEnvelopeTests(unittest.TestCase):
    def test_builds_without_card_source_and_does_not_guess_missing_facts(self) -> None:
        workspace = _workspace()

        report = build_deck_inspection_report(workspace)
        warning_ids = {
            warning.warning_id
            for warning in report.structural_warnings_report.warnings
        }

        self.assertEqual(report.schema_version, "deck_inspection_report.v0")
        self.assertFalse(report.card_fact_coverage.source_available)
        self.assertFalse(report.card_fact_coverage.lookup_attempted)
        self.assertEqual(report.card_fact_coverage.total_entries_considered, 5)
        self.assertEqual(report.missing_card_count, 0)
        self.assertNotIn("missing_card_facts", warning_ids)
        self.assertIn("card fact lookup not attempted", report.user_summary)

    def test_composes_skeleton_and_structural_warnings(self) -> None:
        workspace = _workspace()

        report = build_deck_inspection_report(workspace)

        self.assertEqual(report.skeleton_report.deck_id, "inspection-deck")
        self.assertEqual(report.skeleton_report.zone_entry_counts["commander"], 1)
        self.assertEqual(report.skeleton_report.zone_entry_counts["mainboard"], 3)
        self.assertGreaterEqual(report.warning_count, 1)
        self.assertIn(
            "commander_active_quantity_mismatch",
            {warning.warning_id for warning in report.structural_warnings_report.warnings},
        )

    def test_reports_found_missing_and_ambiguous_card_fact_coverage(self) -> None:
        workspace = _workspace()

        report = build_deck_inspection_report(
            workspace,
            card_records_by_name=_card_records(),
        )

        self.assertTrue(report.card_fact_coverage.source_available)
        self.assertTrue(report.card_fact_coverage.lookup_attempted)
        self.assertEqual(report.found_card_count, 3)
        self.assertEqual(report.missing_card_count, 1)
        self.assertEqual(report.ambiguous_card_count, 1)
        self.assertEqual(
            report.card_fact_coverage.found_entry_ids,
            ("commander", "draw", "maybe"),
        )
        self.assertEqual(report.card_fact_coverage.missing_entry_ids, ("missing",))
        self.assertEqual(report.card_fact_coverage.ambiguous_entry_ids, ("ambiguous",))

    def test_catalog_source_reports_lookup_coverage(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Catalog Deck", deck_id="catalog-deck")
        workspace.mainboard.append(_entry("alias", "Alias Helper"))
        workspace.mainboard.append(_entry("unknown", "Unknown Card"))
        catalog = CardCatalog.from_json_file("tests/fixtures/cards/tiny_cards.json")

        report = build_deck_inspection_report(workspace, card_catalog=catalog)

        self.assertEqual(report.found_card_count, 1)
        self.assertEqual(report.missing_card_count, 1)
        self.assertEqual(report.card_fact_coverage.found_entry_ids, ("alias",))

    def test_role_evidence_is_optional_and_false_by_default(self) -> None:
        report = build_deck_inspection_report(
            _workspace(),
            card_records_by_name=_card_records(),
        )

        self.assertEqual(report.card_role_reports, ())
        self.assertEqual(report.card_role_report_count, 0)

    def test_role_evidence_requires_ruleset_when_requested(self) -> None:
        with self.assertRaisesRegex(DeckInspectionReportError, "ruleset is required"):
            build_deck_inspection_report(
                _workspace(),
                card_records_by_name=_card_records(),
                include_card_role_evidence=True,
            )

    def test_optional_role_evidence_uses_only_found_records(self) -> None:
        ruleset = load_role_rules(ROLE_RULES_FIXTURE)

        report = build_deck_inspection_report(
            _workspace(),
            card_records_by_name=_card_records(),
            ruleset=ruleset,
            include_card_role_evidence=True,
        )

        self.assertEqual(
            [role_report.entry_id for role_report in report.card_role_reports],
            ["commander", "draw", "maybe"],
        )
        draw_report = next(
            role_report
            for role_report in report.card_role_reports
            if role_report.entry_id == "draw"
        )
        self.assertIsNotNone(draw_report.role_report.best_match)
        self.assertEqual(draw_report.role_report.best_match.role_id, "draw")

    def test_to_dict_keeps_summary_evidence_and_debug_separated(self) -> None:
        report = build_deck_inspection_report(
            _workspace(),
            card_records_by_name=_card_records(),
        )

        payload = report.to_dict()
        debug_payload = report.to_dict(include_debug=True)

        self.assertIn("user_summary", payload)
        self.assertIn("machine_evidence", payload)
        self.assertIn("card_fact_coverage", payload)
        self.assertIn("card_role_reports", payload)
        self.assertNotIn("debug_details", payload)
        self.assertIn("debug_details", debug_payload)
        self.assertIn("card_lookup_results", debug_payload["debug_details"])

    def test_building_report_does_not_mutate_workspace(self) -> None:
        workspace = _workspace()
        before = workspace.to_dict()

        build_deck_inspection_report(
            workspace,
            card_records_by_name=_card_records(),
        )

        self.assertEqual(workspace.to_dict(), before)

    def test_rejects_conflicting_card_sources(self) -> None:
        with self.assertRaisesRegex(DeckInspectionReportError, "either"):
            build_deck_inspection_report(
                _workspace(),
                card_records_by_name=_card_records(),
                card_catalog=CardCatalog([]),
            )


    def test_iterable_source_matches_mapping_source_inspection_meaning(
        self,
    ) -> None:
        workspace = DeckWorkspace.create_empty(
            name="Source Parity",
            deck_id="source-parity",
        )
        workspace.mainboard.append(
            _entry(
                "tower",
                "Command Tower",
                quantity=2,
            )
        )

        record = {
            "name": "Command Tower",
            "oracle_id": "oracle-command-tower",
            "scryfall_id": "printing-command-tower",
            "type_line": "Land",
            "oracle_text": "{T}: Add one mana of any color in your commander's color identity.",
        }

        mapping_report = build_deck_inspection_report(
            workspace,
            card_records_by_name={"Command Tower": record},
        )
        iterable_report = build_deck_inspection_report(
            workspace,
            card_records_by_name=[record],
        )

        self.assertEqual(
            iterable_report.card_fact_coverage.to_dict(),
            mapping_report.card_fact_coverage.to_dict(),
        )
        self.assertEqual(
            iterable_report.skeleton_report.card_fact_lookup_status,
            mapping_report.skeleton_report.card_fact_lookup_status,
        )
        self.assertEqual(
            iterable_report.skeleton_report.missing_card_fact_entries,
            mapping_report.skeleton_report.missing_card_fact_entries,
        )
        self.assertEqual(
            iterable_report.skeleton_report.duplicate_nonbasic_warnings,
            mapping_report.skeleton_report.duplicate_nonbasic_warnings,
        )
        self.assertEqual(
            iterable_report.structural_warnings_report.to_dict(),
            mapping_report.structural_warnings_report.to_dict(),
        )

    def test_catalog_source_matches_mapping_source_inspection_meaning(
        self,
    ) -> None:
        workspace = DeckWorkspace.create_empty(
            name="Catalog Parity",
            deck_id="catalog-parity",
        )
        workspace.mainboard.append(
            _entry(
                "tower",
                "Command Tower",
                quantity=2,
            )
        )

        record = {
            "name": "Command Tower",
            "oracle_id": "oracle-command-tower",
            "scryfall_id": "printing-command-tower",
            "type_line": "Land",
            "oracle_text": "{T}: Add one mana of any color in your commander's color identity.",
        }
        catalog_record = CardRecord.from_dict(record)

        mapping_report = build_deck_inspection_report(
            workspace,
            card_records_by_name={"Command Tower": record},
        )
        catalog_report = build_deck_inspection_report(
            workspace,
            card_catalog=CardCatalog([catalog_record]),
        )

        self.assertEqual(
            catalog_report.card_fact_coverage.to_dict(),
            mapping_report.card_fact_coverage.to_dict(),
        )
        self.assertEqual(
            catalog_report.skeleton_report.card_fact_lookup_status,
            mapping_report.skeleton_report.card_fact_lookup_status,
        )
        self.assertEqual(
            catalog_report.skeleton_report.missing_card_fact_entries,
            mapping_report.skeleton_report.missing_card_fact_entries,
        )
        self.assertEqual(
            catalog_report.skeleton_report.duplicate_nonbasic_warnings,
            mapping_report.skeleton_report.duplicate_nonbasic_warnings,
        )
        self.assertEqual(
            catalog_report.structural_warnings_report.to_dict(),
            mapping_report.structural_warnings_report.to_dict(),
        )


if __name__ == "__main__":
    unittest.main()

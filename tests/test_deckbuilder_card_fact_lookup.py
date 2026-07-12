import unittest

from mtg_workbench.cards.catalog import CardCatalog, normalize_lookup_key
from mtg_workbench.deckbuilder.card_fact_lookup import (
    AMBIGUOUS,
    FOUND,
    MISSING,
    CardFactLookupError,
    lookup_deck_entry_card_fact,
    lookup_workspace_card_facts,
)
from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace


def _entry(
    entry_id: str,
    name: str,
    *,
    display_name: str | None = None,
    zone: str = "mainboard",
) -> DeckEntry:
    return DeckEntry(
        entry_id=entry_id,
        quantity=1,
        input_name=name,
        display_name=display_name,
        zone=zone,
        categories=[],
        tags=[],
    )


class CardFactLookupBridgeTests(unittest.TestCase):
    def test_lookup_uses_existing_normalize_lookup_key(self) -> None:
        self.assertEqual(normalize_lookup_key("  Sol   Ring "), "sol ring")

        result = lookup_deck_entry_card_fact(
            _entry("sol-ring", "  sol   ring "),
            card_records=[
                {
                    "name": "Sol Ring",
                    "oracle_id": "oracle-sol-ring",
                    "type_line": "Artifact",
                }
            ],
        )

        self.assertEqual(result.status, FOUND)
        self.assertEqual(result.lookup_key, "sol ring")
        self.assertEqual(result.record["name"], "Sol Ring")

    def test_lookup_supports_supplied_record_aliases(self) -> None:
        result = lookup_deck_entry_card_fact(
            _entry("alias", "Mana Rock"),
            card_records=[
                {
                    "name": "Sol Ring",
                    "aliases": ["Mana Rock"],
                    "oracle_id": "oracle-sol-ring",
                }
            ],
        )

        self.assertEqual(result.status, FOUND)
        self.assertEqual(result.record["name"], "Sol Ring")

    def test_lookup_reports_missing_without_guessing(self) -> None:
        result = lookup_deck_entry_card_fact(
            _entry("missing", "Unknown Card"),
            card_records=[{"name": "Known Card"}],
        )

        self.assertEqual(result.status, MISSING)
        self.assertIsNone(result.record)
        self.assertEqual(result.candidates, ())

    def test_lookup_reports_ambiguous_supplied_records_without_selecting_winner(self) -> None:
        result = lookup_deck_entry_card_fact(
            _entry("ambiguous", "Shared Alias"),
            card_records=[
                {"name": "First Card", "aliases": ["Shared Alias"], "oracle_id": "oracle-first"},
                {"name": "Second Card", "aliases": ["Shared Alias"], "oracle_id": "oracle-second"},
            ],
        )

        self.assertEqual(result.status, AMBIGUOUS)
        self.assertIsNone(result.record)
        self.assertEqual(
            [candidate.display_name for candidate in result.candidates],
            ["First Card", "Second Card"],
        )

    def test_card_catalog_source_resolves_found_and_missing(self) -> None:
        catalog = CardCatalog.from_json_file("tests/fixtures/cards/tiny_cards.json")

        found = lookup_deck_entry_card_fact(_entry("found", "Alias Helper"), catalog=catalog)
        missing = lookup_deck_entry_card_fact(_entry("missing", "Unknown Mystery"), catalog=catalog)

        self.assertEqual(found.status, FOUND)
        self.assertEqual(found.record["name"], "Alias Target")
        self.assertEqual(missing.status, MISSING)

    def test_workspace_lookup_preserves_entry_order_and_counts(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Lookup Deck", deck_id="lookup-deck")
        workspace.commanders.append(_entry("commander", "Commander", zone="commander"))
        workspace.mainboard.append(_entry("known", "Known Card"))
        workspace.maybeboard.append(_entry("unknown", "Unknown Card", zone="maybeboard"))

        report = lookup_workspace_card_facts(
            workspace,
            card_records={
                "Commander": {"name": "Commander"},
                "Known Card": {"name": "Known Card"},
            },
        )

        self.assertEqual(report.schema_version, "card_fact_lookup_report.v0")
        self.assertEqual([result.entry_id for result in report.results], ["commander", "known", "unknown"])
        self.assertEqual(report.found_count, 2)
        self.assertEqual(report.missing_count, 1)
        self.assertEqual(report.ambiguous_count, 0)

    def test_found_records_by_entry_id_returns_only_found_records(self) -> None:
        workspace = DeckWorkspace.create_empty(name="Records Deck", deck_id="records-deck")
        workspace.mainboard.append(_entry("known", "Known Card"))
        workspace.mainboard.append(_entry("missing", "Missing Card"))

        report = lookup_workspace_card_facts(
            workspace,
            card_records=[{"name": "Known Card", "type_line": "Artifact"}],
        )

        self.assertEqual(report.found_records_by_entry_id(), {"known": {"name": "Known Card", "type_line": "Artifact"}})

    def test_to_dict_keeps_summary_evidence_and_debug_records_separated(self) -> None:
        result = lookup_deck_entry_card_fact(
            _entry("known", "Known Card"),
            card_records=[{"name": "Known Card", "type_line": "Artifact"}],
        )

        payload = result.to_dict(include_debug=True, include_record=True)

        self.assertIn("user_summary", payload)
        self.assertIn("machine_evidence", payload)
        self.assertIn("debug_details", payload)
        self.assertEqual(payload["debug_details"]["candidates"][0]["record"]["name"], "Known Card")

    def test_rejects_missing_or_conflicting_sources(self) -> None:
        with self.assertRaises(CardFactLookupError):
            lookup_deck_entry_card_fact(_entry("known", "Known Card"))

        with self.assertRaises(CardFactLookupError):
            lookup_deck_entry_card_fact(
                _entry("known", "Known Card"),
                card_records=[],
                catalog=CardCatalog([]),
            )


if __name__ == "__main__":
    unittest.main()

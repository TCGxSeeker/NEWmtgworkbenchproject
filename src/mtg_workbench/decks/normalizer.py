from __future__ import annotations

from collections import defaultdict

from mtg_workbench.cards.catalog import CardCatalog
from mtg_workbench.decks.models import (
    NormalizedDeckEntry,
    ParsedDeck,
    RawDeck,
    ValidationWarning,
)


def normalize_deck(raw_deck: RawDeck, catalog: CardCatalog) -> ParsedDeck:
    parsed = ParsedDeck(source_path=raw_deck.source_path, source_format=raw_deck.source_format)

    for raw_entry in raw_deck.entries:
        card = catalog.find(raw_entry.raw_name)
        entry = NormalizedDeckEntry(
            quantity=raw_entry.quantity,
            raw_name=raw_entry.raw_name,
            name=card.name if card else None,
            section=raw_entry.section,
            category=raw_entry.category,
            notes=raw_entry.notes,
            line_number=raw_entry.line_number,
            is_known=card is not None,
            is_basic_land=card.is_basic_land if card else False,
        )

        if entry.section == "commander":
            parsed.commanders.append(entry)
        elif entry.section == "maybeboard":
            parsed.maybeboard.append(entry)
        else:
            parsed.mainboard.append(entry)

        if not entry.is_known:
            parsed.unknown_cards.append(entry)

    parsed.warnings.extend(_duplicate_non_basic_warnings(parsed))
    return parsed


def _duplicate_non_basic_warnings(parsed: ParsedDeck) -> list[ValidationWarning]:
    totals: dict[str, int] = defaultdict(int)
    display_names: dict[str, str] = {}
    is_basic: dict[str, bool] = {}

    for entry in [*parsed.commanders, *parsed.mainboard]:
        if not entry.is_known or not entry.name:
            continue
        key = entry.name.casefold()
        totals[key] += entry.quantity
        display_names[key] = entry.name
        is_basic[key] = entry.is_basic_land

    warnings: list[ValidationWarning] = []
    for key in sorted(totals):
        if totals[key] > 1 and not is_basic[key]:
            name = display_names[key]
            warnings.append(
                ValidationWarning(
                    code="duplicate_non_basic",
                    card_name=name,
                    quantity=totals[key],
                    message=f"Known non-basic card appears {totals[key]} times: {name}.",
                )
            )
    return warnings

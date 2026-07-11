from __future__ import annotations

from datetime import datetime, timezone
import re

from mtg_workbench.cards.catalog import CardCatalog
from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace
from mtg_workbench.deckbuilder.mutations import add_entry


_ENTRY_RE = re.compile(r"^\s*(?:(\d+)\s*x?\s+)?(.+?)\s*$", re.IGNORECASE)

_COMMANDER_HEADERS = {"commander", "commanders"}
_MAINBOARD_HEADERS = {"main", "mainboard", "main deck", "deck"}
_MAYBEBOARD_HEADERS = {"maybeboard", "maybe board", "maybe", "sideboard"}
_CATEGORY_HEADERS = {
    "artifacts": "Artifacts",
    "creatures": "Creatures",
    "draw": "Draw",
    "enchantments": "Enchantments",
    "instants": "Instants",
    "interaction": "Interaction",
    "lands": "Lands",
    "planeswalkers": "Planeswalkers",
    "protection": "Protection",
    "ramp": "Ramp",
    "removal": "Removal",
    "sorceries": "Sorceries",
}


def import_plain_text_decklist(
    text: str,
    *,
    catalog: CardCatalog | None = None,
    name: str = "Imported Deck",
    format: str = "commander",
    deck_id: str | None = None,
    source: str | None = None,
    created_at: str | None = None,
    updated_at: str | None = None,
) -> DeckWorkspace:
    timestamp = updated_at or created_at or _current_timestamp()
    workspace = DeckWorkspace.create_empty(
        name=name,
        format=format,
        deck_id=deck_id,
        created_at=created_at or timestamp,
        updated_at=timestamp,
        metadata=_import_metadata(source),
    )

    current_zone = "mainboard"
    current_category: str | None = None

    for raw_line in text.splitlines():
        line = _clean_line(raw_line)
        if not line:
            continue

        zone = _section_header_zone(line)
        if zone:
            current_zone = zone
            current_category = None
            continue

        category = _category_header(line)
        if category:
            current_category = category
            continue

        parsed = _parse_entry_line(line)
        if parsed is None:
            continue

        quantity, card_name, quantity_explicit = parsed
        entry_zone = current_zone
        entry_quantity = quantity
        if entry_zone == "commander" and not quantity_explicit:
            entry_quantity = 1

        display_name, is_unresolved = _resolve_display_name(card_name, catalog)
        add_entry(
            workspace,
            card_name,
            display_name=display_name,
            quantity=entry_quantity,
            zone=entry_zone,
            categories=[current_category] if current_category else [],
            is_unresolved=is_unresolved,
            updated_at=timestamp,
        )

    workspace.saved_state["is_dirty"] = True
    workspace.updated_at = timestamp
    return workspace


def export_plain_text_decklist(workspace: DeckWorkspace) -> str:
    sections: list[tuple[str, list[DeckEntry]]] = [
        ("Commander", workspace.commanders),
        ("Mainboard", workspace.mainboard),
    ]
    if workspace.maybeboard:
        sections.append(("Maybeboard", workspace.maybeboard))

    lines: list[str] = []
    for section_index, (header, entries) in enumerate(sections):
        if section_index:
            lines.append("")
        lines.append(header)
        for entry in entries:
            lines.append(f"{entry.quantity}x {_export_name(entry)}")

    return "\n".join(lines) + "\n"


def _parse_entry_line(line: str) -> tuple[int, str, bool] | None:
    match = _ENTRY_RE.match(line)
    if not match:
        return None
    quantity_text = match.group(1)
    card_name = match.group(2).strip()
    if not card_name:
        return None
    quantity = int(quantity_text) if quantity_text else 1
    return quantity, card_name, quantity_text is not None


def _resolve_display_name(card_name: str, catalog: CardCatalog | None) -> tuple[str | None, bool]:
    if catalog is None:
        return card_name, False
    card = catalog.find(card_name)
    if card is None:
        return None, True
    return card.name, False


def _clean_line(raw_line: str) -> str:
    stripped = raw_line.strip()
    if not stripped:
        return ""
    if stripped.startswith("#") or stripped.startswith("//"):
        return ""
    return stripped.rstrip(":").strip()


def _section_header_zone(line: str) -> str | None:
    normalized = _normalize_header(line)
    if normalized in _COMMANDER_HEADERS:
        return "commander"
    if normalized in _MAINBOARD_HEADERS:
        return "mainboard"
    if normalized in _MAYBEBOARD_HEADERS:
        return "maybeboard"
    return None


def _category_header(line: str) -> str | None:
    return _CATEGORY_HEADERS.get(_normalize_header(line))


def _normalize_header(line: str) -> str:
    return " ".join(line.casefold().split())


def _export_name(entry: DeckEntry) -> str:
    return entry.display_name or entry.input_name


def _import_metadata(source: str | None) -> dict[str, str]:
    metadata = {"import_origin": "plain_text"}
    if source:
        metadata["source"] = source
    return metadata


def _current_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

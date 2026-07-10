from __future__ import annotations

import csv
from pathlib import Path
import re

from mtg_workbench.decks.models import RawDeck, RawDeckEntry


_PLAIN_ENTRY_RE = re.compile(r"^\s*(\d+)\s+(.+?)\s*$")

_COMMANDER_SECTIONS = {"commander", "commanders"}
_MAIN_SECTIONS = {"deck", "main", "main deck", "mainboard"}
_MAYBE_SECTIONS = {"maybeboard", "maybe board", "maybe"}


def parse_decklist(path: str | Path) -> RawDeck:
    deck_path = Path(path)
    if deck_path.suffix.casefold() == ".csv":
        return parse_csv_decklist(deck_path)
    return parse_plain_text_decklist(deck_path)


def parse_plain_text_decklist(path: str | Path) -> RawDeck:
    deck_path = Path(path)
    entries: list[RawDeckEntry] = []
    current_section = "main"

    with deck_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            section = _section_from_header(line)
            if section:
                current_section = section
                continue

            match = _PLAIN_ENTRY_RE.match(line)
            if not match:
                continue

            quantity = int(match.group(1))
            card_name = match.group(2).strip()
            entries.append(
                RawDeckEntry(
                    quantity=quantity,
                    raw_name=card_name,
                    section=current_section,
                    line_number=line_number,
                )
            )

    return RawDeck(source_path=str(deck_path), source_format="plain_text", entries=entries)


def parse_csv_decklist(path: str | Path) -> RawDeck:
    deck_path = Path(path)
    entries: list[RawDeckEntry] = []

    with deck_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for line_number, row in enumerate(reader, start=2):
            raw_name = (row.get("card_name") or row.get("name") or "").strip()
            if not raw_name:
                continue
            quantity_text = (row.get("quantity") or "1").strip()
            quantity = int(quantity_text)
            section = _classify_section(row.get("section"), row.get("category"))
            entries.append(
                RawDeckEntry(
                    quantity=quantity,
                    raw_name=raw_name,
                    section=section,
                    category=_clean_optional(row.get("category")),
                    notes=_clean_optional(row.get("notes")),
                    line_number=line_number,
                )
            )

    return RawDeck(source_path=str(deck_path), source_format="csv", entries=entries)


def _section_from_header(line: str) -> str | None:
    normalized = line.strip().rstrip(":").casefold()
    if normalized in _COMMANDER_SECTIONS:
        return "commander"
    if normalized in _MAIN_SECTIONS:
        return "main"
    if normalized in _MAYBE_SECTIONS:
        return "maybeboard"
    return None


def _classify_section(section: str | None, category: str | None) -> str:
    normalized_candidates = [(candidate or "").strip().casefold() for candidate in [section, category]]
    if any(candidate in _COMMANDER_SECTIONS for candidate in normalized_candidates):
        return "commander"
    if any(candidate in _MAYBE_SECTIONS for candidate in normalized_candidates):
        return "maybeboard"
    if any(candidate in _MAIN_SECTIONS for candidate in normalized_candidates):
        return "main"
    return "main"


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None

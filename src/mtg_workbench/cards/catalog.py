from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any


_SPACE_RE = re.compile(r"\s+")


def normalize_lookup_key(name: str) -> str:
    """Normalize lookup input without stripping punctuation."""
    return _SPACE_RE.sub(" ", name.strip()).casefold()


class CardCatalogAmbiguityError(ValueError):
    """Raised when one lookup key resolves to multiple logical card identities."""


@dataclass(frozen=True)
class CardRecord:
    name: str
    aliases: tuple[str, ...]
    mana_value: float | int | None
    colors: tuple[str, ...]
    color_identity: tuple[str, ...]
    type_line: str
    oracle_text: str
    legalities: dict[str, Any]
    prices: dict[str, Any]
    is_basic_land: bool = False
    oracle_id: str | None = None
    representative_scryfall_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CardRecord":
        return cls(
            name=str(data["name"]),
            aliases=tuple(str(alias) for alias in data.get("aliases", [])),
            mana_value=data.get("mana_value"),
            colors=tuple(str(color) for color in data.get("colors", [])),
            color_identity=tuple(str(color) for color in data.get("color_identity", [])),
            type_line=str(data.get("type_line", "")),
            oracle_text=str(data.get("oracle_text", "")),
            legalities=dict(data.get("legalities", {})),
            prices=dict(data.get("prices", {})),
            is_basic_land=bool(data.get("is_basic_land", False)),
            oracle_id=_optional_text(data.get("oracle_id")),
            representative_scryfall_id=_optional_text(
                data.get("representative_scryfall_id")
                or data.get("scryfall_id")
            ),
        )


class CardCatalog:
    def __init__(self, cards: list[CardRecord]) -> None:
        self.cards = cards
        self._lookup: dict[str, list[CardRecord]] = {}

        for card in cards:
            self._add_lookup(card.name, card)
            for alias in card.aliases:
                self._add_lookup(alias, card)

    @classmethod
    def from_json_file(cls, path: str | Path) -> "CardCatalog":
        with Path(path).open("r", encoding="utf-8") as handle:
            payload = json.load(handle)

        cards = [CardRecord.from_dict(card) for card in payload.get("cards", [])]
        return cls(cards)

    def find_all(self, name: str) -> tuple[CardRecord, ...]:
        key = normalize_lookup_key(name)
        candidates = self._lookup.get(key, [])

        return tuple(sorted(candidates, key=_card_sort_key))

    def find(self, name: str) -> CardRecord | None:
        candidates = self.find_all(name)

        if not candidates:
            return None

        identities = {_logical_identity(card) for card in candidates}

        if len(identities) > 1:
            candidate_names = ", ".join(card.name for card in candidates)
            raise CardCatalogAmbiguityError(
                f"Card lookup is ambiguous for {name!r}: {candidate_names}."
            )

        return candidates[0]

    def _add_lookup(self, name: str, card: CardRecord) -> None:
        key = normalize_lookup_key(name)

        if not key:
            return

        bucket = self._lookup.setdefault(key, [])

        if card not in bucket:
            bucket.append(card)


def _logical_identity(card: CardRecord) -> str:
    if card.oracle_id:
        return f"oracle:{card.oracle_id}"

    return f"name:{normalize_lookup_key(card.name)}"


def _card_sort_key(card: CardRecord) -> tuple[str, str, str]:
    return (
        card.oracle_id or "",
        normalize_lookup_key(card.name),
        card.representative_scryfall_id or "",
    )


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    return text or None

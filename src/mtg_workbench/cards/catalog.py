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
        )


class CardCatalog:
    def __init__(self, cards: list[CardRecord]) -> None:
        self.cards = cards
        self._lookup: dict[str, CardRecord] = {}
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

    def find(self, name: str) -> CardRecord | None:
        return self._lookup.get(normalize_lookup_key(name))

    def _add_lookup(self, name: str, card: CardRecord) -> None:
        key = normalize_lookup_key(name)
        if key:
            self._lookup[key] = card

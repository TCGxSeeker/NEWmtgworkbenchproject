from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RawDeckEntry:
    quantity: int
    raw_name: str
    section: str
    category: str | None = None
    notes: str | None = None
    line_number: int | None = None


@dataclass(frozen=True)
class NormalizedDeckEntry:
    quantity: int
    raw_name: str
    name: str | None
    section: str
    category: str | None = None
    notes: str | None = None
    line_number: int | None = None
    is_known: bool = False
    is_basic_land: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "is_basic_land": self.is_basic_land,
            "is_known": self.is_known,
            "line_number": self.line_number,
            "name": self.name,
            "notes": self.notes,
            "quantity": self.quantity,
            "raw_name": self.raw_name,
            "section": self.section,
        }


@dataclass(frozen=True)
class ValidationWarning:
    code: str
    message: str
    card_name: str | None = None
    quantity: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_name": self.card_name,
            "code": self.code,
            "message": self.message,
            "quantity": self.quantity,
        }


@dataclass
class RawDeck:
    source_path: str
    source_format: str
    entries: list[RawDeckEntry] = field(default_factory=list)


@dataclass
class ParsedDeck:
    source_path: str
    source_format: str
    commanders: list[NormalizedDeckEntry] = field(default_factory=list)
    mainboard: list[NormalizedDeckEntry] = field(default_factory=list)
    maybeboard: list[NormalizedDeckEntry] = field(default_factory=list)
    unknown_cards: list[NormalizedDeckEntry] = field(default_factory=list)
    warnings: list[ValidationWarning] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "commanders": [entry.to_dict() for entry in self.commanders],
            "mainboard": [entry.to_dict() for entry in self.mainboard],
            "maybeboard": [entry.to_dict() for entry in self.maybeboard],
            "source_format": self.source_format,
            "source_path": self.source_path,
            "unknown_cards": [entry.to_dict() for entry in self.unknown_cards],
            "warnings": [warning.to_dict() for warning in self.warnings],
        }

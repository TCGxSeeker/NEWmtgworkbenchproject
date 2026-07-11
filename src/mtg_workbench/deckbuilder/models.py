from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


SCHEMA_VERSION = 1
VALID_ZONES = {"commander", "mainboard", "maybeboard"}

_WORKSPACE_FIELDS = {
    "commanders",
    "created_at",
    "deck_id",
    "format",
    "mainboard",
    "maybeboard",
    "metadata",
    "name",
    "notes",
    "saved_state",
    "schema_version",
    "tags",
    "updated_at",
}

_ENTRY_FIELDS = {
    "categories",
    "date_added",
    "display_name",
    "entry_id",
    "foil",
    "input_name",
    "is_unresolved",
    "notes",
    "oracle_id",
    "pinned",
    "quantity",
    "selected_printing_id",
    "tags",
    "zone",
}


def _default_saved_state() -> dict[str, Any]:
    return {"is_dirty": False}


@dataclass
class DeckEntry:
    entry_id: str
    quantity: int
    input_name: str
    display_name: str | None
    zone: str
    oracle_id: str | None = None
    selected_printing_id: str | None = None
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    notes: str | None = None
    pinned: bool = False
    foil: bool = False
    date_added: str | None = None
    is_unresolved: bool = False
    extra_fields: dict[str, Any] = field(default_factory=dict, repr=False)

    def to_dict(self) -> dict[str, Any]:
        payload = dict(self.extra_fields)
        payload.update(
            {
                "categories": list(self.categories),
                "date_added": self.date_added,
                "display_name": self.display_name,
                "entry_id": self.entry_id,
                "foil": self.foil,
                "input_name": self.input_name,
                "is_unresolved": self.is_unresolved,
                "notes": self.notes,
                "oracle_id": self.oracle_id,
                "pinned": self.pinned,
                "quantity": self.quantity,
                "selected_printing_id": self.selected_printing_id,
                "tags": list(self.tags),
                "zone": self.zone,
            }
        )
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DeckEntry":
        extra_fields = {key: value for key, value in payload.items() if key not in _ENTRY_FIELDS}
        return cls(
            entry_id=payload["entry_id"],
            quantity=payload["quantity"],
            input_name=payload["input_name"],
            display_name=payload["display_name"],
            oracle_id=payload.get("oracle_id"),
            selected_printing_id=payload.get("selected_printing_id"),
            zone=payload["zone"],
            categories=list(payload["categories"]),
            tags=list(payload["tags"]),
            notes=payload.get("notes"),
            pinned=payload.get("pinned", False),
            foil=payload.get("foil", False),
            date_added=payload.get("date_added"),
            is_unresolved=payload["is_unresolved"],
            extra_fields=extra_fields,
        )


@dataclass
class DeckWorkspace:
    deck_id: str
    name: str
    format: str = "commander"
    schema_version: int = SCHEMA_VERSION
    created_at: str | None = None
    updated_at: str | None = None
    tags: list[str] = field(default_factory=list)
    notes: str | None = None
    commanders: list[DeckEntry] = field(default_factory=list)
    mainboard: list[DeckEntry] = field(default_factory=list)
    maybeboard: list[DeckEntry] = field(default_factory=list)
    saved_state: dict[str, Any] = field(default_factory=_default_saved_state)
    metadata: dict[str, Any] = field(default_factory=dict)
    extra_fields: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def create_empty(
        cls,
        name: str = "Untitled Deck",
        format: str = "commander",
        deck_id: str | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
        tags: list[str] | None = None,
        notes: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "DeckWorkspace":
        return cls(
            deck_id=deck_id or str(uuid4()),
            name=name,
            format=format,
            created_at=created_at,
            updated_at=updated_at,
            tags=list(tags or []),
            notes=notes,
            metadata=dict(metadata or {}),
        )

    def all_entries(self) -> list[DeckEntry]:
        return [*self.commanders, *self.mainboard, *self.maybeboard]

    def to_dict(self) -> dict[str, Any]:
        payload = dict(self.extra_fields)
        payload.update(
            {
                "commanders": [entry.to_dict() for entry in self.commanders],
                "created_at": self.created_at,
                "deck_id": self.deck_id,
                "format": self.format,
                "mainboard": [entry.to_dict() for entry in self.mainboard],
                "maybeboard": [entry.to_dict() for entry in self.maybeboard],
                "metadata": dict(self.metadata),
                "name": self.name,
                "notes": self.notes,
                "saved_state": dict(self.saved_state),
                "schema_version": self.schema_version,
                "tags": list(self.tags),
                "updated_at": self.updated_at,
            }
        )
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DeckWorkspace":
        extra_fields = {key: value for key, value in payload.items() if key not in _WORKSPACE_FIELDS}
        return cls(
            schema_version=payload["schema_version"],
            deck_id=payload["deck_id"],
            name=payload["name"],
            format=payload["format"],
            created_at=payload.get("created_at"),
            updated_at=payload.get("updated_at"),
            tags=list(payload["tags"]),
            notes=payload.get("notes"),
            commanders=[DeckEntry.from_dict(entry) for entry in payload["commanders"]],
            mainboard=[DeckEntry.from_dict(entry) for entry in payload["mainboard"]],
            maybeboard=[DeckEntry.from_dict(entry) for entry in payload["maybeboard"]],
            saved_state=dict(payload["saved_state"]),
            metadata=dict(payload.get("metadata") or {}),
            extra_fields=extra_fields,
        )

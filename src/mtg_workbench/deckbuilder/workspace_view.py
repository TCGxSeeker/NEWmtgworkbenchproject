from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace, VALID_ZONES


GROUP_FULL_DECK = "full_deck"
GROUP_ZONE = "zone"
GROUP_CATEGORY = "category"
SORT_ALPHABET = "alphabet"
SORT_QUANTITY = "quantity"
SORT_CATEGORY = "category"
SORT_ZONE = "zone"
UNCATEGORIZED = "Uncategorized"

SUPPORTED_GROUP_MODES = frozenset({GROUP_FULL_DECK, GROUP_ZONE, GROUP_CATEGORY})
SUPPORTED_SORT_MODES = frozenset({SORT_ALPHABET, SORT_QUANTITY, SORT_CATEGORY, SORT_ZONE})
ZONE_ORDER = {"commander": 0, "mainboard": 1, "maybeboard": 2}


class WorkspaceViewError(ValueError):
    pass


@dataclass(frozen=True)
class WorkspaceViewEntry:
    entry_id: str
    zone: str
    quantity: int
    card_name: str
    input_name: str
    display_name: str | None
    categories: tuple[str, ...]
    tags: tuple[str, ...]
    secondary_tags: tuple[str, ...]
    imported_category: str | None
    normalized_category: str | None
    generic_category_hint: str | None
    is_unresolved: bool

    @classmethod
    def from_entry(cls, entry: DeckEntry) -> "WorkspaceViewEntry":
        return cls(
            entry_id=entry.entry_id,
            zone=entry.zone,
            quantity=entry.quantity,
            card_name=entry.display_name or entry.input_name,
            input_name=entry.input_name,
            display_name=entry.display_name,
            categories=tuple(entry.categories),
            tags=tuple(entry.tags),
            secondary_tags=tuple(entry.secondary_tags),
            imported_category=entry.imported_category,
            normalized_category=entry.normalized_category,
            generic_category_hint=entry.generic_category_hint,
            is_unresolved=entry.is_unresolved,
        )

    @property
    def category_labels(self) -> tuple[str, ...]:
        return self.categories or (UNCATEGORIZED,)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "zone": self.zone,
            "quantity": self.quantity,
            "card_name": self.card_name,
            "input_name": self.input_name,
            "display_name": self.display_name,
            "categories": list(self.categories),
            "tags": list(self.tags),
            "secondary_tags": list(self.secondary_tags),
            "imported_category": self.imported_category,
            "normalized_category": self.normalized_category,
            "generic_category_hint": self.generic_category_hint,
            "is_unresolved": self.is_unresolved,
        }


@dataclass(frozen=True)
class WorkspaceViewGroup:
    group_id: str
    label: str
    entry_count: int
    quantity_total: int
    entries: tuple[WorkspaceViewEntry, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "group_id": self.group_id,
            "label": self.label,
            "entry_count": self.entry_count,
            "quantity_total": self.quantity_total,
            "entries": [entry.to_dict() for entry in self.entries],
        }


@dataclass(frozen=True)
class WorkspaceViewProjection:
    schema_version: str
    deck_id: str
    deck_name: str
    group_by: str
    sort_by: str
    filter_text: str | None
    visible_entry_count: int
    visible_quantity_total: int
    grouped_entry_count: int
    grouped_quantity_total: int
    groups: tuple[WorkspaceViewGroup, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "deck_id": self.deck_id,
            "deck_name": self.deck_name,
            "group_by": self.group_by,
            "sort_by": self.sort_by,
            "filter_text": self.filter_text,
            "visible_entry_count": self.visible_entry_count,
            "visible_quantity_total": self.visible_quantity_total,
            "grouped_entry_count": self.grouped_entry_count,
            "grouped_quantity_total": self.grouped_quantity_total,
            "groups": [group.to_dict() for group in self.groups],
        }


def build_workspace_view_projection(
    workspace: DeckWorkspace,
    *,
    group_by: str = GROUP_CATEGORY,
    sort_by: str = SORT_ALPHABET,
    filter_text: str | None = None,
    zones: Iterable[str] | None = None,
) -> WorkspaceViewProjection:
    group_mode = _require_group_mode(group_by)
    sort_mode = _require_sort_mode(sort_by)
    selected_zones = _require_zones(zones)
    clean_filter_text = _clean_filter_text(filter_text)

    entries = tuple(
        WorkspaceViewEntry.from_entry(entry)
        for entry in workspace.all_entries()
        if entry.zone in selected_zones
    )
    filtered_entries = tuple(
        entry for entry in entries if _entry_matches_filter(entry, clean_filter_text)
    )
    sorted_entries = tuple(sorted(filtered_entries, key=lambda entry: _sort_key(entry, sort_mode)))
    groups = _build_groups(sorted_entries, group_mode)

    return WorkspaceViewProjection(
        schema_version="deck_workspace_view_projection.v0",
        deck_id=workspace.deck_id,
        deck_name=workspace.name,
        group_by=group_mode,
        sort_by=sort_mode,
        filter_text=clean_filter_text,
        visible_entry_count=len(sorted_entries),
        visible_quantity_total=sum(entry.quantity for entry in sorted_entries),
        grouped_entry_count=sum(group.entry_count for group in groups),
        grouped_quantity_total=sum(group.quantity_total for group in groups),
        groups=groups,
    )


def _build_groups(
    entries: tuple[WorkspaceViewEntry, ...],
    group_mode: str,
) -> tuple[WorkspaceViewGroup, ...]:
    if group_mode == GROUP_FULL_DECK:
        return (_make_group("full_deck", "Full Deck", entries),)
    if group_mode == GROUP_ZONE:
        return tuple(
            _make_group(zone, _zone_label(zone), tuple(entry for entry in entries if entry.zone == zone))
            for zone in sorted(ZONE_ORDER, key=ZONE_ORDER.__getitem__)
            if any(entry.zone == zone for entry in entries)
        )
    if group_mode == GROUP_CATEGORY:
        labels = _category_labels(entries)
        return tuple(
            _make_group(
                _group_id(label),
                label,
                tuple(entry for entry in entries if label in entry.category_labels),
            )
            for label in labels
        )
    raise WorkspaceViewError(f"Unsupported group mode: {group_mode}.")


def _make_group(
    group_id: str,
    label: str,
    entries: tuple[WorkspaceViewEntry, ...],
) -> WorkspaceViewGroup:
    return WorkspaceViewGroup(
        group_id=group_id,
        label=label,
        entry_count=len(entries),
        quantity_total=sum(entry.quantity for entry in entries),
        entries=entries,
    )


def _category_labels(entries: tuple[WorkspaceViewEntry, ...]) -> tuple[str, ...]:
    labels = {
        label
        for entry in entries
        for label in entry.category_labels
    }
    return tuple(sorted(labels, key=lambda label: (_is_uncategorized(label), _normalize_text(label))))


def _sort_key(entry: WorkspaceViewEntry, sort_mode: str) -> tuple[Any, ...]:
    alphabet_key = (_normalize_text(entry.card_name), entry.entry_id)
    if sort_mode == SORT_ALPHABET:
        return alphabet_key
    if sort_mode == SORT_QUANTITY:
        return (-entry.quantity, *alphabet_key)
    if sort_mode == SORT_CATEGORY:
        first_category = entry.category_labels[0]
        return (_is_uncategorized(first_category), _normalize_text(first_category), *alphabet_key)
    if sort_mode == SORT_ZONE:
        return (ZONE_ORDER[entry.zone], *alphabet_key)
    raise WorkspaceViewError(f"Unsupported sort mode: {sort_mode}.")


def _entry_matches_filter(entry: WorkspaceViewEntry, filter_text: str | None) -> bool:
    if filter_text is None:
        return True
    searchable_fields = (
        entry.card_name,
        entry.input_name,
        entry.display_name,
        *entry.categories,
        *entry.tags,
        *entry.secondary_tags,
        entry.imported_category,
        entry.normalized_category,
        entry.generic_category_hint,
    )
    haystack = _normalize_text(" ".join(field for field in searchable_fields if field))
    return filter_text in haystack


def _require_group_mode(value: str) -> str:
    group_mode = _normalize_mode(value)
    if group_mode not in SUPPORTED_GROUP_MODES:
        raise WorkspaceViewError(
            f"Unsupported group_by: {value}. Expected one of {sorted(SUPPORTED_GROUP_MODES)}."
        )
    return group_mode


def _require_sort_mode(value: str) -> str:
    sort_mode = _normalize_mode(value)
    if sort_mode not in SUPPORTED_SORT_MODES:
        raise WorkspaceViewError(
            f"Unsupported sort_by: {value}. Expected one of {sorted(SUPPORTED_SORT_MODES)}."
        )
    return sort_mode


def _require_zones(zones: Iterable[str] | None) -> tuple[str, ...]:
    if zones is None:
        return tuple(sorted(VALID_ZONES, key=ZONE_ORDER.__getitem__))
    if isinstance(zones, (str, bytes)):
        raise WorkspaceViewError("zones must be an iterable of zone strings.")

    clean_zones: list[str] = []
    seen: set[str] = set()
    for zone in zones:
        if zone not in VALID_ZONES:
            raise WorkspaceViewError(f"Invalid zone: {zone}. Expected one of {sorted(VALID_ZONES)}.")
        if zone not in seen:
            clean_zones.append(zone)
            seen.add(zone)
    return tuple(clean_zones)


def _clean_filter_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = _normalize_text(value)
    return cleaned or None


def _normalize_mode(value: str) -> str:
    return "_".join(str(value).strip().casefold().replace("-", "_").split())


def _normalize_text(value: str) -> str:
    return " ".join(value.casefold().split())


def _group_id(label: str) -> str:
    return _normalize_mode(label) or "uncategorized"


def _is_uncategorized(label: str) -> bool:
    return _normalize_text(label) == _normalize_text(UNCATEGORIZED)


def _zone_label(zone: str) -> str:
    return {
        "commander": "Commander",
        "mainboard": "Mainboard",
        "maybeboard": "Maybeboard",
    }[zone]

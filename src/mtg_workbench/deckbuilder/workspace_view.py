from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from mtg_workbench.deckbuilder.card_fact_lookup import (
    AMBIGUOUS,
    FOUND,
    MISSING,
    CardFactLookupReport,
    CardFactLookupResult,
)
from mtg_workbench.deckbuilder.card_facts import CardFactsError, card_record_to_role_facts
from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace, VALID_ZONES


GROUP_FULL_DECK = "full_deck"
GROUP_ZONE = "zone"
GROUP_CATEGORY = "category"
GROUP_TYPE = "type"
GROUP_MANA_VALUE = "mana_value"
SORT_ALPHABET = "alphabet"
SORT_QUANTITY = "quantity"
SORT_CATEGORY = "category"
SORT_ZONE = "zone"
SORT_TYPE = "type"
SORT_MANA_VALUE = "mana_value"
UNCATEGORIZED = "Uncategorized"
MISSING_CARD_FACTS = "Missing Card Facts"
AMBIGUOUS_CARD_FACTS = "Ambiguous Card Facts"
UNKNOWN_TYPE = "Unknown Type"
UNKNOWN_MANA_VALUE = "Unknown Mana Value"
NOT_REQUESTED = "not_requested"
CHECKED = "checked"

SUPPORTED_GROUP_MODES = frozenset(
    {GROUP_FULL_DECK, GROUP_ZONE, GROUP_CATEGORY, GROUP_TYPE, GROUP_MANA_VALUE}
)
SUPPORTED_SORT_MODES = frozenset(
    {SORT_ALPHABET, SORT_QUANTITY, SORT_CATEGORY, SORT_ZONE, SORT_TYPE, SORT_MANA_VALUE}
)
ZONE_ORDER = {"commander": 0, "mainboard": 1, "maybeboard": 2}
TYPE_ORDER = {
    "Land": 0,
    "Creature": 1,
    "Artifact": 2,
    "Enchantment": 3,
    "Planeswalker": 4,
    "Battle": 5,
    "Instant": 6,
    "Sorcery": 7,
    "Kindred": 8,
}
FACT_STATUS_ORDER = {
    UNKNOWN_TYPE: 50,
    UNKNOWN_MANA_VALUE: 50,
    MISSING_CARD_FACTS: 60,
    AMBIGUOUS_CARD_FACTS: 70,
}


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
    card_fact_status: str
    type_line: str | None
    type_labels: tuple[str, ...]
    mana_value: int | float | None

    @classmethod
    def from_entry(
        cls,
        entry: DeckEntry,
        lookup_result: CardFactLookupResult | None = None,
    ) -> "WorkspaceViewEntry":
        fact_status, type_line, type_labels, mana_value = _facts_from_lookup_result(lookup_result)
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
            card_fact_status=fact_status,
            type_line=type_line,
            type_labels=type_labels,
            mana_value=mana_value,
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
            "card_fact_status": self.card_fact_status,
            "type_line": self.type_line,
            "type_labels": list(self.type_labels),
            "mana_value": self.mana_value,
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
    card_fact_lookup: dict[str, Any]
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
            "card_fact_lookup": dict(self.card_fact_lookup),
            "groups": [group.to_dict() for group in self.groups],
        }


def build_workspace_view_projection(
    workspace: DeckWorkspace,
    *,
    group_by: str = GROUP_CATEGORY,
    sort_by: str = SORT_ALPHABET,
    filter_text: str | None = None,
    zones: Iterable[str] | None = None,
    card_fact_lookup_report: CardFactLookupReport | None = None,
) -> WorkspaceViewProjection:
    group_mode = _require_group_mode(group_by)
    sort_mode = _require_sort_mode(sort_by)
    _require_card_facts_if_needed(group_mode, sort_mode, card_fact_lookup_report)
    selected_zones = _require_zones(zones)
    clean_filter_text = _clean_filter_text(filter_text)
    lookup_results_by_entry_id = _lookup_results_by_entry_id(card_fact_lookup_report)

    entries = tuple(
        WorkspaceViewEntry.from_entry(entry, lookup_results_by_entry_id.get(entry.entry_id))
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
        card_fact_lookup=_card_fact_lookup_summary(card_fact_lookup_report),
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
    if group_mode == GROUP_TYPE:
        labels = _type_group_labels(entries)
        return tuple(
            _make_group(
                _group_id(label),
                label,
                tuple(entry for entry in entries if label in _entry_type_group_labels(entry)),
            )
            for label in labels
        )
    if group_mode == GROUP_MANA_VALUE:
        labels = _mana_value_group_labels(entries)
        return tuple(
            _make_group(
                _group_id(label),
                label,
                tuple(entry for entry in entries if label == _entry_mana_value_group_label(entry)),
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


def _type_group_labels(entries: tuple[WorkspaceViewEntry, ...]) -> tuple[str, ...]:
    labels = {
        label
        for entry in entries
        for label in _entry_type_group_labels(entry)
    }
    return tuple(sorted(labels, key=_type_label_sort_key))


def _mana_value_group_labels(entries: tuple[WorkspaceViewEntry, ...]) -> tuple[str, ...]:
    labels = {_entry_mana_value_group_label(entry) for entry in entries}
    return tuple(sorted(labels, key=_mana_value_label_sort_key))


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
    if sort_mode == SORT_TYPE:
        label = _entry_type_group_labels(entry)[0]
        return (*_type_label_sort_key(label), *alphabet_key)
    if sort_mode == SORT_MANA_VALUE:
        label = _entry_mana_value_group_label(entry)
        return (*_mana_value_label_sort_key(label), *alphabet_key)
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


def _require_card_facts_if_needed(
    group_mode: str,
    sort_mode: str,
    card_fact_lookup_report: CardFactLookupReport | None,
) -> None:
    needs_card_facts = group_mode in {GROUP_TYPE, GROUP_MANA_VALUE} or sort_mode in {
        SORT_TYPE,
        SORT_MANA_VALUE,
    }
    if needs_card_facts and card_fact_lookup_report is None:
        raise WorkspaceViewError(
            "type and mana_value projections require an explicit card_fact_lookup_report."
        )


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


def _lookup_results_by_entry_id(
    card_fact_lookup_report: CardFactLookupReport | None,
) -> dict[str, CardFactLookupResult]:
    if card_fact_lookup_report is None:
        return {}
    return {result.entry_id: result for result in card_fact_lookup_report.results}


def _card_fact_lookup_summary(
    card_fact_lookup_report: CardFactLookupReport | None,
) -> dict[str, Any]:
    if card_fact_lookup_report is None:
        return {
            "status": NOT_REQUESTED,
            "found_count": 0,
            "missing_count": 0,
            "ambiguous_count": 0,
        }
    return {
        "status": CHECKED,
        "found_count": card_fact_lookup_report.found_count,
        "missing_count": card_fact_lookup_report.missing_count,
        "ambiguous_count": card_fact_lookup_report.ambiguous_count,
    }


def _facts_from_lookup_result(
    lookup_result: CardFactLookupResult | None,
) -> tuple[str, str | None, tuple[str, ...], int | float | None]:
    if lookup_result is None:
        return NOT_REQUESTED, None, (), None
    if not lookup_result.is_found:
        return lookup_result.status, None, (), None

    record = lookup_result.record
    if record is None:
        return lookup_result.status, None, (), None

    try:
        facts = card_record_to_role_facts(record)
    except CardFactsError:
        return lookup_result.status, None, (), None

    return (
        lookup_result.status,
        facts.type_line or None,
        _type_labels_from_type_line(facts.type_line),
        facts.mana_value,
    )


def _entry_type_group_labels(entry: WorkspaceViewEntry) -> tuple[str, ...]:
    if entry.card_fact_status == MISSING:
        return (MISSING_CARD_FACTS,)
    if entry.card_fact_status == AMBIGUOUS:
        return (AMBIGUOUS_CARD_FACTS,)
    if entry.card_fact_status == FOUND:
        return entry.type_labels or (UNKNOWN_TYPE,)
    return (UNKNOWN_TYPE,)


def _entry_mana_value_group_label(entry: WorkspaceViewEntry) -> str:
    if entry.card_fact_status == MISSING:
        return MISSING_CARD_FACTS
    if entry.card_fact_status == AMBIGUOUS:
        return AMBIGUOUS_CARD_FACTS
    if entry.card_fact_status == FOUND and entry.mana_value is not None:
        return f"Mana Value {_format_mana_value(entry.mana_value)}"
    return UNKNOWN_MANA_VALUE


def _type_labels_from_type_line(type_line: str) -> tuple[str, ...]:
    labels: list[str] = []
    for segment in type_line.split(" // "):
        type_text = _type_text(segment)
        words = {word.strip() for word in type_text.split() if word.strip()}
        for label in sorted(TYPE_ORDER, key=TYPE_ORDER.__getitem__):
            if label in words and label not in labels:
                labels.append(label)
    return tuple(labels)


def _type_text(type_line: str) -> str:
    for separator in ("\u2014", "\u2013", " - "):
        if separator in type_line:
            return type_line.split(separator, 1)[0].strip()
    return type_line.strip()


def _type_label_sort_key(label: str) -> tuple[int, str]:
    return (
        TYPE_ORDER.get(label, FACT_STATUS_ORDER.get(label, 100)),
        _normalize_text(label),
    )


def _mana_value_label_sort_key(label: str) -> tuple[int, float, str]:
    prefix = "Mana Value "
    if label.startswith(prefix):
        try:
            return (0, float(label[len(prefix):]), label)
        except ValueError:
            return (1, 0.0, label)
    return (FACT_STATUS_ORDER.get(label, 100), 0.0, _normalize_text(label))


def _format_mana_value(value: int | float) -> str:
    if isinstance(value, int):
        return str(value)
    if value.is_integer():
        return str(int(value))
    return str(value)

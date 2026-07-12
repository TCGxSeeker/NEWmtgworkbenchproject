from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from mtg_workbench.deckbuilder.card_facts import card_record_to_role_facts
from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace


ACTIVE_ZONES = ("commander", "mainboard")
ALL_ZONES = ("commander", "mainboard", "maybeboard")
UNCATEGORIZED = "Uncategorized"


@dataclass(frozen=True)
class DeckEntryReference:
    entry_id: str
    zone: str
    quantity: int
    input_name: str
    display_name: str | None
    oracle_id: str | None
    categories: tuple[str, ...]
    is_unresolved: bool

    @property
    def card_name(self) -> str:
        return self.display_name or self.input_name

    @classmethod
    def from_entry(cls, entry: DeckEntry) -> "DeckEntryReference":
        return cls(
            entry_id=entry.entry_id,
            zone=entry.zone,
            quantity=entry.quantity,
            input_name=entry.input_name,
            display_name=entry.display_name,
            oracle_id=entry.oracle_id,
            categories=tuple(entry.categories),
            is_unresolved=entry.is_unresolved,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "zone": self.zone,
            "quantity": self.quantity,
            "input_name": self.input_name,
            "display_name": self.display_name,
            "oracle_id": self.oracle_id,
            "categories": list(self.categories),
            "is_unresolved": self.is_unresolved,
        }


@dataclass(frozen=True)
class DuplicateNonbasicWarning:
    identity: str
    display_name: str
    quantity: int
    entry_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "identity": self.identity,
            "display_name": self.display_name,
            "quantity": self.quantity,
            "entry_ids": list(self.entry_ids),
        }


@dataclass(frozen=True)
class DeckSkeletonReport:
    schema_version: str
    deck_id: str
    deck_name: str
    format: str
    zone_entry_counts: dict[str, int]
    zone_quantity_totals: dict[str, int]
    active_quantity_total: int
    commander_names: tuple[str, ...]
    category_entry_counts: dict[str, int]
    category_quantity_totals: dict[str, int]
    unresolved_entries: tuple[DeckEntryReference, ...]
    missing_card_fact_entries: tuple[DeckEntryReference, ...]
    duplicate_nonbasic_warnings: tuple[DuplicateNonbasicWarning, ...]
    card_fact_lookup_status: str
    user_summary: str
    entries: tuple[DeckEntryReference, ...]

    def to_dict(self, *, include_debug: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "deck_id": self.deck_id,
            "deck_name": self.deck_name,
            "format": self.format,
            "user_summary": self.user_summary,
            "machine_evidence": {
                "zone_entry_counts": dict(self.zone_entry_counts),
                "zone_quantity_totals": dict(self.zone_quantity_totals),
                "active_quantity_total": self.active_quantity_total,
                "commander_names": list(self.commander_names),
                "category_entry_counts": dict(self.category_entry_counts),
                "category_quantity_totals": dict(self.category_quantity_totals),
                "card_fact_lookup_status": self.card_fact_lookup_status,
                "unresolved_entries": [entry.to_dict() for entry in self.unresolved_entries],
                "missing_card_fact_entries": [
                    entry.to_dict() for entry in self.missing_card_fact_entries
                ],
            },
            "mechanical_warnings": {
                "duplicate_nonbasic": [
                    warning.to_dict() for warning in self.duplicate_nonbasic_warnings
                ],
            },
        }

        if include_debug:
            payload["debug_details"] = {
                "entries": [entry.to_dict() for entry in self.entries],
            }

        return payload


def build_deck_skeleton_report(
    workspace: DeckWorkspace,
    *,
    card_records_by_name: Mapping[str, Mapping[str, Any]] | None = None,
) -> DeckSkeletonReport:
    entries = tuple(DeckEntryReference.from_entry(entry) for entry in workspace.all_entries())
    active_entries = tuple(entry for entry in entries if entry.zone in ACTIVE_ZONES)
    record_lookup = _build_record_lookup(card_records_by_name)
    facts_by_entry_id = _facts_by_entry_id(active_entries, record_lookup)

    report = DeckSkeletonReport(
        schema_version="deck_skeleton_report.v0",
        deck_id=workspace.deck_id,
        deck_name=workspace.name,
        format=workspace.format,
        zone_entry_counts=_zone_entry_counts(entries),
        zone_quantity_totals=_zone_quantity_totals(entries),
        active_quantity_total=sum(entry.quantity for entry in active_entries),
        commander_names=tuple(entry.card_name for entry in entries if entry.zone == "commander"),
        category_entry_counts=_category_counts(active_entries, use_quantities=False),
        category_quantity_totals=_category_counts(active_entries, use_quantities=True),
        unresolved_entries=tuple(entry for entry in entries if entry.is_unresolved),
        missing_card_fact_entries=_missing_card_fact_entries(entries, record_lookup),
        duplicate_nonbasic_warnings=_duplicate_nonbasic_warnings(active_entries, facts_by_entry_id),
        card_fact_lookup_status="not_requested" if card_records_by_name is None else "checked",
        user_summary="",
        entries=entries,
    )

    return DeckSkeletonReport(
        **{
            **report.__dict__,
            "user_summary": _build_user_summary(report),
        }
    )


def _build_record_lookup(
    card_records_by_name: Mapping[str, Mapping[str, Any]] | None,
) -> dict[str, Mapping[str, Any]] | None:
    if card_records_by_name is None:
        return None

    lookup: dict[str, Mapping[str, Any]] = {}
    for name, record in card_records_by_name.items():
        key = _normalize_name(name)
        if key and key not in lookup:
            lookup[key] = record
    return lookup


def _facts_by_entry_id(
    entries: tuple[DeckEntryReference, ...],
    record_lookup: dict[str, Mapping[str, Any]] | None,
) -> dict[str, Any]:
    if record_lookup is None:
        return {}

    facts_by_entry_id: dict[str, Any] = {}
    for entry in entries:
        record = _find_record(entry, record_lookup)
        if record is None:
            continue
        facts_by_entry_id[entry.entry_id] = card_record_to_role_facts(dict(record))
    return facts_by_entry_id


def _zone_entry_counts(entries: tuple[DeckEntryReference, ...]) -> dict[str, int]:
    return {zone: sum(1 for entry in entries if entry.zone == zone) for zone in ALL_ZONES}


def _zone_quantity_totals(entries: tuple[DeckEntryReference, ...]) -> dict[str, int]:
    return {zone: sum(entry.quantity for entry in entries if entry.zone == zone) for zone in ALL_ZONES}


def _category_counts(
    entries: tuple[DeckEntryReference, ...],
    *,
    use_quantities: bool,
) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for entry in entries:
        categories = entry.categories or (UNCATEGORIZED,)
        for category in categories:
            counts[category] += entry.quantity if use_quantities else 1
    return dict(sorted(counts.items()))


def _missing_card_fact_entries(
    entries: tuple[DeckEntryReference, ...],
    record_lookup: dict[str, Mapping[str, Any]] | None,
) -> tuple[DeckEntryReference, ...]:
    if record_lookup is None:
        return ()
    return tuple(entry for entry in entries if _find_record(entry, record_lookup) is None)


def _duplicate_nonbasic_warnings(
    entries: tuple[DeckEntryReference, ...],
    facts_by_entry_id: dict[str, Any],
) -> tuple[DuplicateNonbasicWarning, ...]:
    grouped: dict[str, list[DeckEntryReference]] = defaultdict(list)
    display_names: dict[str, str] = {}

    for entry in entries:
        facts = facts_by_entry_id.get(entry.entry_id)
        if facts is None or not _is_confirmed_nonbasic(facts.type_line):
            continue
        identity = entry.oracle_id or _normalize_name(facts.card_name)
        grouped[identity].append(entry)
        display_names.setdefault(identity, facts.card_name)

    warnings: list[DuplicateNonbasicWarning] = []
    for identity in sorted(grouped):
        group = grouped[identity]
        quantity = sum(entry.quantity for entry in group)
        if quantity <= 1:
            continue
        warnings.append(
            DuplicateNonbasicWarning(
                identity=identity,
                display_name=display_names[identity],
                quantity=quantity,
                entry_ids=tuple(entry.entry_id for entry in group),
            )
        )
    return tuple(warnings)


def _find_record(
    entry: DeckEntryReference,
    record_lookup: dict[str, Mapping[str, Any]],
) -> Mapping[str, Any] | None:
    for name in (entry.display_name, entry.input_name):
        key = _normalize_name(name)
        if key in record_lookup:
            return record_lookup[key]
    return None


def _is_confirmed_nonbasic(type_line: str) -> bool:
    normalized = _normalize_name(type_line)
    if not normalized:
        return False
    return not ("basic" in normalized.split() and "land" in normalized.split())


def _build_user_summary(report: DeckSkeletonReport) -> str:
    unresolved_count = len(report.unresolved_entries)
    duplicate_count = len(report.duplicate_nonbasic_warnings)
    return (
        f"{report.deck_name}: {report.active_quantity_total} active cards across "
        f"{report.zone_entry_counts['commander']} commander entries and "
        f"{report.zone_entry_counts['mainboard']} mainboard entries; "
        f"{unresolved_count} unresolved entries; "
        f"{duplicate_count} known non-basic duplicate warnings."
    )


def _normalize_name(value: str | None) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split()).casefold()

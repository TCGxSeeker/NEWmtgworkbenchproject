from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable
from uuid import uuid4

from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace, VALID_ZONES


class WorkspaceMutationError(ValueError):
    pass


def add_entry(
    workspace: DeckWorkspace,
    input_name: str,
    *,
    display_name: str | None = None,
    quantity: int = 1,
    zone: str = "mainboard",
    entry_id: str | None = None,
    oracle_id: str | None = None,
    selected_printing_id: str | None = None,
    categories: Iterable[str] | None = None,
    tags: Iterable[str] | None = None,
    imported_category: str | None = None,
    normalized_category: str | None = None,
    generic_category_hint: str | None = None,
    deck_specific_primary_role: str | None = None,
    secondary_tags: Iterable[str] | None = None,
    category_origin: str | None = None,
    notes: str | None = None,
    pinned: bool = False,
    foil: bool = False,
    date_added: str | None = None,
    is_unresolved: bool = False,
    updated_at: str | None = None,
) -> DeckWorkspace:
    target_zone = _require_zone(zone)
    amount = _require_positive_int(quantity, "quantity")
    clean_input_name = _require_non_empty_string(input_name, "input_name")
    clean_categories = _stable_unique(categories or [], "categories")
    clean_tags = _stable_unique(tags or [], "tags")
    clean_secondary_tags = _stable_unique(secondary_tags or [], "secondary_tags")

    candidate = DeckEntry(
        entry_id=entry_id or str(uuid4()),
        quantity=amount,
        input_name=clean_input_name,
        display_name=display_name,
        oracle_id=oracle_id,
        selected_printing_id=selected_printing_id,
        zone=target_zone,
        categories=clean_categories,
        tags=clean_tags,
        imported_category=imported_category,
        normalized_category=normalized_category,
        generic_category_hint=generic_category_hint,
        deck_specific_primary_role=deck_specific_primary_role,
        secondary_tags=clean_secondary_tags,
        category_origin=category_origin,
        notes=notes,
        pinned=pinned,
        foil=foil,
        date_added=date_added,
        is_unresolved=is_unresolved,
    )

    existing = _find_merge_target(workspace, candidate)
    if existing:
        existing.quantity += amount
        existing.tags = _stable_unique([*existing.tags, *candidate.tags], "tags")
        existing.pinned = existing.pinned or candidate.pinned
        if existing.notes is None and candidate.notes is not None:
            existing.notes = candidate.notes
    else:
        _zone_entries(workspace, target_zone).append(candidate)

    return _mark_dirty(workspace, updated_at)


def remove_entry(
    workspace: DeckWorkspace,
    entry_id: str,
    *,
    updated_at: str | None = None,
) -> DeckWorkspace:
    collection, index, _entry = _require_entry_location(workspace, entry_id)
    del collection[index]
    return _mark_dirty(workspace, updated_at)


def increase_quantity(
    workspace: DeckWorkspace,
    entry_id: str,
    *,
    increment: int = 1,
    updated_at: str | None = None,
) -> DeckWorkspace:
    amount = _require_positive_int(increment, "increment")
    entry = require_entry(workspace, entry_id)
    entry.quantity += amount
    return _mark_dirty(workspace, updated_at)


def decrease_quantity(
    workspace: DeckWorkspace,
    entry_id: str,
    *,
    decrement: int = 1,
    updated_at: str | None = None,
) -> DeckWorkspace:
    amount = _require_positive_int(decrement, "decrement")
    collection, index, entry = _require_entry_location(workspace, entry_id)
    if entry.quantity <= amount:
        del collection[index]
    else:
        entry.quantity -= amount
    return _mark_dirty(workspace, updated_at)


def move_zone(
    workspace: DeckWorkspace,
    entry_id: str,
    zone: str,
    *,
    updated_at: str | None = None,
) -> DeckWorkspace:
    target_zone = _require_zone(zone)
    collection, index, entry = _require_entry_location(workspace, entry_id)
    if entry.zone != target_zone:
        del collection[index]
        entry.zone = target_zone
        _zone_entries(workspace, target_zone).append(entry)
    if target_zone == "commander":
        entry.quantity = 1
    return _mark_dirty(workspace, updated_at)


def set_commander(
    workspace: DeckWorkspace,
    entry_id: str,
    *,
    updated_at: str | None = None,
) -> DeckWorkspace:
    return move_zone(workspace, entry_id, "commander", updated_at=updated_at)


def move_category(
    workspace: DeckWorkspace,
    entry_id: str,
    categories: str | Iterable[str],
    *,
    updated_at: str | None = None,
) -> DeckWorkspace:
    entry = require_entry(workspace, entry_id)
    if isinstance(categories, str):
        entry.categories = [categories]
    else:
        entry.categories = _stable_unique(categories, "categories")
    return _mark_dirty(workspace, updated_at)


def update_tags(
    workspace: DeckWorkspace,
    entry_id: str,
    *,
    tags: Iterable[str] | None = None,
    add: Iterable[str] | None = None,
    remove: Iterable[str] | None = None,
    updated_at: str | None = None,
) -> DeckWorkspace:
    entry = require_entry(workspace, entry_id)
    if tags is not None:
        next_tags = _stable_unique(tags, "tags")
    else:
        next_tags = list(entry.tags)
        if add:
            next_tags = _stable_unique([*next_tags, *add], "tags")
        if remove:
            remove_set = set(remove)
            next_tags = [tag for tag in next_tags if tag not in remove_set]
    entry.tags = next_tags
    return _mark_dirty(workspace, updated_at)


def update_notes(
    workspace: DeckWorkspace,
    entry_id: str,
    notes: str | None,
    *,
    updated_at: str | None = None,
) -> DeckWorkspace:
    entry = require_entry(workspace, entry_id)
    entry.notes = notes
    return _mark_dirty(workspace, updated_at)


def find_entry(workspace: DeckWorkspace, entry_id: str) -> DeckEntry | None:
    for entry in list_entries(workspace):
        if entry.entry_id == entry_id:
            return entry
    return None


def require_entry(workspace: DeckWorkspace, entry_id: str) -> DeckEntry:
    entry = find_entry(workspace, entry_id)
    if entry is None:
        raise WorkspaceMutationError(f"Entry not found: {entry_id}.")
    return entry


def list_entries(workspace: DeckWorkspace) -> list[DeckEntry]:
    return [*workspace.commanders, *workspace.mainboard, *workspace.maybeboard]


def get_zone_entries(workspace: DeckWorkspace, zone: str) -> list[DeckEntry]:
    return _zone_entries(workspace, _require_zone(zone))


def _find_merge_target(workspace: DeckWorkspace, candidate: DeckEntry) -> DeckEntry | None:
    for entry in _zone_entries(workspace, candidate.zone):
        if _can_merge(entry, candidate):
            return entry
    return None


def _can_merge(existing: DeckEntry, candidate: DeckEntry) -> bool:
    if existing.zone != candidate.zone:
        return False
    if existing.selected_printing_id != candidate.selected_printing_id:
        return False
    if existing.categories != candidate.categories:
        return False
    if existing.imported_category != candidate.imported_category:
        return False
    if existing.normalized_category != candidate.normalized_category:
        return False
    if existing.generic_category_hint != candidate.generic_category_hint:
        return False
    if existing.deck_specific_primary_role != candidate.deck_specific_primary_role:
        return False
    if existing.secondary_tags != candidate.secondary_tags:
        return False
    if existing.category_origin != candidate.category_origin:
        return False
    if existing.foil != candidate.foil:
        return False
    if existing.is_unresolved != candidate.is_unresolved:
        return False
    if existing.oracle_id or candidate.oracle_id:
        return existing.oracle_id is not None and existing.oracle_id == candidate.oracle_id
    if existing.is_unresolved:
        return _normalize_name(existing.input_name) == _normalize_name(candidate.input_name)
    return _fallback_name(existing) == _fallback_name(candidate)


def _fallback_name(entry: DeckEntry) -> str:
    return _normalize_name(entry.display_name or entry.input_name)


def _normalize_name(value: str) -> str:
    return " ".join(value.casefold().split())


def _require_entry_location(
    workspace: DeckWorkspace,
    entry_id: str,
) -> tuple[list[DeckEntry], int, DeckEntry]:
    for collection in [workspace.commanders, workspace.mainboard, workspace.maybeboard]:
        for index, entry in enumerate(collection):
            if entry.entry_id == entry_id:
                return collection, index, entry
    raise WorkspaceMutationError(f"Entry not found: {entry_id}.")


def _zone_entries(workspace: DeckWorkspace, zone: str) -> list[DeckEntry]:
    if zone == "commander":
        return workspace.commanders
    if zone == "mainboard":
        return workspace.mainboard
    if zone == "maybeboard":
        return workspace.maybeboard
    raise WorkspaceMutationError(f"Invalid zone: {zone}.")


def _require_zone(zone: str) -> str:
    if zone not in VALID_ZONES:
        raise WorkspaceMutationError(f"Invalid zone: {zone}. Expected one of {sorted(VALID_ZONES)}.")
    return zone


def _require_positive_int(value: int, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise WorkspaceMutationError(f"{field_name} must be a positive integer.")
    if value < 1:
        raise WorkspaceMutationError(f"{field_name} must be at least 1.")
    return value


def _require_non_empty_string(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceMutationError(f"{field_name} must be a non-empty string.")
    return value.strip()


def _stable_unique(values: Iterable[str], field_name: str) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            raise WorkspaceMutationError(f"{field_name} must contain only strings.")
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def _mark_dirty(workspace: DeckWorkspace, updated_at: str | None) -> DeckWorkspace:
    workspace.updated_at = updated_at or _current_timestamp()
    if isinstance(workspace.saved_state, dict):
        workspace.saved_state["is_dirty"] = True
    return workspace


def _current_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

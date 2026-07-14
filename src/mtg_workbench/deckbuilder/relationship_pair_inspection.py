from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from mtg_workbench.deckbuilder.card_behavioral_profile import (
    CardBehavioralProfile,
)
from mtg_workbench.deckbuilder.card_relationship_report import (
    CardRelationshipReport,
    build_card_relationship_report,
)
from mtg_workbench.deckbuilder.relationship_edge_derivation import (
    derive_relationship_edges,
)


class RelationshipPairInspectionError(ValueError):
    pass


def inspect_relationship_pair(
    *,
    source_entry_id: str,
    target_entry_id: str,
    profiles_by_entry_id: Mapping[str, CardBehavioralProfile],
) -> CardRelationshipReport:
    """Inspect one explicit directional pair of behavioral profiles."""

    normalized_source_id = _required_entry_id(
        source_entry_id,
        "source_entry_id",
    )
    normalized_target_id = _required_entry_id(
        target_entry_id,
        "target_entry_id",
    )

    if normalized_source_id == normalized_target_id:
        raise RelationshipPairInspectionError(
            "source_entry_id and target_entry_id must identify "
            "different deck entries."
        )

    if not isinstance(profiles_by_entry_id, Mapping):
        raise RelationshipPairInspectionError(
            "profiles_by_entry_id must be a mapping."
        )

    source_profile = _resolve_profile(
        entry_id=normalized_source_id,
        entry_role="source",
        profiles_by_entry_id=profiles_by_entry_id,
    )
    target_profile = _resolve_profile(
        entry_id=normalized_target_id,
        entry_role="target",
        profiles_by_entry_id=profiles_by_entry_id,
    )

    edges = derive_relationship_edges(
        source_entry_id=normalized_source_id,
        source_profile=source_profile,
        target_entry_id=normalized_target_id,
        target_profile=target_profile,
    )

    return build_card_relationship_report(edges)


def _resolve_profile(
    *,
    entry_id: str,
    entry_role: str,
    profiles_by_entry_id: Mapping[str, CardBehavioralProfile],
) -> CardBehavioralProfile:
    try:
        profile = profiles_by_entry_id[entry_id]
    except KeyError as error:
        raise RelationshipPairInspectionError(
            f"No behavioral profile found for {entry_role} "
            f"entry {entry_id!r}."
        ) from error

    if not isinstance(profile, CardBehavioralProfile):
        raise RelationshipPairInspectionError(
            f"Behavioral profile for {entry_role} entry "
            f"{entry_id!r} must be a CardBehavioralProfile."
        )

    return profile


def _required_entry_id(
    value: Any,
    field_name: str,
) -> str:
    if not isinstance(value, str):
        raise RelationshipPairInspectionError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise RelationshipPairInspectionError(
            f"{field_name} must be a non-empty string."
        )

    return normalized

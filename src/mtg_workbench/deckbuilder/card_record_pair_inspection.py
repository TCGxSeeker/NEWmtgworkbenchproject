from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from mtg_workbench.deckbuilder.behavioral_atom_extraction import (
    extract_card_behavioral_profile,
)
from mtg_workbench.deckbuilder.card_behavioral_profile import (
    CardBehavioralProfile,
    CardBehavioralProfileError,
)
from mtg_workbench.deckbuilder.card_relationship_report import (
    CardRelationshipReport,
)
from mtg_workbench.deckbuilder.relationship_pair_inspection import (
    RelationshipPairInspectionError,
    inspect_relationship_pair,
)


class CardRecordPairInspectionError(ValueError):
    pass


def inspect_card_record_pair(
    *,
    source_entry_id: str,
    source_record: Mapping[str, Any],
    target_entry_id: str,
    target_record: Mapping[str, Any],
) -> CardRelationshipReport:
    """Inspect one explicit directional pair of local card records."""

    normalized_source_id = _required_entry_id(
        source_entry_id,
        "source_entry_id",
    )
    normalized_target_id = _required_entry_id(
        target_entry_id,
        "target_entry_id",
    )

    if normalized_source_id == normalized_target_id:
        raise CardRecordPairInspectionError(
            "source_entry_id and target_entry_id must identify "
            "different deck entries."
        )

    validated_source_record = _required_record(
        source_record,
        "source_record",
    )
    validated_target_record = _required_record(
        target_record,
        "target_record",
    )

    source_profile = _extract_profile(
        record=validated_source_record,
        entry_role="source",
    )
    target_profile = _extract_profile(
        record=validated_target_record,
        entry_role="target",
    )

    profiles_by_entry_id = {
        normalized_source_id: source_profile,
        normalized_target_id: target_profile,
    }

    try:
        return inspect_relationship_pair(
            source_entry_id=normalized_source_id,
            target_entry_id=normalized_target_id,
            profiles_by_entry_id=profiles_by_entry_id,
        )
    except RelationshipPairInspectionError as error:
        raise CardRecordPairInspectionError(str(error)) from error


def _extract_profile(
    *,
    record: Mapping[str, Any],
    entry_role: str,
) -> CardBehavioralProfile:
    try:
        return extract_card_behavioral_profile(record)
    except CardBehavioralProfileError as error:
        raise CardRecordPairInspectionError(
            f"Could not extract {entry_role} behavioral profile: "
            f"{error}"
        ) from error


def _required_record(
    value: Any,
    field_name: str,
) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CardRecordPairInspectionError(
            f"{field_name} must be a mapping."
        )

    return value


def _required_entry_id(
    value: Any,
    field_name: str,
) -> str:
    if not isinstance(value, str):
        raise CardRecordPairInspectionError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise CardRecordPairInspectionError(
            f"{field_name} must be a non-empty string."
        )

    return normalized

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


RESOURCE_KINDS = (
    "mana",
    "treasure",
    "artifact",
    "creature",
    "card_in_hand",
    "graveyard_card",
)

EVENT_KINDS = (
    "spell_cast",
    "noncreature_spell_cast",
    "permanent_entered",
    "attack_declared",
    "combat_damage_dealt",
    "card_discarded",
    "permanent_sacrificed",
    "creature_died",
    "card_drawn",
)

RELATIONSHIP_TYPES = (
    "supplies",
    "triggers",
    "enables",
    "amplifies",
    "protects",
    "recurs",
    "conflicts_with",
)

CONFIDENCE_BANDS = (0, 25, 50, 75, 100)


class RelationshipPrimitiveError(ValueError):
    pass


@dataclass(frozen=True)
class RelationshipEvidence:
    source_behavior: str
    target_behavior: str
    oracle_evidence: tuple[str, ...]
    conditions: tuple[str, ...]
    zones: tuple[str, ...]
    confidence_band: int
    derivation_rule: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_behavior",
            _required_text(self.source_behavior, "source_behavior"),
        )
        object.__setattr__(
            self,
            "target_behavior",
            _required_text(self.target_behavior, "target_behavior"),
        )
        object.__setattr__(
            self,
            "derivation_rule",
            _required_text(self.derivation_rule, "derivation_rule"),
        )
        object.__setattr__(
            self,
            "oracle_evidence",
            _normalized_text_tuple(
                self.oracle_evidence,
                "oracle_evidence",
                require_nonempty=True,
            ),
        )
        object.__setattr__(
            self,
            "conditions",
            _normalized_text_tuple(self.conditions, "conditions"),
        )
        object.__setattr__(
            self,
            "zones",
            _normalized_text_tuple(self.zones, "zones"),
        )

        if type(self.confidence_band) is not int:
            raise RelationshipPrimitiveError(
                "confidence_band must be an integer confidence band."
            )

        if self.confidence_band not in CONFIDENCE_BANDS:
            raise RelationshipPrimitiveError(
                f"Unsupported confidence band: {self.confidence_band!r}."
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "conditions": list(self.conditions),
            "confidence_band": self.confidence_band,
            "derivation_rule": self.derivation_rule,
            "oracle_evidence": list(self.oracle_evidence),
            "source_behavior": self.source_behavior,
            "target_behavior": self.target_behavior,
            "zones": list(self.zones),
        }


@dataclass(frozen=True)
class RelationshipEdge:
    source_entry_id: str
    target_entry_id: str
    relationship_type: str
    evidence: RelationshipEvidence

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_entry_id",
            _required_text(self.source_entry_id, "source_entry_id"),
        )
        object.__setattr__(
            self,
            "target_entry_id",
            _required_text(self.target_entry_id, "target_entry_id"),
        )
        object.__setattr__(
            self,
            "relationship_type",
            _required_text(self.relationship_type, "relationship_type"),
        )

        if self.relationship_type not in RELATIONSHIP_TYPES:
            raise RelationshipPrimitiveError(
                f"Unsupported relationship type: {self.relationship_type!r}."
            )

        if self.source_entry_id == self.target_entry_id:
            raise RelationshipPrimitiveError(
                "Relationship edges must connect different deck entries."
            )

        if not isinstance(self.evidence, RelationshipEvidence):
            raise RelationshipPrimitiveError(
                "evidence must be a RelationshipEvidence instance."
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence": self.evidence.to_dict(),
            "relationship_type": self.relationship_type,
            "source_entry_id": self.source_entry_id,
            "target_entry_id": self.target_entry_id,
        }


def relationship_edge_identity_key(
    edge: RelationshipEdge,
) -> tuple[object, ...]:
    if not isinstance(edge, RelationshipEdge):
        raise RelationshipPrimitiveError(
            "edge must be a RelationshipEdge instance."
        )

    evidence = edge.evidence

    return (
        edge.relationship_type,
        evidence.source_behavior,
        evidence.target_behavior,
        evidence.oracle_evidence,
        evidence.conditions,
        evidence.zones,
        evidence.confidence_band,
        evidence.derivation_rule,
        edge.source_entry_id,
        edge.target_entry_id,
    )


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise RelationshipPrimitiveError(
            f"{field_name} must be a string."
        )

    text = value.strip()

    if not text:
        raise RelationshipPrimitiveError(
            f"{field_name} must be a non-empty string."
        )

    return text


def _normalized_text_tuple(
    values: Iterable[Any],
    field_name: str,
    *,
    require_nonempty: bool = False,
) -> tuple[str, ...]:
    if (
        values is None
        or isinstance(values, (str, bytes, bytearray))
    ):
        raise RelationshipPrimitiveError(
            f"{field_name} must be an iterable of strings."
        )

    try:
        iterator = iter(values)
    except TypeError as error:
        raise RelationshipPrimitiveError(
            f"{field_name} must be an iterable of strings."
        ) from error

    normalized = tuple(
        sorted(
            {
                _required_text(value, field_name)
                for value in iterator
            }
        )
    )

    if require_nonempty and not normalized:
        raise RelationshipPrimitiveError(
            f"{field_name} must contain at least one value."
        )

    return normalized

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable

from mtg_workbench.deckbuilder.relationship_primitives import (
    RelationshipEdge,
)


SCHEMA_VERSION = "card_relationship_report.v0"


class CardRelationshipReportError(ValueError):
    pass


@dataclass(frozen=True)
class CardRelationshipReport:
    schema_version: str
    edges: tuple[RelationshipEdge, ...]
    relationship_types: tuple[str, ...]
    user_summary: str
    machine_evidence: dict[str, Any]
    explanations: tuple[str, ...]
    debug_details: dict[str, Any]

    @property
    def relationship_count(self) -> int:
        return len(self.edges)

    def to_dict(self, *, include_debug: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "user_summary": self.user_summary,
            "relationship_count": self.relationship_count,
            "relationship_types": list(self.relationship_types),
            "machine_evidence": {
                "relationship_count": self.machine_evidence[
                    "relationship_count"
                ],
                "relationship_type_counts": dict(
                    self.machine_evidence["relationship_type_counts"]
                ),
                "edges": list(self.machine_evidence["edges"]),
            },
            "explanations": list(self.explanations),
        }

        if include_debug:
            payload["debug_details"] = dict(self.debug_details)

        return payload


def build_card_relationship_report(
    edges: Iterable[RelationshipEdge],
) -> CardRelationshipReport:
    normalized_edges = _normalize_edges(edges)
    relationship_types = tuple(
        sorted({edge.relationship_type for edge in normalized_edges})
    )
    type_counts = dict(
        sorted(
            Counter(
                edge.relationship_type
                for edge in normalized_edges
            ).items()
        )
    )

    return CardRelationshipReport(
        schema_version=SCHEMA_VERSION,
        edges=normalized_edges,
        relationship_types=relationship_types,
        user_summary=_build_user_summary(normalized_edges),
        machine_evidence={
            "relationship_count": len(normalized_edges),
            "relationship_type_counts": type_counts,
            "edges": [
                edge.to_dict()
                for edge in normalized_edges
            ],
        },
        explanations=tuple(
            _build_explanation(edge)
            for edge in normalized_edges
        ),
        debug_details={
            "report_boundaries": {
                "relationship_derivation": "not_performed",
                "deck_wide_scanning": "not_implemented",
                "all_pairs_comparison": "not_implemented",
                "package_detection": "not_implemented",
                "combo_solving": "not_implemented",
                "synergy_scoring": "not_implemented",
                "recommendations": "not_implemented",
                "strategic_quality_judgments": "not_implemented",
            }
        },
    )


def _normalize_edges(
    edges: Iterable[RelationshipEdge],
) -> tuple[RelationshipEdge, ...]:
    normalized: list[RelationshipEdge] = []

    for edge in edges:
        if not isinstance(edge, RelationshipEdge):
            raise CardRelationshipReportError(
                "Card relationship reports accept only "
                "RelationshipEdge values."
            )

        normalized.append(edge)

    unique = {
        _edge_sort_key(edge): edge
        for edge in normalized
    }

    return tuple(
        unique[key]
        for key in sorted(unique)
    )


def _edge_sort_key(
    edge: RelationshipEdge,
) -> tuple[object, ...]:
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


def _build_user_summary(
    edges: tuple[RelationshipEdge, ...],
) -> str:
    if not edges:
        return "No factual card relationships were provided."

    type_counts = Counter(
        edge.relationship_type
        for edge in edges
    )
    type_summary = ", ".join(
        f"{relationship_type}: {count}"
        for relationship_type, count in sorted(type_counts.items())
    )

    return (
        f"{len(edges)} factual card relationship"
        f"{'' if len(edges) == 1 else 's'} reported "
        f"({type_summary})."
    )


def _build_explanation(
    edge: RelationshipEdge,
) -> str:
    return (
        f"{edge.source_entry_id} {edge.relationship_type} "
        f"{edge.target_entry_id} because "
        f"{edge.evidence.source_behavior} exactly matches "
        f"{edge.evidence.target_behavior}."
    )

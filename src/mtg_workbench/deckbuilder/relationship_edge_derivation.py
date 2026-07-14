from __future__ import annotations

from mtg_workbench.deckbuilder.card_behavioral_profile import (
    BehaviorAtom,
    CardBehavioralProfile,
)
from mtg_workbench.deckbuilder.relationship_primitives import (
    RelationshipEdge,
    RelationshipEvidence,
    relationship_edge_identity_key,
)


def derive_relationship_edges(
    *,
    source_entry_id: str,
    source_profile: CardBehavioralProfile,
    target_entry_id: str,
    target_profile: CardBehavioralProfile,
) -> tuple[RelationshipEdge, ...]:
    edges: list[RelationshipEdge] = []

    edges.extend(
        _derive_exact_matches(
            source_entry_id=source_entry_id,
            target_entry_id=target_entry_id,
            source_atoms=source_profile.outputs,
            target_atoms=target_profile.costs,
            relationship_type="supplies",
            source_dimension="outputs",
            target_dimension="costs",
            derivation_rule="exact_resource_output_matches_cost",
        )
    )

    edges.extend(
        _derive_exact_matches(
            source_entry_id=source_entry_id,
            target_entry_id=target_entry_id,
            source_atoms=source_profile.emitted_events,
            target_atoms=target_profile.observed_events,
            relationship_type="triggers",
            source_dimension="emitted_events",
            target_dimension="observed_events",
            derivation_rule="exact_emitted_event_matches_observer",
        )
    )

    unique = {
        relationship_edge_identity_key(edge): edge
        for edge in edges
    }

    return tuple(
        unique[key]
        for key in sorted(unique)
    )


def _derive_exact_matches(
    *,
    source_entry_id: str,
    target_entry_id: str,
    source_atoms: tuple[BehaviorAtom, ...],
    target_atoms: tuple[BehaviorAtom, ...],
    relationship_type: str,
    source_dimension: str,
    target_dimension: str,
    derivation_rule: str,
) -> tuple[RelationshipEdge, ...]:
    edges: list[RelationshipEdge] = []

    for source_atom in source_atoms:
        for target_atom in target_atoms:
            if source_atom.kind != target_atom.kind:
                continue

            edges.append(
                RelationshipEdge(
                    source_entry_id=source_entry_id,
                    target_entry_id=target_entry_id,
                    relationship_type=relationship_type,
                    evidence=RelationshipEvidence(
                        source_behavior=(
                            f"{source_dimension}:{source_atom.kind}"
                        ),
                        target_behavior=(
                            f"{target_dimension}:{target_atom.kind}"
                        ),
                        oracle_evidence=(
                            source_atom.oracle_evidence
                            + target_atom.oracle_evidence
                        ),
                        conditions=(
                            source_atom.conditions
                            + target_atom.conditions
                        ),
                        zones=(
                            source_atom.zones
                            + target_atom.zones
                        ),
                        confidence_band=100,
                        derivation_rule=derivation_rule,
                    ),
                )
            )

    return tuple(edges)



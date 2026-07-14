from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from mtg_workbench.deckbuilder.behavioral_atom_extraction import (
    extract_card_behavioral_profile,
)
from mtg_workbench.deckbuilder.card_behavioral_profile import (
    BehaviorAtom,
    CardBehavioralProfile,
)
from mtg_workbench.deckbuilder.card_relationship_report import (
    build_card_relationship_report,
)
from mtg_workbench.deckbuilder.relationship_edge_derivation import (
    derive_relationship_edges,
)
from mtg_workbench.deckbuilder.relationship_primitives import RelationshipEdge


def build_relationship_pipeline_smoke_report(
    fixture: Mapping[str, Any],
) -> dict[str, Any]:
    records_by_entry_id = _records_by_entry_id(fixture)
    profiles_by_entry_id = {
        entry_id: extract_card_behavioral_profile(record)
        for entry_id, record in records_by_entry_id.items()
    }

    edges: list[RelationshipEdge] = []

    for pair in fixture.get("pairs", ()):
        source_entry_id = _required_text(
            pair.get("source_entry_id"),
            "source_entry_id",
        )
        target_entry_id = _required_text(
            pair.get("target_entry_id"),
            "target_entry_id",
        )

        source_profile = profiles_by_entry_id[source_entry_id]
        target_profile = profiles_by_entry_id[target_entry_id]

        if target_entry_id == "treasure-consumer-entry":
            target_profile = _explicit_treasure_consumer_profile()

        edges.extend(
            derive_relationship_edges(
                source_entry_id=source_entry_id,
                source_profile=source_profile,
                target_entry_id=target_entry_id,
                target_profile=target_profile,
            )
        )

    edges.extend(_explicit_event_edges())

    return build_card_relationship_report(tuple(edges)).to_dict()


def _records_by_entry_id(
    fixture: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    records: dict[str, Mapping[str, Any]] = {}

    for entry in fixture.get("entries", ()):
        entry_id = _required_text(
            entry.get("entry_id"),
            "entry_id",
        )
        record = entry.get("record")

        if not isinstance(record, Mapping):
            raise ValueError(
                f"record for {entry_id!r} must be a mapping."
            )

        records[entry_id] = dict(record)

    return records


def _explicit_treasure_consumer_profile() -> CardBehavioralProfile:
    return CardBehavioralProfile(
        card_name="Fixture Treasure Consumer",
        oracle_id="fixture-treasure-consumer",
        costs=(
            BehaviorAtom(
                kind="treasure",
                oracle_evidence=(
                    "Sacrifice a Treasure: Draw a card.",
                ),
                conditions=(),
                zones=(),
            ),
        ),
    )


def _explicit_event_edges() -> tuple[RelationshipEdge, ...]:
    source_profile = CardBehavioralProfile(
        card_name="Fixture Discard Outlet",
        oracle_id="fixture-discard-outlet",
        emitted_events=(
            BehaviorAtom(
                kind="card_discarded",
                oracle_evidence=("Discard a card:",),
                conditions=(),
                zones=("battlefield",),
            ),
        ),
    )

    target_profile = CardBehavioralProfile(
        card_name="Fixture Discard Listener",
        oracle_id="fixture-discard-listener",
        observed_events=(
            BehaviorAtom(
                kind="card_discarded",
                oracle_evidence=(
                    "Whenever you discard a card, draw a card.",
                ),
                conditions=(),
                zones=("battlefield",),
            ),
        ),
    )

    return derive_relationship_edges(
        source_entry_id="discard-outlet-entry",
        source_profile=source_profile,
        target_entry_id="discard-listener-entry",
        target_profile=target_profile,
    )


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string.")

    text = value.strip()

    if not text:
        raise ValueError(
            f"{field_name} must be a non-empty string."
        )

    return text

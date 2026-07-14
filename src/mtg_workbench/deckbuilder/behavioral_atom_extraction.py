from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from mtg_workbench.deckbuilder.card_behavioral_profile import (
    BehaviorAtom,
    CardBehavioralProfile,
)


def extract_card_behavioral_profile(
    record: Mapping[str, Any],
) -> CardBehavioralProfile:
    card_name = _text(record.get("name"))
    oracle_id = _optional_text(record.get("oracle_id"))
    oracle_text = _optional_text(record.get("oracle_text")) or ""

    outputs: list[BehaviorAtom] = []
    costs: list[BehaviorAtom] = []
    emitted_events: list[BehaviorAtom] = []
    observed_events: list[BehaviorAtom] = []

    for evidence in _evidence_segments(oracle_text):
        normalized = evidence.casefold()

        if "create a treasure token" in normalized:
            outputs.append(
                BehaviorAtom(
                    kind="treasure",
                    oracle_evidence=(evidence,),
                    conditions=(),
                    zones=(),
                )
            )

        if "discard a card:" in normalized:
            costs.append(
                BehaviorAtom(
                    kind="card_in_hand",
                    oracle_evidence=(evidence,),
                    conditions=(),
                    zones=(),
                )
            )
            emitted_events.append(
                BehaviorAtom(
                    kind="card_discarded",
                    oracle_evidence=(evidence,),
                    conditions=(),
                    zones=(),
                )
            )

        if "sacrifice an artifact:" in normalized:
            costs.append(
                BehaviorAtom(
                    kind="artifact",
                    oracle_evidence=(evidence,),
                    conditions=(),
                    zones=(),
                )
            )
            emitted_events.append(
                BehaviorAtom(
                    kind="permanent_sacrificed",
                    oracle_evidence=(evidence,),
                    conditions=(),
                    zones=(),
                )
            )

        if "whenever you cast a noncreature spell" in normalized:
            observed_events.append(
                BehaviorAtom(
                    kind="noncreature_spell_cast",
                    oracle_evidence=(evidence,),
                    conditions=(),
                    zones=(),
                )
            )

    return CardBehavioralProfile(
        card_name=card_name,
        oracle_id=oracle_id,
        outputs=tuple(outputs),
        costs=tuple(costs),
        requirements=(),
        emitted_events=tuple(emitted_events),
        observed_events=tuple(observed_events),
        permissions=(),
        modifiers=(),
        zone_constraints=(),
        timing_constraints=(),
    )


def _evidence_segments(oracle_text: str) -> tuple[str, ...]:
    segments: list[str] = []

    for line in oracle_text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        segments.append(stripped)

    if not segments and oracle_text.strip():
        segments.append(oracle_text.strip())

    return tuple(segments)


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()

    return ""


def _optional_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None

    text = value.strip()
    return text or None

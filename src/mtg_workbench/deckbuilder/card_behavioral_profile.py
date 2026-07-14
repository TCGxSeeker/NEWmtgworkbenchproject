from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from mtg_workbench.deckbuilder.relationship_primitives import (
    EVENT_KINDS,
    RESOURCE_KINDS,
)


class CardBehavioralProfileError(ValueError):
    pass


@dataclass(frozen=True)
class BehaviorAtom:
    kind: str
    oracle_evidence: tuple[str, ...]
    conditions: tuple[str, ...]
    zones: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "kind",
            _required_text(self.kind, "kind"),
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

    def to_dict(self) -> dict[str, Any]:
        return {
            "conditions": list(self.conditions),
            "kind": self.kind,
            "oracle_evidence": list(self.oracle_evidence),
            "zones": list(self.zones),
        }


@dataclass(frozen=True)
class CardBehavioralProfile:
    card_name: str
    oracle_id: str | None
    outputs: tuple[BehaviorAtom, ...] = ()
    costs: tuple[BehaviorAtom, ...] = ()
    requirements: tuple[BehaviorAtom, ...] = ()
    emitted_events: tuple[BehaviorAtom, ...] = ()
    observed_events: tuple[BehaviorAtom, ...] = ()
    permissions: tuple[BehaviorAtom, ...] = ()
    modifiers: tuple[BehaviorAtom, ...] = ()
    zone_constraints: tuple[str, ...] = ()
    timing_constraints: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "card_name",
            _required_text(self.card_name, "card_name"),
        )
        object.__setattr__(
            self,
            "oracle_id",
            _optional_text(self.oracle_id),
        )

        object.__setattr__(
            self,
            "outputs",
            _normalized_atom_tuple(
                self.outputs,
                field_name="outputs",
                allowed_kinds=RESOURCE_KINDS,
                kind_label="output",
            ),
        )
        object.__setattr__(
            self,
            "costs",
            _normalized_atom_tuple(
                self.costs,
                field_name="costs",
                allowed_kinds=RESOURCE_KINDS,
                kind_label="cost",
            ),
        )
        object.__setattr__(
            self,
            "requirements",
            _normalized_atom_tuple(
                self.requirements,
                field_name="requirements",
            ),
        )
        object.__setattr__(
            self,
            "emitted_events",
            _normalized_atom_tuple(
                self.emitted_events,
                field_name="emitted_events",
                allowed_kinds=EVENT_KINDS,
                kind_label="emitted event",
            ),
        )
        object.__setattr__(
            self,
            "observed_events",
            _normalized_atom_tuple(
                self.observed_events,
                field_name="observed_events",
                allowed_kinds=EVENT_KINDS,
                kind_label="observed event",
            ),
        )
        object.__setattr__(
            self,
            "permissions",
            _normalized_atom_tuple(
                self.permissions,
                field_name="permissions",
            ),
        )
        object.__setattr__(
            self,
            "modifiers",
            _normalized_atom_tuple(
                self.modifiers,
                field_name="modifiers",
            ),
        )
        object.__setattr__(
            self,
            "zone_constraints",
            _normalized_text_tuple(
                self.zone_constraints,
                "zone_constraints",
            ),
        )
        object.__setattr__(
            self,
            "timing_constraints",
            _normalized_text_tuple(
                self.timing_constraints,
                "timing_constraints",
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_name": self.card_name,
            "costs": [atom.to_dict() for atom in self.costs],
            "emitted_events": [
                atom.to_dict() for atom in self.emitted_events
            ],
            "modifiers": [atom.to_dict() for atom in self.modifiers],
            "observed_events": [
                atom.to_dict() for atom in self.observed_events
            ],
            "oracle_id": self.oracle_id,
            "outputs": [atom.to_dict() for atom in self.outputs],
            "permissions": [atom.to_dict() for atom in self.permissions],
            "requirements": [
                atom.to_dict() for atom in self.requirements
            ],
            "timing_constraints": list(self.timing_constraints),
            "zone_constraints": list(self.zone_constraints),
        }


def _normalized_atom_tuple(
    values: Iterable[BehaviorAtom],
    *,
    field_name: str,
    allowed_kinds: tuple[str, ...] | None = None,
    kind_label: str | None = None,
) -> tuple[BehaviorAtom, ...]:
    atoms: list[BehaviorAtom] = []

    for value in values:
        if not isinstance(value, BehaviorAtom):
            raise CardBehavioralProfileError(
                f"{field_name} must contain only BehaviorAtom values."
            )

        if allowed_kinds is not None and value.kind not in allowed_kinds:
            label = kind_label or field_name
            raise CardBehavioralProfileError(
                f"Unsupported {label} kind: {value.kind!r}."
            )

        atoms.append(value)

    unique = {
        (
            atom.kind,
            atom.oracle_evidence,
            atom.conditions,
            atom.zones,
        ): atom
        for atom in atoms
    }

    return tuple(
        unique[key]
        for key in sorted(unique)
    )


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise CardBehavioralProfileError(
            f"{field_name} must be a string."
        )

    text = value.strip()

    if not text:
        raise CardBehavioralProfileError(
            f"{field_name} must be a non-empty string."
        )

    return text


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None

    if not isinstance(value, str):
        raise CardBehavioralProfileError(
            "oracle_id must be a string or None."
        )

    text = value.strip()
    return text or None


def _normalized_text_tuple(
    values: Iterable[Any],
    field_name: str,
    *,
    require_nonempty: bool = False,
) -> tuple[str, ...]:
    normalized = tuple(
        sorted(
            {
                _required_text(value, field_name)
                for value in values
            }
        )
    )

    if require_nonempty and not normalized:
        raise CardBehavioralProfileError(
            f"{field_name} must contain at least one value."
        )

    return normalized

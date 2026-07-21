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


ATOM_COLLECTION_FIELDS = (
    "outputs",
    "costs",
    "requirements",
    "emitted_events",
    "observed_events",
    "permissions",
    "modifiers",
)


def build_relationship_pipeline_smoke_report(
    fixture: Mapping[str, Any],
) -> dict[str, Any]:
    entries_by_entry_id = _entries_by_entry_id(fixture)
    profiles_by_entry_id = {
        entry_id: _profile_for_entry(entry_id, entry)
        for entry_id, entry in entries_by_entry_id.items()
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

        edges.extend(
            derive_relationship_edges(
                source_entry_id=source_entry_id,
                source_profile=source_profile,
                target_entry_id=target_entry_id,
                target_profile=target_profile,
            )
        )

    return build_card_relationship_report(tuple(edges)).to_dict()


def _entries_by_entry_id(
    fixture: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    entries: dict[str, Mapping[str, Any]] = {}

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

        entries[entry_id] = dict(entry)

    return entries


def _profile_for_entry(
    entry_id: str,
    entry: Mapping[str, Any],
) -> CardBehavioralProfile:
    record = entry["record"]
    profile = extract_card_behavioral_profile(record)
    profile_atoms = entry.get("profile_atoms")

    if profile_atoms is None:
        return profile

    if not isinstance(profile_atoms, Mapping):
        raise ValueError(
            f"profile_atoms for {entry_id!r} must be a mapping."
        )

    explicit_atoms = {
        field_name: _profile_atoms(
            profile_atoms.get(field_name, []),
            field_name,
        )
        for field_name in ATOM_COLLECTION_FIELDS
    }

    return CardBehavioralProfile(
        card_name=profile.card_name,
        oracle_id=profile.oracle_id,
        outputs=profile.outputs + explicit_atoms["outputs"],
        costs=profile.costs + explicit_atoms["costs"],
        requirements=(
            profile.requirements
            + explicit_atoms["requirements"]
        ),
        emitted_events=(
            profile.emitted_events
            + explicit_atoms["emitted_events"]
        ),
        observed_events=(
            profile.observed_events
            + explicit_atoms["observed_events"]
        ),
        permissions=profile.permissions + explicit_atoms["permissions"],
        modifiers=profile.modifiers + explicit_atoms["modifiers"],
        zone_constraints=profile.zone_constraints,
        timing_constraints=profile.timing_constraints,
    )


def _profile_atoms(
    value: Any,
    field_name: str,
) -> tuple[BehaviorAtom, ...]:
    if not isinstance(value, list):
        raise ValueError(
            f"profile_atoms.{field_name} must be a list."
        )

    atoms: list[BehaviorAtom] = []

    for index, atom in enumerate(value):
        if not isinstance(atom, Mapping):
            raise ValueError(
                f"profile_atoms.{field_name}[{index}] "
                "must be a mapping."
            )

        atoms.append(
            BehaviorAtom(
                kind=_required_text(
                    atom.get("kind"),
                    f"profile_atoms.{field_name}[{index}].kind",
                ),
                oracle_evidence=_text_tuple(
                    atom.get("oracle_evidence", []),
                    (
                        "profile_atoms."
                        f"{field_name}[{index}].oracle_evidence"
                    ),
                ),
                conditions=_text_tuple(
                    atom.get("conditions", []),
                    f"profile_atoms.{field_name}[{index}].conditions",
                ),
                zones=_text_tuple(
                    atom.get("zones", []),
                    f"profile_atoms.{field_name}[{index}].zones",
                ),
            )
        )

    return tuple(atoms)


def _text_tuple(
    value: Any,
    field_name: str,
) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list.")

    return tuple(
        _required_text(item, field_name)
        for item in value
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

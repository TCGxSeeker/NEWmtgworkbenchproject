from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mtg_workbench.deckbuilder.deck_skeleton_report import DeckSkeletonReport


COMMANDER_FORMAT = "commander"
COMMANDER_ACTIVE_QUANTITY = 100


@dataclass(frozen=True)
class StructuralWarning:
    warning_id: str
    severity: str
    user_summary: str
    machine_evidence: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "warning_id": self.warning_id,
            "severity": self.severity,
            "user_summary": self.user_summary,
            "machine_evidence": dict(self.machine_evidence),
        }


@dataclass(frozen=True)
class StructuralWarningsReport:
    schema_version: str
    deck_id: str
    deck_name: str
    format: str
    warnings: tuple[StructuralWarning, ...]
    user_summary: str

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    def to_dict(self, *, include_debug: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "deck_id": self.deck_id,
            "deck_name": self.deck_name,
            "format": self.format,
            "user_summary": self.user_summary,
            "warning_count": self.warning_count,
            "warnings": [warning.to_dict() for warning in self.warnings],
        }

        if include_debug:
            payload["debug_details"] = {
                "warning_ids": [warning.warning_id for warning in self.warnings],
            }

        return payload


def build_structural_warnings_report(skeleton_report: DeckSkeletonReport) -> StructuralWarningsReport:
    warnings = tuple(_iter_structural_warnings(skeleton_report))
    return StructuralWarningsReport(
        schema_version="structural_warnings_report.v0",
        deck_id=skeleton_report.deck_id,
        deck_name=skeleton_report.deck_name,
        format=skeleton_report.format,
        warnings=warnings,
        user_summary=_build_user_summary(skeleton_report.deck_name, warnings),
    )


def _iter_structural_warnings(skeleton_report: DeckSkeletonReport):
    if skeleton_report.format.casefold() == COMMANDER_FORMAT:
        commander_entries = skeleton_report.zone_entry_counts.get("commander", 0)
        if commander_entries == 0:
            yield StructuralWarning(
                warning_id="missing_commander",
                severity="warning",
                user_summary="Commander deck has no commander entry.",
                machine_evidence={
                    "format": skeleton_report.format,
                    "commander_entry_count": commander_entries,
                },
            )

        if skeleton_report.active_quantity_total != COMMANDER_ACTIVE_QUANTITY:
            yield StructuralWarning(
                warning_id="commander_active_quantity_mismatch",
                severity="warning",
                user_summary="Commander deck active quantity is not 100.",
                machine_evidence={
                    "format": skeleton_report.format,
                    "expected_active_quantity": COMMANDER_ACTIVE_QUANTITY,
                    "actual_active_quantity": skeleton_report.active_quantity_total,
                },
            )

    if skeleton_report.unresolved_entries:
        yield StructuralWarning(
            warning_id="unresolved_entries",
            severity="warning",
            user_summary="Deck contains unresolved entries.",
            machine_evidence={
                "entry_count": len(skeleton_report.unresolved_entries),
                "entry_ids": [entry.entry_id for entry in skeleton_report.unresolved_entries],
            },
        )

    if skeleton_report.missing_card_fact_entries:
        yield StructuralWarning(
            warning_id="missing_card_facts",
            severity="warning",
            user_summary="Deck contains entries without supplied local card facts.",
            machine_evidence={
                "entry_count": len(skeleton_report.missing_card_fact_entries),
                "entry_ids": [
                    entry.entry_id for entry in skeleton_report.missing_card_fact_entries
                ],
            },
        )

    for warning in skeleton_report.duplicate_nonbasic_warnings:
        yield StructuralWarning(
            warning_id="duplicate_known_nonbasic",
            severity="warning",
            user_summary=f"Known non-basic card appears {warning.quantity} times: {warning.display_name}.",
            machine_evidence=warning.to_dict(),
        )


def _build_user_summary(deck_name: str, warnings: tuple[StructuralWarning, ...]) -> str:
    if not warnings:
        return f"{deck_name}: no mechanical structural warnings."
    return f"{deck_name}: {len(warnings)} mechanical structural warnings."

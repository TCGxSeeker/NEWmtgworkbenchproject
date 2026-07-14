from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from mtg_workbench.cards.catalog import CardCatalog, CardRecord
from mtg_workbench.deckbuilder.card_fact_lookup import (
    CardFactLookupReport,
    CardFactLookupResult,
    lookup_workspace_card_facts,
)
from mtg_workbench.deckbuilder.card_role_pipeline import card_record_to_role_evidence_report
from mtg_workbench.deckbuilder.deck_skeleton_report import (
    DeckSkeletonReport,
    build_deck_skeleton_report,
)
from mtg_workbench.deckbuilder.models import DeckWorkspace
from mtg_workbench.deckbuilder.role_report import RoleEvidenceReport
from mtg_workbench.deckbuilder.role_rules import RoleRuleSet
from mtg_workbench.deckbuilder.structural_warnings import (
    StructuralWarningsReport,
    build_structural_warnings_report,
)


SCHEMA_VERSION = "deck_inspection_report.v0"

CardRecordsSource = (
    Iterable[Mapping[str, Any] | CardRecord]
    | Mapping[str, Mapping[str, Any] | CardRecord]
)


class DeckInspectionReportError(ValueError):
    pass


@dataclass(frozen=True)
class CardFactCoverage:
    source_available: bool
    lookup_attempted: bool
    total_entries_considered: int
    found_count: int
    missing_count: int
    ambiguous_count: int
    found_entry_ids: tuple[str, ...]
    missing_entry_ids: tuple[str, ...]
    ambiguous_entry_ids: tuple[str, ...]

    @property
    def has_complete_coverage(self) -> bool:
        return (
            self.lookup_attempted
            and self.found_count == self.total_entries_considered
            and self.missing_count == 0
            and self.ambiguous_count == 0
        )

    @classmethod
    def not_attempted(cls, *, total_entries_considered: int) -> "CardFactCoverage":
        return cls(
            source_available=False,
            lookup_attempted=False,
            total_entries_considered=total_entries_considered,
            found_count=0,
            missing_count=0,
            ambiguous_count=0,
            found_entry_ids=(),
            missing_entry_ids=(),
            ambiguous_entry_ids=(),
        )

    @classmethod
    def from_lookup_report(cls, report: CardFactLookupReport) -> "CardFactCoverage":
        return cls(
            source_available=True,
            lookup_attempted=True,
            total_entries_considered=len(report.results),
            found_count=report.found_count,
            missing_count=report.missing_count,
            ambiguous_count=report.ambiguous_count,
            found_entry_ids=tuple(result.entry_id for result in report.results if result.is_found),
            missing_entry_ids=tuple(result.entry_id for result in report.results if result.is_missing),
            ambiguous_entry_ids=tuple(
                result.entry_id for result in report.results if result.is_ambiguous
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_available": self.source_available,
            "lookup_attempted": self.lookup_attempted,
            "total_entries_considered": self.total_entries_considered,
            "found_count": self.found_count,
            "missing_count": self.missing_count,
            "ambiguous_count": self.ambiguous_count,
            "found_entry_ids": list(self.found_entry_ids),
            "missing_entry_ids": list(self.missing_entry_ids),
            "ambiguous_entry_ids": list(self.ambiguous_entry_ids),
            "has_complete_coverage": self.has_complete_coverage,
        }


@dataclass(frozen=True)
class EntryCardRoleReport:
    entry_id: str
    zone: str
    lookup_name: str
    card_name: str
    role_report: RoleEvidenceReport

    def to_dict(self, *, include_debug: bool = False) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "zone": self.zone,
            "lookup_name": self.lookup_name,
            "card_name": self.card_name,
            "role_report": self.role_report.to_dict(include_debug=include_debug),
        }


@dataclass(frozen=True)
class DeckInspectionReport:
    schema_version: str
    deck_id: str
    deck_name: str
    format: str
    skeleton_report: DeckSkeletonReport
    structural_warnings_report: StructuralWarningsReport
    card_lookup_results: tuple[CardFactLookupResult, ...]
    card_fact_coverage: CardFactCoverage
    card_role_reports: tuple[EntryCardRoleReport, ...]
    user_summary: str
    machine_evidence: dict[str, Any]
    debug_details: dict[str, Any]

    @property
    def found_card_count(self) -> int:
        return self.card_fact_coverage.found_count

    @property
    def missing_card_count(self) -> int:
        return self.card_fact_coverage.missing_count

    @property
    def ambiguous_card_count(self) -> int:
        return self.card_fact_coverage.ambiguous_count

    @property
    def warning_count(self) -> int:
        return self.structural_warnings_report.warning_count

    @property
    def card_role_report_count(self) -> int:
        return len(self.card_role_reports)

    @property
    def has_complete_card_fact_coverage(self) -> bool:
        return self.card_fact_coverage.has_complete_coverage

    def to_dict(self, *, include_debug: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "deck_id": self.deck_id,
            "deck_name": self.deck_name,
            "format": self.format,
            "user_summary": self.user_summary,
            "skeleton_report": self.skeleton_report.to_dict(include_debug=include_debug),
            "structural_warnings_report": self.structural_warnings_report.to_dict(
                include_debug=include_debug
            ),
            "card_fact_coverage": self.card_fact_coverage.to_dict(),
            "card_role_reports": [
                report.to_dict(include_debug=include_debug)
                for report in self.card_role_reports
            ],
            "machine_evidence": dict(self.machine_evidence),
        }

        if include_debug:
            payload["debug_details"] = {
                **self.debug_details,
                "card_lookup_results": [
                    result.to_dict(include_debug=True, include_record=True)
                    for result in self.card_lookup_results
                ],
            }

        return payload


def build_deck_inspection_report(
    workspace: DeckWorkspace,
    *,
    card_records_by_name: CardRecordsSource | None = None,
    card_catalog: CardCatalog | None = None,
    ruleset: RoleRuleSet | None = None,
    include_card_role_evidence: bool = False,
    include_debug: bool = False,
) -> DeckInspectionReport:
    if card_records_by_name is not None and card_catalog is not None:
        raise DeckInspectionReportError("Provide either card_records_by_name or card_catalog, not both.")
    if include_card_role_evidence and ruleset is None:
        raise DeckInspectionReportError(
            "ruleset is required when include_card_role_evidence is true."
        )

    lookup_report = _lookup_report(
        workspace,
        card_records_by_name=card_records_by_name,
        card_catalog=card_catalog,
    )
    skeleton_source = _skeleton_records_from_lookup_report(lookup_report)
    skeleton_report = build_deck_skeleton_report(
        workspace,
        card_records_by_name=skeleton_source,
    )
    structural_warnings_report = build_structural_warnings_report(skeleton_report)
    coverage = (
        CardFactCoverage.from_lookup_report(lookup_report)
        if lookup_report is not None
        else CardFactCoverage.not_attempted(total_entries_considered=len(workspace.all_entries()))
    )
    card_role_reports = _build_card_role_reports(
        lookup_report,
        ruleset=ruleset,
        include_card_role_evidence=include_card_role_evidence,
    )

    report = DeckInspectionReport(
        schema_version=SCHEMA_VERSION,
        deck_id=workspace.deck_id,
        deck_name=workspace.name,
        format=workspace.format,
        skeleton_report=skeleton_report,
        structural_warnings_report=structural_warnings_report,
        card_lookup_results=lookup_report.results if lookup_report is not None else (),
        card_fact_coverage=coverage,
        card_role_reports=card_role_reports,
        user_summary="",
        machine_evidence={},
        debug_details={},
    )

    return DeckInspectionReport(
        **{
            **report.__dict__,
            "user_summary": _build_user_summary(report),
            "machine_evidence": _build_machine_evidence(report),
            "debug_details": _build_debug_details(report) if include_debug else {},
        }
    )


def _lookup_report(
    workspace: DeckWorkspace,
    *,
    card_records_by_name: CardRecordsSource | None,
    card_catalog: CardCatalog | None,
) -> CardFactLookupReport | None:
    if card_records_by_name is None and card_catalog is None:
        return None
    return lookup_workspace_card_facts(
        workspace,
        card_records=card_records_by_name,
        catalog=card_catalog,
    )


def _skeleton_records_from_lookup_report(
    lookup_report: CardFactLookupReport | None,
) -> Mapping[str, Mapping[str, Any]] | None:
    if lookup_report is None:
        return None

    records: dict[str, Mapping[str, Any]] = {}

    for result in lookup_report.results:
        if not result.is_found or result.record is None:
            continue

        records.setdefault(result.lookup_name, result.record)

        record_name = result.record.get("name")
        if isinstance(record_name, str) and record_name.strip():
            records.setdefault(record_name, result.record)

    return records


def _build_card_role_reports(
    lookup_report: CardFactLookupReport | None,
    *,
    ruleset: RoleRuleSet | None,
    include_card_role_evidence: bool,
) -> tuple[EntryCardRoleReport, ...]:
    if not include_card_role_evidence or lookup_report is None:
        return ()

    reports: list[EntryCardRoleReport] = []
    for result in lookup_report.results:
        record = result.record
        if record is None:
            continue
        role_report = card_record_to_role_evidence_report(record, ruleset)
        reports.append(
            EntryCardRoleReport(
                entry_id=result.entry_id,
                zone=result.zone,
                lookup_name=result.lookup_name,
                card_name=role_report.card_name,
                role_report=role_report,
            )
        )
    return tuple(reports)


def _build_user_summary(report: DeckInspectionReport) -> str:
    coverage = report.card_fact_coverage
    lookup_summary = (
        "card fact lookup not attempted"
        if not coverage.lookup_attempted
        else (
            f"{coverage.found_count} found, {coverage.missing_count} missing, "
            f"{coverage.ambiguous_count} ambiguous card fact lookups"
        )
    )
    return (
        f"{report.deck_name}: {report.skeleton_report.active_quantity_total} active cards; "
        f"{lookup_summary}; {report.warning_count} mechanical warnings."
    )


def _build_machine_evidence(report: DeckInspectionReport) -> dict[str, Any]:
    return {
        "active_quantity_total": report.skeleton_report.active_quantity_total,
        "structural_warning_count": report.warning_count,
        "card_fact_coverage": report.card_fact_coverage.to_dict(),
        "card_role_report_count": report.card_role_report_count,
        "role_evidence_is_card_level_only": True,
    }


def _build_debug_details(report: DeckInspectionReport) -> dict[str, Any]:
    return {
        "report_boundaries": {
            "deck_level_role_totals": "not_implemented",
            "strategic_quality_judgments": "not_implemented",
            "recommendations": "not_implemented",
        }
    }

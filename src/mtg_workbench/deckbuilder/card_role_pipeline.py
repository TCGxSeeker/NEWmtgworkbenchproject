from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from mtg_workbench.deckbuilder.card_facts import card_record_to_role_facts
from mtg_workbench.deckbuilder.role_report import RoleEvidenceReport, build_role_evidence_report
from mtg_workbench.deckbuilder.role_rules import RoleRuleSet


def card_record_to_role_evidence_report(
    record: dict[str, Any],
    ruleset: RoleRuleSet,
    *,
    include_unmatched: bool = False,
) -> RoleEvidenceReport:
    facts = card_record_to_role_facts(record)
    return build_role_evidence_report(facts, ruleset, include_unmatched=include_unmatched)


def card_records_to_role_evidence_reports(
    records: Iterable[dict[str, Any]],
    ruleset: RoleRuleSet,
    *,
    include_unmatched: bool = False,
) -> tuple[RoleEvidenceReport, ...]:
    return tuple(
        card_record_to_role_evidence_report(
            record,
            ruleset,
            include_unmatched=include_unmatched,
        )
        for record in records
    )

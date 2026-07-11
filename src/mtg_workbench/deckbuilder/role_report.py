from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mtg_workbench.deckbuilder.role_evidence import (
    CardRoleFacts,
    RoleEvidenceMatch,
    match_all_role_evidence,
)
from mtg_workbench.deckbuilder.role_rules import RoleRuleSet


@dataclass(frozen=True)
class RoleEvidenceReport:
    schema_version: str
    card_name: str
    matched_roles: tuple[RoleEvidenceMatch, ...]
    unmatched_roles: tuple[RoleEvidenceMatch, ...]
    user_summary: str

    @property
    def matched_role_count(self) -> int:
        return len(self.matched_roles)

    @property
    def unmatched_role_count(self) -> int:
        return len(self.unmatched_roles)

    @property
    def best_match(self) -> RoleEvidenceMatch | None:
        if not self.matched_roles:
            return None
        return max(self.matched_roles, key=lambda match: match.score)

    def to_dict(self, *, include_debug: bool = False) -> dict[str, Any]:
        best = self.best_match
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "card_name": self.card_name,
            "user_summary": self.user_summary,
            "matched_role_count": self.matched_role_count,
            "unmatched_role_count": self.unmatched_role_count,
            "best_match": _match_to_dict(best, include_debug=include_debug) if best else None,
            "machine_evidence": [
                _match_to_dict(match, include_debug=include_debug)
                for match in self.matched_roles
            ],
            "explanations": [
                match.explanation
                for match in self.matched_roles
                if match.explanation
            ],
        }

        if self.unmatched_roles:
            payload["unmatched_roles"] = [
                _match_to_dict(match, include_debug=include_debug)
                for match in self.unmatched_roles
            ]

        return payload


def build_role_evidence_report(
    card: CardRoleFacts,
    ruleset: RoleRuleSet,
    *,
    include_unmatched: bool = False,
) -> RoleEvidenceReport:
    all_matches = match_all_role_evidence(card, ruleset, include_unmatched=True)
    matched_roles = tuple(match for match in all_matches if match.matched)
    unmatched_roles = tuple(match for match in all_matches if not match.matched) if include_unmatched else ()

    return RoleEvidenceReport(
        schema_version="role_evidence_report.v0",
        card_name=card.card_name,
        matched_roles=matched_roles,
        unmatched_roles=unmatched_roles,
        user_summary=_build_user_summary(card.card_name, matched_roles),
    )


def _build_user_summary(card_name: str, matched_roles: tuple[RoleEvidenceMatch, ...]) -> str:
    if not matched_roles:
        return f"{card_name}: no role evidence matched."

    best = max(matched_roles, key=lambda match: match.score)
    if len(matched_roles) == 1:
        return f"{card_name}: matched {best.canonical_role} evidence."

    return f"{card_name}: matched {len(matched_roles)} role evidence entries; strongest is {best.canonical_role}."


def _match_to_dict(match: RoleEvidenceMatch | None, *, include_debug: bool) -> dict[str, Any] | None:
    if match is None:
        return None

    payload: dict[str, Any] = {
        "role_id": match.role_id,
        "canonical_role": match.canonical_role,
        "matched": match.matched,
        "score": match.score,
        "matched_field": match.matched_field,
        "matched_value": match.matched_value,
        "exclusion_reason": match.exclusion_reason,
        "user_summary": match.user_summary,
        "explanation": match.explanation,
    }

    if include_debug:
        payload["debug_details"] = match.debug_details

    return payload

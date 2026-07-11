from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mtg_workbench.deckbuilder.role_rules import RoleDefinition, RoleRuleSet, normalize_match_text


@dataclass(frozen=True)
class CardRoleFacts:
    card_name: str
    oracle_text: str = ""
    type_line: str = ""
    subtypes: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    mana_value: int | float | None = None


@dataclass(frozen=True)
class RoleEvidenceMatch:
    role_id: str
    canonical_role: str
    matched: bool
    score: int
    matched_field: str | None = None
    matched_value: str | None = None
    exclusion_reason: str | None = None
    user_summary: str | None = None
    explanation: str | None = None
    debug_details: dict[str, Any] | None = None


def match_role_evidence(card: CardRoleFacts, role: RoleDefinition) -> RoleEvidenceMatch:
    default_score = int(role.score_policy.get("default_score", 0))
    max_score = int(role.score_policy.get("max_score", 100))

    exclusion = _first_exclusion_match(card, role.exclusion_rules)
    if exclusion is not None:
        return RoleEvidenceMatch(
            role_id=role.role_id,
            canonical_role=role.canonical_role,
            matched=False,
            score=default_score,
            matched_field=exclusion["field"],
            matched_value=exclusion["value"],
            exclusion_reason=exclusion["reason"],
            user_summary=role.user_summary_template,
            explanation=exclusion["reason"],
            debug_details={"excluded_by": exclusion},
        )

    candidates = tuple(_iter_evidence_candidates(card, role.evidence_rules))
    if not candidates:
        return RoleEvidenceMatch(
            role_id=role.role_id,
            canonical_role=role.canonical_role,
            matched=False,
            score=default_score,
            user_summary=role.user_summary_template,
            debug_details={"score_policy": role.score_policy},
        )

    best = max(candidates, key=lambda candidate: int(candidate["score"]))
    score = max(0, min(int(best["score"]), max_score))

    return RoleEvidenceMatch(
        role_id=role.role_id,
        canonical_role=role.canonical_role,
        matched=True,
        score=score,
        matched_field=str(best["field"]),
        matched_value=str(best["value"]),
        user_summary=role.user_summary_template,
        explanation=_render_explanation(role.explanation_template, card, best),
        debug_details={"score_policy": role.score_policy, "matched_rule": best},
    )


def match_all_role_evidence(
    card: CardRoleFacts,
    ruleset: RoleRuleSet,
    *,
    include_unmatched: bool = False,
) -> tuple[RoleEvidenceMatch, ...]:
    matches = tuple(match_role_evidence(card, role) for role in ruleset.roles)
    if include_unmatched:
        return matches
    return tuple(match for match in matches if match.matched)


def _iter_evidence_candidates(card: CardRoleFacts, evidence_rules: dict[str, Any]):
    mana_adjustment = _mana_value_adjustment(card, evidence_rules.get("mana_value"))
    if mana_adjustment is None:
        return

    for rule in evidence_rules.get("oracle_text_phrases", []):
        phrase = str(rule.get("phrase", ""))
        if phrase and _contains_normalized(card.oracle_text, phrase):
            yield _candidate("oracle_text", phrase, int(rule.get("score", 0)) + mana_adjustment)

    for rule in evidence_rules.get("type_matches", []):
        field = str(rule.get("field", "type_line"))
        expected = str(rule.get("contains", ""))
        value = _card_field_text(card, field)
        if expected and _contains_normalized(value, expected):
            yield _candidate(field, expected, int(rule.get("score", 0)) + mana_adjustment)

    normalized_subtypes = {normalize_match_text(subtype) for subtype in card.subtypes}
    for rule in evidence_rules.get("subtype_matches", []):
        subtype = str(rule.get("subtype", ""))
        if normalize_match_text(subtype) in normalized_subtypes:
            yield _candidate("subtypes", subtype, int(rule.get("score", 0)) + mana_adjustment)

    normalized_keywords = {normalize_match_text(keyword) for keyword in card.keywords}
    for rule in evidence_rules.get("keyword_matches", []):
        keyword = str(rule.get("keyword", ""))
        if normalize_match_text(keyword) in normalized_keywords:
            yield _candidate("keywords", keyword, int(rule.get("score", 0)) + mana_adjustment)


def _first_exclusion_match(card: CardRoleFacts, exclusion_rules: tuple[dict[str, Any], ...]) -> dict[str, str] | None:
    for rule in exclusion_rules:
        field = str(rule.get("field", ""))
        expected = str(rule.get("contains", ""))
        value = _card_field_text(card, field)
        if field and expected and _contains_normalized(value, expected):
            return {
                "field": field,
                "value": expected,
                "reason": str(rule.get("reason", f"Matched exclusion rule on {field}: {expected}.")),
            }
    return None


def _mana_value_adjustment(card: CardRoleFacts, mana_rule: Any) -> int | None:
    if not isinstance(mana_rule, dict):
        return 0
    if card.mana_value is None:
        return int(mana_rule.get("score_adjustment", 0))

    if "min" in mana_rule and card.mana_value < int(mana_rule["min"]):
        return None
    if "max" in mana_rule and card.mana_value > int(mana_rule["max"]):
        return None
    return int(mana_rule.get("score_adjustment", 0))


def _candidate(field: str, value: str, score: int) -> dict[str, Any]:
    return {"field": field, "value": value, "score": max(0, min(score, 100))}


def _contains_normalized(value: str, expected: str) -> bool:
    return normalize_match_text(expected) in normalize_match_text(value)


def _card_field_text(card: CardRoleFacts, field: str) -> str:
    if field == "oracle_text":
        return card.oracle_text
    if field == "type_line":
        return card.type_line
    return ""


def _render_explanation(template: str | None, card: CardRoleFacts, match: dict[str, Any]) -> str | None:
    if template is None:
        return None
    return template.format(
        card_name=card.card_name,
        matched_field=match["field"],
        matched_value=match["value"],
    )

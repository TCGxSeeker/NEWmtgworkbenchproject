from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import re

import yaml


_SPACE_RE = re.compile(r"\s+")


class RoleRulesError(ValueError):
    pass


@dataclass(frozen=True)
class RoleRuleSet:
    schema_version: int
    roles: tuple[RoleDefinition, ...]
    evidence_score_bands: tuple[EvidenceScoreBand, ...]
    source: str | None = None
    description: str | None = None
    ui_visibility: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RoleRuleSet":
        if not isinstance(payload, dict):
            raise RoleRulesError("Role rules payload must be a mapping.")

        score_bands = tuple(
            EvidenceScoreBand.from_dict(item)
            for item in _require_list(payload, "evidence_score_bands")
        )
        roles = tuple(
            RoleDefinition.from_dict(item)
            for item in _require_list(payload, "roles")
        )

        ruleset = cls(
            schema_version=int(payload.get("schema_version", 1)),
            source=_optional_string(payload.get("source")),
            description=_optional_string(payload.get("description")),
            evidence_score_bands=score_bands,
            ui_visibility=_optional_mapping(payload.get("ui_visibility")),
            roles=roles,
        )
        ruleset.validate()
        return ruleset

    def validate(self) -> None:
        if self.schema_version != 1:
            raise RoleRulesError(f"Unsupported role rules schema_version: {self.schema_version}.")
        if not self.evidence_score_bands:
            raise RoleRulesError("Role rules must define evidence score bands.")
        if not self.roles:
            raise RoleRulesError("Role rules must define at least one role.")

        scores = [band.score for band in self.evidence_score_bands]
        if sorted(scores) != sorted(set(scores)):
            raise RoleRulesError("Evidence score bands must not contain duplicate scores.")
        for score in scores:
            _validate_score(score, "evidence score band")

        role_ids: set[str] = set()
        canonical_roles: set[str] = set()
        for role in self.roles:
            role.validate()
            normalized_role_id = normalize_role_key(role.role_id)
            normalized_canonical = normalize_role_key(role.canonical_role)
            if normalized_role_id in role_ids:
                raise RoleRulesError(f"Duplicate role_id: {role.role_id}.")
            if normalized_canonical in canonical_roles:
                raise RoleRulesError(f"Duplicate canonical_role: {role.canonical_role}.")
            role_ids.add(normalized_role_id)
            canonical_roles.add(normalized_canonical)

    def get_role(self, role_id_or_name: str) -> RoleDefinition | None:
        key = normalize_role_key(role_id_or_name)
        for role in self.roles:
            if key in {normalize_role_key(role.role_id), normalize_role_key(role.canonical_role)}:
                return role
        return None


@dataclass(frozen=True)
class EvidenceScoreBand:
    score: int
    meaning: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "EvidenceScoreBand":
        if not isinstance(payload, dict):
            raise RoleRulesError("Evidence score band must be a mapping.")
        if "score" not in payload:
            raise RoleRulesError("Evidence score band is missing score.")
        if "meaning" not in payload:
            raise RoleRulesError("Evidence score band is missing meaning.")
        return cls(score=int(payload["score"]), meaning=str(payload["meaning"]))


@dataclass(frozen=True)
class RoleDefinition:
    role_id: str
    canonical_role: str
    description: str | None
    evidence_rules: dict[str, Any]
    exclusion_rules: tuple[dict[str, Any], ...]
    score_policy: dict[str, Any]
    user_summary_template: str | None
    explanation_template: str | None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RoleDefinition":
        if not isinstance(payload, dict):
            raise RoleRulesError("Role definition must be a mapping.")

        role = cls(
            role_id=_require_string(payload, "role_id"),
            canonical_role=_require_string(payload, "canonical_role"),
            description=_optional_string(payload.get("description")),
            evidence_rules=_require_mapping(payload, "evidence_rules"),
            exclusion_rules=tuple(_require_exclusion_rules(payload.get("exclusion_rules", []))),
            score_policy=_require_mapping(payload, "score_policy"),
            user_summary_template=_optional_string(payload.get("user_summary_template")),
            explanation_template=_optional_string(payload.get("explanation_template")),
        )
        role.validate()
        return role

    def validate(self) -> None:
        if not normalize_role_key(self.role_id):
            raise RoleRulesError("role_id must not be empty.")
        if not normalize_role_key(self.canonical_role):
            raise RoleRulesError("canonical_role must not be empty.")
        if not self.evidence_rules:
            raise RoleRulesError(f"Role {self.role_id!r} must define evidence_rules.")

        combine = self.score_policy.get("combine")
        if combine != "highest_match":
            raise RoleRulesError(
                f"Role {self.role_id!r} uses unsupported score_policy.combine: {combine!r}."
            )

        default_score = int(self.score_policy.get("default_score", 0))
        max_score = int(self.score_policy.get("max_score", 100))
        _validate_score(default_score, f"{self.role_id} default_score")
        _validate_score(max_score, f"{self.role_id} max_score")
        if default_score > max_score:
            raise RoleRulesError(f"Role {self.role_id!r} default_score must not exceed max_score.")

        _validate_scores_in_mapping(self.evidence_rules, f"role {self.role_id} evidence_rules")


def load_role_rules(path: str | Path) -> RoleRuleSet:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    return RoleRuleSet.from_dict(payload)


def normalize_role_key(value: str) -> str:
    return normalize_match_text(value)


def normalize_match_text(value: str) -> str:
    return _SPACE_RE.sub(" ", str(value).strip()).casefold()


def _require_list(payload: dict[str, Any], key: str) -> list[Any]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise RoleRulesError(f"Role rules field {key!r} must be a list.")
    return value


def _require_mapping(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise RoleRulesError(f"Role rules field {key!r} must be a mapping.")
    return value


def _optional_mapping(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise RoleRulesError("Optional mapping field must be a mapping when provided.")
    return value


def _require_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if value is None:
        raise RoleRulesError(f"Role rules field {key!r} is required.")
    text = str(value)
    if not text.strip():
        raise RoleRulesError(f"Role rules field {key!r} must not be empty.")
    return text


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _require_exclusion_rules(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise RoleRulesError("exclusion_rules must be a list.")
    for item in value:
        if not isinstance(item, dict):
            raise RoleRulesError("Each exclusion rule must be a mapping.")
    return value


def _validate_score(score: int, label: str) -> None:
    if score < 0 or score > 100:
        raise RoleRulesError(f"{label} must be between 0 and 100.")


def _validate_scores_in_mapping(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "score":
                _validate_score(int(item), label)
            elif key == "score_adjustment":
                adjustment = int(item)
                if adjustment < -100 or adjustment > 100:
                    raise RoleRulesError(f"{label} score_adjustment must be between -100 and 100.")
            else:
                _validate_scores_in_mapping(item, label)
    elif isinstance(value, list):
        for item in value:
            _validate_scores_in_mapping(item, label)


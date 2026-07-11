from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import re


_SPACE_RE = re.compile(r"\s+")


class CategoryTaxonomyError(ValueError):
    pass


@dataclass(frozen=True)
class CategoryNormalization:
    input_category: str
    normalized_category: str | None
    category_origin: str

    @property
    def is_known(self) -> bool:
        return self.normalized_category is not None


@dataclass(frozen=True)
class CategoryTaxonomy:
    schema_version: int
    canonical_categories: tuple[str, ...]
    aliases: dict[str, str]
    source: str | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "CategoryTaxonomy":
        canonical_categories = tuple(str(category) for category in payload.get("canonical_categories", []))
        aliases = {str(alias): str(category) for alias, category in dict(payload.get("aliases", {})).items()}
        taxonomy = cls(
            schema_version=int(payload.get("schema_version", 1)),
            source=_optional_string(payload.get("source")),
            description=_optional_string(payload.get("description")),
            canonical_categories=canonical_categories,
            aliases=aliases,
        )
        taxonomy.validate()
        return taxonomy

    def validate(self) -> None:
        if self.schema_version != 1:
            raise CategoryTaxonomyError(f"Unsupported category taxonomy schema_version: {self.schema_version}.")
        if not self.canonical_categories:
            raise CategoryTaxonomyError("Category taxonomy must define at least one canonical category.")

        seen_keys: set[str] = set()
        for category in self.canonical_categories:
            key = normalize_category_key(category)
            if not key:
                raise CategoryTaxonomyError("Canonical categories must not be empty.")
            if key in seen_keys:
                raise CategoryTaxonomyError(f"Duplicate canonical category: {category}.")
            seen_keys.add(key)

        canonical_keys = {normalize_category_key(category) for category in self.canonical_categories}
        for alias, canonical in self.aliases.items():
            if not normalize_category_key(alias):
                raise CategoryTaxonomyError("Category aliases must not be empty.")
            if normalize_category_key(canonical) not in canonical_keys:
                raise CategoryTaxonomyError(f"Alias {alias!r} points to unknown category {canonical!r}.")

    def normalize(self, category: str) -> CategoryNormalization:
        original = category
        key = normalize_category_key(category)
        canonical_by_key = {normalize_category_key(name): name for name in self.canonical_categories}
        if key in canonical_by_key:
            return CategoryNormalization(
                input_category=original,
                normalized_category=canonical_by_key[key],
                category_origin="normalized",
            )

        alias_by_key = {normalize_category_key(alias): target for alias, target in self.aliases.items()}
        if key in alias_by_key:
            return CategoryNormalization(
                input_category=original,
                normalized_category=alias_by_key[key],
                category_origin="normalized",
            )

        return CategoryNormalization(
            input_category=original,
            normalized_category=None,
            category_origin="unknown",
        )

    def is_canonical(self, category: str) -> bool:
        return self.normalize(category).normalized_category in self.canonical_categories and (
            normalize_category_key(category) in {normalize_category_key(name) for name in self.canonical_categories}
        )


def load_category_taxonomy(path: str | Path) -> CategoryTaxonomy:
    payload = _load_tiny_taxonomy_yaml(Path(path))
    return CategoryTaxonomy.from_dict(payload)


def normalize_category_key(category: str) -> str:
    return _SPACE_RE.sub(" ", category.strip()).casefold()


def _load_tiny_taxonomy_yaml(path: Path) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    current_section: str | None = None
    nested_section: str | None = None

    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            if not raw_line.strip() or raw_line.lstrip().startswith("#"):
                continue

            indent = len(raw_line) - len(raw_line.lstrip(" "))
            stripped = raw_line.strip()

            if indent == 0:
                key, value = _split_yaml_pair(stripped)
                current_section = key
                nested_section = None
                if value == "":
                    if key in {"canonical_categories", "deferred"}:
                        payload[key] = []
                    elif key in {"aliases", "field_model"}:
                        payload[key] = {}
                    else:
                        payload[key] = {}
                else:
                    payload[key] = _parse_scalar(value)
                continue

            if current_section is None:
                continue

            if stripped.startswith("- "):
                value = stripped[2:].strip()
                if nested_section and isinstance(payload.get(current_section), dict):
                    nested_values = payload[current_section].setdefault(nested_section, [])
                    nested_values.append(_parse_scalar(value))
                else:
                    section_values = payload.setdefault(current_section, [])
                    if not isinstance(section_values, list):
                        raise CategoryTaxonomyError(f"Section {current_section!r} does not accept list items.")
                    section_values.append(_parse_scalar(value))
                continue

            key, value = _split_yaml_pair(stripped)
            section = payload.setdefault(current_section, {})
            if not isinstance(section, dict):
                raise CategoryTaxonomyError(f"Section {current_section!r} does not accept mapping values.")
            if value == "":
                section[key] = []
                nested_section = key
            else:
                section[key] = _parse_scalar(value)
                nested_section = None

    return payload


def _split_yaml_pair(line: str) -> tuple[str, str]:
    if ":" not in line:
        raise CategoryTaxonomyError(f"Expected YAML key/value pair: {line}.")
    key, value = line.split(":", 1)
    return key.strip(), value.strip()


def _parse_scalar(value: str) -> str | int:
    if value.isdigit():
        return int(value)
    return value


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)

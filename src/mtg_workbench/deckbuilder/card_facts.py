from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from mtg_workbench.deckbuilder.role_evidence import CardRoleFacts


class CardFactsError(ValueError):
    pass


def card_record_to_role_facts(record: dict[str, Any]) -> CardRoleFacts:
    if not isinstance(record, dict):
        raise CardFactsError("Card record must be a dictionary.")

    card_name = _require_card_name(record)
    oracle_text = _text_or_faces(record, "oracle_text", separator="\n")
    type_line = _text_or_faces(record, "type_line", separator=" // ")

    return CardRoleFacts(
        card_name=card_name,
        oracle_text=oracle_text,
        type_line=type_line,
        subtypes=_derive_subtypes(type_line),
        keywords=_keywords(record),
        mana_value=_mana_value(record),
    )


def records_to_role_facts(records: Iterable[dict[str, Any]]) -> tuple[CardRoleFacts, ...]:
    return tuple(card_record_to_role_facts(record) for record in records)


def _require_card_name(record: dict[str, Any]) -> str:
    value = record.get("name")
    if not isinstance(value, str) or not value.strip():
        raise CardFactsError("Card record is missing required name.")
    return value


def _text_or_faces(record: dict[str, Any], field_name: str, *, separator: str) -> str:
    value = record.get(field_name)
    if isinstance(value, str):
        return value
    if field_name in record:
        return ""

    face_values: list[str] = []
    card_faces = record.get("card_faces")
    if isinstance(card_faces, (list, tuple)):
        for face in card_faces:
            if isinstance(face, dict) and isinstance(face.get(field_name), str):
                face_values.append(face[field_name])
    return separator.join(face_values)


def _keywords(record: dict[str, Any]) -> tuple[str, ...]:
    value = record.get("keywords")
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(str(keyword) for keyword in value if keyword is not None)


def _mana_value(record: dict[str, Any]) -> int | float | None:
    for field_name in ("mana_value", "cmc"):
        if field_name not in record:
            continue
        value = _number(record[field_name])
        if value is not None:
            return value
    return None


def _number(value: Any) -> int | float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value) if value.is_integer() else value
    if isinstance(value, str):
        try:
            number = float(value.strip())
        except ValueError:
            return None
        return int(number) if number.is_integer() else number
    return None


def _derive_subtypes(type_line: str) -> tuple[str, ...]:
    subtypes: list[str] = []
    for segment in type_line.split(" // "):
        subtype_text = _subtype_text(segment)
        if not subtype_text:
            continue
        subtypes.extend(subtype_text.split())
    return tuple(subtypes)


def _subtype_text(type_line: str) -> str:
    for separator in ("\\u2014", "\\u2013", " - "):
        separator_text = separator.encode("utf-8").decode("unicode_escape") if separator.startswith("\\u") else separator
        if separator_text in type_line:
            return type_line.split(separator_text, 1)[1].strip()
    return ""

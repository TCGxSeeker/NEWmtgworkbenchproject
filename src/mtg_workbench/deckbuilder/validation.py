from __future__ import annotations

from typing import Any

from mtg_workbench.deckbuilder.models import SCHEMA_VERSION, VALID_CATEGORY_ORIGINS, VALID_ZONES


class WorkspaceValidationError(ValueError):
    def __init__(self, messages: list[str]) -> None:
        self.messages = messages
        super().__init__("; ".join(messages))


def validate_workspace_payload(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["Workspace JSON must be an object."]

    _require_fields(
        errors,
        payload,
        [
            "schema_version",
            "deck_id",
            "name",
            "format",
            "tags",
            "commanders",
            "mainboard",
            "maybeboard",
            "saved_state",
        ],
        "workspace",
    )

    if "schema_version" in payload:
        if not _is_int(payload["schema_version"]):
            errors.append("Workspace field schema_version must be an integer.")
        elif payload["schema_version"] != SCHEMA_VERSION:
            errors.append(f"Unsupported schema_version {payload['schema_version']}; expected {SCHEMA_VERSION}.")

    _check_string(errors, payload, "deck_id", "workspace", allow_empty=False)
    _check_string(errors, payload, "name", "workspace", allow_empty=False)
    _check_string(errors, payload, "format", "workspace", allow_empty=False)
    _check_optional_string(errors, payload, "created_at", "workspace")
    _check_optional_string(errors, payload, "updated_at", "workspace")
    _check_optional_string(errors, payload, "notes", "workspace")
    _check_string_list(errors, payload, "tags", "workspace")

    if "metadata" in payload and not isinstance(payload["metadata"], dict):
        errors.append("Workspace field metadata must be an object when present.")
    if "saved_state" in payload and not isinstance(payload["saved_state"], dict):
        errors.append("Workspace field saved_state must be an object.")

    _check_entry_section(errors, payload, "commanders", "commander")
    _check_entry_section(errors, payload, "mainboard", "mainboard")
    _check_entry_section(errors, payload, "maybeboard", "maybeboard")
    _check_unique_entry_ids(errors, payload)
    return errors


def _check_entry_section(
    errors: list[str],
    payload: dict[str, Any],
    section_name: str,
    expected_zone: str,
) -> None:
    if section_name not in payload:
        return
    section = payload[section_name]
    if not isinstance(section, list):
        errors.append(f"Workspace field {section_name} must be a list.")
        return

    for index, entry in enumerate(section):
        location = f"{section_name}[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{location} must be an object.")
            continue
        _validate_entry(errors, entry, location, expected_zone)


def _validate_entry(
    errors: list[str],
    entry: dict[str, Any],
    location: str,
    expected_zone: str,
) -> None:
    _require_fields(
        errors,
        entry,
        [
            "entry_id",
            "quantity",
            "input_name",
            "display_name",
            "zone",
            "categories",
            "tags",
            "is_unresolved",
        ],
        location,
    )

    _check_string(errors, entry, "entry_id", location, allow_empty=False)
    _check_string(errors, entry, "input_name", location, allow_empty=False)
    _check_optional_string(errors, entry, "display_name", location)
    _check_optional_string(errors, entry, "oracle_id", location)
    _check_optional_string(errors, entry, "selected_printing_id", location)
    _check_optional_string(errors, entry, "notes", location)
    _check_optional_string(errors, entry, "date_added", location)
    _check_optional_string(errors, entry, "imported_category", location)
    _check_optional_string(errors, entry, "normalized_category", location)
    _check_optional_string(errors, entry, "generic_category_hint", location)
    _check_optional_string(errors, entry, "deck_specific_primary_role", location)
    _check_optional_category_origin(errors, entry, location)
    _check_string_list(errors, entry, "categories", location)
    _check_string_list(errors, entry, "tags", location)
    _check_string_list(errors, entry, "secondary_tags", location)

    if "quantity" in entry:
        if not _is_int(entry["quantity"]):
            errors.append(f"{location}.quantity must be an integer.")
        elif entry["quantity"] < 1:
            errors.append(f"{location}.quantity must be at least 1.")

    if "zone" in entry:
        zone = entry["zone"]
        if not isinstance(zone, str):
            errors.append(f"{location}.zone must be a string.")
        elif zone not in VALID_ZONES:
            errors.append(f"{location}.zone must be one of {sorted(VALID_ZONES)}.")
        elif zone != expected_zone:
            errors.append(f"{location}.zone is {zone!r}, but entries in {location.split('[')[0]} must use {expected_zone!r}.")

    _check_bool(errors, entry, "is_unresolved", location)
    _check_optional_bool(errors, entry, "pinned", location)
    _check_optional_bool(errors, entry, "foil", location)



def _check_unique_entry_ids(errors: list[str], payload: dict[str, Any]) -> None:
    first_locations: dict[str, str] = {}

    for section_name in ("commanders", "mainboard", "maybeboard"):
        section = payload.get(section_name)
        if not isinstance(section, list):
            continue

        for index, entry in enumerate(section):
            if not isinstance(entry, dict):
                continue

            entry_id = entry.get("entry_id")
            if not isinstance(entry_id, str) or not entry_id.strip():
                continue

            location = f"{section_name}[{index}]"
            first_location = first_locations.get(entry_id)
            if first_location is not None:
                errors.append(
                    f"Duplicate entry_id {entry_id!r} at {location}; "
                    f"first used at {first_location}."
                )
                continue

            first_locations[entry_id] = location

def _require_fields(errors: list[str], payload: dict[str, Any], fields: list[str], location: str) -> None:
    for field_name in fields:
        if field_name not in payload:
            errors.append(f"Missing required {location} field: {field_name}.")


def _check_string(
    errors: list[str],
    payload: dict[str, Any],
    field_name: str,
    location: str,
    allow_empty: bool,
) -> None:
    if field_name not in payload:
        return
    value = payload[field_name]
    if not isinstance(value, str):
        errors.append(f"{location}.{field_name} must be a string.")
    elif not allow_empty and not value.strip():
        errors.append(f"{location}.{field_name} must not be empty.")


def _check_optional_string(errors: list[str], payload: dict[str, Any], field_name: str, location: str) -> None:
    if field_name not in payload or payload[field_name] is None:
        return
    if not isinstance(payload[field_name], str):
        errors.append(f"{location}.{field_name} must be a string or null.")


def _check_string_list(errors: list[str], payload: dict[str, Any], field_name: str, location: str) -> None:
    if field_name not in payload:
        return
    value = payload[field_name]
    if not isinstance(value, list):
        errors.append(f"{location}.{field_name} must be a list of strings.")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{location}.{field_name}[{index}] must be a string.")


def _check_bool(errors: list[str], payload: dict[str, Any], field_name: str, location: str) -> None:
    if field_name not in payload:
        return
    if not isinstance(payload[field_name], bool):
        errors.append(f"{location}.{field_name} must be a boolean.")


def _check_optional_bool(errors: list[str], payload: dict[str, Any], field_name: str, location: str) -> None:
    if field_name not in payload:
        return
    _check_bool(errors, payload, field_name, location)


def _check_optional_category_origin(errors: list[str], payload: dict[str, Any], location: str) -> None:
    if "category_origin" not in payload or payload["category_origin"] is None:
        return
    value = payload["category_origin"]
    if not isinstance(value, str):
        errors.append(f"{location}.category_origin must be a string or null.")
    elif value not in VALID_CATEGORY_ORIGINS:
        errors.append(f"{location}.category_origin must be one of {sorted(VALID_CATEGORY_ORIGINS)}.")


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)

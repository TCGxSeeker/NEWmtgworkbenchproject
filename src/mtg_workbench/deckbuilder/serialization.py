from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mtg_workbench.deckbuilder.models import DeckWorkspace
from mtg_workbench.deckbuilder.validation import WorkspaceValidationError, validate_workspace_payload


NATIVE_WORKSPACE_EXTENSION = ".mtgwdeck.json"


def is_native_workspace_path(path: str | Path) -> bool:
    return str(path).casefold().endswith(NATIVE_WORKSPACE_EXTENSION)


def dumps_workspace(workspace: DeckWorkspace) -> str:
    payload = workspace.to_dict()
    _raise_if_invalid(payload)
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def loads_workspace(text: str) -> DeckWorkspace:
    try:
        payload: Any = json.loads(text)
    except json.JSONDecodeError as exc:
        message = f"Malformed workspace JSON: {exc.msg} at line {exc.lineno} column {exc.colno}."
        raise WorkspaceValidationError([message]) from exc

    _raise_if_invalid(payload)
    return DeckWorkspace.from_dict(payload)


def _dumps_workspace_for_save(workspace: DeckWorkspace) -> str:
    payload = workspace.to_dict()
    saved_state = payload.get("saved_state")

    if isinstance(saved_state, dict):
        saved_state["is_dirty"] = False

    _raise_if_invalid(payload)
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def save_workspace(workspace: DeckWorkspace, path: str | Path) -> None:
    workspace_path = Path(path)
    workspace_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = workspace_path.with_name(f"{workspace_path.name}.tmp")
    serialized = _dumps_workspace_for_save(workspace)

    try:
        temp_path.write_text(serialized, encoding="utf-8")
        temp_path.replace(workspace_path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise

    _mark_clean(workspace)


def load_workspace(path: str | Path) -> DeckWorkspace:
    workspace_path = Path(path)
    workspace = loads_workspace(workspace_path.read_text(encoding="utf-8"))
    _mark_clean(workspace)
    return workspace


def _raise_if_invalid(payload: Any) -> None:
    errors = validate_workspace_payload(payload)
    if errors:
        raise WorkspaceValidationError(errors)


def _mark_clean(workspace: DeckWorkspace) -> None:
    if isinstance(workspace.saved_state, dict):
        workspace.saved_state["is_dirty"] = False

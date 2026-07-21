from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from mtg_workbench.cards.catalog import CardCatalog
from mtg_workbench.deckbuilder.categories import load_category_taxonomy
from mtg_workbench.deckbuilder.deck_inspection_report import build_deck_inspection_report
from mtg_workbench.deckbuilder.import_export import (
    export_plain_text_decklist,
    import_plain_text_decklist,
)
from mtg_workbench.deckbuilder.mutations import (
    WorkspaceMutationError,
    add_entry,
    add_secondary_tag,
    clear_category_metadata,
    decrease_quantity,
    find_entry,
    increase_quantity,
    move_zone,
    remove_secondary_tag,
    remove_entry,
    replace_secondary_tags,
    set_category_origin,
    set_commander,
    set_generic_category_hint,
    set_imported_category,
    set_normalized_category,
    update_notes,
    update_tags,
)
from mtg_workbench.deckbuilder.models import VALID_CATEGORY_ORIGINS
from mtg_workbench.deckbuilder.role_rules import load_role_rules
from mtg_workbench.deckbuilder.serialization import (
    is_native_workspace_path,
    load_workspace,
    save_workspace,
)
from mtg_workbench.decks.normalizer import normalize_deck
from mtg_workbench.decks.parser import parse_decklist
from mtg_workbench.io.json_output import stable_json
from mtg_workbench.scryfall.indexer import build_scryfall_index
from mtg_workbench.scryfall.search import search_cards


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mtg", description="Local MTG Workbench utilities.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_parser = subparsers.add_parser("parse", help="Parse and normalize a local decklist.")
    parse_parser.add_argument("decklist_path", type=Path)
    parse_parser.add_argument("--cards", required=True, type=Path, help="Local card snapshot JSON.")

    index_parser = subparsers.add_parser(
        "index-scryfall",
        help="Build a local SQLite index from local Scryfall bulk snapshots.",
    )
    index_parser.add_argument("--raw-dir", required=True, type=Path, help="Local Scryfall raw snapshot directory.")
    index_parser.add_argument("--output", required=True, type=Path, help="SQLite index output path.")

    search_parser = subparsers.add_parser("search", help="Search the local Scryfall SQLite index.")
    search_parser.add_argument("query", help="Quoted local Scryfall syntax subset query.")
    search_parser.add_argument("--index", required=True, type=Path, help="Local Scryfall SQLite index path.")
    search_parser.add_argument("--limit", type=int, default=25, help="Maximum result rows to return.")

    inspect_parser = subparsers.add_parser(
        "inspect-deck",
        help="Build a factual inspection report from a native deck workspace.",
    )
    inspect_parser.add_argument("workspace_path", type=Path, help="Native .mtgwdeck.json workspace.")
    card_source_group = inspect_parser.add_mutually_exclusive_group()
    card_source_group.add_argument("--cards", type=Path, help="Local card catalog JSON.")
    card_source_group.add_argument(
        "--card-records",
        type=Path,
        help="Local card-record JSON mapping or list.",
    )
    inspect_parser.add_argument(
        "--role-rules",
        type=Path,
        help="Local role-rules YAML for optional card-level role evidence.",
    )
    inspect_parser.add_argument(
        "--include-role-evidence",
        action="store_true",
        help="Include card-level role evidence for found local card records.",
    )
    inspect_parser.add_argument(
        "--debug",
        action="store_true",
        help="Include debug/internal report details.",
    )
    inspect_parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Emit a compact factual summary instead of the full nested report.",
    )

    workspace_import_parser = subparsers.add_parser(
        "workspace-import",
        help="Import a plain text decklist into a native workspace file.",
    )
    workspace_import_parser.add_argument("decklist_path", type=Path)
    workspace_import_parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Native .mtgwdeck.json output path.",
    )
    workspace_import_parser.add_argument("--cards", type=Path, help="Optional local card catalog JSON.")
    workspace_import_parser.add_argument(
        "--category-taxonomy",
        type=Path,
        help="Optional local category taxonomy YAML.",
    )
    workspace_import_parser.add_argument("--name", default="Imported Deck", help="Workspace deck name.")
    workspace_import_parser.add_argument("--format", default="commander", help="Deck format label.")
    workspace_import_parser.add_argument("--deck-id", default=None, help="Optional stable deck id.")

    workspace_export_parser = subparsers.add_parser(
        "workspace-export",
        help="Export a native workspace file to a plain text decklist.",
    )
    workspace_export_parser.add_argument("workspace_path", type=Path)
    workspace_export_parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Plain text decklist output path.",
    )

    workspace_add_parser = subparsers.add_parser(
        "workspace-add-card",
        help="Add a card entry to a native workspace file.",
    )
    workspace_add_parser.add_argument("workspace_path", type=Path)
    workspace_add_parser.add_argument("card_name")
    workspace_add_parser.add_argument("--output", required=True, type=Path)
    workspace_add_parser.add_argument("--cards", type=Path, help="Optional local card catalog JSON.")
    workspace_add_parser.add_argument("--quantity", type=int, default=1)
    workspace_add_parser.add_argument(
        "--zone",
        choices=("commander", "mainboard", "maybeboard"),
        default="mainboard",
    )
    workspace_add_parser.add_argument("--entry-id", default=None)
    workspace_add_parser.add_argument("--category", action="append", default=[])
    workspace_add_parser.add_argument("--tag", action="append", default=[])
    workspace_add_parser.add_argument("--notes", default=None)
    workspace_add_parser.add_argument(
        "--unresolved",
        action="store_true",
        help="Preserve the card as unresolved instead of resolving display data.",
    )

    workspace_remove_parser = subparsers.add_parser(
        "workspace-remove-entry",
        help="Remove an entry from a native workspace file.",
    )
    workspace_remove_parser.add_argument("workspace_path", type=Path)
    workspace_remove_parser.add_argument("entry_id")
    workspace_remove_parser.add_argument("--output", required=True, type=Path)

    workspace_increase_parser = subparsers.add_parser(
        "workspace-increase-quantity",
        help="Increase an entry quantity in a native workspace file.",
    )
    workspace_increase_parser.add_argument("workspace_path", type=Path)
    workspace_increase_parser.add_argument("entry_id")
    workspace_increase_parser.add_argument("--output", required=True, type=Path)
    workspace_increase_parser.add_argument("--amount", type=int, default=1)

    workspace_decrease_parser = subparsers.add_parser(
        "workspace-decrease-quantity",
        help="Decrease an entry quantity in a native workspace file.",
    )
    workspace_decrease_parser.add_argument("workspace_path", type=Path)
    workspace_decrease_parser.add_argument("entry_id")
    workspace_decrease_parser.add_argument("--output", required=True, type=Path)
    workspace_decrease_parser.add_argument("--amount", type=int, default=1)

    workspace_move_parser = subparsers.add_parser(
        "workspace-move-zone",
        help="Move an entry between commander, mainboard, and maybeboard.",
    )
    workspace_move_parser.add_argument("workspace_path", type=Path)
    workspace_move_parser.add_argument("entry_id")
    workspace_move_parser.add_argument("--output", required=True, type=Path)
    workspace_move_parser.add_argument(
        "--zone",
        required=True,
        choices=("commander", "mainboard", "maybeboard"),
    )

    workspace_commander_parser = subparsers.add_parser(
        "workspace-set-commander",
        help="Move an entry to the commander zone and set quantity to 1.",
    )
    workspace_commander_parser.add_argument("workspace_path", type=Path)
    workspace_commander_parser.add_argument("entry_id")
    workspace_commander_parser.add_argument("--output", required=True, type=Path)

    workspace_imported_category_parser = subparsers.add_parser(
        "workspace-set-imported-category",
        help="Set or clear imported category metadata for a workspace entry.",
    )
    _add_workspace_entry_output_arguments(workspace_imported_category_parser)
    _add_value_or_clear_arguments(workspace_imported_category_parser, "Imported category value.")

    workspace_normalized_category_parser = subparsers.add_parser(
        "workspace-set-normalized-category",
        help="Set or clear normalized category metadata for a workspace entry.",
    )
    _add_workspace_entry_output_arguments(workspace_normalized_category_parser)
    _add_value_or_clear_arguments(workspace_normalized_category_parser, "Normalized category value.")
    workspace_normalized_category_parser.add_argument(
        "--category-taxonomy",
        type=Path,
        help="Optional local category taxonomy YAML for canonical-value validation.",
    )

    workspace_generic_category_parser = subparsers.add_parser(
        "workspace-set-generic-category-hint",
        help="Set or clear generic category hint metadata for a workspace entry.",
    )
    _add_workspace_entry_output_arguments(workspace_generic_category_parser)
    _add_value_or_clear_arguments(workspace_generic_category_parser, "Generic category hint value.")

    workspace_category_origin_parser = subparsers.add_parser(
        "workspace-set-category-origin",
        help="Set or clear category origin metadata for a workspace entry.",
    )
    _add_workspace_entry_output_arguments(workspace_category_origin_parser)
    category_origin_group = workspace_category_origin_parser.add_mutually_exclusive_group(required=True)
    category_origin_group.add_argument("--value", choices=sorted(VALID_CATEGORY_ORIGINS))
    category_origin_group.add_argument("--clear", action="store_true", help="Clear this field.")

    workspace_secondary_add_parser = subparsers.add_parser(
        "workspace-add-secondary-tag",
        help="Add secondary category tag metadata to a workspace entry.",
    )
    _add_workspace_entry_output_arguments(workspace_secondary_add_parser)
    workspace_secondary_add_parser.add_argument("--tag", required=True)

    workspace_secondary_remove_parser = subparsers.add_parser(
        "workspace-remove-secondary-tag",
        help="Remove secondary category tag metadata from a workspace entry.",
    )
    _add_workspace_entry_output_arguments(workspace_secondary_remove_parser)
    workspace_secondary_remove_parser.add_argument("--tag", required=True)

    workspace_secondary_replace_parser = subparsers.add_parser(
        "workspace-replace-secondary-tags",
        help="Replace secondary category tag metadata for a workspace entry.",
    )
    _add_workspace_entry_output_arguments(workspace_secondary_replace_parser)
    workspace_secondary_replace_parser.add_argument("--tag", action="append", default=[])

    workspace_category_clear_parser = subparsers.add_parser(
        "workspace-clear-category-metadata",
        help="Clear category metadata while preserving grouping categories.",
    )
    _add_workspace_entry_output_arguments(workspace_category_clear_parser)

    workspace_notes_parser = subparsers.add_parser(
        "workspace-set-notes",
        help="Set or clear notes for a workspace entry.",
    )
    _add_workspace_entry_output_arguments(workspace_notes_parser)
    _add_value_or_clear_arguments(workspace_notes_parser, "Entry notes value.")

    workspace_tags_replace_parser = subparsers.add_parser(
        "workspace-set-tags",
        help="Replace entry tags for a workspace entry.",
    )
    _add_workspace_entry_output_arguments(workspace_tags_replace_parser)
    workspace_tags_replace_parser.add_argument("--tag", action="append", default=[])

    workspace_tags_add_parser = subparsers.add_parser(
        "workspace-add-tag",
        help="Add one or more tags to a workspace entry.",
    )
    _add_workspace_entry_output_arguments(workspace_tags_add_parser)
    workspace_tags_add_parser.add_argument("--tag", action="append", required=True)

    workspace_tags_remove_parser = subparsers.add_parser(
        "workspace-remove-tag",
        help="Remove one or more tags from a workspace entry.",
    )
    _add_workspace_entry_output_arguments(workspace_tags_remove_parser)
    workspace_tags_remove_parser.add_argument("--tag", action="append", required=True)

    args = parser.parse_args(argv)
    if args.command == "parse":
        return _parse_command(args.decklist_path, args.cards)
    if args.command == "index-scryfall":
        return _index_scryfall_command(args.raw_dir, args.output)
    if args.command == "search":
        return _search_command(args.index, args.query, args.limit)
    if args.command == "inspect-deck":
        return _inspect_deck_command(
            args.workspace_path,
            cards_path=args.cards,
            card_records_path=args.card_records,
            role_rules_path=args.role_rules,
            include_role_evidence=args.include_role_evidence,
            include_debug=args.debug,
            summary_only=args.summary_only,
        )
    if args.command == "workspace-import":
        return _workspace_import_command(
            args.decklist_path,
            output_path=args.output,
            cards_path=args.cards,
            category_taxonomy_path=args.category_taxonomy,
            name=args.name,
            format=args.format,
            deck_id=args.deck_id,
        )
    if args.command == "workspace-export":
        return _workspace_export_command(args.workspace_path, output_path=args.output)
    if args.command == "workspace-add-card":
        return _workspace_add_card_command(
            args.workspace_path,
            args.card_name,
            output_path=args.output,
            cards_path=args.cards,
            quantity=args.quantity,
            zone=args.zone,
            entry_id=args.entry_id,
            categories=args.category,
            tags=args.tag,
            notes=args.notes,
            is_unresolved=args.unresolved,
        )
    if args.command == "workspace-remove-entry":
        return _workspace_remove_entry_command(
            args.workspace_path,
            args.entry_id,
            output_path=args.output,
        )
    if args.command == "workspace-increase-quantity":
        return _workspace_increase_quantity_command(
            args.workspace_path,
            args.entry_id,
            output_path=args.output,
            amount=args.amount,
        )
    if args.command == "workspace-decrease-quantity":
        return _workspace_decrease_quantity_command(
            args.workspace_path,
            args.entry_id,
            output_path=args.output,
            amount=args.amount,
        )
    if args.command == "workspace-move-zone":
        return _workspace_move_zone_command(
            args.workspace_path,
            args.entry_id,
            output_path=args.output,
            zone=args.zone,
        )
    if args.command == "workspace-set-commander":
        return _workspace_set_commander_command(
            args.workspace_path,
            args.entry_id,
            output_path=args.output,
        )
    if args.command == "workspace-set-imported-category":
        return _workspace_set_imported_category_command(
            args.workspace_path,
            args.entry_id,
            value=_value_or_none(args),
            output_path=args.output,
        )
    if args.command == "workspace-set-normalized-category":
        return _workspace_set_normalized_category_command(
            args.workspace_path,
            args.entry_id,
            value=_value_or_none(args),
            output_path=args.output,
            category_taxonomy_path=args.category_taxonomy,
        )
    if args.command == "workspace-set-generic-category-hint":
        return _workspace_set_generic_category_hint_command(
            args.workspace_path,
            args.entry_id,
            value=_value_or_none(args),
            output_path=args.output,
        )
    if args.command == "workspace-set-category-origin":
        return _workspace_set_category_origin_command(
            args.workspace_path,
            args.entry_id,
            value=_value_or_none(args),
            output_path=args.output,
        )
    if args.command == "workspace-add-secondary-tag":
        return _workspace_add_secondary_tag_command(
            args.workspace_path,
            args.entry_id,
            tag=args.tag,
            output_path=args.output,
        )
    if args.command == "workspace-remove-secondary-tag":
        return _workspace_remove_secondary_tag_command(
            args.workspace_path,
            args.entry_id,
            tag=args.tag,
            output_path=args.output,
        )
    if args.command == "workspace-replace-secondary-tags":
        return _workspace_replace_secondary_tags_command(
            args.workspace_path,
            args.entry_id,
            tags=args.tag,
            output_path=args.output,
        )
    if args.command == "workspace-clear-category-metadata":
        return _workspace_clear_category_metadata_command(
            args.workspace_path,
            args.entry_id,
            output_path=args.output,
        )
    if args.command == "workspace-set-notes":
        return _workspace_set_notes_command(
            args.workspace_path,
            args.entry_id,
            notes=_value_or_none(args),
            output_path=args.output,
        )
    if args.command == "workspace-set-tags":
        return _workspace_set_tags_command(
            args.workspace_path,
            args.entry_id,
            tags=args.tag,
            output_path=args.output,
        )
    if args.command == "workspace-add-tag":
        return _workspace_add_tags_command(
            args.workspace_path,
            args.entry_id,
            tags=args.tag,
            output_path=args.output,
        )
    if args.command == "workspace-remove-tag":
        return _workspace_remove_tags_command(
            args.workspace_path,
            args.entry_id,
            tags=args.tag,
            output_path=args.output,
        )
    return 2


def _parse_command(decklist_path: Path, cards_path: Path) -> int:
    catalog = CardCatalog.from_json_file(cards_path)
    raw_deck = parse_decklist(decklist_path)
    parsed = normalize_deck(raw_deck, catalog)
    print(stable_json(parsed.to_dict()))
    return 0


def _index_scryfall_command(raw_dir: Path, output_path: Path) -> int:
    result = build_scryfall_index(raw_dir, output_path)
    print(stable_json(result.to_dict()))
    return 0


def _search_command(index_path: Path, query: str, limit: int) -> int:
    result = search_cards(index_path, query, limit=limit)
    print(stable_json(result))
    return 0


def _inspect_deck_command(
    workspace_path: Path,
    *,
    cards_path: Path | None,
    card_records_path: Path | None,
    role_rules_path: Path | None,
    include_role_evidence: bool,
    include_debug: bool,
    summary_only: bool,
) -> int:
    if include_role_evidence and role_rules_path is None:
        print(
            "error: --role-rules is required when --include-role-evidence is used.",
            file=sys.stderr,
        )
        return 2
    if summary_only and include_debug:
        print("error: --summary-only cannot be combined with --debug.", file=sys.stderr)
        return 2
    if not _require_existing_file(workspace_path, "workspace_path"):
        return 2
    for label, path in (
        ("--cards", cards_path),
        ("--card-records", card_records_path),
        ("--role-rules", role_rules_path),
    ):
        if path is not None and not _require_existing_file(path, label):
            return 2

    workspace = load_workspace(workspace_path)
    card_catalog = CardCatalog.from_json_file(cards_path) if cards_path is not None else None
    card_records = _load_json(card_records_path) if card_records_path is not None else None
    ruleset = load_role_rules(role_rules_path) if role_rules_path is not None else None

    report = build_deck_inspection_report(
        workspace,
        card_records_by_name=card_records,
        card_catalog=card_catalog,
        ruleset=ruleset,
        include_card_role_evidence=include_role_evidence,
        include_debug=include_debug,
    )
    payload = (
        _inspection_summary(report)
        if summary_only
        else report.to_dict(include_debug=include_debug)
    )
    print(stable_json(payload))
    return 0


def _workspace_import_command(
    decklist_path: Path,
    *,
    output_path: Path,
    cards_path: Path | None,
    category_taxonomy_path: Path | None,
    name: str,
    format: str,
    deck_id: str | None,
) -> int:
    if not is_native_workspace_path(output_path):
        print("error: --output must end with .mtgwdeck.json.", file=sys.stderr)
        return 2

    catalog = CardCatalog.from_json_file(cards_path) if cards_path is not None else None
    category_taxonomy = (
        load_category_taxonomy(category_taxonomy_path)
        if category_taxonomy_path is not None
        else None
    )
    workspace = import_plain_text_decklist(
        decklist_path.read_text(encoding="utf-8"),
        catalog=catalog,
        category_taxonomy=category_taxonomy,
        name=name,
        format=format,
        deck_id=deck_id,
        source=str(decklist_path),
    )
    save_workspace(workspace, output_path)
    print(
        stable_json(
            {
                "command": "workspace-import",
                "deck": _workspace_summary(workspace),
                "input_path": str(decklist_path),
                "output_path": str(output_path),
            }
        )
    )
    return 0


def _workspace_export_command(workspace_path: Path, *, output_path: Path) -> int:
    if not _require_native_workspace_path(workspace_path, "workspace_path"):
        return 2

    workspace = load_workspace(workspace_path)
    exported = export_plain_text_decklist(workspace)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(exported, encoding="utf-8")
    print(
        stable_json(
            {
                "command": "workspace-export",
                "deck": _workspace_summary(workspace),
                "input_path": str(workspace_path),
                "line_count": len(exported.splitlines()),
                "output_path": str(output_path),
            }
        )
    )
    return 0


def _workspace_add_card_command(
    workspace_path: Path,
    card_name: str,
    *,
    output_path: Path,
    cards_path: Path | None,
    quantity: int,
    zone: str,
    entry_id: str | None,
    categories: list[str],
    tags: list[str],
    notes: str | None,
    is_unresolved: bool,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    before_ids = _entry_id_set(workspace)
    display_name = None
    resolved_oracle_id = None

    if not is_unresolved:
        if cards_path is not None:
            card = CardCatalog.from_json_file(cards_path).find(card_name)
            if card is None:
                is_unresolved = True
            else:
                display_name = card.name
                resolved_oracle_id = card.oracle_id
        else:
            display_name = card_name

    add_entry(
        workspace,
        card_name,
        display_name=display_name,
        quantity=quantity,
        zone=zone,
        entry_id=entry_id,
        oracle_id=resolved_oracle_id,
        categories=categories,
        tags=tags,
        notes=notes,
        is_unresolved=is_unresolved,
    )
    after_ids = _entry_id_set(workspace)
    changed_entry_id = entry_id or next(iter(sorted(after_ids - before_ids)), None)
    if changed_entry_id is None:
        changed_entry_id = _find_likely_added_entry_id(workspace, card_name, zone)

    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-add-card",
        changed_entry_id=changed_entry_id,
    )


def _workspace_remove_entry_command(
    workspace_path: Path,
    entry_id: str,
    *,
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    remove_entry(workspace, entry_id)
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-remove-entry",
        changed_entry_id=entry_id,
    )


def _workspace_increase_quantity_command(
    workspace_path: Path,
    entry_id: str,
    *,
    output_path: Path,
    amount: int,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    increase_quantity(workspace, entry_id, increment=amount)
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-increase-quantity",
        changed_entry_id=entry_id,
    )


def _workspace_decrease_quantity_command(
    workspace_path: Path,
    entry_id: str,
    *,
    output_path: Path,
    amount: int,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    decrease_quantity(workspace, entry_id, decrement=amount)
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-decrease-quantity",
        changed_entry_id=entry_id,
    )


def _workspace_move_zone_command(
    workspace_path: Path,
    entry_id: str,
    *,
    output_path: Path,
    zone: str,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    move_zone(workspace, entry_id, zone)
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-move-zone",
        changed_entry_id=entry_id,
    )


def _workspace_set_commander_command(
    workspace_path: Path,
    entry_id: str,
    *,
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    set_commander(workspace, entry_id)
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-set-commander",
        changed_entry_id=entry_id,
    )


def _workspace_set_imported_category_command(
    workspace_path: Path,
    entry_id: str,
    *,
    value: str | None,
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    try:
        set_imported_category(workspace, entry_id, value)
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-set-imported-category",
        changed_entry_id=entry_id,
    )


def _workspace_set_normalized_category_command(
    workspace_path: Path,
    entry_id: str,
    *,
    value: str | None,
    output_path: Path,
    category_taxonomy_path: Path | None,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2
    if category_taxonomy_path is not None and not _require_existing_file(
        category_taxonomy_path,
        "--category-taxonomy",
    ):
        return 2

    workspace = load_workspace(workspace_path)
    category_taxonomy = (
        load_category_taxonomy(category_taxonomy_path)
        if category_taxonomy_path is not None
        else None
    )
    try:
        set_normalized_category(
            workspace,
            entry_id,
            value,
            category_taxonomy=category_taxonomy,
        )
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-set-normalized-category",
        changed_entry_id=entry_id,
    )


def _workspace_set_generic_category_hint_command(
    workspace_path: Path,
    entry_id: str,
    *,
    value: str | None,
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    try:
        set_generic_category_hint(workspace, entry_id, value)
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-set-generic-category-hint",
        changed_entry_id=entry_id,
    )


def _workspace_set_category_origin_command(
    workspace_path: Path,
    entry_id: str,
    *,
    value: str | None,
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    try:
        set_category_origin(workspace, entry_id, value)
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-set-category-origin",
        changed_entry_id=entry_id,
    )


def _workspace_add_secondary_tag_command(
    workspace_path: Path,
    entry_id: str,
    *,
    tag: str,
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    try:
        add_secondary_tag(workspace, entry_id, tag)
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-add-secondary-tag",
        changed_entry_id=entry_id,
    )


def _workspace_remove_secondary_tag_command(
    workspace_path: Path,
    entry_id: str,
    *,
    tag: str,
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    try:
        remove_secondary_tag(workspace, entry_id, tag)
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-remove-secondary-tag",
        changed_entry_id=entry_id,
    )


def _workspace_replace_secondary_tags_command(
    workspace_path: Path,
    entry_id: str,
    *,
    tags: list[str],
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    try:
        replace_secondary_tags(workspace, entry_id, tags)
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-replace-secondary-tags",
        changed_entry_id=entry_id,
    )


def _workspace_clear_category_metadata_command(
    workspace_path: Path,
    entry_id: str,
    *,
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    try:
        clear_category_metadata(workspace, entry_id)
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-clear-category-metadata",
        changed_entry_id=entry_id,
    )


def _workspace_set_notes_command(
    workspace_path: Path,
    entry_id: str,
    *,
    notes: str | None,
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    try:
        update_notes(workspace, entry_id, notes)
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-set-notes",
        changed_entry_id=entry_id,
    )


def _workspace_set_tags_command(
    workspace_path: Path,
    entry_id: str,
    *,
    tags: list[str],
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    try:
        update_tags(workspace, entry_id, tags=tags)
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-set-tags",
        changed_entry_id=entry_id,
    )


def _workspace_add_tags_command(
    workspace_path: Path,
    entry_id: str,
    *,
    tags: list[str],
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    try:
        update_tags(workspace, entry_id, add=tags)
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-add-tag",
        changed_entry_id=entry_id,
    )


def _workspace_remove_tags_command(
    workspace_path: Path,
    entry_id: str,
    *,
    tags: list[str],
    output_path: Path,
) -> int:
    if not _require_workspace_io_paths(workspace_path, output_path):
        return 2

    workspace = load_workspace(workspace_path)
    try:
        update_tags(workspace, entry_id, remove=tags)
    except WorkspaceMutationError as error:
        return _print_error(str(error))
    return _save_mutated_workspace(
        workspace,
        output_path=output_path,
        command="workspace-remove-tag",
        changed_entry_id=entry_id,
    )


def _save_mutated_workspace(
    workspace,
    *,
    output_path: Path,
    command: str,
    changed_entry_id: str | None,
) -> int:
    save_workspace(workspace, output_path)
    payload: dict[str, Any] = {
        "command": command,
        "deck": _workspace_summary(workspace),
        "output_path": str(output_path),
    }
    if changed_entry_id is not None:
        payload["entry"] = _entry_summary(workspace, changed_entry_id)
    print(stable_json(payload))
    return 0


def _workspace_summary(workspace) -> dict[str, Any]:
    sections = {
        "commander": workspace.commanders,
        "mainboard": workspace.mainboard,
        "maybeboard": workspace.maybeboard,
    }
    quantity_totals = {
        zone: sum(entry.quantity for entry in entries)
        for zone, entries in sections.items()
    }
    return {
        "active_quantity_total": quantity_totals["commander"] + quantity_totals["mainboard"],
        "deck_id": workspace.deck_id,
        "format": workspace.format,
        "is_dirty": bool(workspace.saved_state.get("is_dirty")),
        "name": workspace.name,
        "quantity_totals": quantity_totals,
        "zone_entry_counts": {
            zone: len(entries)
            for zone, entries in sections.items()
        },
    }


def _entry_summary(workspace, entry_id: str) -> dict[str, Any]:
    entry = find_entry(workspace, entry_id)
    if entry is None:
        return {"entry_id": entry_id, "status": "removed"}
    return {
        "categories": list(entry.categories),
        "category_origin": entry.category_origin,
        "deck_specific_primary_role": entry.deck_specific_primary_role,
        "display_name": entry.display_name,
        "entry_id": entry.entry_id,
        "generic_category_hint": entry.generic_category_hint,
        "imported_category": entry.imported_category,
        "input_name": entry.input_name,
        "is_unresolved": entry.is_unresolved,
        "normalized_category": entry.normalized_category,
        "notes": entry.notes,
        "quantity": entry.quantity,
        "secondary_tags": list(entry.secondary_tags),
        "tags": list(entry.tags),
        "zone": entry.zone,
    }


def _entry_id_set(workspace) -> set[str]:
    return {
        entry.entry_id
        for entry in [*workspace.commanders, *workspace.mainboard, *workspace.maybeboard]
    }


def _find_likely_added_entry_id(workspace, card_name: str, zone: str) -> str | None:
    normalized_name = " ".join(card_name.casefold().split())
    entries = {
        "commander": workspace.commanders,
        "mainboard": workspace.mainboard,
        "maybeboard": workspace.maybeboard,
    }[zone]
    for entry in entries:
        if " ".join(entry.input_name.casefold().split()) == normalized_name:
            return entry.entry_id
    return None


def _inspection_summary(report) -> dict[str, Any]:
    coverage = report.card_fact_coverage
    return {
        "active_quantity_total": report.skeleton_report.active_quantity_total,
        "card_fact_coverage": coverage.to_dict(),
        "card_role_report_count": report.card_role_report_count,
        "deck_id": report.deck_id,
        "deck_name": report.deck_name,
        "format": report.format,
        "schema_version": report.schema_version,
        "structural_warning_count": report.warning_count,
        "user_summary": report.user_summary,
    }


def _require_existing_file(path: Path, label: str) -> bool:
    if path.is_file():
        return True
    print(f"error: {label} does not exist or is not a file: {path}", file=sys.stderr)
    return False


def _require_workspace_io_paths(workspace_path: Path, output_path: Path) -> bool:
    return (
        _require_native_workspace_path(workspace_path, "workspace_path")
        and _require_native_workspace_path(output_path, "--output")
    )


def _require_native_workspace_path(path: Path, label: str) -> bool:
    if is_native_workspace_path(path):
        return True
    print(f"error: {label} must end with .mtgwdeck.json.", file=sys.stderr)
    return False


def _add_workspace_entry_output_arguments(command_parser: argparse.ArgumentParser) -> None:
    command_parser.add_argument("workspace_path", type=Path)
    command_parser.add_argument("entry_id")
    command_parser.add_argument("--output", required=True, type=Path)


def _add_value_or_clear_arguments(command_parser: argparse.ArgumentParser, value_help: str) -> None:
    group = command_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--value", default=None, help=value_help)
    group.add_argument("--clear", action="store_true", help="Clear this field.")


def _value_or_none(args) -> str | None:
    if getattr(args, "clear", False):
        return None
    return args.value


def _print_error(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 2


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

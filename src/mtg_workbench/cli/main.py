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
) -> int:
    if include_role_evidence and role_rules_path is None:
        print(
            "error: --role-rules is required when --include-role-evidence is used.",
            file=sys.stderr,
        )
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
    print(stable_json(report.to_dict(include_debug=include_debug)))
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
    if not is_native_workspace_path(workspace_path):
        print("error: workspace_path must end with .mtgwdeck.json.", file=sys.stderr)
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


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

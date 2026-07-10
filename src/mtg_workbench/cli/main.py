from __future__ import annotations

import argparse
from pathlib import Path
import sys

from mtg_workbench.cards.catalog import CardCatalog
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

    args = parser.parse_args(argv)
    if args.command == "parse":
        return _parse_command(args.decklist_path, args.cards)
    if args.command == "index-scryfall":
        return _index_scryfall_command(args.raw_dir, args.output)
    if args.command == "search":
        return _search_command(args.index, args.query, args.limit)
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


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest

from mtg_workbench.cli.main import main
from mtg_workbench.scryfall.indexer import build_scryfall_index
from mtg_workbench.scryfall.search import parse_query, search_cards


class ScryfallSearchTests(unittest.TestCase):
    def test_bare_name_search_prefers_names(self) -> None:
        with _search_index() as index_path:
            payload = search_cards(index_path, "Lightning", limit=10)

        self.assertEqual(payload["result_count"], 1)
        self.assertEqual(payload["results"][0]["name"], "Lightning Bolt")
        self.assertEqual(payload["unsupported_clauses"], [])

    def test_oracle_text_search(self) -> None:
        with _search_index() as index_path:
            payload = search_cards(index_path, "o:draw", limit=10)

        self.assertIn("Divination", _result_names(payload))
        self.assertEqual(payload["unsupported_clauses"], [])

    def test_type_line_search(self) -> None:
        with _search_index() as index_path:
            payload = search_cards(index_path, "t:creature", limit=10)

        self.assertIn("Llanowar Elves", _result_names(payload))
        self.assertEqual(payload["unsupported_clauses"], [])

    def test_oracle_tag_resolves_before_color_and_mana_filters(self) -> None:
        with _search_index() as index_path:
            payload = search_cards(index_path, "otag:burn ci:r mv<=1", limit=10)

        self.assertEqual(payload["result_count"], 1)
        result = payload["results"][0]
        self.assertEqual(result["name"], "Lightning Bolt")
        self.assertEqual(result["matched_terms"], ["ci:r", "mv<=1", "otag:burn"])
        self.assertEqual(result["tag_matches"][0]["slug"], "burn")
        self.assertEqual(result["color_identity"], ["R"])

    def test_multiple_supported_syntax_clauses_intersect(self) -> None:
        with _search_index() as index_path:
            payload = search_cards(index_path, "mv<=2 id:g t:instant o:draw", limit=10)

        self.assertEqual(payload["result_count"], 1)
        result = payload["results"][0]
        self.assertEqual(result["name"], "Green Draw Trick")
        self.assertEqual(result["matched_terms"], ["id:g", "mv<=2", "o:draw", "t:instant"])
        self.assertEqual(payload["unsupported_clauses"], [])

    def test_unsupported_syntax_is_reported_not_guessed(self) -> None:
        clauses, unsupported = parse_query("pow>=3 otag:burn")

        self.assertEqual([clause.kind for clause in clauses], ["oracle_tag"])
        self.assertEqual(unsupported[0].raw, "pow>=3")
        self.assertEqual(unsupported[0].reason, "unsupported_syntax")

    def test_cli_search_outputs_stable_json(self) -> None:
        with _search_index() as index_path:
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["search", "otag:burn ci:r mv<=1", "--index", str(index_path)])

        self.assertEqual(exit_code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["object"], "mtg_workbench_scryfall_search_result")
        self.assertEqual(payload["results"][0]["name"], "Lightning Bolt")
        self.assertEqual(list(payload.keys()), sorted(payload.keys()))


class ScryfallFutureFilterTests(unittest.TestCase):
    @unittest.expectedFailure
    def test_legal_filter_contract(self) -> None:
        with _search_index() as index_path:
            payload = search_cards(index_path, "legal:commander", limit=10)

        names = _result_names(payload)
        self.assertIn("Lightning Bolt", names)
        self.assertNotIn("Forbidden Tutor", names)
        self.assertEqual(payload["unsupported_clauses"], [])

    @unittest.expectedFailure
    def test_usd_price_filter_contract(self) -> None:
        with _search_index() as index_path:
            payload = search_cards(index_path, "usd<=1", limit=10)

        names = _result_names(payload)
        self.assertIn("Lightning Bolt", names)
        self.assertNotIn("Expensive Dragon", names)
        self.assertEqual(payload["unsupported_clauses"], [])

    @unittest.expectedFailure
    def test_rarity_filter_contract(self) -> None:
        with _search_index() as index_path:
            payload = search_cards(index_path, "r:mythic", limit=10)

        self.assertEqual(_result_names(payload), ["Expensive Dragon"])
        self.assertEqual(payload["unsupported_clauses"], [])

    @unittest.expectedFailure
    def test_set_filter_contract(self) -> None:
        with _search_index() as index_path:
            payload = search_cards(index_path, "set:m21", limit=10)

        self.assertEqual(_result_names(payload), ["Divination"])
        self.assertEqual(payload["unsupported_clauses"], [])

    @unittest.expectedFailure
    def test_commander_candidate_filter_contract(self) -> None:
        with _search_index() as index_path:
            payload = search_cards(index_path, "is:commander", limit=10)

        self.assertEqual(_result_names(payload), ["Example Commander"])
        self.assertEqual(payload["unsupported_clauses"], [])


class _search_index:
    def __enter__(self) -> Path:
        self._temp_dir = tempfile.TemporaryDirectory()
        root = Path(self._temp_dir.name)
        raw_dir = root / "raw" / "scryfall"
        index_path = root / "processed" / "scryfall" / "cards.sqlite"
        _write_snapshot(raw_dir)
        build_scryfall_index(raw_dir, index_path)
        return index_path

    def __exit__(self, exc_type, exc, tb) -> None:
        self._temp_dir.cleanup()


def _write_snapshot(raw_dir: Path) -> None:
    rows_by_type = {
        "oracle_cards": [
            _card(
                scryfall_id="card-bolt",
                oracle_id="oracle-bolt",
                name="Lightning Bolt",
                cmc=1,
                colors=["R"],
                color_identity=["R"],
                type_line="Instant",
                oracle_text="Lightning Bolt deals 3 damage to any target.",
                rarity="common",
                set_code="lea",
                usd="0.25",
            ),
            _card(
                scryfall_id="card-divination",
                oracle_id="oracle-divination",
                name="Divination",
                cmc=3,
                colors=["U"],
                color_identity=["U"],
                type_line="Sorcery",
                oracle_text="Draw two cards.",
                rarity="common",
                set_code="m21",
                usd="0.10",
            ),
            _card(
                scryfall_id="card-elves",
                oracle_id="oracle-elves",
                name="Llanowar Elves",
                cmc=1,
                colors=["G"],
                color_identity=["G"],
                type_line="Creature - Elf Druid",
                oracle_text="{T}: Add {G}.",
                rarity="common",
                set_code="lea",
                usd="0.20",
            ),
            _card(
                scryfall_id="card-green-draw-trick",
                oracle_id="oracle-green-draw-trick",
                name="Green Draw Trick",
                cmc=2,
                colors=["G"],
                color_identity=["G"],
                type_line="Instant",
                oracle_text="Draw a card.",
                rarity="uncommon",
                set_code="grn",
                usd="0.15",
            ),
            _card(
                scryfall_id="card-forbidden-tutor",
                oracle_id="oracle-forbidden-tutor",
                name="Forbidden Tutor",
                cmc=1,
                colors=["B"],
                color_identity=["B"],
                type_line="Sorcery",
                oracle_text="Search your library for a card.",
                legalities={"commander": "banned"},
                rarity="rare",
                set_code="abc",
                usd="0.50",
            ),
            _card(
                scryfall_id="card-expensive-dragon",
                oracle_id="oracle-expensive-dragon",
                name="Expensive Dragon",
                cmc=5,
                colors=["R"],
                color_identity=["R"],
                type_line="Creature - Dragon",
                oracle_text="Flying, haste.",
                rarity="mythic",
                set_code="drg",
                usd="25.00",
            ),
            _card(
                scryfall_id="card-example-commander",
                oracle_id="oracle-example-commander",
                name="Example Commander",
                cmc=3,
                colors=["G"],
                color_identity=["G"],
                type_line="Legendary Creature - Elf Advisor",
                oracle_text="Whenever you cast a creature spell, draw a card.",
                rarity="rare",
                set_code="cmd",
                usd="0.75",
            ),
        ],
        "oracle_tags": [
            {
                "id": "tag-burn",
                "slug": "burn",
                "label": "Burn",
                "description": "Direct damage effects.",
                "aliases": ["direct-damage"],
                "parent_ids": [],
                "child_ids": [],
                "type": "oracle",
                "taggings": [{"oracle_id": "oracle-bolt", "weight": 0.95}],
            },
            {
                "id": "tag-card-draw",
                "slug": "card-draw",
                "label": "Card Draw",
                "description": "Cards that draw cards.",
                "aliases": ["draw"],
                "parent_ids": [],
                "child_ids": [],
                "type": "oracle",
                "taggings": [{"oracle_id": "oracle-divination", "weight": 0.9}],
            },
        ],
    }

    entries = []
    for source_type, rows in rows_by_type.items():
        source_dir = raw_dir / source_type
        source_dir.mkdir(parents=True, exist_ok=True)
        file_path = source_dir / f"{source_type}.jsonl"
        with file_path.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, sort_keys=True))
                handle.write("\n")
        entries.append(
            {
                "bytes_downloaded": file_path.stat().st_size,
                "local_path": str(file_path),
                "name": source_type.replace("_", " ").title(),
                "sha256": "fixture",
                "source_reported_json_size": file_path.stat().st_size,
                "type": source_type,
                "updated_at": "2026-07-09T00:00:00Z",
            }
        )

    raw_dir.mkdir(parents=True, exist_ok=True)
    with (raw_dir / "manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "entries": entries,
                "fetched_at": "2026-07-09T00:00:00Z",
                "object": "mtg_workbench_scryfall_bulk_manifest",
                "source_api": "fixture",
            },
            handle,
            indent=2,
            sort_keys=True,
        )


def _card(
    *,
    scryfall_id: str,
    oracle_id: str,
    name: str,
    cmc: int,
    colors: list[str],
    color_identity: list[str],
    type_line: str,
    oracle_text: str,
    legalities: dict[str, str] | None = None,
    rarity: str = "common",
    set_code: str = "lea",
    usd: str = "0.25",
) -> dict[str, object]:
    return {
        "id": scryfall_id,
        "oracle_id": oracle_id,
        "name": name,
        "mana_cost": "",
        "cmc": cmc,
        "colors": colors,
        "color_identity": color_identity,
        "type_line": type_line,
        "oracle_text": oracle_text,
        "keywords": [],
        "legalities": legalities or {"commander": "legal"},
        "prices": {"usd": usd},
        "edhrec_rank": 100,
        "released_at": "1993-08-05",
        "set": set_code,
        "collector_number": "1",
        "rarity": rarity,
        "layout": "normal",
    }


def _result_names(payload: dict[str, object]) -> list[str]:
    results = payload["results"]
    assert isinstance(results, list)
    return [str(result["name"]) for result in results]


if __name__ == "__main__":
    unittest.main()

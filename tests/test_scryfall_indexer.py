import io
import json
from pathlib import Path
import sqlite3
import tempfile
from contextlib import redirect_stdout
import unittest
from unittest.mock import patch

from mtg_workbench.cards.catalog import normalize_lookup_key
from mtg_workbench.cli.main import main
from mtg_workbench.scryfall import indexer as scryfall_indexer
from mtg_workbench.scryfall.indexer import build_scryfall_index


class ScryfallIndexerTests(unittest.TestCase):
    def test_builds_sqlite_index_from_local_snapshot_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_dir = Path(temp_dir) / "raw" / "scryfall"
            output_path = Path(temp_dir) / "processed" / "scryfall" / "cards.sqlite"
            _write_snapshot(raw_dir)

            result = build_scryfall_index(raw_dir, output_path)

            self.assertTrue(output_path.exists())
            self.assertTrue(Path(result.manifest_path).exists())
            self.assertEqual(result.counts["oracle_cards"], 1)
            self.assertEqual(result.counts["prints"], 2)
            self.assertEqual(result.counts["oracle_taggings"], 1)
            self.assertEqual(result.counts["art_taggings"], 1)

            db = sqlite3.connect(output_path)
            try:
                self.assertEqual(db.execute("SELECT count(*) FROM bulk_sources").fetchone()[0], 7)
                self.assertEqual(db.execute("SELECT count(*) FROM oracle_cards_fts").fetchone()[0], 1)

                name_row = db.execute(
                    "SELECT display_name, oracle_id FROM names WHERE name_key = ?",
                    (normalize_lookup_key(" lightning   bolt "),),
                ).fetchone()
                self.assertEqual(name_row, ("Lightning Bolt", "oracle-bolt"))

                tagged_card = db.execute(
                    """
                    SELECT oc.name
                    FROM oracle_taggings ot
                    JOIN oracle_cards oc ON oc.oracle_id = ot.oracle_id
                    WHERE ot.slug = 'burn'
                    """
                ).fetchone()
                self.assertEqual(tagged_card[0], "Lightning Bolt")
            finally:
                db.close()

    def test_cli_index_scryfall_outputs_stable_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_dir = Path(temp_dir) / "raw" / "scryfall"
            output_path = Path(temp_dir) / "processed" / "scryfall" / "cards.sqlite"
            _write_snapshot(raw_dir)

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "index-scryfall",
                        "--raw-dir",
                        str(raw_dir),
                        "--output",
                        str(output_path),
                    ]
                )

            self.assertEqual(exit_code, 0)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["counts"]["oracle_cards"], 1)
            self.assertEqual(payload["counts"]["oracle_taggings"], 1)
            self.assertEqual(payload["object"], "mtg_workbench_scryfall_index_result")
            self.assertEqual(list(payload.keys()), sorted(payload.keys()))


    def test_failed_rebuild_preserves_existing_index(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_dir = Path(temp_dir) / "raw" / "scryfall"
            output_path = Path(temp_dir) / "processed" / "scryfall" / "cards.sqlite"
            _write_snapshot(raw_dir)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(b"known-good-index")

            manifest_path = raw_dir / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["entries"][0]["local_path"] = str(
                raw_dir / "oracle_cards" / "missing.jsonl"
            )
            manifest_path.write_text(
                json.dumps(manifest, indent=2, sort_keys=True),
                encoding="utf-8",
            )

            with self.assertRaises(FileNotFoundError):
                build_scryfall_index(raw_dir, output_path)

            self.assertEqual(
                output_path.read_bytes(),
                b"known-good-index",
            )
            self.assertFalse(
                output_path.with_name(f"{output_path.name}.tmp").exists()
            )

    def test_stale_absolute_manifest_paths_fall_back_to_raw_root_files(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_dir = Path(temp_dir) / "raw" / "scryfall"
            output_path = Path(temp_dir) / "processed" / "scryfall" / "cards.sqlite"
            _write_snapshot(raw_dir)

            manifest_path = raw_dir / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            stale_root = Path("C:/old/mtg-workbench/data/raw/scryfall")
            for entry in manifest["entries"]:
                original_path = Path(entry["local_path"])
                entry["local_path"] = str(
                    stale_root
                    / entry["type"]
                    / original_path.name
                )
            manifest_path.write_text(
                json.dumps(manifest, indent=2, sort_keys=True),
                encoding="utf-8",
            )

            result = build_scryfall_index(raw_dir, output_path)

            self.assertTrue(output_path.exists())
            self.assertEqual(result.counts["oracle_cards"], 1)
            self.assertEqual(result.counts["prints"], 2)

    def test_manifest_replace_failure_preserves_existing_index_and_manifest(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_dir = Path(temp_dir) / "raw" / "scryfall"
            output_path = Path(temp_dir) / "processed" / "scryfall" / "cards.sqlite"
            index_manifest_path = output_path.parent / "index_manifest.json"
            _write_snapshot(raw_dir)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(b"known-good-index")
            index_manifest_path.write_text(
                json.dumps(
                    {
                        "object": "known-good-index-manifest",
                        "schema_version": 999,
                    },
                    indent=2,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            original_manifest = index_manifest_path.read_text(
                encoding="utf-8"
            )

            original_replace = scryfall_indexer._replace_path

            def fail_manifest_replace(
                source_path: Path,
                target_path: Path,
            ) -> None:
                if (
                    source_path.name == "index_manifest.json.tmp"
                    and target_path.name == "index_manifest.json"
                ):
                    raise OSError("manifest replace failed")
                original_replace(source_path, target_path)

            with patch(
                "mtg_workbench.scryfall.indexer._replace_path",
                side_effect=fail_manifest_replace,
            ):
                with self.assertRaisesRegex(
                    OSError,
                    "manifest replace failed",
                ):
                    build_scryfall_index(raw_dir, output_path)

            self.assertEqual(output_path.read_bytes(), b"known-good-index")
            self.assertEqual(
                index_manifest_path.read_text(encoding="utf-8"),
                original_manifest,
            )
            self.assertFalse(
                output_path.with_name(f"{output_path.name}.tmp").exists()
            )
            self.assertFalse(
                output_path.with_name(f"{output_path.name}.bak").exists()
            )
            self.assertFalse(
                index_manifest_path.with_name(
                    f"{index_manifest_path.name}.tmp"
                ).exists()
            )
            self.assertFalse(
                index_manifest_path.with_name(
                    f"{index_manifest_path.name}.bak"
                ).exists()
            )


def _write_snapshot(raw_dir: Path) -> None:
    rows_by_type = {
        "oracle_cards": [
            {
                "id": "card-bolt",
                "oracle_id": "oracle-bolt",
                "name": "Lightning Bolt",
                "mana_cost": "{R}",
                "cmc": 1,
                "colors": ["R"],
                "color_identity": ["R"],
                "type_line": "Instant",
                "oracle_text": "Lightning Bolt deals 3 damage to any target.",
                "keywords": [],
                "legalities": {"commander": "legal"},
                "prices": {"usd": "0.25"},
                "edhrec_rank": 100,
                "released_at": "1993-08-05",
                "set": "lea",
                "collector_number": "161",
                "rarity": "common",
                "layout": "normal",
            }
        ],
        "default_cards": [
            {
                "id": "print-bolt-default",
                "oracle_id": "oracle-bolt",
                "name": "Lightning Bolt",
                "lang": "en",
                "set": "clu",
                "set_name": "Ravnica: Clue Edition",
                "collector_number": "141",
                "rarity": "common",
                "released_at": "2024-02-23",
                "layout": "normal",
                "cmc": 1,
                "type_line": "Instant",
                "oracle_text": "Lightning Bolt deals 3 damage to any target.",
                "colors": ["R"],
                "color_identity": ["R"],
                "artist": "Christopher Rush",
                "illustration_id": "art-bolt",
                "image_status": "highres_scan",
                "legalities": {"commander": "legal"},
                "prices": {"usd": "0.25"},
            }
        ],
        "all_cards": [
            {
                "id": "print-bolt-all",
                "oracle_id": "oracle-bolt",
                "name": "Lightning Bolt",
                "lang": "en",
                "set": "lea",
                "set_name": "Limited Edition Alpha",
                "collector_number": "161",
                "rarity": "common",
                "released_at": "1993-08-05",
                "layout": "normal",
                "cmc": 1,
                "type_line": "Instant",
                "oracle_text": "Lightning Bolt deals 3 damage to any target.",
                "colors": ["R"],
                "color_identity": ["R"],
                "artist": "Christopher Rush",
                "illustration_id": "art-bolt",
                "image_status": "highres_scan",
                "legalities": {"commander": "legal"},
                "prices": {"usd": "10.00"},
            }
        ],
        "unique_artwork": [
            {
                "id": "art-print-bolt",
                "oracle_id": "oracle-bolt",
                "name": "Lightning Bolt",
                "illustration_id": "art-bolt",
                "artist": "Christopher Rush",
                "set": "lea",
                "collector_number": "161",
                "image_status": "highres_scan",
            }
        ],
        "rulings": [
            {
                "oracle_id": "oracle-bolt",
                "source": "wotc",
                "published_at": "2009-10-01",
                "comment": "Any target includes creatures, players, and planeswalkers.",
            }
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
            }
        ],
        "art_tags": [
            {
                "id": "tag-fire",
                "slug": "fire",
                "label": "Fire",
                "description": "Fire in the art.",
                "aliases": [],
                "parent_ids": [],
                "child_ids": [],
                "type": "art",
                "taggings": [{"illustration_id": "art-bolt", "weight": 0.7}],
            }
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

    manifest = {
        "entries": entries,
        "fetched_at": "2026-07-09T00:00:00Z",
        "object": "mtg_workbench_scryfall_bulk_manifest",
        "source_api": "fixture",
    }
    raw_dir.mkdir(parents=True, exist_ok=True)
    with (raw_dir / "manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)


if __name__ == "__main__":
    unittest.main()

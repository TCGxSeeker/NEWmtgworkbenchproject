from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
import gzip
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterable, Iterator

from mtg_workbench.cards.catalog import normalize_lookup_key


SOURCE_TYPES = (
    "oracle_cards",
    "default_cards",
    "all_cards",
    "unique_artwork",
    "rulings",
    "oracle_tags",
    "art_tags",
)

COLOR_BITS = {"W": 1, "U": 2, "B": 4, "R": 8, "G": 16}
BATCH_SIZE = 5000


@dataclass(frozen=True)
class IndexBuildResult:
    output_path: str
    manifest_path: str
    source_manifest_path: str
    fts_available: bool
    counts: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "counts": self.counts,
            "fts_available": self.fts_available,
            "manifest_path": self.manifest_path,
            "object": "mtg_workbench_scryfall_index_result",
            "output_path": self.output_path,
            "source_manifest_path": self.source_manifest_path,
        }


def build_scryfall_index(raw_dir: str | Path, output_path: str | Path) -> IndexBuildResult:
    """Build an offline SQLite index from local Scryfall bulk snapshot files."""
    raw_root = Path(raw_dir)
    output = Path(output_path)
    manifest_path = raw_root / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Scryfall manifest not found: {manifest_path}")

    manifest = _read_json(manifest_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    temp_output = output.with_name(f"{output.name}.tmp")
    _remove_sqlite_file(temp_output)
    _remove_sqlite_file(output)

    counts = _empty_counts()
    tag_text_by_oracle_id: dict[str, set[str]] = defaultdict(set)
    fts_available = True

    conn = sqlite3.connect(temp_output)
    try:
        conn.execute("PRAGMA journal_mode=OFF")
        conn.execute("PRAGMA synchronous=OFF")
        conn.execute("PRAGMA temp_store=MEMORY")
        conn.execute("PRAGMA cache_size=-200000")
        fts_available = _create_schema(conn)

        conn.execute("BEGIN")
        _insert_bulk_sources(conn, manifest, counts)
        _index_oracle_cards(conn, raw_root, manifest, counts)
        _index_print_cards(conn, raw_root, manifest, "default_cards", counts)
        _index_print_cards(conn, raw_root, manifest, "all_cards", counts)
        _index_unique_artwork(conn, raw_root, manifest, counts)
        _index_rulings(conn, raw_root, manifest, counts)
        _index_oracle_tags(conn, raw_root, manifest, counts, tag_text_by_oracle_id)
        _index_art_tags(conn, raw_root, manifest, counts)
        _index_oracle_card_fts(conn, counts, tag_text_by_oracle_id)
        conn.commit()

        conn.execute("BEGIN")
        _create_indexes(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    temp_output.replace(output)
    index_manifest_path = output.parent / "index_manifest.json"
    _write_index_manifest(
        index_manifest_path,
        output,
        manifest_path,
        manifest,
        counts,
        fts_available,
    )

    return IndexBuildResult(
        output_path=str(output),
        manifest_path=str(index_manifest_path),
        source_manifest_path=str(manifest_path),
        fts_available=fts_available,
        counts=counts,
    )


def _create_schema(conn: sqlite3.Connection) -> bool:
    conn.executescript(
        """
        CREATE TABLE bulk_sources (
            source_type TEXT PRIMARY KEY,
            name TEXT,
            updated_at TEXT,
            local_path TEXT,
            bytes_downloaded INTEGER,
            sha256 TEXT,
            source_reported_json_size INTEGER
        );

        CREATE TABLE oracle_cards (
            oracle_id TEXT PRIMARY KEY,
            scryfall_id TEXT,
            name TEXT NOT NULL,
            normalized_name TEXT NOT NULL,
            mana_cost TEXT,
            mana_value REAL,
            colors TEXT,
            color_identity TEXT,
            colors_mask INTEGER,
            color_identity_mask INTEGER,
            type_line TEXT,
            oracle_text TEXT,
            keywords TEXT,
            legalities TEXT,
            prices TEXT,
            edhrec_rank INTEGER,
            released_at TEXT,
            set_code TEXT,
            collector_number TEXT,
            rarity TEXT,
            layout TEXT,
            is_basic_land INTEGER,
            is_legendary INTEGER,
            is_commander_candidate INTEGER
        );

        CREATE TABLE prints (
            source_type TEXT NOT NULL,
            scryfall_id TEXT NOT NULL,
            oracle_id TEXT,
            name TEXT NOT NULL,
            normalized_name TEXT,
            lang TEXT,
            set_code TEXT,
            set_name TEXT,
            collector_number TEXT,
            rarity TEXT,
            released_at TEXT,
            layout TEXT,
            mana_value REAL,
            type_line TEXT,
            oracle_text TEXT,
            colors TEXT,
            color_identity TEXT,
            colors_mask INTEGER,
            color_identity_mask INTEGER,
            artist TEXT,
            illustration_id TEXT,
            image_status TEXT,
            legalities TEXT,
            prices TEXT,
            PRIMARY KEY (source_type, scryfall_id)
        );

        CREATE TABLE unique_artwork (
            scryfall_id TEXT PRIMARY KEY,
            oracle_id TEXT,
            name TEXT,
            normalized_name TEXT,
            illustration_id TEXT,
            artist TEXT,
            set_code TEXT,
            collector_number TEXT,
            image_status TEXT
        );

        CREATE TABLE names (
            name_key TEXT NOT NULL,
            display_name TEXT NOT NULL,
            oracle_id TEXT NOT NULL,
            scryfall_id TEXT NOT NULL,
            source TEXT NOT NULL,
            PRIMARY KEY (name_key, display_name, oracle_id, scryfall_id, source)
        );

        CREATE TABLE rulings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            oracle_id TEXT NOT NULL,
            source TEXT,
            published_at TEXT,
            comment TEXT
        );

        CREATE TABLE oracle_tags (
            tag_id TEXT PRIMARY KEY,
            slug TEXT NOT NULL,
            label TEXT,
            description TEXT,
            aliases TEXT,
            parent_ids TEXT,
            child_ids TEXT,
            tag_type TEXT
        );

        CREATE TABLE oracle_taggings (
            tag_id TEXT NOT NULL,
            slug TEXT NOT NULL,
            oracle_id TEXT NOT NULL,
            weight REAL,
            PRIMARY KEY (tag_id, oracle_id)
        );

        CREATE TABLE art_tags (
            tag_id TEXT PRIMARY KEY,
            slug TEXT NOT NULL,
            label TEXT,
            description TEXT,
            aliases TEXT,
            parent_ids TEXT,
            child_ids TEXT,
            tag_type TEXT
        );

        CREATE TABLE art_taggings (
            tag_id TEXT NOT NULL,
            slug TEXT NOT NULL,
            illustration_id TEXT NOT NULL,
            weight REAL,
            PRIMARY KEY (tag_id, illustration_id)
        );
        """
    )

    try:
        conn.executescript(
            """
            CREATE VIRTUAL TABLE oracle_cards_fts
            USING fts5(oracle_id UNINDEXED, name, type_line, oracle_text, keywords, tag_text);

            CREATE VIRTUAL TABLE oracle_tags_fts
            USING fts5(tag_id UNINDEXED, slug, label, aliases, description);

            CREATE VIRTUAL TABLE art_tags_fts
            USING fts5(tag_id UNINDEXED, slug, label, aliases, description);
            """
        )
        return True
    except sqlite3.OperationalError:
        conn.executescript(
            """
            CREATE TABLE oracle_cards_fts (
                oracle_id TEXT,
                name TEXT,
                type_line TEXT,
                oracle_text TEXT,
                keywords TEXT,
                tag_text TEXT
            );

            CREATE TABLE oracle_tags_fts (
                tag_id TEXT,
                slug TEXT,
                label TEXT,
                aliases TEXT,
                description TEXT
            );

            CREATE TABLE art_tags_fts (
                tag_id TEXT,
                slug TEXT,
                label TEXT,
                aliases TEXT,
                description TEXT
            );
            """
        )
        return False


def _create_indexes(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE INDEX idx_names_key ON names(name_key);
        CREATE INDEX idx_names_oracle_id ON names(oracle_id);
        CREATE INDEX idx_prints_oracle_id ON prints(oracle_id);
        CREATE INDEX idx_prints_normalized_name ON prints(normalized_name);
        CREATE INDEX idx_prints_color_identity_mask ON prints(color_identity_mask);
        CREATE INDEX idx_prints_mana_value ON prints(mana_value);
        CREATE INDEX idx_oracle_cards_normalized_name ON oracle_cards(normalized_name);
        CREATE INDEX idx_oracle_cards_color_identity_mask ON oracle_cards(color_identity_mask);
        CREATE INDEX idx_oracle_cards_mana_value ON oracle_cards(mana_value);
        CREATE INDEX idx_rulings_oracle_id ON rulings(oracle_id);
        CREATE INDEX idx_oracle_tags_slug ON oracle_tags(slug);
        CREATE INDEX idx_oracle_taggings_slug ON oracle_taggings(slug);
        CREATE INDEX idx_oracle_taggings_oracle_id ON oracle_taggings(oracle_id);
        CREATE INDEX idx_art_tags_slug ON art_tags(slug);
        CREATE INDEX idx_art_taggings_slug ON art_taggings(slug);
        CREATE INDEX idx_art_taggings_illustration_id ON art_taggings(illustration_id);
        """
    )


def _insert_bulk_sources(
    conn: sqlite3.Connection,
    manifest: dict[str, Any],
    counts: dict[str, int],
) -> None:
    rows = []
    for entry in manifest.get("entries", []):
        rows.append(
            (
                _text(entry.get("type")),
                _text(entry.get("name")),
                _text(entry.get("updated_at")),
                _text(entry.get("local_path")),
                _integer(entry.get("bytes_downloaded")),
                _text(entry.get("sha256")),
                _integer(entry.get("source_reported_json_size")),
            )
        )
    conn.executemany(
        """
        INSERT OR REPLACE INTO bulk_sources (
            source_type, name, updated_at, local_path, bytes_downloaded, sha256, source_reported_json_size
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    counts["bulk_sources"] = len(rows)


def _index_oracle_cards(
    conn: sqlite3.Connection,
    raw_root: Path,
    manifest: dict[str, Any],
    counts: dict[str, int],
) -> None:
    card_rows: list[tuple[Any, ...]] = []
    name_rows: list[tuple[str, str, str, str, str]] = []
    for path in _source_paths(raw_root, manifest, "oracle_cards"):
        for card in _iter_json_records(path):
            oracle_id = _text(card.get("oracle_id"))
            scryfall_id = _text(card.get("id"))
            card_rows.append(_oracle_card_row(card, oracle_id, scryfall_id))
            name_rows.extend(_name_rows(card, oracle_id, scryfall_id, "oracle_card"))
            counts["oracle_cards"] += 1
            _flush(
                conn,
                """
                INSERT OR REPLACE INTO oracle_cards (
                    oracle_id, scryfall_id, name, normalized_name, mana_cost, mana_value, colors,
                    color_identity, colors_mask, color_identity_mask, type_line, oracle_text,
                    keywords, legalities, prices, edhrec_rank, released_at, set_code,
                    collector_number, rarity, layout, is_basic_land, is_legendary,
                    is_commander_candidate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                card_rows,
            )
            _flush_names(conn, name_rows)

    _flush(
        conn,
        """
        INSERT OR REPLACE INTO oracle_cards (
            oracle_id, scryfall_id, name, normalized_name, mana_cost, mana_value, colors,
            color_identity, colors_mask, color_identity_mask, type_line, oracle_text,
            keywords, legalities, prices, edhrec_rank, released_at, set_code,
            collector_number, rarity, layout, is_basic_land, is_legendary,
            is_commander_candidate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        card_rows,
        force=True,
    )
    _flush_names(conn, name_rows, force=True)


def _index_print_cards(
    conn: sqlite3.Connection,
    raw_root: Path,
    manifest: dict[str, Any],
    source_type: str,
    counts: dict[str, int],
) -> None:
    print_rows: list[tuple[Any, ...]] = []
    name_rows: list[tuple[str, str, str, str, str]] = []
    for path in _source_paths(raw_root, manifest, source_type):
        for card in _iter_json_records(path):
            oracle_id = _text(card.get("oracle_id"))
            scryfall_id = _text(card.get("id"))
            print_rows.append(_print_row(card, source_type, oracle_id, scryfall_id))
            name_rows.extend(_name_rows(card, oracle_id, scryfall_id, source_type))
            counts["prints"] += 1
            counts[f"{source_type}_prints"] += 1
            _flush_prints(conn, print_rows)
            _flush_names(conn, name_rows)

    _flush_prints(conn, print_rows, force=True)
    _flush_names(conn, name_rows, force=True)


def _index_unique_artwork(
    conn: sqlite3.Connection,
    raw_root: Path,
    manifest: dict[str, Any],
    counts: dict[str, int],
) -> None:
    rows: list[tuple[Any, ...]] = []
    for path in _source_paths(raw_root, manifest, "unique_artwork"):
        for card in _iter_json_records(path):
            rows.append(
                (
                    _text(card.get("id")),
                    _text(card.get("oracle_id")),
                    _text(card.get("name")),
                    normalize_lookup_key(_text(card.get("name"))),
                    _text(card.get("illustration_id")),
                    _text(card.get("artist")),
                    _text(card.get("set")),
                    _text(card.get("collector_number")),
                    _text(card.get("image_status")),
                )
            )
            counts["unique_artwork"] += 1
            _flush(
                conn,
                """
                INSERT OR REPLACE INTO unique_artwork (
                    scryfall_id, oracle_id, name, normalized_name, illustration_id,
                    artist, set_code, collector_number, image_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

    _flush(
        conn,
        """
        INSERT OR REPLACE INTO unique_artwork (
            scryfall_id, oracle_id, name, normalized_name, illustration_id,
            artist, set_code, collector_number, image_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
        force=True,
    )


def _index_rulings(
    conn: sqlite3.Connection,
    raw_root: Path,
    manifest: dict[str, Any],
    counts: dict[str, int],
) -> None:
    rows: list[tuple[Any, ...]] = []
    for path in _source_paths(raw_root, manifest, "rulings"):
        for ruling in _iter_json_records(path):
            rows.append(
                (
                    _text(ruling.get("oracle_id")),
                    _text(ruling.get("source")),
                    _text(ruling.get("published_at")),
                    _text(ruling.get("comment")),
                )
            )
            counts["rulings"] += 1
            _flush(
                conn,
                "INSERT INTO rulings (oracle_id, source, published_at, comment) VALUES (?, ?, ?, ?)",
                rows,
            )
    _flush(
        conn,
        "INSERT INTO rulings (oracle_id, source, published_at, comment) VALUES (?, ?, ?, ?)",
        rows,
        force=True,
    )


def _index_oracle_tags(
    conn: sqlite3.Connection,
    raw_root: Path,
    manifest: dict[str, Any],
    counts: dict[str, int],
    tag_text_by_oracle_id: dict[str, set[str]],
) -> None:
    tag_rows: list[tuple[Any, ...]] = []
    tagging_rows: list[tuple[Any, ...]] = []
    fts_rows: list[tuple[Any, ...]] = []
    for path in _source_paths(raw_root, manifest, "oracle_tags"):
        for tag in _iter_json_records(path):
            tag_id = _text(tag.get("id"))
            slug = _text(tag.get("slug"))
            label = _text(tag.get("label"))
            aliases = _json_text(tag.get("aliases", []))
            tag_rows.append(_tag_row(tag, tag_id, slug))
            fts_rows.append((tag_id, slug, label, _list_text(tag.get("aliases", [])), _text(tag.get("description"))))
            counts["oracle_tags"] += 1
            for tagging in tag.get("taggings", []):
                oracle_id = _text(tagging.get("oracle_id"))
                if not oracle_id:
                    continue
                tagging_rows.append((tag_id, slug, oracle_id, _real(tagging.get("weight"))))
                tag_text_by_oracle_id[oracle_id].update((slug, label, _list_text(tag.get("aliases", []))))
                counts["oracle_taggings"] += 1
            _flush_tags(conn, "oracle_tags", tag_rows)
            _flush(
                conn,
                "INSERT OR REPLACE INTO oracle_taggings (tag_id, slug, oracle_id, weight) VALUES (?, ?, ?, ?)",
                tagging_rows,
            )
            _flush_oracle_tags_fts(conn, fts_rows)

    _flush_tags(conn, "oracle_tags", tag_rows, force=True)
    _flush(
        conn,
        "INSERT OR REPLACE INTO oracle_taggings (tag_id, slug, oracle_id, weight) VALUES (?, ?, ?, ?)",
        tagging_rows,
        force=True,
    )
    _flush_oracle_tags_fts(conn, fts_rows, force=True)


def _index_art_tags(
    conn: sqlite3.Connection,
    raw_root: Path,
    manifest: dict[str, Any],
    counts: dict[str, int],
) -> None:
    tag_rows: list[tuple[Any, ...]] = []
    tagging_rows: list[tuple[Any, ...]] = []
    fts_rows: list[tuple[Any, ...]] = []
    for path in _source_paths(raw_root, manifest, "art_tags"):
        for tag in _iter_json_records(path):
            tag_id = _text(tag.get("id"))
            slug = _text(tag.get("slug"))
            label = _text(tag.get("label"))
            tag_rows.append(_tag_row(tag, tag_id, slug))
            fts_rows.append((tag_id, slug, label, _list_text(tag.get("aliases", [])), _text(tag.get("description"))))
            counts["art_tags"] += 1
            for tagging in tag.get("taggings", []):
                illustration_id = _text(tagging.get("illustration_id"))
                if not illustration_id:
                    continue
                tagging_rows.append((tag_id, slug, illustration_id, _real(tagging.get("weight"))))
                counts["art_taggings"] += 1
            _flush_tags(conn, "art_tags", tag_rows)
            _flush(
                conn,
                "INSERT OR REPLACE INTO art_taggings (tag_id, slug, illustration_id, weight) VALUES (?, ?, ?, ?)",
                tagging_rows,
            )
            _flush_art_tags_fts(conn, fts_rows)

    _flush_tags(conn, "art_tags", tag_rows, force=True)
    _flush(
        conn,
        "INSERT OR REPLACE INTO art_taggings (tag_id, slug, illustration_id, weight) VALUES (?, ?, ?, ?)",
        tagging_rows,
        force=True,
    )
    _flush_art_tags_fts(conn, fts_rows, force=True)


def _index_oracle_card_fts(
    conn: sqlite3.Connection,
    counts: dict[str, int],
    tag_text_by_oracle_id: dict[str, set[str]],
) -> None:
    rows: list[tuple[Any, ...]] = []
    query = """
        SELECT oracle_id, name, type_line, oracle_text, keywords
        FROM oracle_cards
        ORDER BY oracle_id
    """
    for oracle_id, name, type_line, oracle_text, keywords_json in conn.execute(query):
        tag_text = " ".join(sorted(tag_text_by_oracle_id.get(oracle_id, set())))
        keywords = _list_text(_safe_json_loads(keywords_json))
        rows.append((oracle_id, name, type_line, oracle_text, keywords, tag_text))
        counts["oracle_cards_fts"] += 1
        _flush_oracle_cards_fts(conn, rows)
    _flush_oracle_cards_fts(conn, rows, force=True)


def _oracle_card_row(card: dict[str, Any], oracle_id: str, scryfall_id: str) -> tuple[Any, ...]:
    name = _text(card.get("name"))
    type_line = _card_text(card, "type_line")
    oracle_text = _card_text(card, "oracle_text")
    keywords = card.get("keywords", [])
    color_identity = _list_of_text(card.get("color_identity", []))
    colors = _list_of_text(card.get("colors", []))
    return (
        oracle_id,
        scryfall_id,
        name,
        normalize_lookup_key(name),
        _card_text(card, "mana_cost"),
        _real(card.get("cmc")),
        _json_text(colors),
        _json_text(color_identity),
        _color_mask(colors),
        _color_mask(color_identity),
        type_line,
        oracle_text,
        _json_text(keywords),
        _json_text(card.get("legalities", {})),
        _json_text(card.get("prices", {})),
        _integer(card.get("edhrec_rank")),
        _text(card.get("released_at")),
        _text(card.get("set")),
        _text(card.get("collector_number")),
        _text(card.get("rarity")),
        _text(card.get("layout")),
        int(_is_basic_land(type_line)),
        int("Legendary" in type_line),
        int(_is_commander_candidate(type_line, oracle_text)),
    )


def _print_row(
    card: dict[str, Any],
    source_type: str,
    oracle_id: str,
    scryfall_id: str,
) -> tuple[Any, ...]:
    name = _text(card.get("name"))
    colors = _list_of_text(card.get("colors", []))
    color_identity = _list_of_text(card.get("color_identity", []))
    is_all_cards = source_type == "all_cards"
    return (
        source_type,
        scryfall_id,
        oracle_id,
        name,
        normalize_lookup_key(name),
        _text(card.get("lang")),
        _text(card.get("set")),
        _text(card.get("set_name")),
        _text(card.get("collector_number")),
        _text(card.get("rarity")),
        _text(card.get("released_at")),
        _text(card.get("layout")),
        _real(card.get("cmc")),
        _card_text(card, "type_line"),
        "" if is_all_cards else _card_text(card, "oracle_text"),
        _json_text(colors),
        _json_text(color_identity),
        _color_mask(colors),
        _color_mask(color_identity),
        _text(card.get("artist")),
        _text(card.get("illustration_id")),
        _text(card.get("image_status")),
        "{}" if is_all_cards else _json_text(card.get("legalities", {})),
        "{}" if is_all_cards else _json_text(card.get("prices", {})),
    )


def _tag_row(tag: dict[str, Any], tag_id: str, slug: str) -> tuple[Any, ...]:
    return (
        tag_id,
        slug,
        _text(tag.get("label")),
        _text(tag.get("description")),
        _json_text(tag.get("aliases", [])),
        _json_text(tag.get("parent_ids", [])),
        _json_text(tag.get("child_ids", [])),
        _text(tag.get("type")),
    )


def _name_rows(
    card: dict[str, Any],
    oracle_id: str,
    scryfall_id: str,
    source: str,
) -> list[tuple[str, str, str, str, str]]:
    rows = []
    for name in _name_variants(card):
        key = normalize_lookup_key(name)
        if key:
            rows.append((key, name, oracle_id, scryfall_id, source))
    return rows


def _name_variants(card: dict[str, Any]) -> Iterable[str]:
    name = _text(card.get("name"))
    if name:
        yield name
    for face in card.get("card_faces", []) or []:
        face_name = _text(face.get("name"))
        if face_name and face_name != name:
            yield face_name


def _source_paths(raw_root: Path, manifest: dict[str, Any], source_type: str) -> list[Path]:
    entries = [entry for entry in manifest.get("entries", []) if entry.get("type") == source_type]
    paths: list[Path] = []
    for entry in entries:
        candidate = _resolve_local_path(raw_root, entry)
        if not candidate.exists():
            raise FileNotFoundError(f"Local Scryfall source missing for {source_type}: {candidate}")
        paths.append(candidate)

    if paths:
        return paths

    source_dir = raw_root / source_type
    if not source_dir.exists():
        return []
    return sorted(
        path
        for path in source_dir.iterdir()
        if path.suffix in {".json", ".jsonl", ".gz"} or path.name.endswith(".jsonl.gz")
    )


def _resolve_local_path(raw_root: Path, entry: dict[str, Any]) -> Path:
    local_path = Path(_text(entry.get("local_path")))
    candidates = []
    if local_path.is_absolute():
        candidates.append(local_path)
    else:
        candidates.extend(
            [
                Path.cwd() / local_path,
                raw_root / local_path,
                raw_root / _text(entry.get("type")) / local_path.name,
            ]
        )

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[-1]


def _iter_json_records(path: Path) -> Iterator[dict[str, Any]]:
    opener = gzip.open if path.name.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as handle:
        first_non_ws = _peek_non_whitespace(handle)
        if first_non_ws == "[":
            yield from _iter_json_array(handle)
        else:
            for line in handle:
                stripped = line.strip()
                if stripped:
                    yield json.loads(stripped)


def _peek_non_whitespace(handle: Any) -> str:
    while True:
        position = handle.tell()
        char = handle.read(1)
        if not char:
            return ""
        if not char.isspace():
            handle.seek(position)
            return char


def _iter_json_array(handle: Any) -> Iterator[dict[str, Any]]:
    payload = json.load(handle)
    if isinstance(payload, list):
        yield from payload
    elif isinstance(payload, dict) and isinstance(payload.get("data"), list):
        yield from payload["data"]
    else:
        raise ValueError("Expected JSON array or object with data array.")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload


def _write_index_manifest(
    path: Path,
    output_path: Path,
    source_manifest_path: Path,
    source_manifest: dict[str, Any],
    counts: dict[str, int],
    fts_available: bool,
) -> None:
    payload = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "counts": counts,
        "fts_available": fts_available,
        "index_path": str(output_path),
        "no_api_calls": True,
        "object": "mtg_workbench_scryfall_index_manifest",
        "schema_version": 1,
        "source_entries": [
            {
                "bytes_downloaded": entry.get("bytes_downloaded"),
                "local_path": entry.get("local_path"),
                "sha256": entry.get("sha256"),
                "type": entry.get("type"),
                "updated_at": entry.get("updated_at"),
            }
            for entry in source_manifest.get("entries", [])
        ],
        "source_manifest_path": str(source_manifest_path),
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _flush(
    conn: sqlite3.Connection,
    sql: str,
    rows: list[tuple[Any, ...]],
    *,
    force: bool = False,
) -> None:
    if rows and (force or len(rows) >= BATCH_SIZE):
        conn.executemany(sql, rows)
        rows.clear()


def _flush_names(
    conn: sqlite3.Connection,
    rows: list[tuple[str, str, str, str, str]],
    *,
    force: bool = False,
) -> None:
    _flush(
        conn,
        """
        INSERT OR IGNORE INTO names (name_key, display_name, oracle_id, scryfall_id, source)
        VALUES (?, ?, ?, ?, ?)
        """,
        rows,
        force=force,
    )


def _flush_prints(conn: sqlite3.Connection, rows: list[tuple[Any, ...]], *, force: bool = False) -> None:
    _flush(
        conn,
        """
        INSERT OR REPLACE INTO prints (
            source_type, scryfall_id, oracle_id, name, normalized_name, lang, set_code,
            set_name, collector_number, rarity, released_at, layout, mana_value,
            type_line, oracle_text, colors, color_identity, colors_mask,
            color_identity_mask, artist, illustration_id, image_status, legalities, prices
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
        force=force,
    )


def _flush_tags(
    conn: sqlite3.Connection,
    table: str,
    rows: list[tuple[Any, ...]],
    *,
    force: bool = False,
) -> None:
    _flush(
        conn,
        f"""
        INSERT OR REPLACE INTO {table} (
            tag_id, slug, label, description, aliases, parent_ids, child_ids, tag_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
        force=force,
    )


def _flush_oracle_cards_fts(
    conn: sqlite3.Connection,
    rows: list[tuple[Any, ...]],
    *,
    force: bool = False,
) -> None:
    _flush(
        conn,
        """
        INSERT INTO oracle_cards_fts (oracle_id, name, type_line, oracle_text, keywords, tag_text)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows,
        force=force,
    )


def _flush_oracle_tags_fts(
    conn: sqlite3.Connection,
    rows: list[tuple[Any, ...]],
    *,
    force: bool = False,
) -> None:
    _flush(
        conn,
        "INSERT INTO oracle_tags_fts (tag_id, slug, label, aliases, description) VALUES (?, ?, ?, ?, ?)",
        rows,
        force=force,
    )


def _flush_art_tags_fts(
    conn: sqlite3.Connection,
    rows: list[tuple[Any, ...]],
    *,
    force: bool = False,
) -> None:
    _flush(
        conn,
        "INSERT INTO art_tags_fts (tag_id, slug, label, aliases, description) VALUES (?, ?, ?, ?, ?)",
        rows,
        force=force,
    )


def _empty_counts() -> dict[str, int]:
    counts = {
        "art_tags": 0,
        "art_taggings": 0,
        "bulk_sources": 0,
        "oracle_cards": 0,
        "oracle_cards_fts": 0,
        "oracle_tags": 0,
        "oracle_taggings": 0,
        "prints": 0,
        "rulings": 0,
        "unique_artwork": 0,
    }
    for source_type in ("default_cards", "all_cards"):
        counts[f"{source_type}_prints"] = 0
    return counts


def _remove_sqlite_file(path: Path) -> None:
    for candidate in (path, Path(f"{path}-wal"), Path(f"{path}-shm")):
        if candidate.exists():
            candidate.unlink()


def _card_text(card: dict[str, Any], field: str) -> str:
    value = card.get(field)
    if value:
        return _text(value)
    face_values = []
    for face in card.get("card_faces", []) or []:
        face_value = face.get(field)
        if face_value:
            face_values.append(_text(face_value))
    return "\n".join(face_values)


def _is_basic_land(type_line: str) -> bool:
    return "Basic" in type_line and "Land" in type_line


def _is_commander_candidate(type_line: str, oracle_text: str) -> bool:
    lowered = oracle_text.casefold()
    return "Legendary Creature" in type_line or "can be your commander" in lowered


def _color_mask(colors: Iterable[str]) -> int:
    mask = 0
    for color in colors:
        mask |= COLOR_BITS.get(color, 0)
    return mask


def _list_of_text(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [_text(item) for item in value if _text(item)]


def _list_text(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(_text(item) for item in value if _text(item))
    return _text(value)


def _json_text(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _safe_json_loads(value: str | None) -> Any:
    if not value:
        return []
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return []


def _text(value: Any) -> str:
    return "" if value is None else str(value)


def _integer(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _real(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

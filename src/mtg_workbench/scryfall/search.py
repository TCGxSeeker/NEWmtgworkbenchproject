from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import shlex
import sqlite3
from typing import Any, Iterable

from mtg_workbench.cards.catalog import normalize_lookup_key
from mtg_workbench.scryfall.indexer import COLOR_BITS


_MV_RE = re.compile(r"^(mv|cmc)(?::)?(<=|>=|<|>|=)?(.+)$", re.IGNORECASE)
_USD_RE = re.compile(r"^usd(?::)?(<=|>=|<|>|=)?(.+)$", re.IGNORECASE)
_PREFIX_RE = re.compile(r"^([A-Za-z]+):(.*)$")
_UNKNOWN_COMPARISON_RE = re.compile(r"^[A-Za-z]+(?:<=|>=|<|>|=).+")
_LIKE_ESCAPE_RE = re.compile(r"([%_\\])")


@dataclass(frozen=True)
class SearchClause:
    kind: str
    raw: str
    value: str
    operator: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {"kind": self.kind, "raw": self.raw, "value": self.value}
        if self.operator is not None:
            payload["operator"] = self.operator
        return payload


@dataclass(frozen=True)
class UnsupportedClause:
    raw: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return {"raw": self.raw, "reason": self.reason}


def search_cards(index_path: str | Path, query: str, limit: int = 25) -> dict[str, Any]:
    clauses, unsupported = parse_query(query)
    conn = sqlite3.connect(Path(index_path))
    conn.row_factory = sqlite3.Row
    try:
        snapshot_updated_at = _snapshot_updated_at(conn)
        tag_matches: dict[str, list[dict[str, Any]]] = {}
        candidate_ids: set[str] | None = None
        matched_terms: dict[str, set[str]] = {}

        for clause in clauses:
            clause_ids, clause_matches = _resolve_clause(conn, clause)
            candidate_ids = _intersect(candidate_ids, clause_ids)
            for oracle_id, terms in clause_matches.items():
                matched_terms.setdefault(oracle_id, set()).update(terms)
            if clause.kind == "oracle_tag":
                for oracle_id, matches in _tag_matches(conn, clause).items():
                    tag_matches.setdefault(oracle_id, []).extend(matches)

        if candidate_ids is None:
            candidate_ids = set()

        rows = _fetch_result_rows(conn, candidate_ids, limit)
    finally:
        conn.close()

    results = [
        _result_to_dict(
            row,
            matched_terms=sorted(matched_terms.get(row["oracle_id"], set())),
            tag_matches=tag_matches.get(row["oracle_id"], []),
        )
        for row in rows
    ]

    return {
        "object": "mtg_workbench_scryfall_search_result",
        "query": query,
        "result_count": len(candidate_ids),
        "results": results,
        "snapshot_updated_at": snapshot_updated_at,
        "supported_clauses": [clause.to_dict() for clause in clauses],
        "unsupported_clauses": [clause.to_dict() for clause in unsupported],
    }


def parse_query(query: str) -> tuple[list[SearchClause], list[UnsupportedClause]]:
    clauses: list[SearchClause] = []
    unsupported: list[UnsupportedClause] = []
    for raw in _split_query(query):
        mv_match = _MV_RE.match(raw)
        if mv_match:
            operator = mv_match.group(2) or "="
            value = mv_match.group(3).strip()
            if _as_float(value) is None:
                unsupported.append(UnsupportedClause(raw=raw, reason="invalid_mana_value"))
            else:
                clauses.append(SearchClause(kind="mana_value", raw=raw, value=value, operator=operator))
            continue

        usd_match = _USD_RE.match(raw)
        if usd_match:
            operator = usd_match.group(1) or "="
            value = usd_match.group(2).strip()
            if _as_float(value) is None:
                unsupported.append(UnsupportedClause(raw=raw, reason="invalid_usd_price"))
            else:
                clauses.append(SearchClause(kind="usd_price", raw=raw, value=value, operator=operator))
            continue

        prefix_match = _PREFIX_RE.match(raw)
        if prefix_match:
            prefix = prefix_match.group(1).casefold()
            value = prefix_match.group(2).strip()
            if not value:
                unsupported.append(UnsupportedClause(raw=raw, reason="missing_value"))
            elif prefix in {"o", "oracle"}:
                clauses.append(SearchClause(kind="oracle_text", raw=raw, value=value))
            elif prefix in {"t", "type"}:
                clauses.append(SearchClause(kind="type_line", raw=raw, value=value))
            elif prefix == "otag":
                clauses.append(SearchClause(kind="oracle_tag", raw=raw, value=value))
            elif prefix in {"ci", "id"}:
                if _color_mask_from_text(value) is None:
                    unsupported.append(UnsupportedClause(raw=raw, reason="invalid_color_identity"))
                else:
                    clauses.append(SearchClause(kind="color_identity", raw=raw, value=value))
            elif prefix == "legal":
                if value.casefold() == "commander":
                    clauses.append(SearchClause(kind="legality", raw=raw, value=value.casefold()))
                else:
                    unsupported.append(UnsupportedClause(raw=raw, reason="unsupported_syntax"))
            elif prefix in {"r", "rarity"}:
                clauses.append(SearchClause(kind="rarity", raw=raw, value=value.casefold()))
            elif prefix == "set":
                clauses.append(SearchClause(kind="set_code", raw=raw, value=value.casefold()))
            elif prefix == "is":
                if value.casefold() == "commander":
                    clauses.append(SearchClause(kind="commander_candidate", raw=raw, value=value.casefold()))
                else:
                    unsupported.append(UnsupportedClause(raw=raw, reason="unsupported_syntax"))
            else:
                unsupported.append(UnsupportedClause(raw=raw, reason="unsupported_syntax"))
            continue

        if ":" in raw or _UNKNOWN_COMPARISON_RE.match(raw):
            unsupported.append(UnsupportedClause(raw=raw, reason="unsupported_syntax"))
        else:
            clauses.append(SearchClause(kind="bare_text", raw=raw, value=raw))

    return clauses, unsupported


def _resolve_clause(
    conn: sqlite3.Connection,
    clause: SearchClause,
) -> tuple[set[str], dict[str, set[str]]]:
    if clause.kind == "bare_text":
        ids = _bare_text_ids(conn, clause.value)
        return ids, _clause_match_terms(ids, clause.raw)
    if clause.kind == "oracle_text":
        ids = _text_filter_ids(conn, "oracle_text", clause.value)
        return ids, _clause_match_terms(ids, clause.raw)
    if clause.kind == "type_line":
        ids = _text_filter_ids(conn, "type_line", clause.value)
        return ids, _clause_match_terms(ids, clause.raw)
    if clause.kind == "oracle_tag":
        ids = set(_tag_matches(conn, clause).keys())
        return ids, _clause_match_terms(ids, clause.raw)
    if clause.kind == "color_identity":
        mask = _color_mask_from_text(clause.value)
        if mask is None:
            return set(), {}
        ids = _simple_filter_ids(conn, "color_identity_mask = ?", (mask,))
        return ids, _clause_match_terms(ids, clause.raw)
    if clause.kind == "mana_value":
        value = _as_float(clause.value)
        if value is None or clause.operator not in {"=", "<", "<=", ">", ">="}:
            return set(), {}
        ids = _simple_filter_ids(conn, f"mana_value {clause.operator} ?", (value,))
        return ids, _clause_match_terms(ids, clause.raw)
    if clause.kind == "legality":
        ids = _legality_filter_ids(conn, clause.value)
        return ids, _clause_match_terms(ids, clause.raw)
    if clause.kind == "usd_price":
        value = _as_float(clause.value)
        if value is None or clause.operator not in {"=", "<", "<=", ">", ">="}:
            return set(), {}
        ids = _usd_price_filter_ids(conn, clause.operator, value)
        return ids, _clause_match_terms(ids, clause.raw)
    if clause.kind == "rarity":
        ids = _simple_filter_ids(conn, "rarity = ? COLLATE NOCASE", (clause.value,))
        return ids, _clause_match_terms(ids, clause.raw)
    if clause.kind == "set_code":
        ids = _simple_filter_ids(conn, "set_code = ? COLLATE NOCASE", (clause.value,))
        return ids, _clause_match_terms(ids, clause.raw)
    if clause.kind == "commander_candidate":
        ids = _simple_filter_ids(conn, "is_commander_candidate = 1", ())
        return ids, _clause_match_terms(ids, clause.raw)
    return set(), {}


def _bare_text_ids(conn: sqlite3.Connection, value: str) -> set[str]:
    name_key = normalize_lookup_key(value)
    name_like = f"%{_escape_like(name_key)}%"
    rows = conn.execute(
        """
        SELECT oracle_id FROM oracle_cards WHERE normalized_name LIKE ? ESCAPE '\\'
        UNION
        SELECT oracle_id FROM names WHERE name_key LIKE ? ESCAPE '\\'
        """,
        (name_like, name_like),
    ).fetchall()
    name_ids = {row[0] for row in rows}
    if name_ids:
        return name_ids

    return _text_filter_ids(conn, "all_text", value)


def _text_filter_ids(conn: sqlite3.Connection, field: str, value: str) -> set[str]:
    like_value = f"%{_escape_like(value.casefold())}%"
    if field == "oracle_text":
        sql = "SELECT oracle_id FROM oracle_cards WHERE lower(oracle_text) LIKE ? ESCAPE '\\'"
        return {row[0] for row in conn.execute(sql, (like_value,))}
    if field == "type_line":
        sql = "SELECT oracle_id FROM oracle_cards WHERE lower(type_line) LIKE ? ESCAPE '\\'"
        return {row[0] for row in conn.execute(sql, (like_value,))}
    sql = """
        SELECT oracle_id
        FROM oracle_cards
        WHERE lower(name) LIKE ? ESCAPE '\\'
           OR lower(type_line) LIKE ? ESCAPE '\\'
           OR lower(oracle_text) LIKE ? ESCAPE '\\'
    """
    return {row[0] for row in conn.execute(sql, (like_value, like_value, like_value))}


def _simple_filter_ids(conn: sqlite3.Connection, where: str, params: tuple[Any, ...]) -> set[str]:
    return {row[0] for row in conn.execute(f"SELECT oracle_id FROM oracle_cards WHERE {where}", params)}


def _legality_filter_ids(conn: sqlite3.Connection, format_name: str) -> set[str]:
    rows = conn.execute("SELECT oracle_id, legalities FROM oracle_cards")
    matches = set()
    for oracle_id, legalities_json in rows:
        status = _json_object(legalities_json).get(format_name.casefold())
        if isinstance(status, str) and status.casefold() == "legal":
            matches.add(oracle_id)
    return matches


def _usd_price_filter_ids(conn: sqlite3.Connection, operator: str, value: float) -> set[str]:
    rows = conn.execute("SELECT oracle_id, prices FROM oracle_cards")
    matches = set()
    for oracle_id, prices_json in rows:
        price = _as_float(_json_object(prices_json).get("usd"))
        if price is not None and _compare_number(price, operator, value):
            matches.add(oracle_id)
    return matches


def _tag_matches(conn: sqlite3.Connection, clause: SearchClause) -> dict[str, list[dict[str, Any]]]:
    tag_rows = _matching_tags(conn, clause.value)
    if not tag_rows:
        return {}

    tag_ids = [row["tag_id"] for row in tag_rows]
    placeholders = ", ".join("?" for _ in tag_ids)
    rows = conn.execute(
        f"""
        SELECT tag_id, slug, oracle_id, weight
        FROM oracle_taggings
        WHERE tag_id IN ({placeholders})
        ORDER BY slug, weight DESC, oracle_id
        """,
        tuple(tag_ids),
    )
    tag_by_id = {row["tag_id"]: row for row in tag_rows}
    matches: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        tag = tag_by_id[row["tag_id"]]
        matches.setdefault(row["oracle_id"], []).append(
            {
                "label": tag["label"],
                "slug": row["slug"],
                "weight": row["weight"],
            }
        )
    return matches


def _matching_tags(conn: sqlite3.Connection, value: str) -> list[sqlite3.Row]:
    normalized = value.strip().casefold()
    slug = normalized.replace(" ", "-")
    rows = conn.execute(
        """
        SELECT tag_id, slug, label, aliases
        FROM oracle_tags
        ORDER BY slug
        """
    )
    matches = []
    for row in rows:
        aliases = [alias.casefold() for alias in _json_list(row["aliases"])]
        if row["slug"].casefold() == slug or row["label"].casefold() == normalized or normalized in aliases:
            matches.append(row)
    return matches


def _fetch_result_rows(conn: sqlite3.Connection, oracle_ids: set[str], limit: int) -> list[sqlite3.Row]:
    if not oracle_ids:
        return []
    placeholders = ", ".join("?" for _ in oracle_ids)
    return list(
        conn.execute(
            f"""
            SELECT oracle_id, name, mana_value, color_identity, type_line, oracle_text
            FROM oracle_cards
            WHERE oracle_id IN ({placeholders})
            ORDER BY name, oracle_id
            LIMIT ?
            """,
            (*sorted(oracle_ids), max(0, limit)),
        )
    )


def _result_to_dict(
    row: sqlite3.Row,
    *,
    matched_terms: list[str],
    tag_matches: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "color_identity": _json_list(row["color_identity"]),
        "mana_value": row["mana_value"],
        "matched_terms": matched_terms,
        "name": row["name"],
        "oracle_id": row["oracle_id"],
        "oracle_text": row["oracle_text"],
        "tag_matches": tag_matches,
        "type_line": row["type_line"],
    }


def _split_query(query: str) -> list[str]:
    try:
        return shlex.split(query)
    except ValueError:
        return query.split()


def _snapshot_updated_at(conn: sqlite3.Connection) -> str | None:
    row = conn.execute("SELECT max(updated_at) FROM bulk_sources").fetchone()
    return row[0] if row and row[0] else None


def _intersect(left: set[str] | None, right: set[str]) -> set[str]:
    if left is None:
        return set(right)
    return left & right


def _clause_match_terms(oracle_ids: Iterable[str], raw: str) -> dict[str, set[str]]:
    return {oracle_id: {raw} for oracle_id in oracle_ids}


def _color_mask_from_text(value: str) -> int | None:
    normalized = value.strip().upper()
    if normalized in {"C", "COLORLESS", "NONE"}:
        return 0

    colors = [char for char in normalized if char in COLOR_BITS]
    if not colors and normalized:
        return None
    if any(char.isalpha() and char not in COLOR_BITS for char in normalized):
        return None
    mask = 0
    for color in colors:
        mask |= COLOR_BITS[color]
    return mask


def _as_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _compare_number(left: float, operator: str, right: float) -> bool:
    if operator == "=":
        return left == right
    if operator == "<":
        return left < right
    if operator == "<=":
        return left <= right
    if operator == ">":
        return left > right
    if operator == ">=":
        return left >= right
    return False


def _escape_like(value: str) -> str:
    return _LIKE_ESCAPE_RE.sub(r"\\\1", value)


def _json_object(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return {}
    if isinstance(payload, dict):
        return {str(key).casefold(): item for key, item in payload.items()}
    return {}


def _json_list(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return []
    if isinstance(payload, list):
        return [str(item) for item in payload]
    return []

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from mtg_workbench.cards.catalog import CardCatalog, CardRecord, normalize_lookup_key
from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace


FOUND = "found"
MISSING = "missing"
AMBIGUOUS = "ambiguous"


class CardFactLookupError(ValueError):
    pass


@dataclass(frozen=True)
class CardFactCandidate:
    display_name: str
    lookup_key: str
    matched_name: str
    record: dict[str, Any]
    oracle_id: str | None = None
    selected_printing_id: str | None = None

    def to_dict(self, *, include_record: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "display_name": self.display_name,
            "lookup_key": self.lookup_key,
            "matched_name": self.matched_name,
            "oracle_id": self.oracle_id,
            "selected_printing_id": self.selected_printing_id,
        }
        if include_record:
            payload["record"] = dict(self.record)
        return payload


@dataclass(frozen=True)
class CardFactLookupResult:
    entry_id: str
    zone: str
    input_name: str
    display_name: str | None
    lookup_name: str
    lookup_key: str
    status: str
    candidates: tuple[CardFactCandidate, ...]
    user_summary: str

    @property
    def is_found(self) -> bool:
        return self.status == FOUND

    @property
    def is_missing(self) -> bool:
        return self.status == MISSING

    @property
    def is_ambiguous(self) -> bool:
        return self.status == AMBIGUOUS

    @property
    def record(self) -> dict[str, Any] | None:
        if not self.is_found:
            return None
        return dict(self.candidates[0].record)

    def to_dict(
        self,
        *,
        include_debug: bool = False,
        include_record: bool = False,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "entry_id": self.entry_id,
            "zone": self.zone,
            "status": self.status,
            "user_summary": self.user_summary,
            "machine_evidence": {
                "input_name": self.input_name,
                "display_name": self.display_name,
                "lookup_name": self.lookup_name,
                "lookup_key": self.lookup_key,
                "candidate_count": len(self.candidates),
                "candidate_names": [candidate.display_name for candidate in self.candidates],
            },
        }

        if include_debug:
            payload["debug_details"] = {
                "candidates": [
                    candidate.to_dict(include_record=include_record)
                    for candidate in self.candidates
                ],
            }

        return payload


@dataclass(frozen=True)
class CardFactLookupReport:
    schema_version: str
    deck_id: str
    deck_name: str
    results: tuple[CardFactLookupResult, ...]
    user_summary: str

    @property
    def found_count(self) -> int:
        return sum(1 for result in self.results if result.is_found)

    @property
    def missing_count(self) -> int:
        return sum(1 for result in self.results if result.is_missing)

    @property
    def ambiguous_count(self) -> int:
        return sum(1 for result in self.results if result.is_ambiguous)

    def found_records_by_entry_id(self) -> dict[str, dict[str, Any]]:
        return {
            result.entry_id: result.record
            for result in self.results
            if result.record is not None
        }

    def to_dict(
        self,
        *,
        include_debug: bool = False,
        include_records: bool = False,
    ) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "deck_id": self.deck_id,
            "deck_name": self.deck_name,
            "user_summary": self.user_summary,
            "found_count": self.found_count,
            "missing_count": self.missing_count,
            "ambiguous_count": self.ambiguous_count,
            "results": [
                result.to_dict(include_debug=include_debug, include_record=include_records)
                for result in self.results
            ],
        }


def lookup_deck_entry_card_fact(
    entry: DeckEntry,
    *,
    card_records: Iterable[Mapping[str, Any] | CardRecord] | Mapping[str, Mapping[str, Any] | CardRecord] | None = None,
    catalog: CardCatalog | None = None,
) -> CardFactLookupResult:
    resolver = _resolver_from_sources(card_records=card_records, catalog=catalog)
    return _lookup_entry(entry, resolver)


def lookup_workspace_card_facts(
    workspace: DeckWorkspace,
    *,
    card_records: Iterable[Mapping[str, Any] | CardRecord] | Mapping[str, Mapping[str, Any] | CardRecord] | None = None,
    catalog: CardCatalog | None = None,
) -> CardFactLookupReport:
    resolver = _resolver_from_sources(card_records=card_records, catalog=catalog)
    results = tuple(_lookup_entry(entry, resolver) for entry in workspace.all_entries())
    return CardFactLookupReport(
        schema_version="card_fact_lookup_report.v0",
        deck_id=workspace.deck_id,
        deck_name=workspace.name,
        results=results,
        user_summary=_build_report_summary(workspace.name, results),
    )


def _resolver_from_sources(
    *,
    card_records: Iterable[Mapping[str, Any] | CardRecord] | Mapping[str, Mapping[str, Any] | CardRecord] | None,
    catalog: CardCatalog | None,
):
    if card_records is not None and catalog is not None:
        raise CardFactLookupError("Provide either card_records or catalog, not both.")
    if card_records is None and catalog is None:
        raise CardFactLookupError("Card fact lookup requires card_records or catalog.")
    if catalog is not None:
        return _CatalogResolver(catalog)
    return _RecordResolver(card_records)


def _lookup_entry(entry: DeckEntry, resolver) -> CardFactLookupResult:
    lookup_name = entry.display_name or entry.input_name
    lookup_key = normalize_lookup_key(lookup_name)
    candidates = resolver.resolve(lookup_name)

    if not candidates:
        status = MISSING
    elif len(candidates) == 1:
        status = FOUND
    else:
        status = AMBIGUOUS

    return CardFactLookupResult(
        entry_id=entry.entry_id,
        zone=entry.zone,
        input_name=entry.input_name,
        display_name=entry.display_name,
        lookup_name=lookup_name,
        lookup_key=lookup_key,
        status=status,
        candidates=candidates if status != MISSING else (),
        user_summary=_build_result_summary(entry, lookup_name, status, candidates),
    )


class _CatalogResolver:
    def __init__(self, catalog: CardCatalog) -> None:
        self.catalog = catalog

    def resolve(self, lookup_name: str) -> tuple[CardFactCandidate, ...]:
        cards = self.catalog.find_all(lookup_name)

        candidates = [
            _candidate_from_record(
                _card_record_to_dict(card),
                lookup_name,
            )
            for card in cards
        ]

        return tuple(_dedupe_candidates(candidates))


class _RecordResolver:
    def __init__(
        self,
        card_records: Iterable[Mapping[str, Any] | CardRecord] | Mapping[str, Mapping[str, Any] | CardRecord] | None,
    ) -> None:
        self._lookup: dict[str, tuple[CardFactCandidate, ...]] = self._build_lookup(card_records)

    def resolve(self, lookup_name: str) -> tuple[CardFactCandidate, ...]:
        return self._lookup.get(normalize_lookup_key(lookup_name), ())

    def _build_lookup(
        self,
        card_records: Iterable[Mapping[str, Any] | CardRecord] | Mapping[str, Mapping[str, Any] | CardRecord] | None,
    ) -> dict[str, tuple[CardFactCandidate, ...]]:
        grouped: dict[str, list[CardFactCandidate]] = defaultdict(list)
        for record, explicit_name in _iter_records(card_records):
            record_dict = _record_to_dict(record, explicit_name=explicit_name)
            display_name = _display_name(record_dict)
            if not display_name:
                continue

            matched_names = _matched_names(record_dict, explicit_name)
            for matched_name in matched_names:
                candidate = _candidate_from_record(record_dict, matched_name)
                grouped[candidate.lookup_key].append(candidate)

        return {
            key: tuple(_dedupe_candidates(candidates))
            for key, candidates in grouped.items()
        }


def _iter_records(
    card_records: Iterable[Mapping[str, Any] | CardRecord] | Mapping[str, Mapping[str, Any] | CardRecord] | None,
):
    if isinstance(card_records, Mapping):
        for explicit_name, record in card_records.items():
            yield record, str(explicit_name)
        return

    for record in card_records or ():
        yield record, None


def _record_to_dict(
    record: Mapping[str, Any] | CardRecord,
    *,
    explicit_name: str | None = None,
) -> dict[str, Any]:
    if isinstance(record, CardRecord):
        record_dict = _card_record_to_dict(record)
    elif isinstance(record, Mapping):
        record_dict = dict(record)
    else:
        return {}

    if explicit_name and not _text(record_dict.get("name")):
        record_dict["name"] = explicit_name
    return record_dict


def _card_record_to_dict(card: CardRecord) -> dict[str, Any]:
    return {
        "name": card.name,
        "aliases": list(card.aliases),
        "mana_value": card.mana_value,
        "colors": list(card.colors),
        "color_identity": list(card.color_identity),
        "type_line": card.type_line,
        "oracle_text": card.oracle_text,
        "legalities": dict(card.legalities),
        "prices": dict(card.prices),
        "is_basic_land": card.is_basic_land,
        "oracle_id": card.oracle_id,
        "representative_scryfall_id": card.representative_scryfall_id,
    }


def _candidate_from_record(record: dict[str, Any], matched_name: str) -> CardFactCandidate:
    return CardFactCandidate(
        display_name=_display_name(record),
        lookup_key=normalize_lookup_key(matched_name),
        matched_name=matched_name,
        record=dict(record),
        oracle_id=_optional_text(record.get("oracle_id")),
        selected_printing_id=_optional_text(
            record.get("selected_printing_id")
            or record.get("representative_scryfall_id")
            or record.get("scryfall_id")
            or record.get("id")
        ),
    )


def _matched_names(record: dict[str, Any], explicit_name: str | None) -> tuple[str, ...]:
    names: list[str] = []
    for value in (explicit_name, record.get("name")):
        text = _text(value)
        if text:
            names.append(text)

    aliases = record.get("aliases", ())
    if isinstance(aliases, (list, tuple)):
        for alias in aliases:
            text = _text(alias)
            if text:
                names.append(text)

    return tuple(_stable_unique(names))


def _dedupe_candidates(candidates: list[CardFactCandidate]) -> list[CardFactCandidate]:
    deduped: list[CardFactCandidate] = []
    seen: set[str] = set()
    for candidate in candidates:
        identity = _candidate_identity(candidate)
        if identity not in seen:
            deduped.append(candidate)
            seen.add(identity)
    return deduped


def _candidate_identity(candidate: CardFactCandidate) -> str:
    if candidate.oracle_id:
        return f"oracle:{candidate.oracle_id}"
    if candidate.selected_printing_id:
        return f"printing:{candidate.selected_printing_id}"
    return f"name:{normalize_lookup_key(candidate.display_name)}"


def _display_name(record: Mapping[str, Any]) -> str:
    return _text(record.get("name"))


def _optional_text(value: Any) -> str | None:
    text = _text(value)
    return text or None


def _text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return text


def _stable_unique(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def _build_result_summary(
    entry: DeckEntry,
    lookup_name: str,
    status: str,
    candidates: tuple[CardFactCandidate, ...],
) -> str:
    if status == FOUND:
        return f"{entry.entry_id}: found local card facts for {candidates[0].display_name}."
    if status == AMBIGUOUS:
        return f"{entry.entry_id}: ambiguous local card facts for {lookup_name}."
    return f"{entry.entry_id}: no local card facts found for {lookup_name}."


def _build_report_summary(deck_name: str, results: tuple[CardFactLookupResult, ...]) -> str:
    found = sum(1 for result in results if result.is_found)
    missing = sum(1 for result in results if result.is_missing)
    ambiguous = sum(1 for result in results if result.is_ambiguous)
    return f"{deck_name}: {found} found, {missing} missing, {ambiguous} ambiguous card fact lookups."

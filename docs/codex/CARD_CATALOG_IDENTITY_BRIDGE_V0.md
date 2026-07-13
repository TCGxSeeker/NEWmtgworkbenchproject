# Card Catalog Identity Bridge v0

## Status

Implemented and verified.

## Purpose

Align the lightweight CardCatalog path with the repository's established Oracle-card and printing identity model without duplicating the local Scryfall index.

## Existing Architecture Preserved

This slice does not replace or modify:

- the local Scryfall SQLite schema,
- Oracle-level search,
- print-level storage,
- DeckEntry serialization,
- workspace entry identity,
- or future printing-selection UI.

The local Scryfall index remains the canonical Oracle/printing substrate.

## CardRecord Contract

CardRecord now preserves:

- `oracle_id`
- `representative_scryfall_id`

`oracle_id` identifies the canonical game object.

`representative_scryfall_id` identifies the catalog's default display printing. It is not the same as a user's selected printing.

For compatibility with existing Scryfall-derived records, `CardRecord.from_dict()` also accepts `scryfall_id` as a fallback source for `representative_scryfall_id`.

## CardCatalog Contract

Normalized names and aliases now map to all matching CardRecord objects rather than silently overwriting earlier records.

### `find_all(name)`

Returns every matching CardRecord in deterministic order.

Input construction order does not determine candidate order.

### `find(name)`

- No candidates: returns `None`.
- One logical card identity: returns the deterministic representative record.
- Multiple logical identities: raises `CardCatalogAmbiguityError`.

Logical identity is determined by:

1. `oracle_id`, when available.
2. Normalized canonical card name, when Oracle identity is unavailable.

Multiple printings sharing one `oracle_id` are one logical card identity and are not ambiguous.

## Card Fact Lookup Bridge

The catalog resolver now consumes all catalog candidates through `find_all()`.

Candidate identity is deduplicated at Oracle-card level.

Therefore:

- multiple printings of one Oracle card produce `FOUND`,
- aliases spanning different Oracle cards produce `AMBIGUOUS`,
- missing names produce `MISSING`,
- stable Oracle identity is preserved in lookup evidence,
- representative printing identity becomes default selected-printing evidence.

Card-fact lookup remains read-only and does not mutate DeckEntry.

## Determinism

Candidate ordering uses stable identity fields rather than catalog insertion order.

Equivalent catalogs built in different orders produce the same lookup result.

## Explicit Non-Goals

This slice does not:

- choose a newest or cheapest printing,
- inspect ambient SQLite files automatically,
- mutate `DeckEntry.oracle_id`,
- mutate `DeckEntry.selected_printing_id`,
- implement a printing picker,
- change workspace schemas,
- change Scryfall indexing or search,
- or create recommendation behavior.

## Verification

Regression coverage includes:

- stable identity field preservation,
- all alias candidates retained,
- ambiguity across different Oracle IDs,
- deterministic candidate ordering,
- multiple printings under one Oracle ID remaining non-ambiguous,
- catalog lookup preserving Oracle identity,
- representative printing flowing into lookup evidence,
- existing name, alias, punctuation, missing, and record-source behavior.

Full verification after implementation:

- 199 tests passed
- Python source compilation passed
- Git diff hygiene passed

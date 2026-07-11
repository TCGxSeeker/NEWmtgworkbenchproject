# Local Scryfall Syntax Search Spec

## Purpose

Define the first offline syntax-search layer for MTG Workbench. The goal is to support fast local card discovery over `data/processed/scryfall/cards.sqlite` without calling Scryfall or implementing recommendation logic.

Search is infrastructure for a future in-app search bar, card lookup, filtered browsing, and recommendation candidate pools. It is not the product's primary user experience and should not drive the near-term app design.

Long term, the in-app search function should become rich and Scryfall-like for local browsing. The Workbench itself should not become an offline Scryfall clone; deck analysis and deck understanding remain the product center.

## Supported Scope

Support this deterministic local subset:

- Bare text: search normalized card names first, then Oracle card FTS.
- `o:` or `oracle:`: search Oracle text.
- `t:` or `type:`: search type line text.
- `otag:`: resolve Oracle tags first, expand `oracle_taggings.oracle_id`, then join cards.
- `ci:` and `id:`: filter by exact color identity.
- `mv:` and `cmc:`: filter by mana value with `=`, `<`, `<=`, `>`, and `>=`.
- `legal:commander`: include cards whose local legality snapshot is legal in Commander.
- `usd<=N`: compare the local USD price snapshot numerically.
- `r:<rarity>`: filter by rarity, such as `r:mythic`.
- `set:<code>`: filter by local set code.
- `is:commander`: filter cards that the local index marked as commander candidates.

Unsupported syntax must return an explicit unsupported-feature result. Do not guess.

Implemented command:

```powershell
$env:PYTHONPATH='src'
python -m mtg_workbench.cli search "otag:burn-creature ci:r mv<=2" --index data/processed/scryfall/cards.sqlite
```

## Non-Goals

- No live Scryfall API calls.
- No broad Scryfall syntax expansion beyond the already specified Search-2 filters unless explicitly requested.
- No recommendation ranking, deck scoring, card evaluation, or strategic claims.
- No freshness claims beyond the local snapshot manifest.
- No print-level full-text search until disk budget and query needs justify it.
- No search-first app design or search-first main workflow.

## Query Planning Rules

1. Tokenize the query into supported clauses and unsupported clauses.
2. Resolve `otag:` clauses before card filters.
3. Match `otag:` by exact tag slug, exact label, or exact alias.
4. Convert tag matches to `oracle_id` sets using `oracle_taggings`.
5. Apply color identity, mana value, legality, price, rarity, set, and commander-candidate filters after tag expansion.
6. Apply Oracle text, type line, and bare text search over local indexes.
7. Intersect required clauses by default.
8. Return stable JSON with matches, applied filters, unsupported clauses, and snapshot metadata.

The current search layer treats all supported clauses as required intersections. It does not implement boolean groups, negation, regex, print-specific search, or full Scryfall syntax aliases beyond the listed subset.

Multiple syntax additions in one search are required behavior, not an advanced edge case. For example, `mv<=2 id:g t:instant` should return only green instant cards with mana value 2 or less; adding `o:draw` should further narrow those results to matching Oracle text. In a future deck-context search bar, the app may automatically apply the current deck color identity, but users must still be able to see, override, or explicitly set color filters.

## Output Contract

A search result should include:

- `query`
- `snapshot_updated_at`
- `supported_clauses`
- `unsupported_clauses`
- `result_count`
- `results`

Each result should include:

- `oracle_id`
- `name`
- `mana_value`
- `color_identity`
- `type_line`
- `oracle_text`
- `matched_terms`
- `tag_matches`

## Verification Targets

Use tiny SQLite fixtures first. Tests should cover:

- bare name search
- `o:` Oracle text search
- `t:` type line search
- tag-first `otag:` lookup
- `otag:` plus `ci:` filtering
- `mv` comparison filters
- unsupported syntax reporting
- stable JSON key ordering

Current tests live in `tests/test_scryfall_search.py` and build a tiny local SQLite fixture from local JSONL files.

## Phase Search-2 Completed Filter Contracts

Phase Search-2 implemented:

- `legal:commander`
- `usd<=N`
- `r:<rarity>`
- `set:<code>`
- `is:commander`

Additional noted future syntax, not yet implemented:

- `fo:` / `fulloracle:`: full Oracle-style text search alias for narrowing results by card text, such as `fo:draw`.

Search-2 filters use local SQLite data only and must not make freshness claims about prices or legality beyond the snapshot manifest.

## Oracle-Level And Print-Sensitive Filters

Search currently returns Oracle-level card results. Some filters are naturally Oracle-level:

- `o:` / `oracle:`
- `t:` / `type:`
- `otag:`
- `ci:` / `id:`
- `mv:` / `cmc:`
- `legal:commander`
- `is:commander`

Other filters are print-sensitive:

- `set:<code>`
- `r:<rarity>`
- `usd<=N`

Current Search-2 behavior applies those print-sensitive filters from indexed representative Oracle-card fields. That is useful for early local browsing, but it is not the final print-aware model. Future Scryfall-like local search should query `prints`, map matching Scryfall IDs back to Oracle IDs, and preserve the selected printing when set, rarity, collector number, finish, language, or price matters.

Search expansion should now pause and move toward deck understanding work unless the user explicitly asks for more search syntax. The next product priorities are:

1. Deck Skeleton Report v0.
2. Structural Warnings v0.
3. Commander Profile v0.
4. Card Seat / Role Report v0.
5. Recommendation Explanation v0.

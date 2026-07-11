# Scryfall Indexing Plan

## Purpose

Define how local Scryfall bulk snapshots become searchable offline indexes. This document is both the indexing contract and the current implementation guide.

## Core Principle

Scryfall syntax search should be modeled as local query planning over indexes, not live API calls.

Raw Scryfall payloads are source records at the ingestion boundary. MTG Workbench should derive smaller internal records for deck analysis and UI work instead of passing full Scryfall card objects everywhere.

Use Oracle-level records for canonical game-object identity and print-level records for physical or digital printing details.

For Oracle tags, process tags first:

1. Parse `otag:` or related tag syntax.
2. Search the local Oracle tag index by tag slug, label, or alias.
3. Expand matching tags into their `taggings[]`.
4. Collect tagged card `oracle_id` values and tag weights.
5. Join those `oracle_id` values to the local card index.
6. Apply remaining filters such as color identity, mana value, type, legality, price snapshot, or text search.

This mirrors why Oracle tags are stored tag-first: the tag is the search entry point, and its taggings identify the matching cards.

## Recommended Indexes

- `cards_by_oracle_id`: canonical card facts keyed by `oracle_id`.
- `prints_by_scryfall_id`: print-level card records keyed by Scryfall ID.
- `names`: normalized names and aliases to `oracle_id`.
- `oracle_text_fts`: full-text index over Oracle text.
- `type_line_fts`: full-text index over type lines.
- `legalities`: local legality snapshot fields stored on `oracle_cards`.
- `prices`: local representative price snapshot fields stored on `oracle_cards`.
- `rarity`, `set_code`, and `is_commander_candidate`: indexed Oracle-card columns for Search-2 filters.
- Print-level `prices`, `rarity`, `set_code`, collector number, language, finish, and artwork data: stored on `prints` or related print tables for future print-aware search.
- `oracle_tags`: tag slug, label, aliases, parent IDs, child IDs, description.
- `oracle_taggings`: tag slug/id to `oracle_id` plus weight.
- `art_tags`: art tag slug, label, aliases, and taggings where useful.

## Phase Index-1 Implementation

Build `data/processed/scryfall/cards.sqlite` from local files only:

```powershell
$env:PYTHONPATH='src'
python -m mtg_workbench.cli index-scryfall --raw-dir data/raw/scryfall --output data/processed/scryfall/cards.sqlite
```

The indexer should read:

- `manifest.json`
- `oracle_cards/*.jsonl.gz`
- `default_cards/*.jsonl.gz`
- `all_cards/*.jsonl.gz`
- `unique_artwork/*.jsonl.gz`
- `rulings/*.jsonl.gz`
- `oracle_tags/*.jsonl.gz`
- `art_tags/*.jsonl.gz`

Large generated SQLite files remain ignored by Git. `data/processed/scryfall/index_manifest.json` records counts, source snapshot paths, and source timestamps.

## Search Planner Notes

- See `docs/rules/SCRYFALL_SYNTAX_SEARCH.md` for the supported syntax subset.
- Free text should search names first.
- `o:` / `oracle:` should search Oracle text.
- `t:` / `type:` should search type line tokens.
- `otag:` should search the Oracle tag index before card filters.
- `art:` should search art tags before card filters.
- `ci:` / `id:` should filter card color identity.
- `mv:` / `cmc:` should filter numeric mana value.
- `legal:commander` should filter the local Commander legality snapshot only.
- `usd<=N` should filter the local representative USD price snapshot only until print-aware search is implemented.
- `r:<rarity>` and `set:<code>` currently filter indexed local Oracle-card columns; future print-aware search should query `prints` and map matching Scryfall IDs back to Oracle IDs.
- `is:commander` should filter the local commander-candidate marker.
- Unsupported syntax should fail with an explicit unsupported-feature result, not a guessed interpretation.

## SQLite Tables

- `bulk_sources`: source bulk type, local path, updated timestamp, SHA-256, and byte counts.
- `oracle_cards`: oracle-level card facts.
- `prints`: print-level rows from `default_cards` and `all_cards`, with `source_type`.
- `unique_artwork`: artwork-focused print rows keyed by Scryfall ID and illustration ID.
- `names`: normalized names and aliases to `oracle_id`.
- `rulings`: local rulings keyed by `oracle_id`.
- `oracle_tags`: Oracle tag metadata.
- `oracle_taggings`: Oracle tag to `oracle_id` relationships plus weight.
- `art_tags`: art tag metadata.
- `art_taggings`: art tag to illustration relationships plus weight.
- `oracle_cards_fts`: FTS over names, type lines, Oracle text, keywords, and tag text.
- Print rows should remain compact. Use `prints` indexes and the `names` table for print lookups; defer print-level FTS until disk budget and actual query needs justify it.
- `oracle_tags_fts`: FTS over Oracle tag slug, label, aliases, and description.
- `art_tags_fts`: FTS over art tag slug, label, aliases, and description.

## Gotchas

- Do not treat Oracle tags as merely a tag vocabulary.
- Do not attach tags to cards by name; use `oracle_id`.
- Do not call Scryfall during search.
- Do not use tag matches as automatic recommendation authority.
- Do not apply color, mana value, or legality filters before expanding tag searches unless the query planner can prove the result is equivalent.
- Do not require a live API call to search.
- Do not commit generated SQLite indexes.
- Do not treat print-sensitive filters such as set, rarity, collector number, finish, language, or price as final Oracle-level facts.

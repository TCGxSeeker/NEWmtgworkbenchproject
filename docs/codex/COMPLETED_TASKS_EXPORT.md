# Completed Tasks Export

> Historical export snapshot. Do not treat test counts, latest-next-step wording, or current-status claims below as authoritative. Current baseline and next repairs live in `docs/codex/NEXT_SESSION_HANDOFF.md`, `.tasks/NEXT_PROJECT.md`, and `README.md`.

## Project Operating Structure

- Created the project-local Codex structure: `AGENTS.md`, `docs/codex/`, `.tasks/`, and `.agents/skills/`.
  - What this means: The project now has its own operating rules, planning docs, task notes, and reusable Codex workflows. This keeps the MTG Workbench separated from other projects and reduces overlap errors.

## Product Direction

- Captured the core project brief for an offline-first MTG deckbuilder workbench.
  - What this means: The project is aimed at deck import, storage, analysis, reporting, and eventually recommendation drafting. The current direction avoids live-service dependency, popularity-driven ranking, and autonomous final deck decisions.

## Implementation Planning

- Wrote and updated `docs/codex/IMPLEMENTATION_SPEC.md`, `VERIFICATION_PLAN.md`, `HUMAN_VALIDATION_ZONES.md`, `DECISION_LOG.md`, and `GOTCHAS.md`.
  - What this means: Major work now starts with a spec and verification path before code. Risks, assumptions, decisions, and corrections are recorded instead of living only in chat.

## Seed Sources And Data Contracts

- Added MTG philosophy, rules, role taxonomy, budget, gotcha, and master seed source documents.
  - What this means: The project has a doctrine layer for how deckbuilding should be evaluated. These are reference sources, not card databases or decklists.

- Created `docs/rules/DATA_CONTRACTS.md` and tiny raw fixtures for cards, decklists, ownership, commander profiles, roles, packages, templates, budget, reports, and validation triggers.
  - What this means: The project has local fixture formats to build against before importing real curated data. This helps keep future behavior deterministic and testable.

## Decklist Parser And Normalizer

- Implemented a Python CLI package under `src/mtg_workbench/`.
  - What this means: The project now has executable local code, not just planning docs. Python CLI is the current MVP runtime.

- Added decklist parsing for plain text and CSV fixtures.
  - What this means: The tool can read simple decklists, preserve quantities, and separate commander, mainboard, and maybeboard entries when marked.

- Added card-name normalization against a tiny local card snapshot.
  - What this means: Names are normalized deterministically using local data only, including case-insensitive lookup and aliases. Unknown cards are reported instead of guessed.

- Added duplicate non-basic warnings.
  - What this means: Duplicate known non-basic cards are visible as validation warnings, not hard parser failures yet. This preserves useful parser output for later audit stages.

## Scryfall Snapshot Storage

- Created `data/raw/scryfall/` storage locations and downloaded local Scryfall bulk snapshots.
  - What this means: The project has local raw source data for cards, prints, rulings, Oracle tags, and art tags. Runtime behavior can stay offline instead of repeatedly calling external APIs.

- Added `.gitignore` rules for large raw payloads and generated indexes.
  - What this means: Large local data stays on the machine but out of Git. The tracked repo keeps manifests and docs rather than multi-hundred-megabyte payloads.

## Local Scryfall SQLite Index

- Built a compact SQLite indexer for local Scryfall snapshots.
  - What this means: The project can convert local bulk data into `data/processed/scryfall/cards.sqlite` for fast offline lookup. The index includes cards, prints, names, rulings, Oracle tags, Oracle taggings, art tags, and artwork links.

- Generated `data/processed/scryfall/index_manifest.json`.
  - What this means: The generated index records source snapshot paths, timestamps, and counts for reproducibility. This helps avoid pretending stale local data is fresh.

- Documented the tag-first Oracle tag search model.
  - What this means: `otag:` searches should resolve tags first, expand taggings through `oracle_id`, then apply card filters. This matches how Scryfall Oracle tags are actually structured.

## Local Syntax Search

- Wrote `docs/rules/SCRYFALL_SYNTAX_SEARCH.md`.
  - What this means: The first local search subset is defined before expanding the engine. Supported syntax is deliberately narrow and unsupported syntax must be reported, not guessed.

- Implemented a read-only `search` CLI command over the local SQLite index.
  - What this means: The tool can now perform local searches such as `otag:burn-creature ci:r mv<=2` without calling Scryfall. It supports bare text, `o:`, `t:`, `otag:`, `ci/id`, and `mv/cmc` comparisons.

- Added tests for local syntax search behavior.
  - What this means: Search behavior is covered by tiny local SQLite fixtures. Tests verify name search, Oracle text search, type search, tag-first lookup, filtering, stable JSON, and unsupported syntax reporting.

## Search-2 Filters

- Implemented the Search-2 filters for `legal:commander`, `usd<=N`, `r:<rarity>`, `set:<code>`, and `is:commander`.
  - What this means: Local search can now narrow results by Commander legality, local USD snapshot price, rarity, set code, and commander-candidate status. These filters still use local SQLite only and make no live freshness claims.

- Removed expected-failure status from the Search-2 tests.
  - What this means: Search-2 behavior is now required to pass in the normal unit suite instead of being documented as future work.

## Search Scope Reframe

- Reframed local search as infrastructure, not the primary product experience.
  - What this means: Search should still become strong enough for the in-app search bar and future candidate discovery, but this project should not become an offline Scryfall clone. After Search-2, the priority moves toward deck understanding.

- Set the next product priorities after Search-2.
  - What this means: The next work should move toward Deck Skeleton Report v0, Structural Warnings v0, Commander Profile v0, Card Seat / Role Report v0, and Recommendation Explanation v0. Search UI should not outrank deck audit/report generation.

## Verification

- Ran the unit test suite repeatedly as features were added.
  - What this means: At this historical snapshot, the suite passed normally with 25 tests and 0 expected failures. The current suite count is tracked in `docs/codex/NEXT_SESSION_HANDOFF.md`.

- Ran real local smoke checks against the generated Scryfall SQLite index.
  - What this means: The local search command works against the full local snapshot index, not only tiny fixtures. Generated large files remain ignored by Git.

## Free Frontend Tooling Scaffold

- Added an isolated Vite, React, and TypeScript scaffold under `apps/deckbuilder-ui/`.
  - What this means: Future UI experiments have free local tooling available, but the real deckbuilder UI has not been implemented yet.

## Design Gotchas Captured

- Recorded that the eventual UI must not become a cluttered feature collage.
  - What this means: The app can have many capabilities, but the finished interface should be calm, elegant, paced, and readable. Future UI work should not copy the dense mock preview style.

## Current Practical Status

- The project has a working local parser, normalizer, Scryfall indexer, Search-2 local syntax filters, and frontend tooling scaffold.
  - What this means: The foundation for offline card lookup and decklist ingestion exists. The project is not yet a full deckbuilder, audit engine, recommendation engine, or finished UI.

- The clean next implementation target is Deck Skeleton Report v0.
  - What this means: The next useful move is making the tool summarize actual deck shape instead of expanding search syntax further.

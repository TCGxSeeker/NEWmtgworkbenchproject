# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current head: `5c45b2c Define visual card pair comparison`
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 296 tests
- Current product center remains the deckbuilder foundation and deterministic local analysis pipeline

## Current Catchup

Steps 1-4 are complete in the current working tree unless already committed. The next catchup repair should harden local Scryfall index path portability and rebuild atomicity before new feature work.

## Next Recommended Slice

Step 5: Scryfall Index Portability and Atomicity Patch.

Goal: close the remaining local Scryfall index reliability gaps found by audit: make moved-repo local-path resolution robust and protect database/manifest consistency if rebuild fails after a database replacement point.

Expected scope:

1. Inspect `src/mtg_workbench/scryfall/indexer.py`, `tests/test_scryfall_indexer.py`, and `docs/codex/ATOMIC_LOCAL_PERSISTENCE_V0.md`.
2. Make manifest `local_path` resolution robust after repository moves.
3. Avoid cwd-dependent path ambiguity where practical.
4. Harden rebuild atomicity so SQLite DB and manifest stay consistent on partial failure.
5. Keep all behavior local, deterministic, and offline.

## Boundaries

- Do not implement package detection.
- Do not implement synergy scoring.
- Do not compare every card against every other card.
- Do not add deck-level role totals.
- Do not add recommendations, candidate search, add/cut scoring, UI, live APIs, telemetry, hosted services, or AI/LLM calls.
- Do not make strategic quality judgments.
- Do not guess when card facts are unavailable.

## Human Checkpoint

Deck Role Summary v0 still requires explicit approval because it starts deck-level role counting.

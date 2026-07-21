# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: Deck Inspection CLI v0
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 303 tests
- Current product center remains the deckbuilder foundation and deterministic local analysis pipeline

## Current Catchup

Steps 1-6 are complete, origin/master was caught up through Step 6, and Deck Inspection CLI v0 is implemented locally. No active numbered catchup repair remains after Step 6.

## Next Recommended Slice

Native Workspace Import/Export CLI v0.

Goal: expose existing native workspace import/export helpers through tiny CLI commands so deck files can move between plain text and `.mtgwdeck.json` without app UI.

Expected scope:

1. Update `docs/codex/IMPLEMENTATION_SPEC.md` before coding.
2. Inspect `src/mtg_workbench/deckbuilder/import_export.py`.
3. Add minimal CLI commands only if they wrap existing import/export behavior.
4. Add tests against tiny fixtures.
5. Do not add UI, strategic analysis, recommendations, live APIs, or new dependencies.

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

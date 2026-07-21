# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: color identity workspace projection bundle
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 343 tests
- Current product center remains the deckbuilder foundation and deterministic local analysis pipeline

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, Entry Annotation CLI v0, Deck Workspace View Projection v0, Workspace View CLI v0, Card-Fact-Backed Workspace Projection v0, and Color Identity Workspace Projection v0 are implemented and verified.

## Next Recommended Slice

Workspace View Fixture Smoke v0.

Goal: create a tiny deterministic expected-output fixture for `workspace-view` so future grouping/sorting/filtering changes are caught intentionally before UI work.

Expected scope:

1. Update `docs/codex/IMPLEMENTATION_SPEC.md` before coding.
2. Reuse or create tiny workspace/card-record fixtures under `tests/fixtures/deckbuilder/`.
3. Generate one stable expected JSON fixture for fact-backed `workspace-view`.
4. Add a test that compares the exact projection payload to the expected fixture.
5. Prove repeat-run determinism and no workspace mutation.
6. Do not add UI, strategic analysis, recommendations, live APIs, deck-level role totals, syntax filtering, price logic, or new dependencies.

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

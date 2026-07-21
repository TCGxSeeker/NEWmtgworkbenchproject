# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: card-fact-backed workspace projection bundle
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 340 tests
- Current product center remains the deckbuilder foundation and deterministic local analysis pipeline

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, Entry Annotation CLI v0, Deck Workspace View Projection v0, Workspace View CLI v0, and Card-Fact-Backed Workspace Projection v0 are implemented and verified.

## Next Recommended Slice

Color Identity Workspace Projection v0.

Goal: expand read-only workspace projection to use explicitly supplied local card facts for factual color and color-identity grouping/sorting without deck analysis or guessing.

Expected scope:

1. Update `docs/codex/IMPLEMENTATION_SPEC.md` before coding.
2. Inspect `workspace_view.py`, card fact lookup behavior, and group/sort/filter requirements.
3. Use only explicitly supplied local card records or existing local catalog data.
4. Add color and color-identity grouping/sorting only when local facts are found.
5. Keep missing/ambiguous facts visible instead of guessed.
6. Add tests against tiny fixtures.
7. Do not add UI, strategic analysis, recommendations, live APIs, deck-level role totals, syntax filtering, price logic, or new dependencies.

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

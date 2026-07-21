# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: category metadata and entry annotation CLI bundle
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 322 tests
- Current product center remains the deckbuilder foundation and deterministic local analysis pipeline

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, and Entry Annotation CLI v0 are implemented and verified.

## Next Recommended Slice

Deck Workspace View Projection v0.

Goal: create a read-only projection layer that prepares native workspace entries for future deckbuilder grouping, sorting, and current-deck filtering without app UI.

Expected scope:

1. Update `docs/codex/IMPLEMENTATION_SPEC.md` before coding.
2. Inspect deckbuilder view-mode/group/sort/filter docs.
3. Add a small read-only module that groups by existing workspace fields such as zone, category, and full deck.
4. Add deterministic sorting by alphabet, quantity, and current category fields where data already exists.
5. Add simple current-deck text filtering over entry names and tags only.
6. Add tests against tiny in-memory workspaces.
7. Do not add UI, strategic analysis, recommendations, live APIs, deck-level role totals, or new dependencies.

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

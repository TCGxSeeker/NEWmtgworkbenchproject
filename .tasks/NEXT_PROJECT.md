# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: Workspace Projection Contract Docs v0
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 344 tests
- Current product center remains the deckbuilder foundation. Canonical framing:
  this is a strong backend foundation with CLI-verifiable contracts, not generic
  deckbuilder parity as a user-facing product yet.

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, Entry Annotation CLI v0, Deck Workspace View Projection v0, Workspace View CLI v0, Card-Fact-Backed Workspace Projection v0, Color Identity Workspace Projection v0, Workspace View Fixture Smoke v0, and Workspace Projection Contract Docs v0 are implemented and verified.

## Next Recommended Slice

See The Deck v0.

Goal: create the first narrow visible-deck milestone from the existing projection contract, or write its implementation spec if the user wants one more planning checkpoint first.

Context: `deck_workspace_view_projection.v0` is now documented as the contract
future UI should consume.

Expected scope:

1. Update `docs/codex/IMPLEMENTATION_SPEC.md` before editing.
2. Keep the first screen centered on opening and seeing a saved deck.
3. Use only the documented projection contract and existing backend behavior.
4. Show deck rows, group/sort/filter state, and basic deck actions only.
5. Do not surface local fact coverage as normal dashboard content.
6. Do not add strategic analysis, recommendations, live APIs, deck-level role totals, price logic, or new dependencies.

## Boundaries

- Do not implement package detection.
- Do not implement synergy scoring.
- Do not compare every card against every other card.
- Do not add deck-level role totals.
- Do not add recommendations, candidate search, add/cut scoring, UI, live APIs, telemetry, hosted services, or AI/LLM calls.
- Do not make strategic quality judgments.
- Do not guess when card facts are unavailable.
- Do not describe planned/contracted UI capabilities as implemented parity.
- Do not treat safe workspace deletion as complete until a tested helper or command exists.

## Human Checkpoint

Deck Role Summary v0 still requires explicit approval because it starts deck-level role counting.

## Product North Star

1. See the deck.
2. Find and add cards.
3. Understand a card.
4. Validate the deck.
5. Edit safely in bulk.
6. Inspect useful statistics.
7. Manage printings.
8. Recover earlier versions.

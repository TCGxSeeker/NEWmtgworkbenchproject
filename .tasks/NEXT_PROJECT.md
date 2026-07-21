# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: See The Deck v0 Visual Review Checkpoint
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 344 tests
- Current product center remains the deckbuilder foundation. Canonical framing:
  this is a strong backend foundation with CLI-verifiable contracts, not generic
  deckbuilder parity as a user-facing product yet.

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, Entry Annotation CLI v0, Deck Workspace View Projection v0, Workspace View CLI v0, Card-Fact-Backed Workspace Projection v0, Color Identity Workspace Projection v0, Workspace View Fixture Smoke v0, Workspace Projection Contract Docs v0, See The Deck v0, and the See The Deck v0 Visual Review Checkpoint are implemented and verified.

## Next Recommended Slice

Find And Add Cards v0.

Goal: add the smallest explicit search/add workflow around the existing visible deck screen without recommendations, scoring, strategy, or broad syntax expansion.

Context: `See The Deck v0` now renders a calm, fixture-backed deck view. The next product north-star step is finding and adding cards.

Expected scope:

1. Define or refresh the implementation spec before coding.
2. Use local fixture/index data only.
3. Add a minimal card search entry point that returns deterministic local results.
4. Add an explicit add-card path only for user-selected cards.
5. Preserve native workspace mutation safety boundaries and copy-out behavior unless a UI-local temporary state is clearly isolated.
6. Keep unsupported syntax clear instead of guessed.
7. Do not add strategic analysis, recommendations, live APIs, deck-level role totals, price logic, or new dependencies.

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

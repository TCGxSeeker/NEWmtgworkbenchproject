# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: See The Deck v0
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 344 tests
- Current product center remains the deckbuilder foundation. Canonical framing:
  this is a strong backend foundation with CLI-verifiable contracts, not generic
  deckbuilder parity as a user-facing product yet.

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, Entry Annotation CLI v0, Deck Workspace View Projection v0, Workspace View CLI v0, Card-Fact-Backed Workspace Projection v0, Color Identity Workspace Projection v0, Workspace View Fixture Smoke v0, Workspace Projection Contract Docs v0, and See The Deck v0 are implemented and verified.

## Next Recommended Slice

See The Deck v0 Visual Review Checkpoint.

Goal: review the first visible deck screen for readability, spacing, visual feel, and whether it avoids useless/debug data before adding search/add workflows.

Context: `See The Deck v0` exists, but UI taste is a human validation zone.

Expected scope:

1. Open the local dev server.
2. Review desktop and narrow layouts.
3. Confirm the screen feels calm, readable, and deck-centered.
4. Confirm no inactive action buttons or debug metrics are displayed.
5. Capture any requested visual changes before moving to `Find And Add Cards v0`.
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

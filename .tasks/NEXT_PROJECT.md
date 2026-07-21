# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: Find And Add Cards v0
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 344 tests
- Current product center remains the deckbuilder foundation. Canonical framing:
  this is a strong backend foundation with CLI-verifiable contracts, not generic
  deckbuilder parity as a user-facing product yet.

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, Entry Annotation CLI v0, Deck Workspace View Projection v0, Workspace View CLI v0, Card-Fact-Backed Workspace Projection v0, Color Identity Workspace Projection v0, Workspace View Fixture Smoke v0, Workspace Projection Contract Docs v0, See The Deck v0, See The Deck v0 Visual Review Checkpoint, and Find And Add Cards v0 are implemented and verified.

## Next Recommended Slice

Card Details Surface v0.

Goal: add the smallest selected-card details surface around the existing visible deck screen without recommendations, scoring, strategy, pricing, or legality claims.

Context: `Find And Add Cards v0` lets the user search a tiny local fixture and add explicitly selected cards to visible UI state. The next product north-star step is understanding a card.

Expected scope:

1. Define or refresh the implementation spec before coding.
2. Use visible deck entry data and tiny local card fixture data only.
3. Open details from an explicitly selected deck row or search result.
4. Show only factual fields already available in local UI data.
5. Preserve the current deck view, filter, and add-card state while details are open.
6. Keep details progressive and uncluttered.
7. Do not add strategic analysis, recommendations, live APIs, deck-level role totals, price logic, legality claims, or new dependencies.

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

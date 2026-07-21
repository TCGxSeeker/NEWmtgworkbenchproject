# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: Deckbuilder UI Logic Extraction v0
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 344 tests
- Current product center remains the deckbuilder foundation. Canonical framing:
  this is a strong backend foundation with CLI-verifiable contracts, not generic
  deckbuilder parity as a user-facing product yet.

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, Entry Annotation CLI v0, Deck Workspace View Projection v0, Workspace View CLI v0, Card-Fact-Backed Workspace Projection v0, Color Identity Workspace Projection v0, Workspace View Fixture Smoke v0, Workspace Projection Contract Docs v0, See The Deck v0, See The Deck v0 Visual Review Checkpoint, Find And Add Cards v0, Card Details Surface v0, Mechanical Deck Validation Surface v0, and Deckbuilder UI Logic Extraction v0 are implemented and verified.

## Next Recommended Slice

Mechanical Deckbuilder UI Human Review Checkpoint, then Save/Load Workspace UI v0 or backend-to-UI validation wiring.

Goal: review the current fixture-backed deckbuilder UI in-browser for layout/readability, then choose the next small step toward durable deck editing or richer factual validation.

Context: the current UI can see the deck, find/add fixture cards, open factual details, and show compact mechanical validation from UI state. Visual/taste review remains a human validation zone.

Expected scope:

1. Review the details and mechanical validation surfaces in the browser before broadening visible UI.
2. Keep any visual patch small and taste-reviewable.
3. If visual pass is accepted, choose Save/Load Workspace UI v0 or backend-to-UI validation wiring as the next implementation slice.
4. Keep validation factual/mechanical and avoid recommendations, scoring, power-level claims, and strategic judgments.
5. Do not add live APIs, deck-level role totals, price logic, legality claims, or new dependencies without a fresh approved slice.

## Boundaries

- Do not implement package detection.
- Do not implement synergy scoring.
- Do not compare every card against every other card.
- Do not add deck-level role totals.
- Do not add recommendations, candidate search, add/cut scoring, broad unapproved UI, live APIs, telemetry, hosted services, or AI/LLM calls.
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

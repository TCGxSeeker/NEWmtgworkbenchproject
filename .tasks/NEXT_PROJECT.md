# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: User Reviewer Skill v0
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 344 tests
- Current product center remains the deckbuilder foundation. Canonical framing:
  this is a strong backend foundation with CLI-verifiable contracts, not generic
  deckbuilder parity as a user-facing product yet.

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, Entry Annotation CLI v0, Deck Workspace View Projection v0, Workspace View CLI v0, Card-Fact-Backed Workspace Projection v0, Color Identity Workspace Projection v0, Workspace View Fixture Smoke v0, Workspace Projection Contract Docs v0, See The Deck v0, See The Deck v0 Visual Review Checkpoint, Find And Add Cards v0, Card Details Surface v0, Mechanical Deck Validation Surface v0, Deckbuilder UI Logic Extraction v0, and User Reviewer Skill v0 are implemented and verified.

## Next Recommended Slice

Run User Reviewer on the current deckbuilder UI, then Mechanical Deckbuilder UI Human Review Checkpoint.

Goal: use the structured rubric to review the current fixture-backed deckbuilder UI for clarity, calmness, usefulness, hierarchy, and clutter before building more visible surfaces.

Context: the current UI can see the deck, find/add fixture cards, open factual details, and show compact mechanical validation from UI state. The user-reviewer skill provides a repeatable review format, but visual/taste review remains a human validation zone.

Expected scope:

1. Run the `user-reviewer` skill against the current deckbuilder UI.
2. Review the details and mechanical validation surfaces in the browser before broadening visible UI.
3. Keep any visual patch small and taste-reviewable.
4. If visual pass is accepted, choose Save/Load Workspace UI v0 or backend-to-UI validation wiring as the next implementation slice.
5. Keep validation factual/mechanical and avoid recommendations, scoring, power-level claims, and strategic judgments.

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

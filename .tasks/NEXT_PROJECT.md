# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: Deck Library, Context Consolidation, and Save/Open UI v0
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 344 tests
- Current product center remains the deckbuilder foundation. Canonical framing:
  this is a strong backend foundation with CLI-verifiable contracts, not generic
  deckbuilder parity as a user-facing product yet.

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, Entry Annotation CLI v0, Deck Workspace View Projection v0, Workspace View CLI v0, Card-Fact-Backed Workspace Projection v0, Color Identity Workspace Projection v0, Workspace View Fixture Smoke v0, Workspace Projection Contract Docs v0, See The Deck v0, See The Deck v0 Visual Review Checkpoint, Find And Add Cards v0, Card Details Surface v0, Mechanical Deck Validation Surface v0, Deckbuilder UI Logic Extraction v0, User Reviewer Skill v0, Current Deckbuilder UI User Review v0, Current Deckbuilder UI Human Browser Pass v0, and Deck Library, Context Consolidation, and Save/Open UI v0 are implemented and verified.

## Next Recommended Slice

Deck Library and Save/Open Human Browser Pass v0.

Goal: manually review the new browser-local app flow before adding more visible deckbuilder controls.

Context: the app now opens to a deck library, can create in-browser local decks, can open native `.mtgwdeck.json` files through a file picker, can download the current workspace as native JSON, and keeps the deck workspace centered with context below the card area.

Expected scope:

1. Review library first impression, create-deck flow, open-file flow, save/download flow, add-card responsiveness, and deck-context organization.
2. Confirm maybeboard default collapse, hidden non-actionable checks, card details without `Zone`, and safer two-character search trigger.
3. Record human feedback before starting visible remove-card controls, quantity editing, report wiring, or further visual polish.

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

# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: Current Deckbuilder UI Human Browser Pass v0
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 344 tests
- Current product center remains the deckbuilder foundation. Canonical framing:
  this is a strong backend foundation with CLI-verifiable contracts, not generic
  deckbuilder parity as a user-facing product yet.

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, Entry Annotation CLI v0, Deck Workspace View Projection v0, Workspace View CLI v0, Card-Fact-Backed Workspace Projection v0, Color Identity Workspace Projection v0, Workspace View Fixture Smoke v0, Workspace Projection Contract Docs v0, See The Deck v0, See The Deck v0 Visual Review Checkpoint, Find And Add Cards v0, Card Details Surface v0, Mechanical Deck Validation Surface v0, Deckbuilder UI Logic Extraction v0, User Reviewer Skill v0, Current Deckbuilder UI User Review v0, and Current Deckbuilder UI Human Browser Pass v0 are implemented and verified.

## Next Recommended Slice

Deck Library Entry Planning v0, then Deck Context Consolidation v0.

Goal: first capture the deck library as the app home surface, then make a small polish pass on open-deck organization without changing the working feature scope.

Context: the human browser pass accepted the function direction but rejected the current visual quality as final. The user also clarified that MTG Workbench should have a full deck library/home screen before the individual deck screen, using the local proxy utility as a calm but expressive style-feel reference only. After that planning is captured, the deck polish should reduce side-area competition, move snapshot/stats-style information lower or out of the cramped deck area, collapse maybeboard by default, remove non-actionable checks from default UI, and prevent future full-cardpool search from firing on noisy one-character input.

Expected scope:

1. Keep the deck library work to planning or a separately approved small entry-surface slice.
2. Keep open-deck polish limited to organization and default visibility.
3. Preserve current working add/search/details/count-update behavior.
4. Preserve the open deck as the primary editing workspace and keep add-card collapsible.
5. Hide successful background checks such as names resolved and no-duplicate singleton status.
6. Do not implement save/load, backend report wiring, recommendations, scoring, power-level claims, or strategic judgments in this polish slice.

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

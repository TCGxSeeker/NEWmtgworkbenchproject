# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current head: `df46b33 Repair catchup foundation contracts`
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 298 tests
- Current product center remains the deckbuilder foundation and deterministic local analysis pipeline

## Current Catchup

Steps 1-4 are committed. Step 5 is complete in the current working tree unless already committed. The next catchup repair should clarify visual compare source-target direction before new feature work.

## Next Recommended Slice

Step 6: Visual Compare Direction Decision.

Goal: clarify how a future `Inspect interaction` action chooses source and target direction. Current code inspects source-to-target only, and tests correctly lock that reverse direction is not automatic.

Expected scope:

1. Inspect `docs/product/deckbuilder/VISUAL_CARD_PAIR_COMPARE_V0.md`.
2. Inspect relationship and card-record pair inspection tests for current directionality.
3. Document whether UI chooses source first, prompts for direction, or offers explicit reverse inspection later.
4. Keep automatic reverse-direction analysis out unless explicitly approved.
5. Do not implement UI code.

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

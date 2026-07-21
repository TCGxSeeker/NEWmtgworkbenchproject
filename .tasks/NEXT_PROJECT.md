# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Last committed repair checkpoint before Step 6: `7f67e40 Harden Scryfall index persistence`
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 298 tests
- Current product center remains the deckbuilder foundation and deterministic local analysis pipeline

## Current Catchup

Steps 1-5 are committed. Step 6 visual compare direction docs are complete. No active numbered catchup repair remains after Step 6.

## Next Recommended Slice

Readiness Checkpoint After Catchup Repairs.

Goal: review the completed catchup repair queue, commit Step 6, and choose the next bounded implementation slice only after confirming the foundation remains aligned.

Expected scope:

1. Confirm Step 6 docs are committed.
2. Run `python -m unittest discover -s tests`.
3. Run `git diff --check`.
4. Review whether the next slice should be documentation, CLI/report output, or another bounded backend foundation.
5. Do not start app UI code without a fresh implementation handoff.

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

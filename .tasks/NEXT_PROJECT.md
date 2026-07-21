# Next Project

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Branch: `master`
- Current implemented checkpoint: Workspace View Fixture Smoke v0
- Current full-suite baseline: `python -m unittest discover -s tests` passes with 344 tests
- Current product center remains the deckbuilder foundation. Canonical framing:
  this is a strong backend foundation with CLI-verifiable contracts, not generic
  deckbuilder parity as a user-facing product yet.

## Current Catchup

Steps 1-6 are complete. Deck Inspection CLI v0, Native Workspace Import/Export CLI v0, Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, Deck Inspection CLI polish, Category Metadata Mutation CLI v0, Entry Annotation CLI v0, Deck Workspace View Projection v0, Workspace View CLI v0, Card-Fact-Backed Workspace Projection v0, Color Identity Workspace Projection v0, and Workspace View Fixture Smoke v0 are implemented and verified.

## Next Recommended Slice

Workspace Projection Contract Docs v0.

Goal: document the `deck_workspace_view_projection.v0` payload as a consumer-facing contract before future UI or syntax-filter work depends on it.

Context: this is groundwork for the first visible-deck milestone, not an
analysis or recommendation slice.

Expected scope:

1. Update `docs/codex/IMPLEMENTATION_SPEC.md` before editing.
2. Create or update a concise product/rules contract doc for workspace-view projection output.
3. Describe group totals, multi-membership groups, fact status buckets, and current deferred fields.
4. Reference the exact smoke fixture as the current executable contract example.
5. Do not add UI, strategic analysis, recommendations, live APIs, deck-level role totals, syntax filtering, price logic, or new dependencies.

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

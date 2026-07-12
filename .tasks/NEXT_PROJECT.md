# Next Project

## Current Baseline

- Branch: `master`
- Latest milestone: Card Relationship Primitives Plan v0
- Current test baseline: `python -m unittest discover -s tests` passes with 183 tests
- Current product center remains the deckbuilder foundation and deterministic local analysis pipeline

## Next Recommended Slice

Typed Card Relationship Primitive Models v0.

Goal: load and validate `data/fixtures/relationships/card_relationship_primitives.example.json` as typed local objects without deriving relationship edges or making strategic judgments.

Expected scope:

1. Add small model/loader module for the relationship vocabulary.
2. Validate schema version, unique vocabulary values, confidence bands, evidence fields, relationship types, deferred types, and non-goals.
3. Add focused tests around the loader/model behavior.
4. Keep the fixture tiny and local.

## Boundaries

- Do not implement relationship-edge derivation yet.
- Do not implement package detection.
- Do not implement synergy scoring.
- Do not compare every card against every other card.
- Do not add deck-level role totals.
- Do not add recommendations, candidate search, add/cut scoring, UI, live APIs, telemetry, hosted services, or AI/LLM calls.

## Human Checkpoint

Deck Role Summary v0 requires explicit approval because it starts deck-level role counting.

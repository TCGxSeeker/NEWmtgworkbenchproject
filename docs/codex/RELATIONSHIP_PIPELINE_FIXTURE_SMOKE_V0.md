# Relationship Pipeline Fixture Smoke v0

## Status

Implemented and verified.

## Purpose

Prove one small deterministic end-to-end relationship pipeline using synthetic,
local fixture data.

The smoke path demonstrates:

- local fixture records
- bounded behavioral-profile extraction
- explicit profile construction for unsupported fixture-only behaviors
- explicit source-target pair derivation
- factual relationship reporting
- exact expected-output comparison

## Covered relationship types

The fixture proves:

- `supplies`
- `triggers`

## Fixture boundaries

The fixture uses synthetic cards and explicit entry identifiers.

It does not use a real deck as an architectural authority.

The pipeline only derives relationships for declared source-target pairs.
It does not perform all-pairs comparison or candidate discovery.

## Extraction boundary

The smoke fixture uses the bounded extractor where current support exists.

Behaviors outside the extractor's current vocabulary are represented through
explicit factual behavioral profiles rather than guessed or silently inferred.

This includes:

- Treasure consumption
- discard-event observation

## Deterministic behavior

The smoke pipeline verifies:

- stable serialized output
- repeat-run equality
- stable relationship ordering
- stable evidence ordering
- stable relationship-type counts
- source fixture immutability
- unsupported Oracle text producing no behavioral atoms

## Non-goals

This slice does not add:

- deck-wide relationship orchestration
- all-pairs scanning
- candidate discovery
- graph traversal
- package detection
- combo solving
- synergy scoring
- recommendation logic
- card-quality judgments
- commander analysis
- user-interface behavior

## Verification

Added six focused tests covering:

- exact expected-output comparison
- repeat-run determinism
- source-fixture immutability
- unsupported-record behavior
- declared-pair boundaries
- agreement between direct pipeline components

The full test suite passes with 249 tests.

# Explicit Relationship Pair Inspection v0

## Status

Implemented and verified.

## Purpose

Provide a small deterministic orchestration boundary for inspecting one
explicitly requested directional pair of deck-entry behavioral profiles.

## Public boundary

`inspect_relationship_pair(...)` accepts:

- one source deck-entry identifier
- one target deck-entry identifier
- an explicit mapping of entry identifiers to CardBehavioralProfile values

It returns the existing CardRelationshipReport contract.

## Behavior

The inspection boundary:

- validates source and target identifiers
- normalizes surrounding identifier whitespace
- requires two different deck entries
- requires a mapping of resolved behavioral profiles
- resolves only the explicitly requested source and target profiles
- rejects missing profiles clearly
- rejects invalid resolved profile values
- derives only source-to-target relationships
- returns an empty factual report when no supported exact match exists
- does not mutate the provided mapping

## Supported relationship derivation

This slice delegates to the existing bounded relationship derivation rules:

- exact resource output matching an exact target cost produces `supplies`
- exact emitted event matching an exact observed event produces `triggers`

No additional relationship vocabulary or inference rules were added.

## Boundaries

This slice does not perform:

- card-record lookup
- behavioral-profile extraction
- deck-wide scanning
- automatic reverse-direction inspection
- all-pairs comparison
- graph traversal
- package detection
- combo solving
- synergy scoring
- recommendations
- strategic quality judgments
- commander analysis
- network access
- user-interface behavior

## Verification

Focused tests cover:

- successful explicit pair inspection
- empty no-match reporting
- strict source-to-target directionality
- missing source and target profiles
- same-entry rejection
- non-string and empty identifier rejection
- identifier normalization
- non-mapping input rejection
- invalid resolved profile values
- mapping immutability

The full offline Python unit-test suite passes with 272 tests.

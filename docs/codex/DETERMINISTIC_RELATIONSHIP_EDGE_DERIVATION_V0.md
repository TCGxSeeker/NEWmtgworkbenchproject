# Deterministic Relationship Edge Derivation v0

## Status

Implemented and verified.

## Purpose

Derive factual relationship edges between one explicitly supplied source deck-entry profile and one explicitly supplied target deck-entry profile.

This slice does not scan a deck or compare every card against every other card.

## Implemented derivation rules

### Exact resource match

When a source output kind exactly matches a target cost kind:

- relationship type: `supplies`
- confidence band: `100`
- derivation rule: `exact_resource_output_matches_cost`

### Exact event match

When a source emitted-event kind exactly matches a target observed-event kind:

- relationship type: `triggers`
- confidence band: `100`
- derivation rule: `exact_emitted_event_matches_observer`

## Evidence preservation

Each derived edge preserves:

- source deck-entry identifier
- target deck-entry identifier
- matched source behavior
- matched target behavior
- source and target Oracle-text evidence
- source and target conditions
- source and target zones
- confidence band
- explicit derivation-rule identifier

Evidence collections are normalized through the existing relationship primitive models.

## Deterministic behavior

The derivation function:

- returns immutable tuples
- deduplicates equivalent edges
- returns edges in stable deterministic order
- produces no edge for incompatible behavior kinds
- produces no edge for empty profiles

## Architectural boundary

The public function compares one explicit pair:

`derive_relationship_edges(...)`

It does not provide:

- deck-wide scanning
- all-pairs comparison
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

Added eight focused tests covering:

- exact resource-output and cost matching
- exact emitted-event and observer matching
- mismatched resource refusal
- mismatched event refusal
- simultaneous resource and event edges
- duplicate-edge removal
- deterministic edge ordering
- empty-profile behavior

The full test suite passes with 235 tests.

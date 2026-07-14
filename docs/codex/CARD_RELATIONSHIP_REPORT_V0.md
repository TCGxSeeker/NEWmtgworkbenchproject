# Card Relationship Report v0

## Status

Implemented and verified.

## Purpose

Expose already-derived factual relationship edges through a stable,
deterministic report contract.

The report does not derive relationships or scan a deck.

## Report contract

The report provides:

- schema version
- concise user summary
- relationship count
- relationship types
- machine-readable evidence
- factual explanations
- optional debug details

## Machine evidence

Machine evidence preserves:

- relationship count
- relationship-type counts
- serialized relationship edges
- source and target entry identity
- matched behaviors
- Oracle-text evidence
- conditions
- zones
- confidence bands
- derivation-rule identifiers

## Deterministic behavior

The report:

- accepts explicit RelationshipEdge values
- rejects non-edge inputs
- deduplicates equivalent edges
- returns stable edge ordering
- returns stable relationship-type ordering
- returns stable relationship-type counts
- produces a stable empty report

## Progressive disclosure

Default serialization includes:

- concise summary
- machine evidence
- factual explanations

Debug details appear only when explicitly requested.

Debug boundaries state that the report does not perform:

- relationship derivation
- deck-wide scanning
- all-pairs comparison
- package detection
- combo solving
- synergy scoring
- recommendations
- strategic quality judgments

## Non-goals

This slice does not add:

- relationship derivation
- graph traversal
- deck-wide orchestration
- package detection
- combo solving
- synergy scoring
- recommendation logic
- card-quality judgments
- commander analysis
- user-interface behavior

## Verification

Added eight focused tests covering:

- stable empty reports
- edge evidence preservation
- relationship-type counts
- deterministic edge ordering
- factual non-strategic explanations
- optional debug details
- duplicate-edge removal
- invalid input rejection

The full test suite passes with 243 tests.

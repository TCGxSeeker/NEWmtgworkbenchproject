# Relationship Input Contract Hardening v0

## Status

Implemented and verified.

## Purpose

Harden shared relationship and behavioral-profile input contracts before they
are exposed through reusable production-facing orchestration.

## Validation changes

Required text fields now:

- accept strings only
- reject `None`
- reject integers and other non-string values
- reject empty or whitespace-only strings
- no longer coerce arbitrary values with `str(...)`

Collection fields now:

- reject plain strings
- reject bytes and byte arrays
- reject `None`
- reject non-iterable values
- raise domain-specific validation errors
- preserve deterministic sorting and deduplication for valid inputs

## Affected contracts

The hardening applies to:

- RelationshipEvidence
- RelationshipEdge
- BehaviorAtom
- CardBehavioralProfile

## Canonical edge identity

Relationship edge identity and deterministic ordering now use one shared helper:

`relationship_edge_identity_key(...)`

The helper is consumed by:

- deterministic relationship edge derivation
- card relationship reporting

This removes duplicate ordering logic and reduces future contract drift.

## Compatibility

Valid relationship inputs and serialized outputs remain unchanged.

The behavior change applies only to malformed input that was previously:

- silently coerced
- interpreted as character collections
- or allowed to raise raw Python TypeError exceptions

## Non-goals

This slice does not add:

- relationship derivation rules
- behavioral extraction coverage
- card or profile lookup
- deck-wide scanning
- all-pairs comparison
- graph traversal
- package detection
- combo solving
- synergy scoring
- recommendations
- strategic quality judgments
- commander analysis
- user-interface behavior

## Verification

Added eleven focused tests covering:

- None entry-id rejection
- integer entry-id rejection
- non-string behavior rejection
- string-as-evidence rejection
- string-as-conditions rejection
- None zones rejection
- bytes-as-conditions rejection
- None behavioral-atom collections
- valid sorting and deduplication
- shared edge identity stability
- existing relationship behavior compatibility

The full test suite passes with 260 tests.

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
- reject invalid object types inside typed collections
- reject empty required Oracle-evidence collections
- raise domain-specific validation errors
- preserve deterministic sorting and deduplication for valid inputs

Confidence bands now:

- accept only exact integer values
- reject bool values even though Python treats bool as an int subclass
- reject floats even when they compare equal to a supported band
- still require one of `0`, `25`, `50`, `75`, or `100`

Optional Oracle IDs now:

- accept strings or `None`
- reject non-string values

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

Focused tests cover:

- None entry-id rejection
- integer entry-id rejection
- non-string behavior rejection
- bool confidence-band rejection
- float confidence-band rejection
- string-as-evidence rejection
- empty relationship-evidence rejection
- string-as-conditions rejection
- None zones rejection
- invalid edge evidence objects
- bytes-as-conditions rejection
- None behavioral-atom collections
- invalid behavioral-atom objects
- non-string Oracle IDs
- valid sorting and deduplication
- shared edge identity stability
- existing relationship behavior compatibility

Run the current full unit suite from the repository root after changing these contracts.

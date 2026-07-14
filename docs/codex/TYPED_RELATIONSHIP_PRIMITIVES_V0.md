# Typed Relationship Primitives v0

## Status

Implemented and verified.

## Purpose

Provide immutable, validated value objects for factual card relationships without performing relationship derivation, strategic analysis, package detection, combo solving, or recommendations.

## Implemented vocabulary

The module defines the locked v0 vocabularies for:

- resource kinds
- event kinds
- relationship types
- confidence bands

Unsupported or deferred values are rejected explicitly.

## Implemented models

### RelationshipEvidence

Preserves:

- source behavior
- target behavior
- Oracle-text evidence
- conditions
- zones
- confidence band
- deterministic derivation rule

Collection fields are normalized into deterministic, deduplicated tuples.

### RelationshipEdge

Preserves:

- source deck-entry identifier
- target deck-entry identifier
- relationship type
- typed relationship evidence

Edges must connect different deck entries.

## Validation behavior

The models reject:

- blank required fields
- unsupported relationship types
- unsupported confidence bands
- missing Oracle evidence
- invalid evidence objects
- self-relationships

Deferred relationship types such as `converts` remain unsupported.

## Non-goals

This slice does not add:

- Oracle-text parsing
- behavioral profile extraction
- relationship-edge derivation
- graph traversal
- all-pairs comparison
- package detection
- combo solving
- synergy scoring
- recommendations
- card-quality judgments
- user-interface behavior

## Verification

Added eight focused tests covering:

- locked vocabulary
- factual evidence preservation
- entry-level identity
- deterministic serialization
- deterministic collection normalization
- unsupported relationship rejection
- unsupported confidence rejection
- self-relationship rejection

The full test suite passes with 211 tests.

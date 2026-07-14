# Factual Card Behavioral Profile v0

## Status

Implemented and verified.

## Purpose

Provide immutable, validated containers for factual card behaviors that future deterministic extraction rules can populate.

This slice does not extract behaviors from Oracle text and does not derive relationships.

## Implemented models

### BehaviorAtom

Preserves:

- behavior kind
- Oracle-text evidence
- required conditions
- relevant zones

Evidence collections are normalized, deduplicated, and deterministically ordered.

### CardBehavioralProfile

Preserves:

- canonical card name
- optional Oracle identifier
- outputs
- costs
- requirements
- emitted events
- observed events
- permissions
- modifiers
- zone constraints
- timing constraints

## Validation behavior

The models reject:

- blank required text
- behavior atoms without Oracle evidence
- invalid atom objects
- unsupported resource kinds in outputs and costs
- unsupported event kinds in emitted and observed events
- invalid Oracle identifier values

## Architectural boundary

The profile is factual evidence storage only.

It does not provide:

- Oracle-text parsing
- behavioral inference
- relationship derivation
- graph construction
- package detection
- combo solving
- synergy scoring
- recommendations
- card-quality judgments

## Verification

Added eight focused tests covering:

- factual atom preservation
- all behavioral dimensions
- resource vocabulary validation
- event vocabulary validation
- required Oracle evidence
- required card identity
- deterministic evidence normalization
- deterministic profile ordering

The full test suite passes with 219 tests.

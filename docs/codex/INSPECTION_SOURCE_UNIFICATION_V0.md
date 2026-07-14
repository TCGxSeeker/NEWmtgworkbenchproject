# Inspection Source Unification v0

## Status

Implemented and verified.

## Purpose

Ensure equivalent card facts produce equivalent deck inspection results regardless of whether they are supplied as:

- a name-keyed mapping
- an iterable of card records
- a CardCatalog

## Previous behavior

Card fact lookup accepted all supported source shapes, but the deck skeleton only received facts when the original source was a mapping of mappings.

Equivalent data could therefore produce different:

- card fact lookup status
- missing-card-fact evidence
- duplicate nonbasic warnings
- structural warnings

The result depended on the source container rather than the underlying card facts.

## Implemented behavior

Deck inspection now performs card fact lookup first.

The resolved lookup report is then converted into the skeleton-compatible record mapping used by downstream inspection.

This establishes a single evidence path:

1. resolve card facts
2. preserve found, missing, and ambiguous outcomes
3. derive skeleton facts from found lookup records
4. build structural warnings from that same resolved evidence

## Important distinctions

- No source supplied produces `not_requested`.
- A source supplied with no resolved records produces `checked`.
- Missing and ambiguous records are not guessed into found records.
- The workspace remains read-only during inspection.
- Source shape no longer changes inspection meaning.

## Non-goals

This slice does not add:

- strategy judgments
- role totals
- recommendations
- UI behavior
- live APIs
- workspace mutation
- new card-search behavior

## Verification

Added source-parity tests for:

- iterable records versus mapping records
- CardCatalog versus mapping records

The full test suite passes.

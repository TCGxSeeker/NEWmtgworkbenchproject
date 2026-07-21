# Bounded Behavioral Atom Extraction v0

## Status

Implemented and verified.

## Purpose

Add a deliberately small deterministic extractor for unmistakable Oracle-text phrases.

The extractor populates factual behavioral profiles without performing strategic interpretation.

## Supported extraction rules

The v0 extractor recognizes:

- `Create a Treasure token`
  - output: `treasure`

- `Discard a card:`
  - cost: `card_in_hand`
  - emitted event: `card_discarded`

- `Sacrifice an artifact:`
  - cost: `artifact`
  - emitted event: `permanent_sacrificed`

- `Sacrifice a Treasure:`
  - cost: `treasure`
  - emitted event: `permanent_sacrificed`

- `Whenever you cast a noncreature spell`
  - observed event: `noncreature_spell_cast`

Matching is case-insensitive while preserving the original Oracle-text segment as evidence.

## Conservative behavior

Unsupported wording is not guessed.

Missing Oracle text produces an empty factual profile.

The extractor does not infer:

- equivalent wording
- implied resources
- implied events
- card quality
- strategic value

## Non-goals

This slice does not add:

- relationship derivation
- graph construction
- all-pairs comparison
- package detection
- combo solving
- synergy scoring
- recommendations
- card-quality judgments
- fuzzy language interpretation

## Verification

Focused tests cover:

- Treasure output extraction
- discard cost and event extraction
- artifact sacrifice cost and event extraction
- Treasure sacrifice cost and event extraction
- noncreature-spell observation
- multiple supported phrases
- unsupported wording refusal
- missing Oracle text
- case-insensitive matching with preserved evidence

Run the current full unit suite from the repository root after changing this extractor.

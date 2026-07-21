# Explicit Card Record Pair Inspection v0

## Status

Implemented and verified.

## Purpose

Bridge two explicitly supplied local or Scryfall-style card records into the
existing directional factual relationship report.

## Pipeline

1. Validate explicit source and target deck-entry identifiers.
2. Validate both supplied card-record mappings.
3. Extract bounded CardBehavioralProfile values.
4. Inspect only the requested source-to-target direction.
5. Return the existing deterministic CardRelationshipReport.

## Bounded extraction addition

Exact Oracle wording containing `Sacrifice a Treasure:` produces:

- a `treasure` cost atom
- a `permanent_sacrificed` emitted-event atom

No other behavioral extraction vocabulary was added.

## Behavior

The inspection boundary:

- normalizes surrounding entry-id whitespace
- requires two different deck entries
- rejects non-mapping records
- preserves source and target entry identity
- preserves Oracle-text evidence
- translates extraction failures clearly
- returns an empty report for unsupported or unmatched behavior
- does not mutate supplied records
- performs no network access

## Non-goals

This slice does not perform deck-wide scanning, all-pairs comparison, package
detection, combo solving, synergy scoring, recommendations, strategic card
judgments, commander analysis, or UI behavior.

## Verification

Focused tests cover extraction, successful inspection, strict directionality,
unsupported empty reports, validation, identifier normalization, extraction
errors, and input immutability.

At implementation time, the full offline Python unit-test suite passed with 282 tests. Use `docs/codex/NEXT_SESSION_HANDOFF.md` for the current live suite count.

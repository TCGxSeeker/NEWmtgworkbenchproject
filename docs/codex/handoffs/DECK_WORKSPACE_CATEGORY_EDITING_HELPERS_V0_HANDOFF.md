# Deck Workspace Category Editing Helpers v0 Handoff

> Historical handoff. This slice has been completed; do not treat this file's current-state wording as authoritative. Current baseline and next repairs live in `docs/codex/NEXT_SESSION_HANDOFF.md`.

## Current project state

Completed:
- Deck Workspace Model v0
- Deck Workspace Mutations v0
- Deck Workspace Import/Export v0
- Workspace delete doctrine/planned behavior note
- Category Taxonomy v0
- Category Taxonomy Loader/Normalizer v0
- Deck Entry Category Metadata v0

Latest known verification:
- `python -m unittest discover -s tests`
- 86 tests passed

## Hard constraints

- Product remains local/offline-capable.
- No online dependency.
- No live APIs.
- No telemetry.
- No hosted/cloud dependency.
- No AI/LLM calls.
- No app UI.
- No frontend dependencies.
- No recommendations.
- No deck analysis.
- No auto-categorization.
- No role-counting.
- No primary-role enforcement.

## Goal

Add explicit mutation helpers for intentionally editing DeckEntry category metadata after import/add flows.

The data fields already exist. This slice should only add clean editing helpers and tests.

## Core doctrine

- User/imported category text must be preserved unless explicitly changed.
- Normalized category values are additional metadata, not replacements.
- Generic category is a hint.
- Deck-specific role is the truth, but this slice does not enforce that truth.
- Category edits must be explicit and reversible.

## Likely files to touch

- src/mtg_workbench/deckbuilder/mutations.py
- tests/test_deckbuilder_mutations.py
- docs/rules/DECK_WORKSPACE_FORMAT.md
- docs/rules/CATEGORY_TAXONOMY.md
- docs/product/deckbuilder/DECKBUILDER_INTERACTIONS_V0.md
- docs/product/deckbuilder/DECKBUILDER_ACCEPTANCE_CHECKLIST.md
- docs/codex/DECISION_LOG.md if a meaningful decision is made

## Suggested helpers

Use actual model field names if they differ.

- set_imported_category(entry_id, value)
- set_normalized_category(entry_id, value)
- set_generic_category_hint(entry_id, value)
- set_deck_specific_primary_role(entry_id, value)
- set_category_origin(entry_id, value)
- add_secondary_tag(entry_id, tag)
- remove_secondary_tag(entry_id, tag)
- replace_secondary_tags(entry_id, tags)
- clear_category_metadata(entry_id)

## Behavior requirements

- Find entries by entry_id.
- Raise a clear error if entry_id is missing.
- Preserve the existing `categories` grouping field.
- Preserve imported category unless explicitly changed.
- Mutations update `updated_at`.
- Mutations set `saved_state.is_dirty = true`.
- If a taxonomy object is supplied, normalized category may be validated as canonical.
- If no taxonomy object is supplied, preserve values without guessing unless existing validation requires otherwise.
- Do not auto-normalize arbitrary labels in this slice.

## Tests

Add tests for:

- set imported category
- set normalized category
- set generic category hint
- set deck-specific primary role placeholder
- set category origin
- add secondary tag
- remove secondary tag
- replace secondary tags
- clear category metadata
- missing entry_id raises clear error
- mutation marks dirty
- mutation updates updated_at
- existing category grouping field is preserved
- full suite passes with `python -m unittest discover -s tests`

## Acceptance criteria

- Tests pass.
- No network required.
- No frontend dependencies.
- No app UI.
- No recommendations.
- No deck analysis.
- No auto-categorization.
- Category metadata can be intentionally edited after import/add flows.

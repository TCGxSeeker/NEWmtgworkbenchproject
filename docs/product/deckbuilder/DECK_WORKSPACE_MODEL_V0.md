# Deck Workspace Model V0

## Purpose

Define the editable deck concept the first deckbuilder workspace should use. The v0 implementation introduces an app-native JSON workspace format named `.mtgwdeck.json`.

Plain text, CSV, Archidekt-style, and other decklist formats are import/export boundaries. They are not the native saved workspace source of truth.

## Deck Metadata

A deck should plan for:

- Schema version.
- Deck id.
- Deck name.
- Format.
- Intended bracket or power target.
- Tags.
- Created timestamp.
- Updated timestamp.
- Source import path.
- Saved state placeholder.

## Deck Sections

The workspace should keep these sections distinct:

- Commanders.
- Mainboard.
- Maybeboard.

Maybeboard entries do not count toward full reports until moved into the mainboard.

## Deck Entries

Each entry should plan for:

- Quantity.
- Raw imported name.
- Canonical display name when known.
- Oracle id when known.
- Selected printing placeholder.
- Section.
- Category.
- Tags.
- Notes placeholder.
- Unknown-card state.

## Categories And Tags

Categories should support deck organization and future grouping. Tags should remain flexible for user-facing labels, warnings, or future analysis hints, but should not become recommendation authority without an approved rule.

## Selected Printing Placeholder

The selected printing field should support future print identity, foil status, collection identity, and price differences. It should not be required for basic deck editing in V0.

## Saved State Placeholder

The model should distinguish:

- Last saved deck state.
- Current edited workspace state.
- Imported source text or path when available.
- Unsaved changes flag.

## Native JSON Format

Workspace files use `.mtgwdeck.json` and store:

- `schema_version`
- `deck_id`
- `name`
- `format`
- `created_at`
- `updated_at`
- `tags`
- `notes`
- `commanders`
- `mainboard`
- `maybeboard`
- `saved_state`
- `metadata`

See `docs/rules/DECK_WORKSPACE_FORMAT.md` for the implementation contract.

## Implementation Location

The first model slice lives under `src/mtg_workbench/deckbuilder/`:

- `models.py`: `DeckWorkspace` and `DeckEntry` dataclasses.
- `serialization.py`: native JSON save/load helpers.
- `validation.py`: lightweight workspace shape validation and user-facing errors.
- `mutations.py`: in-place workspace edit helpers that return the updated workspace.
- `import_export.py`: plain text import/export conversion helpers.

## Mutation Model

Deck Workspace Mutations v0 supports adding, removing, quantity changes, zone moves, commander assignment, category replacement, tag updates, and note updates.

Mutations update `updated_at` and mark `saved_state.is_dirty` as `true`. Moving an entry to commander sets quantity to `1`, but full Commander legality validation is intentionally deferred.

Duplicate adds merge only when the entry clearly represents the same logical card in the same zone, printing, category set, foil state, and unresolved/known state. Ambiguous or materially different adds stay separate.

## Model Boundaries

Deck workspace state is not the same as card source data. Card facts come from local snapshots or indexes; deck entries refer to those facts by stable identifiers when available.

Unknown or unresolved entries must remain editable and must round-trip without losing the original `input_name`.

## Import And Export Boundary

Plain text import/export is supported for practical movement in and out of the native workspace format. V0 accepts `1x Card Name`, `1 Card Name`, and bare `Card Name` lines, plus common commander/mainboard/maybeboard headers.

Plain text exports are intentionally clean and minimal. They do not attempt to reconstruct comments, every original category header, or external deckbuilder-specific formatting.

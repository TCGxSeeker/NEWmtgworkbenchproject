# Deckbuilder Interactions V0

## Purpose

Define planned user actions for the first deckbuilder workspace. This is interaction planning only; do not implement UI from this file yet.

## Deck Lifecycle

- Create deck.
- Open deck.
- Save deck.
- Track unsaved changes.
- Import decklist.
- Export decklist.

## Add And Edit Cards

- Quick add card by name.
- Add card from search.
- Remove card.
- Increase quantity.
- Decrease quantity.
- Move card category.
- Set card as commander.
- Move card between commander, mainboard, and maybeboard.

Deck Workspace Mutations v0 implements the data-model helpers for these edits. The helpers do not create UI controls yet.

Mutation behavior:

- Adds default to `mainboard` unless another zone is provided.
- Missing `entry_id` values are generated.
- Removing uses `entry_id`.
- Quantity decreases remove the entry when quantity reaches zero.
- Moving to commander sets quantity to `1`.
- Categories are stored as a list and can be replaced.
- Tags can be replaced, added, or removed with stable ordering.
- Notes can be set or cleared.
- Every mutation updates `updated_at` and marks the workspace dirty.

## Filtering And Search Context

- Filter current deck by text.
- Use syntax filter within the current deck.
- Open global card search from the add-card entry point.
- Keep global search distinct from current-deck filtering.
- Preserve visible search/filter context so users know whether they are browsing the deck or the full local card index.

## Workspace Modes

- Switch view mode.
- Switch group mode.
- Switch sort mode.
- Preserve the same deck data across stacks, text, grid, and table views.

## Card Context Actions

Card context actions should include:

- Open details.
- Increase quantity.
- Decrease quantity.
- Add as new card.
- Set as commander.
- Move to category.
- Move to maybeboard.
- Move to mainboard.
- Remove card.

## Import And Export

Import should support plain text decklists first. Export should preserve quantity and card name in a simple decklist format before richer export targets are considered.

Deck Workspace Import/Export v0 implements plain text conversion only:

- Import accepts `1x Card Name`, `1 Card Name`, and bare `Card Name`.
- Import recognizes commander, mainboard, deck, maybeboard, maybe board, and sideboard headers.
- `Sideboard` imports to maybeboard in v0.
- Conservative category headers such as Ramp, Draw, Removal, Interaction, Protection, Lands, Creatures, Instants, and Sorceries may become entry categories.
- Unknown cards remain unresolved entries instead of being dropped.
- Export emits Commander, Mainboard, and Maybeboard sections with `1x Card Name` lines.
- Export uses `display_name` when present and falls back to `input_name`.
- Successful native saves mark the workspace clean.

## Human Validation

User approval is required before final commander selection, final 100-card approval, power-level claims, expensive purchase decisions, combo package changes, or major archetype pivots.

## Deferred Behavior

The v0 mutation and import/export layers do not perform full Commander legality validation, strategic validation, report generation, recommendation drafting, pricing checks, live API calls, external deckbuilder format support, UI work, or visual component behavior.

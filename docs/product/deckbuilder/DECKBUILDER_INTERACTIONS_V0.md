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
- Category metadata can be edited explicitly without changing the grouping category.
- Tags can be replaced, added, or removed with stable ordering.
- Notes can be set or cleared.
- Every mutation updates `updated_at` and marks the workspace dirty.

Category Taxonomy v0 defines the controlled language future category helpers should use. Imported and user category text should be preserved; normalized categories are hints for future reasoning and should not become deck-specific role truth by themselves.

Category Taxonomy Loader/Normalizer v0 can load the tiny local taxonomy fixture and normalize a label to a canonical category or `unknown` result. Deck Entry Category Metadata v0 lets import/mutation helpers preserve both imported and normalized category fields, but it still does not auto-categorize cards or decide deck-specific role truth.

Deck Workspace Category Editing Helpers v0 allows intentional edits to imported category, normalized category, generic category hint, deck-specific primary role placeholder, category origin, and secondary tags. These helpers preserve the current grouping category unless the separate category replacement action is used.

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
- Compare card with.
- Increase quantity.
- Decrease quantity.
- Add as new card.
- Set as commander.
- Move to category.
- Move to maybeboard.
- Move to mainboard.
- Remove card.

## Visual Card Pair Compare

The baseline comparison flow is visual and temporary:

1. Invoke `Compare card with...` from one card.
2. Show a temporary `Choose one more card` state.
3. Selecting the second card opens the comparison overlay.
4. Show exactly two selected cards together.
5. Allow either comparison side to be replaced.
6. Close or cancel comparison and return to the unchanged workspace.

Selection state is transient and is not persisted in `.mtgwdeck.json`.

Opening, changing, or closing comparison does not:

- add, remove, or move cards
- change quantities or categories
- mark the workspace dirty
- produce automatic analysis
- produce a strategic recommendation

A later explicit `Inspect interaction` action may consume the factual
relationship subsystem, but that behavior is not part of baseline visual
comparison.

When interaction inspection is available, the first selected card is the
default source and the second selected card is the default target. Reverse
inspection is not automatic; it must be requested by an explicit reverse or
direction-switch action.

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

Category normalization should use `docs/rules/CATEGORY_TAXONOMY.md` when a category/header clearly matches a canonical category or alias. Unknown category labels should remain user/imported text rather than being guessed.

When category normalization is used during import, the original header should remain available as `imported_category`, while the canonical match should be stored as `normalized_category` and used as the current grouping category.

## Human Validation

User approval is required before final commander selection, final 100-card approval, power-level claims, expensive purchase decisions, combo package changes, or major archetype pivots.

## Deferred Behavior

The v0 mutation and import/export layers do not perform full Commander legality validation, strategic validation, report generation, recommendation drafting, pricing checks, live API calls, external deckbuilder format support, UI work, or visual component behavior.

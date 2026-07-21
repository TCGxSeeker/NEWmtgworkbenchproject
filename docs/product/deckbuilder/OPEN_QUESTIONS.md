# Open Questions

## Blocking Before Deckbuilder Foundation Implementation

- Should Deck Skeleton Report v0 be implemented before the deckbuilder workspace implementation?
- Should stats/details live in a right-side panel, drawer, bottom panel, or separate tab for V0?
- Which card entry fields are required in saved deck state versus derived from local card data?

Resolved: the first saved deck workspace format is native `.mtgwdeck.json`.

Resolved for Deck Workspace Mutations v0:

- Mutation helpers generate `entry_id` values when callers do not provide them.
- Mutations update `updated_at` and set `saved_state.is_dirty` to `true`.
- Duplicate adds merge only when they are clearly the same logical entry.
- Categories remain free-form strings stored as a list.
- Moving a card to commander sets quantity to `1`; legality validation is deferred.

## Blocking Before The Next Deckbuilder Slice

- Should category creation, rename, and reorder get their own helper layer before UI work?
- Should entry IDs remain UUID strings forever or gain a project-specific prefix for easier debugging?

Resolved for Deck Workspace Import/Export v0:

- Plain text is an import/export format, not native saved state.
- Native `.mtgwdeck.json` remains the saved workspace format.
- Successful `save_workspace` marks workspaces clean.
- `Sideboard` imports to maybeboard in v0.

Resolved for workspace CLI access:

- Native workspace import/export commands exist.
- Basic workspace mutation commands exist.
- Category metadata mutation commands exist.
- Entry notes and tags can be edited through explicit copy-out CLI commands.

## Blocking Before Deck Analysis

- What is the first deck skeleton report output shape?
- Which structural warnings are highest priority?
- What role taxonomy should be used for Card Seat / Role Report v0?
- Which commander profile fields are required for v0?

## Non-Blocking Product Questions

- Should the first UI be desktop, local web, or another portable shell?
- Should deck color identity auto-filter global search by default?
- How should users override deck-context color filters?
- How should categories be created, renamed, and reordered?
- Should card printings be selected during add-card flow or in card details?
- How should owned collection status appear without cluttering the main deck view?
- Which probability tool should ship first?

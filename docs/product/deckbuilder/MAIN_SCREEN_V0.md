# Main Screen V0

## Goal

Plan the first deckbuilder screen as a calm, readable workspace for one open deck. This is layout and flow planning only, not visual polish or implementation.

## Primary Layout

1. Deck header at the top.
2. Deck status strip below the header.
3. Workspace controls above the card area.
4. Grouped deck workspace as the largest area.
5. Stats/details panel on the right or in a drawer.

## Deck Header

The header should show:

- Deck name.
- Format.
- Deck size.
- Optional estimated cost.
- Optional bracket or power target.
- Tags.
- Saved state.

Primary header actions:

- Import cards.
- Export decklist.
- More menu.

## Status Strip

The status strip should show concise, actionable state:

- Commander presence.
- Mainboard count.
- Maybeboard count.
- Unknown card count.
- Unsaved changes.
- Report/warning status when available.

## Workspace Controls

Controls should be grouped by task:

- View mode selector.
- Group selector.
- Sort selector.
- Current-deck filter.
- Syntax filter entry point.
- Add-card entry point.

## Card Workspace

The card workspace should display grouped deck entries and preserve deck-editing context. It should support future stacks, text, grid, and table views over the same deck model.

Each visible card entry should allow access to context actions without crowding every row or card tile.

## Stats And Details Area

Stats/details should live in a right-side panel or drawer-style surface. It should support deck facts, selected-card details, and future report summaries without making the main card workspace feel crowded.

## Flow

The first user path should be:

1. Open or create a deck.
2. Import or add cards.
3. Review grouped deck entries.
4. Filter, sort, or switch view.
5. Inspect stats/details when needed.
6. Export or save when ready.

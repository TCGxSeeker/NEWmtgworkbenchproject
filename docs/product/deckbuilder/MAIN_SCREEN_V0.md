# Main Screen V0

## Goal

Plan the first deckbuilder screen as a calm, readable workspace for one open deck. This is layout and flow planning only, not visual polish or implementation.

Implementation note: `See The Deck v0` now provides the first narrow visible
screen using fixture-backed projection data. It is still not the finished main
deckbuilder product.

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

## Temporary Card Pair Overlay

Visual card comparison should use a temporary modal or overlay above the
current deck workspace.

The comparison surface should:

- display exactly two explicitly selected cards
- prefer side-by-side card images when the viewport allows
- remain readable on narrow screens
- provide a visible close action
- support Escape dismissal where keyboard input exists
- allow replacement of either selected card
- preserve the current view, grouping, sorting, filters, and scroll context

The comparison surface should not become:

- a permanent sidebar
- a dashboard widget
- a default report panel
- an automatic recommendation surface

Closing it returns the user to the same deckbuilder context.

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

## New Deck Path

New deck creation should start with a small, clear form:

- deck name
- format
- optional Commander bracket or power target

Advanced setup such as card packages, folder/storage choices, and category
options should use collapsed sections. Hosted visibility states such as private,
unlisted, public profile listing, or theorycrafted/social flags are not core to
the local-first MTG Workbench.

## Empty Deck Guidance

An empty deck should still show the real deck workspace. Empty guidance should
briefly point to import, quick add, and card search without replacing the
workspace with an instructional page.

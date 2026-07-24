# Main Screen Requirements

## Goal

The app should open to a deck library/home screen before entering a specific deck. Once a deck is open, the deck screen should feel like a focused deck workspace: readable, guided, and centered on the current deck.

## App Home / Deck Library

The deck library should be the first full product surface. It should show local saved decks, provide create/open flows, and make it clear which deck is currently being edited once opened.

Deck library planning lives in `docs/product/deckbuilder/DECK_LIBRARY_REQUIREMENTS.md`.

## Required Screen Areas

For the open-deck workspace:

- Deck header.
- Deck status line.
- Import cards action.
- More menu.
- Add card area.
- Quick add.
- View mode selector.
- Group-by selector.
- Sort-by selector.
- Deck filter.
- Syntax filter.
- Grouped card workspace.
- Card context menu.
- Stats panel location.

## Deck Header

Plan for:

- Deck name.
- Format.
- Deck size.
- Estimated cost, optional.
- Bracket or power target, optional.
- Tags.
- Saved state.

## Layout Notes

- Header should stay compact and readable.
- Controls should be grouped by task: view controls, add/search controls, deck actions, and stats/report access.
- The card workspace should get the most screen space.
- Stats may live in a side panel, drawer, or lower panel, but should not crowd the card list by default.
- Warnings should surface only when actionable.

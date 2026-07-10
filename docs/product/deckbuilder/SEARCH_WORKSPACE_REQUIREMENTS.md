# Search Workspace Requirements

## Search Contexts

### Global Card Search

Searches the local Scryfall index to find cards to add. This supports card lookup, card browsing, and future recommendation candidate pools.

### Current-Deck Filter

Filters cards already in the open deck. This should be fast, visible, and safe to clear.

### Syntax Search

Uses the local syntax engine against either global card data or the current deck, depending on context.

## Search Tabs

Core:

- Card search.
- Syntax search.

Future:

- Landbase helper.
- Combo helper.
- External recommendation-style helper, if manually supported later.

## Advanced Search Fields

- Format.
- Color.
- Color identity.
- Rarity.
- Type.
- Supertype.
- Subtype.
- Oracle text.
- Mana cost.
- Mana value comparison.
- Power comparison.
- Toughness comparison.
- Artist.
- Collector number.
- Flavor/lore text.
- Sort direction.
- Sort by.
- Game filter.
- Collection filter.
- Printing mode.

## Deck Context

When editing a mono-color or multi-color deck, search should make deck color identity easy to apply. The app may auto-apply deck color identity, but the active filter must remain visible and user-controllable.

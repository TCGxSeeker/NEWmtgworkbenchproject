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

Search tabs should separate workflows cleanly. Do not mix recommendation,
landbase, combo, or syntax behavior into ordinary card-name search unless the
user explicitly selects that mode.

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

## Search/Add Presentation

- Search/add may open as a focused overlay, drawer, or expanded panel while the
  current deck remains contextually visible.
- Keep advanced search, filter, and sort controls collapsed by default.
- Show result count quietly after search.
- Provide clear add/increase, decrease, and more/details actions per result
  when the result surface can support them.
- When a card has been added from search, show immediate quantity feedback such
  as `Copies: N`, a highlighted result state, or a visible quantity marker.
- Card-image grid results are desirable once local image support exists; do not
  download images automatically during normal app use.
- Price display is optional and must wait for a verified local pricing snapshot
  and a separate UI decision.

# Group, Sort, And Filter Requirements

## Group-By Modes

Core:

- Category.
- Type.
- Mana value.
- Color.
- Color identity.
- Full deck.

Future:

- Owned status.
- Price band.
- Rarity.
- Edition.
- Date added.

## Sort Modes

Core:

- Alphabet.
- Mana value.
- Type.
- Color.
- Color identity.
- Category.
- Quantity.
- Price.

Future:

- Owned status.
- Rarity.
- Edition.
- Date added.
- Artist.
- Power.
- Toughness.

## Filters

- Deck filter applies to cards already in the open deck.
- Syntax filter may apply to the current deck or global card data depending on context.
- Filters should be visible, removable, and composable.
- Multiple syntax clauses should intersect by default.

## Implementation Notes

Deck Workspace View Projection v0 implements the first read-only projection over existing workspace fields only:

- Grouping: `full_deck`, `zone`, and `category`.
- Sorting: `alphabet`, `quantity`, `category`, and `zone`.
- Filtering: simple current-deck text filtering over saved entry text fields.

Type, mana value, color, color identity, price, rarity, printing, and syntax-backed filtering require local card facts or the syntax engine and are deferred.

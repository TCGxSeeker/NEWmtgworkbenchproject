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

Deck Workspace View Projection v0 implements the first read-only projection over existing workspace fields:

- Grouping: `full_deck`, `zone`, and `category`.
- Sorting: `alphabet`, `quantity`, `category`, and `zone`.
- Filtering: simple current-deck text filtering over saved entry text fields.

Card-Fact-Backed Workspace Projection v0 adds factual projection modes when explicit local card facts are supplied:

- Grouping: `type` and `mana_value`.
- Sorting: `type` and `mana_value`.
- Missing and ambiguous facts remain visible as explicit status buckets.

Color Identity Workspace Projection v0 adds factual color projection modes when explicit local card facts are supplied:

- Grouping: `color` and `color_identity`.
- Sorting: `color` and `color_identity`.
- Multicolor cards can appear in multiple `color` groups.
- `color_identity` uses one WUBRG-ordered identity group such as `UG`.
- Missing and ambiguous facts remain visible as explicit status buckets.

Price, rarity, printing, and syntax-backed filtering require later local data adapters or the syntax engine and are deferred.

Workspace View Fixture Smoke v0 keeps an exact expected JSON fixture for one fact-backed `workspace-view` run so future changes to grouping, sorting, missing facts, ambiguous facts, or stable output order are reviewed intentionally.

The current projection payload is documented in
`docs/rules/WORKSPACE_VIEW_PROJECTION_CONTRACT.md`.

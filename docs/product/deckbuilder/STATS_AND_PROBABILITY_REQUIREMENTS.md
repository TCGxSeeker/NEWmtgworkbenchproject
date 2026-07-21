# Stats And Probability Requirements

## Deck Stats

Document and eventually display:

- Color cost distribution.
- Color production distribution.
- Average mana value.
- Total mana value.
- Mana curve.
- Mana curve by color.

## Placement

- Deck stats are an expected endpoint feature.
- They may live below the primary deck workspace on scroll, in a dedicated tab,
  or in a pinned optional panel.
- They should not crowd the default top-of-page deckbuilding workspace.
- Charts should become focusable/filtering aids only when the behavior is clear
  and reversible.

## Color And Mana Displays

- Show color-cost distribution separately from color-production distribution.
- Preserve colorless as its own state instead of merging it into missing data.
- Mana curve should support whole-deck view first.
- Mana curve by color should be a secondary/expanded view.
- Average mana value and total mana value should be visible near the curve.

## Probability Tools

Plan for:

- Probability of drawing at least N cards.
- Probability of drawing exactly N cards.
- Selected grouping basis.
- Cards drawn count.
- Category odds.
- Type odds.
- Custom group odds.
- Table output.
- Chart output later.

Probability controls should support:

- at least / exactly / at most mode
- number of matching cards
- grouping basis, such as category, type, custom group, or full deck
- cards drawn count
- focused/selected/full-deck scope once card selection exists

## Display Rules

- Charts should explain something, not decorate the page.
- Probability tools may live behind a panel, tab, or drawer.
- Defaults should be understandable to newer players.
- Calculations must be deterministic and fixture-tested before UI exposure.
- Avoid optimization buttons until the underlying rules are explicit and human
  validation zones are defined.
- Do not show ads, hosted widgets, or live external pricing/service data.
- Price/cost stats must wait for verified local snapshot support and a separate
  UI decision.

# Card Actions Requirements

## Core Actions

- Open details.
- Compare card with.
- Increase quantity.
- Decrease quantity.
- Add as new card.
- Set as commander.
- Move to category.
- Remove card.

## Open Details

The first details surface should be factual and local-data-only. It should
open from an explicitly selected deck row or search result and preserve the
current deck context.

V0 details may show:

- card name
- type line
- oracle text if locally available
- mana value
- color identity
- quantity
- categories
- tags and notes

Current zone does not need to appear in the basic details panel when the selected card's deck location is already visually clear. Show zone only for workflows where it helps, such as moving cards, comparing board sections, or reviewing search results that are not yet in the deck.

V0 details must not show live price, legality claims, EDHREC rank, salt score,
printing marketplace data, external links, recommendations, role judgment, or
power-level commentary unless a later slice provides verified local data and a
specific UI decision.

## Future Actions

- Pin card.
- Switch printing.
- Switch to foil.
- Multi-select.
- Card extras.

## Visual Card Pair Compare

`Compare card with...` is a core planned deckbuilder action.

Baseline behavior:

- Start from one explicitly selected card.
- Enter a temporary state asking the user to select one more card.
- Open a temporary modal or overlay after the second selection.
- Show exactly two selected cards together.
- Prefer side-by-side card images when the viewport allows.
- Allow either selected card to be replaced.
- Provide an obvious close action.
- Return to the unchanged deck workspace when closed.

The baseline comparison surface must not automatically show:

- synergy scores
- relationship reports
- role comparisons
- add/cut recommendations
- winner or loser labels
- purchase guidance

A future explicit `Inspect interaction` control may reveal factual
relationship evidence through progressive disclosure.

If interaction inspection is added, it must be directional. The card that
started the comparison is the default source, the second selected card is the
default target, and reverse inspection must be a separate explicit action.

## Interaction Notes

- Keep frequent actions close to the card row or card tile.
- Move less common actions into a context menu.
- Destructive actions should be reversible or confirmed depending on risk.
- Card actions must respect commander, mainboard, and maybeboard sections.

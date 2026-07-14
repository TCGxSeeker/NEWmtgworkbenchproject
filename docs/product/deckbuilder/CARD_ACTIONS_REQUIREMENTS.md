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

## Interaction Notes

- Keep frequent actions close to the card row or card tile.
- Move less common actions into a context menu.
- Destructive actions should be reversible or confirmed depending on risk.
- Card actions must respect commander, mainboard, and maybeboard sections.

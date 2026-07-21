# Visual Card Pair Compare v0

## Status

Approved product interaction contract. No UI implementation exists yet.

## Purpose

Provide the smallest useful card-comparison feature inside the primary
deckbuilder workspace.

The user can place two selected cards together and read them without opening
separate pages or leaving the deck.

## User Flow

1. Open a card context menu.
2. Choose `Compare card with...`.
3. Enter a temporary `Choose one more card` state.
4. Select a second card.
5. Open a temporary comparison overlay.
6. Display exactly two selected cards together.
7. Replace either selected card or close the overlay.
8. Return to the unchanged deckbuilder workspace.

## Baseline Display

Required:

- exactly two selected cards
- card images when locally available
- card names when images are unavailable
- clear indication of the two selected cards
- an obvious close action
- readable desktop and narrow-screen behavior

Optional when locally available:

- selected printing
- foil or nonfoil indicator
- quantity in the open deck
- local snapshot price
- ownership indicator

Optional metadata must not crowd the card images.

## State Behavior

Comparison state is transient.

Opening, changing, or closing comparison must not:

- alter deck contents
- alter quantities
- move zones or categories
- change tags or notes
- mark the workspace dirty
- persist selected comparison cards in the native deck file

The prior view mode, grouping, sorting, filters, and scroll context should be
restored when comparison closes.

## Progressive Disclosure

Baseline comparison is visual only.

A later explicit control may be labeled:

`Inspect interaction`

That action may request the factual card-relationship report. It must remain
user-initiated and collapsed by default.

## Interaction Inspection Direction

Baseline visual comparison has no source or target direction. It only places
two selected cards beside each other.

If a later `Inspect interaction` control is used, the inspection is
directional:

- the card that started `Compare card with...` is the default source
- the second selected card is the default target
- the UI must label the direction clearly, such as `source -> target`
- reverse inspection must require an explicit user action
- reverse results must be requested and displayed separately
- no automatic reverse-direction analysis should run in the baseline flow

Replacing either side should preserve a clear source-target label when
inspection is open. Closing comparison should discard the inspection state
with the rest of the transient comparison state.

## Explicit Non-Goals

Visual Card Pair Compare v0 does not automatically:

- summarize Oracle text
- declare synergy
- identify a combo
- rank either card
- choose a winner
- suggest an add or cut
- score deck fit
- show raw algorithm evidence
- change the deck
- call a network service

## Layout Doctrine

The open deck remains the primary product surface.

The overlay is temporary and dismissible. It must not create another
permanent panel or reduce the main card workspace into a secondary area.

## Future UI Acceptance Criteria

When UI implementation begins, component or interaction tests should prove:

- exactly two selected cards are displayed
- second-card selection can be cancelled
- either comparison side can be replaced
- closing restores the prior deck context
- Escape closes the overlay where keyboard input exists
- comparison does not invoke deck mutations
- comparison does not mark the workspace dirty
- no analysis appears without an explicit secondary action

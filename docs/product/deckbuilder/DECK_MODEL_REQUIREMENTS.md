# Deck Model Requirements

## Purpose

Define the data the main deckbuilder workspace needs before UI work begins.

## Deck Metadata

- Deck id.
- Deck name.
- Format.
- Intended bracket or power target, optional.
- Tags.
- Created/updated timestamps.
- Saved state.
- Source import path, optional.

## Card Entries

Each deck card entry should preserve:

- Quantity.
- Canonical card name.
- Raw imported name.
- Oracle id when known.
- Scryfall id / printing id when selected.
- Section: commander, mainboard, maybeboard.
- Category.
- Notes.
- Owned status, optional.
- Price snapshot, optional.

## Workspace State

Persist separately from card facts:

- Current view mode.
- Group-by mode.
- Sort-by mode.
- Active deck filter.
- Active syntax filter.
- Expanded/collapsed groups.
- Selected cards.

## Invariants

- Maybeboard cards do not count toward main deck reports until moved.
- Unknown cards remain visible and fixable.
- Commander entries remain distinct from mainboard entries.
- Local snapshot data should be traceable by snapshot manifest.

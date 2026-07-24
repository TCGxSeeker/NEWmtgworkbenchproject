# Deck Library Requirements

## Goal

The deck library is the app home screen before a user opens a specific deck. It should provide a calm, expressive local workspace for finding, creating, opening, and organizing saved MTG Workbench decks.

## Relationship To Deck Screen

The deck library is the entry surface. The deck screen remains the primary editing workspace once a deck is open.

The flow should feel similar to:

1. Open MTG Workbench.
2. Review recent or saved decks.
3. Create a new deck or open an existing one.
4. Land inside the focused deck workspace.

## Core V0 Capabilities

- Show saved local deck workspaces.
- Show deck name, format, mainboard count, commander count, maybeboard count, and saved state when available.
- Create a new local deck workspace.
- Open an existing local deck workspace.
- Keep import actions available without making import the only path.
- Keep search global only if it helps find decks or cards deliberately.

## Future Capabilities

- Deck folders or collections.
- Tags and filters.
- Recent decks.
- Duplicate deck.
- Rename deck.
- Safe visibility-delete or remove-from-library flow.
- Last updated timestamp.
- Optional deck thumbnail or commander image when local image data exists.

## Visual Direction

Use the local proxy utility reference for feel only: calm dark framing, generous margins, expressive but restrained buttons, readable panels, and a distinct secondary library area.

Do not import the reference app's domain content, service behavior, or exact layout. Do not make the library a busy analytics dashboard.

## Non-Goals

- No hosted visibility states such as private, unlisted, or public profiles.
- No account login requirement.
- No cloud deck sync.
- No live external service lookup.
- No recommendation or scoring surface on the library home screen.

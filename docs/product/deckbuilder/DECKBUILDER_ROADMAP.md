# Deckbuilder Roadmap

## Purpose

Define the deckbuilder product flow before full UI implementation. The deck library is the app home screen, and the open-deck workspace is the primary editing screen. Local search, stats, and reports should support deck understanding rather than become the center of the app.

Screenshots from Archidekt/Deckcheck-style tools are product inspiration only. Extract capabilities and workflow patterns, not exact styling.

## Roadmap

1. Deck library / app home.
   - Plan a calm local deck library before the open-deck screen. It should create/open decks and show saved local workspaces without becoming a dashboard.

2. Deck data model / workspace contracts.
   - Define deck metadata, card entries, categories, commanders, maybeboard, quantities, printings, ownership state, and saved state.

3. Main deck screen layout.
   - Plan a calm workspace with a deck header, status line, action controls, grouped card area, and stats location.

4. View modes.
   - Support stacks, text, grid, and table views over the same deck model.

5. Grouping, sorting, and filtering.
   - Implement category, type, mana value, color, color identity, full deck, sort controls, current-deck filtering, and syntax filtering.

6. Add-card and syntax-search workspace.
   - Distinguish global card search, current-deck filter, and syntax search context.

7. Card context actions.
   - Provide common card actions without cluttering each card row.
   - Include a baseline `Compare card with...` flow that places exactly two
     explicitly selected cards together in a temporary visual overlay.
   - Keep visual comparison separate from analysis, recommendations, and
     permanent workspace panels.

8. Deck stats and probability tools.
   - Surface color, curve, mana value, and draw probability information only
     when useful, likely below the main deck workspace or in a dedicated tab.
   - Keep stats as deck-understanding support rather than a default dashboard.

9. Save/load/import/export workflows.
   - Preserve local-first deck storage, plain text import/export, and stable machine-readable state.

10. Future UI implementation plan.
   - Build UI only after model contracts and CLI behavior are stable enough to avoid churn.

## Immediate Product Priority

After Search-2 filters, complete Deckbuilder Foundation v0 planning and Deck Skeleton Report v0 planning before implementation. Search remains a substrate for adding and finding cards; the app path should move from deck library into the focused deckbuilder workspace.

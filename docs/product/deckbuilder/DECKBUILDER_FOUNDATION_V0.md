# Deckbuilder Foundation V0

## Purpose

Define the first main product surface before implementation. Deckbuilder Foundation v0 centers the editable deck workspace and treats search, stats, import/export, and card details as supporting surfaces.

Current implementation status: native workspace model, in-memory mutation helpers, plain text import/export helpers, workspace view projections, and the first narrow `See The Deck v0` frontend screen exist. Finished app UI, reports, recommendations, scoring, live APIs, and full legality validation remain out of scope.

## Scope

Foundation v0 plans:

- Deck header.
- Deck status strip.
- View mode selector.
- Group selector.
- Sort selector.
- Current-deck filter.
- Syntax filter entry point.
- Add-card entry point.
- Grouped deck workspace.
- Card context actions.
- Right-side or drawer-style stats/details area.
- Import/export entry points.

## Non-Goals

- No broad application UI code beyond the approved `See The Deck v0` screen.
- No new frontend dependencies.
- No recommendation engine.
- No scoring rubric.
- No production styling or glass/liquid visual implementation.
- No schema migration until the V0 workspace model is reviewed.

## Product Center

The main deckbuilder workspace is the product center. Users should be able to understand and edit one deck without being forced into search-first, stats-first, or report-first workflows.

Supporting features should answer workspace questions:

- Search helps add or inspect cards.
- Filters help understand the current deck.
- Stats/details explain the deck without crowding the card workspace.
- Import/export moves decklists in and out cleanly.

## Foundation Sequence

1. Finalize the V0 deck workspace model.
2. Finalize the V0 main screen flow.
3. Finalize V0 interactions and command boundaries.
4. Add fixture-ready acceptance checks.
5. Start implementation only after the planning checklist passes.

## Related Docs

- `MAIN_SCREEN_V0.md`
- `DECK_WORKSPACE_MODEL_V0.md`
- `DECKBUILDER_INTERACTIONS_V0.md`
- `DECKBUILDER_ACCEPTANCE_CHECKLIST.md`
- `OPEN_QUESTIONS.md`

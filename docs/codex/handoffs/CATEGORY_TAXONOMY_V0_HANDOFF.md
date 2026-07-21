# Category Taxonomy v0 Handoff

> Historical handoff. This slice has been completed; do not treat this file's current-state wording as authoritative. Current baseline and next repairs live in `docs/codex/NEXT_SESSION_HANDOFF.md`.

## Current project state

Completed deckbuilder foundation slices:
- Deck Workspace Model v0
- Deck Workspace Mutations v0
- Deck Workspace Import/Export v0
- Workspace save/load clean-dirty behavior
- Workspace delete/visibility behavior patch

Important delete clarification:
"Deleting a deck" means removing the visible deck/workspace from the user's workspace/library view.
It must not imply deleting canonical card database information, Scryfall-derived data, shared card records, or local card index data.

## Hard constraints

- Product remains local/offline-capable.
- No online dependency.
- No live APIs.
- No telemetry.
- No hosted/cloud dependency.
- No built-in AI/LLM calls.
- No frontend dependencies in this slice.
- No app UI in this slice.
- No recommendations in this slice.
- No full deck analysis in this slice.
- No large category/card dataset ingestion in this slice.

## Category Taxonomy v0 goal

Create a controlled category language for deckbuilder card roles and imported decklist headers.

This is a rules/data foundation slice.

Do not ingest a huge card-to-category dataset yet.
Do not auto-categorize every card yet.
Do not overwrite imported user categories.

Core doctrine:
- Generic card category is a hint.
- Deck-specific role is the truth.
- User/imported categories should be preserved.
- Normalized categories should help the app reason later.
- One primary role should be supported later to avoid count inflation.

## Suggested files

Create/update:

- docs/rules/CATEGORY_TAXONOMY.md
- data/fixtures/categories/category_taxonomy.example.yaml or similar small fixture
- docs/product/deckbuilder/DECKBUILDER_INTERACTIONS_V0.md if needed
- docs/product/deckbuilder/DECKBUILDER_ACCEPTANCE_CHECKLIST.md if needed
- docs/codex/DECISION_LOG.md with a short entry

## Suggested canonical categories

- Commander
- Land
- Ramp
- Fixing
- Draw
- Selection
- Tutor
- Engine
- Interaction
- Removal
- Countermagic
- Board Wipe
- Protection
- Recursion
- Sac Outlet
- Token Maker
- Aristocrat Payoff
- Combo Piece
- Payoff
- Wincon
- Stax
- Voltron
- Equipment
- Aura
- Utility
- Flex
- Pet Card

## Alias examples

- Card Advantage -> Draw
- Card Draw -> Draw
- Cantrip -> Selection
- Filtering -> Selection
- Looting -> Selection
- Rummaging -> Selection
- Mana Rock -> Ramp
- Mana Dork -> Ramp
- Acceleration -> Ramp
- Spot Removal -> Removal
- Counterspell -> Countermagic
- Counterspells -> Countermagic
- Boardwipe -> Board Wipe
- Wrath -> Board Wipe
- Protection Spell -> Protection
- Finisher -> Wincon
- Closer -> Wincon
- Win Condition -> Wincon
- Graveyard Recursion -> Recursion
- Reanimation -> Recursion
- Sacrifice Outlet -> Sac Outlet

## Needed conceptual separation

Future docs/model should distinguish:

- imported_category
- normalized_category
- generic_category_hint
- deck_specific_primary_role
- secondary_tags
- category_origin: imported | user | normalized | inferred | taxonomy_default

Category Taxonomy v0 does not need to implement all fields yet, but should document the distinction.

## Acceptance criteria

- Taxonomy doc exists.
- Canonical categories are defined.
- Aliases/synonyms are defined.
- Imported user categories vs normalized/inferred categories are clearly separated.
- Tiny fixture/example exists if consistent with repo style.
- No network required.
- Existing tests pass.
- No large datasets added.
- No auto-categorization implemented yet.

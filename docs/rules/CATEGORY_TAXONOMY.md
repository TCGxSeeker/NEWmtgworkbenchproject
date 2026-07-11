# Category Taxonomy

## Purpose

Category Taxonomy v0 defines a controlled category language for deckbuilder card roles and imported decklist headers.

This is a rules/data foundation slice. It does not auto-categorize cards, ingest card-to-category datasets, overwrite user categories, or perform deck analysis.

## Core Doctrine

- Generic card category is a hint.
- Deck-specific role is the truth.
- Imported and user categories must be preserved.
- Normalized categories help the app reason later.
- Future role counting should support one primary role to avoid count inflation.

## Canonical Categories

| Category | Meaning |
| --- | --- |
| Commander | Commander or partner/background commander slot. |
| Land | Land or land-slot card. |
| Ramp | Mana acceleration. |
| Fixing | Color smoothing or mana fixing. |
| Draw | Card advantage or repeatable card flow. |
| Selection | Card filtering, cantrips, looting, rummaging, or top-deck selection. |
| Tutor | Finds a specific card or narrow card class. |
| Engine | Repeatable value system that drives the deck over time. |
| Interaction | Broad answer card or stack/board interaction. |
| Removal | Targeted permanent or creature answer. |
| Countermagic | Counterspell or stack denial. |
| Board Wipe | Mass removal or reset effect. |
| Protection | Protects commander, board, combo, or key permanent. |
| Recursion | Returns cards from graveyard or reused resources. |
| Sac Outlet | Enables sacrificing permanents as a repeatable action. |
| Token Maker | Produces tokens as a primary contribution. |
| Aristocrat Payoff | Rewards deaths, sacrifices, or drain patterns. |
| Combo Piece | Required or enabling combo component. |
| Payoff | Converts setup into advantage or pressure. |
| Wincon | Primary or realistic route to ending the game. |
| Stax | Restricts opponents through rules, taxes, or denial. |
| Voltron | Supports commander/piece damage through buffs or equipment-style pressure. |
| Equipment | Equipment card or equipment package piece. |
| Aura | Aura card or aura package piece. |
| Utility | Flexible support card that does not fit a sharper role yet. |
| Flex | Intentional flexible slot. |
| Pet Card | User-protected preference card. |

## Alias Map

Aliases normalize imported headers and user labels to canonical categories when the match is clear.

| Alias | Canonical Category |
| --- | --- |
| Acceleration | Ramp |
| Boardwipe | Board Wipe |
| Cantrip | Selection |
| Card Advantage | Draw |
| Card Draw | Draw |
| Closer | Wincon |
| Counterspell | Countermagic |
| Counterspells | Countermagic |
| Filtering | Selection |
| Finisher | Wincon |
| Graveyard Recursion | Recursion |
| Looting | Selection |
| Mana Dork | Ramp |
| Mana Rock | Ramp |
| Protection Spell | Protection |
| Reanimation | Recursion |
| Rummaging | Selection |
| Sacrifice Outlet | Sac Outlet |
| Spot Removal | Removal |
| Win Condition | Wincon |
| Wrath | Board Wipe |

## Category Fields

Deck Entry Category Metadata v0 stores these distinctions on native deck entries:

- `imported_category`: original category/header from imported decklists.
- `normalized_category`: taxonomy-normalized category when an alias or canonical category matches.
- `generic_category_hint`: broad card-category hint from imports, defaults, or user labels.
- `deck_specific_primary_role`: the role that counts for this exact deck context.
- `secondary_tags`: non-counting labels or supporting role hints.
- `category_origin`: source of the category, such as `imported`, `user`, `normalized`, `inferred`, `taxonomy_default`, or `unknown`.

`categories` remains the current grouping field for deckbuilder behavior. Metadata fields preserve provenance and future analysis context; they do not make a category count as a deck-specific role by themselves.

## Normalization Rules

- Preserve the original imported or user category text.
- Trim whitespace and compare category aliases case-insensitively.
- Normalize repeated spaces before matching.
- Match canonical names and listed aliases only.
- If a label is unknown, keep it as imported/user text and do not guess.
- Do not infer deck-specific role from generic category alone.

## Loader/Normalizer V0

The v0 loader lives in `src/mtg_workbench/deckbuilder/categories.py`.

It supports the tiny local fixture shape in `data/fixtures/categories/category_taxonomy.example.yaml` without adding a YAML dependency. It loads:

- `schema_version`
- `source`
- `description`
- `canonical_categories`
- `aliases`

The normalizer returns:

- `input_category`: original user/imported label.
- `normalized_category`: canonical category when an exact canonical or alias match exists.
- `category_origin`: `normalized` or `unknown`.

Unknown labels return `normalized_category: None` and keep the original label intact.

Loader/Normalizer v0 does not mutate `DeckWorkspace` or `DeckEntry` categories by itself.

## Deck Entry Category Metadata V0

The native `DeckEntry` model now preserves imported and normalized category metadata. Plain text import can use a supplied local taxonomy to recognize canonical or alias category headers.

When taxonomy import recognizes a category header:

- `categories` receives the normalized category for current grouping.
- `imported_category` keeps the source header exactly as cleaned by the importer.
- `normalized_category` keeps the canonical category.
- `generic_category_hint` keeps the canonical category as a non-authoritative hint.
- `category_origin` records `normalized`.

When a conservative built-in header is recognized without taxonomy normalization, `categories` and `generic_category_hint` keep that header, `imported_category` keeps the source header, `normalized_category` remains empty, and `category_origin` records `imported`.

Unknown category labels are not guessed.

## Deck Workspace Category Editing Helpers V0

Category metadata can be edited after import/add flows through explicit workspace mutation helpers.

Supported edits:

- Set or clear `imported_category`.
- Set or clear `normalized_category`.
- Set or clear `generic_category_hint`.
- Set or clear `deck_specific_primary_role`.
- Set or clear `category_origin`.
- Add, remove, replace, or clear `secondary_tags`.
- Clear all category metadata while preserving `categories`.

Helpers preserve the current `categories` grouping field unless a caller uses the separate category replacement helper. Supplying a taxonomy can validate that `normalized_category` is canonical; helpers do not auto-normalize arbitrary labels.

## Deferred

- No card-to-category dataset ingestion.
- No automatic card categorization.
- No role-counting engine.
- No primary-role enforcement in the model.
- No recommendation behavior.
- No UI controls.
- No large external data source.
- No automatic category mutation outside explicit import/mutation helpers.

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

Future model and analysis work should distinguish:

- `imported_category`: original category/header from imported decklists.
- `normalized_category`: taxonomy-normalized category when an alias or canonical category matches.
- `generic_category_hint`: broad card-category hint from imports, defaults, or user labels.
- `deck_specific_primary_role`: the role that counts for this exact deck context.
- `secondary_tags`: non-counting labels or supporting role hints.
- `category_origin`: source of the category, such as `imported`, `user`, `normalized`, `inferred`, or `taxonomy_default`.

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

V0 does not mutate `DeckWorkspace` or `DeckEntry` categories. Import/export integration should wait until the model can preserve both imported and normalized category fields.

## Deferred

- No card-to-category dataset ingestion.
- No automatic card categorization.
- No role-counting engine.
- No primary-role enforcement in the model.
- No recommendation behavior.
- No UI controls.
- No large external data source.
- No workspace category mutation from taxonomy normalization yet.

# Workspace View Projection Contract

## Purpose

`deck_workspace_view_projection.v0` is the read-only view-model contract for
showing an open deck as grouped, sorted, and filtered card rows. It prepares
deck data for future UI screens without mutating `.mtgwdeck.json` files and
without performing deck analysis.

This contract supports the first visible deckbuilder milestone: see the deck.

## Producer And Consumers

Current producer:

- `src/mtg_workbench/deckbuilder/workspace_view.py`
- CLI preview: `python -m mtg_workbench.cli workspace-view ...`

Current executable example:

- `tests/fixtures/deckbuilder/workspace_view_smoke_expected.json`
- `tests/test_deckbuilder_workspace_view_smoke.py`

Future consumers:

- main deck screen
- grouped card workspace
- table/list/stacks/grid view adapters
- current-deck filter controls

## Boundaries

The projection is view data. It must not be treated as:

- deck analysis
- deck legality validation
- role counting
- recommendation data
- scoring data
- power-level data
- price optimization
- persisted deck state

Projection output may include machine-readable facts needed to render or debug
the view, but the standard UI should emphasize deckbuilder card rows and
actions. Local fact coverage, missing facts, ambiguous facts, and unresolved
plumbing belong in advanced validation/details views unless they require a
direct user fix.

## Top-Level Fields

Required top-level fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `deck_workspace_view_projection.v0` for this contract. |
| `deck_id` | Native workspace deck id. |
| `deck_name` | Native workspace deck name. |
| `group_by` | Normalized group mode actually used. |
| `sort_by` | Normalized sort mode actually used. |
| `filter_text` | Normalized current-deck filter text, or `null`. |
| `visible_entry_count` | Count of unique visible entries after zone and text filters. |
| `visible_quantity_total` | Quantity total for unique visible entries. |
| `grouped_entry_count` | Count of entries across groups, including repeated memberships. |
| `grouped_quantity_total` | Quantity total across groups, including repeated memberships. |
| `card_fact_lookup` | Lookup status summary for fact-backed projections. |
| `groups` | Ordered list of projection groups. |

## Group Fields

Each group contains:

| Field | Meaning |
| --- | --- |
| `group_id` | Stable normalized id derived from the label. |
| `label` | Human-readable group label. |
| `entry_count` | Number of entries inside this group. |
| `quantity_total` | Quantity total inside this group. |
| `entries` | Ordered card rows for this group. |

Group labels are output labels, not deck analysis conclusions. Examples:
`Commander`, `Mainboard`, `Ramp`, `Mana Value 2`, `Creature`, `Blue`,
`Colorless`, `UG`, `Missing Card Facts`, and `Ambiguous Card Facts`.

## Entry Fields

Each entry contains:

| Field | Meaning |
| --- | --- |
| `entry_id` | Stable deck-entry id. |
| `zone` | `commander`, `mainboard`, or `maybeboard`. |
| `quantity` | Quantity for this deck entry. |
| `card_name` | Display name when known, otherwise input name. |
| `input_name` | Original or user-entered name preserved by the workspace. |
| `display_name` | Resolved display name, or `null`. |
| `categories` | Current grouping categories stored on the entry. |
| `tags` | User or workflow tags stored on the entry. |
| `secondary_tags` | Secondary category/role tags stored on the entry. |
| `imported_category` | Imported source category label, or `null`. |
| `normalized_category` | Taxonomy-normalized category label, or `null`. |
| `generic_category_hint` | Generic category hint, or `null`. |
| `is_unresolved` | Whether the entry is unresolved in the workspace. |
| `card_fact_status` | `not_requested`, `found`, `missing`, or `ambiguous`. |
| `type_line` | Local card type line when available, otherwise `null`. |
| `type_labels` | Structured type labels derived for grouping/sorting. |
| `mana_value` | Local mana value when available, otherwise `null`. |
| `colors` | WUBRG-ordered color list, empty list for colorless, or `null`. |
| `color_identity` | WUBRG-ordered identity list, empty list for colorless, or `null`. |

Future fields require a new contract note or schema version decision before UI
code relies on them.

## Supported Modes

Current group modes:

- `full_deck`
- `zone`
- `category`
- `type`
- `mana_value`
- `color`
- `color_identity`

Current sort modes:

- `alphabet`
- `quantity`
- `category`
- `zone`
- `type`
- `mana_value`
- `color`
- `color_identity`

Fact-backed modes require explicit local card facts:

- group by `type`, `mana_value`, `color`, or `color_identity`
- sort by `type`, `mana_value`, `color`, or `color_identity`

If a fact-backed mode is requested without local card facts, the command must
fail clearly instead of guessing from card names or categories.

## Counting Semantics

`visible_entry_count` and `visible_quantity_total` count each visible entry once
after zone filtering and current-deck text filtering.

`grouped_entry_count` and `grouped_quantity_total` count entries inside groups.
These totals may be larger than visible totals when a group mode supports
multiple memberships.

Known multi-membership group modes:

- `category`: an entry with multiple categories appears in each category group.
- `type`: an artifact creature may appear in both `Creature` and `Artifact`.
- `color`: a multicolor card appears in each color group.

Known single-membership group modes:

- `full_deck`
- `zone`
- `mana_value`
- `color_identity`

Future UI must label totals carefully and avoid treating grouped totals as deck
analysis totals.

## Fact Status Buckets

`card_fact_status` values:

- `not_requested`: no card-fact lookup was supplied.
- `found`: exactly one local card fact candidate matched the entry.
- `missing`: no local card fact candidate matched the entry.
- `ambiguous`: more than one local candidate matched the entry.

Fact-status labels such as `Missing Card Facts`, `Ambiguous Card Facts`,
`Unknown Type`, `Unknown Mana Value`, `Unknown Color`, and
`Unknown Color Identity` keep entries visible instead of guessing.

Standard deckbuilder UI should not make local fact coverage a primary dashboard
metric. It may show actionable repair prompts or expose full status details in
advanced validation/debug views.

## Ordering Semantics

Zone order is:

1. `commander`
2. `mainboard`
3. `maybeboard`

Color order is WUBRG:

1. `W`
2. `U`
3. `B`
4. `R`
5. `G`

Type order is:

1. `Land`
2. `Creature`
3. `Artifact`
4. `Enchantment`
5. `Planeswalker`
6. `Battle`
7. `Instant`
8. `Sorcery`
9. `Kindred`

Alphabetical tie-breakers use normalized card name and then `entry_id` for
stable output.

## Filtering Semantics

The current `filter_text` is a simple current-deck text filter. It is
case-insensitive, trims repeated whitespace, and searches saved deck-entry text
fields such as card name, categories, tags, secondary tags, imported category,
normalized category, and generic category hint.

This is not Scryfall syntax search. Syntax-backed current-deck filtering is
deferred and must be added as its own explicit slice.

## Deferred Fields And Behaviors

Deferred beyond this contract:

- visual stacks/text/grid/table components
- syntax-backed current-deck filtering
- global search/add workflow
- price, rarity, edition, printing, artist, power, and toughness projections
- sideboard as a first-class zone
- bulk selection and drag/drop behavior
- undo/redo or version recovery
- deck legality validation
- statistics and probability tools
- recommendations, scoring, and strategic analysis

## Verification

Current verification commands:

```powershell
python -m unittest tests.test_deckbuilder_workspace_view_smoke
python -m unittest tests.test_deckbuilder_workspace_view
python -m unittest tests.test_cli_workspace_view
python -m unittest discover -s tests
git diff --check
```

Current baseline: 344 tests pass from `G:\Documents\New MTG project`.

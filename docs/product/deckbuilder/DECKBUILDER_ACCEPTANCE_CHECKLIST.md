# Deckbuilder Acceptance Checklist

## Planning Readiness

- [x] Stale phase language is removed from current core docs.
- [x] `README.md` exists at the repository root.
- [x] `.gitattributes` exists at the repository root.
- [x] Deckbuilder Foundation v0 docs exist.
- [x] The main deckbuilder workspace is clearly the product center.
- [x] Search, stats, import/export, and reports are described as supporting surfaces.
- [x] Implementation boundaries are explicit.
- [x] No finished deckbuilder app UI has been implemented.
- [x] No new frontend dependencies have been installed for current backend CLI slices.
- [x] Open questions are listed before implementation starts.

## Required V0 Docs

- [x] `DECKBUILDER_FOUNDATION_V0.md`
- [x] `MAIN_SCREEN_V0.md`
- [x] `DECK_WORKSPACE_MODEL_V0.md`
- [x] `DECKBUILDER_INTERACTIONS_V0.md`
- [x] `DECKBUILDER_ACCEPTANCE_CHECKLIST.md`
- [x] `OPEN_QUESTIONS.md`

## Before Implementation

- [x] Decide whether Deck Skeleton Report v0 or Deckbuilder Foundation implementation comes first.
- [x] Define any required saved deck file format before persistence work.
- [x] Confirm the first implementation target and verification command.

## Deck Workspace Model V0

- [x] Native `.mtgwdeck.json` format is documented.
- [x] Workspace and entry model objects exist.
- [x] Native JSON save/load helpers exist.
- [x] Malformed workspace validation errors are user-facing.
- [x] Tiny workspace fixtures exist.
- [x] Unit tests cover round-trip preservation and malformed input.

## Deck Workspace Mutations V0

- [x] Mutation behavior is documented.
- [x] Entry id generation is documented and tested.
- [x] Add/remove helpers exist.
- [x] Increase/decrease helpers exist.
- [x] Zone move and set-commander helpers exist.
- [x] Category, tag, and note update helpers exist.
- [x] Duplicate add policy is documented and tested.
- [x] Mutations update `updated_at`.
- [x] Mutations mark `saved_state.is_dirty` true.
- [x] Commander moves set quantity to `1`.
- [x] Native workspace round trip still works after mutations.
- [x] `workspace-add-card` CLI wraps add-entry behavior for native workspace files.
- [x] `workspace-remove-entry` CLI wraps remove-entry behavior.
- [x] `workspace-increase-quantity` and `workspace-decrease-quantity` CLI commands wrap quantity helpers.
- [x] `workspace-move-zone` and `workspace-set-commander` CLI commands wrap zone helpers.
- [x] Mutation CLI commands require explicit `--output` paths.
- [x] No UI code or frontend dependency changes were added for this slice.

Deferred beyond this slice:

- Full Commander legality validation.
- Deck-specific role editing CLI.
- Bulk edit and multi-select mutation commands.
- UI mutation controls.

## Deck Workspace Import/Export V0

- [x] Plain text import/export behavior is documented.
- [x] `1x Card Name` import lines are supported.
- [x] `1 Card Name` import lines are supported.
- [x] Bare `Card Name` import lines are supported.
- [x] Commander, mainboard, and maybeboard headers are supported.
- [x] `Sideboard` safely imports to maybeboard.
- [x] Conservative category headers can become entry categories.
- [x] Unresolved cards are preserved.
- [x] Export emits clean `1x Card Name` text.
- [x] Export falls back to `input_name` for unresolved cards.
- [x] Successful native saves mark workspaces clean.
- [x] `workspace-import` CLI writes native `.mtgwdeck.json` files from plain text.
- [x] `workspace-export` CLI writes plain text decklists from native workspaces.
- [x] No UI code, frontend dependency changes, live APIs, reports, or recommendation logic were added for this slice.

Deferred beyond this slice:

- Deck Workspace Mutations CLI commands.
- Full external deckbuilder format support.
- Perfect reconstruction of original comments or every source header.
- Full Commander legality validation.

## Category Taxonomy V0

- [x] Category taxonomy doc exists.
- [x] Canonical categories are defined.
- [x] Aliases and synonyms are defined.
- [x] Imported/user categories are separated from normalized and inferred categories.
- [x] Tiny local category fixture exists.
- [x] Generic category is documented as a hint.
- [x] Deck-specific role is documented as the truth.
- [x] No large card-to-category dataset was added.
- [x] No auto-categorization, recommendations, analysis, UI, or frontend dependency changes were added for this slice.

Deferred beyond this slice:

- Primary-role enforcement.
- Role-counting engine.
- Card-to-category dataset ingestion.

## Category Taxonomy Loader/Normalizer V0

- [x] Category taxonomy loader exists.
- [x] Category label normalizer exists.
- [x] Alias normalization is tested.
- [x] Canonical category normalization is tested.
- [x] Unknown category labels are preserved without guessing.
- [x] Alias targets are validated.
- [x] No workspace categories are mutated by taxonomy normalization in this slice.
- [x] No new dependencies, UI, recommendations, analysis, or large datasets were added.

Deferred beyond this slice:

- Primary-role enforcement.
- Role-counting engine.
- Card-to-category dataset ingestion.

## Deck Entry Category Metadata V0

- [x] `DeckEntry` stores imported category labels.
- [x] `DeckEntry` stores taxonomy-normalized category labels.
- [x] `DeckEntry` stores generic category hints.
- [x] `DeckEntry` stores a future deck-specific primary role placeholder.
- [x] `DeckEntry` stores secondary tags.
- [x] `DeckEntry` stores category origin.
- [x] Native `.mtgwdeck.json` round trips preserve category metadata.
- [x] Workspace validation reports malformed category metadata.
- [x] Mutation helpers can create entries with category metadata.
- [x] Plain text import can use the local category taxonomy when supplied.
- [x] Unknown category labels are not guessed.
- [x] No UI code, frontend dependency changes, recommendations, role counting, auto-categorization, live APIs, or large datasets were added.

Deferred beyond this slice:

- Primary-role enforcement.
- Role-counting engine.
- Card-to-category dataset ingestion.
- UI controls for category metadata.
- Strategic category/role recommendations.

## Deck Workspace Category Editing Helpers V0

- [x] Imported category can be set or cleared by entry id.
- [x] Normalized category can be set or cleared by entry id.
- [x] Normalized category can be validated against a supplied taxonomy.
- [x] Generic category hint can be set or cleared by entry id.
- [x] Deck-specific primary role placeholder can be set or cleared by entry id.
- [x] Category origin can be set or cleared by entry id.
- [x] Secondary tags can be added, removed, replaced, and cleared.
- [x] Missing entry ids raise clear errors.
- [x] Category metadata edits preserve the current `categories` grouping field.
- [x] Category metadata edits update `updated_at`.
- [x] Category metadata edits mark `saved_state.is_dirty` true.
- [x] No UI code, frontend dependency changes, recommendations, role counting, auto-categorization, live APIs, or large datasets were added.

Deferred beyond this slice:

- UI controls for category metadata.
- Primary-role enforcement.
- Role-counting engine.
- Strategic category/role recommendations.

## Category Metadata Mutation CLI V0

- [x] Imported category metadata can be set or cleared from the CLI.
- [x] Normalized category metadata can be set or cleared from the CLI.
- [x] Normalized category metadata can be validated with a supplied local taxonomy.
- [x] Generic category hint metadata can be set or cleared from the CLI.
- [x] Category origin metadata can be set or cleared from the CLI.
- [x] Secondary tags can be added, removed, replaced, and cleared from the CLI.
- [x] All category metadata can be cleared while preserving `categories`.
- [x] Category metadata CLI commands require explicit `--output` paths.
- [x] Category metadata CLI output includes stable entry summaries.
- [x] Deck-specific primary-role assignment remains intentionally unexposed.
- [x] No UI code, frontend dependency changes, recommendations, role counting, auto-categorization, live APIs, or large datasets were added.

Deferred beyond this slice:

- Deck-specific role editing CLI.
- UI controls for category metadata.
- Primary-role enforcement.
- Role-counting engine.
- Strategic category/role recommendations.

## Entry Annotation CLI V0

- [x] Entry notes can be set or cleared from the CLI.
- [x] Entry tags can be replaced from the CLI.
- [x] Entry tags can be added from the CLI.
- [x] Entry tags can be removed from the CLI.
- [x] Annotation CLI commands require explicit `--output` paths.
- [x] Annotation CLI output includes stable entry summaries.
- [x] No UI code, frontend dependency changes, analysis, recommendations, live APIs, or large datasets were added.

Deferred beyond this slice:

- Bulk edit and multi-select annotation commands.
- UI controls for notes and tags.

## Deck Workspace View Projection V0

- [x] Workspace entries can be projected without mutating the workspace.
- [x] `full_deck`, `zone`, and `category` grouping are supported.
- [x] `alphabet`, `quantity`, `category`, and `zone` sorting are supported.
- [x] Current-deck text filtering uses existing saved entry text fields.
- [x] Unresolved entries remain visible in projection output.
- [x] Multi-category entries expose explicit grouped totals.
- [x] Unsupported group, sort, and zone inputs raise clear errors.
- [x] No UI code, frontend dependency changes, card fact lookup, deck analysis, role counting, recommendations, live APIs, or large datasets were added.

Deferred beyond this slice:

- Visual view modes such as stacks, grid, text, and table.
- Syntax-backed current-deck filtering.
- Type, mana value, color, color identity, price, rarity, and printing projections.
- Category creation, rename, and reorder helpers.

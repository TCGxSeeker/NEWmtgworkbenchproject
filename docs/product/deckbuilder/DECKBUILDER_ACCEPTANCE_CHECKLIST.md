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

## Workspace View CLI V0

- [x] `workspace-view` prints read-only projection JSON from a native workspace.
- [x] `--group-by` supports the projection layer's current group modes.
- [x] `--sort-by` supports the projection layer's current sort modes.
- [x] `--filter` supports current-deck text filtering.
- [x] Repeated `--zone` options can limit visible zones.
- [x] The command validates native workspace input and existing files.
- [x] Unsupported projection options return clear errors.
- [x] The command does not write output files or mutate the workspace.
- [x] No UI code, frontend dependency changes, card fact lookup, deck analysis, role counting, recommendations, live APIs, or large datasets were added.

Deferred beyond this slice:

- Workspace projection output formats besides JSON.
- Syntax-backed filtering.
- UI controls for group, sort, and filter state.

## Card-Fact-Backed Workspace Projection V0

- [x] `type` grouping is supported when explicit local card facts are supplied.
- [x] `mana_value` grouping is supported when explicit local card facts are supplied.
- [x] `type` sorting is supported when explicit local card facts are supplied.
- [x] `mana_value` sorting is supported when explicit local card facts are supplied.
- [x] Missing card facts stay visible as `Missing Card Facts`.
- [x] Ambiguous card facts stay visible as `Ambiguous Card Facts`.
- [x] Projection output exposes found, missing, and ambiguous lookup counts.
- [x] `workspace-view` accepts `--cards` or `--card-records` for local fact-backed projections.
- [x] Fact-backed modes fail clearly when no local card source is supplied.
- [x] No UI code, frontend dependency changes, deck analysis, role counting, recommendations, live APIs, or large datasets were added.

Deferred beyond this slice:

- Color and color identity projection modes.
- Price, rarity, edition, and printing projection modes.
- Syntax-backed current-deck filtering.
- Deck-level role totals or strategic reports.

## Color Identity Workspace Projection V0

- [x] `color` grouping is supported when explicit local card facts are supplied.
- [x] `color_identity` grouping is supported when explicit local card facts are supplied.
- [x] `color` sorting is supported when explicit local card facts are supplied.
- [x] `color_identity` sorting is supported when explicit local card facts are supplied.
- [x] Colorless cards are distinguished from missing or unknown color facts.
- [x] Missing card facts stay visible as `Missing Card Facts`.
- [x] Ambiguous card facts stay visible as `Ambiguous Card Facts`.
- [x] `workspace-view` can use the new modes through `--cards` or `--card-records`.
- [x] Fact-backed modes fail clearly when no local card source is supplied.
- [x] No UI code, frontend dependency changes, deck analysis, role counting, recommendations, live APIs, price logic, or large datasets were added.

Deferred beyond this slice:

- Price, rarity, edition, and printing projection modes.
- Syntax-backed current-deck filtering.
- Deck-level role totals or strategic reports.

## Workspace View Fixture Smoke V0

- [x] Tiny native workspace fixture exists for `workspace-view`.
- [x] Tiny local card-record fixture exists for fact-backed projection.
- [x] Exact expected JSON fixture exists.
- [x] Smoke test exercises the real CLI command.
- [x] Repeated CLI output is deterministic.
- [x] Source workspace file is not mutated.
- [x] Missing and ambiguous card facts remain visible.
- [x] Forbidden strategic/recommendation fields are absent from the projection payload.

Deferred beyond this slice:

- Projection contract documentation for future UI consumers.
- Syntax-backed current-deck filtering.
- Price, rarity, edition, and printing projection modes.
- Deck-level role totals or strategic reports.

## Workspace Projection Contract Docs V0

- [x] `deck_workspace_view_projection.v0` purpose is documented.
- [x] Producer and future consumers are documented.
- [x] Top-level projection fields are documented.
- [x] Group fields are documented.
- [x] Entry fields are documented.
- [x] Grouping, sorting, filtering, and counting semantics are documented.
- [x] Fact status buckets are documented as advanced/background validation data.
- [x] The smoke fixture is referenced as the executable example.
- [x] Deferred UI, syntax, stats, legality, printing, and recommendation behavior is explicit.

Deferred beyond this slice:

- First visible deck screen implementation.
- Syntax-backed current-deck filtering.
- Global search/add workflow.
- Card detail surface.
- Full legality, statistics, printings, bulk edit, and version recovery behavior.

## See The Deck V0

- [x] Existing Vite starter screen is replaced with a deck workspace screen.
- [x] Screen uses tiny local fixture data shaped like `deck_workspace_view_projection.v0`.
- [x] Deck header shows deck name, format context, active quantity, maybeboard quantity, and saved state.
- [x] Grouped view displays card rows by category.
- [x] Table view displays the same entries in a compact table.
- [x] Current-deck text filter works locally.
- [x] Groups can be collapsed and expanded.
- [x] Default UI does not surface local fact coverage as dashboard content.
- [x] No inactive import, export, add-card, mutation, recommendation, scoring, price, legality, or debug controls are displayed.
- [x] No new frontend dependencies were added.

Deferred beyond this slice:

- Opening user-selected deck files.
- Global search/add workflow.
- Card details surface.
- Mutation controls.
- Syntax-backed filtering.
- Full legality, statistics, printings, bulk edit, and version recovery behavior.

## See The Deck V0 Visual Review Checkpoint

- [x] Desktop layout was reviewed from the local Vite app.
- [x] Narrow layout was reviewed from the local Vite app.
- [x] Narrow-screen deck title and status controls no longer visibly overflow.
- [x] The grouped card workspace stays ahead of the secondary snapshot panel on stacked layouts.
- [x] The default screen remains deck-centered and avoids inactive workflow buttons.
- [x] Local fact coverage, missing/ambiguous fact plumbing, recommendations, scoring, price logic, legality claims, and debug data remain out of the default UI.

Deferred beyond this checkpoint:

- Human taste review beyond objective layout issues.
- Opening user-selected deck files.
- Global search/add workflow.
- Card details surface.

## Find And Add Cards V0

- [x] Functional Add Card entry point exists on the visible deck screen.
- [x] Search uses a tiny local TypeScript card fixture only.
- [x] Search results appear only after user-entered search text.
- [x] Plain local search checks candidate name, type line, category, tags, colors, and color identity.
- [x] The current-deck filter remains separate from global card search.
- [x] Add target can be set to mainboard or maybeboard.
- [x] Adding an existing same-card/same-zone/same-category entry increments quantity.
- [x] Adding a new selected card creates a visible deck entry.
- [x] Added cards update visible deck counts and grouped/table views.
- [x] Local additions mark the visible workspace as unsaved.
- [x] No recommendations, scoring, legality claims, price logic, live APIs, broad syntax expansion, backend persistence, or new dependencies were added.

Deferred beyond this slice:

- Saving UI edits to native `.mtgwdeck.json` files.
- Loading user-selected workspace files into the app.
- Wiring global search to the local Scryfall SQLite index.
- Syntax-backed global search UI.
- Validation warnings for added cards.

## Card Details Surface V0

- [x] Deck rows can open a factual card details panel.
- [x] Table rows can open the same factual card details panel.
- [x] Search results can open details without adding the card.
- [x] Details preserve the current deck, filter, and add-card context.
- [x] Details show only local fields already present in visible fixture data.
- [x] Details can be closed without mutating deck state.
- [x] No live price, legality claims, EDHREC rank, salt score, marketplace links, oracle tags, recommendations, scoring, role judgment, or card images were added.
- [x] No new frontend dependencies were added.

Deferred beyond this slice:

- Card images.
- Oracle text and oracle tags from local indexed data.
- Printing selector and foil state UI.
- Legality, price, rank, and salt fields backed by approved local data.
- Rich visual treatment beyond the functional v0 panel.

## Mechanical Deck Validation Surface V0

- [x] Sidebar shows a compact mechanical validation panel.
- [x] Commander presence is checked from current UI deck state.
- [x] Commander active card count is checked against 100.
- [x] Unresolved workspace entries are reported if present.
- [x] Duplicate non-basic active cards are reported if quantity exceeds one.
- [x] Basic lands are excluded from duplicate non-basic warnings.
- [x] Validation updates after visible add-card actions.
- [x] No recommendations, scoring, power-level claims, role counts, commander philosophy checks, price logic, legality claims, or card-quality judgments were added.
- [x] No new frontend dependencies were added.

Deferred beyond this slice:

- Wiring to persisted native workspace files.
- Wiring to the backend deck inspection report envelope.
- Broader structural audits such as land/ramp/draw/interaction ratios.
- Full legality enforcement.
- User-facing validation copy polish after human visual review.

## Deckbuilder UI Logic Extraction V0

- [x] Pure grouping helper logic is outside `App.tsx`.
- [x] Pure current-deck filter helper logic is outside `App.tsx`.
- [x] Pure local search matching helper logic is outside `App.tsx`.
- [x] Pure add-entry projection helper logic is outside `App.tsx`.
- [x] Pure card-details mapping helper logic is outside `App.tsx`.
- [x] Pure mechanical validation helper logic is outside `App.tsx`.
- [x] `App.tsx` remains responsible for rendering and state orchestration.
- [x] No visible behavior, new UI capability, persistence, backend wiring, or new dependency was added.

Deferred beyond this slice:

- Dedicated frontend unit tests for helper functions.
- Splitting React components into smaller files.
- Wiring helpers to persisted native workspace files or backend report payloads.

## User Reviewer Skill V0

- [x] Project-local `user-reviewer` skill exists.
- [x] Deckbuilder user review rubric exists.
- [x] Reviewer output includes ratings, clutter risk, pass items, polish items, blockers, and a suggested next visual change.
- [x] Skill preserves human validation as the final taste authority.
- [x] Skill avoids deck strategy, recommendation, scoring, legality, pricing, and power-level judgment.

Deferred beyond this slice:

- Running a user-review pass against the current browser UI.
- Automating screenshot capture for reviewer input.
- Turning reviewer feedback into implementation without human checkpoint.

## Current Deckbuilder UI User Review V0

- [x] Dated user-review report exists for the current fixture-backed deckbuilder UI.
- [x] Report rates overall readiness, clarity, visual calm, deckbuilder usefulness, hierarchy, and clutter risk.
- [x] Report separates pass items, polish items, blockers, and do-not-change guidance.
- [x] Report preserves human validation as the final visual/taste authority.
- [x] Report avoids deck strategy, recommendation, scoring, legality, pricing, and power-level judgment.

Deferred beyond this slice:

- Live in-browser human validation.
- Implementing the suggested visual consolidation.
- Adding automated screenshot capture to reviewer workflow.

## Current Deckbuilder UI Human Browser Pass V0

- [x] Human browser-pass notes are captured in the current UI review report.
- [x] Accepted function direction is recorded.
- [x] Organization and underexpressed layout concerns are recorded.
- [x] Mechanical-check corrections are recorded.
- [x] Card-details field correction is recorded.
- [x] Maybeboard collapsed-by-default preference is recorded.
- [x] Full-cardpool search trigger concern is recorded.
- [x] Next polish direction is updated toward deck-context consolidation.

Deferred beyond this slice:

- Implementing the visual polish changes.
- Adding visible remove-card controls.
- Adding card-level duplicate warning presentation.
- Implementing duplicate exception logic from local card rules/evidence.

## Deck Library Direction Capture V0

- [x] Deck library/home screen is documented as the app entry surface.
- [x] Open-deck workspace remains the primary editing screen after a deck is selected.
- [x] Local proxy utility visual reference is captured as calm/expressive style feel only.
- [x] Hosted visibility states, account behavior, cloud sync, and live services are excluded from the library requirements.
- [x] Deck library should support create/open saved local workspaces before the deck screen.

Deferred beyond this slice:

- Implementing a deck library route or UI screen.
- Wiring deck library to saved `.mtgwdeck.json` files.
- Designing final visuals for the deck library.
- Implementing safe deck deletion or remove-from-library behavior.

## Deck Library, Context Consolidation, And Save/Open UI V0

- [x] App opens to a deck library/home screen before the deck workspace.
- [x] Library lists available in-browser local deck workspaces.
- [x] Create-deck flow opens a new editable local deck workspace.
- [x] Open-file action accepts native `.mtgwdeck.json` workspace files through the browser file picker.
- [x] Save action downloads the current deck as native `.mtgwdeck.json`.
- [x] Malformed workspace files show clear local errors.
- [x] Current add-card, search, details, and count-update behavior is preserved.
- [x] Deck snapshot/context has moved below the main card workspace.
- [x] Maybeboard groups are collapsed by default when a deck is opened.
- [x] Successful background checks such as resolved names and no duplicate issues are not listed as default validation items.
- [x] Duplicate non-basic warnings are targeted to affected entries when present.
- [x] Card details no longer show `Zone` by default.
- [x] Local card search requires at least two free-text characters before showing results.
- [x] No new frontend dependencies, live APIs, cloud sync, recommendations, scoring, or strategic judgments were added.

Deferred beyond this slice:

- Persistent deck library storage across browser reloads.
- Scanning a local deck folder.
- Overwriting the original opened file path.
- Backend-to-frontend report wiring.
- Full local Scryfall search wiring in the frontend.
- Visible remove-card and quantity-edit controls.
- Final visual polish approval.

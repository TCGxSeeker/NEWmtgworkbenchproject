# Implementation Spec

## Goal

Build the MTG Workbench as an offline-first, deterministic Commander deckbuilding assistant. The project should import decklists, normalize cards against local data, analyze deck structure, flag issues, and produce explainable reports and recommendation drafts without depending on AI, live APIs, telemetry, or popularity metrics.

## Scope

This spec covers the intended MVP, completed foundation phases, and next planning phases. New feature work should update this document before implementation when it changes architecture, data contracts, or multi-file behavior.

The MVP should prove:

- Local decklist ingestion works.
- Card names normalize against local card data.
- Commander deck structure can be audited deterministically.
- Reports expose useful statistics, warnings, and human approval flags.
- The system functions without internet access.

## Non-Goals

- No chatbot wrapper.
- No EDHREC clone.
- No live API dependency for core analysis.
- No autonomous final deckbuilding.
- No card purchase automation.
- No production web UI before the CLI and deterministic engine are stable.
- No fresh price, legality, or newly released card claims unless backed by verified local snapshots.
- No recommendation ranking based on popularity, telemetry, repeat user behavior, or generic staple status.

## Source of Truth

Use the user interview answers, supplemental hand-off, and `docs/sources/MTG_PROJECT_MASTER_SEED.md` as the highest-priority product sources. If repo files conflict with them, prefer these sources and record the conflict in `docs/codex/DECISION_LOG.md`.

Current repository inspection found project operating files, source seed docs, tiny raw fixtures, Python parser/search source, tests, local Scryfall indexing support, a free frontend tooling scaffold, native workspace support, factual deck inspection reports, role evidence plumbing, and relationship primitive/report/pair-inspection foundations. The recommender, scoring rubric, strategic deck analysis, finished UI, and full curated project data are still future work. Missing facts should become TODOs or fixtures, not invented details.

Current baseline: from `G:\Documents\New MTG project`, the full Python suite passes with 344 tests after Deck Library, Context Consolidation, and Save/Open UI v0.

## Key Decisions Before Building

- Approved runtime: Python CLI, because the MVP needs local parsing, deterministic tests, simple fixtures, and portable offline behavior.
- Phase 2 command: `mtg parse <decklist_path> --cards <card_snapshot_path>`.
- Future commands: `mtg audit` and `mtg final-check` after structural audit exists.
- Proposed data style: YAML for editable rules and profiles, CSV for decklist/ownership table inputs, JSON for local card snapshots and machine-readable report outputs, Markdown for doctrine, source notes, and future rendered reports.
- Scryfall usage: approved manual bulk-data snapshot ingestion into `data/raw/scryfall/`; not runtime analysis and not an API dependency for parser/normalizer behavior.
- UI: future phase only, after CLI behavior and report outputs are stable.

These are proposed decisions, not irreversible implementation commitments.

## Files Likely Involved

Planning files:

- `docs/codex/PROJECT_BRIEF.md`
- `docs/codex/IMPLEMENTATION_SPEC.md`
- `docs/codex/VERIFICATION_PLAN.md`
- `docs/codex/HUMAN_VALIDATION_ZONES.md`
- `docs/codex/AUTOMATION_DECISIONS.md`
- `docs/codex/DECISION_LOG.md`
- `docs/codex/GOTCHAS.md`
- `docs/rules/DATA_CONTRACTS.md`
- `docs/sources/MTG_PROJECT_MASTER_SEED.md`

Future implementation files:

```text
src/mtg_workbench/
  cli/
  cards/
  decks/
  analysis/
  recommendations/
  rules/
  reports/
  data/
  utils/
data/
  cards/
  decks/
  owned/
  commander_profiles/
  packages/
  templates/
  sources/
tests/
  fixtures/
  normalization/
  analysis/
  recommendations/
  reports/
```

Product planning files:

```text
docs/product/deckbuilder/
  DECKBUILDER_ROADMAP.md
  MAIN_SCREEN_REQUIREMENTS.md
  DECK_MODEL_REQUIREMENTS.md
  VIEW_MODES_REQUIREMENTS.md
  GROUP_SORT_FILTER_REQUIREMENTS.md
  SEARCH_WORKSPACE_REQUIREMENTS.md
  CARD_ACTIONS_REQUIREMENTS.md
  STATS_AND_PROBABILITY_REQUIREMENTS.md
  IMPORT_EXPORT_REQUIREMENTS.md
  UI_NON_GOALS.md
  OPEN_QUESTIONS.md
```

Tooling files:

```text
docs/codex/TOOLING_PLAN.md
apps/deckbuilder-ui/
```

Phase 1 seed and contract fixtures:

```text
data/raw/cards/
data/raw/decklists/
data/raw/owned/
data/raw/commander_profiles/
data/raw/roles/
data/raw/packages/
data/raw/templates/
data/raw/budget/
data/raw/validation/
data/raw/reports/
data/raw/regression_tests/
data/raw/scryfall/
```

## MVP User Loop

1. Import a local Commander decklist.
2. Parse quantities, commander markers, main deck, categories, lands, and maybeboard where present.
3. Normalize card names against a local card snapshot.
4. Report unknown cards instead of guessing.
5. Analyze deck structure.
6. Check color identity, quantities, duplicates, curve, land count, ramp, draw, interaction, protection, engines, payoffs, win conditions, budget, and ownership constraints where local data exists.
7. Generate an audit report.
8. Generate a final-check packet with human validation flags.
9. Capture corrections as gotchas and future regression tests.

## Domain Model

| Object | Purpose | Key Fields | Populated By | Consumed By |
| --- | --- | --- | --- | --- |
| `Card` | Local card facts | name, aliases, mana value, colors, color identity, type line, Oracle text, prices snapshot, legality snapshot | local card snapshot, overrides | normalization, analysis, reports |
| `Deck` | Imported deck state | commander, main, maybeboard, categories, source path | deck parser | all analysis passes |
| `CommanderProfile` | Commander plan and constraints | commander, gameplan, colors, key roles, forbidden pivots | local YAML profile | plan checks, recommendations |
| `DeckAnalysis` | Audit result | counts, curve, warnings, role totals, validation results | analysis passes | reports, final-check |
| `RoleTag` | Card function in context | card, role, confidence, source, notes | local rules, overrides | role counts, recommendations |
| `Package` | Synergy/combo package | name, cards, purpose, required pieces, risks | local YAML package files | package detection |
| `BudgetProfile` | Budget constraints | card cap, deck cap, exception policy | local YAML | budget checks |
| `OwnershipProfile` | Owned/on-hand data | card name, quantity, location, proxy policy | CSV/local files | ownership checks |
| `Recommendation` | Draft add/cut proposal | add, cut, reason, impacts, confidence, risks, approval flag | recommendation engine | recommendation reports |
| `ValidationResult` | Check result | check id, status, evidence, severity, human review flag | validation passes | final-check |
| `AuditReport` | User-facing output | summary, stats, warnings, checklist, draft recommendations | report generator | CLI output, future UI |

## Deterministic Analysis Passes

The engine should be built in small passes:

1. Decklist parsing.
2. Card name normalization.
3. Quantity validation.
4. Duplicate detection.
5. Commander detection.
6. Color identity validation.
7. Local legality validation if local legality data exists.
8. Mana curve and mana value distribution.
9. Mana source and color pip analysis.
10. Land, ramp, draw, interaction, protection, engine, payoff, and win-condition audits.
11. Role/category counting.
12. Package detection.
13. Commander plan detection.
14. Budget threshold checks.
15. Ownership/on-hand checks.
16. Human validation trigger checks.
17. Report generation.

## Recommendation Rules

Recommendations are drafts, not final authority. They must cite local rules, local data, or user-approved exceptions.

A recommendation should evaluate whether a candidate:

- Supports the commander plan.
- Preserves or improves an existing package.
- Fills a missing role.
- Improves speed, consistency, protection, interaction, card flow, or closing power.
- Respects budget and ownership mode.
- Avoids unnecessary staples.
- Avoids diluting the primary plan.
- Has a clear cut candidate or role reason.
- Has identifiable risks and verification notes.

## Rules-As-Data Plan

| Artifact | Format | Location |
| --- | --- | --- |
| Deckbuilding templates | YAML | `data/templates/` |
| Bracket and power assumptions | YAML/Markdown | `docs/rules/` or `data/sources/` |
| Budget thresholds | YAML | `data/sources/` |
| Role definitions | YAML | `data/sources/` |
| Package definitions | YAML | `data/packages/` |
| Recommendation weights | YAML | `data/sources/` |
| Human validation triggers | YAML | `data/sources/` |
| Card tagging overrides | YAML or CSV | `data/cards/` |
| Commander profiles | YAML | `data/commander_profiles/` |
| Ownership/on-hand lists | CSV | `data/owned/` |
| Report templates | Markdown | `docs/reports/` |

## Implementation Steps

### Phase 0: Planning Baseline

Status: completed. Definition of done: docs agree on offline-first behavior, human validation zones, current feature/code status, and visible open questions.

### Phase 1: Local Data Contracts And Fixtures

Create minimal local fixtures and schemas for cards, decklists, ownership, commander profiles, roles, packages, templates, budget profiles, validation triggers, report outputs, and generic regression tests. Definition of done: `docs/rules/DATA_CONTRACTS.md` defines the formats, fixtures exist locally, structured fixtures can be syntax-checked without internet, and doctrine files are not treated as parser/card inputs.

### Phase 2: Decklist Parser And Normalizer

Implement import parsing and card-name normalization against tiny local fixtures only. Definition of done: plain text and CSV decklists parse correctly, quantities are preserved, commanders are detected when marked, aliases and case-insensitive names normalize to local snapshot display names, unknown cards are reported rather than guessed, duplicate known non-basic cards produce warnings, and stable JSON output is available from the CLI.

Phase 2 must not add API calls, external services, recommendation logic, structural audit logic beyond basic validation warnings, UI, or card-specific deckbuilding conclusions.

### Manual Scryfall Bulk Snapshot

The project may store manually fetched Scryfall bulk data under `data/raw/scryfall/` as raw local source snapshots. Snapshot payloads are intentionally ignored by Git because they are large. The tracked repository should keep only documentation and small manifests. Runtime features must continue to work from local files and must not call Scryfall directly unless a future user-approved ingestion command is built.

### Phase Index-1: Local Scryfall SQLite Index

Build `data/processed/scryfall/cards.sqlite` from the local Scryfall bulk snapshot. The indexer should process all local bulk types currently stored: oracle cards, default cards, all cards, unique artwork, rulings, oracle tags, and art tags. This is an offline ingestion step only. It must not call Scryfall and must not implement recommendation logic.

Keep the generated index compact. Oracle cards and tags should receive full-text indexes for syntax-search planning. Print rows should be stored with indexed columns and name lookup rows rather than a full print-level FTS copy, because the local machine has limited free disk space.

### Phase Search-1: Local Syntax Search Planner

Implement a read-only local search command over `data/processed/scryfall/cards.sqlite`. The first supported syntax subset should be bare text, `o:`/`oracle:`, `t:`/`type:`, `otag:`, `ci:`/`id:`, and `mv:`/`cmc:` comparisons. Definition of done: tiny SQLite fixture tests prove tag-first `otag:` resolution, card filtering, unsupported syntax reporting, and stable JSON output.

Phase Search-1 must not call external APIs, implement recommendations, infer deckbuilding quality, or claim data freshness beyond the local snapshot manifest.

Search is a substrate, not the product center. It supports future in-app search, card lookup, filtered browsing, and recommendation candidate pools. The long-term in-app search should become Scryfall-like enough to be useful locally, but the Workbench should not become an offline Scryfall clone and should not be designed around search-first workflows.

Current command:

```powershell
$env:PYTHONPATH='src'
python -m mtg_workbench.cli search "otag:burn-creature ci:r mv<=2" --index data/processed/scryfall/cards.sqlite
```

### Phase Search-2: Scoped Local Search Filters

Status: completed for the already specified filters: `legal:commander`, `usd<=N`, `r:<rarity>`, `set:<code>`, and `is:commander`. Definition of done: Search-2 tests are required passing tests, the full suite passes, and CLI smoke checks run against the local SQLite index.

Do not expand into broad Scryfall syntax coverage unless explicitly requested. Unsupported syntax should continue to return clear unsupported-syntax messages.

Implemented behavior: Search-2 reads legality and price from the local indexed JSON fields, rarity/set/commander-candidate from indexed columns, and continues intersecting multiple clauses in one query.

### Phase Product-1: Main Deckbuilder Workspace Planning

Use `docs/product/deckbuilder/` as the product requirements source for the first UI surface. The deckbuilder is the primary user screen; search, stats, reports, and probability tools should support this workspace rather than replace it.

Definition of done: requirements exist for deck model contracts, main screen layout, view modes, group/sort/filter behavior, search workspace, card actions, stats/probability tools, import/export, UI non-goals, and open questions.

### Phase Product-2: Deckbuilder Foundation v0 Planning

Status: planning scaffold prepared; implementation not started.

Create the first implementation-ready planning layer for the main deckbuilder workspace without building UI code. Definition of done: `DECKBUILDER_FOUNDATION_V0.md`, `MAIN_SCREEN_V0.md`, `DECK_WORKSPACE_MODEL_V0.md`, `DECKBUILDER_INTERACTIONS_V0.md`, and `DECKBUILDER_ACCEPTANCE_CHECKLIST.md` define the centered workspace, editable deck model, planned interactions, implementation boundaries, and planning-readiness checks.

### Phase Product-3: Deck Workspace Model v0

Status: implemented as the first Deckbuilder Foundation code slice; no UI code, reports, recommendations, scoring logic, or frontend dependencies were added.

Implement the app-native editable deck workspace model without UI code. Definition of done: `src/mtg_workbench/deckbuilder/` defines workspace and entry dataclasses, native `.mtgwdeck.json` serialization, lightweight shape validation, clear malformed-file errors, and tests proving empty workspace creation, zone preservation, unknown-card preservation, categories/tags/notes, stable JSON round trips, and missing-field failures.

Native workspace files preserve deckbuilding state that import/export formats cannot represent. Plain text, CSV, Archidekt-style, and future external formats remain boundaries for import/export rather than the saved workspace source of truth.

### Phase Product-4: Deck Workspace Mutations v0

Status: implemented as an in-memory Deckbuilder Foundation slice; no UI code, reports, recommendations, scoring logic, or frontend dependencies were added.

Implement focused in-memory mutation helpers for `DeckWorkspace` objects without UI code, reports, recommendations, scoring logic, frontend dependencies, or full Commander legality validation. Definition of done: `src/mtg_workbench/deckbuilder/mutations.py` can add, remove, increase, decrease, move zones, set commander, move categories, update tags, and update notes while preserving unresolved entries, applying the v0 duplicate-add policy, generating missing entry ids, marking the workspace dirty, updating `updated_at`, and keeping native JSON round trips valid.

The v0 mutation style should mutate the passed `DeckWorkspace` in place and return it for simple caller chaining. Save/load should remain clean unless a mutation has been applied after loading.

### Phase Product-4A: Deck Workspace Mutation CLI v0

Status: implemented and verified.

Expose a small safe subset of existing workspace mutation helpers through local file-based CLI commands. Definition of done: commands can add a card, remove an entry, increase quantity, decrease quantity, move an entry between commander/mainboard/maybeboard, and set commander for native `.mtgwdeck.json` files; each command requires an explicit `--output`, writes a native workspace, emits a stable JSON summary, and has focused tests against tiny temporary workspaces.

Deck Workspace Mutation CLI v0 must not add UI, frontend dependencies, deck analysis, deck-level role totals, strategic validation, recommendations, scoring, live APIs, telemetry, hosted services, AI/LLM calls, external deckbuilder formats, or new dependencies.

### Phase Product-4B: Category Metadata Mutation CLI v0

Status: implemented and verified.

Expose explicit file-based CLI wrappers for the existing category metadata helpers. Definition of done: commands can set or clear imported category, normalized category, generic category hint, category origin, secondary tags, and all category metadata for entries in native `.mtgwdeck.json` files; each command requires an explicit `--output`, preserves the grouping `categories` field unless a future grouping command is used, emits stable JSON summaries, and has focused tests against tiny temporary workspaces.

This slice does not expose deck-specific primary-role assignment. That field represents future deck-context truth and should remain out of the broad mechanical CLI until a dedicated human-approved role-editing slice exists.

Category Metadata Mutation CLI v0 must not add UI, frontend dependencies, deck analysis, deck-level role totals, strategic validation, recommendations, scoring, live APIs, telemetry, hosted services, AI/LLM calls, external deckbuilder formats, or new dependencies.

### Phase Product-4C: Entry Annotation CLI v0

Status: implemented and verified.

Expose explicit file-based CLI wrappers for existing entry note and tag helpers. Definition of done: commands can set or clear entry notes, replace tags, add tags, and remove tags for entries in native `.mtgwdeck.json` files; each command requires an explicit `--output`, emits stable JSON summaries, preserves zones and quantities, and has focused tests.

Entry Annotation CLI v0 must not add UI, frontend dependencies, deck analysis, deck-level role totals, strategic validation, recommendations, scoring, live APIs, telemetry, hosted services, AI/LLM calls, external deckbuilder formats, or new dependencies.

### Phase Product-4D: Deck Workspace View Projection v0

Status: implemented and verified.

Create a read-only projection layer that prepares existing native workspace entries for future deckbuilder grouping, sorting, and current-deck text filtering without app UI. Definition of done: a small module can project a `DeckWorkspace` into stable grouped output for `full_deck`, `zone`, and `category`; sort visible entries by `alphabet`, `quantity`, `category`, or `zone`; filter current deck entries by local workspace text fields; preserve unresolved entries; and leave the input workspace unchanged.

Category grouping may use multiple category memberships when an entry has multiple `categories`; projection-level totals should remain explicit so callers do not mistake view grouping for deck analysis.

Deck Workspace View Projection v0 must not add UI, frontend dependencies, card-fact lookup, deck analysis, deck-level role totals, strategic validation, recommendations, scoring, live APIs, telemetry, hosted services, AI/LLM calls, external deckbuilder formats, or new dependencies.

### Phase Product-4E: Workspace View CLI v0

Status: implemented and verified.

Expose Deck Workspace View Projection v0 through a read-only local CLI command. Definition of done: `workspace-view <deck.mtgwdeck.json>` emits stable projection JSON, accepts `--group-by`, `--sort-by`, `--filter`, and repeated `--zone` options, validates native workspace input, reports unsupported projection options clearly, writes no output file, and has focused tests against tiny temporary workspaces.

Workspace View CLI v0 must not add UI, frontend dependencies, card-fact lookup, deck analysis, deck-level role totals, strategic validation, recommendations, scoring, live APIs, telemetry, hosted services, AI/LLM calls, external deckbuilder formats, or new dependencies.

### Phase Product-4F: Card-Fact-Backed Workspace Projection v0

Status: implemented and verified.

Expand read-only workspace projection with factual type and mana-value grouping/sorting when an explicit local card source is supplied. Definition of done: projection supports `type` and `mana_value` group/sort modes, uses `CardFactLookupReport` results rather than re-resolving records, places missing and ambiguous fact lookups into explicit status buckets, exposes found/missing/ambiguous lookup counts, preserves unresolved entries, leaves input workspaces unchanged, and updates `workspace-view` so callers can pass `--cards` or `--card-records`.

If `type` or `mana_value` projection is requested without local card facts, it must fail clearly instead of guessing from saved entry names or categories.

Card-Fact-Backed Workspace Projection v0 must not add UI, frontend dependencies, deck analysis, deck-level role totals, strategic validation, recommendations, scoring, live APIs, telemetry, hosted services, AI/LLM calls, external deckbuilder formats, syntax filtering, or new dependencies.

### Phase Product-4G: Color Identity Workspace Projection v0

Status: implemented and verified.

Expand read-only workspace projection with factual color and color-identity grouping/sorting when an explicit local card source is supplied. Definition of done: projection supports `color` and `color_identity` group/sort modes, reads `colors` and `color_identity` only from found local card facts, distinguishes `Colorless` from missing/unknown color data, keeps missing and ambiguous fact lookups in explicit status buckets, preserves unresolved entries, leaves input workspaces unchanged, and the existing `workspace-view --cards/--card-records` command can use the new modes.

V0 behavior: `color` grouping may place a multicolor card into multiple color groups. `color_identity` grouping uses the exact WUBRG-ordered identity combination as one group, such as `UG`, so identity filtering remains comparable for future Commander work.

Color Identity Workspace Projection v0 must not add UI, frontend dependencies, deck analysis, deck-level role totals, strategic validation, recommendations, scoring, live APIs, telemetry, hosted services, AI/LLM calls, external deckbuilder formats, syntax filtering, price logic, or new dependencies.

### Phase Product-4H: Workspace View Fixture Smoke v0

Status: implemented and verified.

Freeze one tiny end-to-end `workspace-view` contract before projection behavior grows again. Definition of done: a native workspace fixture, local card-record fixture, exact expected JSON fixture, and smoke test prove fact-backed color-identity grouping and mana-value sorting through the CLI; repeated runs produce identical JSON; the source workspace file is not mutated; missing and ambiguous facts stay visible; and the payload contains no strategic analysis or recommendation fields.

Workspace View Fixture Smoke v0 must not add UI, frontend dependencies, deck analysis, deck-level role totals, strategic validation, recommendations, scoring, live APIs, telemetry, hosted services, AI/LLM calls, external deckbuilder formats, syntax filtering, price logic, or new dependencies.

### Phase Product-4I: Workspace Projection Contract Docs v0

Status: implemented and verified.

Document `deck_workspace_view_projection.v0` as the current consumer contract for future deckbuilder screens. Definition of done: a concise contract doc identifies the projection purpose, producer, intended consumers, top-level fields, group fields, entry fields, grouping/sorting/filtering semantics, grouped-total caveats, fact-status buckets, fixture-backed example, and UI visibility doctrine.

This slice is documentation only. It must not add UI, frontend dependencies, code behavior, deck analysis, deck-level role totals, strategic validation, recommendations, scoring, live APIs, telemetry, hosted services, AI/LLM calls, external deckbuilder formats, syntax filtering, price logic, or new dependencies.

### Phase Product-4J: See The Deck v0

Status: implemented and verified.

Create the first visible deck screen from the existing frontend scaffold and the documented workspace projection contract. Definition of done: the app opens to one calm deck workspace; shows deck name, format, saved state, useful counts, grouped card rows, and a table alternative; supports local current-deck text filtering and group collapse/expand; uses only fixture-backed projection data; and keeps local fact coverage, recommendation content, scoring, legality claims, charts, inactive action buttons, and debug plumbing out of the default UI.

This slice may update existing frontend scaffold files and add tiny local frontend fixture data. It must not add frontend dependencies, backend behavior, live APIs, telemetry, hosted services, AI/LLM calls, deck analysis, deck-level role totals, strategic validation, recommendations, scoring, price logic, syntax filtering, import/export wiring, card mutation wiring, or generated build output.

### Phase Product-4K: See The Deck v0 Visual Review Checkpoint

Status: implemented and verified.

Review the first visible deck screen against the product's calm, readable,
deck-centered UI direction before expanding into search/add workflows.
Definition of done: desktop and narrow layouts render without obvious
horizontal overflow; the card workspace remains the primary surface; no
inactive controls, local fact/debug coverage, recommendation content, scoring,
price logic, legality claims, or strategic analysis appear in the default UI;
and any visual changes remain small enough for human review.

This checkpoint may update existing frontend styling and current-status docs.
It must not add frontend dependencies, app routing, backend behavior, live APIs,
telemetry, hosted services, AI/LLM calls, deck analysis, deck-level role totals,
recommendations, scoring, price logic, syntax filtering, import/export wiring,
card mutation wiring, or generated build output.

### Phase Product-4L: Find And Add Cards v0

Status: implemented and verified.

Add the smallest visible search/add workflow to the existing fixture-backed
deckbuilder screen. Definition of done: the screen has a functional add-card
entry point, searches a tiny local card fixture without network access, shows
deterministic local results only after user input, adds an explicitly selected
card into the visible deck state, preserves quantities by incrementing an
existing same-card/same-zone entry when appropriate, marks the visible workspace
as unsaved after local edits, and keeps the current-deck filter distinct from
global card search.

This slice may update existing frontend files and add tiny TypeScript fixture
data. It must not add frontend dependencies, backend behavior, persistence,
file writes, live APIs, telemetry, hosted services, AI/LLM calls, deck analysis,
recommendations, scoring, price logic, legality claims, broad Scryfall syntax
coverage, import/export wiring, full mutation command wiring, or generated
build output.

### Phase Product-4M: Card Details Surface v0

Status: implemented and verified.

Add the smallest selected-card details surface to the existing fixture-backed
deckbuilder screen. Definition of done: an explicitly selected deck row, table
row, or search result can open a focused details panel; the panel preserves the
current deck/search context; it shows only factual local fields already present
in visible deck entries or tiny search fixture data; and it can be dismissed
without changing deck state.

V0 details may show card name, type line, mana value, color identity, current
zone, quantity, categories, tags, and notes when locally available. This slice
must not add frontend dependencies, backend persistence, live APIs, telemetry,
hosted services, AI/LLM calls, deck analysis, recommendations, scoring, price
logic, legality claims, EDHREC rank, salt score, marketplace links, oracle tags,
printing management, card images, broad Scryfall syntax expansion, or generated
build output.

### Phase Product-4N: Mechanical Deck Validation Surface v0

Status: implemented and verified.

Add the smallest visible mechanical validation surface to the existing
fixture-backed deckbuilder screen. Definition of done: the screen summarizes
current Commander deck readiness from local UI state only; reports missing
commander, active card count mismatch against 100, unresolved card entries, and
duplicate non-basic active cards; updates after visible add-card actions; and
keeps validation short enough to support the deck workspace rather than replace
it.

This slice must not add frontend dependencies, backend persistence, live APIs,
telemetry, hosted services, AI/LLM calls, deck analysis beyond the listed
mechanical checks, recommendations, scoring, power-level claims, commander
philosophy checks, role counts, package detection, price logic, legality claims,
card-quality judgments, or generated build output.

### Phase Product-4O: Deckbuilder UI Logic Extraction v0

Status: implemented and verified.

Move pure deckbuilder UI helper logic out of the main React component without
changing visible behavior. Definition of done: grouping, filtering, search
matching, add-entry projection, card-details mapping, formatting, and mechanical
validation helpers live in a small TypeScript module; `App.tsx` remains focused
on rendering and state orchestration; and the current deckbuilder UI behaves the
same under build/lint verification.

This slice must not add new UI capabilities, frontend dependencies, backend
persistence, live APIs, telemetry, hosted services, AI/LLM calls, deck analysis,
recommendations, scoring, power-level claims, commander philosophy checks, role
counts, package detection, price logic, legality claims, card-quality judgments,
or generated build output.

### Phase Product-4P: User Reviewer Skill v0

Status: implemented and verified.

Create a project-local user-reviewer skill and deckbuilder review rubric for
completed UI or visualization checkpoints. Definition of done: the skill can be
invoked to review a completed section, produce ratings, identify clutter and
clarity risks, distinguish blocking issues from polish, and preserve the rule
that human review remains the final taste authority.

This slice must not implement app UI, change product behavior, add frontend
dependencies, create automated screenshots, replace human validation, add live
services, add AI/LLM product behavior, score deck quality, or make strategic MTG
recommendations.

### Phase Product-4Q: Current Deckbuilder UI User Review v0

Status: implemented and verified.

Run the project-local user-reviewer workflow against the current fixture-backed
deckbuilder UI checkpoint. Definition of done: a dated review report records
the reviewed section, assumed user goal, ratings, clutter risk, pass items,
polish items, blockers, suggested next visual change, and human validation
status.

This slice is documentation/review only. It must not implement app UI, change
product behavior, add frontend dependencies, automate screenshots, replace human
validation, add live services, add AI/LLM product behavior, score deck quality,
or make strategic MTG recommendations.

### Phase Product-4R: Current Deckbuilder UI Human Browser Pass v0

Status: implemented and verified.

Capture the user's in-browser review of the current fixture-backed deckbuilder
UI. Definition of done: durable notes record accepted functions, organization
issues, visual-quality concerns, mechanical-check corrections, card-detail
field corrections, maybeboard display preference, search-trigger concerns, and
the next recommended polish direction.

This slice is documentation/review only. It must not implement app UI, change
product behavior, add frontend dependencies, replace human validation, add live
services, add AI/LLM product behavior, score deck quality, or make strategic MTG
recommendations.

### Phase Product-4S: Deck Library Direction Capture v0

Status: documented.

Record that MTG Workbench should open to a local deck library/home screen before
an individual deck workspace. The open-deck screen remains the primary editing
surface after selection, but the app shell should support a calm, expressive
library flow for creating and opening saved local decks.

Reference and requirements:

- `docs/product/deckbuilder/DECK_LIBRARY_REQUIREMENTS.md`
- `docs/product/deckbuilder/reference/VISUAL_REFERENCE_NOTES.md`

This slice is documentation only. It must not implement the deck library UI,
add account behavior, cloud sync, hosted visibility, live services,
recommendations, scoring, or a stats dashboard.

### Phase Product-4T: Deck Library, Context Consolidation, and Save/Open UI v0

Status: implemented and verified.

Implement the first browser-local app flow across the three next deckbuilder
workflow items:

1. Deck library entry: show a calm local home screen before the open-deck
   workspace, with create-deck and open existing workspace entry points.
2. Deck context consolidation: keep the deck card workspace primary, move
   snapshot/validation context below or out of the cramped side area, collapse
   maybeboard by default, hide successful background checks, and remove `Zone`
   from basic card details.
3. Save/open workspace UI: support opening a user-selected `.mtgwdeck.json`
   file and downloading the current workspace as native `.mtgwdeck.json`.

Implementation assumptions:

- Browser V0 cannot scan folders or overwrite arbitrary local files directly.
  Use a file input for open and a browser download for save/export.
- Preserve the current fixture-backed add/search/details/count-update behavior.
- Keep full-cardpool search safe by avoiding broad one-character free-text
  result bursts.
- Do not add frontend dependencies, backend server behavior, live APIs,
  recommendations, scoring, strategic judgments, account behavior, cloud sync,
  or hosted visibility states.

Verification:

- `npm run build` and `npm run lint` in `apps/deckbuilder-ui`.
- `python -m unittest discover -s tests`.
- `git diff --check`.
- Manual browser pass for the new library/open-deck flow.

Implemented scope:

- App opens to a browser-local deck library/home screen.
- Users can create a new in-browser local deck.
- Users can open a selected native `.mtgwdeck.json` file.
- Users can download the current deck as native `.mtgwdeck.json`.
- The open-deck screen keeps cards as the primary workspace and moves deck
  snapshot/mechanical warnings below the main card area.
- Maybeboard groups collapse by default when a deck is opened.
- Card details hide `Zone` by default.
- Search waits for at least two free-text characters before returning results.

### Phase Product-5: Deck Workspace Import/Export v0

Status: implemented for plain text import/export; no UI code, frontend dependencies, reports, recommendations, live APIs, telemetry, or full legality validation were added.

Implement local plain text conversion for native deck workspaces without UI code, frontend dependencies, reports, recommendations, online dependencies, live APIs, telemetry, or full legality validation. Definition of done: `src/mtg_workbench/deckbuilder/import_export.py` can import plain text decklists into `DeckWorkspace`, export `DeckWorkspace` objects to clean plain text, preserve quantities, zones, unresolved cards, conservative categories, and native save/load behavior, and tests prove import, export, save/load/export, unresolved fallback, and no-network behavior.

Plain text remains an import/export boundary format. `.mtgwdeck.json` remains the saved workspace source of truth.

### Phase Product-5A: Native Workspace Import/Export CLI v0

Status: implemented and verified.

Expose the existing plain text import/export helpers through minimal local CLI commands. Definition of done: `python -m mtg_workbench.cli workspace-import <decklist.txt> --output <deck.mtgwdeck.json>` writes a native workspace file, `python -m mtg_workbench.cli workspace-export <deck.mtgwdeck.json> --output <decklist.txt>` writes a plain text decklist, both commands emit stable JSON summaries, tests cover tiny fixtures, and native workspace files remain the source of truth while plain text remains a boundary format.

Native Workspace Import/Export CLI v0 must not add UI, frontend dependencies, reports beyond command summaries, strategic analysis, deck-level role totals, recommendations, scoring, live APIs, telemetry, hosted services, AI/LLM calls, external deckbuilder formats, or new dependencies.

### Phase Product-6: Category Taxonomy v0

Status: implemented as a rules/data foundation slice; no code auto-categorization, UI, frontend dependencies, recommendations, large datasets, online dependencies, telemetry, or deck analysis were added.

Define a controlled category language for deckbuilder card roles and imported decklist headers. Definition of done: `docs/rules/CATEGORY_TAXONOMY.md` defines canonical categories, aliases, normalization doctrine, imported/user category preservation, future category field distinctions, and deferred behavior; `data/fixtures/categories/category_taxonomy.example.yaml` provides a tiny local example fixture.

Generic card category is a hint. Deck-specific role is the truth.

### Phase Hygiene-1: Test Command Hygiene v0

Status: implemented.

Make the canonical test command work from the repository root without manual environment setup. Definition of done: `python -m unittest discover -s tests` imports the `src/` package through repository-local setup, passes the full test suite, and does not add external dependencies.

### Phase Product-7: Category Taxonomy Loader/Normalizer v0

Status: implemented as a rules/data utility slice.

Load the tiny local category taxonomy fixture and normalize category labels without mutating deck entries. Definition of done: `src/mtg_workbench/deckbuilder/categories.py` can load canonical categories and aliases from the local fixture, normalize labels case-insensitively with repeated-space cleanup, preserve the original input label in the result, report unknown labels without guessing, and validate alias targets. No card auto-categorization, deck analysis, recommendation logic, UI, frontend dependency, live API, telemetry, or large dataset ingestion is included.

### Phase Product-8: Deck Entry Category Metadata v0

Status: implemented.

Preserve category provenance on native deck entries so imported/user labels and taxonomy-normalized categories can coexist. Definition of done: `DeckEntry` supports imported category, normalized category, generic category hint, future deck-specific primary role, secondary tags, and category origin fields; native `.mtgwdeck.json` round trips preserve those fields; validation reports malformed metadata clearly; mutations can create entries with metadata; plain text import can use the local category taxonomy when supplied; and tests prove alias-backed category import without implementing auto-categorization, role counting, deck analysis, recommendations, UI, live APIs, or large datasets.

`categories` remains the compatibility grouping field for current deckbuilder behavior. Deck-specific primary role remains a future human-approved analysis concept, not a derived truth in this slice.

### Phase Product-9: Deck Workspace Category Editing Helpers v0

Status: implemented.

Add explicit in-memory mutation helpers for editing deck entry category metadata after import/add flows. Definition of done: helpers can set or clear imported category, normalized category, generic category hint, deck-specific primary role placeholder, and category origin; helpers can add, remove, replace, or clear secondary tags; every helper finds entries by `entry_id`, raises clear missing-entry errors, preserves the existing `categories` grouping field, marks the workspace dirty, updates `updated_at`, and keeps native workspace round trips valid.

If a category taxonomy is supplied, normalized categories may be validated as canonical taxonomy categories. Without a taxonomy, helpers preserve caller-supplied values without guessing or auto-normalizing. This phase must not add auto-categorization, role counting, recommendation logic, deck analysis, UI code, frontend dependencies, live APIs, telemetry, or large datasets.

### Phase Algorithm-1: Deterministic Deck Analysis Algorithm v0

Status: planned.

Design the local/offline rules-based algorithm before implementing deck analysis or recommendations. Definition of done: `docs/product/algorithm/DETERMINISTIC_DECK_ANALYSIS_ALGORITHM_V0.md` documents inputs, algorithm layers, mechanical validation, feature extraction, role/category classification, shell audit, commander thesis matching, package detection, candidate search, add/cut scoring, explanation output, phase plan, non-goals, and future acceptance criteria.

The algorithm plan must preserve core doctrine: Oracle text and local card data are evidence, generic category is a hint, deck-specific role is the truth, imported/user labels are preserved, recommendations must be explainable and reproducible, and `no_swap` is valid. This phase must not add analyzer code, recommendations, AI/LLM calls, live APIs, UI, frontend dependencies, telemetry, hosted services, popularity-based ranking, full combo solving, full judge legality, or full price optimization.

### Phase Algorithm-2: Role Rules v0

Status: implemented as a local rules-format scaffold.

Create the first local/offline role-rule format for future deterministic card-function classification. Definition of done: `docs/rules/ROLE_RULES.md` documents the purpose, taxonomy distinction, YAML schema, evidence scoring, explanation behavior, imported/user category preservation, deck-specific role deferral, UI visibility doctrine, and non-goals; `data/fixtures/roles/role_rules.example.yaml` defines a tiny example ruleset for Land, Ramp, Draw, Selection, Tutor, Interaction, Removal, Countermagic, Board Wipe, Protection, Recursion, Engine, Payoff, and Wincon.

Role Rules v0 must not add analyzer code, recommendations, candidate search, add/cut scoring, full deck analysis, AI/LLM calls, live APIs, telemetry, hosted services, frontend dependencies, UI code, large card-to-role datasets, full Scryfall auto-categorization, or primary-role enforcement.

### Phase Algorithm-3: Role Rules Loader v0

Status: implemented.

Build the smallest local loader for the Role Rules v0 fixture. Default assumptions: support only the tiny YAML subset first, use casefolded substring phrase matching with whitespace normalization, and combine scores with `highest_match` only. Do not implement additive capped scoring, card classification, deck analysis, recommendations, UI, candidate search, role enforcement, online dependencies, live APIs, telemetry, hosted services, frontend dependencies, or AI/LLM calls.

### Phase Algorithm-4: Role Evidence Matcher v0

Status: implemented.

Match explicit local `CardRoleFacts` against loaded role rules without performing deck analysis or workspace-wide classification. Definition of done: the matcher supports normalized Oracle text phrase matches, type-line matches, subtype matches, keyword matches, mana value constraints, exclusion rules, `highest_match` score selection, deterministic `RoleEvidenceMatch` output, and tests for matching, exclusion, constraints, and unmatched-role behavior.

Role Evidence Matcher v0 must not add recommendations, candidate search, add/cut scoring, full deck analysis, UI, frontend dependencies, online dependencies, live APIs, telemetry, hosted services, AI/LLM calls, or primary-role enforcement.

### Phase Algorithm-5: Role Evidence Report v0

Status: implemented.

Wrap role evidence matches in a small report object that keeps progressive-disclosure output boundaries. Definition of done: role evidence reports expose a concise `user_summary`, matched and unmatched role counts, best match, machine-readable evidence, optional explanations, and debug details only when explicitly requested.

Role Evidence Report v0 is not a full deck report, structural audit, recommendation report, candidate search surface, UI component, or primary-role classifier.

### Phase Algorithm-6: Card Facts Adapter v0

Status: implemented.

Create a small local/offline adapter that converts local or Scryfall-ish card record dictionaries into `CardRoleFacts` for the existing role evidence matcher. Definition of done: `card_record_to_role_facts(record)` maps name, Oracle text, type line, keywords, mana value, and conservative subtypes; two-faced `card_faces` records combine face Oracle text and type lines; missing optional data becomes empty strings, empty tuples, or `None`; missing name raises a clear `CardFactsError`; and tests prove the adapter output can feed `build_role_evidence_report`.

Card Facts Adapter v0 must not add deck analysis, recommendations, candidate search, add/cut scoring, primary-role selection, UI, frontend dependencies, online dependencies, live APIs, telemetry, hosted services, AI/LLM calls, or large dataset ingestion.

### Phase Algorithm-7: Card Role Evidence Pipeline v0

Status: implemented.

Create the smallest bridge from local or Scryfall-ish card records to `RoleEvidenceReport` objects. Definition of done: `card_record_to_role_evidence_report(record, ruleset)` converts one record through `card_record_to_role_facts` and `build_role_evidence_report`; `card_records_to_role_evidence_reports(records, ruleset)` preserves input order and returns a tuple; `include_unmatched` is passed through for advanced/debug reporting; and clear `CardFactsError` validation behavior is preserved.

Card Role Evidence Pipeline v0 must remain card-level evidence plumbing only. It must not add deck analysis, recommendations, candidate search, add/cut scoring, primary-role selection, UI, frontend dependencies, online dependencies, live APIs, telemetry, hosted services, AI/LLM calls, or large dataset ingestion.

### Phase Algorithm-8: Deck Skeleton Report v0

Status: implemented.

Create the first deterministic deck inventory report from `DeckWorkspace`. Definition of done: `build_deck_skeleton_report(workspace, card_records_by_name=None)` reports deck metadata, zone entry counts, zone quantity totals, active deck quantity, commander names, active category counts, unresolved entries, missing card-fact entries when local records are supplied, and known non-basic duplicate warnings only when local card facts confirm the duplicate is non-basic.

Deck Skeleton Report v0 must not make strategic quality judgments, perform deck-level role counting, infer missing card facts, implement recommendations, candidate search, add/cut scoring, commander philosophy checks, UI, frontend dependencies, online dependencies, live APIs, telemetry, hosted services, AI/LLM calls, or large dataset ingestion.

### Phase Algorithm-9: Structural Warnings v0

Status: implemented.

Create a mechanical warning report that consumes `DeckSkeletonReport` facts. Definition of done: `build_structural_warnings_report(skeleton_report)` reports missing Commander commander entries, Commander active quantity mismatches, unresolved entries, missing local card facts, and known non-basic duplicate warnings already proven by the skeleton report.

Structural Warnings v0 must not make strategic quality judgments, count deck-level roles, infer unavailable card facts, inspect raw card records independently, implement recommendations, candidate search, add/cut scoring, commander philosophy checks, UI, frontend dependencies, online dependencies, live APIs, telemetry, hosted services, AI/LLM calls, or large dataset ingestion.

### Phase Algorithm-10: Local Card Fact Lookup Bridge v0

Status: implemented.

Create a deterministic bridge from `DeckWorkspace` entries to local card fact records. Definition of done: lookup uses the existing `normalize_lookup_key` helper, accepts either supplied local card records or an existing `CardCatalog`, returns explicit `found`, `missing`, or `ambiguous` results, preserves entry order, reports missing and ambiguous data instead of guessing, and exposes found records by entry id for later report layers.

Local Card Fact Lookup Bridge v0 must not mutate workspaces, implement deck-level role counting, select primary roles, make strategic quality judgments, inspect live services, call APIs, add UI, add frontend dependencies, ingest large data, implement recommendations, candidate search, add/cut scoring, commander profiles, package analysis, price optimization, or combo solving.

### Phase Algorithm-11: Deck Inspection Report Envelope v0

Status: implemented.

Create a bounded report envelope that composes existing deck skeleton facts, mechanical structural warnings, optional local card fact lookup coverage, and optional card-level role evidence. Definition of done: `build_deck_inspection_report(...)` always builds the skeleton and structural warning reports, succeeds without a card source by marking lookup as not attempted, reports found/missing/ambiguous local card facts when a source is supplied, optionally emits card-level role evidence only for deterministically found records with a supplied ruleset, and keeps user summaries, machine evidence, and debug details separated.

Deck Inspection Report Envelope v0 must not mutate workspaces, implement deck-level role totals, select primary roles, make shell-quality or strategic judgments, create low-ramp/draw warnings, implement recommendations, candidate search, add/cut scoring, commander profiles, package analysis, UI, frontend dependencies, online dependencies, live APIs, telemetry, hosted services, AI/LLM calls, price optimization, or combo solving.

### Phase Algorithm-12: Deck Inspection Fixture Smoke v0

Status: implemented.

Create a stable end-to-end fixture for the factual deck inspection report envelope. Definition of done: tiny workspace and card-record fixtures produce a deterministic expected report, the fixture proves no network use, no workspace mutation, card fact coverage, optional found-card-only role evidence, and absence of forbidden strategic fields.

Deck Inspection Fixture Smoke v0 must not add product UI, live data, recommendation behavior, deck-quality claims, deck-level role totals, candidate search, add/cut scoring, package detection, commander analysis, online dependencies, telemetry, hosted services, or AI/LLM calls.

### Phase Algorithm-12A: Deck Inspection CLI v0

Status: implemented and verified.

Expose the existing factual deck inspection report envelope through the local Python CLI. Definition of done: `python -m mtg_workbench.cli inspect-deck <workspace.mtgwdeck.json>` loads a native deck workspace, emits stable JSON, optionally consumes a tiny local card-record fixture or local card catalog, optionally includes card-level role evidence only when local role rules are supplied, and keeps summary, machine evidence, and debug output separated.

Deck Inspection CLI v0 must not mutate workspaces, implement deck-level role totals, select primary roles, make shell-quality or strategic judgments, create low-ramp/draw warnings, implement recommendations, candidate search, add/cut scoring, commander profiles, package analysis, UI, frontend dependencies, online dependencies, live APIs, telemetry, hosted services, AI/LLM calls, price optimization, or combo solving.

### Phase Algorithm-12B: Deck Inspection CLI Polish v0

Status: implemented and verified.

Add small ergonomics to the factual inspection CLI without changing report semantics. Definition of done: `inspect-deck --summary-only` emits a compact factual summary, missing workspace/card source files return clear user-facing errors, debug output remains explicit, and tests prove summary-only output does not include nested report/debug payloads.

Deck Inspection CLI Polish v0 must not add deck-level role totals, strategic judgments, recommendations, scoring, UI, frontend dependencies, live APIs, telemetry, hosted services, AI/LLM calls, or new report semantics.

### Phase Algorithm-13: Card Relationship Primitives v0

Status: implemented as a planning and vocabulary contract.

Define the smallest deterministic vocabulary for factual relationships between deck entries before implementing relationship models or edge derivation. Definition of done: `docs/codex/CARD_RELATIONSHIP_PRIMITIVES_V0.md` documents the doctrine, behavior-interface direction, evidence contract, confidence bands, derivation boundaries, non-goals, and planned implementation order; `data/fixtures/relationships/card_relationship_primitives.example.json` locks a tiny machine-readable vocabulary fixture; tests verify the fixture contract.

Card Relationship Primitives v0 must not implement relationship derivation, all-pairs comparison, package detection, synergy scoring, recommendations, candidate search, add/cut scoring, commander analysis, deck-level role totals, card-quality judgments, UI, frontend dependencies, online dependencies, live APIs, telemetry, hosted services, or AI/LLM calls.

### Phase Relationship-1: Typed Relationship Primitives v0

Status: implemented and verified.

Load and validate the relationship vocabulary fixture as typed local objects. Definition of done: the loader validates schema version, unique vocabulary values, supported relationship types, evidence fields, confidence bands, deferred types, and explicit non-goals without deriving edges or making strategic judgments.

Typed Relationship Primitives v0 must not implement relationship derivation, package detection, synergy scoring, all-pairs comparison, deck-level role totals, recommendations, candidate search, add/cut scoring, UI, live APIs, telemetry, hosted services, or AI/LLM calls.

### Phase Relationship-1A: Factual Card Behavioral Profile v0

Status: implemented and verified.

Define a factual card behavioral profile shape for explicit outputs, costs, requirements, emitted events, observed events, permissions, modifiers, zone constraints, timing constraints, and source evidence. Definition of done: profiles preserve card and entry identity, reject malformed values, serialize deterministically, and avoid strategic role or quality claims.

Factual Card Behavioral Profile v0 must not extract behavior from Oracle text, derive relationships, classify deck roles, score synergy, recommend cards, or inspect live services.

### Phase Relationship-1B: Bounded Behavioral Atom Extraction v0

Status: implemented and verified.

Extract only a tiny, explicit, low-risk set of factual behavior atoms from local card records and Oracle text. Definition of done: supported phrase patterns produce traceable atoms, unsupported wording remains unextracted, source records are not mutated, and output remains deterministic.

Bounded Behavioral Atom Extraction v0 must not try to understand every Magic card, infer strategy, assign quality, select primary roles, derive deck-level counts, make recommendations, or broaden extraction beyond documented tested rules.

### Phase Tooling-1: Free Frontend Tooling Scaffold

Install or document free tooling required for later UI work, isolated under `apps/deckbuilder-ui/`. Definition of done: Node/npm are available, a Vite React TypeScript scaffold exists, dependencies are project-local, build verification passes, and no product features are implemented.

Do not add paid tools, account-based services, secrets, telemetry, Electron/Tauri packaging, or broad UI implementation in this phase.

### Phase 3: Deck Skeleton Report v0

Generate the first deck-understanding report from parsed deck data. Definition of done: a fixture deck produces stable counts for commander, mainboard, maybeboard, total cards, known/unknown cards, basic/non-basic grouping, broad card types, mana values, colors, and obvious missing-data warnings.

### Phase 4: Structural Warnings v0

Implement deterministic warnings for the first mechanical deck-shape issues. Definition of done: fixture decks produce stable warnings for card count issues, duplicate known non-basics, missing commander, unresolved unknown cards, basic color identity mismatches where local data exists, and early land/ramp/draw/interaction count placeholders.

### Phase 5: Commander Profile v0

Create a local commander profile contract and parser. Definition of done: a fixture profile can declare commander identity, intended bracket, deck thesis, primary plan, avoid patterns, required roles, budget posture, and human validation notes.

### Phase 6: Card Seat / Role Report v0

Generate a first role/seat report from local role definitions and optional overrides. Definition of done: a fixture deck can report which cards are counted as ramp, draw, interaction, protection, engine, payoff, win condition, glue, or unknown role without making card-cut decisions.

### Phase 7: Recommendation Explanation v0

Create explanation scaffolding for future recommendation drafts. Definition of done: output can explain why a candidate would be considered, which role it affects, what evidence supports it, what risks remain, and what human approval is required. It must not autonomously finalize cuts or additions.

### Later Phase: Structural Audit Engine

Implement `DeckAnalysis` and deterministic audit passes for curve, colors, card types, lands, ramp, draw, interaction, protection, engines, payoffs, and win conditions. Definition of done: known fixture decks produce expected stable counts.

### Later Phase: Final-Check Report

Generate a review packet with validation results, unresolved risks, and human approval flags. Definition of done: reports include mechanical checks and never claim final strategic approval automatically.

### Later Phase: Recommendation Draft Engine

Generate ranked draft recommendations from local logic only. Definition of done: every recommendation includes reason, role impact, package impact, budget/ownership impact where relevant, risks, confidence, and approval requirements.

### Later Phase: Optional UI Planning

Only after CLI behavior is stable, design the luxury workbench UI. Definition of done: UI plan preserves deterministic CLI behavior and prevents copy overflow.


### Phase Relationship-2: Deterministic Relationship Edge Derivation v0

Status: implemented and verified.

Goal:

Derive factual relationship edges between one explicitly supplied source deck
entry profile and one explicitly supplied target deck entry profile.

Initial supported derivation rules:

1. An exact source output-kind match against a target cost-kind produces a
   `supplies` relationship.
2. An exact source emitted-event match against a target observed-event produces
   a `triggers` relationship.

Required behavior:

- source and target deck-entry identifiers are supplied explicitly
- only compatible behavior dimensions are compared
- matched source and target behaviors are preserved
- Oracle-text evidence remains traceable
- conditions and zones are preserved deterministically
- derivation-rule identifiers are explicit
- exact v0 matches use confidence band 100
- duplicate edges are removed deterministically
- returned edges have stable ordering

This phase must not add:

- deck-wide scanning
- all-pairs comparison
- package detection
- combo solving
- synergy scoring
- recommendation logic
- candidate search
- card-quality judgments
- commander analysis
- user-interface behavior

Verification:

- focused unit tests for exact resource matches
- focused unit tests for exact event matches
- negative tests for mismatched behaviors
- deterministic ordering and deduplication tests
- entry-identity preservation tests
- full offline Python unit-test suite


### Phase Relationship-3: Card Relationship Report v0

Status: implemented and verified.

Goal:

Expose already-derived factual relationship edges through a stable,
deterministic report contract.

The report must separate:

- concise user summary
- machine-readable relationship evidence
- optional explanations
- optional debug details

Required behavior:

- accept an explicit iterable of RelationshipEdge values
- preserve source and target deck-entry identity
- preserve every edge's traceable evidence
- group or count relationships without assigning strategic value
- return deterministic ordering
- serialize to a stable versioned dictionary
- include debug details only when explicitly requested
- expose explicit report boundaries

This phase must not add:

- relationship derivation
- deck-wide scanning
- all-pairs comparison
- graph traversal
- package detection
- combo solving
- synergy scoring
- recommendation logic
- card-quality judgments
- commander analysis
- user-interface behavior

Verification:

- focused tests for empty reports
- focused tests for multiple relationship types
- deterministic ordering tests
- machine-evidence preservation tests
- debug inclusion and exclusion tests
- input validation tests
- full offline Python unit-test suite


### Phase Relationship-4: Relationship Pipeline Fixture Smoke v0

Status: implemented and verified.

Goal:

Prove one tiny deterministic end-to-end relationship pipeline using synthetic,
local fixture records.

Pipeline:

1. Load explicit local card records.
2. Extract bounded factual behavioral profiles.
3. Derive relationships only for explicitly declared source-target pairs.
4. Build a factual Card Relationship Report.
5. Compare the report against a stable expected-output fixture.

Required behavior:

- use synthetic fixture records rather than a real sample deck
- preserve source and target deck-entry identity
- exercise both `supplies` and `triggers`
- include an unsupported card record that produces no behavioral atoms
- perform no deck-wide scanning
- perform no all-pairs comparison
- require no network access
- produce stable deterministic JSON-compatible output

This phase must not add:

- general deck relationship orchestration
- candidate discovery
- graph traversal
- package detection
- combo solving
- synergy scoring
- recommendations
- strategic quality judgments
- commander analysis
- user-interface behavior

Verification:

- focused fixture smoke test
- exact expected-output comparison
- repeat-run determinism check
- source fixture immutability check
- full offline Python unit-test suite


### Phase Relationship-5: Relationship Input Contract Hardening v0

Status: implemented and verified.

Goal:

Harden the relationship primitive and behavioral-profile input contracts before
they are exposed through reusable production-facing orchestration.

Required behavior:

- required text fields accept strings only
- non-string values are rejected rather than coerced with `str`
- collection fields reject plain strings and bytes
- `None` collection values produce domain-specific validation errors
- valid collection values remain normalized, deduplicated, and sorted
- canonical RelationshipEdge identity and ordering use one shared helper
- derivation and report layers use the shared edge identity helper
- existing valid serialized output remains unchanged

Files likely involved:

- `src/mtg_workbench/deckbuilder/relationship_primitives.py`
- `src/mtg_workbench/deckbuilder/card_behavioral_profile.py`
- `src/mtg_workbench/deckbuilder/relationship_edge_derivation.py`
- `src/mtg_workbench/deckbuilder/card_relationship_report.py`
- focused relationship contract tests

Human validation zones:

None. This slice tightens deterministic validation and does not alter scoring,
strategy, recommendations, user-facing product behavior, or persisted workspace
schemas.

This phase must not add:

- new relationship derivation rules
- behavioral extraction coverage
- deck-wide scanning
- all-pairs comparison
- profile lookup or card lookup
- package detection
- combo solving
- synergy scoring
- recommendations
- strategic quality judgments
- commander analysis
- user-interface behavior

Verification:

- focused regression tests for non-string required fields
- focused regression tests for string-as-collection inputs
- focused regression tests for `None` collections
- shared edge identity and deterministic ordering tests
- existing relationship derivation and report tests
- full offline Python unit-test suite


### Phase Relationship-6: Explicit Relationship Pair Inspection v0

Status: implemented and verified.

Goal:

Create a small production-facing orchestration boundary for inspecting one
explicitly requested source-target relationship pair from an explicit mapping
of already-resolved CardBehavioralProfile values.

Required behavior:

- accept one explicit source deck-entry identifier
- accept one explicit target deck-entry identifier
- accept a mapping of deck-entry identifiers to CardBehavioralProfile values
- validate request identifiers as non-empty strings
- require source and target identifiers to be different
- resolve both profiles without guessing
- report missing source or target profiles clearly
- reject non-CardBehavioralProfile mapping values
- derive relationships only in the requested source-to-target direction
- return an empty CardRelationshipReport when no supported exact match exists
- return the existing deterministic CardRelationshipReport contract
- preserve all existing relationship evidence and entry identity

Files likely involved:

- `src/mtg_workbench/deckbuilder/relationship_pair_inspection.py`
- `tests/test_relationship_pair_inspection.py`
- `docs/codex/EXPLICIT_RELATIONSHIP_PAIR_INSPECTION_V0.md`

Human validation zones:

None. This slice adds deterministic factual orchestration only and does not
alter strategy, scoring, recommendations, or persisted workspace schemas.

This phase must not add:

- card-record lookup
- behavioral-profile extraction
- workspace scanning
- deck-wide relationship orchestration
- reverse-direction comparison unless explicitly requested separately
- all-pairs comparison
- graph traversal
- package detection
- combo solving
- synergy scoring
- recommendations
- strategic quality judgments
- commander analysis
- user-interface behavior
- live APIs or network access

Verification:

- focused tests for successful explicit pair inspection
- focused tests for no-match empty reports
- focused tests for missing source and target profiles
- focused tests for same-entry rejection
- focused tests for invalid profile-map values
- focused tests for directionality
- input mapping immutability test
- full offline Python unit-test suite


### Phase Relationship-7: Explicit Card Record Pair Inspection v0

Status: implemented and verified.

Goal:

Create a bounded production-facing bridge from two explicitly supplied local
or Scryfall-style card records to the existing directional factual
relationship report.

Pipeline:

1. Validate two explicit deck-entry identifiers.
2. Validate two explicit card-record mappings.
3. Extract one bounded CardBehavioralProfile from each record.
4. Inspect only the requested source-to-target direction.
5. Return the existing deterministic CardRelationshipReport.

Required behavior:

- accept one explicit source entry identifier and source card record
- accept one explicit target entry identifier and target card record
- require different source and target entry identifiers
- reject non-mapping card records with domain-specific errors
- normalize surrounding entry-identifier whitespace
- extract profiles without mutating either supplied record
- preserve source and target deck-entry identity
- preserve extracted Oracle-text evidence
- return an empty report when no supported exact relationship exists
- translate profile-extraction failures into clear source/target errors
- use no network access

Bounded extractor addition:

- exact wording containing `Sacrifice a Treasure:` produces a `treasure`
  cost atom
- the same wording emits `permanent_sacrificed`
- no other extraction vocabulary is added in this slice

This phase does not add:

- workspace scanning
- deck-wide relationship orchestration
- automatic reverse-direction inspection
- all-pairs comparison
- graph traversal
- broad Oracle-text extraction expansion
- package detection
- combo solving
- synergy scoring
- recommendations
- add/cut comparison
- strategic card-quality judgments
- commander analysis
- user-interface behavior
- live APIs or network access

Verification:

- focused Treasure-consumer extraction regression
- successful explicit card-record pair inspection
- strict directionality test
- unsupported/no-match empty report test
- source and target record validation tests
- same-entry rejection test
- identifier-normalization test
- source-record extraction-error test
- input-record immutability test
- full offline Python unit-test suite


### Phase Product-10: Visual Card Pair Compare v0 Planning

Status: implemented as a product interaction contract; no UI code added.

Goal:

Define the smallest useful baseline for placing two explicitly selected cards
together inside the primary deckbuilder workspace without introducing
analysis clutter.

Baseline interaction:

1. The user chooses `Compare card with...` from one card context action.
2. The deckbuilder enters a temporary `Choose one more card` state.
3. Selecting the second card opens a temporary modal or overlay.
4. The overlay displays exactly two selected card images together.
5. The user may replace either selected card.
6. Closing comparison returns to the unchanged deck workspace.

Required behavior:

- operate only from cards explicitly selected by the user
- compare exactly two cards
- prefer side-by-side presentation when screen width allows
- remain readable on narrow screens
- provide an obvious close action
- support Escape dismissal where keyboard input exists
- preserve the open deck, grouping, sorting, filters, and scroll context
- perform no deck mutation when comparison opens, changes, or closes
- keep comparison state transient and outside persisted deck state
- avoid permanent panels or dashboard widgets
- avoid automatic relationship analysis
- avoid automatic strategic card comparisons

Deferred progressive disclosure:

A later explicit `Inspect interaction` action may consume the factual
relationship-report pipeline. It must remain separate from baseline visual
comparison and must not appear automatically.

This planning phase must not add:

- React components
- modal implementation
- card-image loading behavior
- frontend state management
- automatic relationship reports
- synergy scores
- add/cut recommendations
- card winner labels
- purchase recommendations
- deck mutations
- persistent comparison state
- network dependencies

Verification:

- the deckbuilder roadmap explicitly contains the baseline comparison flow
- card-action requirements classify visual comparison as a core planned action
- deckbuilder interaction requirements define selection and dismissal behavior
- main-screen planning keeps comparison temporary
- a dedicated bounded interaction contract records its state and non-goals
- no application or frontend code is changed
- the full offline Python unit-test suite remains green

## Current Catchup Repair Queue

Before starting new feature work, continue repairing the audit findings captured after the July 12 implementation burst.

Completed:

- Step 1: Current docs/status/handoff repair.
- Step 2: Relationship Smoke Repair v0.
- Step 3: Relationship Contract Hardening Patch.
- Step 4: Workspace/Card Lookup Integrity Patch.
- Step 5: Scryfall Index Portability and Atomicity Patch.

Completed:

- Step 6: Visual Compare Direction Decision.

Remaining:

- No active numbered catchup repair remains. Readiness checkpoint passed and
  Deck Inspection CLI v0 is implemented.

## Verification Plan

Phase 2 verification:

```bash
$env:PYTHONPATH='src'
python -m unittest discover -s tests
python -m mtg_workbench.cli parse tests/fixtures/decklists/plain_commander.txt --cards tests/fixtures/cards/tiny_cards.json
python -m mtg_workbench.cli parse tests/fixtures/decklists/csv_commander.csv --cards tests/fixtures/cards/tiny_cards.json
```

Future verification should include:

- Unit tests.
- Fixture decklists.
- Known-good audit outputs.
- Regression tests for gotchas.
- Card normalization tests.
- Decklist parser tests.
- Role count tests.
- Package detection tests.
- Budget and ownership rule tests.
- Recommendation scoring tests.
- Final-check report tests.
- Manual human review checklist.

Verification must not require internet access.

## Human Validation Zones

Require explicit approval before implementing or changing:

- Stack/runtime selection if not using the proposed Python CLI.
- Scoring rubric or Commander bracket mapping.
- Recommendation weights or card evaluation rules.
- Commander identity, final cuts/additions, combo packages, archetype pivots, and power-level claims.
- Scryfall ingestion behavior.
- Source-of-truth data overwrites or local data deletion.
- Paid services, account login, secrets, or external integrations.
- UI tone, brand direction, or user-facing copy.

## Risks

- Only tiny local fixtures and local Scryfall snapshots exist; full curated project data is still pending.
- Scoring rubric and Commander bracket mapping are not defined yet.
- Role taxonomy and package definitions are still conceptual.
- Recommendations may feel weak until local rules, overrides, and examples mature.
- Local snapshots can become stale if update workflow is not designed carefully.
- A future UI could drift into generic text or overflow if not validated with real content.

## Definition Of Done For This Spec

- Goal is stated.
- Scope and non-goals are stated.
- Files likely affected are listed.
- MVP user loop is defined.
- Domain model is defined.
- Implementation phases are sequenced.
- Verification approach is stated.
- Human validation zones are stated.
- Risks and open questions are stated.
- Current feature/code status is accurate.

## Open Questions

### Blocking Before Feature Code

- None for Phase 2. Python CLI, tiny local fixtures, and local card snapshot usage are approved.

### Non-Blocking

- Exact scoring rubric and Commander bracket mapping.
- Initial role taxonomy.
- Initial package definition format.
- Budget threshold defaults.
- Owned/on-hand CSV format.

### Future Design

- Whether account login ever matters.
- Whether optional Scryfall bulk updates should be monthly, manually triggered, or both.
- Whether the eventual UI should be desktop, web, or another portable shell.

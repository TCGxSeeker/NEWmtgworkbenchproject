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

Current repository inspection found project operating files, source seed docs, tiny raw fixtures, Python parser/search source, tests, local Scryfall indexing support, and a free frontend tooling scaffold. The deterministic analyzer, recommender, finished UI, scoring rubric, and full curated project data are still future work. Missing facts should become TODOs or fixtures, not invented details.

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

### Phase Product-5: Deck Workspace Import/Export v0

Status: implemented for plain text import/export; no UI code, frontend dependencies, reports, recommendations, live APIs, telemetry, or full legality validation were added.

Implement local plain text conversion for native deck workspaces without UI code, frontend dependencies, reports, recommendations, online dependencies, live APIs, telemetry, or full legality validation. Definition of done: `src/mtg_workbench/deckbuilder/import_export.py` can import plain text decklists into `DeckWorkspace`, export `DeckWorkspace` objects to clean plain text, preserve quantities, zones, unresolved cards, conservative categories, and native save/load behavior, and tests prove import, export, save/load/export, unresolved fallback, and no-network behavior.

Plain text remains an import/export boundary format. `.mtgwdeck.json` remains the saved workspace source of truth.

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

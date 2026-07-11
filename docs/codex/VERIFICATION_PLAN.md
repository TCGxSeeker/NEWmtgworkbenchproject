# Verification Plan

## Baseline Documentation Checks

Run after planning or documentation changes:

```bash
git rev-parse --show-toplevel
rg --files --hidden -g '!.git/**'
git status --short
```

Expected root: `C:/Users/StDeL/Documents/New MTG project`.

## Verification Principles

- Verification must not require internet access.
- External data must be represented by local fixtures or local snapshots.
- Unknown cards, missing data, and invalid inputs must fail visibly instead of being guessed.
- Recommendation outputs must cite local rules, local data, or explicit user-approved exceptions.
- Human validation flags must be testable and visible in reports.

## Standard Test Command

Run Python tests from the repository root:

```powershell
python -m unittest discover -s tests
```

The repository-root `mtg_workbench` import shim points submodule imports at `src/mtg_workbench`.

## Future Test Categories

Add unit and fixture tests for:

- Decklist parser behavior.
- Card name normalization.
- Quantity preservation and deck count legality.
- Commander detection.
- Duplicate detection.
- Unknown or missing card reporting.
- Color identity validation.
- Local legality checks when local data exists.
- Mana curve and mana value distribution.
- Mana source and color pip analysis.
- Land, ramp, draw, interaction, protection, engine, payoff, and win-condition counts.
- Role count and context-specific tagging.
- Package detection.
- Budget threshold checks.
- Ownership/on-hand checks.
- Recommendation scoring and confidence.
- Final-check report generation.
- Gotcha regression tests.

## Fixture Requirements

Create local fixtures in Phase 1 before parser or recommendation work:

- Minimal local card snapshot.
- Valid Commander decklist.
- Invalid decklist with unknown cards.
- Decklist with commander and maybeboard markers.
- Owned-card CSV.
- Budget profile.
- Commander profile.
- Package definition.
- Known-good audit output.
- Role definition.
- Deckbuilding template.
- Human validation trigger file.
- Recommendation report output.
- Generic regression test categories.

## Phase 1 Contract Checks

Run these after changing source seeds, data contracts, or raw fixtures:

```bash
git rev-parse --show-toplevel
rg --files --hidden -g '!.git/**'
python -c "import json; json.load(open('data/raw/cards/sample_card_data_seed.json')); json.load(open('data/raw/reports/sample_audit_report.json')); json.load(open('data/raw/reports/sample_recommendation_report.json'))"
python -c "import csv; [list(csv.DictReader(open(p, newline=''))) for p in ['data/raw/decklists/sample_csv_decklist.csv','data/raw/owned/sample_owned_cards.csv']]"
git status --short
```

YAML fixtures are currently source templates. Until a runtime and YAML parser are approved, verify them by manual review and file presence rather than adding dependencies.

## Scryfall Bulk Snapshot Checks

After manually downloading Scryfall bulk data:

```powershell
Test-Path data/raw/scryfall/manifest.json
Get-ChildItem data/raw/scryfall -Recurse -File | Select-Object FullName,Length
Get-Content -Raw data/raw/scryfall/manifest.json | ConvertFrom-Json | Out-Null
```

Snapshot payloads under `data/raw/scryfall/**` should remain ignored by Git. Keep runtime tests local and deterministic; do not add live API calls to parser or normalizer tests.

## Scryfall Index Checks

After building the local Scryfall index:

```powershell
$env:PYTHONPATH='src'
python -m mtg_workbench.cli index-scryfall --raw-dir data/raw/scryfall --output data/processed/scryfall/cards.sqlite
python -m unittest discover -s tests
python -c "import sqlite3; db=sqlite3.connect('data/processed/scryfall/cards.sqlite'); print(db.execute('select count(*) from oracle_cards').fetchone()[0]); print(db.execute('select count(*) from oracle_taggings').fetchone()[0])"
```

Expected behavior: index generation uses local files only, creates `cards.sqlite`, writes `data/processed/scryfall/index_manifest.json`, and stores Oracle tag relationships by `oracle_id`. The index should stay compact enough to leave usable disk space; print rows are indexed by columns and names rather than full print-level FTS.

## Local Syntax Search Checks

Before implementing search, verify the spec exists:

```powershell
Test-Path docs/rules/SCRYFALL_SYNTAX_SEARCH.md
```

After implementation, run:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests
python -m mtg_workbench.cli search "otag:burn-creature ci:r mv<=2" --index data/processed/scryfall/cards.sqlite
python -m mtg_workbench.cli search "o:draw t:creature" --index data/processed/scryfall/cards.sqlite
```

Expected behavior: search uses SQLite only, returns stable JSON, matches Oracle tags by exact slug, label, or alias, expands Oracle tags through `oracle_taggings.oracle_id`, applies card filters after tag expansion, and reports unsupported syntax instead of guessing.

Search-2 filter tests are required passing tests. The suite should no longer report expected failures for `legal:commander`, `usd<=N`, `r:<rarity>`, `set:<code>`, or `is:commander`.

Search-2 verification:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests
python -m mtg_workbench.cli search "legal:commander r:common" --index data/processed/scryfall/cards.sqlite --limit 5
python -m mtg_workbench.cli search "usd<=1 set:m21" --index data/processed/scryfall/cards.sqlite --limit 5
python -m mtg_workbench.cli search "is:commander" --index data/processed/scryfall/cards.sqlite --limit 5
```

Expected behavior: Search-2 filters use local SQLite only, multiple clauses intersect, unsupported syntax remains explicit, and the full unit suite has no expected failures once decorators are removed.

Latest Search-2 run on 2026-07-10:

- `python -m unittest discover -s tests`: passed, 25 tests, 0 expected failures
- `python -m mtg_workbench.cli search "legal:commander r:common" --index data/processed/scryfall/cards.sqlite --limit 5`: passed
- `python -m mtg_workbench.cli search "usd<=1 set:m21" --index data/processed/scryfall/cards.sqlite --limit 5`: passed
- `python -m mtg_workbench.cli search "is:commander" --index data/processed/scryfall/cards.sqlite --limit 5`: passed
- `python -m mtg_workbench.cli search "pow>=3 legal:commander" --index data/processed/scryfall/cards.sqlite --limit 3`: passed, with `pow>=3` reported as unsupported syntax
- Rebuilt `data/processed/scryfall/cards.sqlite` from local raw snapshots only; `index_manifest.json` now reports schema version 2 and the rebuilt SQLite file contains indexes for rarity, set code, and commander-candidate filters

## Deckbuilder Product Planning Checks

After deckbuilder product docs change:

```powershell
Test-Path docs/product/deckbuilder/DECKBUILDER_ROADMAP.md
Test-Path docs/product/deckbuilder/MAIN_SCREEN_REQUIREMENTS.md
Test-Path docs/product/deckbuilder/DECK_MODEL_REQUIREMENTS.md
Test-Path docs/product/deckbuilder/VIEW_MODES_REQUIREMENTS.md
Test-Path docs/product/deckbuilder/GROUP_SORT_FILTER_REQUIREMENTS.md
Test-Path docs/product/deckbuilder/SEARCH_WORKSPACE_REQUIREMENTS.md
Test-Path docs/product/deckbuilder/CARD_ACTIONS_REQUIREMENTS.md
Test-Path docs/product/deckbuilder/STATS_AND_PROBABILITY_REQUIREMENTS.md
Test-Path docs/product/deckbuilder/IMPORT_EXPORT_REQUIREMENTS.md
Test-Path docs/product/deckbuilder/UI_NON_GOALS.md
Test-Path docs/product/deckbuilder/OPEN_QUESTIONS.md
Test-Path docs/product/deckbuilder/reference/README.md
Test-Path data/ui_reference/deckbuilder/README.md
```

Expected behavior: docs exist, reference screenshots are treated as inspiration rather than clone requirements, and the roadmap keeps the deckbuilder workspace as the primary user screen.

## Tooling Scaffold Checks

After free frontend tooling setup:

```powershell
& 'C:\Program Files\nodejs\node.exe' --version
& 'C:\Program Files\nodejs\npm.cmd' --version
Test-Path docs/codex/TOOLING_PLAN.md
Test-Path apps/deckbuilder-ui/package.json
$env:Path = 'C:\Program Files\nodejs;' + $env:Path
Push-Location apps/deckbuilder-ui
& 'C:\Program Files\nodejs\npm.cmd' ci
& 'C:\Program Files\nodejs\npm.cmd' run build
& 'C:\Program Files\nodejs\npm.cmd' run lint
Pop-Location
```

Expected behavior: the frontend scaffold restores from the lockfile, builds, dependencies are project-local, generated `node_modules` is ignored, and no product features are implemented. Dependency restoration may require network access unless the npm cache is warm.

Latest run on 2026-07-10:

- `node --version`: `v24.18.0`
- `npm --version`: `11.16.0`
- `npm run build`: passed in `apps/deckbuilder-ui`
- `npm run lint`: passed in `apps/deckbuilder-ui`
- `python -m unittest discover -s tests`: current baseline is 25 passing tests and 0 expected failures
- `git check-ignore -v apps/deckbuilder-ui/node_modules apps/deckbuilder-ui/dist`: confirmed ignored by scaffold `.gitignore`

## Deckbuilder Foundation V0 Planning Checks

After Deckbuilder Foundation v0 docs change:

```powershell
Test-Path README.md
Test-Path .gitattributes
Test-Path docs/product/deckbuilder/DECKBUILDER_FOUNDATION_V0.md
Test-Path docs/product/deckbuilder/MAIN_SCREEN_V0.md
Test-Path docs/product/deckbuilder/DECK_WORKSPACE_MODEL_V0.md
Test-Path docs/product/deckbuilder/DECKBUILDER_INTERACTIONS_V0.md
Test-Path docs/product/deckbuilder/DECKBUILDER_ACCEPTANCE_CHECKLIST.md
Test-Path docs/product/deckbuilder/OPEN_QUESTIONS.md
git diff --check
```

Expected behavior: stale phase language is removed, the main deckbuilder workspace remains centered, implementation boundaries are explicit, and open questions are listed before implementation starts.

Latest Deckbuilder Foundation v0 planning run on 2026-07-10:

- Required file presence checks: passed
- Stale-language search for old feature-code, commit-history, and Search-2 test-count wording: no matches
- `git diff --check`: passed; Git reported expected line-ending normalization warnings after adding `.gitattributes`
- `python -m unittest discover -s tests`: passed, 25 tests, 0 failures
- Frontend build/lint checks: not run because this pass did not change frontend code or dependencies

## Deck Workspace Model V0 Checks

After changing native workspace model code or format docs:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests
Test-Path docs/rules/DECK_WORKSPACE_FORMAT.md
Test-Path tests/fixtures/deckbuilder/sample_workspace.mtgwdeck.json
```

Expected behavior: native `.mtgwdeck.json` workspaces can be created, saved, loaded, and round-tripped without losing commander/mainboard/maybeboard entries, quantities, unknown-card state, categories, tags, notes, or optional metadata. Malformed workspace files should fail with clear validation errors. No network access or frontend dependency installation is required.

Latest Deck Workspace Model v0 run on 2026-07-10:

- `python -m unittest discover -s tests`: passed, 35 tests, 0 failures
- Deck workspace file presence checks: passed
- `python -m json.tool` on tiny deckbuilder fixtures: passed
- Stale-boundary search for old implementation/save-format wording: no matches
- `git diff --check`: passed; Git reported expected line-ending normalization warnings from `.gitattributes`
- Frontend build/lint checks: not run because this pass did not change frontend code or dependencies

## Deck Workspace Mutations V0 Checks

After changing workspace mutation helpers:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests
python -m unittest tests.test_deckbuilder_mutations
```

Expected behavior: mutation helpers edit `DeckWorkspace` in memory, return the updated workspace, preserve native `.mtgwdeck.json` round trips, mark `saved_state.is_dirty` true, update `updated_at`, preserve unresolved entries, merge only clearly identical duplicate adds, create separate entries for ambiguous or materially different adds, set commander moves to quantity `1`, and avoid UI code, frontend dependencies, network access, reports, recommendations, or full legality validation.

Latest Deck Workspace Mutations v0 run on 2026-07-10:

- `python -m unittest discover -s tests`: passed, 60 tests, 0 failures
- `python -m py_compile src/mtg_workbench/deckbuilder/mutations.py tests/test_deckbuilder_mutations.py`: passed
- Mutation file presence checks: passed
- `python -m json.tool` on tiny deckbuilder fixtures: passed
- Stale-boundary search for old mutation/save-format wording: no matches
- `git diff --check`: passed; Git reported expected line-ending normalization warnings from `.gitattributes`
- Frontend build/lint checks: not run because this pass did not change frontend code or dependencies

## Deck Workspace Import/Export V0 Checks

After changing workspace import/export helpers:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests
python -m unittest tests.test_deckbuilder_import_export
```

Expected behavior: plain text decklists import into native `DeckWorkspace` objects, `1x Card Name`, `1 Card Name`, and bare card-name lines are supported, commander/mainboard/maybeboard sections are preserved, conservative category headers are applied, unresolved cards are preserved, workspace export uses `1x Card Name` lines with display-name fallback to input name, successful saves mark workspaces clean, and no network access, UI code, frontend dependencies, reports, recommendations, live APIs, telemetry, or full legality validation are involved.

Latest Deck Workspace Import/Export v0 run on 2026-07-10:

- `python -m unittest discover -s tests`: passed, 71 tests, 0 failures
- `python -m py_compile src/mtg_workbench/deckbuilder/import_export.py tests/test_deckbuilder_import_export.py src/mtg_workbench/deckbuilder/serialization.py`: passed
- Import/export file presence checks: passed
- `python -m json.tool` on tiny deckbuilder JSON fixtures: passed
- Stale-boundary search for old import/save-format wording: no matches
- `git diff --check`: passed; Git reported expected line-ending normalization warnings from `.gitattributes`
- Frontend build/lint checks: not run because this pass did not change frontend code or dependencies

## Category Taxonomy V0 Checks

After changing category taxonomy docs or fixtures:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests
Test-Path docs/rules/CATEGORY_TAXONOMY.md
Test-Path data/fixtures/categories/category_taxonomy.example.yaml
```

Expected behavior: taxonomy docs define canonical categories, aliases, normalization approach, imported/user category preservation, future field distinctions, and deferred auto-categorization behavior. The fixture remains tiny and local. No network access, UI code, frontend dependencies, recommendations, full deck analysis, telemetry, live APIs, or large card-to-category datasets are involved.

Latest Category Taxonomy v0 run on 2026-07-11:

- `python -m unittest discover -s tests`: failed because `src` was not on `PYTHONPATH`; tests could not import `mtg_workbench`
- `$env:PYTHONPATH='src'; python -m unittest discover -s tests`: passed, 71 tests, 0 failures
- Category taxonomy file presence checks: passed
- `git diff --check`: passed

## Test Command Hygiene V0 Checks

After changing repository Python import/test setup:

```powershell
python -m unittest discover -s tests
```

Expected behavior: tests run from the repository root without manual `PYTHONPATH` setup, no external dependencies are added, and existing test behavior is unchanged.

Latest Test Command Hygiene v0 run on 2026-07-11:

- `python -m unittest discover -s tests`: passed, 71 tests, 0 failures
- `python -c "import mtg_workbench, mtg_workbench.cards.catalog as c"`: passed
- `git diff --check`: passed

## Category Taxonomy Loader/Normalizer V0 Checks

After changing category taxonomy loader or normalization behavior:

```powershell
python -m unittest discover -s tests
python -m unittest tests.test_deckbuilder_categories
```

Expected behavior: the loader reads the tiny local taxonomy fixture, validates canonical categories and alias targets, normalizes labels case-insensitively after whitespace cleanup, preserves the original label in normalization results, reports unknown labels without guessing, and does not mutate deck workspaces or auto-categorize cards.

Latest Category Taxonomy Loader/Normalizer v0 run on 2026-07-11:

- `python -m unittest discover -s tests`: passed, 80 tests, 0 failures
- `python -m unittest tests.test_deckbuilder_categories`: passed, 9 tests, 0 failures
- `python -m py_compile src/mtg_workbench/deckbuilder/categories.py tests/test_deckbuilder_categories.py`: passed
- `git diff --check`: passed

## Deck Entry Category Metadata V0 Checks

After changing deck entry category metadata fields or taxonomy-backed import behavior:

```powershell
python -m unittest discover -s tests
python -m unittest tests.test_deckbuilder_workspace tests.test_deckbuilder_mutations tests.test_deckbuilder_import_export
git diff --check
```

Expected behavior: native `.mtgwdeck.json` entries preserve imported category labels, normalized category labels, generic category hints, future deck-specific primary role placeholders, secondary tags, and category origin values. Plain text import may use the local taxonomy fixture when supplied, while unknown category labels remain preserved instead of guessed. This slice must not add auto-categorization, role counting, recommendations, UI code, frontend dependencies, network calls, live APIs, or large datasets.

Latest Deck Entry Category Metadata v0 run on 2026-07-11:

- `python -m unittest tests.test_deckbuilder_workspace tests.test_deckbuilder_mutations tests.test_deckbuilder_import_export`: passed, 52 tests, 0 failures
- `python -m py_compile src/mtg_workbench/deckbuilder/models.py src/mtg_workbench/deckbuilder/validation.py src/mtg_workbench/deckbuilder/mutations.py src/mtg_workbench/deckbuilder/import_export.py`: passed
- `python -m unittest discover -s tests`: passed, 86 tests, 0 failures
- `git diff --check`: passed

## Manual Human Review Checklist

Use manual review for:

- Scoring rubric interpretation.
- Commander bracket estimates.
- Recommendation logic and tradeoffs.
- Package warning quality.
- Card role meaning in this exact deck.
- Expensive card exceptions.
- Meta-specific claims.
- UI copy, layout, and text overflow when UI work begins.
- Fresh pricing, legality, and newly released card assumptions.

## CLI Verification Targets

Phase 2 parser and normalizer checks:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests
python -m mtg_workbench.cli parse tests/fixtures/decklists/plain_commander.txt --cards tests/fixtures/cards/tiny_cards.json
python -m mtg_workbench.cli parse tests/fixtures/decklists/csv_commander.csv --cards tests/fixtures/cards/tiny_cards.json
```

Expected Phase 2 behavior:

- Plain text and CSV decklists parse.
- Quantities are preserved.
- Commander entries are separated from main deck entries.
- Names normalize against local card snapshot names and aliases only.
- Unknown cards are reported.
- Duplicate known non-basic cards produce warnings.
- Output is stable JSON.
- No internet access, API call, recommendation logic, structural audit engine, or UI is involved.

## Skill Checks

Validate local skill files when they change:

```bash
python C:/Users/StDeL/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/project-launch-spec
python C:/Users/StDeL/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/verification-gate
python C:/Users/StDeL/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/gotcha-capture
```

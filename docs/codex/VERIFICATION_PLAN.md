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

Pending Search-2 filter tests are marked with `@unittest.expectedFailure` until the filters are implemented. When implementing those filters, remove the decorators and require the same full suite to pass normally.

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
Push-Location apps/deckbuilder-ui
& 'C:\Program Files\nodejs\npm.cmd' run build
& 'C:\Program Files\nodejs\npm.cmd' run lint
Pop-Location
```

Expected behavior: the frontend scaffold builds, dependencies are project-local, generated `node_modules` is ignored, and no product features are implemented.

Latest run on 2026-07-10:

- `node --version`: `v24.18.0`
- `npm --version`: `11.16.0`
- `npm run build`: passed in `apps/deckbuilder-ui`
- `npm run lint`: passed in `apps/deckbuilder-ui`
- `python -m unittest discover -s tests`: passed with 24 tests and 5 expected Search-2 failures
- `git check-ignore -v apps/deckbuilder-ui/node_modules apps/deckbuilder-ui/dist`: confirmed ignored by scaffold `.gitignore`

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

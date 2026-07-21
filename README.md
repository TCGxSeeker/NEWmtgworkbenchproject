# MTG Workbench

Offline-first Commander deckbuilding workbench for importing decklists, normalizing cards against local data, searching local Scryfall snapshots, and preparing deterministic deck reports.

## Current Status

The project has operating docs, source fixtures, parser/normalizer code, local Scryfall snapshot/index/search infrastructure, Search-2 filters, free frontend tooling, native `.mtgwdeck.json` workspace support, plain text import/export with CLI access, workspace mutation CLI access, deterministic role evidence, local card fact lookup, deck skeleton and structural warning reports, a bounded deck inspection envelope with CLI access, typed card relationship primitives, factual behavioral profiles, bounded behavioral atom extraction, deterministic relationship edge derivation, factual relationship reports, and stable end-to-end inspection and relationship smoke fixtures.

No finished deckbuilder UI, recommendation engine, scoring rubric, structural audit engine, or full deck report exists yet.

Current verified baseline: from `G:\Documents\New MTG project`, `python -m unittest discover -s tests` passes with 317 tests after Deck Workspace Mutation CLI v0, deckbuilder checklist cleanup, and Deck Inspection CLI polish.

## Basic Commands

Run Python tests from the repo root:

```powershell
python -m unittest discover -s tests
```

The repository-root `mtg_workbench` import shim points submodule imports at `src/mtg_workbench`, so manual `PYTHONPATH` setup is not required for the standard test command.

Run a factual deck inspection report from a native workspace:

```powershell
python -m mtg_workbench.cli inspect-deck tests/fixtures/deckbuilder/inspection_smoke_workspace.mtgwdeck.json --card-records tests/fixtures/deckbuilder/inspection_smoke_card_records.json
python -m mtg_workbench.cli inspect-deck tests/fixtures/deckbuilder/inspection_smoke_workspace.mtgwdeck.json --card-records tests/fixtures/deckbuilder/inspection_smoke_card_records.json --summary-only
```

Import and export native workspaces:

```powershell
python -m mtg_workbench.cli workspace-import tests/fixtures/deckbuilder/commander_import.txt --cards tests/fixtures/cards/tiny_cards.json --output deck.mtgwdeck.json
python -m mtg_workbench.cli workspace-export deck.mtgwdeck.json --output decklist.txt
python -m mtg_workbench.cli workspace-add-card deck.mtgwdeck.json "Arcane Helper" --cards tests/fixtures/cards/tiny_cards.json --output deck-edited.mtgwdeck.json
```

Run the frontend scaffold checks:

```powershell
$env:Path = 'C:\Program Files\nodejs;' + $env:Path
Push-Location apps/deckbuilder-ui
& 'C:\Program Files\nodejs\npm.cmd' ci
& 'C:\Program Files\nodejs\npm.cmd' run build
& 'C:\Program Files\nodejs\npm.cmd' run lint
Pop-Location
```

## Data Rules

- Core behavior should work from local files.
- Do not add live API calls to parser, normalizer, report, or search behavior without an approved ingestion/update design.
- Raw Scryfall bulk snapshots live under `data/raw/scryfall/` and are ignored by Git.
- Generated SQLite indexes live under `data/processed/scryfall/` and are ignored by Git, except small manifests.
- Large payloads, dependency folders, build outputs, caches, and secrets should not be committed.

## Planning Docs

- Project operating docs: `docs/codex/`
- Rules and data contracts: `docs/rules/`
- Deterministic algorithm planning: `docs/product/algorithm/`
- Next-session handoff: `docs/codex/NEXT_SESSION_HANDOFF.md`
- Deckbuilder product planning: `docs/product/deckbuilder/`
- Deckbuilder Foundation v0 planning: `docs/product/deckbuilder/DECKBUILDER_FOUNDATION_V0.md`
- Native workspace format: `docs/rules/DECK_WORKSPACE_FORMAT.md`
- Local Codex skills: `.agents/skills/`

## Implementation Boundary

Deckbuilder Foundation implementation includes the native workspace model, in-memory mutation helpers and CLI commands, plain text import/export and CLI commands, role-rule loading, local card fact lookup, card facts adaptation, card-level role evidence pipelines, structural deck reports, mechanical warnings, a factual deck inspection envelope and CLI command, typed relationship primitives, bounded behavior extraction, deterministic pairwise edge derivation, factual relationship reporting, and stable smoke fixtures. Do not add app UI, new frontend dependencies, full deck analysis, recommendations, scoring logic, strategic quality judgments, live APIs, or visual components until their own implementation slice is approved.

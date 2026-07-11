# MTG Workbench

Offline-first Commander deckbuilding workbench for importing decklists, normalizing cards against local data, searching local Scryfall snapshots, and preparing deterministic deck reports.

## Current Status

The project has operating docs, source fixtures, parser/normalizer code, local Scryfall snapshot/index/search infrastructure, Search-2 filters, free frontend tooling, Deckbuilder Foundation helpers for native `.mtgwdeck.json` files plus plain text import/export, deterministic algorithm planning, and Role Rules v0 docs/fixtures.

No finished deckbuilder UI, recommendation engine, scoring rubric, or structural audit engine exists yet.

## Basic Commands

Run Python tests from the repo root:

```powershell
python -m unittest discover -s tests
```

The repository-root `mtg_workbench` import shim points submodule imports at `src/mtg_workbench`, so manual `PYTHONPATH` setup is not required for the standard test command.

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

Deckbuilder Foundation implementation has begun with the native workspace model, in-memory mutation helpers, and plain text import/export only. Do not add app UI, new frontend dependencies, reports, recommendations, scoring logic, live APIs, or visual components until their own implementation slice is approved.

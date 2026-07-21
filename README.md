# MTG Workbench

Offline-first Commander deckbuilding workbench for importing decklists, normalizing cards against local data, searching local Scryfall snapshots, and preparing deterministic deck reports.

## Current Status

The project has operating docs, source fixtures, parser/normalizer code, local Scryfall snapshot/index/search infrastructure, Search-2 filters, free frontend tooling, native `.mtgwdeck.json` workspace support, plain text import/export, deterministic role evidence, local card fact lookup, deck skeleton and structural warning reports, a bounded deck inspection envelope, typed card relationship primitives, factual behavioral profiles, bounded behavioral atom extraction, deterministic relationship edge derivation, factual relationship reports, and stable end-to-end inspection and relationship smoke fixtures.

No finished deckbuilder UI, recommendation engine, scoring rubric, structural audit engine, or full deck report exists yet.

Current verified baseline: from `G:\Documents\New MTG project`, `python -m unittest discover -s tests` passes with 298 tests after the Step 6 visual compare direction documentation update. The last committed repair checkpoint before Step 6 was `7f67e40 Harden Scryfall index persistence`; see `docs/codex/NEXT_SESSION_HANDOFF.md` for the active handoff.

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

Deckbuilder Foundation implementation includes the native workspace model, in-memory mutation helpers, plain text import/export, role-rule loading, local card fact lookup, card facts adaptation, card-level role evidence pipelines, structural deck reports, mechanical warnings, a factual deck inspection envelope, typed relationship primitives, bounded behavior extraction, deterministic pairwise edge derivation, factual relationship reporting, and stable smoke fixtures. Do not add app UI, new frontend dependencies, full deck analysis, recommendations, scoring logic, strategic quality judgments, live APIs, or visual components until their own implementation slice is approved.

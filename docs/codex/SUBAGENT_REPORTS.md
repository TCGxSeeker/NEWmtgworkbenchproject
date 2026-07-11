# Subagent Reports

## 2026-07-10 Planning Scaffold Readiness Rerun

### Task Delegated

Four read-only subagents reviewed whether the repository is organized well enough to continue planning after Search-2:

- Planning scaffold and product docs.
- Implementation readiness for Deck Skeleton Report v0.
- Verification and reproducibility.
- Repository hygiene and isolation.

### Files And Areas Reviewed

- `AGENTS.md`
- `.tasks/`
- `.agents/skills/`
- `docs/codex/`
- `docs/product/deckbuilder/`
- `docs/rules/`
- `src/`
- `tests/`
- `data/raw/scryfall/`
- `data/processed/scryfall/`
- `apps/deckbuilder-ui/`
- `.gitignore`

### Key Strengths

- The project is well separated from sibling workspaces and the repo root is clearly defined.
- Planning docs are modular and cover project brief, implementation spec, verification, decisions, gotchas, automation, tooling, and human validation zones.
- Product planning docs are split into useful deckbuilder surfaces: model, main screen, views, grouping/filtering, search, actions, stats, import/export, non-goals, and open questions.
- Parser, normalizer, catalog, CLI, Scryfall indexing/search, and tests are cleanly separated.
- Search is properly scoped as infrastructure, with Deckbuilder Foundation v0 queued as the next product-centered planning milestone.
- Ignored artifact hygiene is strong for `node_modules`, `dist`, large Scryfall payloads, generated SQLite, and Python caches.
- Python tests are offline and deterministic; current suite is 25 passing tests with no expected failures.

### Issues And Risks

- Resolved during follow-up cleanup: stale Search-2 test-count notes were removed from `docs/codex/VERIFICATION_PLAN.md`.
- Resolved during follow-up cleanup: pre-feature-code wording was revised in `docs/codex/IMPLEMENTATION_SPEC.md`.
- Resolved during follow-up cleanup: `AGENTS.md` commit guidance now reflects the established checkpoint-commit workflow.
- Resolved during this report update: `docs/codex/SUBAGENT_REPORTS.md` is no longer a placeholder.
- Deck Skeleton Report v0 lacks a concrete JSON output contract, golden fixture, and missing-data test case.
- No first-class `analysis` or `reports` package exists yet, so future report logic needs a clear module boundary.
- Frontend verification now prefers `npm ci`; expected Node/npm versions still need to remain visible when tooling changes.
- Full Scryfall verification depends on ignored local payloads; clean checkout checks should be separated from local-snapshot checks.
- Scryfall snapshot integrity checks should compare manifest hashes, byte counts, SQLite `quick_check`, and table counts.
- Resolved during follow-up cleanup: `.gitattributes` exists at the repository root.
- Resolved during follow-up cleanup: `README.md` exists at the repository root.

### Recommended Actions

1. Commit the completed Search-2 work before starting Deck Skeleton Report v0.
2. Keep stale-note cleanup current in `docs/codex/VERIFICATION_PLAN.md`, `docs/codex/IMPLEMENTATION_SPEC.md`, and `AGENTS.md`.
3. Define a Deck Skeleton Report v0 mini-spec before coding: JSON shape, CLI command, fixtures, warnings, and acceptance checks.
4. Add `src/mtg_workbench/reports/` or `src/mtg_workbench/analysis/` for report logic rather than expanding parser or normalizer code.
5. Add a golden skeleton-report fixture and at least one missing-data fixture case.
6. Split verification docs into clean-checkout checks and local-full-snapshot checks.
7. Keep frontend verification docs using `npm ci` and document Node/npm expectations when tooling changes.
8. Add Scryfall integrity verification commands.
9. Maintain `.gitattributes` and the root `README.md` as the repository grows.

### Actions Taken

- Recorded this rerun summary in `docs/codex/SUBAGENT_REPORTS.md`.
- No implementation or planning fixes were applied during the subagent review itself.

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
- Search is properly scoped as infrastructure, with Deck Skeleton Report v0 queued as the next product-centered phase.
- Ignored artifact hygiene is strong for `node_modules`, `dist`, large Scryfall payloads, generated SQLite, and Python caches.
- Python tests are offline and deterministic; current suite is 25 passing tests with no expected failures.

### Issues And Risks

- `docs/codex/VERIFICATION_PLAN.md` has conflicting historical notes: Search-2 is now 25 passing tests, but an older tooling entry still mentions 24 tests and 5 expected failures.
- `docs/codex/IMPLEMENTATION_SPEC.md` still contains pre-feature-code wording even though parser, search, indexing, and frontend tooling now exist.
- `AGENTS.md` commit guidance says there is no commit history yet, which is no longer true.
- `docs/codex/SUBAGENT_REPORTS.md` was still a placeholder before this update.
- Deck Skeleton Report v0 lacks a concrete JSON output contract, golden fixture, and missing-data test case.
- No first-class `analysis` or `reports` package exists yet, so future report logic needs a clear module boundary.
- Frontend verification should prefer `npm ci` and should pin or document the expected Node/npm version.
- Full Scryfall verification depends on ignored local payloads; clean checkout checks should be separated from local-snapshot checks.
- Scryfall snapshot integrity checks should compare manifest hashes, byte counts, SQLite `quick_check`, and table counts.
- No `.gitattributes` exists, so Windows line-ending warnings may create noisy future diffs.
- No root `README.md` exists yet for non-Codex onboarding.

### Recommended Actions

1. Commit the completed Search-2 work before starting Deck Skeleton Report v0.
2. Clean stale notes in `docs/codex/VERIFICATION_PLAN.md`, `docs/codex/IMPLEMENTATION_SPEC.md`, and `AGENTS.md`.
3. Define a Deck Skeleton Report v0 mini-spec before coding: JSON shape, CLI command, fixtures, warnings, and acceptance checks.
4. Add `src/mtg_workbench/reports/` or `src/mtg_workbench/analysis/` for report logic rather than expanding parser or normalizer code.
5. Add a golden skeleton-report fixture and at least one missing-data fixture case.
6. Split verification docs into clean-checkout checks and local-full-snapshot checks.
7. Update frontend verification docs to prefer `npm ci` and document Node/npm expectations.
8. Add Scryfall integrity verification commands.
9. Consider adding `.gitattributes` and a minimal root `README.md` as follow-up scaffolding cleanup.

### Actions Taken

- Recorded this rerun summary in `docs/codex/SUBAGENT_REPORTS.md`.
- No implementation or planning fixes were applied during the subagent review itself.

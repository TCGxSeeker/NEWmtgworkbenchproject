# Decision Log

## 2026-07-08

- Decision: Create a project-local operating structure under `docs/codex/`, `.tasks/`, and `.agents/skills/`.
  - Reason: Keep this project separated from sibling workspaces.
  - Alternatives considered: ad hoc notes or shared project conventions.
  - Risk: Hidden directories can be missed by simple file listing.
  - Status: Accepted.

## 2026-07-09

- Decision: Treat the interview answers and supplemental hand-off as the source of truth.
  - Reason: They define the project philosophy, MVP, constraints, and validation gates.
  - Alternatives considered: continue from generic starter templates.
  - Risk: Future details such as scoring rubric and data formats are still unresolved.
  - Status: Accepted.

- Decision: Build an offline-first local CLI MVP before any web UI.
  - Reason: The MVP must prove parsing, normalization, analysis, and reporting with local data only.
  - Alternatives considered: production web app first, chatbot wrapper, API-backed recommendation tool.
  - Risk: CLI may not capture the eventual luxury UI experience.
  - Status: Accepted for MVP.

- Decision: Reject popularity-driven recommendation logic.
  - Reason: The system must preserve deck identity and evaluate actual card function in context.
  - Alternatives considered: EDHREC-style staple ranking, live popularity metrics, repeat-user behavior.
  - Risk: Requires richer local rules and fixtures before recommendations feel strong.
  - Status: Accepted.

- Decision: Use deterministic local rules and rules-as-data where reasonable.
  - Reason: Rules must be inspectable, editable, diffable, testable, and offline.
  - Alternatives considered: hardcoded magic numbers, AI-dependent reasoning, external services.
  - Risk: More upfront schema and fixture work.
  - Status: Accepted.

- Decision: Keep strategic deck choices under human approval.
  - Reason: Commander identity, archetype, power level, final cuts, and fun factor are subjective and high-impact.
  - Alternatives considered: autonomous final deckbuilding.
  - Risk: More approval checkpoints.
  - Status: Accepted.

- Decision: Treat Scryfall as optional future local-data ingestion, not an MVP runtime dependency.
  - Reason: The base system must function without internet access.
  - Alternatives considered: live Scryfall calls in analysis.
  - Risk: Local snapshots can become stale.
  - Status: Accepted.

- Decision: No blocking conflicts were found in the current repo.
  - Reason: Existing docs were lightweight templates and did not contradict the hand-off.
  - Alternatives considered: preserve earlier generic wording.
  - Risk: Some previous text is superseded.
  - Status: Recorded.

- Decision: Save the MTG project master seed in `docs/sources/MTG_PROJECT_MASTER_SEED.md`.
  - Reason: The seed file explicitly requests this location and defines doctrine for Phase 1 data contracts.
  - Alternatives considered: keep the file only outside the repository or split it into companion files immediately.
  - Risk: The file is doctrine, not card data, and must not be parsed as a decklist or card database.
  - Status: Accepted.

- Decision: Create Phase 1 data contracts before feature code.
  - Reason: The project needs offline local formats for cards, decklists, ownership, commander profiles, roles, packages, templates, budget profiles, validation triggers, reports, and generic regression tests.
  - Alternatives considered: implement parser/analyzer first.
  - Risk: Contracts may evolve after real curated data is provided.
  - Status: Accepted.

- Decision: Use YAML for editable rules/profiles, CSV for table inputs, JSON for local card snapshots and machine report outputs, and Markdown for doctrine/source notes.
  - Reason: These formats are local, diffable, human-editable, and testable without internet.
  - Alternatives considered: database-first storage or hardcoded Python constants.
  - Risk: YAML validation will need an approved parser once implementation begins.
  - Status: Proposed for Phase 1.

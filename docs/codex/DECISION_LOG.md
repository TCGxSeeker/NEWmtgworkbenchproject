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

- Decision: Proceed to Phase 2 with a Python CLI parser and normalizer.
  - Reason: The user approved Python CLI as the MVP runtime and requested a small parser/normalizer layer against tiny local fixtures.
  - Alternatives considered: waiting for full card database, adding API-backed normalization, starting with UI.
  - Risk: Tiny fixtures prove behavior but not full MTG coverage.
  - Status: Accepted for Phase 2.

- Decision: Keep Phase 2 output to stable JSON parse results and basic validation warnings.
  - Reason: Structural audit and recommendations are future phases.
  - Alternatives considered: adding audit/recommendation behavior now.
  - Risk: Output will be intentionally limited.
  - Status: Accepted.

- Decision: Allow a manually triggered Scryfall bulk-data snapshot under `data/raw/scryfall/`.
  - Reason: The user explicitly approved grabbing the full Scryfall bulk data and wants local locations for each relevant piece.
  - Alternatives considered: waiting for a future ingestion command, using live API calls at runtime, or committing full payloads.
  - Risk: Bulk files are large and can become stale; they must not become runtime API dependencies.
  - Status: Accepted for local snapshot storage.

- Decision: Model Oracle tag search as tag-first query planning.
  - Reason: Oracle tags are associated to cards through `taggings[]` with `oracle_id`, so `otag:` should resolve tag matches before card filters.
  - Alternatives considered: attaching tags to card records first and searching only card-side flattened fields.
  - Risk: The indexer must maintain a reliable `oracle_id` join and preserve tag weights.
  - Status: Accepted for future Scryfall indexing.

- Decision: Build a local SQLite Scryfall index from all stored bulk types.
  - Reason: The deckbuilder needs efficient local search calls and should function without API calls after snapshots are stored.
  - Alternatives considered: searching compressed JSONL directly, using an external search service, or calling Scryfall search live.
  - Risk: Generated indexes can be large and must be regenerated after snapshot updates.
  - Status: Accepted for local indexing.

- Decision: Keep print indexing compact instead of adding print-level FTS in Phase Index-1.
  - Reason: The first full index attempt exhausted available disk space; oracle-level FTS plus indexed print columns supports the planned syntax-search core without duplicating every print's text.
  - Alternatives considered: full print FTS, external search service, skipping all_cards rows.
  - Risk: Future print-specific text search may need an opt-in expanded index.
  - Status: Accepted for Phase Index-1.

- Decision: Start local syntax search with a narrow supported subset.
  - Reason: The workbench needs useful offline search soon, but a full Scryfall syntax clone would be too broad for the first pass.
  - Alternatives considered: implement the entire syntax at once, use live Scryfall search, or delay search until audit features.
  - Risk: Users may try unsupported syntax early; unsupported clauses must be explicit and test-covered.
  - Status: Accepted for Phase Search-1.

- Decision: Return unsupported syntax alongside valid search results instead of failing the whole query.
  - Reason: Users can still get useful local search output while seeing exactly which clauses were ignored.
  - Alternatives considered: hard failure on any unsupported token, silently dropping unsupported clauses.
  - Risk: Users may overlook unsupported clauses unless the UI surfaces them clearly later.
  - Status: Accepted for CLI Phase Search-1.

- Decision: Treat search as substrate, not the product center.
  - Reason: Local syntax search verifies offline Scryfall querying and supports future lookup, browsing, and candidate pools, but the Workbench product is deck understanding.
  - Alternatives considered: continuing toward an offline Scryfall clone or designing the app around search-first workflows.
  - Risk: Search still needs to become strong in-app later, so scope limits must not be confused with abandoning search quality.
  - Status: Accepted.

- Decision: Complete only the specified Search-2 filters before moving toward deck-understanding work.
  - Reason: The pending filters are useful infrastructure, but broad syntax expansion should not delay Deck Skeleton Report v0 and structural analysis.
  - Alternatives considered: full Scryfall syntax parity now, stopping search immediately, or prioritizing search UI.
  - Risk: Future users may expect more search operators; unsupported syntax must stay explicit until those operators are deliberately added.
  - Status: Accepted.

## 2026-07-10

- Decision: Treat the deckbuilder workspace as the primary product screen.
  - Reason: The user clarified that the next priority is planning the main deckbuilder surface from Archidekt/Deckcheck-style capability examples.
  - Alternatives considered: search-first UI, dashboard-first UI, or continuing only CLI/backend work.
  - Risk: UI planning can drift into visual cloning if not constrained.
  - Status: Accepted for product planning.

- Decision: Use reference screenshots for capability extraction only.
  - Reason: The screenshots are tidy examples but not the final UI goal or clone target.
  - Alternatives considered: copying exact visual styling, ignoring the references entirely.
  - Risk: Capability notes may miss subtle interaction details until the PDF is manually reviewed in a proper viewer.
  - Status: Accepted.

- Decision: Set up only free, isolated frontend tooling before UI implementation.
  - Reason: Future glass/liquid UI work needs Node-based tooling, but the product should not be over-built before deckbuilder requirements and model contracts are ready.
  - Alternatives considered: no frontend tooling yet, paid UI kits, desktop packaging now, or product UI implementation now.
  - Risk: Tooling can create the impression that UI implementation has started; docs must keep this as scaffold-only.
  - Status: Accepted.

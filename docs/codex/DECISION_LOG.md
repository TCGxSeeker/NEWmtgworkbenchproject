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

- Decision: Complete Search-2 with only the approved local filters.
  - Reason: `legal:commander`, `usd<=N`, `r:<rarity>`, `set:<code>`, and `is:commander` are useful for future in-app lookup while keeping search scoped as infrastructure.
  - Alternatives considered: broader Scryfall syntax parity, live Scryfall queries, or delaying all search work until deck reports.
  - Risk: Price and legality filters reflect only the local snapshot and can become stale.
  - Status: Accepted and implemented.

- Decision: Prioritize Deckbuilder Foundation v0 as the next product planning milestone.
  - Reason: The main deckbuilder workspace is the product center, and supporting search, stats, import/export, and report features should be planned around that screen.
  - Alternatives considered: continuing broad search syntax expansion, starting UI implementation immediately, or prioritizing report-only planning.
  - Risk: Foundation planning can still drift into implementation if boundaries are not kept explicit.
  - Status: Accepted for planning.

- Decision: Use `.mtgwdeck.json` as the native saved deck workspace format.
  - Reason: The deckbuilder needs to preserve editable workspace state, unknown cards, zones, categories, tags, selected printing placeholders, notes, metadata, and future saved-state fields beyond what plain decklist exports can represent.
  - Alternatives considered: plain text as native state, CSV as native state, or external deckbuilder export formats as native state.
  - Risk: The schema will need explicit versioning and migration discipline as the deckbuilder grows.
  - Status: Accepted for Deck Workspace Model v0.

- Decision: Implement Deck Workspace Mutations v0 as in-place helpers that return the workspace.
  - Reason: `DeckWorkspace` is a mutable dataclass with mutable section lists, and in-place helpers keep future CLI/UI callers straightforward while still supporting chained calls.
  - Alternatives considered: immutable copy-return helpers or direct caller-managed list editing.
  - Risk: Callers must understand that the input object changes immediately.
  - Status: Accepted for Deck Workspace Mutations v0.

- Decision: Treat plain text decklists as import/export formats, not native workspace state.
  - Reason: Plain text is useful for moving decklists in and out, but `.mtgwdeck.json` preserves zones, unresolved state, categories, tags, metadata, selected-printing placeholders, and saved-state data.
  - Alternatives considered: storing plain text as the primary deck state or waiting for external deckbuilder import formats first.
  - Risk: Plain text round trips will not perfectly reconstruct comments or every original header choice.
  - Status: Accepted for Deck Workspace Import/Export v0.

- Decision: Mark workspaces clean after successful native save and after file load.
  - Reason: Dirty state should represent unsaved in-memory changes, not a persisted file that was just loaded or successfully written.
  - Alternatives considered: preserving dirty state from disk or waiting for a full workspace session layer.
  - Risk: Low-level JSON dumps can still serialize dirty state for tests or diagnostics, so callers should use `save_workspace` for real saves.
  - Status: Accepted for Deck Workspace Import/Export v0.

## 2026-07-11

- Decision: Define Category Taxonomy v0 as a controlled category language, not an auto-categorization engine.
  - Reason: Imported/user categories should be preserved, normalized categories should help future reasoning, and deck-specific role must remain the source of truth.
  - Alternatives considered: auto-categorizing cards immediately, ingesting a large card-to-category dataset, or treating imported category names as authoritative deck roles.
  - Risk: Future code may over-count roles if category hints are treated as primary roles without a deck-context role model.
  - Status: Accepted for Category Taxonomy v0.

- Decision: Use a repository-root import shim for test command hygiene.
  - Reason: The project uses a `src/` layout, and the standard command `python -m unittest discover -s tests` should work from the repository root without manual `PYTHONPATH` setup.
  - Alternatives considered: requiring `PYTHONPATH`, editing every test file, adding packaging/install steps, or using `sitecustomize.py`.
  - Risk: The root shim duplicates minimal package metadata and must keep pointing submodule imports at `src/mtg_workbench`.
  - Status: Accepted for Test Command Hygiene v0.

- Decision: Keep Category Taxonomy Loader/Normalizer v0 separate from workspace mutation.
  - Reason: The current deck entry model cannot preserve imported and normalized category fields separately yet, so the normalizer should return `input_category`, `normalized_category`, and origin metadata without overwriting user/imported labels.
  - Alternatives considered: immediately normalizing import/export categories in place or adding deck-entry schema fields in this slice.
  - Risk: Import/export will not use aliases automatically until a later category field-model slice.
  - Status: Accepted for Category Taxonomy Loader/Normalizer v0.

- Decision: Preserve deck entry category provenance separately from grouping categories and future role truth.
  - Reason: Imported labels, taxonomy-normalized categories, generic hints, and deck-specific roles have different meanings and should not overwrite each other.
  - Alternatives considered: continuing to store only `categories`, normalizing imported labels in place, or enforcing primary roles immediately.
  - Risk: The model has more nullable metadata fields before UI controls exist, so future code must avoid treating empty fields as analysis failures.
  - Status: Accepted for Deck Entry Category Metadata v0.

- Decision: Add explicit category metadata edit helpers without changing the grouping category.
  - Reason: Users and future UI actions need to revise imported, normalized, hint, origin, and secondary-tag metadata after import without silently changing deck organization.
  - Alternatives considered: overloading `move_category`, auto-normalizing all category edits, or waiting for UI controls before adding mutation helpers.
  - Risk: Callers must choose between grouping edits and metadata edits deliberately.
  - Status: Accepted for Deck Workspace Category Editing Helpers v0.

- Decision: Design deterministic rules-based analysis before implementing automated deck analysis or recommendations.
  - Reason: The product needs reproducible local evidence, explainable scoring, and clear human validation boundaries before any recommendation engine exists.
  - Alternatives considered: implementing analysis directly from current fixtures, AI-assisted recommendations, live API-backed recommendations, or popularity-driven ranking.
  - Risk: The algorithm may need refinement once real deck fixtures and scoring rubrics are supplied.
  - Status: Accepted for Deterministic Deck Analysis Algorithm v0 planning.

- Decision: Use YAML for Role Rules v0 with deterministic 0-100 evidence bands.
  - Reason: Role rules need to be local, readable, editable, fixture-friendly, and explainable before any analyzer or recommender is implemented.
  - Alternatives considered: hardcoded role rules, JSON-only rules, database-first storage, or immediate card-to-role dataset ingestion.
  - Risk: The first schema may need refinement once a loader and real card fixtures exercise edge cases.
  - Status: Accepted for Role Rules v0.

- Decision: Start Role Rules Loader v0 with the tiny YAML subset and `highest_match` scoring only.
  - Reason: The next slice should verify deterministic loading and simple evidence matching before expanding scoring or classification behavior.
  - Alternatives considered: full YAML support, additive capped scoring, immediate card classification, or starting deck analysis directly.
  - Risk: Early loader behavior will be intentionally narrow and may need expansion after fixture-backed tests.
  - Status: Accepted as next-slice default.

- Decision: Keep Role Evidence Matcher v0 scoped to explicit `CardRoleFacts`.
  - Reason: Matching should prove deterministic local evidence behavior before deriving facts from full card records or deck workspaces.
  - Alternatives considered: classifying full decks immediately, deriving card facts from the Scryfall index in the same slice, or selecting primary roles automatically.
  - Risk: Callers must build `CardRoleFacts` explicitly until a later bridge slice exists.
  - Status: Accepted for Role Evidence Matcher v0.

- Decision: Separate role evidence report summaries from machine/debug evidence.
  - Reason: The UI visibility doctrine requires concise default summaries, optional explanations, and raw evidence only for advanced/debug contexts.
  - Alternatives considered: returning raw matcher objects only, flattening all evidence into user-visible text, or waiting for full deck reports.
  - Risk: This report is intentionally card-level role evidence, not a full deck report.
  - Status: Accepted for Role Evidence Report v0.

- Decision: Add a small Card Facts Adapter before full card classification.
  - Reason: Role evidence matching needs a deterministic bridge from local/Scryfall-ish card dictionaries to explicit `CardRoleFacts` without starting deck analysis.
  - Alternatives considered: making the matcher accept raw card records directly, deriving facts inside full deck analysis, or ingesting large Scryfall datasets first.
  - Risk: The adapter uses conservative subtype parsing and may need expansion when richer local card models arrive.
  - Status: Accepted for Card Facts Adapter v0.

- Decision: Add a thin Card Role Evidence Pipeline before deck-level reports.
  - Reason: Local/Scryfall-ish card records should flow through the existing card facts adapter and role evidence report without teaching the matcher about raw record shapes.
  - Alternatives considered: making report builders accept raw dictionaries directly, starting deck analysis immediately, or selecting primary roles in the same slice.
  - Risk: This remains card-level evidence only, so future deck reports still need an explicit workspace/deck aggregation layer.
  - Status: Accepted for Card Role Evidence Pipeline v0.

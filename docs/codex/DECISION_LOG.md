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

- Decision: Start deck reporting with structural skeleton facts only.
  - Reason: The product needs a trustworthy inventory layer before structural warnings, role summaries, or analysis can make use of deck data.
  - Alternatives considered: starting strategic analysis immediately, counting deck-level roles from card evidence, or warning on duplicate cards without local card facts.
  - Risk: Skeleton v0 intentionally omits strategic quality judgments and may feel sparse until Structural Warnings v0 is added.
  - Status: Accepted for Deck Skeleton Report v0.

- Decision: Keep Structural Warnings v0 mechanical and skeleton-driven.
  - Reason: Warnings can safely surface missing commander, active quantity, unresolved entries, missing local facts, and known non-basic duplicates without making strategy or quality claims.
  - Alternatives considered: adding shell-quality warnings, role-density warnings, or inspecting raw card records directly.
  - Risk: The warning set is intentionally narrow until deck-level role counting and strategy checks are approved.
  - Status: Accepted for Structural Warnings v0.

- Decision: Use the existing card catalog lookup key for deckbuilder card fact resolution.
  - Reason: `normalize_lookup_key` is already used by `CardCatalog` and local Scryfall indexing/search, so the deckbuilder bridge should not create another card-name normalization system.
  - Alternatives considered: keeping the private skeleton-report normalizer, matching on raw entry names only, or querying the local Scryfall index directly in this slice.
  - Risk: `CardCatalog.find()` cannot expose ambiguous matches, so ambiguity reporting is limited to supplied record collections where duplicate normalized keys can be observed.
  - Status: Accepted for Local Card Fact Lookup Bridge v0.

## 2026-07-12

- Decision: Add a Deck Inspection Report envelope before deck-level role summaries.
  - Reason: The project needs one stable report object that composes skeleton facts, mechanical warnings, card fact coverage, and optional card-level role evidence without starting strategic analysis.
  - Alternatives considered: jumping directly to deck role counts, shell-quality warnings, or a full deck report.
  - Risk: The envelope may feel factual and sparse until later approved slices add deck-context role summaries and analysis.
  - Status: Accepted for Deck Inspection Report Envelope v0.

- Decision: Add a stable deck inspection smoke fixture before broadening reports.
  - Reason: The factual report envelope needs a deterministic end-to-end guard against network use, workspace mutation, accidental strategic fields, and output drift.
  - Alternatives considered: relying only on unit tests or moving directly into CLI/report surfaces.
  - Risk: Expected-output fixtures require intentional updates when report shape changes.
  - Status: Accepted for Deck Inspection Fixture Smoke v0.

- Decision: Plan card relationships as behavioral primitives before deriving edges.
  - Reason: Future synergy/package work needs a factual vocabulary for behavior interfaces and relationship evidence before any scoring or judgment exists.
  - Alternatives considered: package detection first, role-count-driven relationships, all-pairs card comparison, or recommendation-oriented synergy scoring.
  - Risk: The primitive vocabulary may need refinement once typed models and behavior extraction reveal real edge cases.
  - Status: Accepted for Card Relationship Primitives v0 planning.

## 2026-07-20

- Decision: Repair post-July-12 foundation drift before starting new feature work.
  - Reason: The multi-agent catchup audit found stale status docs, moved-repository path drift, a relationship smoke contradiction, validation gaps, lookup parity concerns, and Scryfall index portability risks even though the full suite currently passes.
  - Alternatives considered: proceeding directly into the next deckbuilder or relationship feature slice, or treating passing tests as proof that the foundation is pristine.
  - Risk: Cleanup delays new visible features, but it reduces later backtracking and keeps the deterministic foundation honest.
  - Status: Accepted for the current catchup repair queue.

- Decision: Relationship smoke fixtures may use explicit fixture-level profile atoms, but edges must come only from declared source-target pairs.
  - Reason: The smoke fixture needs to demonstrate unsupported behavior such as discard-event observation without hiding pair injection in Python code or pretending the bounded extractor supports more than it does.
  - Alternatives considered: keeping hardcoded event edges in the smoke helper, expanding the bounded extractor to support discard listeners immediately, or removing the trigger relationship from the smoke fixture.
  - Risk: Fixture-level atoms are a smoke-test convenience, not a general card modeling feature; future production behavior still needs explicit extraction or profile sources.
  - Status: Accepted for Relationship Smoke Repair v0.

- Decision: Treat relationship confidence bands as exact integer contract values.
  - Reason: Python equality lets `False` match `0` and `25.0` match `25`, but relationship evidence should preserve explicit deterministic band values rather than accepting lookalikes.
  - Alternatives considered: relying on membership checks only, coercing numeric values to integers, or accepting any numeric value that compares equal to a supported band.
  - Risk: Callers that pass malformed confidence bands now receive domain-specific validation errors instead of permissive acceptance.
  - Status: Accepted for Relationship Contract Hardening Patch.

- Decision: Use normalized canonical card name as the no-Oracle logical identity for local card fact lookup.
  - Reason: `CardCatalog` already treats no-Oracle records with the same normalized name as one logical card identity, so deckbuilder lookup should not turn different printings of that same name into ambiguity.
  - Alternatives considered: using selected printing identity first, treating all no-Oracle duplicates as ambiguous, or requiring Oracle IDs before lookup can resolve a card.
  - Risk: Distinct real cards without Oracle IDs but sharing the same name cannot be separated until richer identity data is supplied; aliases across different no-Oracle names still remain ambiguous.
  - Status: Accepted for Workspace/Card Lookup Integrity Patch.

- Decision: Treat Scryfall SQLite DB and index manifest replacement as one local rebuild checkpoint.
  - Reason: A rebuilt database without its matching `index_manifest.json` can misrepresent snapshot provenance, especially after repository moves or partial failures.
  - Alternatives considered: writing the manifest after replacing the DB, ignoring stale manifest risk, or requiring manual cleanup after failed rebuilds.
  - Risk: Cross-file replacement cannot be crash-atomic at the filesystem level, but handled failures now roll back both files and remove temporary outputs.
  - Status: Accepted for Scryfall Index Portability and Atomicity Patch.

- Decision: Keep visual card comparison direction-free, and make optional relationship inspection explicitly source-to-target.
  - Reason: The pair-inspection implementation derives one directional relationship at a time, and tests lock that reverse direction is not automatic.
  - Alternatives considered: automatically inspecting both directions, prompting for direction before visual comparison, or showing relationship evidence by default.
  - Risk: Users may need a clear affordance to inspect the reverse direction later, but the baseline compare flow remains calm and analysis-free.
  - Status: Accepted for Visual Compare Direction Decision.

- Decision: Expose the factual deck inspection envelope through the CLI before broader deck analysis.
  - Reason: The backend already has deterministic skeleton, structural warning, card lookup, and optional card-level role evidence reports, but users need a local command to run that bounded report outside tests.
  - Alternatives considered: starting deck-level role counting, adding UI, or continuing only with internal report modules.
  - Risk: The command may look report-like while still intentionally omitting strategic analysis, so CLI help and docs must preserve the factual-only boundary.
  - Status: Accepted for Deck Inspection CLI v0.

- Decision: Expose native workspace import/export through file-based CLI commands.
  - Reason: Plain text is a boundary format and `.mtgwdeck.json` is the saved workspace source of truth, so a tiny local CLI bridge helps move deck files without starting UI work.
  - Alternatives considered: adding app UI import/export, expanding to external deckbuilder formats, or leaving import/export helpers internal only.
  - Risk: The commands intentionally do not preserve every original comment/header from source text, so richer format preservation remains a future explicit slice.
  - Status: Accepted for Native Workspace Import/Export CLI v0.

- Decision: Require explicit output paths for workspace mutation CLI commands.
  - Reason: Mutation commands edit saved deck workspaces, so copy-out behavior is safer than silently overwriting the input file.
  - Alternatives considered: in-place mutation by default, a single broad mutation command, or deferring mutation CLI until app UI exists.
  - Risk: Users must pass an extra path, but the workflow remains reviewable and can still overwrite intentionally by using the same path.
  - Status: Accepted for Deck Workspace Mutation CLI v0.

- Decision: Add compact factual summaries to `inspect-deck` through `--summary-only`.
  - Reason: The full inspection envelope is useful for machines and debugging, but quick CLI review needs a smaller payload that still avoids strategic claims.
  - Alternatives considered: changing the default inspect output, adding prose output, or exposing debug fields by default.
  - Risk: Summary-only output may need additional fields later, but it keeps raw report details behind an explicit full-output path.
  - Status: Accepted for Deck Inspection CLI Polish v0.

- Decision: Expose category metadata and entry annotation edits through explicit copy-out CLI commands.
  - Reason: The deckbuilder workspace already has safe in-memory helpers for imported/normalized category metadata, secondary tags, notes, and tags, and file-based commands make those saved workspace edits testable before UI work.
  - Alternatives considered: waiting for app UI controls, adding one broad generic mutation command, or exposing deck-specific primary-role assignment now.
  - Risk: The command list is intentionally mechanical and may later consolidate behind UI actions, but the explicit CLI surface avoids hidden strategic role changes.
  - Status: Accepted for Category Metadata Mutation CLI v0 and Entry Annotation CLI v0.

- Decision: Add a read-only workspace view projection layer before UI implementation.
  - Reason: The main deckbuilder screen will need grouped, sorted, and filtered entry data, and this behavior can be made deterministic without building visual components or starting analysis.
  - Alternatives considered: waiting until React UI work, projecting directly inside future UI components, or expanding projection through card facts immediately.
  - Risk: V0 only covers existing workspace fields, so type/mana/color/price projections need later card-fact-backed slices.
  - Status: Accepted for Deck Workspace View Projection v0.

- Decision: Expose workspace view projections through a read-only CLI command.
  - Reason: The projection layer should be inspectable and testable from local files before any deckbuilder UI consumes it.
  - Alternatives considered: leaving projection internal-only until UI work or adding a saved projection output file.
  - Risk: CLI JSON is a developer-facing preview of view data, not a committed UI contract.
  - Status: Accepted for Workspace View CLI v0.

- Decision: Add type and mana-value projection through explicit local card fact lookup results.
  - Reason: The main deckbuilder needs factual grouping and sorting beyond saved categories, but missing and ambiguous card data must stay visible instead of being guessed.
  - Alternatives considered: parsing type/mana value directly from workspace labels, requiring all entries to resolve before projection, or waiting until UI implementation.
  - Risk: Projection behavior now depends on local card source coverage; future UI must clearly surface missing/ambiguous fact buckets.
  - Status: Accepted for Card-Fact-Backed Workspace Projection v0.

- Decision: Add color and color-identity projection through explicit local card fact lookup results.
  - Reason: Future deckbuilder controls need factual color views, but colorless, missing, and ambiguous data must be distinct.
  - Alternatives considered: deriving color from saved categories, treating missing color fields as colorless, or waiting until UI implementation.
  - Risk: Multicolor `color` grouping duplicates entries across visible groups by design, so consumers must use grouped totals consciously.
  - Status: Accepted for Color Identity Workspace Projection v0.

- Decision: Lock one end-to-end workspace-view projection with an exact expected JSON fixture.
  - Reason: The future deckbuilder UI will consume projection output, so grouping, sorting, missing facts, ambiguity, and stable ordering should have fixture-level contract coverage before more modes are added.
  - Alternatives considered: relying only on focused unit tests, waiting until UI implementation, or snapshotting a large real deck.
  - Risk: The fixture protects one representative projection, not every future view mode; broader contracts still need their own explicit slices.
  - Status: Accepted for Workspace View Fixture Smoke v0.

- Decision: Document `deck_workspace_view_projection.v0` as a consumer contract before UI work.
  - Reason: The first visible deck screen should consume a stable view model without exposing backend validation plumbing as normal deckbuilder UI.
  - Alternatives considered: letting future UI infer behavior from tests, documenting only after UI implementation, or treating projection JSON as a private implementation detail.
  - Risk: The contract may need a future version if syntax filters, price, rarity, printing, or sideboard fields are added.
  - Status: Accepted for Workspace Projection Contract Docs v0.

- Decision: Implement `See The Deck v0` as a fixture-backed visible deck screen.
  - Reason: The product needs to start moving from backend contracts toward a usable deckbuilder surface, but the first UI slice should only show data and controls that already work.
  - Alternatives considered: adding import/add/export buttons immediately, starting with card-image grid view, or surfacing inspection/debug coverage in the default screen.
  - Risk: The screen is not yet connected to user-selected deck files or backend mutation commands; human visual review is required before expanding workflows.
  - Status: Accepted for See The Deck v0.

- Decision: Keep `See The Deck v0` deck-first on stacked layouts.
  - Reason: Narrow visual review showed the header/status and secondary snapshot panel could crowd the first card workspace.
  - Alternatives considered: leaving the secondary snapshot above the card list, hiding the snapshot entirely, or adding new drawer behavior.
  - Risk: The snapshot panel still repeats some header counts until a real details/stats surface exists.
  - Status: Accepted for See The Deck v0 Visual Review Checkpoint.

- Decision: Implement `Find And Add Cards v0` as local UI state over a tiny card fixture.
  - Reason: The first add workflow should prove the visible deckbuilder loop without adding persistence, backend file writes, live search, recommendations, scoring, or broader syntax behavior.
  - Alternatives considered: wiring directly to native workspace file mutation commands, opening full local Scryfall search in the UI, or adding recommendation-style candidate lists.
  - Risk: Added cards reset on refresh until app-native persistence is explicitly wired.
  - Status: Accepted for Find And Add Cards v0.

- Decision: Preserve the collapsible add-card panel concept but reject current styling as final.
  - Reason: Human review found the function highly responsive and the collapsible add-card surface directionally useful, while calling the visual treatment rough test-flight quality.
  - Alternatives considered: treating the current screen as visually approved, or removing the collapsible add surface entirely.
  - Risk: Future UI work may need a deliberate visual design pass before adding too many more visible workflows.
  - Status: Accepted as human validation feedback after Find And Add Cards v0.

- Decision: Capture side-project screenshot cues as visual inspiration only.
  - Reason: The user identified satisfying visual qualities such as polished buttons, responsive feel, clear panels, and calm dark styling, while explicitly excluding the side project's non-MTG domain content.
  - Alternatives considered: ignoring the screenshot, copying the design directly, or storing unrelated side-project product details in MTG Workbench docs.
  - Risk: Future visual work could overfit to a utility layout unless references remain capability/style cues rather than clone targets.
  - Status: Accepted as visual-reference guidance.

- Decision: Capture Archidekt new-deck and search/add screenshots as pathing reference only.
  - Reason: The screenshots show useful deckbuilder interaction patterns: simple deck creation, advanced options hidden by default, empty deck guidance, focused search tabs, card-image search grids, and immediate quantity feedback after add.
  - Alternatives considered: cloning the interface, ignoring the reference, or importing hosted/account/advertising behavior into the local app.
  - Risk: The reference is visually dense in places, so MTG Workbench must keep search/add secondary to the deck workspace and calmer than the source.
  - Status: Accepted as product-reference guidance.

- Decision: Treat deck stats and probability tools as endpoint features, not default dashboard clutter.
  - Reason: The reference screenshot confirms stats are expected, but the user is comfortable with them living below the deck on scroll or in their own tab.
  - Alternatives considered: making stats a top-level dashboard, hiding stats entirely, or adding optimizer controls immediately.
  - Risk: Stats can become visually noisy unless placement and progressive disclosure stay deliberate.
  - Status: Accepted as product-reference guidance.

- Decision: Scope Card Details Surface v0 to local factual fields.
  - Reason: The reference screenshots show rich details, tags, prices, legalities, printings, and links, but many of those fields require online services, local snapshots, or separate policy decisions.
  - Alternatives considered: copying the full rich details surface now, ignoring card details, or mixing recommendation/debug fields into the first details view.
  - Risk: The first details slice may feel plain until local images, oracle tags, legality, and printing data are wired.
  - Status: Accepted as next-slice guidance.

- Decision: Implement Card Details Surface v0 as a factual local panel.
  - Reason: The deckbuilder's next north-star step is understanding a card, and the current UI already has explicit deck rows, table rows, and search results that can open factual details without adding strategic claims.
  - Alternatives considered: copying the richer Archidekt modal, adding card images immediately, or waiting until the local Scryfall index is wired into the frontend.
  - Risk: The panel is intentionally plain and fixture-limited until local oracle text, images, printings, and richer local facts are separately approved and wired.
  - Status: Accepted for Card Details Surface v0.

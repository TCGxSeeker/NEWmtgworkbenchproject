# Next Session Handoff

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Current branch: `master`
- Current implemented checkpoint: Deck Library, Context Consolidation, and Save/Open UI v0
- Remote: `origin` at `https://github.com/TCGxSeeker/NEWmtgworkbenchproject.git`
- Steps 1-4 repair batch committed as `df46b33 Repair catchup foundation contracts`
- Step 5 Scryfall index repairs committed as `7f67e40 Harden Scryfall index persistence`
- Step 6 visual compare direction docs are complete
- Current verification: `python -m unittest discover -s tests` passed with 344 tests
- Current frontend verification: `npm run build` and `npm run lint` passed in
  `apps/deckbuilder-ui`
- Current focused deck workspace view projection verification: `python -m unittest tests.test_deckbuilder_workspace_view` passed with 14 tests
- Current focused workspace view CLI verification: `python -m unittest tests.test_cli_workspace_view` passed with 7 tests
- Current focused workspace category/annotation CLI verification: `python -m unittest tests.test_cli_workspace_category_metadata` passed with 5 tests
- Current focused Deck Workspace Mutation CLI verification: `python -m unittest tests.test_cli_workspace_mutations` passed with 6 tests
- Current Deck Workspace Mutation CLI smoke: `workspace-add-card` added `Alias Helper` to a temporary native workspace with local card catalog resolution
- Current focused Native Workspace Import/Export CLI verification: `python -m unittest tests.test_cli_workspace_import_export` passed with 5 tests
- Current Native Workspace Import/Export CLI smoke: `workspace-import` and `workspace-export` round-tripped `tests/fixtures/deckbuilder/commander_import.txt` through a temporary `.mtgwdeck.json` file
- Current focused Deck Inspection CLI verification: `python -m unittest tests.test_cli_inspect_deck` passed with 8 tests
- Current Deck Inspection CLI smoke: `python -m mtg_workbench.cli inspect-deck tests/fixtures/deckbuilder/inspection_smoke_workspace.mtgwdeck.json --card-records tests/fixtures/deckbuilder/inspection_smoke_card_records.json` passed
- Current Deck Inspection CLI summary smoke: `python -m mtg_workbench.cli inspect-deck tests/fixtures/deckbuilder/inspection_smoke_workspace.mtgwdeck.json --card-records tests/fixtures/deckbuilder/inspection_smoke_card_records.json --summary-only` passed
- Current focused pair-inspection verification: `python -m unittest tests.test_relationship_pair_inspection tests.test_card_record_pair_inspection` passed with 21 tests
- Current focused Scryfall index verification: `python -m unittest tests.test_scryfall_indexer` passed with 5 tests
- Current focused workspace/card lookup verification: `python -m unittest tests.test_deckbuilder_mutations tests.test_cards_catalog tests.test_deckbuilder_card_fact_lookup tests.test_deckbuilder_deck_inspection_report` passed with 85 tests
- Current focused contract verification: `python -m unittest tests.test_relationship_input_contract_hardening tests.test_relationship_primitives tests.test_card_behavioral_profile tests.test_behavioral_atom_extraction` passed with 42 tests
- Current focused smoke verification: `python -m unittest tests.test_relationship_pipeline_fixture_smoke` passed with 7 tests
- Current whitespace check: `git diff --check` passed
- Frontend scaffold verification before Step 1 repairs: `npm run build` and `npm run lint` passed in `apps/deckbuilder-ui`

## Current Completed Milestones

- Deck Workspace Model v0
- Deck Workspace Mutations v0
- Deck Workspace Import/Export v0
- Category Taxonomy v0
- Category Taxonomy Loader/Normalizer v0
- Deck Entry Category Metadata v0
- Deck Workspace Category Editing Helpers v0
- Deterministic Deck Analysis Algorithm Spec v0
- Role Rules v0
- Role Rules Loader v0
- Role Evidence Matcher v0
- Role Evidence Report v0
- Card Facts Adapter v0
- Local Card Fact Lookup Bridge v0
- Card Role Evidence Pipeline v0
- Deck Skeleton Report v0
- Structural Warnings v0
- Deck Inspection Report Envelope v0
- Deck Inspection Fixture Smoke v0
- Card Relationship Primitives Plan v0
- Workspace Entry Identity Integrity v0
- Card Catalog Identity Bridge v0
- Deck Inspection Source Unification v0
- Atomic Local Persistence v0
- Typed Relationship Primitives v0
- Factual Card Behavioral Profile v0
- Bounded Behavioral Atom Extraction v0
- Deterministic Relationship Edge Derivation v0
- Card Relationship Report v0
- Relationship Pipeline Fixture Smoke v0
- Relationship Input Contract Hardening v0
- Explicit Relationship Pair Inspection v0
- Explicit Card Record Pair Inspection v0
- Visual Card Pair Compare v0 Planning
- Deck Inspection CLI v0
- Native Workspace Import/Export CLI v0
- Deck Workspace Mutation CLI v0
- Deckbuilder Acceptance Checklist Cleanup
- Deck Inspection CLI Polish v0
- Category Metadata Mutation CLI v0
- Entry Annotation CLI v0
- Deck Workspace View Projection v0
- Workspace View CLI v0
- Card-Fact-Backed Workspace Projection v0
- Color Identity Workspace Projection v0
- Workspace View Fixture Smoke v0
- Workspace Projection Contract Docs v0
- See The Deck v0
- See The Deck v0 Visual Review Checkpoint
- Find And Add Cards v0
- Card Details Surface v0
- Mechanical Deck Validation Surface v0
- Deckbuilder UI Logic Extraction v0
- User Reviewer Skill v0
- Current Deckbuilder UI User Review v0
- Current Deckbuilder UI Human Browser Pass v0
- Deck Library, Context Consolidation, and Save/Open UI v0

## Audit Status

The repository is functional but not pristine. The full unit suite, compile checks, CLI smoke checks, local search smoke checks, frontend build, frontend lint, and current whitespace check passed before Step 1 repairs. The multi-agent catchup audit still found contract drift, stale documentation, and a few fragile behaviors that should be repaired before new feature work.

Step 1 is a documentation/status repair pass only. It should align current docs, handoffs, task pointers, and verification notes with the moved `G:` repository and the completed post-July-12 work.

## Completed Catchup Repairs

### Step 1: Current Docs/Status Repair

Updated current repository path, current head, current test baseline, stale historical handoff markers, and the active repair queue.

### Step 2: Relationship Smoke Repair v0

Removed hidden relationship injection from the smoke helper. The discard listener behavior now lives in explicit fixture-level `profile_atoms`, and the discard relationship is produced only when the fixture declares the source-target pair. A regression test proves undeclared event pairs are not invented.

### Step 3: Relationship Contract Hardening Patch

Tightened confidence-band validation so only exact integer band values are accepted, added missing negative tests for malformed relationship/profile inputs, and updated bounded atom extraction docs for the Treasure-sacrifice rule.

### Step 4: Workspace/Card Lookup Integrity Patch

Rejected invalid supplied workspace entry IDs before entry creation, aligned no-Oracle lookup identity with `CardCatalog`, and added independent expected-output assertions for inspection source unification.

### Step 5: Scryfall Index Portability and Atomicity Patch

Added moved-repo fallback for stale Scryfall manifest source paths and hardened DB/manifest replacement so handled manifest replacement failures restore the previous local index state.

### Step 6: Visual Compare Direction Decision

Clarified how a future `Inspect interaction` UI action chooses source and target direction. Baseline visual comparison remains direction-free and analysis-free. Optional relationship inspection uses the card that started comparison as the default source and the second selected card as the default target. Reverse inspection is not automatic and must be requested explicitly.

Known files:

- `docs/product/deckbuilder/VISUAL_CARD_PAIR_COMPARE_V0.md`
- `src/mtg_workbench/deckbuilder/relationship_pair_inspection.py`
- `src/mtg_workbench/deckbuilder/card_record_pair_inspection.py`
- `tests/test_relationship_pair_inspection.py`
- `tests/test_card_record_pair_inspection.py`

## Active Catchup Repair Queue

- No active numbered catchup repair remains after Step 6.
- Before starting new feature work, do a deliberate readiness checkpoint and
  choose the next bounded slice.
- Deck Inspection CLI v0 exposes the factual report envelope through
  `python -m mtg_workbench.cli inspect-deck`.
- Native Workspace Import/Export CLI v0 exposes plain text to
  `.mtgwdeck.json` movement through `workspace-import` and `workspace-export`.
- Deck Workspace Mutation CLI v0 exposes safe copy-out commands for add,
  remove, quantity, zone move, and set commander.
- Deck Inspection CLI Polish v0 adds `--summary-only` and clear missing-file
  errors.
- Category Metadata Mutation CLI v0 exposes safe copy-out commands for imported
  category, normalized category, generic category hint, category origin,
  secondary tags, and clearing category metadata.
- Entry Annotation CLI v0 exposes safe copy-out commands for notes and tags.
- Deck Workspace View Projection v0 creates read-only grouped, sorted, and
  filtered projections over existing saved workspace fields.
- Workspace View CLI v0 exposes those projections through
  `python -m mtg_workbench.cli workspace-view`.
- Card-Fact-Backed Workspace Projection v0 adds factual `type` and
  `mana_value` grouping/sorting when explicit local card facts are supplied.
  Missing and ambiguous facts remain visible as status buckets.
- Color Identity Workspace Projection v0 adds factual `color` and
  `color_identity` grouping/sorting when explicit local card facts are supplied.
  Colorless, missing, and ambiguous data remain distinct.
- Workspace View Fixture Smoke v0 locks one exact expected-output fixture for
  `workspace-view` through the real CLI, local card records, color-identity
  grouping, mana-value sorting, deterministic reruns, and no workspace mutation.
- Workspace Projection Contract Docs v0 documents
  `deck_workspace_view_projection.v0` as the current consumer contract for
  future deckbuilder screens.
- See The Deck v0 replaces the starter Vite screen with a fixture-backed deck
  workspace that supports grouped/table views, current-deck filtering, and group
  collapse without showing inactive workflow buttons or debug metrics.
- See The Deck v0 Visual Review Checkpoint corrected narrow-screen overflow,
  kept the deck workspace ahead of the secondary snapshot panel on stacked
  layouts, and preserved the no-debug/no-inactive-controls default UI.
- Find And Add Cards v0 adds a functional Add Card entry point, tiny local
  card-search fixture, mainboard/maybeboard add target, explicit add action,
  quantity incrementing for same-card/same-zone entries, visible unsaved state,
  and separate current-deck filtering versus global card search.
- Card Details Surface v0 adds explicit details actions on deck rows, table
  rows, and search results. The panel shows only local factual fields already
  present in the fixture data and does not add live price, legality, rank, salt,
  printing, marketplace, oracle-tag, recommendation, scoring, role-judgment, or
  card-image behavior.
- Mechanical Deck Validation Surface v0 adds a compact sidebar check from
  current UI deck state only: commander presence, Commander active count versus
  100, unresolved entries, and duplicate non-basic active cards.
- Deckbuilder UI Logic Extraction v0 moves pure UI helpers into
  `apps/deckbuilder-ui/src/deckUiLogic.ts` without adding visible behavior. This
  keeps `App.tsx` focused on rendering and state orchestration before save/load
  or backend validation wiring.
- User Reviewer Skill v0 adds `.agents/skills/user-reviewer/SKILL.md` and
  `docs/product/deckbuilder/USER_REVIEW_RUBRIC.md` for structured user-perspective
  ratings of completed UI or visualization checkpoints.
- Current Deckbuilder UI User Review v0 adds
  `docs/product/deckbuilder/reviews/CURRENT_UI_USER_REVIEW_2026-07-24.md`.
  The review found medium clutter risk, no blockers for continuation, and a
  recommended next visual move: consolidate the right-side supporting area into
  a calmer progressively disclosed deck context region.
- Current Deckbuilder UI Human Browser Pass v0 records the user's live review:
  functions feel directionally right, visual quality is not final, organization
  needs work, deck snapshot should move lower or out of the cramped side area,
  default mechanical checks should only show actionable warnings, maybeboard
  should be collapsed by default, and full-cardpool search should avoid noisy
  single-character broad lookup.
- Human pass after Find And Add Cards v0: function is highly responsive, and
  the add-card workflow works well as its own collapsible window/panel. Visual
  style is not approved as final; treat it as rough test-flight styling that
  should be modernized later.
- Visual reference note captured from a side-project screenshot: keep the
  transferable cues around polished dark panels, smooth glowing buttons, calm
  success/status banners, tab-like mode controls, and separated side panels.
  Do not import the side project's non-MTG domain, card/deck names, file paths,
  APIs, or service behavior.
- Archidekt reference screenshots captured for new-deck and search/add pathing:
  keep the ideas of a simple new-deck form, collapsed advanced setup, empty
  deck guidance, focused search workspace, search tabs, card-image result grids,
  and immediate added-card quantity feedback. Do not copy hosted visibility
  states, ads, account/profile features, online integrations, recommendation
  tabs, price-source behavior, or exact layout density.
- Archidekt deck-stats screenshot captured as endpoint-feature guidance:
  stats/probability tools may live below the deck, in a tab, or in an optional
  pinned panel; they should cover color cost/production, average and total mana
  value, mana curve, mana curve by color, and draw probability controls. Do not
  add optimizer buttons until local deterministic rules and human validation
  zones are defined.
- Archidekt card-details screenshots captured as next-slice guidance:
  details may use a focused overlay/drawer with card image or placeholder,
  tabs such as card options/card info/oracle tags/more options, and factual
  fields. For v0, show only local factual fields already available. Defer live
  price, legality, EDHREC rank, salt score, printing marketplace data, external
  links, and oracle tags unless backed by verified local data and an explicit
  UI decision.

## Current Readiness Snapshot

- Deckbuilder acceptance checklist checkboxes: all current items complete after
  Deck Library, Context Consolidation, and Save/Open UI v0.
- Native workspace model, editing, import/export, category metadata, annotation,
  and view-projection backend are the most complete deckbuilder areas.
- Finished app UI, recommendation logic, scoring, commander analysis, and
  strategic deck reports remain intentionally early or deferred.
- Canonical framing: MTG Workbench has a strong deckbuilder backend foundation
  with CLI-verifiable contracts. It does not yet have generic deckbuilder parity
  as a user-facing product.
- Safe workspace deletion is doctrine/planned behavior, not completed
  functionality, until a dedicated helper or command exists with tests.

## Next Refresh Notes

- Safe stopping point: Deck Library, Context Consolidation, and Save/Open UI v0 is implemented and verified.
- Human validation note: preserve the collapsible add-card panel concept, but
  do not preserve the current rough visual treatment as final direction.
- Human validation note: Card Details Surface v0 is a functional factual panel,
  not final visual treatment. Review it before expanding details into richer
  images, printings, oracle text, or tabs.
- Visual reference note: `docs/product/deckbuilder/reference/VISUAL_REFERENCE_NOTES.md`
  captures approved style cues only; it is not a clone target or domain source.
- Deck library note: `docs/product/deckbuilder/DECK_LIBRARY_REQUIREMENTS.md`
  captures the clarified app path. MTG Workbench should open to a calm local
  deck library/home screen before entering an individual deck workspace.
- Archidekt pathing reference:
  `docs/product/deckbuilder/reference/ARCHIDEKT_NEW_DECK_SEARCH_REFERENCE.md`
  captures capability and interaction cues only.
- Next recommended slice: Deck Library and Save/Open Human Browser Pass v0.
- Suggested scope: review the library first impression, create-deck flow,
  open-file flow, save/download flow, add-card responsiveness, deck-context
  organization, maybeboard collapsed-by-default behavior, hidden non-actionable
  validation checks, card details without `Zone`, and two-character search
  trigger.
- Product north-star sequence: see the deck, find and add cards, understand a
  card, validate the deck, edit safely in bulk, inspect useful statistics, manage
  printings, and recover earlier versions.
- Deck Role Summary v0 still requires explicit approval because it starts
  deck-level role counting.
- Do not start recommendations, scoring, commander analysis, package detection,
  app UI, or deck-level strategic judgment without a fresh handoff.
- Do not route near-term deckbuilder parity work through recommendation
  commentary unless the user explicitly asks for it.

## Core Constraints

- Product remains local/offline-capable.
- No online dependency.
- No live APIs.
- No telemetry.
- No hosted/cloud dependency.
- No AI/LLM calls.
- Oracle text and local card data are evidence.
- Generic category is a hint.
- Deck-specific role is the truth.
- User/imported labels must be preserved.
- Missing, unknown, or ambiguous facts must stay visible instead of being guessed.
- Not all internal algorithm data should become visible UI text.

## UI Visibility Doctrine

Future UI should use progressive disclosure:

1. Default UI: short human-readable summaries.
2. Expanded UI: concise why-this-was-flagged explanations.
3. Advanced/debug UI: raw rule evidence, confidence scores, matched phrases, and internal data.

Future output schemas should separate machine-readable evidence, concise user-facing summaries, optional explanation text, and debug/internal details.

## Do Not Start Yet

- Full deck analysis.
- Recommendations.
- Candidate search.
- Add/cut scoring.
- Package detection.
- Commander analysis.
- Synergy scoring.
- Deck-level role totals.
- All-pairs relationship comparison.
- Broad unapproved app UI.
- Frontend dependencies.
- Online services or live API calls.
- Full Scryfall auto-categorization.
- Primary-role enforcement.
- Strategic quality judgments.

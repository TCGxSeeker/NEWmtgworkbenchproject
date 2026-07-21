# Next Session Handoff

## Current Baseline

- Repository root: `G:\Documents\New MTG project`
- Current branch: `master`
- Last committed repair checkpoint before Step 6: `7f67e40 Harden Scryfall index persistence`
- Remote: `origin` at `https://github.com/TCGxSeeker/NEWmtgworkbenchproject.git`
- Steps 1-4 repair batch committed as `df46b33 Repair catchup foundation contracts`
- Step 5 Scryfall index repairs committed as `7f67e40 Harden Scryfall index persistence`
- Step 6 visual compare direction docs are complete
- Current verification: `python -m unittest discover -s tests` passed with 298 tests
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
- Workspace visibility-delete behavior
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
- App UI.
- Frontend dependencies.
- Online services or live API calls.
- Full Scryfall auto-categorization.
- Primary-role enforcement.
- Strategic quality judgments.

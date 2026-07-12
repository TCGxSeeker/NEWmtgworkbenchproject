# Next Session Handoff

## Current Baseline

- Repository root: `C:/Users/StDeL/Documents/New MTG project`
- Current branch: `master`
- Current head: `578144b Plan Card Relationship Primitives v0`
- Remote: `origin` at `https://github.com/TCGxSeeker/NEWmtgworkbenchproject.git`
- Working tree at refresh time: clean
- Current verification: `python -m unittest discover -s tests` passed with 183 tests
- `git diff --check` passed

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

## Most Recent Changes

Deck Inspection Fixture Smoke v0 added a stable end-to-end fixture for `build_deck_inspection_report`. It verifies deterministic output, no network use, no workspace mutation, card fact coverage, optional found-card-only role evidence, and no strategic/reporting fields that imply recommendations or deck quality.

Card Relationship Primitives Plan v0 added `docs/codex/CARD_RELATIONSHIP_PRIMITIVES_V0.md`, a tiny JSON vocabulary fixture, and tests that lock the planning contract. It is a vocabulary and doctrine contract only, not a relationship engine.

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

## UI Visibility Doctrine

Not all internal algorithm data should become visible UI text.

Future UI should use progressive disclosure:

1. Default UI: short human-readable summaries.
2. Expanded UI: concise why-this-was-flagged explanations.
3. Advanced/debug UI: raw rule evidence, confidence scores, matched phrases, and internal data.

Future output schemas should separate machine-readable evidence, concise user-facing summaries, optional explanation text, and debug/internal details.

## Established Report Defaults

- `build_deck_skeleton_report` inventories deck metadata, zones, quantities, commander names, active categories, unresolved entries, missing local facts, and known non-basic duplicates.
- `build_structural_warnings_report` consumes skeleton facts and emits mechanical warnings only.
- `build_deck_inspection_report` composes skeleton facts, structural warnings, card fact lookup coverage, and optional found-card-only role evidence.
- Deck inspection smoke fixtures are stable expected-output fixtures, not product UI.
- Role evidence remains card-level advisory metadata.
- Deck-level role counting is not implemented.
- Full deck classification is not implemented.

## Relationship Primitive Defaults

- Facts describe cards.
- Interfaces describe behavior.
- Edges describe relationships.
- Subgraphs may later describe packages.
- Context may later describe relevance.
- Judgment comes last.

Current relationship primitives are planning vocabulary only:

- `supplies`
- `triggers`
- `enables`
- `amplifies`
- `protects`
- `recurs`
- `conflicts_with`

Deferred relationship concepts remain out of v0:

- `redundant_with`
- `competes_with`
- `converts`
- `closes_with`

## Parsed Next Steps

Recommended next implementation order:

1. Typed Card Relationship Primitive Models v0: load and validate the existing JSON vocabulary fixture as typed local objects. Do not derive edges yet.
2. Card Behavioral Profile Model v0: define a factual profile shape for outputs, costs, requirements, events, permissions, modifiers, zone constraints, and timing constraints. Do not extract behavior yet.
3. Bounded Behavior Atom Extraction v0: extract only explicit low-risk atoms from local card facts and Oracle text. Do not infer strategy or quality.
4. Relationship Edge Derivation v0: derive edges only between compatible behavior groups with traceable evidence. Do not compare every card against every other card.
5. Card Relationship Report v0: expose relationship evidence with summary, machine evidence, optional explanations, and debug details.
6. Deck Role Summary v0: start only after explicit human approval for deck-level role counting.

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

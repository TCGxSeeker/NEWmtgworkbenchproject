# Next Session Handoff

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
- Card Role Evidence Pipeline v0
- Deck Skeleton Report v0

## Current Branch

- `card-role-evidence-pipeline-v0`

## Current Test Status

- `python -m unittest discover -s tests`
- Latest known result: 148 tests passing
- `git diff --check` passing

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

## UI Visibility Doctrine

Not all internal algorithm data should become visible UI text.

Future UI should use progressive disclosure:

1. Default UI: short human-readable summaries.
2. Expanded UI: concise why-this-was-flagged explanations.
3. Advanced/debug UI: raw rule evidence, confidence scores, matched phrases, and internal data.

Future output schemas should separate machine-readable evidence, concise user-facing summaries, optional explanation text, and debug/internal details.

## Next Recommended Slice

Structural Warnings v0, limited to mechanical warnings that consume Deck Skeleton Report v0 facts.

## Established Role Evidence Defaults

- Role rules load from the tiny YAML fixture format.
- Evidence phrase matching uses casefolded substring matching with whitespace normalization.
- Score combination uses `highest_match` only.
- Role evidence matching works from explicit `CardRoleFacts`.
- `card_record_to_role_facts` converts local/Scryfall-ish records into `CardRoleFacts`.
- `card_record_to_role_evidence_report` converts one local/Scryfall-ish record into a card-level `RoleEvidenceReport`.
- `card_records_to_role_evidence_reports` returns a tuple of card-level reports in input order.
- Role evidence reports separate user summaries, machine evidence, explanations, and optional debug details.
- `build_deck_skeleton_report` inventories deck metadata, zones, quantities, commander names, active categories, unresolved entries, missing local facts, and known non-basic duplicates.
- Additive capped scoring is not implemented.
- Deck-level role counting is not implemented.
- Full deck classification is not implemented.
- Do not implement deck analysis, recommendations, UI, candidate search, or role enforcement yet.

## Structural Warning Defaults

- Warnings should be mechanical only.
- No strategic quality judgments.
- No deck-level role counting yet.
- No guessing when card facts are unavailable.
- Missing facts should be surfaced as missing data, not inferred.

## Do Not Start Yet

- Full deck analysis.
- Recommendations.
- Candidate search.
- Add/cut scoring.
- App UI.
- Frontend dependencies.
- Online services or live API calls.
- Full Scryfall auto-categorization.
- Primary-role enforcement.

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

## Current Test Status

- `python -m unittest discover -s tests`
- Latest known result: 98 tests passing
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

Role Rules Loader v0.

## Role Rules Loader V0 Defaults

- Support only the tiny YAML subset first.
- Use casefolded substring phrase matching with whitespace normalization.
- Use `highest_match` score combination only.
- Do not implement additive capped scoring yet.
- Do not classify cards yet.
- Do not implement deck analysis, recommendations, UI, candidate search, or role enforcement yet.

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

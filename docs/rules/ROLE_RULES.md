# Role Rules

## Purpose

Role Rules v0 defines the first local/offline rules format for detecting what a card can do from local card data and Oracle text evidence.

Role rules support future deterministic deck analysis. They do not implement analysis, recommendations, candidate search, add/cut scoring, or primary-role enforcement.

## Category Taxonomy vs Role Rules

Category taxonomy normalizes labels such as imported headers or user categories. It preserves what a user or source called a card group.

Role rules evaluate evidence from card data. They describe why a card may count as ramp, draw, removal, protection, or another role in a deck context.

Generic category is a hint. Deck-specific role is the truth. User/imported labels must remain preserved even when role evidence disagrees.

## YAML Schema

Role rules use YAML so rules remain local, readable, editable, and diffable.

Top-level fields:

- `schema_version`: rules format version.
- `source`: short fixture or ruleset id.
- `description`: human-readable ruleset summary.
- `evidence_score_bands`: score scale documentation.
- `ui_visibility`: output visibility doctrine for future UI/report schemas.
- `roles`: list of role definitions.

Each role should support:

- `role_id`: stable machine id.
- `canonical_role`: display role name.
- `description`: role definition.
- `evidence_rules`: deterministic matching rules.
- `exclusion_rules`: reasons a matching card should not count.
- `score_policy`: how matching evidence becomes a 0-100 score.
- `explanation_template`: concise explanation text.
- `user_summary_template`: short UI/report summary.

Evidence rules may include:

- `oracle_text_phrases`: exact or normalized phrase matches against Oracle text.
- `type_matches`: card type, supertype, or type-line matches.
- `subtype_matches`: subtype matches.
- `keyword_matches`: keyword matches when local card data exposes them.
- `mana_value`: optional comparison constraints.

## Evidence Scoring

Use deterministic 0-100 evidence score bands:

- `0`: no evidence.
- `25`: weak hint.
- `50`: plausible role.
- `75`: strong role.
- `100`: exact/direct role evidence.

Scores are evidence confidence, not deckbuilding approval. Missing data should lower confidence or produce a missing-data note; it should not be guessed.

## Explanation Output

Role evidence should be explainable with:

- Matched rule id.
- Matched field.
- Matched phrase/type/subtype/keyword.
- Evidence score.
- Exclusion reason when excluded.
- User-facing summary.
- Optional detailed explanation.

Rules should be reproducible: the same local card facts and same ruleset should produce the same evidence.

## Imported/User Categories

Imported and user categories remain preserved in deck entries. Role rules may use them as hints only when explicitly allowed by a future analyzer.

Role rules must not overwrite:

- `categories`
- `imported_category`
- `normalized_category`
- `generic_category_hint`
- `deck_specific_primary_role`
- `secondary_tags`
- `category_origin`

## Deck-Specific Role Selection

Role Rules v0 may produce possible role evidence. It does not choose the one primary deck-specific role that counts for shell totals.

Primary role selection is deferred until a future role classification slice can evaluate commander thesis, package context, user intent, and human validation flags.

## UI Visibility Doctrine

Not all algorithm data should become visible UI text.

The deterministic algorithm may produce internal evidence, scores, role matches, rule hits, warnings, and explanations. Future UI should present this through progressive disclosure:

1. Default UI: short human-readable summaries.
2. Expanded UI: concise why-this-was-flagged explanations.
3. Advanced/debug UI: raw rule evidence, confidence scores, matched phrases, and internal data.

Future output schemas should separate:

- Machine-readable evidence.
- Concise user-facing summary.
- Optional explanation text.
- Debug/internal details.

The UI should avoid overwhelming users with raw algorithm text.

## Non-Goals

Role Rules v0 does not:

- Add AI/LLM behavior.
- Add live API calls.
- Add telemetry or hosted services.
- Implement recommendations.
- Implement candidate search.
- Implement add/cut scoring.
- Implement full deck analysis.
- Auto-categorize the full Scryfall database.
- Enforce primary roles.
- Solve every Magic card.
- Replace user/imported labels.

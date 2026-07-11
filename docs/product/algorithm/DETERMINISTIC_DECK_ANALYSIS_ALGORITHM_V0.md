# Deterministic Deck Analysis Algorithm V0

## 1. Purpose

Define the future local/offline rules-based algorithm for MTG Workbench deck analysis and recommendation drafting.

The algorithm must be deterministic, reproducible, explainable, and based on local evidence. It must not depend on AI/LLM calls, live APIs, telemetry, popularity metrics, or hosted services.

This is a planning document only. It does not implement deck analysis or recommendations.

## 2. Inputs

Primary inputs:

- Native `.mtgwdeck.json` workspace.
- Local card snapshot or local Scryfall-derived index.
- Category taxonomy and aliases.
- Future local role rules.
- Future commander profile.
- Future package definitions.
- Future budget and ownership profiles.
- User-set intent such as target bracket, budget posture, and protected cards.

Important evidence:

- Oracle text.
- Type line.
- Mana cost and mana value.
- Colors and color identity.
- Local legality snapshot.
- Local price snapshot when present.
- User/imported labels, preserved as hints.

## 3. Algorithm Layers

The algorithm should run in ordered layers:

1. Workspace load and shape validation.
2. Card identity resolution.
3. Mechanical validation.
4. Card feature extraction.
5. Role and category classification.
6. Deck shell audit.
7. Commander thesis matching.
8. Package detection.
9. Candidate search pool creation.
10. Add scoring.
11. Cut scoring.
12. Pairing and no-swap decision.
13. Explanation packet generation.

Each layer should emit structured evidence, warnings, and missing-data notes for later reporting.

## 4. Mechanical Validation

Mechanical validation runs before quality judgments.

Checks should include:

- Commander, mainboard, and maybeboard separation.
- Card count by zone.
- Quantity preservation.
- Unknown or unresolved entries.
- Duplicate non-basic detection.
- Basic land handling.
- Color identity containment.
- Local legality when local legality data exists.
- Missing local card facts.
- Maybeboard exclusion from active deck totals.

Mechanical failures should block confidence-heavy claims but should not erase user data.

## 5. Card Feature Extraction

Feature extraction converts local card data into stable facts:

- Mana value.
- Mana cost pips by color.
- Color and color identity.
- Type, supertype, subtype, and card type groups.
- Oracle text tokens and phrase matches.
- Keyword actions and evergreen keywords where detectable.
- Produces mana, draws cards, tutors, removes, counters, protects, recurs, wipes, creates tokens, or wins.
- Commander eligibility when locally knowable.
- Local price and owned status when present.

Extraction should store evidence references such as source field, matched phrase, and local rule id.

Card Facts Adapter v0 bridges local or Scryfall-ish record dictionaries into `CardRoleFacts` for role evidence matching. It does not perform deck analysis or primary-role selection.

## 6. Role/Category Classification

Generic category is a hint. Deck-specific role is the truth.

Classification should combine:

- User/imported category labels.
- Normalized category metadata.
- Oracle text and type evidence.
- Future local role rules.
- Commander profile needs.
- Package context.

Each role assignment should include:

- Role name.
- Primary or secondary status.
- Confidence.
- Evidence.
- Reason it counts.
- Reason it may not count.
- Human-review flag when ambiguous.

The algorithm should avoid double-counting by allowing one primary counted role per card for shell totals, with secondary roles kept as explanatory tags.

## 7. Shell Audit

Shell audit compares the active deck against local target bands.

Initial shell dimensions:

- Land count.
- Ramp count.
- Draw/card advantage count.
- Interaction count.
- Removal count.
- Board wipe count.
- Protection count.
- Recursion count.
- Engine count.
- Payoff count.
- Win condition count.
- Mana curve.
- Color source and color pip pressure.

Targets should be local rules, not universal truths. Reports must show the target source and whether data was missing or uncertain.

## 8. Commander Thesis Matching

Commander thesis matching asks whether the deck supports the declared commander plan.

Inputs may include:

- Commander profile.
- Deck notes.
- Tags.
- Protected cards.
- Intended bracket or power target.
- User-declared avoid patterns.

The algorithm should compare roles and packages against the commander thesis, then report alignment, gaps, and conflicts. It must not choose a commander philosophy or archetype pivot without human approval.

## 9. Package Detection

Package detection identifies local, named groups of cards or effects.

Package outputs should include:

- Package id and name.
- Detected pieces.
- Missing pieces.
- Protected glue.
- Payoffs.
- Risks.
- Human validation requirement for combo or archetype-impacting changes.

This is not a full combo solver. Detection should use curated local package definitions and clear evidence.

## 10. Candidate Search

Candidate search creates local candidate pools for possible additions.

Sources:

- Local card index.
- Local syntax search.
- Local role rules.
- Commander color identity.
- Budget and ownership constraints.
- Format legality snapshot when available.
- User exclusions and protected cards.

Search should narrow candidates by deterministic filters before scoring. It should not call live services or use popularity rankings.

## 11. Add Scoring

Add scoring estimates why a card could help.

Possible score components:

- Fills missing primary role.
- Supports commander thesis.
- Completes or strengthens a package.
- Improves curve.
- Improves color requirements.
- Improves interaction density.
- Respects budget and ownership mode.
- Avoids protected strategy conflicts.
- Has local evidence for claimed function.

Every score must be decomposable into named components. Unknown data should lower confidence, not invite guessing.

## 12. Cut Scoring

Cut scoring estimates which cards are least essential.

Possible score components:

- Redundant role above target.
- Weak commander thesis alignment.
- High mana value pressure.
- Color strain.
- Package conflict.
- No local evidence for claimed role.
- User-marked flex slot.
- Unowned or over-budget card when budget mode requires it.

Protected, pinned, commander, package-glue, pet-card, and human-validation cards should receive strong cut penalties or be excluded from automatic cut pairing.

## 13. Explanation Output

Recommendation output must be explainable and reproducible.

Each recommendation draft should include:

- Proposed add, cut, or `no_swap`.
- Score components.
- Evidence lines.
- Role impact.
- Package impact.
- Budget and ownership impact.
- Curve and color impact.
- Risks and missing data.
- Human validation flags.
- Deterministic rule ids used.

`no_swap` is valid when no candidate improves the deck enough or when strategic uncertainty is too high.

## 13.1 UI Visibility Doctrine

Not all algorithm data should become visible UI text.

The deterministic algorithm may produce internal evidence, scores, role matches, rule hits, warnings, and explanations. Future UI should present this through progressive disclosure:

1. Default UI: short human-readable summaries.
2. Expanded UI: concise why-this-was-flagged explanations.
3. Advanced/debug UI: raw rule evidence, confidence scores, matched phrases, and internal data.

Future output schemas should keep separate fields for:

- Machine-readable evidence.
- Concise user-facing summary.
- Optional explanation text.
- Debug/internal details.

The UI should avoid overwhelming users with raw algorithm text.

## 14. Phase Plan

Suggested implementation sequence:

1. Deck Skeleton Report v0: counts, zones, unresolved cards, card types, mana values.
2. Structural Warnings v0: duplicates, count issues, missing commander, color identity warnings.
3. Card Feature Extraction v0: stable local facts from card data and Oracle text.
4. Role Classification v0: local rule-backed role hints with confidence.
5. Shell Audit v0: target-band comparison for core deck structure.
6. Commander Profile v0: declared thesis and avoid-pattern checks.
7. Package Detection v0: curated local packages only.
8. Recommendation Explanation v0: explanation packet format before scoring.
9. Candidate Search v0: local candidate pools using existing search infrastructure.
10. Add/Cut Scoring v0: decomposable scoring with no-swap support.

Each phase should include fixtures, expected outputs, and regression tests before broadening scope.

## 15. Non-Goals

Explicitly deferred:

- AI/LLM recommendations.
- Live API lookup.
- Popularity-based recommendations.
- Telemetry or user behavior learning.
- Full combo solver.
- Full legality judge engine.
- Full price optimizer.
- Autonomous final cuts or additions.
- Commander philosophy changes without human approval.
- UI implementation.
- Frontend dependencies.

## 16. Future Acceptance Criteria

Before implementation is considered ready:

- Analysis runs offline from local fixtures.
- Same input produces same output.
- Unknown cards remain visible.
- Missing data lowers confidence and is reported.
- Mechanical validation runs before recommendations.
- Role counts distinguish generic hints from deck-specific primary roles.
- Recommendations cite local evidence and rule ids.
- No-swap is tested.
- Protected cards are not cut automatically.
- Human validation flags appear for power claims, combo changes, expensive cards, and archetype pivots.
- Tests cover happy paths, missing data, bad imports, wrong-role cards, protected glue, and no-swap cases.

# Implementation Spec

## Goal

Build the MTG Workbench as an offline-first, deterministic Commander deckbuilding assistant. The project should import decklists, normalize cards against local data, analyze deck structure, flag issues, and produce explainable reports and recommendation drafts without depending on AI, live APIs, telemetry, or popularity metrics.

## Scope

This spec covers the intended MVP and first implementation phases. No feature code should be written until this document is reviewed and the first implementation step is approved.

The MVP should prove:

- Local decklist ingestion works.
- Card names normalize against local card data.
- Commander deck structure can be audited deterministically.
- Reports expose useful statistics, warnings, and human approval flags.
- The system functions without internet access.

## Non-Goals

- No chatbot wrapper.
- No EDHREC clone.
- No live API dependency for core analysis.
- No autonomous final deckbuilding.
- No card purchase automation.
- No production web UI before the CLI and deterministic engine are stable.
- No fresh price, legality, or newly released card claims unless backed by verified local snapshots.
- No recommendation ranking based on popularity, telemetry, repeat user behavior, or generic staple status.

## Source of Truth

Use the user interview answers and supplemental hand-off as the highest-priority product source. If repo files conflict with them, prefer the interview answers and record the conflict in `docs/codex/DECISION_LOG.md`.

Current repository inspection found only project operating files: `AGENTS.md`, `docs/codex/`, `.tasks/`, and `.agents/skills/`. There is no source code, test suite, card data, deck fixture, README, local rule file, CSV export, or prior implementation artifact yet. Missing facts should become TODOs or fixtures, not invented details.

## Key Decisions Before Building

- Proposed runtime: Python CLI, because the MVP needs local parsing, deterministic tests, simple fixtures, and portable offline behavior.
- Proposed first commands: `mtg audit` and `mtg final-check`.
- Proposed data style: YAML for editable rules, CSV for ownership lists, JSON for local card snapshots, Markdown for reports and docs.
- Scryfall usage: optional future manual bulk-data ingestion only, not runtime analysis.
- UI: future phase only, after CLI behavior and report outputs are stable.

These are proposed decisions, not irreversible implementation commitments.

## Files Likely Involved

Planning files:

- `docs/codex/PROJECT_BRIEF.md`
- `docs/codex/IMPLEMENTATION_SPEC.md`
- `docs/codex/VERIFICATION_PLAN.md`
- `docs/codex/HUMAN_VALIDATION_ZONES.md`
- `docs/codex/AUTOMATION_DECISIONS.md`
- `docs/codex/DECISION_LOG.md`
- `docs/codex/GOTCHAS.md`

Future implementation files:

```text
src/mtg_workbench/
  cli/
  cards/
  decks/
  analysis/
  recommendations/
  rules/
  reports/
  data/
  utils/
data/
  cards/
  decks/
  owned/
  commander_profiles/
  packages/
  templates/
  sources/
tests/
  fixtures/
  normalization/
  analysis/
  recommendations/
  reports/
```

## MVP User Loop

1. Import a local Commander decklist.
2. Parse quantities, commander markers, main deck, categories, lands, and maybeboard where present.
3. Normalize card names against a local card snapshot.
4. Report unknown cards instead of guessing.
5. Analyze deck structure.
6. Check color identity, quantities, duplicates, curve, land count, ramp, draw, interaction, protection, engines, payoffs, win conditions, budget, and ownership constraints where local data exists.
7. Generate an audit report.
8. Generate a final-check packet with human validation flags.
9. Capture corrections as gotchas and future regression tests.

## Domain Model

| Object | Purpose | Key Fields | Populated By | Consumed By |
| --- | --- | --- | --- | --- |
| `Card` | Local card facts | name, aliases, mana value, colors, color identity, type line, Oracle text, prices snapshot, legality snapshot | local card snapshot, overrides | normalization, analysis, reports |
| `Deck` | Imported deck state | commander, main, maybeboard, categories, source path | deck parser | all analysis passes |
| `CommanderProfile` | Commander plan and constraints | commander, gameplan, colors, key roles, forbidden pivots | local YAML profile | plan checks, recommendations |
| `DeckAnalysis` | Audit result | counts, curve, warnings, role totals, validation results | analysis passes | reports, final-check |
| `RoleTag` | Card function in context | card, role, confidence, source, notes | local rules, overrides | role counts, recommendations |
| `Package` | Synergy/combo package | name, cards, purpose, required pieces, risks | local YAML package files | package detection |
| `BudgetProfile` | Budget constraints | card cap, deck cap, exception policy | local YAML | budget checks |
| `OwnershipProfile` | Owned/on-hand data | card name, quantity, location, proxy policy | CSV/local files | ownership checks |
| `Recommendation` | Draft add/cut proposal | add, cut, reason, impacts, confidence, risks, approval flag | recommendation engine | recommendation reports |
| `ValidationResult` | Check result | check id, status, evidence, severity, human review flag | validation passes | final-check |
| `AuditReport` | User-facing output | summary, stats, warnings, checklist, draft recommendations | report generator | CLI output, future UI |

## Deterministic Analysis Passes

The engine should be built in small passes:

1. Decklist parsing.
2. Card name normalization.
3. Quantity validation.
4. Duplicate detection.
5. Commander detection.
6. Color identity validation.
7. Local legality validation if local legality data exists.
8. Mana curve and mana value distribution.
9. Mana source and color pip analysis.
10. Land, ramp, draw, interaction, protection, engine, payoff, and win-condition audits.
11. Role/category counting.
12. Package detection.
13. Commander plan detection.
14. Budget threshold checks.
15. Ownership/on-hand checks.
16. Human validation trigger checks.
17. Report generation.

## Recommendation Rules

Recommendations are drafts, not final authority. They must cite local rules, local data, or user-approved exceptions.

A recommendation should evaluate whether a candidate:

- Supports the commander plan.
- Preserves or improves an existing package.
- Fills a missing role.
- Improves speed, consistency, protection, interaction, card flow, or closing power.
- Respects budget and ownership mode.
- Avoids unnecessary staples.
- Avoids diluting the primary plan.
- Has a clear cut candidate or role reason.
- Has identifiable risks and verification notes.

## Rules-As-Data Plan

| Artifact | Format | Location |
| --- | --- | --- |
| Deckbuilding templates | YAML | `data/templates/` |
| Bracket and power assumptions | YAML/Markdown | `docs/rules/` or `data/sources/` |
| Budget thresholds | YAML | `data/sources/` |
| Role definitions | YAML | `data/sources/` |
| Package definitions | YAML | `data/packages/` |
| Recommendation weights | YAML | `data/sources/` |
| Human validation triggers | YAML | `data/sources/` |
| Card tagging overrides | YAML or CSV | `data/cards/` |
| Commander profiles | YAML | `data/commander_profiles/` |
| Ownership/on-hand lists | CSV | `data/owned/` |
| Report templates | Markdown | `docs/reports/` |

## Implementation Steps

### Phase 0: Planning Baseline

Finish and review planning docs. Definition of done: docs agree on offline-first behavior, human validation zones, no feature code exists, and open questions are visible.

### Phase 1: Local Data Contracts And Fixtures

Create minimal local fixtures and schemas for cards, decklists, ownership, commander profiles, packages, and templates. Definition of done: fixtures load locally, invalid fixtures fail cleanly, no internet access is required.

### Phase 2: Decklist Parser And Normalizer

Implement import parsing and card-name normalization. Definition of done: sample decklists parse correctly, quantities are preserved, commanders are detected when marked, and unknown cards are reported rather than guessed.

### Phase 3: Structural Audit Engine

Implement `DeckAnalysis` and deterministic audit passes for curve, colors, card types, lands, ramp, draw, interaction, protection, engines, payoffs, and win conditions. Definition of done: known fixture decks produce expected stable counts.

### Phase 4: Final-Check Report

Generate a review packet with validation results, unresolved risks, and human approval flags. Definition of done: reports include mechanical checks and never claim final strategic approval automatically.

### Phase 5: Recommendation Draft Engine

Generate ranked draft recommendations from local logic only. Definition of done: every recommendation includes reason, role impact, package impact, budget/ownership impact where relevant, risks, confidence, and approval requirements.

### Phase 6: Optional UI Planning

Only after CLI behavior is stable, design the luxury workbench UI. Definition of done: UI plan preserves deterministic CLI behavior and prevents copy overflow.

## Verification Plan

Before coding, update `docs/codex/VERIFICATION_PLAN.md` with exact commands once stack and CLI shape are approved.

Future verification should include:

- Unit tests.
- Fixture decklists.
- Known-good audit outputs.
- Regression tests for gotchas.
- Card normalization tests.
- Decklist parser tests.
- Role count tests.
- Package detection tests.
- Budget and ownership rule tests.
- Recommendation scoring tests.
- Final-check report tests.
- Manual human review checklist.

Verification must not require internet access.

## Human Validation Zones

Require explicit approval before implementing or changing:

- Stack/runtime selection if not using the proposed Python CLI.
- Scoring rubric or Commander bracket mapping.
- Recommendation weights or card evaluation rules.
- Commander identity, final cuts/additions, combo packages, archetype pivots, and power-level claims.
- Scryfall ingestion behavior.
- Source-of-truth data overwrites or local data deletion.
- Paid services, account login, secrets, or external integrations.
- UI tone, brand direction, or user-facing copy.

## Risks

- No local card data or deck fixtures exist yet.
- Scoring rubric and Commander bracket mapping are not defined yet.
- Role taxonomy and package definitions are still conceptual.
- Recommendations may feel weak until local rules, overrides, and examples mature.
- Local snapshots can become stale if update workflow is not designed carefully.
- A future UI could drift into generic text or overflow if not validated with real content.

## Definition Of Done For This Spec

- Goal is stated.
- Scope and non-goals are stated.
- Files likely affected are listed.
- MVP user loop is defined.
- Domain model is defined.
- Implementation phases are sequenced.
- Verification approach is stated.
- Human validation zones are stated.
- Risks and open questions are stated.
- No feature code is created.

## Open Questions

### Blocking Before Feature Code

- Do you approve Python as the default CLI runtime?
- Can we create the first local card fixture format in Phase 1?
- Can we create or use one sample Commander decklist fixture in Phase 1?

### Non-Blocking

- Exact scoring rubric and Commander bracket mapping.
- Initial role taxonomy.
- Initial package definition format.
- Budget threshold defaults.
- Owned/on-hand CSV format.

### Future Design

- Whether account login ever matters.
- Whether optional Scryfall bulk updates should be monthly, manually triggered, or both.
- Whether the eventual UI should be desktop, web, or another portable shell.

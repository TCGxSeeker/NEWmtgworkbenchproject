# Data Contracts

## Purpose

Define the local, offline formats MTG Workbench will use before parser, analyzer, recommender, or UI code exists. These contracts are derived from `docs/sources/MTG_PROJECT_MASTER_SEED.md`.

Do not treat seed docs as card data. Do not extract card names or decklists from doctrine files. Phase 1 fixtures are intentionally tiny and generic.

## Format Decisions

| Contract | Format | Raw Fixture | Future Processed Location |
| --- | --- | --- | --- |
| Card data | JSON | `data/raw/cards/sample_card_data_seed.json` | `data/cards/` |
| Decklists | TXT and CSV | `data/raw/decklists/` | `data/decks/` |
| Owned/on-hand cards | CSV | `data/raw/owned/sample_owned_cards.csv` | `data/owned/` |
| Commander profiles | YAML, with Markdown notes allowed | `data/raw/commander_profiles/` | `data/commander_profiles/` |
| Role definitions | YAML | `data/raw/roles/sample_role_definitions.yaml` | `data/sources/` |
| Package definitions | YAML | `data/raw/packages/sample_package_definition.yaml` | `data/packages/` |
| Deckbuilding templates | YAML | `data/raw/templates/sample_deckbuilding_template.yaml` | `data/templates/` |
| Budget profiles | YAML | `data/raw/budget/sample_budget_profile.yaml` | `data/sources/` |
| Human validation triggers | YAML | `data/raw/validation/sample_human_validation_triggers.yaml` | `data/sources/` |
| Audit report output | JSON plus future Markdown rendering | `data/raw/reports/sample_audit_report.json` | `docs/reports/` |
| Recommendation report output | JSON plus future Markdown rendering | `data/raw/reports/sample_recommendation_report.json` | `docs/reports/` |
| Generic regression tests | YAML | `data/raw/regression_tests/sample_generic_regression_tests.yaml` | `tests/fixtures/` |

## Contract Requirements

### Card Data

Must include stable local facts: canonical name, aliases, mana value, colors, color identity, type line, Oracle text, legality snapshot, price snapshot, and source metadata. Unknown cards must be reported instead of guessed.

### Decklists

Must preserve quantity, section, card name, category if present, and notes if present. Commander and maybeboard sections must remain distinct from the main deck.

### Owned/On-Hand Cards

Must preserve card name, quantity, location, condition, and notes. Ownership checks must not imply purchase advice.

### Commander Profiles

Must describe the commander billboard: commander name, color identity, function type, conversion, required materials, implied packages, avoid patterns, win routes, deck thesis, and human-review notes.

### Role Definitions

Must separate broad role from specific seat. A role must define when it counts, when it does not count, required evidence, and related human-review concerns.

### Package Definitions

Must describe package purpose, required materials, protected glue, payoff types, warning signs, and cut restrictions.

### Deckbuilding Templates

Must describe target shell counts and warnings. Templates are comparison guides, not automatic deck approval.

### Budget Profiles

Must define budget mode, card cap, deck cap, ownership policy, proxy policy, exception process, and pricing-source requirements.

### Human Validation Triggers

Must identify conditions that require explicit user review before proceeding.

### Audit Report Output

Must show commander billboard, deck thesis, structural audit, package map, protected glue, warnings, human validation zones, and final status. Reports must not automatically mark a deck approved.

### Recommendation Report Output

Must show source card if replacing, candidate card, intent, reason, role impact, package impact, budget impact, ownership impact, confidence, risks, verification notes, and approval requirement. `no_swap` is a valid outcome.

### Generic Regression Tests

Must start without real card names. Tests should capture behavior categories such as wrong-seat replacement, structural repair before swap, package glue protection, no-swap, fake turbo, high-land shell, branch detection, and budget compression.

## Validation Rules

- All machine-readable fixtures must be local files.
- Verification must not require internet access.
- Missing data must be explicit.
- Source-of-truth overwrites require human approval.
- Doctrine files are not parser inputs.
- Recommendation logic must cite local evidence.
- Human validation flags must survive report generation.

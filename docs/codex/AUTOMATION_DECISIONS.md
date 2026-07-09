# Automation Decisions

## Core Policy

Automate mechanical work. Augment strategic judgment. Do not fully automate final authority.

## Fully Automatable After Rules Exist

- Decklist parsing and ingestion.
- Card name normalization.
- CSV parsing.
- Local data loading.
- Category and role counting.
- Mana curve and mana value reports.
- Color identity checks.
- Duplicate detection.
- Missing-card detection.
- Budget threshold flagging.
- Ownership/on-hand checks.
- Land, ramp, draw, interaction, protection, engine, payoff, and win-condition ratio checks.
- Local template comparisons.
- Draft recommendation generation.
- Changelog creation.
- Report generation.
- Validation checklist generation.

## Assist Only

Require human approval before finalizing:

- Final deck identity decisions.
- Commander philosophy.
- Choice between multiple valid build directions.
- Final card cuts or additions.
- Power-level judgment.
- cEDH versus budget-competitive classification.
- Meta-specific calls.
- Fun-factor decisions.
- Expensive card exceptions.
- Combo package inclusion or removal.
- Archetype pivots.

## Automation Test

Before automating, ask:

1. Does the task require taste, judgment, or subjective quality? If yes, augment instead of fully automating.
2. Would an 80% correct output be acceptable? If no, augment with human review.
3. What is the cost of failure? If high, require human sign-off.

Favor augmentation over automation unless the workflow is low-risk, repeatable, and objectively verifiable.

## External Data Automation

No live API call is part of core MVP logic. Optional future Scryfall bulk updates may be implemented only as manually triggered import workflows into local files, with rate limits and clear user approval.

## Decision Record

- 2026-07-08: Initial policy created. Automation must stay local to this repository unless the user explicitly approves a broader scope.
- 2026-07-09: Offline-first MVP policy accepted from the hand-off. Core logic must run from local data and deterministic rules. External data refreshes are optional future ingestion workflows, not base dependencies.

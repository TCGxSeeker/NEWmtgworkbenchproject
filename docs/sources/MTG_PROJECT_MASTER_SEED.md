# MTG Workbench + Intense Deckbuilding Master Seed

## Purpose

This is a single Markdown handoff file for Codex to read before Phase 1 local data contracts.

It combines:

1. **Steps / usage instructions**
2. **Workbench seed data**
3. **Intense deckbuilding seed data**

This file should teach Codex the shape of the project without asking it to parse specific decklists or card names yet.

Codex should use this as doctrine, not as card data.

---

# Part 0 — Steps for Codex

## Step 1 — Read this file first

Codex should read this entire file before creating local data contracts, fixtures, schemas, parser logic, recommendation logic, or UI.

This file is source-seed material for the MTG Workbench project.

It is not a decklist.
It is not card data.
It is not a card-name extraction target.
It is not a popularity/recommendation dataset.
It is not a live API plan.

## Step 2 — Preserve the architecture constraints

The MVP must be:

- offline-first
- deterministic
- local-file based
- testable without internet
- independent of live APIs
- independent of popularity metrics
- independent of repeat-user behavior tracking
- independent of telemetry

The core program must work from:

- local rules
- local configs
- local card snapshots
- local decklists
- local ownership lists
- local fixtures
- local validation checks
- deterministic code paths

External APIs may be considered later only as optional, manually triggered import workflows.

## Step 3 — Do not parse card names or decklists from this file yet

This document contains doctrine extracted from long MTG project conversations.

Codex should not:

- extract specific card names from this file
- parse embedded decklists from this file
- create card-specific recommendations from this file
- create card-name-specific tests from this file
- infer a complete card database from this file
- assume any raw decklist inside the source text is ready to become structured data

Card-specific logic comes later after local card data contracts exist.

## Step 4 — Extract reusable doctrine only

Codex should extract:

- project philosophy
- deckbuilding rules
- commander billboard structure
- card seat structure
- package map structure
- structural audit requirements
- recommendation flow
- no-swap doctrine
- budget-compression rules
- branch-detection rules
- human validation zones
- generic regression test categories
- local data contract needs

## Step 5 — Create or update docs, not feature code

After reading this file, Codex should create or update planning docs such as:

- `docs/codex/IMPLEMENTATION_SPEC.md`
- `docs/codex/VERIFICATION_PLAN.md`
- `docs/codex/DECISION_LOG.md`
- `docs/codex/GOTCHAS.md`
- `docs/rules/DATA_CONTRACTS.md`

Codex may also create tiny local fixtures if explicitly asked during Phase 1.

Codex should not implement parser, analyzer, recommender, UI, or deployment logic yet.

## Step 6 — Use this file to inform Phase 1

Phase 1 should define local data contracts and tiny fixtures for:

1. Card data
2. Decklists
3. Owned/on-hand cards
4. Commander profiles
5. Role definitions
6. Package definitions
7. Deckbuilding templates
8. Budget profiles
9. Human validation triggers
10. Audit report output
11. Recommendation report output
12. Generic regression tests

## Step 7 — Stop after Phase 1 planning artifacts

After producing Phase 1 docs and fixtures, Codex should stop and summarize:

1. Files created or updated
2. Data formats chosen
3. Example fixtures created
4. Validation rules proposed
5. What Phase 2 should build next
6. Any questions that block Phase 2

---

# Part 1 — Recommended File Placement

Save this file as:

```text
docs/sources/MTG_PROJECT_MASTER_SEED.md
```

Optional companion filenames:

```text
docs/sources/MTG_WORKBENCH_BUILD_PHILOSOPHY_SEED.md
docs/sources/MTG_INTENSE_DECKBUILDING_SEED.md
```

If using this one master file, Codex should not require the two companion files.

---

# Part 2 — Suggested Git Commands

After saving this file:

```powershell
git add .
git commit -m "Add MTG project master seed"
```

Then begin Phase 1 with Codex.

---

# Part 3 — Codex Prompt to Process This File

Paste this into Codex after saving this Markdown file:

```text
Read docs/sources/MTG_PROJECT_MASTER_SEED.md.

Use it as source-seed material for the MTG Workbench project.

Do not parse card names yet.
Do not parse decklists yet.
Do not create card-specific recommendations yet.
Do not implement feature code yet.
Do not add API calls.
Do not add external dependencies.
Do not create a web UI.

Extract doctrine, rules, schemas, report requirements, validation gates, and generic regression test categories.

Then begin Phase 1: local data contracts and tiny fixtures.

Create or update:

- docs/codex/IMPLEMENTATION_SPEC.md
- docs/codex/VERIFICATION_PLAN.md
- docs/codex/DECISION_LOG.md
- docs/codex/GOTCHAS.md
- docs/rules/DATA_CONTRACTS.md

Define local offline formats for:

1. Card data
2. Decklists
3. Owned/on-hand cards
4. Commander profiles
5. Role definitions
6. Package definitions
7. Deckbuilding templates
8. Budget profiles
9. Human validation triggers
10. Audit report output
11. Recommendation report output
12. Generic regression tests

Create tiny example fixtures only if useful.

Stop after docs and fixtures.

Final response should summarize:

1. Files created or updated
2. Data formats chosen
3. Example fixtures created
4. Validation rules proposed
5. What Phase 2 should build next
6. Any blocking questions
```

---

# Part 4 — Workbench Seed Data

## Workbench Seed Purpose

This section defines what the MTG Workbench project is supposed to become.

It is the app/system philosophy layer.

It should inform architecture, docs, workflows, skills, data contracts, reports, tests, and validation gates.

It should not be treated as card data.

## Project Identity

The MTG Workbench is a local, deterministic Commander deckbuilding workbench.

It is intended to become an offline “Jarvis of MTG” style assistant where deckbuilding philosophy, rules, templates, analysis methods, gotchas, and validation gates are encoded into local files and program logic.

The goal is not to recreate a literal model brain.

The goal is to transplant the reusable reasoning structure into the repository as durable artifacts:

- source-of-truth docs
- editable project rules
- local data structures
- deterministic analysis passes
- recommendation logic
- validation gates
- human approval zones
- regression tests
- example fixtures
- reusable Codex skills
- gotcha capture loops
- report templates

## What This Project Is Not

This project is not:

- a generic MTG deckbuilder
- a generic deck optimizer
- an EDHREC clone
- a popularity-based recommender
- a chatbot wrapper
- an API-dependent deckbuilding tool
- a telemetry-driven learning system
- an autonomous final decklist generator

## Offline-First Constraint

The MVP must be offline-first.

The base program must not depend on:

- popularity metrics
- repeat user behavior
- telemetry
- live API calls
- cloud services
- internet access
- external recommendation engines

The base program should operate from:

- local files
- local card data
- local rules
- local configs
- local decklists
- local ownership lists
- local test fixtures
- deterministic coded logic paths

External APIs, live lookups, and external data refreshes may be considered later only as optional, manually triggered import workflows.

They are not part of the core architecture and must not be required for the MVP.

## Core User Loop

The intended user loop:

1. Import a decklist.
2. Normalize card names.
3. Parse quantities, commanders, main deck cards, lands, and categories if present.
4. Analyze structure.
5. Identify the commander plan.
6. Classify cards by actual function in this specific deck.
7. Detect packages.
8. Audit ramp, draw, interaction, protection, engines, payoffs, lands, win conditions, and flex slots.
9. Check budget constraints.
10. Check ownership/on-hand constraints.
11. Compare the deck against local templates and rules.
12. Identify missing roles or overfilled roles.
13. Generate ranked recommendation drafts.
14. Explain add/cut reasoning.
15. Produce a final review packet.
16. Require human approval for major strategic or subjective decisions.
17. Capture corrections as gotchas for future regression tests and skill updates.

## Core Architecture Direction

The long-term architecture should be layered:

1. Local card database
2. Deck parser
3. Local rules engine
4. Commander billboard builder
5. Card seat analyzer
6. Structural audit engine
7. Package detection engine
8. Recommendation scorer
9. Explanation generator
10. Optional local/AI language layer later

The LLM must not be the whole brain.

The core intelligence should live in:

- local rules
- schemas
- templates
- package definitions
- commander profiles
- seat reasons
- thresholds
- failure cases
- regression tests
- gotchas
- report formats

The optional AI layer should act as a voice, summarizer, and flexible interpreter on top of a deterministic spine.

## Prototype v1 Lesson

If an older MTG Workbench prototype exists, do not treat it as the final product.

Treat it as:

- a spec mine
- a failure map
- a source of working pieces
- a source of UI lessons
- a source of bad recommendation examples
- a source of regression tests

Known v1 value:

- deck import/parsing progress
- local offline card cache usage
- audit math
- package detection attempts
- recommendation UI scaffolding
- examples of recommender failure modes

Known v1 weakness:

- compares source and candidate cards too directly
- does not prioritize structural audit first
- does not build a commander billboard first
- does not always explain the source card’s seat
- does not always explain the candidate card’s seat
- does not do enough same-seat delta scoring
- does not protect package glue reliably
- forces weak swaps instead of allowing no-swap
- may surface math without surfacing strategic structure visually

Preferred v2 target:

```text
Commander Billboard → Structural Audit → Card Seat Reasoning → Recommendation Explanation
```

## Core Project Philosophy

A strong deck is not a pile of good cards.

A strong deck is one commander-specific move practiced until the cheap cards start looking unfair.

The system should prioritize:

1. Deck identity before generic staples.
2. Commander text before broad archetype assumptions.
3. Actual function before card fame.
4. Package fit before isolated card quality.
5. Structural health before card-level swaps.
6. Seat reasoning before candidate recommendation.
7. Repeatable engine behavior before cool payoff cards.
8. Compact win routes before scattered value.
9. Budget function translation before exact card replacement.
10. Human approval before subjective final decisions.

## Transferable Brain Doctrine

The thing to transfer is not the model.

The thing to transfer is the accumulated MTG reasoning system.

The more decisions are turned into:

- rules
- schemas
- examples
- tests
- thresholds
- seat reasons
- known bad outputs
- gotchas

the less fragile the system becomes.

This is how the project survives model updates, tool changes, and vibe drift.

## Suggested Portable Brain Folder

Eventually create:

```text
mtg_jarvis_brain/
  commander_billboard_rules.md
  card_seat_reasoning.md
  role_subtypes.yaml
  package_definitions.yaml
  protected_anchor_rules.yaml
  structural_audit_rules.yaml
  recommendation_scoring.yaml
  budget_competitive_rules.md
  branch_detection_rules.md
  high_land_shell_rules.md
  failure_cases.json
  regression_tests.json
  report_templates/
  example_decks/
  style_guide.md
```

This folder is the portable operating doctrine.

## Workbench Report Doctrine

The audit screen should not only show math.

It should surface structural interpretation.

Reports should show:

- commander billboard
- deck thesis
- structural audit
- role counts
- package map
- protected glue
- seat map
- warning categories
- recommendation intent
- no-swap results
- human validation zones
- final review checklist

A report that calculates counts but does not explain deck structure is incomplete.

## Workbench Human Validation Zones

The system must require human approval before:

- finalizing a 100-card decklist
- changing commander identity
- changing the deck’s primary archetype
- adding or removing combo packages
- making expensive card exceptions
- claiming competitive viability
- assigning final power level
- approving purchase recommendations
- publishing decklists
- overwriting source-of-truth datasets
- deleting local data
- modifying project rules
- modifying recommendation weights
- modifying validation gates

## Workbench Gotchas

General gotchas:

- Do not turn every deck into generic staples.
- Do not ignore deck identity.
- Do not recommend cards without explaining what they replace or improve.
- Do not confuse card category with card purpose in this specific deck.
- Do not claim competitive viability without evidence.
- Do not count emotionally adjacent cards as fulfilling a role unless they actually do the job.
- Do not overwrite source data without approval.
- Do not fully automate subjective final calls.
- Do not require internet access for base analysis.
- Do not use popularity as a proxy for card quality.
- Do not rank cards by repeat user behavior.
- Do not build telemetry or usage-history scoring into the base system.
- Do not require external APIs for core analysis.
- Do not assume live services are available.
- If external data is useful later, treat it as optional manual ingestion into local files.
- Do not make card-level swaps before structural audit.
- Do not treat card similarity as deck improvement.
- Do not let local corpus overlap override seat reasoning.
- Do not cut package glue just because it looks weak alone.
- Do not average different branches into an incoherent hybrid.
- Do not copy turbo land counts into budget decks without turbo mana.
- Do not add backup engines if they make the main engine slower.
- Do not force a recommendation when no-swap is correct.

---

# Part 5 — Intense Deckbuilding Seed Data

## Intense Deckbuilding Seed Purpose

This section defines how the MTG Workbench should think about decks.

This is not card data.
This is not a decklist.
This is not a recommendation output.
This is not a popularity model.
This is not a source for parsing individual card names.

Use this section to teach Codex how the project thinks about Commander deck construction, budget-competitive conversion, role assignment, card seats, packages, cuts, swaps, structural audits, and final review.

Do not extract specific card names from this section yet.
Do not parse decklists from this section yet.
Do not build card-specific logic from this section yet.

This section exists to define the reasoning shape.

## Core Doctrine

A Commander deck is not a pile of good cards.

A Commander deck is one practiced move, supported by redundant materials, protected by the right interaction, and pointed toward a real win.

The default question is not:

```text
What cards are good?
```

The correct question is:

```text
What is the deck trying to do repeatedly, and which cards make that move happen?
```

## Prime Directive

Build around the commander’s conversion.

Every serious deck must answer:

1. What does the commander convert?
2. What resource does the commander create?
3. What resource does the commander consume?
4. What material must exist before the commander matters?
5. What material becomes better because of the commander?
6. What does the deck do if the commander is removed?
7. How does the deck actually close the game?
8. Which cards are engine pieces?
9. Which cards are package glue?
10. Which cards are generic filler pretending to be synergy?

## Deckbuilding Philosophy

The project should prefer:

- commander-specific engines over generic value
- role compression over raw card quality
- compact win routes over scattered payoffs
- package-aware cuts over category-based cuts
- actual card function over broad card type
- budget function translation over expensive card imitation
- structural repair before optimization
- no-swap over weak swaps
- human approval for subjective final calls

The project should avoid:

- generic staple soup
- popularity-based reasoning
- copying expensive lists card-for-card
- treating categories as seats
- averaging different archetype branches into one muddled list
- cutting ugly package glue before understanding its job
- lowering land count without matching acceleration
- adding backup engines that slow the primary engine
- recommending cards without explaining what they replace
- forcing a swap when the current card is already correct

## One Practiced Move

Every deck should be reduced to one practiced move.

Examples of practiced move shapes:

```text
cheap enablers -> commander trigger -> resource snowball -> compact payoff
```

```text
cheap artifacts -> enter/die triggers -> draw/mana/damage -> recursion loop
```

```text
creatures/tokens -> commander conversion -> cards/mana -> table kill
```

```text
lands entering/sacrificing -> mana/cards/board -> recursion burst -> payoff
```

```text
spells cast/copied -> card velocity -> mana burst -> deterministic finish
```

```text
graveyard setup -> recursion engine -> repeated ETB/death value -> win outlet
```

If the deck cannot be summarized as one practiced move, it is probably unfocused.

## Deck Thesis Template

Every deck should have a thesis.

```yaml
deck_thesis:
  this_deck_wants_to:
    - establish: "[required material]"
    - convert: "[resource A] into [resource B]"
    - repeat: "[commander-enabled action]"
    - protect: "[engine, commander, package, or combo]"
    - win_through: "[primary kill route]"
    - fallback_plan: "[backup route]"
  good_when:
    - "[what opening or board state means the deck is functioning]"
  bad_when:
    - "[what failure pattern means the deck is unfocused]"
```

Good thesis shape:

```text
specific setup -> commander conversion -> repeated resource advantage -> protected finish
```

Bad thesis shape:

```text
random good cards -> maybe commander survives -> maybe value happens
```

## Commander Billboard

Before building or recommending, create a commander billboard.

```yaml
commander_billboard:
  commander_name: TODO
  color_identity: TODO
  mana_value: TODO
  commander_function_type: TODO
  primary_conversion: TODO
  secondary_conversion: TODO
  main_resource_created: TODO
  main_resource_consumed: TODO
  required_materials: []
  implied_packages: []
  payoff_types: []
  protection_needs: []
  interaction_needs: []
  deck_speed: slow | medium | fast | turbo
  commander_dependency: low | medium | high
  backup_plan_required: true
  avoid_patterns: []
  primary_win_route: TODO
  backup_win_route: TODO
```

## Commander Function Types

Use these labels when classifying commanders:

```yaml
commander_function_types:
  - card_advantage_commander
  - mana_engine_commander
  - cost_reduction_commander
  - combat_trigger_commander
  - sacrifice_engine_commander
  - graveyard_engine_commander
  - artifact_engine_commander
  - token_engine_commander
  - spell_copy_commander
  - voltron_commander
  - tribal_payoff_commander
  - blink_commander
  - aristocrats_commander
  - landfall_commander
  - theft_or_cast_from_exile_commander
  - combo_outlet_commander
  - stax_commander
  - recursion_commander
  - damage_conversion_commander
  - tap_ability_commander
  - counters_commander
  - equipment_or_aura_commander
  - topdeck_commander
  - discard_commander
```

## Conversion Types

The commander’s conversion is the heart of the deck.

```yaml
conversion_types:
  - combat_damage_to_cards
  - combat_damage_to_mana
  - combat_damage_to_treasures
  - combat_damage_to_stolen_cards
  - artifacts_entering_to_damage
  - artifacts_entering_to_cards
  - artifacts_dying_to_counters
  - artifacts_dying_to_mana
  - creatures_dying_to_drain
  - creatures_dying_to_cards
  - spells_cast_to_tokens
  - spells_cast_to_damage
  - spells_copied_to_cards
  - lands_entering_to_tokens
  - lands_entering_to_mana
  - lands_entering_to_cards
  - lands_sacrificed_to_mana
  - lands_returned_to_board_presence
  - discard_to_damage
  - discard_to_cards
  - tokens_to_mana
  - tokens_to_cards
  - graveyard_to_battlefield
  - mana_spent_to_board_presence
  - tapping_creatures_to_mana
  - board_presence_to_card_velocity
```

## Branch Detection

When multiple strong examples point in different directions, do not average them into mush.

Identify branches.

A branch is a distinct strategic version of a commander or archetype.

```yaml
branch_profile:
  branch_name: TODO
  thesis: TODO
  speed: slow | medium | fast | turbo
  commander_dependency: low | medium | high
  land_count_range: TODO
  ramp_style: TODO
  draw_style: TODO
  interaction_style: TODO
  protection_style: TODO
  key_packages: []
  win_routes: []
  budget_translation_notes: TODO
  risks: []
```

Common branch types:

```yaml
branch_types:
  - midrange_engine
  - turbo_combo
  - protected_one_card_commander_combo
  - land_combo
  - blink_combo
  - aristocrats_engine
  - graveyard_recursion
  - voltron_pressure
  - high_land_combo_shell
  - stax_control
  - go_wide_storm
  - artifact_sacrifice
  - spell_copy_combo
  - token_combo
  - counters_pressure
  - control_combo
  - value_combo
```

Branch rule:

```text
Do not combine branches unless intentionally building a hybrid.
```

A hybrid must explain:

- what each branch contributes
- which branch is primary
- which branch is secondary
- what is being cut to make room
- whether the deck becomes slower or less consistent

## BDD-Style Core Shells

These are starting shells, not laws.

### Default 2–3 Color Commander Shell

```yaml
default_commander_shell:
  commanders: 1-2
  lands: 36
  nonlands: 62-63
  ramp: 9-12
  draw_or_card_flow: 8-12
  interaction: 6-10
  protection_or_resilience: 4-8
  engine_enablers: 10-16
  payoffs_or_win_pressure: 6-10
  tutors_selection_redundancy: 3-6
  flex_meta_spice: 3-6
```

### Budget-Competitive Shell

Budget-competitive decks should reduce flex and increase redundancy.

```yaml
budget_competitive_shell:
  commanders: 1-2
  lands: 34-38
  ramp_or_mana_advantage: 8-12
  cheap_card_flow: 8-12
  interaction_and_protection_combined: 10-16
  engine_enablers: 12-18
  payoffs_or_closers: 5-8
  tutors_selection_redundancy: 3-8
  flex_spice: 0-4
```

### Turbo / cEDH-Inspired Shell

Use only when the deck has enough acceleration and velocity to justify it.

```yaml
turbo_or_cedh_inspired_shell:
  lands: 23-28
  mana_ramp_burst: 20-25
  card_advantage_selection: 6-12
  tutors: 6-12
  stack_interaction_protection: 12-22
  targeted_removal: 3-7
  deck_plan_synergy: 6-12
  dedicated_wincons: 3-10
  board_wipes: 0-1
```

Warning:

```text
Do not copy turbo land counts without turbo mana.
```

### High-Land Budget Combo Shell

Use when lands are engine material, not just mana sources.

```yaml
high_land_budget_combo_shell:
  lands: 38-42
  land_pressure_valves: 10-15
  draw_or_hand_quality: 10-14
  ramp: 8-12
  interaction_protection: 5-8
  compact_win_packages: 2-4
  remaining_slots: engine_redundancy
```

Valid pressure valves include:

```yaml
land_pressure_valves:
  - cycling_lands
  - utility_lands
  - spell_lands
  - looting
  - rummaging
  - retrace_style_effects
  - flashback_or_jumpstart_costs
  - land_recursion
  - landfall_triggers
  - commander_mana_sinks
  - land_sacrifice
  - land_return
  - graveyard_land_access
```

Bad fit warning:

```text
High-land shells are wrong when the deck needs spell density more than land density.
```

### Casual Interaction Shell

```yaml
casual_interaction_guideline:
  targeted_removal: 8-10
  board_wipes: 0-2
```

### Commander-Dependent Combo Shell

```yaml
commander_dependent_combo_shell:
  lands: 34-37
  ramp_or_mana_advantage: 8-12
  cheap_card_flow: 10-16
  protection: 8-14
  interaction: 4-8
  haste_or_activation_support_if_needed: 3-7
  combo_pieces: 4-8
  tutors_or_redundant_access: 3-8
  flex: 0-3
```

Doctrine:

```text
If the commander is the combo engine, protect the commander.
```

### Spell-Storm / Copy Shell

```yaml
spell_storm_or_copy_shell:
  lands: 32-36
  cheap_cantrips_or_velocity: 12-20
  rituals_or_burst_mana: 6-12
  protection_or_stack_interaction: 8-14
  engine_enablers: 8-14
  win_buttons: 3-7
  recursion_or_rebuy: 2-6
  flex: 0-3
```

Warning:

```text
Spell-storm shells should avoid excess lands unless many lands also function as spells.
```

### Artifact Sacrifice / Artifact Density Shell

```yaml
artifact_sacrifice_density_shell:
  lands: 34-37
  artifact_count_target: high
  cheap_artifacts: 12-22
  sacrifice_outlets: 4-8
  recursion: 4-8
  payoff_or_conversion_pieces: 6-10
  draw_or_card_flow: 8-12
  interaction: 6-10
  protection_or_resilience: 3-7
  closers: 3-6
```

Doctrine:

```text
Artifact count is structural, not decorative.
```

### Go-Wide Combat Storm Shell

```yaml
go_wide_combat_storm_shell:
  lands: 32-35
  cheap_body_makers: 12-20
  commander_enabling_spells: 10-18
  burst_mana: 5-10
  protection: 4-8
  kill_buttons: 4-8
  card_velocity: 8-14
  interaction: 2-6
```

Warning:

```text
This shell usually needs spell and body density more than extra lands.
```

### Landfall / Land Recursion Shell

```yaml
landfall_recursion_shell:
  lands: 38-42
  extra_land_drop_effects: 4-8
  land_search_or_ramp: 8-14
  land_recursion: 4-8
  landfall_payoffs: 6-12
  draw_or_card_flow: 8-12
  interaction: 5-8
  closers: 3-6
```

Doctrine:

```text
If lands are the engine, land count can be high, but flood must be weaponized.
```

## Card Seat Reasoning

A card’s seat is the exact job it performs in this deck.

A broad role is not enough.

Example broad role labels:

```yaml
broad_roles:
  - ramp
  - draw
  - removal
  - protection
  - payoff
  - engine
  - land
  - combo
  - tutor
  - recursion
```

These are not specific enough for recommendations.

The recommender must determine the specific seat.

```yaml
card_seat:
  card_name: TODO
  broad_role: TODO
  specific_seat: TODO
  package_membership: []
  why_it_is_here: TODO
  what_it_enables: []
  what_gets_worse_if_cut: []
  replaceability: core | important | flexible | cuttable
  human_review_required: true
```

## Seat Types

```yaml
seat_types:
  - commander_enabler
  - engine_starter
  - engine_payoff
  - engine_multiplier
  - resource_converter
  - mana_accelerator
  - color_fixer
  - cost_reducer
  - ritual_or_burst_mana
  - true_card_advantage
  - card_selection
  - cantrip
  - impulse_draw
  - loot
  - rummage
  - sacrifice_outlet
  - recursion_piece
  - combo_piece
  - combo_outlet
  - combat_enabler
  - evasion_enabler
  - type_enabler
  - token_maker
  - artifact_maker
  - graveyard_filler
  - protection_piece
  - stack_interaction
  - spot_removal
  - board_wipe
  - stax_or_check_piece
  - win_condition
  - backup_win_condition
  - land_fixing
  - utility_land
  - package_glue
  - flex_card
  - filler
```

## Package Map

Decks should be represented as packages.

```yaml
package_map:
  primary_package:
    name: TODO
    purpose: TODO
    required_materials: []
    protected_glue: []
    payoff_types: []
  secondary_package:
    name: TODO
    purpose: TODO
    required_materials: []
    protected_glue: []
    payoff_types: []
  support_package:
    name: TODO
    purpose: TODO
    required_materials: []
    protected_glue: []
    payoff_types: []
  backup_package:
    name: TODO
    purpose: TODO
    required_materials: []
    protected_glue: []
    payoff_types: []
  do_not_dilute_package:
    name: TODO
    reason: TODO
```

## Package Types

```yaml
package_types:
  - artifact_density
  - artifact_sacrifice
  - treasure_production
  - spell_copy
  - big_spell_payoff
  - blink_value
  - blink_combo
  - graveyard_recursion
  - creature_sacrifice
  - aristocrats_drain
  - combat_damage_triggers
  - evasive_creature_swarm
  - token_multiplication
  - counter_scaling
  - equipment_or_aura_scaling
  - tribal_typing
  - type_changing
  - landfall
  - discard_matters
  - cast_from_exile
  - topdeck_manipulation
  - cost_reduction
  - mana_untap_loops
  - etb_loops
  - death_loops
  - land_sacrifice
  - land_recursion
  - storm_lite
  - commander_tap_ability
  - commander_damage
  - compact_combo
```

## Package Glue Protection

Package glue can look weak in isolation.

Do not cut package glue unless the replacement preserves the same engine function.

A card may be package glue if it:

- enables the commander
- enables a type line
- enables a trigger
- bridges two packages
- converts a necessary resource
- provides irreplaceable redundancy
- enables the win condition
- keeps the engine functional
- looks bad only when removed from context

```yaml
package_glue_review:
  card_name: TODO
  package: TODO
  glue_function: TODO
  why_it_looks_weak: TODO
  why_it_is_structurally_important: TODO
  replacement_requirements: []
  cut_permission: protected | human_review_required | cuttable
```

## Structural Audit First

Before card-level recommendations, check whether the deck structure is broken.

Do not fine-tune while the house is on fire.

```yaml
structural_audit:
  total_cards: TODO
  commander_count: TODO
  land_count: TODO
  target_land_count: TODO
  land_delta: TODO
  ramp_count: TODO
  draw_count: TODO
  interaction_count: TODO
  protection_count: TODO
  engine_count: TODO
  payoff_count: TODO
  tutor_or_selection_count: TODO
  average_mana_value: TODO
  early_play_count: TODO
  high_mv_count: TODO
  color_requirement_warnings: []
  package_warnings: []
  structural_warnings: []
  structural_status: pass | warning | structural_repair_required
```

Structural repair triggers:

```yaml
structural_repair_triggers:
  - too_many_lands
  - too_few_lands
  - too_little_ramp
  - too_little_draw_or_card_flow
  - too_little_interaction
  - too_little_protection
  - too_many_high_mv_cards
  - too_many_tapped_lands_for_speed
  - unsupported_color_requirements
  - too_many_payoffs_without_enablers
  - too_many_enablers_without_payoffs
  - expensive_commander_without_acceleration
  - combo_package_missing_outlet
  - combo_package_missing_enabler
  - commander_plan_not_supported
  - no_real_closing_power
  - multiple_conflicting_engines
  - theme_cards_without_engine_contribution
```

If `structural_status` is `structural_repair_required`, normal card recommendations should stop.

The system should produce a structural repair plan first.

## Deckbuilding Intake Protocol

When starting from a decklist:

1. Parse deck structure.
2. Identify commander.
3. Build commander billboard.
4. Identify deck thesis.
5. Run structural audit.
6. Identify packages.
7. Identify protected glue.
8. Identify win routes.
9. Identify failure patterns.
10. Only then suggest changes.

When starting from a card pool:

1. Do not assume the card pool is a deck.
2. Identify real engine cores.
3. Identify commander candidates or commander needs.
4. Cluster cards by repeated action.
5. Find the strongest practiced move.
6. Choose commander that makes that move repeatable.
7. Prefer owned cards when possible.
8. Recommend only high-impact cheap orders.
9. Avoid turning the pool into soup.
10. Build a deck thesis before building a list.

## Card Pool Analysis Doctrine

A pile of cards is not a deck.

When analyzing a card pool, look for engines, not names.

Engine core examples:

```yaml
engine_core_patterns:
  - cheap_spells_to_draw_or_damage
  - blink_loop_to_etb_value
  - lands_entering_to_triggers
  - lands_sacrificing_to_mana_or_value
  - artifacts_entering_to_cards_or_damage
  - artifacts_dying_to_counters_or_mana
  - treasures_to_mana_or_combo
  - counters_to_pressure
  - modified_creatures_to_payoffs
  - graveyard_recursion_to_value_loop
  - creature_deaths_to_drain
  - tokens_to_mana_or_cards
```

Commander fit questions:

```yaml
commander_fit_questions:
  - does_the_commander_generate_cards_mana_or_a_win_condition
  - is_the_commander_cheap_enough_for_the_plan
  - does_the_commander_reduce_deckbuilding_burden
  - does_the_commander_turn_mediocre_cards_into_good_cards
  - does_the_commander_support_one_practiced_move
  - does_the_commander_work_with_owned_cards
  - does_the_commander_need_expensive_support_to_function
  - does_the_commander_create_a_clear_kill_route
```

Minimum-order upgrade path:

```yaml
minimum_order_upgrade_path:
  owned_core: []
  strongly_recommended_cheap_orders: []
  optional_upgrades: []
  refused_cards_or_effects: []
```

## Recommendation Doctrine

The recommender is not a card-similarity engine.

Card similarity is not deck improvement.

A card can be good for the deck and still be the wrong replacement for a specific source card.

### Recommendation Flow

```yaml
recommendation_flow:
  - build_commander_billboard
  - run_structural_audit
  - identify_deck_thesis
  - identify_source_card_seat
  - identify_source_package_membership
  - identify_candidate_card_seat
  - compare_source_and_candidate_seats
  - determine_package_impact
  - score_recommendation
  - allow_no_swap
  - require_human_approval_when_needed
```

### Recommendation Intents

```yaml
recommendation_intents:
  - same_seat_upgrade
  - structural_repair
  - package_rebuild
  - sidegrade_to_new_theme
  - role_change_with_justification
  - budget_downshift
  - owned_substitution
  - combo_redundancy
  - protection_upgrade
  - curve_reduction
  - package_glue_protection
  - no_swap
```

### Same-Seat Review

```yaml
same_seat_review:
  source_card:
    broad_role: TODO
    specific_seat: TODO
    why_it_is_in_deck: TODO
    what_it_enables: []
    weakness: TODO
  candidate_card:
    broad_role: TODO
    specific_seat: TODO
    why_it_would_be_in_deck: TODO
    what_it_enables: []
    weakness: TODO
  verdict: same-seat upgrade | sidegrade | downgrade | wrong-seat | no-swap
  reason: TODO
  human_review_required: true
```

Upgrade should improve at least two:

```yaml
upgrade_requirements:
  - lower_effective_mana_cost
  - better_commander_synergy
  - better_package_fit
  - better_floor
  - better_ceiling
  - more_role_compression
  - better_timing
  - better_recursion_compatibility
  - better_tutor_compatibility
  - better_protection
  - better_redundancy
  - better_budget_fit
  - better_ownership_fit
  - better_closing_power
  - lower_dead_card_risk
```

If not, return `no_swap`.

## No-Swap Doctrine

No-swap is valid.

Weak recommendations are worse than no recommendations.

Return `no_swap` when:

- the source card already fits its seat well
- the candidate does not preserve the package
- the candidate is generically good but contextually wrong
- the deck needs structural repair first
- the replacement weakens the practiced move
- the system lacks enough local evidence
- the change is subjective and requires human judgment

## Budget-Competitive Doctrine

Budget competitive does not mean weaker cEDH.

Budget competitive means:

```text
focused commander-enabled plan + cheap redundancy + compact win route + enough protection
```

Budget competitive decks should prioritize:

- command-zone engine
- cheap redundant enablers
- compact win route
- low dead-card count
- interaction while developing
- role compression
- one practiced move
- redundancy over expensive tutors
- card flow over premium search when needed
- budget land count appropriate to actual mana access
- fewer backup engines
- high percentage of cards that actively support the win

Budget competitive decks should avoid:

- expensive value without immediate impact
- cards only good when already winning
- high-mana theme pieces
- generic staples that do not support the engine
- cute packages requiring too many unsupported pieces
- slow draw that does not advance the plan
- backup engines that slow the main engine
- fake turbo land counts

## Budget Compression

When reducing cost:

1. Preserve the core win route.
2. Preserve the commander-enabled engine.
3. Identify architecture cards.
4. Reduce expensive tutors if redundancy/card flow can compensate.
5. Replace premium interaction with cheap narrow interaction.
6. Replace fast mana with land count, rocks, rituals, treasures, or card velocity.
7. Cut casual haymakers.
8. Cut backup engines.
9. Keep the deck’s real kill intact.
10. Prefer many cheap role-players over one expensive card in a weak 99.

### Expensive Card Function Buckets

```yaml
expensive_card_buckets:
  architecture:
    definition: "Teaches how the deck actually works."
    replacement_rule: "Preserve the function even if the exact card is unavailable."
  consistency:
    definition: "Improves access, smoothing, or setup."
    replacement_rule: "Replace with redundancy, card flow, or cheaper search."
  comfort:
    definition: "Useful armor plating or meta flexibility."
    replacement_rule: "Cut or replace first when budget is tight."
```

Architecture functions:

```yaml
architecture_functions:
  - mana_amplification
  - untap_conversion
  - commander_outlet
  - spell_recursion
  - interaction_as_combo
  - combo_bridge
  - deterministic_win_outlet
  - package_glue
  - commander_enabling_protection
```

Consistency functions:

```yaml
consistency_functions:
  - tutor
  - transmute_style_search
  - card_selection
  - cantrip
  - rummage
  - loot
  - impulse_draw
  - redundant_setup_piece
  - flexible_recursion
```

Comfort functions:

```yaml
comfort_functions:
  - generic_counterspell
  - flexible_protection
  - fog
  - meta_removal
  - broad_answer
  - comfort_interaction
  - utility_value_piece
```

## Function Maps, Not Shopping Lists

Strong lists should be used as function maps, not shopping lists.

Extract:

- what the deck is trying to do
- what resources it converts
- which functions are essential
- which packages are protected
- what expensive cards are doing
- which roles are redundant
- which roles are irreplaceable
- what budget versions must preserve

Do not blindly import specific cards.

Correct translation:

```text
premium function -> budget-accessible functional equivalent or redundancy plan
```

## Protection Doctrine

If the commander is the engine, protection is structural.

Protection may include:

```yaml
protection_types:
  - stack_interaction
  - hexproof_effect
  - bounce_protection
  - untap_protection
  - sacrifice_protection
  - recursion
  - proactive_disruption
  - silence_style_protection
  - cheap_permission
  - timing_window_creation
```

Budget decks often replace free protection with multiple cheap narrow protection pieces.

The system should evaluate protection by whether it protects the deck’s actual win attempt.

## Interaction Doctrine

Interaction should match deck speed and purpose.

Ask:

- Does this protect the combo turn?
- Does this stop opposing wins?
- Does this remove blockers?
- Does this answer hate pieces?
- Does this function while developing?
- Is this too slow for the deck?
- Does this also support a package?

Do not count all interaction equally.

## Draw and Card Flow Doctrine

Do not treat “draws a card” as automatically solving card advantage.

Card flow seats:

```yaml
card_flow_seats:
  - true_card_advantage
  - card_selection
  - rummage
  - loot
  - impulse_draw
  - cantrip
  - tutor
  - transmute_or_search
  - graveyard_setup
  - storm_velocity
  - reload
  - topdeck_access
  - commander_triggered_draw
```

Budget decks may use more card flow to compensate for fewer tutors.

Card velocity matters when a deck needs to assemble a compact route without premium search.

## Tutor Doctrine

Tutors are powerful but expensive.

When budget is compressed:

- reduce premium tutors where possible
- increase redundancy
- increase draw/card flow
- increase commander access
- use functional overlap
- preserve win condition access

A deck with fewer tutors must be more redundant and more focused.

## Mana Doctrine

Mana plan must match deck speed.

Do not set land count from vibes.

Ask:

- What is the commander’s mana value?
- Does the commander need to be cast early?
- Does the deck have premium acceleration?
- Does the deck use rituals or one-turn burst mana?
- Does the deck have cheap card selection?
- Does the deck convert lands into action?
- Does the deck require spell density?
- Does the deck have enough colored sources?
- Are tapped lands acceptable for this speed?
- Does the deck have fake turbo risk?

### Fake Turbo Warning

```text
Low land count without premium acceleration is fake turbo.
```

Fake turbo causes non-games.

Budget decks may need:

- more lands
- more cheap rocks
- more cantrips
- more rummage
- more redundancy
- more utility lands
- more land-to-action conversion

## Win Condition Doctrine

Every deck must have a real way to close.

Ask:

- How does the deck win?
- How many cards does the win require?
- Does the commander reduce required pieces?
- Does the deck have redundant access?
- Can the deck protect the win attempt?
- Does the deck kill one player or the table?
- Does the deck durdle without ending?
- Does the win route match the engine?

Compact win routes are especially important in budget-competitive shells.

## Cut Discipline

Cut generic cards before weird synergy glue.

### Cut Priority

```yaml
cut_priority:
  - off_plan_expensive_value
  - slow_generic_draw
  - overcosted_ramp
  - win_more_payoff
  - redundant_high_mv_card
  - generic_creature_without_engine_text
  - removal_that_does_not_match_needs
  - cute_card_that_requires_already_winning
  - theme_card_with_no_engine_contribution
  - backup_engine_that_slows_primary_plan
```

### Protect Priority

```yaml
protect_priority:
  - cheap_commander_enabler
  - cheap_engine_piece
  - role_compressed_card
  - package_glue
  - combo_piece
  - low_mana_draw_or_selection
  - low_mana_interaction
  - mana_piece_that_supports_commander_timing
  - resource_converter
  - card_that_makes_practiced_move_repeatable
```

## Final Deck Review Packet

Before a deck is considered ready, generate a final review packet.

```yaml
final_review_packet:
  commander_billboard: required
  deck_thesis: required
  branch_identity: required
  structural_audit: required
  package_map: required
  protected_glue: required
  win_condition_review: required
  mana_plan_review: required
  card_flow_review: required
  protection_review: required
  interaction_review: required
  budget_review: required
  ownership_review: required
  cut_risk_review: required
  human_validation_zones: required
  final_status: draft | needs_repair | ready_for_human_review | approved_by_human
```

The system must not mark a deck approved automatically.

## Generic Regression Tests

Do not use real card names yet.

Create generic tests first.

```yaml
generic_regression_tests:
  wrong_seat_replacement:
    description: "A reusable mana source should not be replaced by a one-shot utility artifact unless the source seat is also one-shot utility."
  structural_repair_before_swap:
    description: "A deck with wildly broken land count should trigger structural repair before normal swaps."
  package_glue_protection:
    description: "A weak-looking card that enables the primary package should be protected."
  package_pivot:
    description: "A rebuild around a different package should be labeled package_rebuild or sidegrade_to_new_theme."
  no_swap:
    description: "An optimized card should produce NO_SWAP when candidates do not improve its seat."
  ui_structure:
    description: "Audit output should surface structural interpretation, not only raw counts."
  budget_compression:
    description: "When tutors are reduced for cost, redundancy and card flow should increase."
  fake_turbo:
    description: "Low land count without matching acceleration should trigger a mana-plan warning."
  high_land_shell:
    description: "High-land builds should pass only if enough lands convert into action."
  branch_detection:
    description: "Distinct strategies should be identified as branches instead of averaged."
```

## Codex Instruction

When Codex uses this file:

1. Do not parse card names.
2. Do not parse decklists.
3. Extract deckbuilding doctrine only.
4. Convert doctrine into local rules, schemas, fixtures, validation checks, reports, and tests.
5. Preserve offline-first design.
6. Preserve human approval gates.
7. Prefer deterministic logic.
8. Prefer role/seat reasoning over generic categories.
9. Preserve no-swap behavior.
10. Treat this as deckbuilding doctrine, not card data.

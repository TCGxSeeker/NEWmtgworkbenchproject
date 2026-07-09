# MTG Workbench Build Philosophy Seed

## Purpose

This document distills the deckbuilding philosophy, analysis process, failure lessons, and architecture direction for the MTG Workbench project.

Do not treat this file as a card database.
Do not parse individual decklists from this file.
Do not extract specific card names from this file yet.
Do not use this file to create card-specific recommendations.

Use this file to design the project's local rules, data contracts, analysis passes, validation checks, and recommendation logic.

The goal is to encode the reusable reasoning system behind the MTG project into a local, deterministic, offline-first program.

The project should eventually feel like an MTG deckbuilding cockpit:

- import decklist
- identify commander plan
- run structural audit
- classify card seats
- detect packages
- protect package glue
- generate explainable recommendations
- allow no-swap when appropriate
- produce a final review packet
- preserve human approval over strategic calls

The program should not become:

- a generic deck optimizer
- a popularity-based recommender
- an EDHREC clone
- a live API wrapper
- a chatbot-only deckbuilder
- an autonomous final decklist generator

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

The system should survive model updates, tool changes, and vibe drift because the actual reasoning has been codified into local artifacts.

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
- does not always explain the source card's seat
- does not always explain the candidate card's seat
- does not do enough same-seat delta scoring
- does not protect package glue reliably
- forces weak swaps instead of allowing no-swap
- may surface math without surfacing strategic structure visually

Preferred v2 target:

Commander Billboard -> Structural Audit -> Card Seat Reasoning -> Recommendation Explanation

## Core Deckbuilding Philosophy

A strong deck is not a pile of good cards.

A strong deck is one commander-specific move practiced until the cheap cards start looking unfair.

The system should prioritize:

1. Deck identity before generic staples.
2. Commander text before broad archetype assumptions.
3. Actual function before card fame.
4. Package fit before isolated card quality.
5. Structural health before card-level swaps.
6. Seat reasoning before candidate recommendation.
7. Repeatable engine behavior before "cool payoff" cards.
8. Compact win routes before scattered value.
9. Budget function translation before exact card replacement.
10. Human approval before subjective final decisions.

## Commander Billboard System

Every deck starts with a commander billboard.

The commander billboard answers:

- What does the commander actually do?
- What resource does the commander create?
- What resource does the commander consume?
- What action does the commander reward?
- What board state does the commander require?
- What is the commander's primary conversion?
- What is the commander's secondary conversion?
- What packages does the commander imply?
- What cards become better because of the commander?
- What cards are traps despite looking on-theme?
- What does the deck need to close the game?

### Commander Billboard Fields

```yaml
commander_billboard:
  commander_name: TODO
  color_identity: TODO
  mana_value: TODO
  commander_function: TODO
  primary_conversion: TODO
  secondary_conversion: TODO
  main_resource_created: TODO
  main_resource_consumed: TODO
  required_materials: []
  implied_packages: []
  avoid_patterns: []
  primary_kill_route: TODO
  backup_kill_route: TODO
  deck_thesis: TODO
```

# Card Relationship Primitives v0

## Status

Planning and vocabulary contract only.

This document does not authorize package detection, strategic analysis,
commander evaluation, recommendations, or card-quality judgments.

## Purpose

Card Relationship Primitives v0 defines the smallest deterministic vocabulary
needed to describe factual relationships between deck entries.

The system should understand facts and compatible behavior before it attempts
classification, deck analysis, or recommendation.

Core doctrine:

> Facts describe cards.
> Interfaces describe behavior.
> Edges describe relationships.
> Subgraphs may later describe packages.
> Context may later describe relevance.
> Judgment comes last.

## Architectural Direction

The relationship system uses a behavioral interface graph.

A card is not primarily represented as a generic role. Instead, factual card
data may eventually produce a behavioral profile containing:

- outputs
- costs
- requirements
- emitted events
- observed events
- permissions
- modifiers
- zone constraints
- timing constraints

Relationships are derived only when compatible behaviors have explicit,
traceable evidence.

Roles remain advisory metadata. They are not the ontology of the deck.

## Vocabulary Fixture

The machine-readable planning fixture is:

`data/fixtures/relationships/card_relationship_primitives.example.json`

The fixture is a versioned vocabulary contract. It is not yet an executable
rules engine.

Schema version:

`card_relationship_primitives.v0`

## Initial Resources

The v0 planning vocabulary recognizes these resource concepts:

- mana
- Treasure
- artifact
- creature
- card in hand
- graveyard card

This does not claim complete Magic rules coverage.

Unsupported or ambiguous resources must remain explicit rather than being
guessed.

## Initial Events

The v0 planning vocabulary recognizes:

- spell cast
- noncreature spell cast
- permanent entered
- attack declared
- combat damage dealt
- card discarded
- permanent sacrificed
- creature died
- card drawn

Event names describe factual game events. They do not imply strategic value.

## Primitive Relationship Types

### SUPPLIES

The source produces a resource that the target explicitly consumes or requires.

Example:

A Treasure producer may supply an artifact-sacrifice cost.

### TRIGGERS

The source emits an event that the target explicitly observes.

Example:

A sacrifice outlet may trigger a permanent-sacrificed listener.

### ENABLES

The source satisfies an explicit prerequisite or grants a permission needed by
the target.

Example:

A card that permits casting from exile may enable a spell that otherwise
cannot be cast from that zone.

### AMPLIFIES

The source mechanically increases the output, frequency, or magnitude of the
target's supported behavior.

Amplification must be supported by direct rules evidence. General strategic
praise is not amplification evidence.

### PROTECTS

The source directly prevents, redirects, or answers disruption affecting the
target or a required state.

This primitive describes mechanical protection only. It does not determine
whether the protection is strategically sufficient.

### RECURS

The source returns, reuses, or makes available a target card or supported
resource from a previously unavailable zone.

### CONFLICTS_WITH

The source and target have explicit mechanical requirements that cannot both
be satisfied, or one directly prevents the other's supported behavior.

This is not a declaration that either card is bad.

## Deferred Relationship Types

The following concepts are intentionally deferred:

- redundant with
- competes with
- converts
- closes with

These concepts require additional contextual or strategic interpretation and
must not enter v0 accidentally.

## Evidence Contract

Every future relationship edge must preserve:

- source entry identifier
- target entry identifier
- relationship type
- matched source behavior
- matched target behavior
- Oracle-text evidence
- required conditions
- zone compatibility
- confidence band
- deterministic derivation rule

An edge without traceable evidence is unsupported.

## Confidence Bands

The initial shared confidence bands are:

- 0
- 25
- 50
- 75
- 100

Confidence represents evidence strength under a deterministic rule. It does not
represent card quality, deck power, or recommendation strength.

## Derivation Boundaries

Relationship derivation must not default to comparing every card against every
other card.

Later implementations should index compatible behavioral interfaces, such as:

- resource producers
- resource consumers
- event emitters
- event observers
- requirement providers
- protection providers
- recursion providers

Only compatible groups should be considered for an edge.

## Entry-Level Identity

Relationships belong to deck entries, not merely canonical card names.

This preserves:

- zone
- quantity
- imported labels
- deck-specific metadata
- unresolved state
- future commander context

Canonical card facts may be shared, but deck-entry relationships remain
contextual records.

## Explicit Non-Goals

Card Relationship Primitives v0 does not provide:

- synergy scoring
- deck-level role totals
- package detection
- commander analysis
- recommendations
- card-quality judgments
- all-pairs comparison
- hidden inference
- combo solving
- candidate search
- add or cut scoring
- user-interface behavior

## Planned Implementation Order

1. Lock doctrine and vocabulary fixture.
2. Add typed relationship primitive models.
3. Add a factual card behavioral-profile model.
4. Add bounded behavioral atom extraction.
5. Add deterministic relationship-edge derivation.
6. Add a card relationship report.
7. Add an end-to-end fixture smoke test.
8. Plan package motifs only after the graph contract is stable.

Each step must land independently with tests before the next step begins.

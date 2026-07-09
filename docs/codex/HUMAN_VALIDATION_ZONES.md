# Human Validation Zones

Require explicit human review before changing or finalizing:

- Commander selection or commander identity.
- Final 100-card decklist approval.
- Deck primary archetype or major build direction.
- Combo package inclusion or removal.
- Final card cuts or additions.
- Cards over the normal budget threshold.
- Expensive card exceptions.
- Power-level claims.
- Commander bracket estimates.
- cEDH versus budget-competitive classification.
- Competitive viability claims.
- Meta-specific calls.
- Fun factor decisions.
- Live purchase recommendations.
- Publishing decklists.
- Core deck strategy changes.
- Scoring rubric logic.
- Recommendation weights or recommendation logic concepts.
- Card evaluation rules.
- Validation gates.
- Project rules.
- Source-of-truth dataset overwrites.
- Local data deletion.
- Fresh pricing, legality, or newly released card assumptions.
- External API usage, including Scryfall update behavior.
- Paid services.
- Account login, authentication, authorization, secrets, API keys, or environment handling.
- Production deployment configuration.
- Large dependency changes.
- Destructive file, database, or data operations.
- User-facing copy where tone or brand taste matters.

## Required Review Format

For any validation-zone change, present:

- Proposed action.
- Why it is needed.
- Expected effect.
- Data or rule source.
- Risk if wrong.
- Rollback or undo path.
- Alternatives.

Do not proceed until the user explicitly approves the proposed direction.

## Automation Boundary

Codex and the program may recommend, score options, explain tradeoffs, and propose changes. They must not finalize major strategic decisions without human approval.

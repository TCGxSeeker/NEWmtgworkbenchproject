# Verification Plan

## Baseline Documentation Checks

Run after planning or documentation changes:

```bash
git rev-parse --show-toplevel
rg --files --hidden -g '!.git/**'
git status --short
```

Expected root: `C:/Users/StDeL/Documents/New MTG project`.

## Verification Principles

- Verification must not require internet access.
- External data must be represented by local fixtures or local snapshots.
- Unknown cards, missing data, and invalid inputs must fail visibly instead of being guessed.
- Recommendation outputs must cite local rules, local data, or explicit user-approved exceptions.
- Human validation flags must be testable and visible in reports.

## Future Test Categories

Add unit and fixture tests for:

- Decklist parser behavior.
- Card name normalization.
- Quantity preservation and deck count legality.
- Commander detection.
- Duplicate detection.
- Unknown or missing card reporting.
- Color identity validation.
- Local legality checks when local data exists.
- Mana curve and mana value distribution.
- Mana source and color pip analysis.
- Land, ramp, draw, interaction, protection, engine, payoff, and win-condition counts.
- Role count and context-specific tagging.
- Package detection.
- Budget threshold checks.
- Ownership/on-hand checks.
- Recommendation scoring and confidence.
- Final-check report generation.
- Gotcha regression tests.

## Fixture Requirements

Create local fixtures in Phase 1 before parser or recommendation work:

- Minimal local card snapshot.
- Valid Commander decklist.
- Invalid decklist with unknown cards.
- Decklist with commander and maybeboard markers.
- Owned-card CSV.
- Budget profile.
- Commander profile.
- Package definition.
- Known-good audit output.

## Manual Human Review Checklist

Use manual review for:

- Scoring rubric interpretation.
- Commander bracket estimates.
- Recommendation logic and tradeoffs.
- Package warning quality.
- Card role meaning in this exact deck.
- Expensive card exceptions.
- Meta-specific claims.
- UI copy, layout, and text overflow when UI work begins.
- Fresh pricing, legality, and newly released card assumptions.

## CLI Verification Targets

Once implementation begins, the first target should be a local CLI smoke test similar to:

```bash
mtg audit tests/fixtures/decks/sample.txt --cards tests/fixtures/cards/sample.json
mtg final-check tests/fixtures/decks/sample.txt --cards tests/fixtures/cards/sample.json
```

Exact commands must be updated after the stack and CLI shape are chosen.

## Skill Checks

Validate local skill files when they change:

```bash
python C:/Users/StDeL/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/project-launch-spec
python C:/Users/StDeL/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/verification-gate
python C:/Users/StDeL/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/gotcha-capture
```

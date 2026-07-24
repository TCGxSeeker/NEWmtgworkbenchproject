---
name: user-reviewer
description: Use after a completed UI, visualization, report preview, or deckbuilder workflow slice to review it from a normal user perspective and return ratings, risks, and actionable polish notes without replacing human validation.
---

# User Reviewer Skill

## When to Use

Use this skill after a completed visible section needs a user-centered review, especially:

- deckbuilder screens
- visualization previews
- workflow checkpoints
- report/readout surfaces
- before expanding a UI slice with more features

## When Not to Use

Do not use this skill for:

- unfinished implementation work
- backend-only code reviews
- security reviews
- deck power-level scoring
- recommendation quality judgment
- final brand/taste approval
- replacing the user's human validation pass

## Required Inputs

- Section or workflow being reviewed.
- Screenshot, browser view, rendered preview, or concise description.
- Relevant task goal and constraints.
- Known project UI doctrine or non-goals.
- Any user feedback already given.

## Review Standards

Review against the MTG Workbench product direction:

- deckbuilder-centered workflow
- calm, modern, readable presentation
- progressive disclosure
- clear visual hierarchy
- useful information only
- no dense feature-collage dashboard
- no premature recommendations, scoring, legality claims, or power-level claims
- no raw debug data in default UI
- responsive layout sanity
- understandable to capable MTG players and newer deckbuilders

## Workflow

1. Identify what section is complete enough to review.
2. State the assumed user goal for that section.
3. Inspect the visible UI or provided artifact.
4. Rate clarity, usefulness, calmness, hierarchy, and clutter risk.
5. Identify what passes.
6. Identify polish issues that can wait.
7. Identify blocking concerns that should be fixed before building on it.
8. Separate user-facing concerns from implementation concerns.
9. Recommend one next visual or workflow improvement.
10. Preserve the final decision for human validation.

## Output Format

```text
User Reviewer Report

Section reviewed:
Assumed user goal:

Overall rating: /10
Clarity rating: /10
Visual calm rating: /10
Deckbuilder usefulness: /10
Hierarchy rating: /10
Clutter risk: Low / Medium / High

Pass:
- ...

Needs polish:
- ...

Blocking concerns:
- ...

Suggested next visual change:
- ...

Do not change:
- ...

Human validation needed:
- Yes. Final UI taste approval remains with the user.
```

## Gotchas

- Do not praise clutter because it shows many features.
- Do not request more dashboard widgets by default.
- Do not treat internal validation, debug data, or algorithm evidence as normal user-facing content.
- Do not recommend live services, pricing, legality, or recommendation features unless the reviewed slice explicitly includes approved local data and scope.
- Do not confuse Archidekt/Moxfield parity with copying their density or hosted-service behavior.
- Do not present ratings as objective truth; they are structured review signals.

## Verification

Confirm that the review:

- names the reviewed section
- gives numeric ratings
- identifies clutter risk
- separates pass, polish, and blockers
- preserves human validation
- stays within approved project scope
- avoids deck strategy, recommendation, and power-level judgment

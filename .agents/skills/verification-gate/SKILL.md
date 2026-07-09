---
name: verification-gate
description: Use before and after implementation to define, run, and report verification checks for a Codex task.
---

# Verification Gate Skill

## When to Use

Use this before making meaningful changes and again after completing them.

## Workflow

1. Identify what must be true for the task to be successful.
2. Identify available automated checks.
3. Identify required manual checks.
4. Identify high-risk areas.
5. Write or update `docs/codex/VERIFICATION_PLAN.md`.
6. After implementation, run available checks.
7. Report pass/fail/blocked status.

## Verification Categories

Consider:

- tests
- lint
- type check
- build
- smoke test
- sample input/output
- UI review
- security review
- data integrity review
- regression check

## Gotchas

- Do not claim success without evidence.
- If a check cannot be run, say why.
- Do not skip manual validation for high-risk areas.
- Do not treat "no errors shown" as full verification.

## Completion Format

Return:

- Checks run
- Results
- Checks not run
- Reason not run
- Remaining risks
- Recommended next step

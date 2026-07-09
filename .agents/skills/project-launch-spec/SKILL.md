---
name: project-launch-spec
description: Use when starting a new feature, refactor, tool, automation, or project. Produces a project brief, implementation spec, verification plan, and human validation checklist before coding.
---

# Project Launch Spec Skill

## When to Use

Use this skill when the user wants to start a new project, feature, refactor, automation, or multi-file change.

## When Not to Use

Do not use this skill for tiny one-line fixes, formatting-only edits, or simple questions.

## Required Inputs

- User goal
- Repository context
- Known constraints
- Desired output
- Any existing files or examples

## Workflow

1. Identify the core problem.
2. Identify who the solution is for.
3. Identify who it is not for.
4. Define the smallest useful version.
5. Inspect the repository structure.
6. Identify files likely involved.
7. Write `docs/codex/PROJECT_BRIEF.md`.
8. Write `docs/codex/IMPLEMENTATION_SPEC.md`.
9. Write `docs/codex/VERIFICATION_PLAN.md`.
10. Write `docs/codex/HUMAN_VALIDATION_ZONES.md`.
11. Ask for review only if blocked by missing information.

## Expected Outputs

- Project brief
- Implementation spec
- Verification plan
- Human validation zones
- Clear next implementation step

## Gotchas

- Do not jump directly into coding.
- Do not overbuild the first version.
- Do not assume the user wants full automation.
- Always document assumptions.
- Always include verification.

## Verification

Confirm that the spec includes:

- goal
- scope
- non-goals
- files affected
- implementation steps
- risks
- validation steps
- definition of done

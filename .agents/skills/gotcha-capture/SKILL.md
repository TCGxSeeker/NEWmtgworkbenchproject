---
name: gotcha-capture
description: Use when the user corrects Codex, identifies an edge case, rejects an output style, or points out a recurring mistake.
---

# Gotcha Capture Skill

## When to Use

Use this when the user says something like:

- not that
- wrong
- remember this
- next time
- you missed
- that broke
- don't do that again
- this should work differently

## Workflow

1. Identify the correction.
2. Determine whether it applies globally, to this project, or to a specific skill.
3. Update `docs/codex/GOTCHAS.md`.
4. If a related skill exists, update its Gotchas section.
5. If the correction affects implementation rules, update `AGENTS.md`.
6. Summarize what was updated.

## Gotchas

- Do not store random preferences that are unlikely to matter again.
- Do not overwrite existing gotchas; append and organize them.
- Do not minimize workflow corrections by only acknowledging them in chat; update the durable project rules when they affect repeated work.
- Do not hide uncertainty. If the correction is ambiguous, record it as a question.

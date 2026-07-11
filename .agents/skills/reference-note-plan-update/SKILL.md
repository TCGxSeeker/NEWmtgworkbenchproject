---
name: reference-note-plan-update
description: Use when the user provides an article, blog post, hand-off, screenshot notes, external reference, or design discussion and wants Codex to extract durable project-relevant notes, update planning/reference docs, or memorize a workflow without implementing code.
---

# Reference Note Plan Update Skill

## When to Use

Use this skill when the user asks to:

- Analyze a reference source for project relevance.
- Capture notes from an article, hand-off, screenshot, PDF, or discussion.
- Update planning docs from external context.
- Memorize a repeated note-taking or planning-update workflow.
- Record lessons without implementing code.

## When Not to Use

Do not use this skill for:

- Direct feature implementation.
- Schema changes or migrations.
- Recommendation-engine logic.
- UI construction.
- Simple factual questions that do not need repo updates.

## Required Inputs

- Source material or link.
- The project question or concern the source should inform.
- Scope limits, especially whether code/schema changes are forbidden.
- Preferred destination file, if the user names one.

## Workflow

1. Identify the task goal, likely files, verification method, human validation zones, and whether subagents would help.
2. If the source is a link, browse it and rely on source-specific summaries rather than long quotes.
3. Extract only lessons relevant to MTG Workbench goals, current phase, and known constraints.
4. Separate decisions from non-decisions:
   - Document confirmed lessons as reference notes.
   - Document unresolved tradeoffs as open questions.
   - Do not silently convert a reference lesson into an implementation commitment.
5. Choose the closest existing reference or planning location:
   - Use the user-requested path when it exists or can be reasonably created.
   - Otherwise use the nearest existing `docs/product/**/reference/`, `docs/rules/`, or `docs/codex/` location and note why.
6. Update docs only, unless the user explicitly approves implementation.
7. If the reference reveals a risk in existing behavior, document the risk and future correction path before changing code.
8. Preserve scope guards:
   - No recommendation-engine expansion.
   - No schema changes unless already approved.
   - No live-service dependency unless explicitly requested.
   - No UI implementation from reference notes alone.
9. Add source links and concise project-specific implications.
10. Run verification and summarize changed files, captured principles, open questions, and remaining risks.

## Expected Outputs

- A project reference note, planning update, or decision/open-question entry.
- Clear distinction between source facts, project implications, and future decisions.
- Exact file paths changed.
- Verification results.

## Gotchas

- Do not overfit to another author's architecture; translate only what supports MTG Workbench.
- Do not copy long article passages.
- Do not treat web/API examples as permission to add live API calls.
- Do not let a reference note override user-approved offline-first behavior.
- Do not implement code while the user asked for documentation only.
- Do not bury important caveats in chat only; preserve durable notes in the repo.

## Verification

Run the relevant checks:

```powershell
git diff --check
git status --short
```

For skill edits, also run:

```powershell
python C:/Users/StDeL/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/reference-note-plan-update
```

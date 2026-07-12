# Repository Guidelines

## Repository Isolation

Treat `C:\Users\StDeL\Documents\New MTG project` as the only workspace. Before editing, verify the root with `git rev-parse --show-toplevel` and keep changes inside that path. Do not copy files, config, dependencies, generated output, or `.env` values from sibling projects unless explicitly requested. This repository has no Git remote, so add one only after confirming the destination.

## Codex Project Instructions

### Working Mode

Before making changes, Codex must identify:

1. The goal of the task.
2. The files likely involved.
3. The verification method.
4. Any human validation zones.
5. Whether subagents would help.

Prefer small, reviewable changes. Avoid broad rewrites unless explicitly requested.

### Workflow Integrity Rule

Do not intentionally cut corners in the required project workflow. If a required step is genuinely not applicable, state why. If a constraint prevents a check, plan update, or validation step, report the constraint and provide the safest smaller alternative. Never imply that planning, verification, review, or validation happened when it did not.

### Planning Rule

For any feature, refactor, architecture change, automation, or multi-file task:

1. Create or update `docs/codex/IMPLEMENTATION_SPEC.md`.
2. Show key decisions before building.
3. Document assumptions.
4. Wait only if genuinely blocked; otherwise proceed with best judgment.

### Verification Rule

Before building, state how the work can be verified.

After building, run the relevant checks when available, such as:

- tests
- linting
- type checks
- smoke tests
- CLI commands
- sample input/output checks
- manual review checklist

If verification cannot be run, explain why and provide exact manual verification steps.

### Human Validation Zones

Codex must require explicit human review before changing:

- payment logic
- authentication or authorization
- secrets, API keys, or environment handling
- destructive database operations
- production deployment configuration
- large dependency changes
- user-facing copy where tone/brand taste matters
- project rules, scoring systems, or evaluation logic

### Subagent Rule

Use subagents when work benefits from parallel review, multiple perspectives, or independent workstreams.

Good subagent uses:

- security review
- bug review
- test coverage review
- architecture review
- documentation review
- performance review
- alternative implementation proposals

Subagents should each have a narrow task and return findings, risks, and recommended actions.

### Skill Rule

When a workflow has been repeated or corrected more than once, propose turning it into a Codex skill in `.agents/skills`.

Every skill should include:

- when to use it
- when not to use it
- exact steps
- required inputs
- expected outputs
- gotchas
- verification steps

### Gotchas Rule

When the user corrects Codex, update `docs/codex/GOTCHAS.md`.

If the correction applies to a skill, update that skill's `SKILL.md` with a Gotchas section.

### Automation Rule

Before automating anything, run this test:

1. Does the task require taste, judgment, or subjective quality?
   - If yes, augment instead of fully automating.
2. Would an 80% correct output be acceptable?
   - If no, augment with human review.
3. What is the cost of failure?
   - If high, require human sign-off.

Favor augmentation over automation unless the workflow is low-risk, repeatable, and objectively verifiable.

### Completion Response Format

At the end of each task, summarize:

- What changed
- Files changed
- How to verify
- Known risks
- Suggested next step

## Project Structure & Module Organization

Use this repository-specific structure for Codex planning, task tracking, and local skills:

```text
AGENTS.md
apps/deckbuilder-ui/  Free Vite + React + TypeScript UI scaffold
docs/codex/      Project brief, specs, verification, decisions, gotchas
.tasks/          Immediate next work and backlog
.agents/skills/  Project-local Codex skills
src/             Python package for CLI, parsing, card data, and search
tests/           Python unit tests and fixtures
```

Avoid committing build output, dependency folders, caches, or editor artifacts.

## Build, Test, and Development Commands

Use these checks from the repository root unless noted:

```powershell
$env:PYTHONPATH = 'src'
python -m unittest discover -s tests
```

Runs the Python parser, normalizer, Scryfall indexing/search, and fixture tests.

```powershell
$env:Path = 'C:\Program Files\nodejs;' + $env:Path
Push-Location apps/deckbuilder-ui
& 'C:\Program Files\nodejs\npm.cmd' ci
& 'C:\Program Files\nodejs\npm.cmd' run build
& 'C:\Program Files\nodejs\npm.cmd' run lint
Pop-Location
```

Restores, builds, and lints the free frontend scaffold. Use `npm.cmd` if PowerShell blocks `npm.ps1`. Dependency restoration may require network access unless the npm cache is warm.

## Coding Style & Naming Conventions

Follow the conventions of the chosen language and framework. Use consistent indentation, descriptive names, and focused modules. If a formatter or linter is added, commit its config and run it before review.

## Testing Guidelines

Add tests with new behavior and bug fixes. Use names such as `feature.test.ts`, `test_feature.py`, or the framework default. Cover normal behavior, edge cases, and regressions. Keep shared fixtures in `tests/fixtures/`.

## Commit & Pull Request Guidelines

This repo now uses small, checkpoint-style commits with concise imperative messages, such as `Complete Search-2 filters` or `Add deckbuilder foundation docs`. Before committing, run relevant checks, review `git status --short`, and keep generated artifacts ignored. Pull requests should include what changed, why, verification, related issues, UI screenshots when UI changes exist, and remaining risks or follow-ups.

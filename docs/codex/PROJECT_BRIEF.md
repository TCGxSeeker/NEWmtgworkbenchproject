# Project Brief

## Source of Truth

Use the user's interview answers and the supplemental hand-off as the current project source of truth. If older repository notes conflict with those answers, prefer the interview and record the conflict in `docs/codex/DECISION_LOG.md`.

## Core Problem

Commander deckbuilding is repetitive, data-heavy, and easy to distort with generic staples, popularity shortcuts, or vague power claims. This project should make deckbuilding easier by importing decklists, normalizing cards, analyzing structure, detecting missing roles/packages, checking budget and ownership constraints, and producing deterministic recommendation drafts for human approval.

## Product Vision

This is a local, deterministic Magic: The Gathering Commander deckbuilding workbench: an offline "Jarvis of MTG" that encodes the user's deckbuilding philosophy, rules, templates, gotchas, analysis methods, and approval gates into repository files, local data, tests, and reusable Codex skills.

This is not:

- A generic MTG deckbuilder.
- A chatbot wrapper.
- An EDHREC clone.
- An API-dependent recommendation tool.
- A system that finalizes strategic deck decisions without human review.

## Audience

The primary user is the repository owner. The long-term audience is capable MTG players and newer players who want a portable, local workbench for Commander deck analysis, budget-aware improvements, and explainable recommendations.

## Not For

The project is not for people who do not play MTG, users uninterested in deckbuilder tools, or users who want popularity-driven recommendations without deck identity, budget, ownership, and strategy constraints.

## MVP

Prefer a local CLI MVP before any web UI. The MVP should prove the project can parse, normalize, analyze, and report on Commander decklists using local data only. The smallest useful CLI should likely start with:

- `mtg audit`: import a decklist, normalize cards, run structural checks, and produce an audit report.
- `mtg final-check`: produce a review packet with validation results and human approval flags.

Additional commands such as `mtg recommend`, `mtg owned-search`, `mtg compare`, and `mtg explain-card` should wait until the audit model, fixtures, and deterministic rules are stable.

## Version 1 Success

Version 1 succeeds when a user can import a supported decklist, receive a deterministic deck report, inspect deck statistics, see missing roles and package warnings, export the decklist, and review recommendation drafts that explain add/cut reasoning without claiming final authority.

## Failure Cases To Avoid

- Bad or misleading deck reports.
- Card count miscalculations.
- Incorrect scoring, bracket, legality, or pricing claims.
- Card search or normalization failures.
- Recommendations based on fame, popularity, or generic staple status.
- Ignoring commander plan or deck identity.
- UI copy overflow or generic filler text when UI work eventually begins.
- Requiring internet access for base analysis.

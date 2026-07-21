# Gotchas

## Repository Gotchas

- The active repository root is `G:\Documents\New MTG project`; older `C:\Users\StDeL\Documents\New MTG project` references are stale unless explicitly discussing history.
- The repository now has Python source/tests and an isolated frontend scaffold, but no production app build or finished UI.
- The repository has a configured Git remote. Verify `git remote -v` before changing remote configuration, pushing to a new destination, or assuming GitHub state.
- Hidden directories such as `.tasks/` and `.agents/` may not appear in simple file listings. Use `rg --files --hidden -g '!.git/**'`.
- Do not assume conventions from nearby projects apply here.
- Do not intentionally cut corners in project workflow. If a required step does not apply or cannot be run, explain why and choose the safest smaller alternative instead of silently skipping it.

## Workflow Corrections

### 2026-07-12: Do Not Intentionally Cut Corners

- Symptom: Workflow shortcuts can make planning, validation, or handoff quality look complete when it is not.
- Cause: Compressing required project steps because a task feels small, obvious, repetitive, or inconvenient.
- Fix: Follow the required workflow unless a step is genuinely inapplicable or blocked; document any skipped or blocked step explicitly.
- Prevention: Keep `AGENTS.md`, local skills, specs, verification plans, and final summaries honest about what was planned, run, skipped, or deferred.
- Regression test: Not directly testable in code; verify through review of task summaries and verification evidence.
- Skill update: Update planning and verification skill gotchas to reinforce this rule.

### 2026-07-14: Distinguish Focused and Full Test Counts

- Symptom: A focused relationship command reported 42 passing tests, which could appear to mean the repository test suite had unexpectedly shrunk.
- Cause: Explicitly naming test modules runs only those selected modules; it does not perform repository-wide discovery.
- Fix: Label focused commands as focused verification and use `python -m unittest discover -s tests` as the authoritative full-suite command.
- Prevention: State separate expected counts for focused verification and full discovery whenever both commands are provided.
- Regression test: Not directly testable in application code; verify through workflow documentation and command output.
- Skill update: No skill change required.

## MTG Workbench Gotchas

- Do not turn every deck into generic staples.
- Do not ignore deck identity.
- Do not recommend cards without explaining what they replace or improve.
- Do not confuse card category with card purpose in this specific deck.
- Do not claim competitive viability without evidence.
- Do not count emotionally adjacent cards as fulfilling a role unless they actually do the job.
- Do not overwrite source data without approval.
- Do not fully automate subjective final calls.
- Do not require internet access for base analysis.
- Do not use popularity as a proxy for card quality.
- Do not rank cards by repeat user behavior.
- Do not build telemetry or usage-history scoring into the base system.
- Do not require external APIs for core analysis.
- Do not assume Scryfall, EDHREC, Moxfield, Archidekt, or any other live service is available.
- If external data is useful later, treat it as optional manual ingestion into local files.
- Do not make fresh pricing or legality claims unless a verified local snapshot supports them.
- Do not let recommendations become final authority; they are drafts for human review.
- Do not invent missing source documents, scoring rubrics, card data, or deckbuilding rules.
- Do not parse card names or decklists from doctrine seed files.
- Do not make card-level swaps before structural audit.
- Do not treat card similarity as deck improvement.
- Do not cut package glue just because it looks weak alone.
- Do not average different branches into an incoherent hybrid.
- Do not copy turbo land counts into budget decks without matching acceleration.
- Do not add backup engines if they make the main engine slower.
- Do not force a recommendation when no-swap is correct.
- Do not let raw counts replace structural interpretation in reports.
- Do not normalize unknown card names by guessing.
- Do not treat duplicate known non-basic cards as hard parser failures in Phase 2; warn instead.
- Do not let the Phase 2 parser grow into structural audit or recommendation logic.
- Do not commit full Scryfall bulk payloads to Git; keep large snapshots local and ignored.
- Do not treat a Scryfall snapshot as fresh forever; record snapshot timestamps and source URLs.
- Do not treat Oracle tags as just a loose tag vocabulary; `otag:` search should resolve tags first, then pull cards through `oracle_id` taggings.
- Do not search compressed Scryfall JSONL directly in production paths when a local index exists.
- Do not commit generated SQLite search indexes.
- Do not build redundant full-text indexes over every print row unless disk budget and query needs justify it.
- Do not treat unknown comparison syntax such as `pow>=3` as bare text; report it as unsupported syntax.
- Do not make `otag:` substring-fuzzy by default; match exact tag slug, label, or alias before expanding taggings.
- Do not let the future UI become a dense feature collage. The workbench can expose many features, but the finished visual design should feel clean, calm, elegant, and intentionally paced rather than ugly, cluttered, or panel-stuffed.
- Do not let local search expansion turn the project into an offline Scryfall clone. Search should become strong enough for in-app lookup and candidate discovery, but deck analysis is the product.
- Do not prioritize search UI over deck audit, reports, commander profiles, role/seat reporting, or recommendation explanation.
- Do not design the main app around search-first workflows. The user should feel guided through deck understanding, not buried under widgets.
- Future UI should use progressive disclosure, clear hierarchy, strong whitespace, readable typography, restrained accents, and actionable warnings only. Avoid dense sci-fi control panels unless explicitly requested.
- Do not treat syntax filters as independent searches. Multiple syntax additions in one query must intersect, such as `mv<=2 id:g t:instant o:draw`.
- In future deck-context search, color identity should be auto-applied or strongly available from the current deck context, while remaining visible and user-controllable.
- Do not treat Archidekt/Deckcheck-style screenshots as clone requirements. Extract deckbuilder capabilities and tidy interaction patterns, not exact styling.
- Do not let the deckbuilder workspace become secondary to search, stats, probability tools, or reports. Those features support the primary deck screen.
- Do not treat frontend tooling scaffold as product implementation. A Vite/React shell is infrastructure until deckbuilder contracts and UI requirements are ready.
- Do not install paid UI kits, account-gated services, telemetry tools, or desktop packaging frameworks without an explicit human checkpoint.
- Do not treat "Delete Deck" as deleting card data. In the future UI, deleting a deck should remove/close/delete only that deck's native `.mtgwdeck.json` workspace and remove its cards from the current deck view; it must never delete cards from the local Scryfall/card database, card snapshots, shared indexes, owned-card data, source fixtures, or other decks.
- Do not surface local fact coverage, missing-card facts, ambiguous-card facts, or unresolved-card plumbing as standard deckbuilder UI data. Treat those as background validation or advanced/debug review unless the user explicitly opens a validation/details view; normal screens should emphasize generic deckbuilder actions and useful deck contents.
- Do not describe MTG Workbench as having generic deckbuilder parity yet. The accurate status is a strong deckbuilder backend foundation with CLI-verifiable contracts, while the user-facing deckbuilder product still needs visible card presentation, search/add workflow, card details, validation, bulk safety, statistics, printing management, and version recovery.
- Do not count planned/contracted UI features as implemented deckbuilder functionality. Mark them as planned until there is working product behavior, even when backend data models or documentation already exist.
- Do not treat safe workspace deletion as implemented until a dedicated helper or command exists and has tests. Current delete behavior is doctrine and UI intent, not completed functionality.
- Keep recommendation commentary off the near-term deckbuilder parity path unless the user explicitly asks for it. The current parity sequence is about seeing the deck, finding/adding cards, understanding cards, validating, editing safely, inspecting stats, managing printings, and recovering versions.

## Capture Format

When a gotcha is discovered, record:

- Date.
- Symptom.
- Cause.
- Fix.
- Prevention.
- Whether it should become a regression test.
- Whether a skill should be updated.

# Gotchas

## Repository Gotchas

- The repository now has Python source/tests and an isolated frontend scaffold, but no production app build, finished UI, or Git remote.
- Hidden directories such as `.tasks/` and `.agents/` may not appear in simple file listings. Use `rg --files --hidden -g '!.git/**'`.
- Do not assume conventions from nearby projects apply here.

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

## Capture Format

When a gotcha is discovered, record:

- Date.
- Symptom.
- Cause.
- Fix.
- Prevention.
- Whether it should become a regression test.
- Whether a skill should be updated.

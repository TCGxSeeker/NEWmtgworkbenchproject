# Gotchas

## Repository Gotchas

- The repository currently has no build system, test framework, package manager, source code, fixtures, local card data, or remote.
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

## Capture Format

When a gotcha is discovered, record:

- Date.
- Symptom.
- Cause.
- Fix.
- Prevention.
- Whether it should become a regression test.
- Whether a skill should be updated.

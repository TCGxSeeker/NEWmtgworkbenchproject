# Backlog

## Active Catchup Repair Queue

- No active numbered catchup repair remains after Step 6.
- Readiness checkpoint passed before Deck Inspection CLI v0.
- Native Workspace Import/Export CLI v0 is implemented and verified.
- Deck Workspace Mutation CLI v0 is implemented and verified.
- Deck Inspection CLI Polish v0 is implemented and verified.
- Deckbuilder Acceptance Checklist cleanup is complete.
- Category Metadata Mutation CLI v0 is implemented and verified.
- Entry Annotation CLI v0 is implemented and verified.
- Deck Workspace View Projection v0 is implemented and verified.
- Workspace View CLI v0 is implemented and verified.
- Card-Fact-Backed Workspace Projection v0 is implemented and verified.
- Color Identity Workspace Projection v0 is implemented and verified.
- Workspace View Fixture Smoke v0 is implemented and verified.
- Workspace Projection Contract Docs v0 is implemented and verified.
- See The Deck v0 is implemented and verified.
- See The Deck v0 Visual Review Checkpoint is implemented and verified.

## Completed Catchup Repairs

- Step 1: Current docs/status/handoff repair.
- Step 2: Relationship Smoke Repair v0.
  - Removed hidden relationship injection from the smoke helper.
  - Moved the discard observer behavior into explicit fixture-level profile atoms and a declared source-target pair.
  - Added a regression test proving undeclared event pairs are not invented.
- Step 3: Relationship Contract Hardening Patch.
  - Tightened confidence-band validation so bools and floats are rejected.
  - Added missing negative tests for empty relationship evidence, invalid edge evidence objects, invalid atom objects, and non-string Oracle IDs.
  - Updated bounded atom extraction docs to include the current Treasure-sacrifice rule.
- Step 4: Workspace/Card Lookup Integrity Patch.
  - Rejected invalid supplied workspace entry IDs before entry creation.
  - Aligned no-Oracle card fact identity with `CardCatalog` by using normalized canonical card names before printing IDs.
  - Added independent expected-output assertions for inspection source unification.
- Step 5: Scryfall Index Portability and Atomicity Patch.
  - Added moved-repo fallback for stale Scryfall manifest `local_path` values.
  - Preferred raw-root resolution before cwd fallback for relative paths.
  - Wrote the next index manifest before replacing live outputs and restored prior DB/manifest on handled replacement failure.
- Step 6: Visual Compare Direction Decision.
  - Kept baseline card comparison visual and direction-free.
  - Defined optional `Inspect interaction` as explicit source-to-target inspection.
  - Required reverse inspection to be a separate user action, not automatic.

## Near Term

- Find And Add Cards v0.
- Keep deck inspection reports factual and deterministic.
- Keep unsupported Scryfall syntax explicit instead of guessed.
- Decide when Deck Role Summary v0 is safe to start, because it introduces deck-level role counting.
- Define fixture expectations before broadening any relationship or analysis behavior.

## Later

- Expand local Scryfall syntax only when explicitly prioritized.
- Add Commander Profile v0.
- Add category creation, rename, and reorder helpers after projection behavior stays stable.
- Add Card Seat / Role Report v0 after deck-level role-counting approval.
- Add Recommendation Explanation v0 after factual reports and role/context boundaries stabilize.
- Build deeper deterministic structural audit passes.
- Define the deck scoring rubric with human review.
- Add report generation after audit output stabilizes.
- Plan the luxury UI only after backend behavior is reliable.

## Deferred By Doctrine

- Package detection.
- Synergy scoring.
- Commander analysis.
- Recommendations.
- Candidate search.
- Add/cut scoring.
- App UI.
- Live APIs or hosted dependencies.

# Current Deckbuilder UI User Review

Date: 2026-07-24

## Review Inputs

- Current implemented deckbuilder UI source in `apps/deckbuilder-ui/`.
- Current UI rubric in `docs/product/deckbuilder/USER_REVIEW_RUBRIC.md`.
- Existing human feedback: add-card workflow is responsive and the collapsible panel concept is good; current visual treatment is rough test-flight quality and not final.

This report did not replace a live human browser pass. It is a structured reviewer pass to guide the next human checkpoint.

## User Reviewer Report

Section reviewed: current fixture-backed deckbuilder screen, including grouped/table deck view, current-deck filter, collapsible add-card panel, factual card details panel, and mechanical validation sidebar.

Assumed user goal: open a deck workspace, understand the current deck contents, add a card from local fixture search, inspect selected card facts, and notice basic mechanical deck-shape warnings without being pulled into recommendations or scoring.

Overall rating: 6/10

Clarity rating: 7/10

Visual calm rating: 5/10

Deckbuilder usefulness: 7/10

Hierarchy rating: 6/10

Clutter risk: Medium

## Pass

- The deck remains the primary workspace.
- The add-card surface is explicitly collapsible and does not replace the deck view.
- Current-deck filtering and global local-card search are separated.
- Details are factual and local-only, avoiding price, legality, power, recommendation, and ranking claims.
- Mechanical validation is short and actionable instead of becoming a full dashboard.
- Controls shown on the screen map to working fixture-backed behavior.
- Default UI avoids raw debug data and backend fact-coverage plumbing.

## Needs Polish

- The screen still feels like a functional test flight rather than the final calm workbench.
- Details, validation, and deck snapshot compete for attention in the right-side/supporting area.
- Button styling and panel hierarchy need a more polished visual system before larger UI surfaces are added.
- The mechanical validation panel is useful, but its language should eventually feel less developer-like and more deckbuilder-native.
- Card rows need a future visual treatment that makes card identity easier to scan without adding card-image clutter too early.

## Blocking Concerns

- No blocking concerns for backend or fixture-backed UI continuation.
- Human visual review is still required before treating the current visual direction as accepted.
- Do not build broad new UI surfaces on this exact styling without a polish checkpoint.

## Suggested Next Visual Change

- Consolidate the supporting right-side area into a calmer "Deck context" region that can progressively disclose snapshot, validation, and selected-card details rather than showing too many support panels at equal weight.

## Do Not Change

- Keep the collapsible add-card panel concept.
- Keep current-deck filter separate from global/local card search.
- Keep factual details local-only until richer local data is explicitly wired.
- Keep validation mechanical and short.
- Keep recommendations, scoring, power claims, pricing, legality, and strategic judgment out of the default UI.

## Human Validation Needed

Yes. Final UI taste approval remains with the user.

## Human Browser Pass Addendum

Date: 2026-07-24

Reviewer: user

### Ratings And Notes

1. Overall feel: functions feel generally right, but organization is strange and underexpressed. Some of this may resolve naturally as completion grows, but it should not be ignored.
2. Clarity: the top header communicates deck name, card count, format, maybeboard quantity, and save state. Deck snapshot is self-explanatory but contributes to organization issues.
3. Visual calm: the UI is calm in broad direction, but the current visual quality is not acceptable as final and needs a dedicated polish pass.
4. Deckbuilder usefulness: visible deck review and add-card behavior are present and useful, but remove-card behavior is not visible yet.
5. Supporting area: deck snapshot should move lower than the primary deck view, closer to Archidekt-style stats placement, to leave more room for card image stacks and grouped card presentation.

### Specific Corrections

- The `Groups` field in Deck Snapshot is unclear and should not be exposed without a clearer basis.
- `Names resolved` should not appear as a default mechanical check.
- Singleton status should not be a normal visible checklist item. Duplicate non-basic cards should produce targeted visual warnings on the affected cards instead.
- Duplicate exceptions exist, such as cards that allow multiple copies; future duplicate validation must account for local card rules/evidence before warning.
- Card details do not need to show `Zone` in the basic details panel.
- Maybeboard should be optionally visible and collapsed by default.
- Group/Table switching works, but later visual options could use a more satisfying sliding segmented control or a dropdown when more modes exist.
- Add-card behavior works and count updates immediately.
- Full-cardpool search should not perform noisy instant 1-character broad lookup. Single-letter input such as `r` should not explode into broad result lists across the full database.

### Revised Reviewer Outcome

Overall rating: 5/10

Clarity rating: 6/10

Visual calm rating: 4/10

Deckbuilder usefulness: 7/10

Hierarchy rating: 5/10

Clutter risk: Medium

### Revised Next Visual Change

Prioritize a small deck-context consolidation and polish pass before larger visible workflow work. Move snapshot/stats-style information out of the cramped right-side deck area, collapse maybeboard by default, remove default `Names resolved` and singleton checklist display, and reserve duplicate warnings for targeted card-level alerts.

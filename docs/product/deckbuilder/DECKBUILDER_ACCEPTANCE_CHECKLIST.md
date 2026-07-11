# Deckbuilder Acceptance Checklist

## Planning Readiness

- [ ] Stale phase language is removed from core docs.
- [ ] `README.md` exists at the repository root.
- [ ] `.gitattributes` exists at the repository root.
- [ ] Deckbuilder Foundation v0 docs exist.
- [ ] The main deckbuilder workspace is clearly the product center.
- [ ] Search, stats, import/export, and reports are described as supporting surfaces.
- [ ] Implementation boundaries are explicit.
- [ ] No application UI code has been added for this planning pass.
- [ ] No new frontend dependencies have been installed for this planning pass.
- [ ] Open questions are listed before implementation starts.

## Required V0 Docs

- [ ] `DECKBUILDER_FOUNDATION_V0.md`
- [ ] `MAIN_SCREEN_V0.md`
- [ ] `DECK_WORKSPACE_MODEL_V0.md`
- [ ] `DECKBUILDER_INTERACTIONS_V0.md`
- [ ] `DECKBUILDER_ACCEPTANCE_CHECKLIST.md`
- [ ] `OPEN_QUESTIONS.md`

## Before Implementation

- [x] Decide whether Deck Skeleton Report v0 or Deckbuilder Foundation implementation comes first.
- [x] Define any required saved deck file format before persistence work.
- [x] Confirm the first implementation target and verification command.

## Deck Workspace Model V0

- [x] Native `.mtgwdeck.json` format is documented.
- [x] Workspace and entry model objects exist.
- [x] Native JSON save/load helpers exist.
- [x] Malformed workspace validation errors are user-facing.
- [x] Tiny workspace fixtures exist.
- [x] Unit tests cover round-trip preservation and malformed input.

## Deck Workspace Mutations V0

- [x] Mutation behavior is documented.
- [x] Entry id generation is documented and tested.
- [x] Add/remove helpers exist.
- [x] Increase/decrease helpers exist.
- [x] Zone move and set-commander helpers exist.
- [x] Category, tag, and note update helpers exist.
- [x] Duplicate add policy is documented and tested.
- [x] Mutations update `updated_at`.
- [x] Mutations mark `saved_state.is_dirty` true.
- [x] Commander moves set quantity to `1`.
- [x] Native workspace round trip still works after mutations.
- [x] No UI code or frontend dependency changes were added for this slice.

Deferred beyond this slice:

- Full Commander legality validation.
- Deck Workspace Mutations CLI commands.

## Deck Workspace Import/Export V0

- [x] Plain text import/export behavior is documented.
- [x] `1x Card Name` import lines are supported.
- [x] `1 Card Name` import lines are supported.
- [x] Bare `Card Name` import lines are supported.
- [x] Commander, mainboard, and maybeboard headers are supported.
- [x] `Sideboard` safely imports to maybeboard.
- [x] Conservative category headers can become entry categories.
- [x] Unresolved cards are preserved.
- [x] Export emits clean `1x Card Name` text.
- [x] Export falls back to `input_name` for unresolved cards.
- [x] Successful native saves mark workspaces clean.
- [x] No UI code, frontend dependency changes, live APIs, reports, or recommendation logic were added for this slice.

Deferred beyond this slice:

- Minimal Deck Workspace CLI commands.
- Full external deckbuilder format support.
- Perfect reconstruction of original comments or every source header.
- Full Commander legality validation.

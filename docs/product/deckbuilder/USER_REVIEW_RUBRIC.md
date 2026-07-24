# User Review Rubric

## Purpose

Use this rubric to review completed MTG Workbench UI or visualization slices from a user perspective before building more features on top of them. It is a structured review aid, not final approval.

## Review Lens

The reviewer should ask whether the section helps a capable MTG player or newer deckbuilder understand and act without feeling buried. The deckbuilder workspace should remain the center of the experience.

## Rating Categories

Rate each category from 1 to 10.

- Overall: how ready the section feels as a foundation for the next slice.
- Clarity: whether the user can tell what the section is for.
- Visual calm: whether spacing, density, and contrast feel readable instead of noisy.
- Deckbuilder usefulness: whether the section supports deck editing or understanding.
- Hierarchy: whether primary actions and information are easy to find.

## Clutter Risk

Use Low, Medium, or High.

- Low: the section is focused and easy to scan.
- Medium: the section works, but extra labels, panels, or repeated data compete for attention.
- High: the section feels like a feature collage or debug dashboard.

## Pass Criteria

A section passes user review when:

- the main user goal is obvious
- the deck remains the primary workspace
- controls map to working behavior
- labels are short and specific
- warnings are actionable
- advanced/internal data is hidden or absent
- layout remains readable on expected viewport sizes

## Common Polish Notes

Record these as polish unless they block comprehension:

- button style is not final
- spacing feels slightly dense
- panel order could be improved
- copy could be warmer or shorter
- icon choice could be clearer
- visual accent is too loud

## Blocking Concerns

Treat these as blockers before building on the slice:

- inactive or misleading controls
- text overflow or overlap
- user cannot identify the primary action
- warnings make claims unsupported by local data
- debug/internal data is visible by default
- UI implies recommendations, scoring, legality, pricing, or power-level judgment outside approved scope
- a dense dashboard distracts from the deckbuilder workflow

## Human Validation

The reviewer can flag risks and suggest changes, but final visual/taste approval remains with the user. For MTG Workbench, user review should augment human validation, not replace it.

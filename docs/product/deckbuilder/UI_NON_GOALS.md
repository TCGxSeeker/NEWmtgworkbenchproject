# UI Non-Goals

## Product Surface Guardrails

- Do not clone Archidekt, Deckcheck, or Scryfall styling.
- Do not make the main deckbuilder screen search-first.
- Do not show every metric at once.
- Do not create a dense feature-collage dashboard.
- Do not use warnings as decoration.
- Do not let charts crowd the deck workspace.
- Do not use a dense sci-fi control panel aesthetic unless explicitly requested.
- Do not carry forward rough proof-of-function styling as final visual direction.
- Do not treat an accepted interaction concept as approval of its current visual polish.
- Do not import visual-reference domain content, card names, product names, file paths, or service behavior into MTG Workbench.
- Do not copy hosted deck visibility or social/profile states from external deckbuilder references into the local-first v0 product.
- Do not add ad slots, sponsored panels, or external recommendation tabs as default product surfaces.
- Do not add optimizer-style controls before local deterministic rules and human validation zones are defined.
- Do not show live price, legality, rank, salt-score, printing, or external-link claims in card details without verified local data or a separate approved external-link policy.
- Do not treat deck snapshot, mechanical checks, or card details as equal-weight panels competing with the main card workspace.
- Do not show successful background checks such as resolved names or no duplicate issues as default UI checklist rows.
- Do not show broad full-cardpool results for single-character free-text input.

## Preferred Direction

- Progressive disclosure.
- Clean dashboard cards.
- Clear page hierarchy.
- Fewer visible panels per screen.
- Strong whitespace.
- Readable typography.
- Restrained accent colors.
- Warnings surfaced only when actionable.
- Charts only when they explain something.
- Collapsible/drawer-style work surfaces are acceptable when they keep the main deck view centered.
- The add-card workflow may remain a collapsible panel concept, but the final styling should feel more modern and polished than the current fixture-backed test screen.
- Future dark UI passes may borrow the feel of polished panels, soft borders, smooth buttons, and calm status banners from approved visual references without cloning them.
- Search/add can use focused overlays or expanded panels, but it should remain a supporting workflow around the deck workspace.
- Stats and probability tools may live below the deck or in a tab, but they should support deck understanding instead of becoming the main dashboard.
- Card details should help the user understand the selected card without turning into a marketplace, legality oracle, recommendation panel, or debug report.
- Snapshot/stats-style information should generally sit below the main deck view, in a tab, or in a calmer progressive-disclosure context area so card stacks and grouped deck presentation have room.
- Mechanical warnings should appear only when actionable. Duplicate non-basic warnings should target the affected card entries rather than living as a permanent checklist item.
- Maybeboard should be optionally visible and collapsed by default.

The user should feel guided through deck understanding, not buried under widgets.

# Card Identity And Printing Model

## Source And Placement

Sources:

- [EDHREC at Home: Card Data](https://gamesfreaksa.info/blog/edhrec-at-home-pt-3)
- [EDHREC at Home: Talking to Scryfall](https://gamesfreaksa.info/blog/edhrec-at-home-pt-4)

The requested `docs/product/shared_ui/reference/` folder does not exist yet, so this note is placed in the closest existing product reference folder: `docs/product/deckbuilder/reference/`.

## Reference Lessons

Scryfall's Card Object can be treated as the source substrate for card data. It is comprehensive enough to seed local card data, but MTG Workbench should derive smaller internal card records instead of passing full raw Scryfall payloads through parser, report, search, UI, and future collection workflows.

Oracle ID should represent the canonical game object. This is the identity deck analysis, legality checks, role counts, and future recommendation candidate pools should use when the printing does not matter.

Scryfall ID should represent a specific physical or digital printing. A single game object can have many Scryfall IDs, and those printings can differ by art, set, language, finish, collector number, and price.

A representative Scryfall ID can provide the default display printing for a card. Later, a selected Scryfall ID can support user-chosen printing, foil status, collection identity, and price differences without changing the underlying Oracle-level card identity.

Color identity should be stored in a structured comparable form. The article uses flag-style values so a card is legal in a deck when all card color bits are contained within the deck or commander color identity. MTG Workbench already indexes color identity masks for local Scryfall search, but the long-term internal model still needs an explicit contract.

Card types should also be stored in a structured form suitable for grouping, filtering, reports, and UI view modes. Raw type lines are still useful for display, but structured type values are better for deck statistics and deckbuilder grouping.

Commander legality has two related layers:

- Format legality from local Scryfall legality snapshots, such as `legal:commander`.
- Deck color legality, where a card's color identity must be contained within the deck or commander color identity.

These notes support deckbuilder modeling, local search filtering, card details, printing management, future collection features, and price-aware display. They do not define recommendation-engine behavior.

## Scryfall Boundary Lessons

The Scryfall API and bulk files should be treated as external source formats, not as MTG Workbench's internal model. A Scryfall-facing object can mirror the raw payload, while the Workbench model should keep only the fields needed for deck import, deck analysis, local search, card details, printing selection, and collection tracking.

Scryfall bulk data comes in multiple useful scopes:

- Oracle Cards: one row per Oracle ID, best for game-object analysis.
- Default Cards: a representative display printing for each game object.
- All Cards: print-level records for set, rarity, language, finish, collector number, and price differences.
- Rulings and tags: supporting lookup data that should remain separate from core deck identity.

MTG Workbench should keep that split visible. Oracle-level analysis should not accidentally become print-aware, and print-aware features should not overwrite canonical Oracle-level identity.

## Search And Printing Implications

Current Search-2 support is useful but should be interpreted carefully:

- `o:`, `t:`, `otag:`, `ci:`/`id:`, `mv:`/`cmc:`, `legal:commander`, and `is:commander` are naturally Oracle-level filters.
- `set:<code>`, `r:<rarity>`, and `usd<=N` are print-sensitive concepts.

Until MTG Workbench implements print-aware search, `set`, `rarity`, and price filters should be treated as representative or indexed snapshot fields, not as exhaustive "any printing" answers. Future print-aware search should query print records, map matching Scryfall IDs back to Oracle IDs, and preserve the selected printing when the user is browsing, pricing, or managing a collection.

## Internal Model Implications

Future card model planning should distinguish:

- `oracle_id`: canonical game object identity.
- `representative_scryfall_id`: default display printing.
- `selected_scryfall_id`: user-selected printing when collection or display preferences matter.
- `color_identity`: structured comparable value.
- `card_types`: structured grouping/filtering value.
- `type_line`: raw display text.
- `oracle_text`: current rules text used for gameplay meaning.
- `mana_cost` and `mana_value`: report and filtering fields.

## Non-Decisions

- Do not change schemas from this note alone.
- Do not require the UI to expose printing selection in the first deckbuilder version.
- Do not expand this into recommendation scoring or card evaluation logic.

## Open Question

Should MTG Workbench represent color identity and card types as strings, normalized arrays, bitmasks, or a hybrid model?

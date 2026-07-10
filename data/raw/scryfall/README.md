# Scryfall Bulk Snapshots

This folder stores manually fetched Scryfall bulk-data snapshots as local source data.

Large payloads in this tree are ignored by Git. Keep only small documentation and manifest files tracked.

Use these snapshots as future local ingestion sources only. Runtime parser, normalizer, audit, and recommendation behavior must not call Scryfall directly unless a future ingestion workflow is explicitly approved.

## Folders

- `bulk-data-index/`: Raw response from `https://api.scryfall.com/bulk-data`.
- `oracle_cards/`: One card per Oracle ID.
- `unique_artwork/`: Cards selected for unique artwork/image coverage.
- `default_cards/`: English/default card objects.
- `all_cards/`: Every card object in every language.
- `rulings/`: Rulings keyed by Oracle IDs.
- `art_tags/`: Tagger art tags.
- `oracle_tags/`: Tagger Oracle text tags.

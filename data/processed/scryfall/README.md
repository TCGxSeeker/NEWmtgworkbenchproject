# Processed Scryfall Indexes

This directory is for generated local search indexes derived from `data/raw/scryfall/`.

The main Phase Index-1 artifact is:

```powershell
$env:PYTHONPATH='src'
python -m mtg_workbench.cli index-scryfall --raw-dir data/raw/scryfall --output data/processed/scryfall/cards.sqlite
```

`cards.sqlite` is ignored by Git because it can be regenerated from local raw snapshots. `index_manifest.json` records source paths, source timestamps, row counts, and whether SQLite FTS was available.

Indexing must not call Scryfall or any other live service.

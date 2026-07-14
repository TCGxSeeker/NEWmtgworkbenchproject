# Atomic Local Persistence v0

## Status

Implemented and verified.

## Purpose

Protect local workspace files and the local Scryfall SQLite index from destructive partial writes.

## Previous workspace-save behavior

Workspace saves:

- marked the in-memory workspace clean before persistence succeeded
- wrote directly to the destination path
- could leave the workspace claiming to be saved after a failed write
- did not preserve the prior file through an atomic replacement boundary

## Implemented workspace-save behavior

Workspace saves now:

1. serialize a clean-state payload without mutating the live workspace
2. write that payload to a temporary sibling file
3. atomically replace the destination
4. mark the live workspace clean only after replacement succeeds
5. remove the temporary file when persistence fails

A failed save therefore preserves:

- the previous destination file
- the workspace dirty state

## Previous Scryfall rebuild behavior

The index rebuild removed the existing live SQLite database before the new temporary database completed successfully.

A failed rebuild could therefore destroy the last known-good index.

## Implemented Scryfall rebuild behavior

The index builder now:

1. removes only stale temporary output
2. leaves the live database untouched during construction
3. builds and closes the complete temporary database
4. replaces the live database only after the rebuild succeeds
5. removes temporary output after a failure

A failed rebuild therefore preserves the existing index.

## Non-goals

This slice does not add:

- backup versioning
- recovery history
- cloud synchronization
- live APIs
- UI behavior
- schema changes
- strategy or recommendation behavior

## Verification

Added failure-path tests confirming:

- failed workspace replacement preserves the prior file
- failed workspace replacement preserves dirty state
- failed workspace replacement removes temporary output
- failed Scryfall rebuild preserves the existing index
- failed Scryfall rebuild removes temporary output

The full test suite passes with 203 tests.

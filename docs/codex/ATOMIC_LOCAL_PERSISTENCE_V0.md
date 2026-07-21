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
4. writes the next index manifest to a temporary sibling file
5. backs up the previous database and manifest when they exist
6. replaces the live database and manifest only after both next outputs exist
7. restores the previous database and manifest when replacement fails
8. removes temporary and backup files after success or failure

A failed rebuild therefore preserves the existing index and index manifest during normal handled failures.

## Moved-repository source paths

Scryfall source manifests may contain `local_path` values from an older checkout location.

The indexer now resolves source files by checking:

1. the recorded path, when it still exists
2. the current raw root plus the source type and recorded filename
3. the current raw root plus the recorded filename

For relative paths, raw-root locations are preferred before cwd-based fallback. This keeps local snapshot rebuilds portable after moving the repository.

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
- failed Scryfall manifest replacement restores the previous index and manifest
- failed Scryfall rebuild removes temporary output
- stale absolute Scryfall source paths fall back to the current raw root

Run the current full unit suite from the repository root after changing this persistence behavior.

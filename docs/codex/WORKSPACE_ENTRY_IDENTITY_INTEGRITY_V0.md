# Workspace Entry Identity Integrity v0

## Status

Implemented and verified.

## Purpose

Deck-entry identity must be deterministic and unambiguous before relationships, packages, commander context, or recommendations can reference entries safely.

Every stored `entry_id` is therefore treated as a globally unique workspace identity key rather than a descriptive label.

## Contract

### Stored workspace identity

- Every `entry_id` must be a nonempty string.
- Every `entry_id` must be unique across:
  - `commanders`
  - `mainboard`
  - `maybeboard`
- Duplicate IDs inside one zone are invalid.
- Duplicate IDs across zones are invalid.
- Native workspace loading fails explicitly when duplicate IDs are present.

### Mutation behavior

- `None` means a new unique `entry_id` should be generated.
- Any caller-supplied `entry_id` must be a nonempty string after trimming.
- Non-string, blank, or whitespace-only supplied IDs are rejected before creating an entry.
- A caller-supplied `entry_id` may not reuse an ID owned by another stored entry.
- A materially different entry with an existing ID is rejected.
- An incoming ID already owned by another entry may not be silently discarded during a merge.
- Generated IDs retry until an unused ID is produced.

### Merge behavior

Materially identical entries may still merge according to the existing mutation contract.

During a legitimate merge:

- the existing stored entry remains authoritative,
- its existing `entry_id` is preserved,
- quantities and supported metadata merge normally,
- an unused incoming ID is not stored.

This preserves convenient duplicate-card addition without creating multiple stored entries that share one identity.

### Defensive malformed-state behavior

Direct Python mutation can bypass serialization and normal mutation APIs.

Identity-sensitive helpers therefore fail explicitly when malformed in-memory state contains multiple entries with the same ID.

The behavior is:

- zero matches: return `None` or raise the existing not-found error,
- one match: return or mutate that entry,
- multiple matches: raise `WorkspaceMutationError`.

No lookup or removal operation may silently choose the first duplicate.

## Verification

Regression coverage includes:

- duplicate IDs inside one zone,
- duplicate IDs across zones,
- supplied IDs owned by different entries,
- occupied incoming IDs during otherwise valid merges,
- preservation of the existing ID during legitimate merges,
- generated-ID collision retry,
- ambiguous in-memory lookup rejection,
- ambiguous in-memory removal rejection,
- native workspace round-trip behavior.
- non-string supplied entry IDs,
- blank supplied entry IDs,
- trimming supplied entry IDs.

## Architectural Consequence

Future relationship edges may safely identify deck entries by `entry_id`, provided workspaces enter the system through validated loading or supported mutation paths.

This slice does not implement card relationships. It only establishes the identity invariant required by them.

## Doctrine

> Understand facts and relationships first; classify and judge later.

Reliable relationships require reliable identity.

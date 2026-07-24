import type {
  WorkspaceViewEntry,
  WorkspaceViewProjection,
} from './workspaceProjection'

type NativeDeckZone = WorkspaceViewEntry['zone']

type NativeDeckEntry = {
  entry_id: string
  quantity: number
  input_name: string
  display_name: string | null
  oracle_id?: string | null
  selected_printing_id?: string | null
  zone: NativeDeckZone
  categories: string[]
  tags: string[]
  imported_category?: string | null
  normalized_category?: string | null
  generic_category_hint?: string | null
  deck_specific_primary_role?: string | null
  secondary_tags?: string[]
  category_origin?: string | null
  notes?: string | null
  pinned?: boolean
  foil?: boolean
  date_added?: string | null
  is_unresolved: boolean
}

type NativeDeckWorkspace = {
  schema_version: number
  deck_id: string
  name: string
  format: string
  created_at?: string | null
  updated_at?: string | null
  tags: string[]
  notes?: string | null
  commanders: NativeDeckEntry[]
  mainboard: NativeDeckEntry[]
  maybeboard: NativeDeckEntry[]
  saved_state: {
    is_dirty?: boolean
    last_saved_at?: string | null
    [key: string]: unknown
  }
  metadata?: Record<string, unknown>
}

type PreviewFacts = {
  type_line?: string | null
  type_labels?: string[]
  mana_value?: number | null
  colors?: string[] | null
  color_identity?: string[] | null
}

export type DeckWorkspaceState = {
  deckId: string
  deckName: string
  format: string
  createdAt: string | null
  updatedAt: string | null
  tags: string[]
  notes: string | null
  metadata: Record<string, unknown>
  savedState: {
    isDirty: boolean
    lastSavedAt: string | null
  }
  sourceLabel: string
  entries: WorkspaceViewEntry[]
}

export type DeckLibraryItem = {
  deckId: string
  name: string
  format: string
  activeQuantity: number
  commanderCount: number
  maybeboardQuantity: number
  commanderName: string
  updatedAt: string | null
  isDirty: boolean
}

export class WorkspaceFileError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'WorkspaceFileError'
  }
}

export function deckStateFromProjection(
  projection: WorkspaceViewProjection,
  sourceLabel = 'Bundled fixture',
): DeckWorkspaceState {
  return {
    deckId: projection.deck_id,
    deckName: projection.deck_name,
    format: 'commander',
    createdAt: null,
    updatedAt: null,
    tags: ['fixture'],
    notes: null,
    metadata: {
      source: 'workspace_view_projection',
    },
    savedState: {
      isDirty: false,
      lastSavedAt: null,
    },
    sourceLabel,
    entries: uniqueProjectionEntries(projection.groups.flatMap((group) => group.entries)),
  }
}

export function createEmptyDeckState(
  name: string,
  format: string,
  now = new Date().toISOString(),
): DeckWorkspaceState {
  return {
    deckId: `deck-${slugify(name)}-${Date.now().toString(36)}`,
    deckName: name,
    format,
    createdAt: now,
    updatedAt: now,
    tags: [],
    notes: null,
    metadata: {
      created_by: 'deckbuilder-ui-v0',
    },
    savedState: {
      isDirty: true,
      lastSavedAt: null,
    },
    sourceLabel: 'New local workspace',
    entries: [],
  }
}

export function markDeckDirty(
  state: DeckWorkspaceState,
  entries: WorkspaceViewEntry[],
): DeckWorkspaceState {
  return {
    ...state,
    entries,
    updatedAt: new Date().toISOString(),
    savedState: {
      ...state.savedState,
      isDirty: true,
    },
  }
}

export function markDeckClean(
  state: DeckWorkspaceState,
  savedAt: string,
): DeckWorkspaceState {
  return {
    ...state,
    updatedAt: savedAt,
    savedState: {
      ...state.savedState,
      isDirty: false,
      lastSavedAt: savedAt,
    },
  }
}

export function parseNativeWorkspaceText(
  text: string,
  sourceLabel: string,
): DeckWorkspaceState {
  let payload: unknown
  try {
    payload = JSON.parse(text)
  } catch (error) {
    throw new WorkspaceFileError(
      error instanceof Error ? `Malformed workspace JSON: ${error.message}` : 'Malformed workspace JSON.',
    )
  }

  const errors = validateNativeWorkspace(payload)
  if (errors.length > 0) {
    throw new WorkspaceFileError(errors.join(' '))
  }

  const workspace = payload as NativeDeckWorkspace
  const previewFacts = readPreviewFacts(workspace.metadata)
  return {
    deckId: workspace.deck_id,
    deckName: workspace.name,
    format: workspace.format,
    createdAt: workspace.created_at ?? null,
    updatedAt: workspace.updated_at ?? null,
    tags: [...workspace.tags],
    notes: workspace.notes ?? null,
    metadata: { ...(workspace.metadata ?? {}) },
    savedState: {
      isDirty: Boolean(workspace.saved_state.is_dirty),
      lastSavedAt: stringOrNull(workspace.saved_state.last_saved_at),
    },
    sourceLabel,
    entries: [
      ...workspace.commanders.map((entry) => nativeEntryToViewEntry(entry, 'commander', previewFacts)),
      ...workspace.mainboard.map((entry) => nativeEntryToViewEntry(entry, 'mainboard', previewFacts)),
      ...workspace.maybeboard.map((entry) => nativeEntryToViewEntry(entry, 'maybeboard', previewFacts)),
    ],
  }
}

export function serializeDeckState(
  state: DeckWorkspaceState,
  savedAt: string,
): string {
  const payload: NativeDeckWorkspace = {
    schema_version: 1,
    deck_id: state.deckId,
    name: state.deckName,
    format: state.format,
    created_at: state.createdAt,
    updated_at: savedAt,
    tags: [...state.tags],
    notes: state.notes,
    commanders: state.entries
      .filter((entry) => entry.zone === 'commander')
      .map(viewEntryToNativeEntry),
    mainboard: state.entries
      .filter((entry) => entry.zone === 'mainboard')
      .map(viewEntryToNativeEntry),
    maybeboard: state.entries
      .filter((entry) => entry.zone === 'maybeboard')
      .map(viewEntryToNativeEntry),
    saved_state: {
      is_dirty: false,
      last_saved_at: savedAt,
    },
    metadata: {
      ...state.metadata,
      ui_preview_facts: buildPreviewFacts(state.entries),
    },
  }

  return `${JSON.stringify(payload, null, 2)}\n`
}

export function deckStateToLibraryItem(
  state: DeckWorkspaceState,
): DeckLibraryItem {
  const activeEntries = state.entries.filter((entry) => entry.zone !== 'maybeboard')
  const commanderEntries = state.entries.filter((entry) => entry.zone === 'commander')
  const maybeboardEntries = state.entries.filter((entry) => entry.zone === 'maybeboard')
  const commanderName = commanderEntries[0]?.card_name ?? 'No commander'

  return {
    deckId: state.deckId,
    name: state.deckName,
    format: state.format,
    activeQuantity: activeEntries.reduce((total, entry) => total + entry.quantity, 0),
    commanderCount: commanderEntries.reduce((total, entry) => total + entry.quantity, 0),
    maybeboardQuantity: maybeboardEntries.reduce((total, entry) => total + entry.quantity, 0),
    commanderName,
    updatedAt: state.updatedAt,
    isDirty: state.savedState.isDirty,
  }
}

export function upsertLibraryItem(
  items: DeckLibraryItem[],
  item: DeckLibraryItem,
) {
  const existingIndex = items.findIndex((existing) => existing.deckId === item.deckId)
  if (existingIndex === -1) {
    return [item, ...items]
  }

  return items.map((existing, index) => (index === existingIndex ? item : existing))
}

export function workspaceDownloadName(state: DeckWorkspaceState) {
  return `${slugify(state.deckName) || 'untitled-deck'}.mtgwdeck.json`
}

function validateNativeWorkspace(payload: unknown) {
  const errors: string[] = []
  if (!isRecord(payload)) {
    return ['Workspace JSON must be an object.']
  }

  for (const fieldName of [
    'schema_version',
    'deck_id',
    'name',
    'format',
    'tags',
    'commanders',
    'mainboard',
    'maybeboard',
    'saved_state',
  ]) {
    if (!(fieldName in payload)) {
      errors.push(`Missing required workspace field: ${fieldName}.`)
    }
  }

  if ('schema_version' in payload && payload.schema_version !== 1) {
    errors.push('Workspace schema_version must be 1.')
  }
  checkString(errors, payload, 'deck_id')
  checkString(errors, payload, 'name')
  checkString(errors, payload, 'format')
  checkStringList(errors, payload, 'tags')
  checkEntrySection(errors, payload, 'commanders', 'commander')
  checkEntrySection(errors, payload, 'mainboard', 'mainboard')
  checkEntrySection(errors, payload, 'maybeboard', 'maybeboard')
  if ('saved_state' in payload && !isRecord(payload.saved_state)) {
    errors.push('Workspace saved_state must be an object.')
  }

  return errors
}

function checkEntrySection(
  errors: string[],
  payload: Record<string, unknown>,
  fieldName: string,
  expectedZone: NativeDeckZone,
) {
  if (!(fieldName in payload)) {
    return
  }
  const entries = payload[fieldName]
  if (!Array.isArray(entries)) {
    errors.push(`Workspace ${fieldName} must be a list.`)
    return
  }

  entries.forEach((entry, index) => {
    const location = `${fieldName}[${index}]`
    if (!isRecord(entry)) {
      errors.push(`${location} must be an object.`)
      return
    }

    for (const entryField of [
      'entry_id',
      'quantity',
      'input_name',
      'display_name',
      'zone',
      'categories',
      'tags',
      'is_unresolved',
    ]) {
      if (!(entryField in entry)) {
        errors.push(`Missing required ${location} field: ${entryField}.`)
      }
    }

    checkString(errors, entry, 'entry_id', location)
    checkString(errors, entry, 'input_name', location)
    if ('display_name' in entry && entry.display_name !== null && typeof entry.display_name !== 'string') {
      errors.push(`${location}.display_name must be a string or null.`)
    }
    checkStringList(errors, entry, 'categories', location)
    checkStringList(errors, entry, 'tags', location)
    if (entry.zone !== expectedZone) {
      errors.push(`${location}.zone must be ${expectedZone}.`)
    }
    if (!Number.isInteger(entry.quantity) || Number(entry.quantity) < 1) {
      errors.push(`${location}.quantity must be a positive integer.`)
    }
    if (typeof entry.is_unresolved !== 'boolean') {
      errors.push(`${location}.is_unresolved must be a boolean.`)
    }
  })
}

function checkString(
  errors: string[],
  payload: Record<string, unknown>,
  fieldName: string,
  location = 'workspace',
) {
  if (!(fieldName in payload)) {
    return
  }
  if (typeof payload[fieldName] !== 'string' || !String(payload[fieldName]).trim()) {
    errors.push(`${location}.${fieldName} must be a non-empty string.`)
  }
}

function checkStringList(
  errors: string[],
  payload: Record<string, unknown>,
  fieldName: string,
  location = 'workspace',
) {
  if (!(fieldName in payload)) {
    return
  }
  const value = payload[fieldName]
  if (!Array.isArray(value) || value.some((item) => typeof item !== 'string')) {
    errors.push(`${location}.${fieldName} must be a list of strings.`)
  }
}

function nativeEntryToViewEntry(
  entry: NativeDeckEntry,
  zone: NativeDeckZone,
  previewFacts: Map<string, PreviewFacts>,
): WorkspaceViewEntry {
  const facts = previewFacts.get(entry.entry_id)
  const displayName = entry.display_name ?? entry.input_name
  return {
    entry_id: entry.entry_id,
    zone,
    quantity: entry.quantity,
    card_name: displayName,
    input_name: entry.input_name,
    display_name: entry.display_name,
    oracle_id: entry.oracle_id ?? null,
    selected_printing_id: entry.selected_printing_id ?? null,
    categories: [...entry.categories],
    tags: [...entry.tags],
    secondary_tags: [...(entry.secondary_tags ?? [])],
    imported_category: entry.imported_category ?? null,
    normalized_category: entry.normalized_category ?? null,
    generic_category_hint: entry.generic_category_hint ?? null,
    deck_specific_primary_role: entry.deck_specific_primary_role ?? null,
    category_origin: entry.category_origin ?? null,
    notes: entry.notes ?? null,
    pinned: Boolean(entry.pinned),
    foil: Boolean(entry.foil),
    date_added: entry.date_added ?? null,
    is_unresolved: entry.is_unresolved,
    card_fact_status: facts ? 'found' : 'not_requested',
    type_line: facts?.type_line ?? null,
    type_labels: facts?.type_labels ?? [],
    mana_value: facts?.mana_value ?? null,
    colors: facts?.colors ?? null,
    color_identity: facts?.color_identity ?? null,
  }
}

function viewEntryToNativeEntry(entry: WorkspaceViewEntry): NativeDeckEntry {
  return {
    entry_id: entry.entry_id,
    quantity: entry.quantity,
    input_name: entry.input_name,
    display_name: entry.display_name,
    oracle_id: entry.oracle_id ?? null,
    selected_printing_id: entry.selected_printing_id ?? null,
    zone: entry.zone,
    categories: [...entry.categories],
    tags: [...entry.tags],
    imported_category: entry.imported_category,
    normalized_category: entry.normalized_category,
    generic_category_hint: entry.generic_category_hint,
    deck_specific_primary_role: entry.deck_specific_primary_role ?? null,
    secondary_tags: [...entry.secondary_tags],
    category_origin: entry.category_origin ?? null,
    notes: entry.notes ?? null,
    pinned: Boolean(entry.pinned),
    foil: Boolean(entry.foil),
    date_added: entry.date_added ?? null,
    is_unresolved: entry.is_unresolved,
  }
}

function buildPreviewFacts(entries: WorkspaceViewEntry[]) {
  return Object.fromEntries(
    entries.map((entry) => [
      entry.entry_id,
      {
        type_line: entry.type_line,
        type_labels: entry.type_labels,
        mana_value: entry.mana_value,
        colors: entry.colors,
        color_identity: entry.color_identity,
      },
    ]),
  )
}

function readPreviewFacts(metadata: Record<string, unknown> | undefined) {
  const previewFacts = new Map<string, PreviewFacts>()
  const rawFacts = metadata?.ui_preview_facts
  if (!isRecord(rawFacts)) {
    return previewFacts
  }

  for (const [entryId, value] of Object.entries(rawFacts)) {
    if (!isRecord(value)) {
      continue
    }
    previewFacts.set(entryId, {
      type_line: optionalString(value.type_line),
      type_labels: stringArrayOrEmpty(value.type_labels),
      mana_value: optionalNumber(value.mana_value),
      colors: optionalStringArray(value.colors),
      color_identity: optionalStringArray(value.color_identity),
    })
  }

  return previewFacts
}

function uniqueProjectionEntries(entries: WorkspaceViewEntry[]) {
  const seen = new Set<string>()
  return entries.filter((entry) => {
    if (seen.has(entry.entry_id)) {
      return false
    }
    seen.add(entry.entry_id)
    return true
  })
}

function optionalString(value: unknown) {
  return typeof value === 'string' ? value : null
}

function optionalNumber(value: unknown) {
  return typeof value === 'number' && Number.isFinite(value) ? value : null
}

function optionalStringArray(value: unknown) {
  return Array.isArray(value) && value.every((item) => typeof item === 'string')
    ? [...value]
    : null
}

function stringArrayOrEmpty(value: unknown) {
  return optionalStringArray(value) ?? []
}

function stringOrNull(value: unknown) {
  return typeof value === 'string' ? value : null
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function slugify(value: string) {
  return value
    .trim()
    .toLocaleLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
}

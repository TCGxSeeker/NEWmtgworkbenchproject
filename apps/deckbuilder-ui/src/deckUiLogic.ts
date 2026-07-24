import type { CardSearchCandidate } from './cardSearchFixture'
import type { WorkspaceViewEntry, WorkspaceViewGroup } from './workspaceProjection'

export type ViewMode = 'grouped' | 'table'
export type DeckZone = WorkspaceViewEntry['zone']
export type AddZone = Extract<DeckZone, 'mainboard' | 'maybeboard'>
export type CardDetailsSource = 'deck' | 'search'

export type CardDetails = {
  source: CardDetailsSource
  card_name: string
  type_line: string
  mana_value: number | null
  color_identity: string[]
  quantity: number | null
  categories: string[]
  tags: string[]
  notes: string | null
}

export type ValidationItem = {
  id: string
  status: 'pass' | 'warning'
  label: string
  detail: string
}

export const ACTIVE_ZONES = new Set<DeckZone>(['commander', 'mainboard'])
export const ADD_ZONES: AddZone[] = ['mainboard', 'maybeboard']
export const MIN_FREE_TEXT_SEARCH_LENGTH = 2

const MAX_SEARCH_RESULTS = 6
const COMMANDER_ACTIVE_CARD_TARGET = 100
const GROUP_ORDER = [
  'Commander',
  'Lands',
  'Ramp',
  'Draw',
  'Selection',
  'Interaction',
  'Removal',
  'Protection',
  'Creatures',
  'Recursion',
  'Engine',
  'Payoff',
  'Wincon',
  'Maybeboard',
  'Uncategorized',
]

export function uniqueEntries(entries: WorkspaceViewEntry[]) {
  const seen = new Set<string>()
  return entries.filter((entry) => {
    if (seen.has(entry.entry_id)) {
      return false
    }
    seen.add(entry.entry_id)
    return true
  })
}

export function buildGroups(entries: WorkspaceViewEntry[]): WorkspaceViewGroup[] {
  const groupsByLabel = new Map<string, WorkspaceViewEntry[]>()
  for (const entry of entries) {
    const label = entry.categories[0] ?? 'Uncategorized'
    groupsByLabel.set(label, [...(groupsByLabel.get(label) ?? []), entry])
  }

  return Array.from(groupsByLabel.entries())
    .sort(([left], [right]) => compareGroupLabels(left, right))
    .map(([label, groupEntries]) => {
      const sortedEntries = [...groupEntries].sort(compareEntriesForDisplay)
      return {
        group_id: normalizeGroupId(label),
        label,
        entry_count: sortedEntries.length,
        quantity_total: sortedEntries.reduce((total, entry) => total + entry.quantity, 0),
        entries: sortedEntries,
      }
    })
}

export function cardCandidateToEntry(
  candidate: CardSearchCandidate,
  zone: AddZone,
  category: string,
  currentEntries: WorkspaceViewEntry[],
): WorkspaceViewEntry {
  const existingAddCount = currentEntries.filter((entry) =>
    entry.entry_id.startsWith(`added-${candidate.card_id}-${zone}`),
  ).length

  return {
    entry_id: `added-${candidate.card_id}-${zone}-${existingAddCount + 1}`,
    zone,
    quantity: 1,
    card_name: candidate.card_name,
    input_name: candidate.card_name,
    display_name: candidate.card_name,
    categories: [category],
    tags: candidate.tags,
    secondary_tags: [],
    imported_category: null,
    normalized_category: category === 'Maybeboard' ? null : category,
    generic_category_hint: category === 'Maybeboard' ? null : category,
    is_unresolved: false,
    card_fact_status: 'found',
    type_line: candidate.type_line,
    type_labels: deriveTypeLabels(candidate.type_line),
    mana_value: candidate.mana_value,
    colors: candidate.colors,
    color_identity: candidate.color_identity,
  }
}

export function categoryForCandidate(candidate: CardSearchCandidate, zone: AddZone) {
  if (zone === 'maybeboard') {
    return 'Maybeboard'
  }
  return candidate.categories[0] ?? 'Uncategorized'
}

export function entryMatchesFilter(entry: WorkspaceViewEntry, filterText: string) {
  const normalizedFilter = normalizeText(filterText)
  if (!normalizedFilter) {
    return true
  }

  const searchable = [
    entry.card_name,
    entry.input_name,
    entry.display_name ?? '',
    entry.type_line ?? '',
    entry.zone,
    ...entry.categories,
    ...entry.tags,
    ...entry.secondary_tags,
  ].join(' ')

  return normalizeText(searchable).includes(normalizedFilter)
}

export function searchLocalCards(query: string, candidates: CardSearchCandidate[]) {
  const normalizedQuery = normalizeText(query)
  if (!isCardSearchReady(query)) {
    return []
  }

  return candidates
    .filter((candidate) => candidateMatchesSearch(candidate, normalizedQuery))
    .sort((left, right) => left.card_name.localeCompare(right.card_name))
    .slice(0, MAX_SEARCH_RESULTS)
}

export function candidateQuantityInDeck(
  entries: WorkspaceViewEntry[],
  cardName: string,
) {
  return entries
    .filter((entry) => normalizeText(entry.card_name) === normalizeText(cardName))
    .reduce((total, entry) => total + entry.quantity, 0)
}

export function buildMechanicalValidationItems(
  entries: WorkspaceViewEntry[],
): ValidationItem[] {
  const activeEntries = entries.filter((entry) => ACTIVE_ZONES.has(entry.zone))
  const activeQuantity = activeEntries.reduce((total, entry) => total + entry.quantity, 0)
  const commanderEntries = entries.filter((entry) => entry.zone === 'commander')
  const unresolvedEntries = entries.filter((entry) => entry.is_unresolved)
  const duplicateNonBasics = duplicateNonBasicNames(activeEntries)
  const items: ValidationItem[] = []

  if (commanderEntries.length === 0) {
    items.push({
      id: 'commander-present',
      status: 'warning',
      label: 'Commander missing',
      detail: 'Set one commander before final deck review.',
    })
  }

  if (activeQuantity !== COMMANDER_ACTIVE_CARD_TARGET) {
    items.push({
      id: 'active-count',
      status: 'warning',
      label: 'Commander size',
      detail: `${activeQuantity} active cards; target is ${COMMANDER_ACTIVE_CARD_TARGET}.`,
    })
  }

  if (unresolvedEntries.length > 0) {
    items.push({
      id: 'unresolved-cards',
      status: 'warning',
      label: 'Unresolved cards',
      detail: `${unresolvedEntries.length} entry${unresolvedEntries.length === 1 ? '' : 'ies'} need name review.`,
    })
  }

  if (duplicateNonBasics.length > 0) {
    items.push({
      id: 'duplicate-non-basics',
      status: 'warning',
      label: 'Duplicate non-basics',
      detail: duplicateNonBasics.join(', '),
    })
  }

  return items
}

export function duplicateNonBasicNameSet(entries: WorkspaceViewEntry[]) {
  const duplicateNames = duplicateNonBasicNames(entries.filter((entry) => ACTIVE_ZONES.has(entry.zone)))
  return new Set(
    duplicateNames.map((label) => normalizeText(label.replace(/\sx\d+$/, ''))),
  )
}

export function isDuplicateNonBasicEntry(
  entry: WorkspaceViewEntry,
  duplicateNames: Set<string>,
) {
  return ACTIVE_ZONES.has(entry.zone) && duplicateNames.has(normalizeText(entry.card_name))
}

export function entryToDetails(entry: WorkspaceViewEntry): CardDetails {
  return {
    source: 'deck',
    card_name: entry.card_name,
    type_line: entry.type_line ?? 'Card',
    mana_value: entry.mana_value,
    color_identity: entry.color_identity ?? [],
    quantity: entry.quantity,
    categories: entry.categories,
    tags: [...entry.tags, ...entry.secondary_tags],
    notes: entry.notes ?? null,
  }
}

export function candidateToDetails(
  candidate: CardSearchCandidate,
  quantityInDeck: number,
): CardDetails {
  return {
    source: 'search',
    card_name: candidate.card_name,
    type_line: candidate.type_line,
    mana_value: candidate.mana_value,
    color_identity: candidate.color_identity,
    quantity: quantityInDeck > 0 ? quantityInDeck : null,
    categories: candidate.categories,
    tags: candidate.tags,
    notes: null,
  }
}

export function normalizeText(value: string) {
  return value.trim().toLocaleLowerCase().replace(/\s+/g, ' ')
}

export function isCardSearchReady(query: string) {
  return normalizeText(query).length >= MIN_FREE_TEXT_SEARCH_LENGTH
}

export function formatManaValue(value: number | null) {
  if (value === null) {
    return '-'
  }
  return Number.isInteger(value) ? `${value}` : value.toFixed(1)
}

export function formatColors(colors: string[] | null | undefined) {
  return !colors || colors.length === 0 ? 'Colorless' : colors.join('')
}

export function zoneLabel(zone: string) {
  if (zone === 'commander') {
    return 'Commander'
  }
  if (zone === 'maybeboard') {
    return 'Maybeboard'
  }
  return 'Mainboard'
}

function compareGroupLabels(left: string, right: string) {
  const leftIndex = GROUP_ORDER.indexOf(left)
  const rightIndex = GROUP_ORDER.indexOf(right)
  if (leftIndex !== -1 || rightIndex !== -1) {
    return (leftIndex === -1 ? GROUP_ORDER.length : leftIndex) -
      (rightIndex === -1 ? GROUP_ORDER.length : rightIndex)
  }
  return left.localeCompare(right)
}

function compareEntriesForDisplay(left: WorkspaceViewEntry, right: WorkspaceViewEntry) {
  const leftManaValue = left.mana_value ?? Number.POSITIVE_INFINITY
  const rightManaValue = right.mana_value ?? Number.POSITIVE_INFINITY
  if (leftManaValue !== rightManaValue) {
    return leftManaValue - rightManaValue
  }
  return left.card_name.localeCompare(right.card_name)
}

function candidateMatchesSearch(
  candidate: CardSearchCandidate,
  normalizedQuery: string,
) {
  const searchable = [
    candidate.card_name,
    candidate.type_line,
    ...candidate.categories,
    ...candidate.tags,
    ...candidate.colors,
    ...candidate.color_identity,
  ].join(' ')

  return normalizeText(searchable).includes(normalizedQuery)
}

function deriveTypeLabels(typeLine: string) {
  const supertypeText = typeLine.split(/[-\u2014]/)[0] ?? ''
  const labels = ['Artifact', 'Creature', 'Enchantment', 'Instant', 'Land', 'Planeswalker', 'Sorcery']
  return labels.filter((label) => supertypeText.includes(label))
}

function normalizeGroupId(label: string) {
  return normalizeText(label).replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') ||
    'uncategorized'
}

function duplicateNonBasicNames(entries: WorkspaceViewEntry[]) {
  const totalsByName = new Map<string, { displayName: string; quantity: number }>()

  for (const entry of entries) {
    if (isBasicLand(entry)) {
      continue
    }

    const key = normalizeText(entry.card_name)
    const existing = totalsByName.get(key)
    totalsByName.set(key, {
      displayName: existing?.displayName ?? entry.card_name,
      quantity: (existing?.quantity ?? 0) + entry.quantity,
    })
  }

  return Array.from(totalsByName.values())
    .filter((entry) => entry.quantity > 1)
    .map((entry) => `${entry.displayName} x${entry.quantity}`)
    .sort((left, right) => left.localeCompare(right))
}

function isBasicLand(entry: WorkspaceViewEntry) {
  const typeLine = normalizeText(entry.type_line ?? '')
  return typeLine.includes('basic land')
}

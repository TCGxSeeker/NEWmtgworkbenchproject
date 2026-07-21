import {
  BookOpen,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  CircleAlert,
  Filter,
  Info,
  Layers,
  Plus,
  Search,
  Table2,
  X,
} from 'lucide-react'
import { useMemo, useState } from 'react'
import './App.css'
import {
  type CardSearchCandidate,
  localCardSearchFixture,
} from './cardSearchFixture'
import {
  type WorkspaceViewEntry,
  type WorkspaceViewGroup,
  workspaceViewProjection,
} from './workspaceProjection'

type ViewMode = 'grouped' | 'table'
type DeckZone = WorkspaceViewEntry['zone']
type AddZone = Extract<DeckZone, 'mainboard' | 'maybeboard'>
type CardDetailsSource = 'deck' | 'search'

type CardDetails = {
  source: CardDetailsSource
  card_name: string
  type_line: string
  mana_value: number | null
  color_identity: string[]
  zone: DeckZone | null
  quantity: number | null
  categories: string[]
  tags: string[]
  notes: string | null
}

const ACTIVE_ZONES = new Set<DeckZone>(['commander', 'mainboard'])
const ADD_ZONES: AddZone[] = ['mainboard', 'maybeboard']
const MAX_SEARCH_RESULTS = 6
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

function App() {
  const [viewMode, setViewMode] = useState<ViewMode>('grouped')
  const [filterText, setFilterText] = useState('')
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(new Set())
  const [deckEntries, setDeckEntries] = useState<WorkspaceViewEntry[]>(() =>
    uniqueEntries(workspaceViewProjection.groups.flatMap((group) => group.entries)),
  )
  const [isAddOpen, setIsAddOpen] = useState(false)
  const [cardSearchText, setCardSearchText] = useState('')
  const [addZone, setAddZone] = useState<AddZone>('mainboard')
  const [hasLocalEdits, setHasLocalEdits] = useState(false)
  const [lastAdded, setLastAdded] = useState<string | null>(null)
  const [selectedCardDetails, setSelectedCardDetails] = useState<CardDetails | null>(null)

  const allGroups = useMemo(() => buildGroups(deckEntries), [deckEntries])
  const visibleEntries = useMemo(
    () => deckEntries.filter((entry) => entryMatchesFilter(entry, filterText)),
    [deckEntries, filterText],
  )
  const visibleEntryIds = useMemo(
    () => new Set(visibleEntries.map((entry) => entry.entry_id)),
    [visibleEntries],
  )
  const visibleGroups = useMemo(
    () =>
      allGroups
        .map((group) => ({
          ...group,
          entries: group.entries.filter((entry) => visibleEntryIds.has(entry.entry_id)),
        }))
        .filter((group) => group.entries.length > 0),
    [allGroups, visibleEntryIds],
  )
  const searchResults = useMemo(
    () => searchLocalCards(cardSearchText),
    [cardSearchText],
  )

  const activeQuantity = deckEntries
    .filter((entry) => ACTIVE_ZONES.has(entry.zone))
    .reduce((total, entry) => total + entry.quantity, 0)
  const maybeboardQuantity = deckEntries
    .filter((entry) => entry.zone === 'maybeboard')
    .reduce((total, entry) => total + entry.quantity, 0)
  const commanderName =
    deckEntries.find((entry) => entry.zone === 'commander')?.card_name ?? 'Not set'

  function toggleGroup(groupId: string) {
    setCollapsedGroups((current) => {
      const next = new Set(current)
      if (next.has(groupId)) {
        next.delete(groupId)
      } else {
        next.add(groupId)
      }
      return next
    })
  }

  function addCandidateToDeck(candidate: CardSearchCandidate) {
    const targetCategory = categoryForCandidate(candidate, addZone)

    setDeckEntries((current) => {
      const matchingEntry = current.find(
        (entry) =>
          entry.zone === addZone &&
          normalizeText(entry.card_name) === normalizeText(candidate.card_name) &&
          normalizeText(entry.categories[0] ?? '') === normalizeText(targetCategory),
      )

      if (matchingEntry) {
        return current.map((entry) =>
          entry.entry_id === matchingEntry.entry_id
            ? { ...entry, quantity: entry.quantity + 1 }
            : entry,
        )
      }

      return [
        ...current,
        cardCandidateToEntry(candidate, addZone, targetCategory, current),
      ]
    })
    setHasLocalEdits(true)
    setLastAdded(`${candidate.card_name} added to ${zoneLabel(addZone)}.`)
  }

  return (
    <main className="app-shell">
      <header className="deck-header" aria-labelledby="deck-title">
        <div className="brand-mark" aria-hidden="true">
          MW
        </div>
        <div className="deck-heading">
          <p className="eyebrow">Local workspace</p>
          <h1 id="deck-title">{workspaceViewProjection.deck_name}</h1>
          <div className="deck-meta" aria-label="Deck summary">
            <span>Commander</span>
            <span>{activeQuantity} active cards</span>
            <span>{maybeboardQuantity} maybeboard</span>
            <span className={hasLocalEdits ? 'unsaved-state' : 'saved-state'}>
              {hasLocalEdits ? (
                <CircleAlert size={16} aria-hidden="true" />
              ) : (
                <CheckCircle2 size={16} aria-hidden="true" />
              )}
              {hasLocalEdits ? 'Unsaved' : 'Saved'}
            </span>
          </div>
        </div>
      </header>

      <section className="workspace-bar" aria-label="Deck workspace controls">
        <div className="view-toggle" aria-label="View mode">
          <button
            type="button"
            className={viewMode === 'grouped' ? 'active' : ''}
            onClick={() => setViewMode('grouped')}
          >
            <Layers size={16} aria-hidden="true" />
            Grouped
          </button>
          <button
            type="button"
            className={viewMode === 'table' ? 'active' : ''}
            onClick={() => setViewMode('table')}
          >
            <Table2 size={16} aria-hidden="true" />
            Table
          </button>
        </div>

        <div className="state-chips" aria-label="Projection state">
          <span>Group: Category</span>
          <span>Sort: Mana Value</span>
        </div>

        <button
          type="button"
          className={isAddOpen ? 'add-card-toggle active' : 'add-card-toggle'}
          onClick={() => setIsAddOpen((current) => !current)}
        >
          {isAddOpen ? (
            <X size={16} aria-hidden="true" />
          ) : (
            <Plus size={16} aria-hidden="true" />
          )}
          {isAddOpen ? 'Close add' : 'Add card'}
        </button>

        <label className="deck-filter">
          <Search size={17} aria-hidden="true" />
          <span className="sr-only">Filter current deck</span>
          <input
            value={filterText}
            onChange={(event) => setFilterText(event.target.value)}
            placeholder="Filter current deck"
          />
        </label>
      </section>

      {isAddOpen && (
        <section className="add-card-panel" aria-label="Find and add cards">
          <div className="add-card-header">
            <div>
              <p className="eyebrow">Local card search</p>
              <h2>Find and add</h2>
            </div>
            <div className="add-zone-toggle" aria-label="Add target zone">
              {ADD_ZONES.map((zone) => (
                <button
                  key={zone}
                  type="button"
                  className={addZone === zone ? 'active' : ''}
                  onClick={() => setAddZone(zone)}
                >
                  {zoneLabel(zone)}
                </button>
              ))}
            </div>
          </div>

          <label className="card-search-field">
            <Search size={17} aria-hidden="true" />
            <span className="sr-only">Search local card catalog</span>
            <input
              value={cardSearchText}
              onChange={(event) => setCardSearchText(event.target.value)}
              placeholder="Search local card catalog"
            />
          </label>

          {lastAdded && (
            <p className="add-status" role="status">
              {lastAdded}
            </p>
          )}

          <SearchResults
            addZone={addZone}
            deckEntries={deckEntries}
            query={cardSearchText}
            results={searchResults}
            onAdd={addCandidateToDeck}
            onOpenDetails={setSelectedCardDetails}
          />
        </section>
      )}

      {selectedCardDetails && (
        <CardDetailsPanel
          details={selectedCardDetails}
          onClose={() => setSelectedCardDetails(null)}
        />
      )}

      <section className="workspace-layout">
        <section className="deck-workspace" aria-label="Deck cards">
          <div className="workspace-title">
            <div>
              <p className="eyebrow">Current view</p>
              <h2>{viewMode === 'grouped' ? 'Grouped deck' : 'Deck table'}</h2>
            </div>
            <div className="row-count">
              <Filter size={15} aria-hidden="true" />
              {visibleEntries.length} entries
            </div>
          </div>

          {viewMode === 'grouped' ? (
            <GroupedDeck
              groups={visibleGroups}
              collapsedGroups={collapsedGroups}
              onToggleGroup={toggleGroup}
              onOpenDetails={setSelectedCardDetails}
            />
          ) : (
            <DeckTable
              entries={visibleEntries}
              onOpenDetails={setSelectedCardDetails}
            />
          )}
        </section>

        <aside className="deck-sidebar" aria-label="Deck facts">
          <div>
            <p className="eyebrow">Deck snapshot</p>
            <h2>Open deck</h2>
          </div>
          <dl className="fact-list">
            <div>
              <dt>Format</dt>
              <dd>Commander</dd>
            </div>
            <div>
              <dt>Active quantity</dt>
              <dd>{activeQuantity}</dd>
            </div>
            <div>
              <dt>Maybeboard</dt>
              <dd>{maybeboardQuantity}</dd>
            </div>
            <div>
              <dt>Groups</dt>
              <dd>{allGroups.length}</dd>
            </div>
          </dl>
          <div className="sidebar-note">
            <BookOpen size={17} aria-hidden="true" />
            <span>{commanderName} is set as commander.</span>
          </div>
        </aside>
      </section>
    </main>
  )
}

function SearchResults({
  addZone,
  deckEntries,
  query,
  results,
  onAdd,
  onOpenDetails,
}: {
  addZone: AddZone
  deckEntries: WorkspaceViewEntry[]
  query: string
  results: CardSearchCandidate[]
  onAdd: (candidate: CardSearchCandidate) => void
  onOpenDetails: (details: CardDetails) => void
}) {
  if (!normalizeText(query)) {
    return null
  }

  if (results.length === 0) {
    return (
      <div className="search-empty">
        <p>No local matches.</p>
      </div>
    )
  }

  return (
    <div className="search-results">
      {results.map((candidate) => {
        const quantityInDeck = candidateQuantityInDeck(deckEntries, candidate.card_name)
        return (
          <article className="search-result" key={candidate.card_id}>
            <div className="search-result-main">
              <strong>{candidate.card_name}</strong>
              <span>{candidate.type_line}</span>
            </div>
            <div className="search-result-meta">
              <span>{candidate.categories[0] ?? 'Uncategorized'}</span>
              <span>MV {formatManaValue(candidate.mana_value)}</span>
              <span>{formatColors(candidate.color_identity)}</span>
              {quantityInDeck > 0 && <span>{quantityInDeck} in deck</span>}
            </div>
            <div className="search-result-actions">
              <button
                type="button"
                className="details-trigger"
                onClick={() => onOpenDetails(candidateToDetails(candidate, quantityInDeck))}
              >
                <Info size={15} aria-hidden="true" />
                Details
              </button>
              <button
                type="button"
                className="result-add"
                onClick={() => onAdd(candidate)}
              >
                <Plus size={15} aria-hidden="true" />
                Add to {zoneLabel(addZone)}
              </button>
            </div>
          </article>
        )
      })}
    </div>
  )
}

function GroupedDeck({
  groups,
  collapsedGroups,
  onToggleGroup,
  onOpenDetails,
}: {
  groups: WorkspaceViewGroup[]
  collapsedGroups: Set<string>
  onToggleGroup: (groupId: string) => void
  onOpenDetails: (details: CardDetails) => void
}) {
  if (groups.length === 0) {
    return <EmptyState />
  }

  return (
    <div className="group-list">
      {groups.map((group) => {
        const isCollapsed = collapsedGroups.has(group.group_id)
        const quantityTotal = group.entries.reduce((total, entry) => total + entry.quantity, 0)
        return (
          <section className="deck-group" key={group.group_id}>
            <button
              type="button"
              className="group-heading"
              onClick={() => onToggleGroup(group.group_id)}
              aria-expanded={!isCollapsed}
            >
              <span className="group-title">
                {isCollapsed ? (
                  <ChevronRight size={18} aria-hidden="true" />
                ) : (
                  <ChevronDown size={18} aria-hidden="true" />
                )}
                {group.label}
              </span>
              <span className="group-count">
                {quantityTotal} {quantityTotal === 1 ? 'card' : 'cards'}
              </span>
            </button>
            {!isCollapsed && (
              <div className="card-rows">
                {group.entries.map((entry) => (
                  <DeckRow
                    entry={entry}
                    key={entry.entry_id}
                    onOpenDetails={onOpenDetails}
                  />
                ))}
              </div>
            )}
          </section>
        )
      })}
    </div>
  )
}

function DeckTable({
  entries,
  onOpenDetails,
}: {
  entries: WorkspaceViewEntry[]
  onOpenDetails: (details: CardDetails) => void
}) {
  if (entries.length === 0) {
    return <EmptyState />
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Qty</th>
            <th>Card</th>
            <th>Category</th>
            <th>Mana</th>
            <th>Type</th>
            <th>Zone</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((entry) => (
            <tr key={entry.entry_id}>
              <td>{entry.quantity}</td>
              <td>{entry.card_name}</td>
              <td>{entry.categories[0] ?? 'Uncategorized'}</td>
              <td>{formatManaValue(entry.mana_value)}</td>
              <td>{entry.type_labels.join(', ') || 'Card'}</td>
              <td>{zoneLabel(entry.zone)}</td>
              <td>
                <button
                  type="button"
                  className="details-trigger compact"
                  onClick={() => onOpenDetails(entryToDetails(entry))}
                >
                  <Info size={14} aria-hidden="true" />
                  Details
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function DeckRow({
  entry,
  onOpenDetails,
}: {
  entry: WorkspaceViewEntry
  onOpenDetails: (details: CardDetails) => void
}) {
  return (
    <article className="deck-row">
      <div className="quantity" aria-label={`${entry.quantity} copies`}>
        {entry.quantity}
      </div>
      <div className="card-name">
        <strong>{entry.card_name}</strong>
        <span>{entry.type_line ?? 'Card'}</span>
      </div>
      <div className="category-pills" aria-label="Categories">
        {(entry.categories.length > 0 ? entry.categories : ['Uncategorized']).map((category) => (
          <span key={category}>{category}</span>
        ))}
      </div>
      <div className="mana-value" aria-label="Mana value">
        {formatManaValue(entry.mana_value)}
      </div>
      <div className="zone-pill">{zoneLabel(entry.zone)}</div>
      <button
        type="button"
        className="details-trigger"
        onClick={() => onOpenDetails(entryToDetails(entry))}
      >
        <Info size={15} aria-hidden="true" />
        Details
      </button>
    </article>
  )
}

function CardDetailsPanel({
  details,
  onClose,
}: {
  details: CardDetails
  onClose: () => void
}) {
  const tagLabels = [...details.tags]

  return (
    <section className="card-details-panel" aria-label={`${details.card_name} details`}>
      <div className="card-details-header">
        <div>
          <p className="eyebrow">{details.source === 'deck' ? 'Deck card' : 'Search result'}</p>
          <h2>{details.card_name}</h2>
        </div>
        <button
          type="button"
          className="details-close"
          onClick={onClose}
          aria-label="Close card details"
        >
          <X size={16} aria-hidden="true" />
          Close
        </button>
      </div>

      <dl className="details-grid">
        <DetailField label="Type" value={details.type_line || 'Card'} />
        <DetailField label="Mana value" value={formatManaValue(details.mana_value)} />
        <DetailField label="Color identity" value={formatColors(details.color_identity)} />
        <DetailField label="Zone" value={details.zone ? zoneLabel(details.zone) : 'Not in deck'} />
        <DetailField
          label="Quantity"
          value={details.quantity === null ? 'Not in deck' : `${details.quantity}`}
        />
        <DetailPills
          label="Categories"
          values={details.categories.length > 0 ? details.categories : ['Uncategorized']}
        />
        {tagLabels.length > 0 && <DetailPills label="Tags" values={tagLabels} />}
        {details.notes && <DetailField label="Notes" value={details.notes} />}
      </dl>
    </section>
  )
}

function DetailField({ label, value }: { label: string; value: string }) {
  return (
    <div className="details-field">
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  )
}

function DetailPills({ label, values }: { label: string; values: string[] }) {
  return (
    <div className="details-field">
      <dt>{label}</dt>
      <dd className="details-pills">
        {values.map((value) => (
          <span key={value}>{value}</span>
        ))}
      </dd>
    </div>
  )
}

function EmptyState() {
  return (
    <div className="empty-state">
      <p>No cards match the current filter.</p>
    </div>
  )
}

function entryToDetails(entry: WorkspaceViewEntry): CardDetails {
  return {
    source: 'deck',
    card_name: entry.card_name,
    type_line: entry.type_line ?? 'Card',
    mana_value: entry.mana_value,
    color_identity: entry.color_identity ?? [],
    zone: entry.zone,
    quantity: entry.quantity,
    categories: entry.categories,
    tags: [...entry.tags, ...entry.secondary_tags],
    notes: null,
  }
}

function candidateToDetails(
  candidate: CardSearchCandidate,
  quantityInDeck: number,
): CardDetails {
  return {
    source: 'search',
    card_name: candidate.card_name,
    type_line: candidate.type_line,
    mana_value: candidate.mana_value,
    color_identity: candidate.color_identity,
    zone: null,
    quantity: quantityInDeck > 0 ? quantityInDeck : null,
    categories: candidate.categories,
    tags: candidate.tags,
    notes: null,
  }
}

function uniqueEntries(entries: WorkspaceViewEntry[]) {
  const seen = new Set<string>()
  return entries.filter((entry) => {
    if (seen.has(entry.entry_id)) {
      return false
    }
    seen.add(entry.entry_id)
    return true
  })
}

function buildGroups(entries: WorkspaceViewEntry[]): WorkspaceViewGroup[] {
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

function cardCandidateToEntry(
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

function categoryForCandidate(candidate: CardSearchCandidate, zone: AddZone) {
  if (zone === 'maybeboard') {
    return 'Maybeboard'
  }
  return candidate.categories[0] ?? 'Uncategorized'
}

function entryMatchesFilter(entry: WorkspaceViewEntry, filterText: string) {
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

function searchLocalCards(query: string) {
  const normalizedQuery = normalizeText(query)
  if (!normalizedQuery) {
    return []
  }

  return localCardSearchFixture
    .filter((candidate) => candidateMatchesSearch(candidate, normalizedQuery))
    .sort((left, right) => left.card_name.localeCompare(right.card_name))
    .slice(0, MAX_SEARCH_RESULTS)
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

function candidateQuantityInDeck(entries: WorkspaceViewEntry[], cardName: string) {
  return entries
    .filter((entry) => normalizeText(entry.card_name) === normalizeText(cardName))
    .reduce((total, entry) => total + entry.quantity, 0)
}

function deriveTypeLabels(typeLine: string) {
  const supertypeText = typeLine.split(/[-—]/)[0] ?? ''
  const labels = ['Artifact', 'Creature', 'Enchantment', 'Instant', 'Land', 'Planeswalker', 'Sorcery']
  return labels.filter((label) => supertypeText.includes(label))
}

function normalizeGroupId(label: string) {
  return normalizeText(label).replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') ||
    'uncategorized'
}

function normalizeText(value: string) {
  return value.trim().toLocaleLowerCase().replace(/\s+/g, ' ')
}

function formatManaValue(value: number | null) {
  if (value === null) {
    return '-'
  }
  return Number.isInteger(value) ? `${value}` : value.toFixed(1)
}

function formatColors(colors: string[] | null | undefined) {
  return !colors || colors.length === 0 ? 'Colorless' : colors.join('')
}

function zoneLabel(zone: string) {
  if (zone === 'commander') {
    return 'Commander'
  }
  if (zone === 'maybeboard') {
    return 'Maybeboard'
  }
  return 'Mainboard'
}

export default App

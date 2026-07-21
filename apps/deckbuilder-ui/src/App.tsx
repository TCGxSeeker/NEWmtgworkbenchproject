import {
  BookOpen,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Filter,
  Layers,
  Search,
  Table2,
} from 'lucide-react'
import { useMemo, useState } from 'react'
import './App.css'
import {
  type WorkspaceViewEntry,
  type WorkspaceViewGroup,
  workspaceViewProjection,
} from './workspaceProjection'

type ViewMode = 'grouped' | 'table'

const ACTIVE_ZONES = new Set(['commander', 'mainboard'])

function App() {
  const [viewMode, setViewMode] = useState<ViewMode>('grouped')
  const [filterText, setFilterText] = useState('')
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(new Set())

  const allEntries = useMemo(
    () => uniqueEntries(workspaceViewProjection.groups.flatMap((group) => group.entries)),
    [],
  )
  const visibleEntries = useMemo(
    () => allEntries.filter((entry) => entryMatchesFilter(entry, filterText)),
    [allEntries, filterText],
  )
  const visibleEntryIds = useMemo(
    () => new Set(visibleEntries.map((entry) => entry.entry_id)),
    [visibleEntries],
  )
  const visibleGroups = useMemo(
    () =>
      workspaceViewProjection.groups
        .map((group) => ({
          ...group,
          entries: group.entries.filter((entry) => visibleEntryIds.has(entry.entry_id)),
        }))
        .filter((group) => group.entries.length > 0),
    [visibleEntryIds],
  )

  const activeQuantity = visibleEntries
    .filter((entry) => ACTIVE_ZONES.has(entry.zone))
    .reduce((total, entry) => total + entry.quantity, 0)
  const maybeboardQuantity = visibleEntries
    .filter((entry) => entry.zone === 'maybeboard')
    .reduce((total, entry) => total + entry.quantity, 0)
  const commanderName =
    visibleEntries.find((entry) => entry.zone === 'commander')?.card_name ?? 'Not set'

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
            <span className="saved-state">
              <CheckCircle2 size={16} aria-hidden="true" />
              Saved
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
            />
          ) : (
            <DeckTable entries={visibleEntries} />
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
              <dd>{visibleGroups.length}</dd>
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

function GroupedDeck({
  groups,
  collapsedGroups,
  onToggleGroup,
}: {
  groups: WorkspaceViewGroup[]
  collapsedGroups: Set<string>
  onToggleGroup: (groupId: string) => void
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
                  <DeckRow entry={entry} key={entry.entry_id} />
                ))}
              </div>
            )}
          </section>
        )
      })}
    </div>
  )
}

function DeckTable({ entries }: { entries: WorkspaceViewEntry[] }) {
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
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function DeckRow({ entry }: { entry: WorkspaceViewEntry }) {
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
    </article>
  )
}

function EmptyState() {
  return (
    <div className="empty-state">
      <p>No cards match the current filter.</p>
    </div>
  )
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

function normalizeText(value: string) {
  return value.trim().toLocaleLowerCase().replace(/\s+/g, ' ')
}

function formatManaValue(value: number | null) {
  if (value === null) {
    return '-'
  }
  return Number.isInteger(value) ? `${value}` : value.toFixed(1)
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

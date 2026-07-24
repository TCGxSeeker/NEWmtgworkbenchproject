import {
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  CircleAlert,
  FilePlus2,
  Filter,
  FolderOpen,
  Home,
  Info,
  Layers,
  Library,
  Plus,
  Save,
  Search,
  Table2,
  Upload,
  X,
} from 'lucide-react'
import {
  type ChangeEvent,
  type FormEvent,
  useMemo,
  useRef,
  useState,
} from 'react'
import './App.css'
import {
  type CardSearchCandidate,
  localCardSearchFixture,
} from './cardSearchFixture'
import {
  ACTIVE_ZONES,
  ADD_ZONES,
  MIN_FREE_TEXT_SEARCH_LENGTH,
  type AddZone,
  type CardDetails,
  type ValidationItem,
  type ViewMode,
  buildGroups,
  buildMechanicalValidationItems,
  candidateQuantityInDeck,
  candidateToDetails,
  cardCandidateToEntry,
  categoryForCandidate,
  duplicateNonBasicNameSet,
  entryMatchesFilter,
  entryToDetails,
  formatColors,
  formatManaValue,
  isCardSearchReady,
  isDuplicateNonBasicEntry,
  normalizeText,
  searchLocalCards,
  zoneLabel,
} from './deckUiLogic'
import {
  type WorkspaceViewEntry,
  type WorkspaceViewGroup,
  workspaceViewProjection,
} from './workspaceProjection'
import {
  type DeckLibraryItem,
  type DeckWorkspaceState,
  WorkspaceFileError,
  createEmptyDeckState,
  deckStateFromProjection,
  deckStateToLibraryItem,
  markDeckClean,
  markDeckDirty,
  parseNativeWorkspaceText,
  serializeDeckState,
  workspaceDownloadName,
} from './workspaceFiles'

type AppScreen = 'library' | 'deck'

const initialDeckState = deckStateFromProjection(workspaceViewProjection)

function App() {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [screen, setScreen] = useState<AppScreen>('library')
  const [deckState, setDeckState] = useState<DeckWorkspaceState>(() => initialDeckState)
  const [libraryDecks, setLibraryDecks] = useState<Record<string, DeckWorkspaceState>>(() => ({
    [initialDeckState.deckId]: initialDeckState,
  }))
  const [libraryStatus, setLibraryStatus] = useState<string | null>(null)
  const [fileError, setFileError] = useState<string | null>(null)
  const [newDeckName, setNewDeckName] = useState('')
  const [newDeckFormat, setNewDeckFormat] = useState('commander')
  const [viewMode, setViewMode] = useState<ViewMode>('grouped')
  const [filterText, setFilterText] = useState('')
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(
    () => defaultCollapsedGroupsFor(initialDeckState.entries),
  )
  const [isAddOpen, setIsAddOpen] = useState(false)
  const [cardSearchText, setCardSearchText] = useState('')
  const [addZone, setAddZone] = useState<AddZone>('mainboard')
  const [lastAdded, setLastAdded] = useState<string | null>(null)
  const [workspaceMessage, setWorkspaceMessage] = useState<string | null>(null)
  const [selectedCardDetails, setSelectedCardDetails] = useState<CardDetails | null>(null)

  const deckEntries = deckState.entries
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
    () => searchLocalCards(cardSearchText, localCardSearchFixture),
    [cardSearchText],
  )
  const validationItems = useMemo(
    () => buildMechanicalValidationItems(deckEntries),
    [deckEntries],
  )
  const duplicateNames = useMemo(() => duplicateNonBasicNameSet(deckEntries), [deckEntries])
  const libraryItems = useMemo(
    () =>
      Object.values(libraryDecks)
        .map(deckStateToLibraryItem)
        .sort(compareLibraryItems),
    [libraryDecks],
  )

  const activeQuantity = deckEntries
    .filter((entry) => ACTIVE_ZONES.has(entry.zone))
    .reduce((total, entry) => total + entry.quantity, 0)
  const maybeboardQuantity = deckEntries
    .filter((entry) => entry.zone === 'maybeboard')
    .reduce((total, entry) => total + entry.quantity, 0)
  const commanderName =
    deckEntries.find((entry) => entry.zone === 'commander')?.card_name ?? 'No commander'

  function setActiveDeck(nextDeckState: DeckWorkspaceState) {
    setDeckState(nextDeckState)
    setCollapsedGroups(defaultCollapsedGroupsFor(nextDeckState.entries))
    setLibraryDecks((current) => ({
      ...current,
      [nextDeckState.deckId]: nextDeckState,
    }))
  }

  function updateDeckEntries(
    updater: (entries: WorkspaceViewEntry[]) => WorkspaceViewEntry[],
  ) {
    setDeckState((current) => {
      const nextDeckState = markDeckDirty(current, updater(current.entries))
      setLibraryDecks((decks) => ({
        ...decks,
        [nextDeckState.deckId]: nextDeckState,
      }))
      return nextDeckState
    })
  }

  function openLibraryDeck(deckId: string) {
    const nextDeckState = libraryDecks[deckId]
    if (!nextDeckState) {
      return
    }
    setDeckState(nextDeckState)
    setScreen('deck')
    setFileError(null)
    setWorkspaceMessage(`${nextDeckState.deckName} opened from the library.`)
  }

  function createDeck(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const deckName = newDeckName.trim() || 'Untitled Deck'
    const nextDeckState = createEmptyDeckState(deckName, newDeckFormat)
    setActiveDeck(nextDeckState)
    setNewDeckName('')
    setNewDeckFormat('commander')
    setFileError(null)
    setLibraryStatus(`${deckName} created.`)
    setWorkspaceMessage(`${deckName} is ready for cards.`)
    setScreen('deck')
  }

  function requestWorkspaceFile() {
    fileInputRef.current?.click()
  }

  async function openWorkspaceFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.currentTarget.files?.[0]
    event.currentTarget.value = ''
    if (!file) {
      return
    }

    try {
      const text = await file.text()
      const nextDeckState = parseNativeWorkspaceText(text, file.name)
      setActiveDeck(nextDeckState)
      setScreen('deck')
      setFileError(null)
      setLibraryStatus(`${nextDeckState.deckName} opened from ${file.name}.`)
      setWorkspaceMessage(`${nextDeckState.deckName} opened from ${file.name}.`)
    } catch (error) {
      const message =
        error instanceof WorkspaceFileError || error instanceof Error
          ? error.message
          : 'Could not open that workspace file.'
      setFileError(message)
    }
  }

  function saveCurrentWorkspace() {
    const savedAt = new Date().toISOString()
    downloadTextFile(
      workspaceDownloadName(deckState),
      serializeDeckState(deckState, savedAt),
    )
    const cleanDeckState = markDeckClean(deckState, savedAt)
    setActiveDeck(cleanDeckState)
    setWorkspaceMessage(`${cleanDeckState.deckName} workspace download prepared.`)
  }

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

    updateDeckEntries((current) => {
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
    setWorkspaceMessage(null)
    setLastAdded(`${candidate.card_name} added to ${zoneLabel(addZone)}.`)
  }

  const workspaceFileInput = (
    <input
      ref={fileInputRef}
      className="sr-only"
      type="file"
      accept=".mtgwdeck.json,.json,application/json"
      onChange={openWorkspaceFile}
    />
  )

  if (screen === 'library') {
    return (
      <main className="app-shell library-shell">
        {workspaceFileInput}
        <DeckLibraryScreen
          fileError={fileError}
          items={libraryItems}
          newDeckFormat={newDeckFormat}
          newDeckName={newDeckName}
          status={libraryStatus}
          onCreateDeck={createDeck}
          onNewDeckFormatChange={setNewDeckFormat}
          onNewDeckNameChange={setNewDeckName}
          onOpenDeck={openLibraryDeck}
          onOpenFile={requestWorkspaceFile}
        />
      </main>
    )
  }

  return (
    <main className="app-shell">
      {workspaceFileInput}
      <header className="deck-header" aria-labelledby="deck-title">
        <div className="brand-mark" aria-hidden="true">
          MW
        </div>
        <div className="deck-heading">
          <p className="eyebrow">Local workspace</p>
          <h1 id="deck-title">{deckState.deckName}</h1>
          <div className="deck-meta" aria-label="Deck summary">
            <span>{titleCase(deckState.format)}</span>
            <span>{activeQuantity} active cards</span>
            <span>{maybeboardQuantity} maybeboard</span>
            <span className={deckState.savedState.isDirty ? 'unsaved-state' : 'saved-state'}>
              {deckState.savedState.isDirty ? (
                <CircleAlert size={16} aria-hidden="true" />
              ) : (
                <CheckCircle2 size={16} aria-hidden="true" />
              )}
              {deckState.savedState.isDirty ? 'Unsaved' : 'Saved'}
            </span>
          </div>
        </div>
        <div className="deck-header-actions" aria-label="Workspace actions">
          <button type="button" className="secondary-action" onClick={() => setScreen('library')}>
            <ArrowLeft size={16} aria-hidden="true" />
            Library
          </button>
          <button type="button" className="secondary-action" onClick={requestWorkspaceFile}>
            <Upload size={16} aria-hidden="true" />
            Open
          </button>
          <button type="button" className="primary-action" onClick={saveCurrentWorkspace}>
            <Save size={16} aria-hidden="true" />
            Save
          </button>
        </div>
      </header>

      {(workspaceMessage || fileError) && (
        <div className={fileError ? 'status-banner warning' : 'status-banner'} role="status">
          {fileError ?? workspaceMessage}
        </div>
      )}

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
            collapsedGroups={collapsedGroups}
            duplicateNames={duplicateNames}
            groups={visibleGroups}
            onOpenDetails={setSelectedCardDetails}
            onToggleGroup={toggleGroup}
          />
        ) : (
          <DeckTable
            duplicateNames={duplicateNames}
            entries={visibleEntries}
            onOpenDetails={setSelectedCardDetails}
          />
        )}
      </section>

      <section className="deck-context-panel" aria-label="Deck context">
        <DeckSnapshot
          activeQuantity={activeQuantity}
          commanderName={commanderName}
          format={deckState.format}
          maybeboardQuantity={maybeboardQuantity}
          sourceLabel={deckState.sourceLabel}
        />
        <ValidationPanel items={validationItems} />
      </section>
    </main>
  )
}

function DeckLibraryScreen({
  fileError,
  items,
  newDeckFormat,
  newDeckName,
  status,
  onCreateDeck,
  onNewDeckFormatChange,
  onNewDeckNameChange,
  onOpenDeck,
  onOpenFile,
}: {
  fileError: string | null
  items: DeckLibraryItem[]
  newDeckFormat: string
  newDeckName: string
  status: string | null
  onCreateDeck: (event: FormEvent<HTMLFormElement>) => void
  onNewDeckFormatChange: (value: string) => void
  onNewDeckNameChange: (value: string) => void
  onOpenDeck: (deckId: string) => void
  onOpenFile: () => void
}) {
  return (
    <>
      <header className="library-hero" aria-labelledby="library-title">
        <div>
          <p className="eyebrow">Local deck library</p>
          <h1 id="library-title">MTG Workbench</h1>
          <p>
            Create, open, and continue local Commander deck projects before
            entering the focused deck workspace.
          </p>
        </div>
        <div className="library-hero-actions">
          <button type="button" className="secondary-action" onClick={onOpenFile}>
            <Upload size={16} aria-hidden="true" />
            Open file
          </button>
        </div>
      </header>

      {(status || fileError) && (
        <div className={fileError ? 'status-banner warning' : 'status-banner'} role="status">
          {fileError ?? status}
        </div>
      )}

      <section className="library-layout" aria-label="Deck library">
        <section className="library-panel deck-list-panel">
          <div className="library-section-title">
            <div>
              <p className="eyebrow">Saved locally</p>
              <h2>Decks</h2>
            </div>
            <Library size={20} aria-hidden="true" />
          </div>
          <div className="deck-library-list">
            {items.map((item) => (
              <DeckLibraryCard
                item={item}
                key={item.deckId}
                onOpenDeck={onOpenDeck}
              />
            ))}
          </div>
        </section>

        <aside className="library-panel create-deck-panel">
          <div className="library-section-title">
            <div>
              <p className="eyebrow">New project</p>
              <h2>Create deck</h2>
            </div>
            <FilePlus2 size={20} aria-hidden="true" />
          </div>
          <form className="new-deck-form" onSubmit={onCreateDeck}>
            <label>
              <span>Deck name</span>
              <input
                value={newDeckName}
                onChange={(event) => onNewDeckNameChange(event.target.value)}
                placeholder="Untitled Commander Deck"
              />
            </label>
            <label>
              <span>Format</span>
              <select
                value={newDeckFormat}
                onChange={(event) => onNewDeckFormatChange(event.target.value)}
              >
                <option value="commander">Commander</option>
                <option value="casual">Casual</option>
              </select>
            </label>
            <button type="submit" className="primary-action">
              <Plus size={16} aria-hidden="true" />
              Create deck
            </button>
          </form>
          <div className="library-note">
            <Home size={17} aria-hidden="true" />
            <span>Files stay local. Opening uses your file picker; saving downloads a native workspace JSON.</span>
          </div>
        </aside>
      </section>
    </>
  )
}

function DeckLibraryCard({
  item,
  onOpenDeck,
}: {
  item: DeckLibraryItem
  onOpenDeck: (deckId: string) => void
}) {
  return (
    <article className="deck-library-card">
      <div className="deck-library-main">
        <h3>{item.name}</h3>
        <p>{item.commanderName}</p>
      </div>
      <div className="deck-library-meta" aria-label={`${item.name} summary`}>
        <span>{titleCase(item.format)}</span>
        <span>{item.activeQuantity} active</span>
        <span>{item.maybeboardQuantity} maybe</span>
        <span className={item.isDirty ? 'unsaved-state' : 'saved-state'}>
          {item.isDirty ? 'Unsaved' : 'Saved'}
        </span>
      </div>
      <button type="button" className="primary-action compact" onClick={() => onOpenDeck(item.deckId)}>
        <FolderOpen size={15} aria-hidden="true" />
        Open
      </button>
    </article>
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

  if (!isCardSearchReady(query)) {
    return (
      <div className="search-empty">
        <p>Type at least {MIN_FREE_TEXT_SEARCH_LENGTH} characters to search local cards.</p>
      </div>
    )
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
  collapsedGroups,
  duplicateNames,
  groups,
  onToggleGroup,
  onOpenDetails,
}: {
  collapsedGroups: Set<string>
  duplicateNames: Set<string>
  groups: WorkspaceViewGroup[]
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
                    duplicateNames={duplicateNames}
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
  duplicateNames,
  entries,
  onOpenDetails,
}: {
  duplicateNames: Set<string>
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
          {entries.map((entry) => {
            const hasDuplicateWarning = isDuplicateNonBasicEntry(entry, duplicateNames)
            return (
              <tr className={hasDuplicateWarning ? 'duplicate-warning' : ''} key={entry.entry_id}>
                <td>{entry.quantity}</td>
                <td>
                  {entry.card_name}
                  {hasDuplicateWarning && <small className="inline-warning">Duplicate</small>}
                </td>
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
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

function DeckRow({
  duplicateNames,
  entry,
  onOpenDetails,
}: {
  duplicateNames: Set<string>
  entry: WorkspaceViewEntry
  onOpenDetails: (details: CardDetails) => void
}) {
  const hasDuplicateWarning = isDuplicateNonBasicEntry(entry, duplicateNames)
  return (
    <article className={hasDuplicateWarning ? 'deck-row duplicate-warning' : 'deck-row'}>
      <div className="quantity" aria-label={`${entry.quantity} copies`}>
        {entry.quantity}
      </div>
      <div className="card-name">
        <strong>{entry.card_name}</strong>
        <span>{entry.type_line ?? 'Card'}</span>
        {hasDuplicateWarning && <small className="inline-warning">Duplicate active non-basic</small>}
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

function DeckSnapshot({
  activeQuantity,
  commanderName,
  format,
  maybeboardQuantity,
  sourceLabel,
}: {
  activeQuantity: number
  commanderName: string
  format: string
  maybeboardQuantity: number
  sourceLabel: string
}) {
  return (
    <section className="context-card" aria-label="Deck snapshot">
      <div>
        <p className="eyebrow">Deck snapshot</p>
        <h2>Current deck</h2>
      </div>
      <dl className="fact-list">
        <div>
          <dt>Format</dt>
          <dd>{titleCase(format)}</dd>
        </div>
        <div>
          <dt>Active cards</dt>
          <dd>{activeQuantity}</dd>
        </div>
        <div>
          <dt>Maybeboard</dt>
          <dd>{maybeboardQuantity}</dd>
        </div>
        <div>
          <dt>Source</dt>
          <dd>{sourceLabel}</dd>
        </div>
      </dl>
      <div className="sidebar-note">
        <BookOpen size={17} aria-hidden="true" />
        <span>{commanderName} is the current commander slot.</span>
      </div>
    </section>
  )
}

function ValidationPanel({ items }: { items: ValidationItem[] }) {
  const warningCount = items.length

  return (
    <section className="validation-panel context-card" aria-label="Mechanical deck validation">
      <div className="validation-heading">
        <div>
          <p className="eyebrow">Mechanical warnings</p>
          <h3>{warningCount === 0 ? 'No current warnings' : `${warningCount} warning${warningCount === 1 ? '' : 's'}`}</h3>
        </div>
      </div>
      {items.length === 0 ? (
        <div className="validation-empty">
          <CheckCircle2 size={16} aria-hidden="true" />
          <span>No actionable mechanical warnings from this local state.</span>
        </div>
      ) : (
        <ul className="validation-list">
          {items.map((item) => (
            <li className={item.status} key={item.id}>
              <CircleAlert size={16} aria-hidden="true" />
              <span>
                <strong>{item.label}</strong>
                <small>{item.detail}</small>
              </span>
            </li>
          ))}
        </ul>
      )}
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

function compareLibraryItems(left: DeckLibraryItem, right: DeckLibraryItem) {
  const updatedComparison = (right.updatedAt ?? '').localeCompare(left.updatedAt ?? '')
  if (updatedComparison !== 0) {
    return updatedComparison
  }
  return left.name.localeCompare(right.name)
}

function downloadTextFile(filename: string, content: string) {
  const blob = new Blob([content], { type: 'application/json' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.href = url
  link.download = filename
  document.body.append(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}

function titleCase(value: string) {
  return value
    .split(/[\s_-]+/)
    .filter(Boolean)
    .map((part) => `${part.charAt(0).toLocaleUpperCase()}${part.slice(1)}`)
    .join(' ')
}

function defaultCollapsedGroupsFor(entries: WorkspaceViewEntry[]) {
  return new Set(
    buildGroups(entries)
      .filter((group) =>
        group.entries.length > 0 &&
        (group.entries.every((entry) => entry.zone === 'maybeboard') ||
          normalizeText(group.label).includes('maybe')),
      )
      .map((group) => group.group_id),
  )
}

export default App

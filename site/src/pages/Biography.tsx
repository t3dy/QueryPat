import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

/* ─── Auto-Extracted schema (original 646 events) ─── */
interface BioEvent {
  bio_id: number
  event_type: string
  summary: string
  detail: string | null
  date_start: string | null
  date_end: string | null
  date_display: string | null
  date_confidence: string | null
  source_type: string | null
  source_name: string | null
  source_doc_id: string | null
  source_seg_id: string | null
  contradicted_by: number[] | null
  contradiction_note: string | null
  reliability: string
  people_involved: string[] | null
  notes: string | null
}

interface BioIndex {
  total: number
  by_type: { type: string; count: number }[]
  reliability_counts: Record<string, number>
}

/* ─── Curated schema (119 style-audited events) ─── */
interface CuratedBioEvent {
  id: string
  date: string
  date_precision: string
  event: string
  category: string
  entities: string[]
  location: string
  source: string
  importance: number
  notes: string
}

/* ─── Dictionary index entry ─── */
interface DictEntry {
  canonical_name: string
  slug: string
}

/* ─── Constants for auto-extracted tab ─── */
const EVENT_TYPE_LABELS: Record<string, string> = {
  birth: 'Birth',
  death: 'Death',
  marriage: 'Marriage',
  divorce: 'Divorce',
  residence: 'Residence',
  employment: 'Employment',
  publication: 'Publication',
  vision: 'Vision / Theophany',
  health: 'Health',
  relationship: 'Relationship',
  legal: 'Legal',
  financial: 'Financial',
  travel: 'Travel',
  substance_use: 'Substance Use',
  correspondence: 'Correspondence',
  other: 'Other',
}

const RELIABILITY_COLORS: Record<string, string> = {
  confirmed: '#2d6a4f',
  likely: '#40916c',
  disputed: '#e76f51',
  contradicted: '#d62828',
  unverified: '#6c757d',
}

/* ─── Constants for curated tab ─── */
const CATEGORY_NAMES: Record<string, string> = {
  birth: 'Birth',
  death: 'Death',
  education: 'Education',
  reading: 'Reading',
  philosophical_influence: 'Philosophical Influence',
  religious_experience: 'Religious Experience',
  visionary_experience: 'Visionary Experience',
  religious_thought: 'Religious Thought',
  publication: 'Publication',
  award: 'Award',
  marriage: 'Marriage',
  divorce: 'Divorce',
  family: 'Family',
  friendship: 'Friendship',
  professional_network: 'Professional Network',
  financial: 'Financial',
  health: 'Health',
  drug_use: 'Drug Use',
  residence: 'Residence',
  travel: 'Travel',
  lecture: 'Lecture',
  correspondence: 'Correspondence',
  employment: 'Employment',
  film_adaptation: 'Film Adaptation',
  crime: 'Crime',
}

const CATEGORY_COLORS: Record<string, string> = {
  birth: '#C09A4D',
  death: '#8B6B6B',
  education: '#6B8E6B',
  reading: '#6B8E6B',
  philosophical_influence: '#6B8E6B',
  religious_experience: '#9B6B9B',
  visionary_experience: '#9B6B9B',
  religious_thought: '#9B6B9B',
  publication: '#8B7355',
  award: '#C09A4D',
  marriage: '#A18B6B',
  divorce: '#A18B6B',
  family: '#A18B6B',
  friendship: '#7B8FA1',
  professional_network: '#7B8FA1',
  financial: '#9B8B8B',
  health: '#8B6B6B',
  drug_use: '#8B6B6B',
  residence: '#9B8B8B',
  travel: '#9B8B8B',
  lecture: '#7B8FA1',
  correspondence: '#7B8FA1',
  employment: '#9B8B8B',
  film_adaptation: '#8B7355',
  crime: '#8B6B6B',
}

const ERA_RANGES: [string, number, number][] = [
  ['Early Life (1928\u20131946)', 1928, 1946],
  ['Apprenticeship (1947\u20131954)', 1947, 1954],
  ['Rising Author (1955\u20131963)', 1955, 1963],
  ['Peak & Crisis (1964\u20131973)', 1964, 1973],
  ['2-3-74 & Exegesis (1974\u20131982)', 1974, 1982],
]

const DENSITY_LABELS: Record<number, string> = {
  0: 'All Events',
  3: 'Intellectual Biography',
  4: 'Major Events Only',
}

/* ─── Helpers ─── */
function getYear(date: string): number {
  const d = date.replace(/^c\.\s*/, '')
  const m = d.match(/^(\d{4})/)
  return m ? parseInt(m[1]) : 0
}

function importanceDots(n: number): string {
  return '\u2022'.repeat(n)
}

type TabId = 'curated' | 'auto'

/* ═══════════════════════════════════════════════════════
   Main Biography Page
   ═══════════════════════════════════════════════════════ */
export default function Biography() {
  const [activeTab, setActiveTab] = useState<TabId>('curated')

  return (
    <>
      <div className="page-header">
        <h1>Philip K. Dick &mdash; Biography</h1>
        <p>
          Biographical events drawn from the Exegesis, letters, interviews, and secondary sources.
        </p>
      </div>

      {/* Tab switcher */}
      <div style={{
        display: 'flex', gap: 0, marginBottom: '1.5rem',
        borderBottom: '2px solid var(--border-light)',
      }}>
        <button
          onClick={() => setActiveTab('curated')}
          style={{
            padding: '0.6rem 1.25rem',
            background: activeTab === 'curated' ? 'var(--accent-bg)' : 'transparent',
            border: 'none',
            borderBottom: activeTab === 'curated' ? '2px solid var(--accent)' : '2px solid transparent',
            fontFamily: 'var(--font-heading)',
            fontSize: '0.95rem',
            color: activeTab === 'curated' ? 'var(--accent)' : 'var(--text-secondary)',
            cursor: 'pointer',
            fontWeight: activeTab === 'curated' ? 600 : 400,
            marginBottom: '-2px',
          }}
        >
          Curated (119)
        </button>
        <button
          onClick={() => setActiveTab('auto')}
          style={{
            padding: '0.6rem 1.25rem',
            background: activeTab === 'auto' ? 'var(--accent-bg)' : 'transparent',
            border: 'none',
            borderBottom: activeTab === 'auto' ? '2px solid var(--accent)' : '2px solid transparent',
            fontFamily: 'var(--font-heading)',
            fontSize: '0.95rem',
            color: activeTab === 'auto' ? 'var(--accent)' : 'var(--text-secondary)',
            cursor: 'pointer',
            fontWeight: activeTab === 'auto' ? 600 : 400,
            marginBottom: '-2px',
          }}
        >
          Auto-Extracted (646)
        </button>
      </div>

      {activeTab === 'curated' ? <CuratedTab /> : <AutoExtractedTab />}
    </>
  )
}

/* ═══════════════════════════════════════════════════════
   CURATED TAB — 119 style-audited entries
   ═══════════════════════════════════════════════════════ */
function CuratedTab() {
  const { data: events, loading, error } = useData<CuratedBioEvent[]>('biography/curated.json')
  const { data: dictIndex } = useData<DictEntry[]>('dictionary/index.json')

  const [activeCategory, setActiveCategory] = useState<string | null>(null)
  const [activeEra, setActiveEra] = useState<number | null>(null)
  const [minImportance, setMinImportance] = useState(0)
  const [searchQuery, setSearchQuery] = useState('')

  // Build dictionary lookup: lowercase name -> slug
  const dictLookup = useMemo(() => {
    const map = new Map<string, string>()
    if (!dictIndex) return map
    for (const entry of dictIndex) {
      map.set(entry.canonical_name.toLowerCase(), entry.slug)
    }
    return map
  }, [dictIndex])

  const filteredEvents = useMemo(() => {
    if (!events) return []
    let filtered = events
    if (activeCategory) {
      filtered = filtered.filter(e => e.category === activeCategory)
    }
    if (activeEra !== null) {
      const [, start, end] = ERA_RANGES[activeEra]
      filtered = filtered.filter(e => {
        const y = getYear(e.date)
        return y >= start && y <= end
      })
    }
    if (minImportance > 0) {
      filtered = filtered.filter(e => e.importance >= minImportance)
    }
    if (searchQuery) {
      const q = searchQuery.toLowerCase()
      filtered = filtered.filter(e =>
        e.event.toLowerCase().includes(q) ||
        e.date.includes(q) ||
        e.source.toLowerCase().includes(q) ||
        (e.entities || []).some(ent => ent.toLowerCase().includes(q)) ||
        (e.location || '').toLowerCase().includes(q)
      )
    }
    return filtered
  }, [events, activeCategory, activeEra, minImportance, searchQuery])

  const categoryCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    if (!events) return counts
    for (const e of events) {
      counts[e.category] = (counts[e.category] || 0) + 1
    }
    return counts
  }, [events])

  if (loading) return <div className="loading">Reconstructing a life...</div>
  if (error) return <div className="loading">Error loading curated biography data.</div>

  return (
    <div className="sidebar-layout">
      {/* Sidebar filters */}
      <div className="sidebar">
        <input
          type="text"
          className="search-input"
          placeholder="Search events, people, places..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
        />

        <div style={{ marginBottom: '1.5rem' }}>
          <h3>Density</h3>
          <ul>
            {Object.entries(DENSITY_LABELS).map(([level, label]) => (
              <li key={level}>
                <a
                  href="#"
                  className={minImportance === Number(level) ? 'active' : ''}
                  onClick={e => { e.preventDefault(); setMinImportance(Number(level)) }}
                >
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <h3>Eras</h3>
          <ul>
            <li>
              <a
                href="#"
                className={activeEra === null ? 'active' : ''}
                onClick={e => { e.preventDefault(); setActiveEra(null) }}
              >
                All Eras ({events?.length ?? 0})
              </a>
            </li>
            {ERA_RANGES.map(([label], i) => (
              <li key={i}>
                <a
                  href="#"
                  className={activeEra === i ? 'active' : ''}
                  onClick={e => { e.preventDefault(); setActiveEra(i) }}
                >
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <h3>Categories</h3>
          <ul>
            <li>
              <a
                href="#"
                className={activeCategory === null ? 'active' : ''}
                onClick={e => { e.preventDefault(); setActiveCategory(null) }}
              >
                All Categories
              </a>
            </li>
            {Object.entries(CATEGORY_NAMES).map(([key, name]) =>
              categoryCounts[key] ? (
                <li key={key}>
                  <a
                    href="#"
                    className={activeCategory === key ? 'active' : ''}
                    onClick={e => { e.preventDefault(); setActiveCategory(key) }}
                  >
                    <span style={{
                      display: 'inline-block', width: 8, height: 8,
                      borderRadius: '50%', background: CATEGORY_COLORS[key] || '#9B8B8B',
                      marginRight: '0.5rem', verticalAlign: 'middle',
                    }} />
                    {name}
                    <span style={{ float: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                      {categoryCounts[key]}
                    </span>
                  </a>
                </li>
              ) : null
            )}
          </ul>
        </div>
      </div>

      {/* Main content */}
      <div>
        <p style={{ color: 'var(--text-muted)', margin: '0 0 1rem', fontSize: '0.9rem' }}>
          {filteredEvents.length} event{filteredEvents.length !== 1 ? 's' : ''}
          {minImportance > 0 && (
            <span style={{ marginLeft: '0.5rem' }}>(importance &ge; {minImportance})</span>
          )}
        </p>

        {filteredEvents.map(event => (
          <CuratedEventCard
            key={event.id}
            event={event}
            dictLookup={dictLookup}
            onCategoryClick={setActiveCategory}
            onSearchEntity={setSearchQuery}
          />
        ))}

        {filteredEvents.length === 0 && (
          <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
            No events match the current filters.
          </p>
        )}
      </div>
    </div>
  )
}

/* ─── Curated event card ─── */
function CuratedEventCard({ event, dictLookup, onCategoryClick, onSearchEntity }: {
  event: CuratedBioEvent
  dictLookup: Map<string, string>
  onCategoryClick: (cat: string) => void
  onSearchEntity: (q: string) => void
}) {
  const catColor = CATEGORY_COLORS[event.category] || '#9B8B8B'

  return (
    <div className="card" style={{ borderLeft: `4px solid ${catColor}`, marginBottom: '0.75rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem' }}>
        <div style={{ flex: 1 }}>
          <span style={{
            fontFamily: 'var(--font-mono)', fontSize: '0.85rem',
            color: 'var(--text-secondary)', fontVariantNumeric: 'tabular-nums',
          }}>
            {event.date}
          </span>
          <span style={{
            marginLeft: '0.75rem', color: 'var(--accent)',
            fontSize: '0.75rem', letterSpacing: '1px',
          }} title={`Importance: ${event.importance}/5`}>
            {importanceDots(event.importance)}
          </span>
        </div>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
          {event.source}
        </span>
      </div>

      <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.95rem', margin: '0.5rem 0', lineHeight: 1.6 }}>
        {event.event}
      </p>

      {event.location && (
        <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', margin: '0.25rem 0' }}>
          {event.location}
        </p>
      )}

      {/* Tags row: category + entities */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.5rem' }}>
        {/* Category badge */}
        <span
          className="badge"
          style={{
            background: catColor + '22',
            color: catColor,
            border: `1px solid ${catColor}55`,
            cursor: 'pointer',
            fontSize: '0.72rem',
          }}
          onClick={() => onCategoryClick(event.category)}
        >
          {CATEGORY_NAMES[event.category] || event.category}
        </span>

        {/* Entity tags */}
        {(event.entities || []).map((entity, j) => {
          const slug = dictLookup.get(entity.toLowerCase()) ?? null
          if (slug) {
            return (
              <Link
                key={j}
                to={`/dictionary/${slug}`}
                className="badge entity-linked"
                style={{
                  background: '#C09A4D22',
                  color: '#7b3f00',
                  border: '1px solid #C09A4D55',
                  fontSize: '0.72rem',
                  textDecoration: 'none',
                  cursor: 'pointer',
                }}
              >
                {entity} &#x2197;
              </Link>
            )
          }
          return (
            <span
              key={j}
              className="badge"
              style={{
                background: 'var(--bg-secondary)',
                color: 'var(--text-secondary)',
                border: '1px solid var(--border-light)',
                fontSize: '0.72rem',
                cursor: 'pointer',
              }}
              onClick={() => onSearchEntity(entity)}
            >
              {entity}
            </span>
          )
        })}
      </div>

      {event.notes && (
        <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '0.5rem', fontStyle: 'italic' }}>
          {event.notes}
        </p>
      )}
    </div>
  )
}

/* ═══════════════════════════════════════════════════════
   AUTO-EXTRACTED TAB — original 646 entries
   ═══════════════════════════════════════════════════════ */
function AutoExtractedTab() {
  const { data: index } = useData<BioIndex>('biography/index.json')
  const { data: events, loading, error } = useData<BioEvent[]>('biography/events.json')
  const [typeFilter, setTypeFilter] = useState<string>('all')
  const [reliabilityFilter, setReliabilityFilter] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')

  const filtered = useMemo(() => {
    if (!events) return []
    return events.filter(e => {
      if (typeFilter !== 'all' && e.event_type !== typeFilter) return false
      if (reliabilityFilter !== 'all' && e.reliability !== reliabilityFilter) return false
      if (searchQuery) {
        const q = searchQuery.toLowerCase()
        const haystack = [e.summary, e.detail, e.date_display, ...(e.people_involved || [])].join(' ').toLowerCase()
        if (!haystack.includes(q)) return false
      }
      return true
    })
  }, [events, typeFilter, reliabilityFilter, searchQuery])

  // Group by decade
  const decades = useMemo(() => {
    const groups: Record<string, BioEvent[]> = {}
    for (const e of filtered) {
      const year = e.date_start?.slice(0, 4)
      const decade = year ? `${year.slice(0, 3)}0s` : 'Undated'
      if (!groups[decade]) groups[decade] = []
      groups[decade].push(e)
    }
    return Object.entries(groups).sort(([a], [b]) => a.localeCompare(b))
  }, [filtered])

  if (loading) return <div className="loading">Loading...</div>
  if (error) return <div className="loading">Error loading biography data.</div>

  return (
    <div className="sidebar-layout">
      {/* Sidebar filters */}
      <div className="sidebar">
        <input
          type="text"
          className="search-input"
          placeholder="Search biography events..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
        />

        <div style={{ marginBottom: '1.5rem' }}>
          <h3>Event Type</h3>
          <ul>
            <li>
              <a
                href="#"
                className={typeFilter === 'all' ? 'active' : ''}
                onClick={e => { e.preventDefault(); setTypeFilter('all') }}
              >
                All events
              </a>
            </li>
            {index?.by_type.map(t => (
              <li key={t.type}>
                <a
                  href="#"
                  className={typeFilter === t.type ? 'active' : ''}
                  onClick={e => { e.preventDefault(); setTypeFilter(t.type) }}
                >
                  {EVENT_TYPE_LABELS[t.type] || t.type}
                  <span style={{ float: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>{t.count}</span>
                </a>
              </li>
            ))}
          </ul>
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <h3>Reliability</h3>
          <ul>
            <li>
              <a
                href="#"
                className={reliabilityFilter === 'all' ? 'active' : ''}
                onClick={e => { e.preventDefault(); setReliabilityFilter('all') }}
              >
                All
              </a>
            </li>
            {Object.entries(index?.reliability_counts || {}).map(([r, c]) => (
              <li key={r}>
                <a
                  href="#"
                  className={reliabilityFilter === r ? 'active' : ''}
                  onClick={e => { e.preventDefault(); setReliabilityFilter(r) }}
                >
                  <span style={{ color: RELIABILITY_COLORS[r] || 'inherit' }}>
                    {r.charAt(0).toUpperCase() + r.slice(1)}
                  </span>
                  <span style={{ float: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>{c}</span>
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Main content */}
      <div>
        <p style={{ color: 'var(--text-muted)', margin: '0 0 1rem', fontSize: '0.9rem' }}>
          {filtered.length} event{filtered.length !== 1 ? 's' : ''} shown
          {index && <span style={{ marginLeft: '0.5rem' }}>of {index.total} total</span>}
        </p>

        {decades.map(([decade, decadeEvents]) => (
          <div key={decade} style={{ marginBottom: '2rem' }}>
            <h2 style={{
              fontFamily: 'var(--font-heading)', fontSize: '1.2rem',
              borderBottom: '2px solid var(--border-light)', paddingBottom: '0.5rem',
              marginBottom: '0.75rem', color: 'var(--accent)',
            }}>
              {decade}
            </h2>
            {decadeEvents.map(event => (
              <AutoEventCard key={event.bio_id} event={event} />
            ))}
          </div>
        ))}

        {filtered.length === 0 && (
          <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
            No events match your filters.
          </p>
        )}
      </div>
    </div>
  )
}

/* ─── Auto-extracted event card ─── */
function AutoEventCard({ event }: { event: BioEvent }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div
      className="card"
      style={{
        borderLeft: `4px solid ${RELIABILITY_COLORS[event.reliability] || '#6c757d'}`,
        cursor: 'pointer',
        marginBottom: '0.75rem',
      }}
      onClick={() => setExpanded(!expanded)}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem' }}>
        <div style={{ flex: 1 }}>
          <span className="badge badge-category" style={{ marginRight: '0.5rem' }}>
            {EVENT_TYPE_LABELS[event.event_type] || event.event_type}
          </span>
          <span className="badge" style={{
            background: RELIABILITY_COLORS[event.reliability] || '#6c757d',
            color: '#fff',
            fontSize: '0.7rem',
          }}>
            {event.reliability}
          </span>
          {event.date_display && (
            <span style={{ marginLeft: '1rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              {event.date_display}
            </span>
          )}
        </div>
      </div>

      <p style={{ margin: '0.5rem 0 0', lineHeight: 1.6 }}>{event.summary}</p>

      {expanded && (
        <div style={{ marginTop: '1rem', paddingTop: '0.75rem', borderTop: '1px solid var(--border-light)' }}>
          {event.detail && <p style={{ fontStyle: 'italic' }}>{event.detail}</p>}

          {event.people_involved && event.people_involved.length > 0 && (
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              People: {event.people_involved.join(', ')}
            </p>
          )}

          {event.source_type && (
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Source: {event.source_type.replace(/_/g, ' ')}
              {event.source_name && ` (${event.source_name})`}
            </p>
          )}

          {event.contradiction_note && (
            <div style={{
              marginTop: '0.5rem', padding: '0.75rem',
              background: '#fff3cd', borderRadius: '4px', fontSize: '0.85rem',
            }}>
              Contradiction: {event.contradiction_note}
            </div>
          )}

          {event.source_seg_id && (
            <Link
              to={`/segments/${event.source_seg_id}`}
              style={{ display: 'inline-block', marginTop: '0.5rem', fontSize: '0.85rem' }}
              onClick={e => e.stopPropagation()}
            >
              View source segment
            </Link>
          )}
        </div>
      )}
    </div>
  )
}

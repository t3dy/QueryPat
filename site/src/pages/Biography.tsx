import { useState, useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useData } from '../hooks/useData'

/* ─── Curated schema (style-audited events) ─── */
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
  theophany_id?: string | null
  theophany_slug?: string | null
}

/* ─── Dictionary index entry ─── */
interface DictEntry {
  canonical_name: string
  slug: string
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
  paranormal_experience: 'Paranormal Experience',
  mystical_experience: 'Mystical Experience',
  gnostic_experience: 'Gnostic Experience',
  hearing_voices_experience: 'Hearing Voices Experience',
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
  paranormal_experience: '#6B8B9B',
  mystical_experience: '#7B6B9B',
  gnostic_experience: '#6B7B9B',
  hearing_voices_experience: '#B06B9B',
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

// type TabId = 'curated' | 'auto'  // Re-enable when auto-extracted tab is restored

/* ═══════════════════════════════════════════════════════
   Main Biography Page
   ═══════════════════════════════════════════════════════ */
export default function Biography() {
  const [searchParams] = useSearchParams()
  const initialQuery = searchParams.get('q') || ''

  return (
    <>
      <div className="page-header">
        <h1>Philip K. Dick &mdash; Biography</h1>
        <p>
          Biographical events drawn from letters, interviews, and secondary sources.
        </p>
      </div>

      <CuratedTab initialQuery={initialQuery} />
    </>
  )
}

/* ═══════════════════════════════════════════════════════
   CURATED TAB — 119 style-audited entries
   ═══════════════════════════════════════════════════════ */
/* ─── Letter-derived (auto-extracted) event ─── */
interface LetterEvent {
  bio_id: number
  summary: string
  date_start: string
  date_end?: string | null
  date_display?: string
  date_confidence?: string
  event_type: string
  location?: string | null
  source_type: string
  source_name?: string
  source_letter_id?: string
  themes?: string  // JSON-encoded array
  notable_correspondence?: string | null
  theophany_id?: string | null
  theophany_slug?: string | null
  evidence_quote?: string | null
}

const THEME_LABELS: Record<string, string> = {
  drugs: 'Drugs',
  music: 'Music',
  career: 'Career',
  relationships: 'Relationships',
  politics: 'Politics',
  religion: 'Religion',
  philosophy: 'Philosophy',
  visionary: 'Visionary',
  sf_community: 'SF Community',
}

const THEME_ORDER = ['drugs', 'music', 'career', 'relationships', 'politics', 'religion', 'philosophy', 'visionary', 'sf_community']

function CuratedTab({ initialQuery = '' }: { initialQuery?: string }) {
  const { data: events, loading, error } = useData<CuratedBioEvent[]>('biography/curated.json')
  const { data: rawLetterEvents } = useData<LetterEvent[]>('biography/events.json')
  const { data: dictIndex } = useData<DictEntry[]>('dictionary/index.json')

  // Filter letter-source events from the events.json list (it contains 646 auto-extracted + 18 letter-derived)
  const letterEvents = useMemo(() => {
    return (rawLetterEvents || []).filter(e => e.source_type === 'letter')
  }, [rawLetterEvents])

  const [activeCategory, setActiveCategory] = useState<string | null>(null)
  const [activeEra, setActiveEra] = useState<number | null>(null)
  const [activeThemes, setActiveThemes] = useState<Set<string>>(new Set())
  const [minImportance, setMinImportance] = useState(0)
  const [searchQuery, setSearchQuery] = useState(initialQuery)
  const [showLetters] = useState(true)

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
    // Themes filter doesn't apply to curated events (no themes data yet); hide the curated list when filtering by theme
    if (activeThemes.size > 0) {
      filtered = []
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
  }, [events, activeCategory, activeEra, minImportance, searchQuery, activeThemes])

  const filteredLetterEvents = useMemo(() => {
    if (!showLetters) return []
    let filtered = letterEvents
    if (activeEra !== null) {
      const [, start, end] = ERA_RANGES[activeEra]
      filtered = filtered.filter(e => {
        const y = getYear(e.date_start || '')
        return y >= start && y <= end
      })
    }
    if (activeThemes.size > 0) {
      filtered = filtered.filter(e => {
        try {
          const themes: string[] = JSON.parse(e.themes || '[]')
          return themes.some(t => activeThemes.has(t))
        } catch { return false }
      })
    }
    if (searchQuery) {
      const q = searchQuery.toLowerCase()
      filtered = filtered.filter(e =>
        (e.summary || '').toLowerCase().includes(q) ||
        (e.date_start || '').includes(q) ||
        (e.source_letter_id || '').toLowerCase().includes(q) ||
        (e.location || '').toLowerCase().includes(q)
      )
    }
    return filtered
  }, [letterEvents, showLetters, activeEra, activeThemes, searchQuery])

  const categoryCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    if (!events) return counts
    for (const e of events) {
      counts[e.category] = (counts[e.category] || 0) + 1
    }
    return counts
  }, [events])

  const themeCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    for (const e of letterEvents) {
      try {
        const themes: string[] = JSON.parse(e.themes || '[]')
        for (const t of themes) counts[t] = (counts[t] || 0) + 1
      } catch { continue }
    }
    return counts
  }, [letterEvents])

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
          <h3>Themes <span style={{fontSize:'0.75rem', color:'var(--text-muted)', fontWeight:'normal'}}>(letters)</span></h3>
          <ul>
            <li>
              <a
                href="#"
                className={activeThemes.size === 0 ? 'active' : ''}
                onClick={e => { e.preventDefault(); setActiveThemes(new Set()) }}
              >
                All ({letterEvents.length})
              </a>
            </li>
            {THEME_ORDER.filter(t => themeCounts[t]).map(t => {
              const isActive = activeThemes.has(t)
              return (
                <li key={t}>
                  <a
                    href="#"
                    className={isActive ? 'active' : ''}
                    onClick={e => {
                      e.preventDefault()
                      const next = new Set(activeThemes)
                      if (isActive) next.delete(t)
                      else next.add(t)
                      setActiveThemes(next)
                    }}
                  >
                    {THEME_LABELS[t] || t}
                    <span style={{ float: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                      {themeCounts[t]}
                    </span>
                  </a>
                </li>
              )
            })}
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
          {filteredEvents.length} curated event{filteredEvents.length !== 1 ? 's' : ''}
          {filteredLetterEvents.length > 0 && ` · ${filteredLetterEvents.length} from letters`}
          {minImportance > 0 && (
            <span style={{ marginLeft: '0.5rem' }}>(importance &ge; {minImportance})</span>
          )}
          {activeThemes.size > 0 && (
            <span style={{ marginLeft: '0.5rem', color: '#9B6B9B' }}>
              themes: {[...activeThemes].join(', ')}
            </span>
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

        {filteredLetterEvents.length > 0 && (
          <>
            <h2 style={{
              marginTop: filteredEvents.length > 0 ? '2rem' : 0,
              borderBottom: '1px solid var(--border, rgba(0,0,0,0.1))',
              paddingBottom: '0.5rem',
            }}>
              From the <em>Selected Letters</em>
              <span style={{ float: 'right', color: 'var(--text-muted)', fontSize: '0.85rem', fontWeight: 'normal' }}>
                {filteredLetterEvents.length} event{filteredLetterEvents.length !== 1 ? 's' : ''}
              </span>
            </h2>
            {filteredLetterEvents.map(ev => <LetterEventCard key={ev.bio_id} event={ev} />)}
          </>
        )}

        {filteredEvents.length === 0 && filteredLetterEvents.length === 0 && (
          <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
            No events match the current filters.
          </p>
        )}
      </div>
    </div>
  )
}

/* ─── Letter-derived event card ─── */
function LetterEventCard({ event }: { event: LetterEvent }) {
  const themes: string[] = (() => { try { return JSON.parse(event.themes || '[]') } catch { return [] } })()
  return (
    <div className="card" style={{ borderLeft: '4px solid #7B8FA1', marginBottom: '0.75rem', background: 'rgba(123,143,161,0.04)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem' }}>
        <span style={{
          fontFamily: 'var(--font-mono)', fontSize: '0.85rem',
          color: 'var(--text-secondary)', fontVariantNumeric: 'tabular-nums',
        }}>
          {event.date_start || event.date_display}
        </span>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          letter
        </span>
      </div>
      <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.95rem', margin: '0.5rem 0', lineHeight: 1.6 }}>
        {event.summary}
      </p>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.5rem', alignItems: 'center' }}>
        {themes.map(t => (
          <span key={t} className="badge" style={{
            background: 'rgba(123,143,161,0.15)', color: '#7B8FA1',
            border: '1px solid rgba(123,143,161,0.4)', fontSize: '0.7rem',
          }}>
            {THEME_LABELS[t] || t}
          </span>
        ))}
        {event.notable_correspondence && (
          <span className="badge" style={{
            background: 'rgba(192,154,77,0.15)', color: 'var(--accent)',
            border: '1px solid rgba(192,154,77,0.4)', fontSize: '0.7rem',
          }}>
            {event.notable_correspondence.replace(/_/g, ' ')}
          </span>
        )}
        {event.theophany_id && (
          <Link
            to={`/theophanies/${event.theophany_slug || event.theophany_id.replace(/^THEO_/, '').toLowerCase().replace(/_/g, '-')}`}
            style={{
              background: '#9B6B9B', color: '#fff',
              padding: '0.15rem 0.4rem', fontSize: '0.7rem',
              borderRadius: '3px', textDecoration: 'none',
              textTransform: 'uppercase', letterSpacing: '0.05em',
            }}
          >
            → vision
          </Link>
        )}
      </div>
      {event.evidence_quote && (
        <blockquote style={{
          fontSize: '0.85rem', color: 'var(--text-muted)',
          borderLeft: '2px solid var(--border, rgba(0,0,0,0.1))',
          padding: '0 0.75rem', margin: '0.5rem 0 0', fontStyle: 'italic',
        }}>
          "{event.evidence_quote}"
        </blockquote>
      )}
      {event.source_letter_id && (
        <p style={{ color: 'var(--text-muted)', fontSize: '0.75rem', margin: '0.4rem 0 0' }}>
          Source: {event.source_letter_id}
        </p>
      )}
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

      {event.theophany_id && (
        <Link
          to={`/theophanies/${event.theophany_slug || event.theophany_id.replace(/^THEO_/, '').toLowerCase().replace(/_/g, '-')}`}
          style={{
            display: 'inline-block', marginTop: '0.4rem',
            background: '#9B6B9B', color: '#fff',
            padding: '0.15rem 0.5rem', fontSize: '0.7rem',
            borderRadius: '3px', textDecoration: 'none',
            textTransform: 'uppercase', letterSpacing: '0.05em',
          }}
        >
          → linked theophany
        </Link>
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

/* AutoExtractedTab and AutoEventCard removed — code is in git history.
   Re-add when auto-extracted biography data is ready for display. */

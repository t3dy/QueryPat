import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

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

export default function Biography() {
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
    <>
      <div className="page-header">
        <h1>Philip K. Dick — Biography</h1>
        <p>
          Biographical events extracted from the Exegesis, letters, interviews, and secondary sources.
          {index && <span style={{ marginLeft: '1rem', color: 'var(--text-muted)' }}>{index.total} events</span>}
        </p>
      </div>

      <div style={{ display: 'flex', gap: '2rem', alignItems: 'flex-start' }}>
        {/* Sidebar filters */}
        <div className="category-sidebar">
          <h3>Event Type</h3>
          <div
            className={`category-item ${typeFilter === 'all' ? 'active' : ''}`}
            onClick={() => setTypeFilter('all')}
          >
            All events
          </div>
          {index?.by_type.map(t => (
            <div
              key={t.type}
              className={`category-item ${typeFilter === t.type ? 'active' : ''}`}
              onClick={() => setTypeFilter(t.type)}
            >
              {EVENT_TYPE_LABELS[t.type] || t.type}
              <span className="category-count">{t.count}</span>
            </div>
          ))}

          <h3 style={{ marginTop: '1.5rem' }}>Reliability</h3>
          <div
            className={`category-item ${reliabilityFilter === 'all' ? 'active' : ''}`}
            onClick={() => setReliabilityFilter('all')}
          >
            All
          </div>
          {Object.entries(index?.reliability_counts || {}).map(([r, c]) => (
            <div
              key={r}
              className={`category-item ${reliabilityFilter === r ? 'active' : ''}`}
              onClick={() => setReliabilityFilter(r)}
            >
              <span style={{ color: RELIABILITY_COLORS[r] || 'inherit' }}>
                {r.charAt(0).toUpperCase() + r.slice(1)}
              </span>
              <span className="category-count">{c}</span>
            </div>
          ))}
        </div>

        {/* Main content */}
        <div style={{ flex: 1 }}>
          <input
            type="text"
            className="search-input"
            placeholder="Search biography events..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
          />

          <p style={{ color: 'var(--text-muted)', margin: '0.5rem 0 1.5rem' }}>
            {filtered.length} event{filtered.length !== 1 ? 's' : ''} shown
          </p>

          {decades.map(([decade, events]) => (
            <div key={decade} style={{ marginBottom: '2rem' }}>
              <h2 style={{ borderBottom: '2px solid var(--border-light)', paddingBottom: '0.5rem' }}>
                {decade}
              </h2>
              {events.map(event => (
                <BioEventCard key={event.bio_id} event={event} />
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
    </>
  )
}

function BioEventCard({ event }: { event: BioEvent }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div
      className="card"
      style={{
        borderLeft: `4px solid ${RELIABILITY_COLORS[event.reliability] || '#6c757d'}`,
        cursor: 'pointer',
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

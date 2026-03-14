import { useState, useMemo } from 'react'
import { Link, useParams, NavLink } from 'react-router-dom'
import { useData } from '../hooks/useData'
import { formatSegmentTitle } from '../utils/formatTitle'

interface TimelineIndex {
  year: string
  count: number
  bio_events?: number
}

interface Segment {
  seg_id: string
  slug: string
  title: string
  date_display: string
  date_confidence: string
  concise_summary: string
  recurring_concepts: string[] | null
  people_entities: string[] | null
  word_count: number
}

interface BioEvent {
  bio_id: string
  summary: string
  date_start: string
  date_end: string | null
  event_type: string
  source_name: string
  date_confidence: string | null
  location: string | null
  _type: 'biography_event'
}

type TimelineEntry = Segment | BioEvent

function isBioEvent(entry: TimelineEntry): entry is BioEvent {
  return '_type' in entry && (entry as BioEvent)._type === 'biography_event'
}

export default function Timeline() {
  const { year } = useParams()
  const { data: index } = useData<TimelineIndex[]>('timeline/index.json')
  const selectedYear = year || (index && index.length > 0 ? index[0].year : null)
  const { data: entries, loading } = useData<TimelineEntry[]>(
    selectedYear ? `timeline/years/${selectedYear}.json` : null
  )
  const [search, setSearch] = useState('')

  const filtered = useMemo(() => {
    if (!entries || !Array.isArray(entries)) return []
    if (!search) return entries
    const q = search.toLowerCase()
    return entries.filter(entry => {
      if (isBioEvent(entry)) {
        return (entry.summary || '').toLowerCase().includes(q) ||
          (entry.event_type || '').toLowerCase().includes(q) ||
          (entry.location || '').toLowerCase().includes(q)
      }
      const s = entry as Segment
      return (s.concise_summary || '').toLowerCase().includes(q) ||
        (s.title || '').toLowerCase().includes(q) ||
        (s.recurring_concepts || []).some(c => c.toLowerCase().includes(q)) ||
        (s.people_entities || []).some(p => p.toLowerCase().includes(q))
    })
  }, [entries, search])

  return (
    <>
      <div className="page-header">
        <h1>Exegesis Timeline</h1>
        <p>Browse Philip K. Dick's <em>Exegesis</em> writings in chronological order</p>
      </div>

      <div className="sidebar-layout">
        <div className="sidebar">
          <h3>Years</h3>
          <ul>
            {index?.map(y => (
              <li key={y.year}>
                <NavLink to={`/timeline/${y.year}`}>
                  {y.year} <span style={{opacity:0.5}}>
                    ({y.count || 0}{y.bio_events ? `+${y.bio_events}` : ''})
                  </span>
                </NavLink>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <input
            className="search-input"
            type="text"
            placeholder="Filter segments..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />

          {loading ? (
            <div className="loading">Loading...</div>
          ) : (
            <>
              <p style={{color:'var(--text-muted)', marginBottom:'1rem', fontSize:'0.85rem'}}>
                {filtered.length} entr{filtered.length !== 1 ? 'ies' : 'y'} in {selectedYear}
              </p>
              {filtered.map((entry, i) => {
                if (isBioEvent(entry)) {
                  return (
                    <div key={`bio-${entry.bio_id || i}`} className="card" style={{marginBottom:'0.75rem', borderLeft:'3px solid var(--accent)'}}>
                      <div className="card-meta">
                        <span>{entry.date_start}</span>
                        <span className="badge badge-category">{entry.event_type || 'biography'}</span>
                        {entry.source_name && <span style={{opacity:0.6}}>{entry.source_name}</span>}
                      </div>
                      <p style={{marginTop:'0.5rem'}}>{entry.summary}</p>
                      {entry.location && (
                        <p style={{color:'var(--text-muted)', fontSize:'0.8rem', margin:'0.25rem 0 0'}}>
                          {entry.location}
                        </p>
                      )}
                    </div>
                  )
                }
                const seg = entry as Segment
                return (
                  <div key={seg.seg_id} className="card" style={{marginBottom:'0.75rem'}}>
                    <h3>
                      <Link to={`/segments/${seg.seg_id}`}>{formatSegmentTitle(seg.title, seg.seg_id)}</Link>
                    </h3>
                    <div className="card-meta">
                      <span>{seg.date_display}</span>
                      {seg.word_count && <span>{seg.word_count.toLocaleString()} words</span>}
                      {seg.date_confidence && seg.date_confidence !== 'exact' && (
                        <span className="badge badge-category">{seg.date_confidence}</span>
                      )}
                    </div>
                    {seg.concise_summary && (
                      <p style={{marginTop:'0.5rem'}}>{seg.concise_summary}</p>
                    )}
                    {seg.recurring_concepts && seg.recurring_concepts.length > 0 && (
                      <div style={{display:'flex', flexWrap:'wrap', gap:'0.35rem', marginTop:'0.5rem'}}>
                        {seg.recurring_concepts.slice(0, 5).map(c => (
                          <span key={c} className="badge badge-category">{c}</span>
                        ))}
                      </div>
                    )}
                  </div>
                )
              })}
            </>
          )}
        </div>
      </div>
    </>
  )
}

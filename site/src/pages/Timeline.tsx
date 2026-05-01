import { useState, useMemo } from 'react'
import { Link, useParams, NavLink } from 'react-router-dom'
import { useData } from '../hooks/useData'
import { formatSegmentTitle } from '../utils/formatTitle'

interface TimelineIndex {
  year: string
  count: number
  bio_events?: number
  theophanies?: number
  total?: number
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
  theophany_id?: string | null
  theophany_slug?: string | null
  _type: 'biography_event'
}

interface TheophanyEntry {
  theophany_id: string
  name: string
  slug: string
  summary: string
  date_start: string
  date_end: string
  date_display: string
  date_confidence: string
  experience_type: string
  importance: string
  contested_status: string
  parent_theophany_id: string | null
  _type: 'theophany'
}

type TimelineEntry = Segment | BioEvent | TheophanyEntry

function isBioEvent(entry: TimelineEntry): entry is BioEvent {
  return '_type' in entry && (entry as BioEvent)._type === 'biography_event'
}

function isTheophany(entry: TimelineEntry): entry is TheophanyEntry {
  return '_type' in entry && (entry as TheophanyEntry)._type === 'theophany'
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
      if (isTheophany(entry)) {
        return (entry.summary || '').toLowerCase().includes(q) ||
          (entry.name || '').toLowerCase().includes(q) ||
          (entry.experience_type || '').toLowerCase().includes(q)
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
        <h1>Timeline</h1>
        <p>Philip K. Dick's life (1928&ndash;1982) &mdash; biography events, <em>Exegesis</em> writings, and visionary experiences arrayed by year</p>
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
                if (isTheophany(entry)) {
                  return (
                    <div key={`theo-${entry.theophany_id}-${i}`} className="card" style={{marginBottom:'0.75rem', borderLeft:'3px solid #9B6B9B', background:'rgba(155, 107, 155, 0.05)'}}>
                      <div className="card-meta">
                        <span>{entry.date_display}</span>
                        <span className="badge badge-category" style={{background:'#9B6B9B', color:'#fff'}}>theophany &middot; {entry.experience_type}</span>
                        {entry.importance === 'canonical' && <span style={{fontSize:'0.7rem', padding:'0.1rem 0.35rem', background:'var(--accent)', color:'#fff', borderRadius:'3px'}}>canonical</span>}
                      </div>
                      <h3 style={{margin:'0.5rem 0 0.25rem'}}>
                        <Link to={`/theophanies/${entry.slug}`}>{entry.name}</Link>
                      </h3>
                      <p style={{marginTop:'0.25rem'}}>{entry.summary}</p>
                    </div>
                  )
                }
                if (isBioEvent(entry)) {
                  const theoSlug = entry.theophany_slug || (entry.theophany_id
                    ? entry.theophany_id.replace(/^THEO_/, '').toLowerCase().replace(/_/g, '-')
                    : null)
                  return (
                    <div key={`bio-${entry.bio_id || i}`} className="card" style={{marginBottom:'0.75rem', borderLeft:'3px solid var(--accent)'}}>
                      <div className="card-meta">
                        <span>{entry.date_start}</span>
                        <span className="badge badge-category">{entry.event_type || 'biography'}</span>
                        {entry.source_name && <span style={{opacity:0.6}}>{entry.source_name}</span>}
                        {entry.theophany_id && theoSlug && (
                          <Link to={`/theophanies/${theoSlug}`} style={{
                            background:'#9B6B9B', color:'#fff',
                            padding:'0.1rem 0.4rem', fontSize:'0.7rem',
                            borderRadius:'3px', textDecoration:'none',
                            textTransform:'uppercase', letterSpacing:'0.03em',
                          }}>
                            ← vision
                          </Link>
                        )}
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

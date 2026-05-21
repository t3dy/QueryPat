import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

const LANE_LABELS: Record<string, string> = {
  A: 'Fiction', B: 'Exegesis', C: 'Scholarship', D: 'Synthesis', E: 'Primary'
}

const LANE_COLORS: Record<string, string> = {
  A: '#8b5cf6', B: '#d97706', C: '#2563eb', D: '#059669', E: '#dc2626'
}

interface ArchiveEntry {
  doc_id: string
  title: string
  slug: string
  author: string
  doc_type: string
  category: string
  date_display: string
  date_start: string
  is_pkd_authored: boolean
  card_summary: string
  page_count: number
  ingest_level: string
  evidentiary_lane: string | null
  people_mentioned: string[]
  works_discussed: string[]
  linked_terms: string[]
}

export default function Archive() {
  const { data: entries, loading } = useData<ArchiveEntry[]>('archive/index.json')
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState<string>('all')
  const [lane, setLane] = useState<string>('all')
  const [sortBy, setSortBy] = useState<string>('date')

  const categories = useMemo(() => {
    if (!entries) return []
    const cats = new Set(entries.map(e => e.category).filter(Boolean))
    return ['all', ...Array.from(cats).sort()]
  }, [entries])

  const lanes = useMemo(() => {
    if (!entries) return []
    const laneSet = new Set(entries.map(e => e.evidentiary_lane).filter(Boolean) as string[])
    return ['all', ...Array.from(laneSet).sort()]
  }, [entries])

  const filtered = useMemo(() => {
    if (!entries) return []
    let result = entries
    if (category !== 'all') {
      result = result.filter(e => e.category === category)
    }
    if (lane !== 'all') {
      result = result.filter(e => e.evidentiary_lane === lane)
    }
    if (search) {
      const q = search.toLowerCase()
      result = result.filter(e =>
        (e.title || '').toLowerCase().includes(q) ||
        (e.author || '').toLowerCase().includes(q) ||
        (e.card_summary || '').toLowerCase().includes(q)
      )
    }
    return [...result].sort((a, b) => {
      if (sortBy === 'title') return (a.title || '').localeCompare(b.title || '')
      if (sortBy === 'pages') return (b.page_count || 0) - (a.page_count || 0)
      if (sortBy === 'relationships') {
        const ar = (a.people_mentioned?.length || 0) + (a.works_discussed?.length || 0) + (a.linked_terms?.length || 0)
        const br = (b.people_mentioned?.length || 0) + (b.works_discussed?.length || 0) + (b.linked_terms?.length || 0)
        return br - ar || (a.title || '').localeCompare(b.title || '')
      }
      return (b.date_start || '').localeCompare(a.date_start || '') || (a.title || '').localeCompare(b.title || '')
    })
  }, [entries, search, category, lane, sortBy])

  if (loading) return <div className="loading">Loading...</div>

  return (
    <>
      <div className="page-header">
        <h1>Archive</h1>
        <p>{entries?.length} documents ({filtered.length} shown)</p>
      </div>

      <div className="sidebar-layout">
        <div className="sidebar">
          <h3>Categories</h3>
          <ul>
            {categories.map(c => (
              <li key={c}>
                <a
                  href="#"
                  className={category === c ? 'active' : ''}
                  onClick={e => { e.preventDefault(); setCategory(c) }}
                >
                  {c === 'all' ? 'All' : c}
                  {c !== 'all' && (
                    <span style={{opacity:0.5, marginLeft:'0.25rem'}}>
                      ({entries?.filter(e => e.category === c).length})
                    </span>
                  )}
                </a>
              </li>
            ))}
          </ul>

          <h3 style={{ marginTop: '1.5rem' }}>Evidence Lane</h3>
          <ul>
            {lanes.map(l => (
              <li key={l}>
                <a
                  href="#"
                  className={lane === l ? 'active' : ''}
                  onClick={e => { e.preventDefault(); setLane(l) }}
                >
                  {l === 'all' ? 'All Lanes' : LANE_LABELS[l] || l}
                  {l !== 'all' && (
                    <span style={{opacity:0.5, marginLeft:'0.25rem'}}>
                      ({entries?.filter(e => e.evidentiary_lane === l).length})
                    </span>
                  )}
                </a>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <div className="toolbar-row">
            <input
              className="search-input"
              type="text"
              placeholder="Search archive..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <select className="filter-select" value={sortBy} onChange={e => setSortBy(e.target.value)} aria-label="Sort archive">
              <option value="date">Newest First</option>
              <option value="title">Title</option>
              <option value="pages">Page Count</option>
              <option value="relationships">Most Linked</option>
            </select>
          </div>

          <div className="card-grid">
            {filtered.map(entry => (
              <div key={entry.doc_id} className="card">
                <h3>
                  <Link to={`/archive/${entry.slug}`}>{entry.title}</Link>
                </h3>
                <div className="card-meta">
                  {entry.author && <span>{entry.author}</span>}
                  {entry.date_display && entry.date_display !== 'Unknown' && <span>{entry.date_display}</span>}
                  {entry.page_count && <span>{entry.page_count} pp</span>}
                  <span className="badge badge-category">{entry.category}</span>
                  {entry.is_pkd_authored && <span className="badge badge-provisional">PKD</span>}
                  {entry.evidentiary_lane && (
                    <span className="badge" style={{
                      background: LANE_COLORS[entry.evidentiary_lane] || 'var(--border-light)',
                      color: '#fff', fontSize: '0.7rem'
                    }}>
                      {LANE_LABELS[entry.evidentiary_lane] || entry.evidentiary_lane}
                    </span>
                  )}
                </div>
                {entry.card_summary && (
                  <p style={{marginTop:'0.5rem'}}>
                    {entry.card_summary.slice(0, 200)}
                    {entry.card_summary.length > 200 ? '...' : ''}
                  </p>
                )}
                {((entry.people_mentioned?.length > 0) || (entry.works_discussed?.length > 0) || (entry.linked_terms?.length > 0)) && (
                  <div style={{fontSize:'0.75rem', color:'var(--text-muted)', marginTop:'0.35rem'}}>
                    {[
                      entry.people_mentioned?.length > 0 && `${entry.people_mentioned.length} people`,
                      entry.works_discussed?.length > 0 && `${entry.works_discussed.length} works`,
                      entry.linked_terms?.length > 0 && `${entry.linked_terms.length} terms`,
                    ].filter(Boolean).join(' \u00b7 ')}
                  </div>
                )}
              </div>
            ))}
          </div>

          {filtered.length === 0 && (
            <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
              No documents match the current filters.
            </p>
          )}
        </div>
      </div>
    </>
  )
}

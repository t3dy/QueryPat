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

  const categories = useMemo(() => {
    if (!entries) return []
    const cats = new Set(entries.map(e => e.category).filter(Boolean))
    return ['all', ...Array.from(cats).sort()]
  }, [entries])

  const filtered = useMemo(() => {
    if (!entries) return []
    let result = entries
    if (category !== 'all') {
      result = result.filter(e => e.category === category)
    }
    if (search) {
      const q = search.toLowerCase()
      result = result.filter(e =>
        (e.title || '').toLowerCase().includes(q) ||
        (e.author || '').toLowerCase().includes(q) ||
        (e.card_summary || '').toLowerCase().includes(q)
      )
    }
    return result
  }, [entries, search, category])

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
        </div>

        <div>
          <input
            className="search-input"
            type="text"
            placeholder="Search archive..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />

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

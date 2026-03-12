import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

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
                </div>
                {entry.card_summary && (
                  <p style={{marginTop:'0.5rem'}}>
                    {entry.card_summary.slice(0, 200)}
                    {entry.card_summary.length > 200 ? '...' : ''}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}

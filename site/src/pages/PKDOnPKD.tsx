import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface TopSource {
  doc_id: string
  doc_slug: string
  doc_title: string
  doc_type: string
  date_display: string
  mention_count: number
}

interface PKDOnPKDIndexRow {
  work_id: string
  canonical_title: string
  slug: string
  author: string
  work_type: string
  category: string
  mention_count: number
  source_doc_count: number
  source_doc_types: Record<string, number>
  card_summary: string
  page_summary: string
  top_sources: TopSource[]
}

const SOURCE_LABELS: Record<string, string> = {
  archive_pdf: 'Primary text',
  biography: 'Biography',
  exegesis_section: 'Exegesis',
  fan_publication: 'Fan publication',
  interview: 'Interview',
  letter: 'Letter',
  novel: 'Novel',
  scholarship: 'Scholarship',
  short_story: 'Short story',
  other: 'Other writing',
}

const SORT_LABELS: Record<string, string> = {
  mentions: 'Most Mentions',
  sources: 'Most Sources',
  title: 'Title',
}

export default function PKDOnPKD() {
  const { data: records, loading } = useData<PKDOnPKDIndexRow[]>('pkd-on-pkd/index.json')
  const [search, setSearch] = useState('')
  const [sourceType, setSourceType] = useState('all')
  const [sortBy, setSortBy] = useState('mentions')

  const sourceTypes = useMemo(() => {
    if (!records) return []
    const counts = new Map<string, number>()
    for (const row of records) {
      for (const [type, count] of Object.entries(row.source_doc_types || {})) {
        counts.set(type, (counts.get(type) || 0) + (count > 0 ? 1 : 0))
      }
    }
    return Array.from(counts.entries()).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
  }, [records])

  const filtered = useMemo(() => {
    if (!records) return []
    const q = search.toLowerCase()
    const result = records.filter(row => {
      if (sourceType !== 'all' && !(row.source_doc_types || {})[sourceType]) return false
      if (!q) return true
      return (
        row.canonical_title.toLowerCase().includes(q) ||
        (row.card_summary || '').toLowerCase().includes(q) ||
        (row.page_summary || '').toLowerCase().includes(q)
      )
    })

    return [...result].sort((a, b) => {
      if (sortBy === 'title') return a.canonical_title.localeCompare(b.canonical_title)
      if (sortBy === 'sources') return (b.source_doc_count || 0) - (a.source_doc_count || 0) || a.canonical_title.localeCompare(b.canonical_title)
      return (b.mention_count || 0) - (a.mention_count || 0) || a.canonical_title.localeCompare(b.canonical_title)
    })
  }, [records, search, sourceType, sortBy])

  if (loading) return <div className="loading">Loading PKD on PKD...</div>

  return (
    <>
      <div className="page-header">
        <h1>PKD on PKD</h1>
        <p>
          {records?.length} novels catalogued by the places PKD mentions them in letters, interviews,
          the Exegesis, and other PKD-authored writings.
        </p>
      </div>

      <div className="sidebar-layout">
        <div className="sidebar">
          <h3>Source Type</h3>
          <ul>
            <li>
              <a href="#" className={sourceType === 'all' ? 'active' : ''} onClick={e => { e.preventDefault(); setSourceType('all') }}>
                All Sources
              </a>
            </li>
            {sourceTypes.map(([type, count]) => (
              <li key={type}>
                <a href="#" className={sourceType === type ? 'active' : ''} onClick={e => { e.preventDefault(); setSourceType(type) }}>
                  {SOURCE_LABELS[type] || type.replace(/_/g, ' ')}
                  <span style={{ float: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>{count}</span>
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
              placeholder="Search novels or summaries..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <select className="filter-select" value={sortBy} onChange={e => setSortBy(e.target.value)} aria-label="Sort PKD on PKD">
              {Object.entries(SORT_LABELS).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </div>

          <div className="card-grid">
            {filtered.map(row => (
              <div key={row.work_id} className="card">
                <h3>
                  <Link to={`/pkd-on-pkd/${row.slug}`}>{row.canonical_title}</Link>
                </h3>
                <div className="card-meta">
                  <span>{row.mention_count} mention{row.mention_count === 1 ? '' : 's'}</span>
                  <span>{row.source_doc_count} source{row.source_doc_count === 1 ? '' : 's'}</span>
                  <span className="badge badge-category">{row.category}</span>
                  <span>{SOURCE_LABELS[row.work_type] || row.work_type}</span>
                </div>
                <p style={{ marginTop: '0.5rem' }}>{row.card_summary}</p>
                {row.top_sources?.length > 0 && (
                  <div className="card-meta" style={{ marginTop: '0.75rem' }}>
                    {row.top_sources.slice(0, 3).map(source => (
                      <span key={source.doc_id} className="badge badge-background">
                        {source.doc_title} ({source.mention_count})
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}

import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface TermSummary {
  term_id: string
  canonical_name: string
  slug: string
  status: string
  review_state: string
  primary_category: string
  mention_count: number
  card_description: string
  first_appearance: string
  peak_usage_start: string
}

export default function Dictionary() {
  const { data: terms, loading } = useData<TermSummary[]>('dictionary/index.json')
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState<string>('all')

  const categories = useMemo(() => {
    if (!terms) return []
    const cats = new Set(terms.map(t => t.primary_category).filter(Boolean))
    return ['all', ...Array.from(cats).sort()]
  }, [terms])

  const filtered = useMemo(() => {
    if (!terms) return []
    let result = terms
    if (category !== 'all') {
      result = result.filter(t => t.primary_category === category)
    }
    if (search) {
      const q = search.toLowerCase()
      result = result.filter(t =>
        t.canonical_name.toLowerCase().includes(q) ||
        (t.card_description || '').toLowerCase().includes(q) ||
        (t.primary_category || '').toLowerCase().includes(q)
      )
    }
    return result
  }, [terms, search, category])

  if (loading) return <div className="loading">Loading...</div>

  return (
    <>
      <div className="page-header">
        <h1>Dictionary</h1>
        <p>{terms?.length} terms ({filtered.length} shown)</p>
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
                  {c === 'all' ? 'All Categories' : c}
                  {c !== 'all' && (
                    <span style={{opacity:0.5, marginLeft:'0.25rem'}}>
                      ({terms?.filter(t => t.primary_category === c).length})
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
            placeholder="Search terms..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />

          <div className="card-grid">
            {filtered.map(term => (
              <div key={term.term_id} className="card">
                <h3>
                  <Link to={`/dictionary/${term.slug}`}>{term.canonical_name}</Link>
                </h3>
                <div className="card-meta">
                  <span>{term.mention_count.toLocaleString()} mentions</span>
                  <span className={`badge badge-${term.status}`}>{term.status}</span>
                  {term.primary_category && (
                    <span className="badge badge-category">{term.primary_category}</span>
                  )}
                  {term.review_state !== 'unreviewed' && (
                    <span className="confidence-label">{term.review_state}</span>
                  )}
                </div>
                {term.card_description && (
                  <p style={{marginTop:'0.5rem'}}>
                    {term.card_description.slice(0, 200)}
                    {term.card_description.length > 200 ? '...' : ''}
                  </p>
                )}
                {term.first_appearance && (
                  <div className="card-meta">
                    <span>First: {term.first_appearance}</span>
                    {term.peak_usage_start && <span>Peak: {term.peak_usage_start}</span>}
                  </div>
                )}
              </div>
            ))}
          </div>

          {filtered.length === 0 && (
            <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
              No terms match the current filters.
            </p>
          )}
        </div>
      </div>
    </>
  )
}

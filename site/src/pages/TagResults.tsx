import { useMemo } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useData } from '../hooks/useData'
import { formatSegmentTitle } from '../utils/formatTitle'

interface SearchEntry {
  type: 'segment' | 'term' | 'archive' | 'name' | 'biography'
  id: string
  slug: string
  title: string
  text: string
  date?: string
  author?: string
  category?: string
}

const GROUP_ORDER: { type: string; label: string }[] = [
  { type: 'term', label: 'Dictionary Terms' },
  { type: 'biography', label: 'Biography Events' },
  { type: 'segment', label: 'Exegesis Summaries' },
  { type: 'name', label: 'Names' },
  { type: 'archive', label: 'Archive Documents' },
]

function getLink(entry: SearchEntry): string {
  switch (entry.type) {
    case 'segment': return `/segments/${entry.id}`
    case 'term': return `/dictionary/${entry.slug}`
    case 'archive': return `/archive/${entry.slug}`
    case 'name': return `/names/${entry.slug}`
    case 'biography': return `/biography`
    default: return '/'
  }
}

export default function TagResults() {
  const { tagname } = useParams()
  const { data: entries, loading } = useData<SearchEntry[]>('search_index.json')

  const tag = decodeURIComponent(tagname || '').toLowerCase()
  const tagDisplay = decodeURIComponent(tagname || '').replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase())

  const grouped = useMemo(() => {
    if (!entries || !tag) return []
    // Exact match on tag in title, text, or category
    const matches = entries.filter(e => {
      const titleLower = (e.title || '').toLowerCase()
      const textLower = (e.text || '').toLowerCase()
      const catLower = (e.category || '').toLowerCase()
      return titleLower.includes(tag) || textLower.includes(tag) || catLower.includes(tag)
    })

    return GROUP_ORDER.map(g => ({
      ...g,
      items: matches.filter(m => m.type === g.type),
    })).filter(g => g.items.length > 0)
  }, [entries, tag])

  const totalCount = grouped.reduce((sum, g) => sum + g.items.length, 0)

  if (loading) return <div className="loading">Loading...</div>

  return (
    <>
      <div className="page-header">
        <h1>{tagDisplay}</h1>
        <p>Everything in the Knowledge Portal related to this concept ({totalCount} results)</p>
      </div>

      {totalCount === 0 && (
        <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
          No results found for "{tagDisplay}".
        </p>
      )}

      {grouped.map(g => (
        <GroupedSection key={g.type} label={g.label} items={g.items} />
      ))}
    </>
  )
}

function GroupedSection({ label, items }: { label: string; items: SearchEntry[] }) {
  const INITIAL = 5
  const showAll = items.length <= INITIAL

  return (
    <div className="search-group">
      <h2 className="search-group-title">
        {label}
        <span className="search-group-count">{items.length}</span>
      </h2>
      {(showAll ? items : items.slice(0, INITIAL)).map(item => (
        <div key={`${item.type}-${item.id}`} className="card" style={{ marginBottom: '0.5rem' }}>
          <h3>
            <Link to={getLink(item)}>
              {item.type === 'segment' ? formatSegmentTitle(item.title) : item.title}
            </Link>
          </h3>
          <div className="card-meta">
            {item.date && <span>{item.date}</span>}
            {item.category && <span className="badge badge-category">{item.category}</span>}
          </div>
          {item.text && (
            <p style={{ marginTop: '0.35rem', fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
              {item.text.slice(0, 160)}{item.text.length > 160 ? '...' : ''}
            </p>
          )}
        </div>
      ))}
      {!showAll && (
        <Link to={`/search?q=${encodeURIComponent(label.split(' ')[0])}`} style={{ fontSize: '0.9rem' }}>
          Show all {items.length} &rarr;
        </Link>
      )}
    </div>
  )
}

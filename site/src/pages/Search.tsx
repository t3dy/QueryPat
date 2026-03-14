import { useState, useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useData } from '../hooks/useData'
import Fuse from 'fuse.js'
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

const TYPE_LABELS: Record<string, string> = {
  segment: 'Exegesis Summary',
  term: 'Dictionary Term',
  archive: 'Archive Document',
  name: 'Name',
  biography: 'Biography Event',
}

const GROUP_ORDER: { type: string; label: string }[] = [
  { type: 'term', label: 'Dictionary' },
  { type: 'biography', label: 'Biography' },
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

function highlightMatch(text: string, query: string, maxLen: number): string {
  if (!text || !query) return text?.slice(0, maxLen) || ''
  const lower = text.toLowerCase()
  const idx = lower.indexOf(query.toLowerCase())
  if (idx === -1) return text.slice(0, maxLen) + (text.length > maxLen ? '...' : '')
  const start = Math.max(0, idx - 60)
  const end = Math.min(text.length, idx + query.length + 100)
  let snippet = (start > 0 ? '...' : '') + text.slice(start, end) + (end < text.length ? '...' : '')
  if (snippet.length > maxLen + 6) snippet = snippet.slice(0, maxLen) + '...'
  return snippet
}

export default function Search() {
  const [searchParams] = useSearchParams()
  const initialQuery = searchParams.get('q') || ''
  const { data: entries } = useData<SearchEntry[]>('search_index.json')
  const [query, setQuery] = useState(initialQuery)
  const [expandedGroups, setExpandedGroups] = useState<Set<string>>(new Set())

  const fuse = useMemo(() => {
    if (!entries) return null
    return new Fuse(entries, {
      keys: [
        { name: 'title', weight: 3 },
        { name: 'text', weight: 1 },
        { name: 'author', weight: 1 },
        { name: 'category', weight: 2 },
      ],
      threshold: 0.3,
      includeMatches: true,
      minMatchCharLength: 2,
    })
  }, [entries])

  const grouped = useMemo(() => {
    if (!fuse || !query || query.length < 2) return []
    const hits = fuse.search(query, { limit: 200 })
    return GROUP_ORDER.map(g => ({
      ...g,
      items: hits.filter(h => h.item.type === g.type),
    })).filter(g => g.items.length > 0)
  }, [fuse, query])

  const totalCount = grouped.reduce((sum, g) => sum + g.items.length, 0)

  const toggleGroup = (type: string) => {
    setExpandedGroups(prev => {
      const next = new Set(prev)
      if (next.has(type)) next.delete(type)
      else next.add(type)
      return next
    })
  }

  const INITIAL_SHOW = 5

  return (
    <>
      <div className="page-header">
        <h1>Search</h1>
        <p>Search across the entire Knowledge Portal</p>
      </div>

      <input
        className="search-input"
        type="text"
        placeholder="Search the Exegesis corpus..."
        value={query}
        onChange={e => setQuery(e.target.value)}
        autoFocus
      />

      {query.length >= 2 && totalCount > 0 && (
        <p style={{ color: 'var(--text-muted)', marginBottom: '1rem', fontSize: '0.85rem' }}>
          {totalCount} result{totalCount !== 1 ? 's' : ''} for "{query}"
        </p>
      )}

      {grouped.map(g => {
        const expanded = expandedGroups.has(g.type)
        const shown = expanded ? g.items : g.items.slice(0, INITIAL_SHOW)

        return (
          <div key={g.type} className="search-group">
            <h2 className="search-group-title">
              {g.label}
              <span className="search-group-count">{g.items.length}</span>
            </h2>
            {shown.map(hit => (
              <div key={`${hit.item.type}-${hit.item.id}`} className="card" style={{ marginBottom: '0.5rem' }}>
                <h3>
                  <Link to={getLink(hit.item)}>
                    {hit.item.type === 'segment' ? formatSegmentTitle(hit.item.title) : hit.item.title}
                  </Link>
                </h3>
                <div className="card-meta">
                  <span className="badge badge-category">{TYPE_LABELS[hit.item.type]}</span>
                  {hit.item.date && <span>{hit.item.date}</span>}
                  {hit.item.author && <span>{hit.item.author}</span>}
                  {hit.item.category && <span>{hit.item.category}</span>}
                </div>
                {hit.item.text && (
                  <p style={{ marginTop: '0.35rem', fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
                    {highlightMatch(hit.item.text, query, 200)}
                  </p>
                )}
              </div>
            ))}
            {g.items.length > INITIAL_SHOW && (
              <button
                className="search-show-all"
                onClick={() => toggleGroup(g.type)}
              >
                {expanded ? 'Show fewer' : `Show all ${g.items.length} results`}
              </button>
            )}
          </div>
        )
      })}

      {query.length >= 2 && totalCount === 0 && (
        <p className="loading">No results found for "{query}"</p>
      )}
    </>
  )
}

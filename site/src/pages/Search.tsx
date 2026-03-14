import { useState, useMemo, useCallback } from 'react'
import { Link } from 'react-router-dom'
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

export default function Search() {
  const { data: entries } = useData<SearchEntry[]>('search_index.json')
  const [query, setQuery] = useState('')
  const [scope, setScope] = useState<'all' | 'segment' | 'term' | 'archive' | 'name' | 'biography'>('all')

  const fuse = useMemo(() => {
    if (!entries) return null
    return new Fuse(entries, {
      keys: ['title', 'text', 'author', 'category'],
      threshold: 0.3,
      includeMatches: true,
      minMatchCharLength: 2,
    })
  }, [entries])

  const results = useMemo(() => {
    if (!fuse || !query || query.length < 2) return []
    let hits = fuse.search(query, { limit: 100 })
    if (scope !== 'all') {
      hits = hits.filter(h => h.item.type === scope)
    }
    return hits
  }, [fuse, query, scope])

  const getLink = useCallback((entry: SearchEntry) => {
    switch (entry.type) {
      case 'segment': return `/segments/${entry.id}`
      case 'term': return `/dictionary/${entry.slug}`
      case 'archive': return `/archive/${entry.slug}`
      case 'name': return `/names/${entry.slug}`
      case 'biography': return `/biography`
      default: return '/'
    }
  }, [])

  const counts = useMemo(() => {
    if (!fuse || !query || query.length < 2) return { segment: 0, term: 0, archive: 0, name: 0, biography: 0 }
    const all = fuse.search(query, { limit: 500 })
    return {
      segment: all.filter(h => h.item.type === 'segment').length,
      term: all.filter(h => h.item.type === 'term').length,
      archive: all.filter(h => h.item.type === 'archive').length,
      name: all.filter(h => h.item.type === 'name').length,
      biography: all.filter(h => h.item.type === 'biography').length,
    }
  }, [fuse, query])

  return (
    <>
      <div className="page-header">
        <h1>Search</h1>
        <p>Search across segments, dictionary terms, archive documents, names, and biography</p>
      </div>

      <input
        className="search-input"
        type="text"
        placeholder="Search the Exegesis corpus..."
        value={query}
        onChange={e => setQuery(e.target.value)}
        autoFocus
      />

      {query.length >= 2 && (
        <div style={{display:'flex', gap:'0.5rem', marginBottom:'1rem'}}>
          <button
            onClick={() => setScope('all')}
            className={`badge ${scope === 'all' ? 'badge-provisional' : 'badge-category'}`}
            style={{cursor:'pointer', border:'none'}}
          >
            All ({counts.segment + counts.term + counts.archive + counts.name + counts.biography})
          </button>
          <button
            onClick={() => setScope('segment')}
            className={`badge ${scope === 'segment' ? 'badge-provisional' : 'badge-category'}`}
            style={{cursor:'pointer', border:'none'}}
          >
            Segments ({counts.segment})
          </button>
          <button
            onClick={() => setScope('term')}
            className={`badge ${scope === 'term' ? 'badge-provisional' : 'badge-category'}`}
            style={{cursor:'pointer', border:'none'}}
          >
            Terms ({counts.term})
          </button>
          <button
            onClick={() => setScope('archive')}
            className={`badge ${scope === 'archive' ? 'badge-provisional' : 'badge-category'}`}
            style={{cursor:'pointer', border:'none'}}
          >
            Archive ({counts.archive})
          </button>
          <button
            onClick={() => setScope('name')}
            className={`badge ${scope === 'name' ? 'badge-provisional' : 'badge-category'}`}
            style={{cursor:'pointer', border:'none'}}
          >
            Names ({counts.name})
          </button>
          <button
            onClick={() => setScope('biography')}
            className={`badge ${scope === 'biography' ? 'badge-provisional' : 'badge-category'}`}
            style={{cursor:'pointer', border:'none'}}
          >
            Biography ({counts.biography})
          </button>
        </div>
      )}

      {results.map(hit => (
        <div key={`${hit.item.type}-${hit.item.id}`} className="card" style={{marginBottom:'0.75rem'}}>
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
            <p style={{marginTop:'0.5rem', fontSize:'0.9rem', color:'var(--text-secondary)'}}>
              {hit.item.text.slice(0, 200)}
              {hit.item.text.length > 200 ? '...' : ''}
            </p>
          )}
        </div>
      ))}

      {query.length >= 2 && results.length === 0 && (
        <p className="loading">No results found for "{query}"</p>
      )}
    </>
  )
}

import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface NameSummary {
  name_id: string
  canonical_form: string
  slug: string
  entity_type: string
  source_type: string
  status: string
  review_state: string
  mention_count: number
  card_description: string
  etymology: string | null
  allusion_type: string[] | null
  first_work: string | null
}

const TYPE_LABELS: Record<string, string> = {
  character: 'Character',
  place: 'Place',
  organization: 'Organization',
  deity_figure: 'Deity / Figure',
  historical_person: 'Historical Person',
  other: 'Other',
}

export default function Names() {
  const { data: names, loading } = useData<NameSummary[]>('names/index.json')
  const [search, setSearch] = useState('')
  const [entityType, setEntityType] = useState<string>('all')

  const types = useMemo(() => {
    if (!names) return []
    const ts = new Set(names.map(n => n.entity_type).filter(Boolean))
    return ['all', ...Array.from(ts).sort()]
  }, [names])

  const filtered = useMemo(() => {
    if (!names) return []
    let result = names
    if (entityType !== 'all') {
      result = result.filter(n => n.entity_type === entityType)
    }
    if (search) {
      const q = search.toLowerCase()
      result = result.filter(n =>
        n.canonical_form.toLowerCase().includes(q) ||
        (n.card_description || '').toLowerCase().includes(q) ||
        (n.etymology || '').toLowerCase().includes(q)
      )
    }
    return result
  }, [names, search, entityType])

  if (loading) return <div className="loading">Loading...</div>

  return (
    <>
      <div className="page-header">
        <h1>Names</h1>
        <p>{names?.length} names ({filtered.length} shown)</p>
      </div>

      <div className="sidebar-layout">
        <div className="sidebar">
          <h3>Entity Type</h3>
          <ul>
            {types.map(t => (
              <li key={t}>
                <a
                  href="#"
                  className={entityType === t ? 'active' : ''}
                  onClick={e => { e.preventDefault(); setEntityType(t) }}
                >
                  {t === 'all' ? 'All Types' : TYPE_LABELS[t] || t}
                  {t !== 'all' && (
                    <span style={{opacity:0.5, marginLeft:'0.25rem'}}>
                      ({names?.filter(n => n.entity_type === t).length})
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
            placeholder="Search names..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />

          <div className="card-grid">
            {filtered.map(name => (
              <div key={name.name_id} className="card">
                <h3>
                  <Link to={`/names/${name.slug}`}>{name.canonical_form}</Link>
                </h3>
                <div className="card-meta">
                  <span>{name.mention_count} mention{name.mention_count !== 1 ? 's' : ''}</span>
                  <span className="badge badge-category">
                    {TYPE_LABELS[name.entity_type] || name.entity_type}
                  </span>
                  {name.source_type && (
                    <span className="confidence-label">{name.source_type}</span>
                  )}
                </div>
                {name.etymology && (
                  <p style={{marginTop:'0.25rem', fontStyle:'italic', fontSize:'0.85rem', color:'var(--text-secondary)'}}>
                    Etymology: {name.etymology}
                  </p>
                )}
                {name.card_description && (
                  <p style={{marginTop:'0.5rem'}}>
                    {name.card_description.slice(0, 200)}
                    {name.card_description.length > 200 ? '...' : ''}
                  </p>
                )}
                {name.first_work && (
                  <div className="card-meta">
                    <span>First work: {name.first_work}</span>
                  </div>
                )}
                {name.allusion_type && name.allusion_type.length > 0 && (
                  <div className="card-meta">
                    {name.allusion_type.map((a, i) => (
                      <span key={i} className="badge badge-accepted">{a}</span>
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

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
  wordplay_note: string | null
  allusion_type: string[] | null
  first_work: string | null
  work_list: string[] | null
}

const TYPE_LABELS: Record<string, string> = {
  character: 'Character',
  place: 'Place',
  organization: 'Organization',
  deity_figure: 'Deity / Figure',
  historical_person: 'Historical Person',
  other: 'Other',
}

const SOURCE_LABELS: Record<string, string> = {
  fiction: 'Fiction',
  exegesis: 'Exegesis',
  both: 'Both',
  reference: 'Reference',
}

export default function Names() {
  const { data: names, loading } = useData<NameSummary[]>('names/index.json')
  const [search, setSearch] = useState('')
  const [entityType, setEntityType] = useState<string>('all')
  const [sourceFilter, setSourceFilter] = useState<string>('all')

  const types = useMemo(() => {
    if (!names) return []
    const ts = new Set(names.map(n => n.entity_type).filter(Boolean))
    return ['all', ...Array.from(ts).sort()]
  }, [names])

  const sourceTypes = useMemo(() => {
    if (!names) return []
    const st = new Set(names.map(n => n.source_type).filter(Boolean))
    return ['all', ...Array.from(st).sort()]
  }, [names])

  const filtered = useMemo(() => {
    if (!names) return []
    let result = names
    if (entityType !== 'all') {
      result = result.filter(n => n.entity_type === entityType)
    }
    if (sourceFilter !== 'all') {
      result = result.filter(n => n.source_type === sourceFilter)
    }
    if (search) {
      const q = search.toLowerCase()
      result = result.filter(n =>
        n.canonical_form.toLowerCase().includes(q) ||
        (n.card_description || '').toLowerCase().includes(q) ||
        (n.etymology || '').toLowerCase().includes(q) ||
        (n.first_work || '').toLowerCase().includes(q)
      )
    }
    return result
  }, [names, search, entityType, sourceFilter])

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

          <h3>Source</h3>
          <ul>
            {sourceTypes.map(s => (
              <li key={s}>
                <a
                  href="#"
                  className={sourceFilter === s ? 'active' : ''}
                  onClick={e => { e.preventDefault(); setSourceFilter(s) }}
                >
                  {s === 'all' ? 'All Sources' : SOURCE_LABELS[s] || s}
                  {s !== 'all' && (
                    <span style={{opacity:0.5, marginLeft:'0.25rem'}}>
                      ({names?.filter(n => n.source_type === s).length})
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
                  <span className="badge badge-category">
                    {TYPE_LABELS[name.entity_type] || name.entity_type}
                  </span>
                  {name.source_type && (
                    <span className={`badge ${name.source_type === 'fiction' ? 'badge-provisional' : name.source_type === 'both' ? 'badge-accepted' : 'badge-background'}`}>
                      {SOURCE_LABELS[name.source_type] || name.source_type}
                    </span>
                  )}
                  {name.mention_count > 0 && (
                    <span>{name.mention_count} mention{name.mention_count !== 1 ? 's' : ''}</span>
                  )}
                </div>
                {name.first_work && name.entity_type === 'character' && (
                  <p style={{marginTop:'0.25rem', fontSize:'0.85rem', color:'var(--text-secondary)'}}>
                    <em>{name.work_list && name.work_list.length > 1 ? name.work_list.join(', ') : name.first_work}</em>
                  </p>
                )}
                {name.etymology && (
                  <p style={{marginTop:'0.25rem', fontStyle:'italic', fontSize:'0.85rem', color:'var(--text-secondary)'}}>
                    {name.etymology}
                  </p>
                )}
                {name.card_description && (
                  <p style={{marginTop:'0.5rem'}}>
                    {name.card_description.slice(0, 200)}
                    {name.card_description.length > 200 ? '...' : ''}
                  </p>
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

          {filtered.length === 0 && (
            <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
              No names match the current filters.
            </p>
          )}
        </div>
      </div>
    </>
  )
}

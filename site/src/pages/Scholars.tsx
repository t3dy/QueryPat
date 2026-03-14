import { useState, useMemo } from 'react'
import { useData } from '../hooks/useData'

interface ScholarPDF {
  title: string
  filename: string
  category: string
  date?: string
  pages?: number
}

interface Scholar {
  scholar_id: string
  name: string
  role: string
  tier: number
  affiliation?: string
  key_works: string[]
  interpretive_stance: string
  relevance: string
  archive_pdfs: ScholarPDF[]
  pdf_count: number
}

const TIER_NAMES: Record<number, string> = {
  1: 'Major Biographers',
  2: 'Scholars & Critics',
  3: 'Editors & Curators',
  4: 'Associates & Contributors',
  5: 'Media Sources',
}

const TIER_COLORS: Record<number, string> = {
  1: '#C09A4D',
  2: '#8B7355',
  3: '#6B8E6B',
  4: '#7B8FA1',
  5: '#8A8A8A',
}

export default function Scholars() {
  const { data: scholars, loading } = useData<Scholar[]>('scholars.json')
  const [search, setSearch] = useState('')
  const [activeTier, setActiveTier] = useState<number | null>(null)
  const [expandedId, setExpandedId] = useState<string | null>(null)

  const tierCounts = useMemo(() => {
    if (!scholars) return {} as Record<number, number>
    const counts: Record<number, number> = {}
    for (const s of scholars) {
      counts[s.tier] = (counts[s.tier] || 0) + 1
    }
    return counts
  }, [scholars])

  const filtered = useMemo(() => {
    if (!scholars) return []
    let result = scholars
    if (activeTier !== null) {
      result = result.filter(s => s.tier === activeTier)
    }
    if (search) {
      const q = search.toLowerCase()
      result = result.filter(s =>
        s.name.toLowerCase().includes(q) ||
        s.role.toLowerCase().includes(q) ||
        s.interpretive_stance.toLowerCase().includes(q) ||
        (s.key_works || []).some(w => w.toLowerCase().includes(q)) ||
        (s.affiliation || '').toLowerCase().includes(q)
      )
    }
    return result
  }, [scholars, search, activeTier])

  if (loading) return <div className="loading">Loading...</div>

  return (
    <>
      <div className="page-header">
        <h1>Scholars</h1>
        <p>{scholars?.length} scholars &amp; sources ({filtered.length} shown)</p>
      </div>

      <div className="sidebar-layout">
        <div className="sidebar">
          <h3>Tiers</h3>
          <ul>
            <li>
              <a
                href="#"
                className={activeTier === null ? 'active' : ''}
                onClick={e => { e.preventDefault(); setActiveTier(null) }}
              >
                All ({scholars?.length})
              </a>
            </li>
            {([1, 2, 3, 4, 5] as number[]).map(tier =>
              tierCounts[tier] ? (
                <li key={tier}>
                  <a
                    href="#"
                    className={activeTier === tier ? 'active' : ''}
                    onClick={e => { e.preventDefault(); setActiveTier(tier) }}
                    style={{ borderLeft: `3px solid ${TIER_COLORS[tier]}`, paddingLeft: '0.5rem' }}
                  >
                    {TIER_NAMES[tier]}
                    <span style={{ opacity: 0.5, marginLeft: '0.25rem' }}>
                      ({tierCounts[tier]})
                    </span>
                  </a>
                </li>
              ) : null
            )}
          </ul>
        </div>

        <div>
          <input
            className="search-input"
            type="text"
            placeholder="Search scholars..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />

          <div className="card-grid">
            {filtered.map(s => {
              const isExpanded = expandedId === s.scholar_id
              return (
                <div
                  key={s.scholar_id}
                  className="card"
                  style={{ cursor: 'pointer', borderLeft: `3px solid ${TIER_COLORS[s.tier]}` }}
                  onClick={() => setExpandedId(isExpanded ? null : s.scholar_id)}
                >
                  <h3>{s.name}</h3>
                  <div className="card-meta">
                    <span className="badge" style={{ background: TIER_COLORS[s.tier] + '33', color: TIER_COLORS[s.tier] }}>
                      {s.role}
                    </span>
                    <span className="badge badge-category">{TIER_NAMES[s.tier]}</span>
                    <span>{s.pdf_count} PDF{s.pdf_count !== 1 ? 's' : ''}</span>
                  </div>
                  {s.affiliation && (
                    <p style={{ marginTop: '0.25rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                      {s.affiliation}
                    </p>
                  )}

                  {!isExpanded && s.interpretive_stance && (
                    <p style={{ marginTop: '0.5rem' }}>
                      {s.interpretive_stance.slice(0, 200)}
                      {s.interpretive_stance.length > 200 ? '...' : ''}
                    </p>
                  )}

                  {isExpanded && (
                    <div style={{ marginTop: '1rem' }}>
                      {s.interpretive_stance && (
                        <div style={{ marginBottom: '1rem' }}>
                          <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                            Interpretive Stance
                          </h4>
                          <p>{s.interpretive_stance}</p>
                        </div>
                      )}

                      {s.key_works && s.key_works.length > 0 && (
                        <div style={{ marginBottom: '1rem' }}>
                          <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                            Key Works
                          </h4>
                          <ul style={{ margin: 0, paddingLeft: '1.25rem' }}>
                            {s.key_works.map((w, i) => <li key={i}>{w}</li>)}
                          </ul>
                        </div>
                      )}

                      {s.relevance && (
                        <div style={{ marginBottom: '1rem' }}>
                          <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                            Relevance
                          </h4>
                          <p>{s.relevance}</p>
                        </div>
                      )}

                      {s.archive_pdfs && s.archive_pdfs.length > 0 && (
                        <div>
                          <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.5rem' }}>
                            Archive Documents ({s.pdf_count})
                          </h4>
                          <div style={{ display: 'grid', gap: '0.5rem' }}>
                            {s.archive_pdfs.map((pdf, i) => (
                              <div
                                key={i}
                                style={{
                                  padding: '0.5rem 0.75rem',
                                  background: 'var(--bg-card, rgba(255,255,255,0.03))',
                                  borderRadius: '4px',
                                  fontSize: '0.9rem',
                                }}
                              >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: '0.5rem' }}>
                                  <span>{pdf.title || pdf.filename}</span>
                                  <span style={{ opacity: 0.5, whiteSpace: 'nowrap', fontSize: '0.8rem' }}>
                                    {pdf.date}
                                  </span>
                                </div>
                                <div className="card-meta" style={{ marginTop: '0.25rem' }}>
                                  <span className="badge badge-category">{pdf.category}</span>
                                  {pdf.pages != null && pdf.pages > 0 && (
                                    <span>{pdf.pages} pages</span>
                                  )}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </>
  )
}

import { useState, useMemo, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface ScholarPDF {
  title: string
  filename: string
  category: string
  date?: string
  pages?: number
}

interface ScholarDispute {
  opponent: string
  issue: string
}

interface ScholarQuote {
  quote: string
  source?: string
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
  key_arguments?: string[]
  scholarly_lineage?: string
  disputes?: ScholarDispute[]
  quotable_lines?: ScholarQuote[]
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
  const location = useLocation()
  const [search, setSearch] = useState('')
  const [activeTier, setActiveTier] = useState<number | null>(null)
  const [expandedId, setExpandedId] = useState<string | null>(null)
  const [sortBy, setSortBy] = useState<string>('tier')

  // Read URL hash on mount or when scholars load: open + scroll to the matching scholar.
  useEffect(() => {
    if (!scholars) return
    // HashRouter encodes routes as #/foo, so a target inside the route is in location.hash after a second '#'.
    // Simpler: use window.location.hash directly and parse out anything after the second '#'.
    const raw = window.location.hash || ''
    const parts = raw.split('#').filter(Boolean)  // ['/scholars', 'pamela-jackson'] or ['/scholars']
    const targetSlug = parts.length >= 2 ? parts[parts.length - 1] : null
    if (!targetSlug) return
    const target = scholars.find(s =>
      s.scholar_id === targetSlug ||
      s.scholar_id === targetSlug.toLowerCase() ||
      s.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') === targetSlug.toLowerCase()
    )
    if (!target) return
    setExpandedId(target.scholar_id)
    // Scroll after the next paint
    requestAnimationFrame(() => {
      const el = document.getElementById(`scholar-${target.scholar_id}`)
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    })
  }, [scholars, location.hash])

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
    return [...result].sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name)
      if (sortBy === 'pdfs') return (b.pdf_count || 0) - (a.pdf_count || 0) || a.name.localeCompare(b.name)
      if (sortBy === 'works') return (b.key_works?.length || 0) - (a.key_works?.length || 0) || a.name.localeCompare(b.name)
      return (a.tier || 99) - (b.tier || 99) || a.name.localeCompare(b.name)
    })
  }, [scholars, search, activeTier, sortBy])

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
          <div className="toolbar-row">
            <input
              className="search-input"
              type="text"
              placeholder="Search scholars..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <select className="filter-select" value={sortBy} onChange={e => setSortBy(e.target.value)} aria-label="Sort scholars">
              <option value="tier">Tier</option>
              <option value="name">Name</option>
              <option value="pdfs">Archive PDFs</option>
              <option value="works">Key Works</option>
            </select>
          </div>

          {filtered.length === 0 && (
            <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
              No scholars match the current filters.
            </p>
          )}

          <div className="card-grid">
            {filtered.map(s => {
              const isExpanded = expandedId === s.scholar_id
              return (
                <div
                  key={s.scholar_id}
                  id={`scholar-${s.scholar_id}`}
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

                      {s.key_arguments && s.key_arguments.length > 0 && (
                        <div style={{ marginBottom: '1rem' }}>
                          <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                            Key Arguments
                          </h4>
                          <ul style={{ margin: 0, paddingLeft: '1.25rem' }}>
                            {s.key_arguments.map((a, i) => <li key={i}>{a}</li>)}
                          </ul>
                        </div>
                      )}

                      {s.scholarly_lineage && (
                        <div style={{ marginBottom: '1rem' }}>
                          <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                            Scholarly Lineage
                          </h4>
                          <p>{s.scholarly_lineage}</p>
                        </div>
                      )}

                      {s.disputes && s.disputes.length > 0 && (
                        <div style={{ marginBottom: '1rem' }}>
                          <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                            Disputes
                          </h4>
                          <ul style={{ margin: 0, paddingLeft: '1.25rem' }}>
                            {s.disputes.map((d, i) => (
                              <li key={i}>
                                <strong>{d.opponent}:</strong> {d.issue}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {s.quotable_lines && s.quotable_lines.length > 0 && (
                        <div style={{ marginBottom: '1rem' }}>
                          <h4 style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                            Quotable Lines
                          </h4>
                          <ul style={{ margin: 0, paddingLeft: '1.25rem', listStyle: 'none' }}>
                            {s.quotable_lines.map((q, i) => (
                              <li key={i} style={{ marginBottom: '0.5rem' }}>
                                <em>"{q.quote}"</em>
                                {q.source && <span style={{ opacity: 0.6, fontSize: '0.85rem' }}> — {q.source}</span>}
                              </li>
                            ))}
                          </ul>
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

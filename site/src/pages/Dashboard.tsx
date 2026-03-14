import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface Analytics {
  totals: {
    documents: number
    segments: number
    terms_public: number
    terms_total: number
    evidence_packets: number
    archive_docs: number
    timeline_events: number
  }
  top_terms: { name: string; count: number; category: string }[]
  segments_per_year: { year: string; count: number; bio_events?: number; has_content?: boolean }[]
}

export default function Dashboard() {
  const { data, loading } = useData<Analytics>('analytics.json')

  if (loading || !data) return <div className="loading">Loading...</div>

  const t = data.totals

  return (
    <>
      <div className="hero-header">
        <h1>The Exegesis Knowledge Portal</h1>
        <p className="hero-subtitle">
          A scholarly reference for Philip K. Dick's <em>Exegesis</em> &mdash; theology, philosophy, and vision
        </p>
      </div>

      <div className="stats-grid">
        <Link to="/timeline" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{t.segments.toLocaleString()}</div>
          <div className="stat-label">Exegesis Summaries</div>
        </Link>
        <Link to="/dictionary" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{t.terms_public.toLocaleString()}</div>
          <div className="stat-label">Dictionary Terms</div>
        </Link>
        <Link to="/archive" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{t.archive_docs.toLocaleString()}</div>
          <div className="stat-label">Archive Documents</div>
        </Link>
        <Link to="/biography" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">119</div>
          <div className="stat-label">Biography Events</div>
        </Link>
      </div>

      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'2rem', marginTop:'1rem'}}>
        <div className="detail-section">
          <h2>Key Concepts</h2>
          <ul>
            {data.top_terms.slice(0, 12).map(t => (
              <li key={t.name}>
                <Link to={`/dictionary/${t.name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`}>
                  {t.name}
                </Link>
                <span style={{color:'var(--text-muted)', marginLeft:'0.5rem'}}>
                  ({t.count.toLocaleString()})
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="detail-section">
          <h2>Browse by Year</h2>
          <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:'0.25rem 0 0.75rem'}}>
            Philip K. Dick (1928&ndash;1982)
          </p>
          {(() => {
            const decades = new Map<string, typeof data.segments_per_year>()
            for (const y of data.segments_per_year) {
              const dec = y.year.slice(0, 3) + '0s'
              if (!decades.has(dec)) decades.set(dec, [])
              decades.get(dec)!.push(y)
            }
            return Array.from(decades.entries()).map(([dec, years]) => (
              <div key={dec} style={{marginBottom:'0.75rem'}}>
                <div style={{fontWeight:600, fontSize:'0.85rem', color:'var(--text-muted)', marginBottom:'0.25rem'}}>{dec}</div>
                <div style={{display:'flex', flexWrap:'wrap', gap:'0.25rem'}}>
                  {years.map(y => {
                    const total = y.count + (y.bio_events || 0)
                    const hasContent = y.has_content || total > 0
                    return (
                      <Link
                        key={y.year}
                        to={hasContent ? `/timeline/${y.year}` : '#'}
                        style={{
                          display:'inline-block',
                          padding:'0.2rem 0.45rem',
                          fontSize:'0.8rem',
                          borderRadius:'4px',
                          textDecoration:'none',
                          background: y.count > 100 ? 'var(--accent)' : y.count > 0 ? 'var(--accent-muted, rgba(var(--accent-rgb, 100,100,200), 0.2))' : hasContent ? 'var(--bg-elevated, #f0f0f0)' : 'transparent',
                          color: y.count > 100 ? '#fff' : hasContent ? 'var(--text)' : 'var(--text-muted)',
                          opacity: hasContent ? 1 : 0.4,
                          cursor: hasContent ? 'pointer' : 'default',
                        }}
                        title={`${y.year}: ${y.count} Exegesis entries${y.bio_events ? `, ${y.bio_events} biography events` : ''}`}
                      >
                        {y.year.slice(2)}
                      </Link>
                    )
                  })}
                </div>
              </div>
            ))
          })()}
        </div>
      </div>
    </>
  )
}

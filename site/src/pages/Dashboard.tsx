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
  segments_per_year: { year: string; count: number }[]
}

export default function Dashboard() {
  const { data, loading } = useData<Analytics>('analytics.json')

  if (loading || !data) return <div className="loading">Loading...</div>

  const t = data.totals

  return (
    <>
      <div className="page-header">
        <h1>The Exegesis Knowledge Portal</h1>
        <p>A unified scholarly browser for Philip K. Dick's <em>Exegesis</em></p>
      </div>

      <div className="stats-grid">
        <Link to="/timeline" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{t.segments.toLocaleString()}</div>
          <div className="stat-label">Segments</div>
        </Link>
        <Link to="/dictionary" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{t.terms_public.toLocaleString()}</div>
          <div className="stat-label">Dictionary Terms</div>
        </Link>
        <Link to="/archive" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{t.archive_docs.toLocaleString()}</div>
          <div className="stat-label">Archive Documents</div>
        </Link>
        <div className="stat-card">
          <div className="stat-value">{t.evidence_packets.toLocaleString()}</div>
          <div className="stat-label">Evidence Packets</div>
        </div>
      </div>

      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'2rem'}}>
        <div className="detail-section">
          <h2>Top Terms</h2>
          <ul>
            {data.top_terms.slice(0, 15).map(t => (
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
          <h2>Segments by Year</h2>
          <ul>
            {data.segments_per_year.map(y => (
              <li key={y.year}>
                <Link to={`/timeline/${y.year}`}>{y.year}</Link>
                <span style={{color:'var(--text-muted)', marginLeft:'0.5rem'}}>
                  ({y.count} segments)
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </>
  )
}

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
          <ul>
            {data.segments_per_year.map(y => (
              <li key={y.year}>
                <Link to={`/timeline/${y.year}`}>{y.year}</Link>
                <span style={{color:'var(--text-muted)', marginLeft:'0.5rem'}}>
                  ({y.count} entries)
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </>
  )
}

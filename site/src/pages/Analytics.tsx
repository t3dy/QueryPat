import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface Analytics {
  totals: Record<string, number>
  top_terms: { name: string; count: number; category: string }[]
  segments_per_year: { year: string; count: number }[]
  term_categories: { category: string; count: number }[]
  archive_categories: { category: string; count: number }[]
}

export default function Analytics() {
  const { data, loading } = useData<Analytics>('analytics.json')

  if (loading || !data) return <div className="loading">Loading...</div>

  const maxTermCount = Math.max(...data.top_terms.map(t => t.count))
  const maxYearCount = Math.max(...data.segments_per_year.map(y => y.count))

  return (
    <>
      <div className="page-header">
        <h1>Analytics</h1>
        <p>Corpus statistics and term distribution</p>
      </div>

      <div className="stats-grid">
        {Object.entries(data.totals).map(([key, val]) => (
          <div key={key} className="stat-card">
            <div className="stat-value">{val.toLocaleString()}</div>
            <div className="stat-label">{key.replace(/_/g, ' ')}</div>
          </div>
        ))}
      </div>

      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'2rem'}}>
        <div className="detail-section">
          <h2>Top 30 Terms by Frequency</h2>
          {data.top_terms.map(t => (
            <div key={t.name} style={{marginBottom:'0.4rem'}}>
              <div style={{display:'flex', justifyContent:'space-between', fontSize:'0.85rem'}}>
                <Link to={`/dictionary/${t.name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`}>
                  {t.name}
                </Link>
                <span style={{color:'var(--text-muted)'}}>{t.count.toLocaleString()}</span>
              </div>
              <div style={{
                height:'4px',
                background:'var(--border-light)',
                borderRadius:'2px',
                overflow:'hidden',
              }}>
                <div style={{
                  width:`${(t.count / maxTermCount) * 100}%`,
                  height:'100%',
                  background:'var(--accent)',
                  borderRadius:'2px',
                }} />
              </div>
            </div>
          ))}
        </div>

        <div>
          <div className="detail-section">
            <h2>Segments per Year</h2>
            {data.segments_per_year.map(y => (
              <div key={y.year} style={{marginBottom:'0.4rem'}}>
                <div style={{display:'flex', justifyContent:'space-between', fontSize:'0.85rem'}}>
                  <Link to={`/timeline/${y.year}`}>{y.year}</Link>
                  <span style={{color:'var(--text-muted)'}}>{y.count}</span>
                </div>
                <div style={{
                  height:'4px',
                  background:'var(--border-light)',
                  borderRadius:'2px',
                  overflow:'hidden',
                }}>
                  <div style={{
                    width:`${(y.count / maxYearCount) * 100}%`,
                    height:'100%',
                    background:'var(--accent)',
                    borderRadius:'2px',
                  }} />
                </div>
              </div>
            ))}
          </div>

          <div className="detail-section">
            <h2>Term Categories</h2>
            {data.term_categories.map(c => (
              <div key={c.category} style={{display:'flex', justifyContent:'space-between', fontSize:'0.85rem', marginBottom:'0.3rem'}}>
                <span>{c.category}</span>
                <span style={{color:'var(--text-muted)'}}>{c.count}</span>
              </div>
            ))}
          </div>

          <div className="detail-section">
            <h2>Archive Categories</h2>
            {data.archive_categories.map(c => (
              <div key={c.category} style={{display:'flex', justifyContent:'space-between', fontSize:'0.85rem', marginBottom:'0.3rem'}}>
                <span>{c.category}</span>
                <span style={{color:'var(--text-muted)'}}>{c.count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}

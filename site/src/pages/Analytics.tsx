import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

const LANE_COLORS: Record<string, string> = {
  A: '#8b5cf6', B: '#d97706', C: '#2563eb', D: '#059669', E: '#dc2626'
}

interface Analytics {
  totals: Record<string, number>
  top_terms: { name: string; count: number; category: string }[]
  segments_per_year: { year: string; count: number }[]
  term_categories: { category: string; count: number }[]
  archive_categories: { category: string; count: number }[]
  evidentiary_lanes?: { lane: string; label: string; count: number }[]
  quality?: {
    terms_accepted?: number
    terms_with_evidence?: number
    archive_with_text?: number
    archive_with_lanes?: number
    segments_with_works?: number
    biography_with_location?: number
  }
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

      {data.evidentiary_lanes && data.evidentiary_lanes.length > 0 && (
        <div className="detail-section">
          <h2>Evidentiary Lanes</h2>
          <p style={{fontSize:'0.85rem', color:'var(--text-muted)', marginBottom:'1rem'}}>
            Document classification by source type
          </p>
          {(() => {
            const maxLane = Math.max(...data.evidentiary_lanes!.map(l => l.count))
            return data.evidentiary_lanes!.map(l => (
              <div key={l.lane} style={{marginBottom:'0.5rem'}}>
                <div style={{display:'flex', justifyContent:'space-between', fontSize:'0.85rem'}}>
                  <span>Lane {l.lane}: {l.label}</span>
                  <span style={{color:'var(--text-muted)'}}>{l.count}</span>
                </div>
                <div style={{height:'6px', background:'var(--border-light)', borderRadius:'3px', overflow:'hidden'}}>
                  <div style={{
                    width:`${(l.count / maxLane) * 100}%`,
                    height:'100%',
                    background: LANE_COLORS[l.lane] || 'var(--accent)',
                    borderRadius:'3px',
                  }} />
                </div>
              </div>
            ))
          })()}
        </div>
      )}

      {data.quality && (
        <div className="detail-section">
          <h2>Data Quality</h2>
          <div className="stats-grid">
            {data.quality.terms_accepted != null && (
              <div className="stat-card">
                <div className="stat-value">{data.quality.terms_accepted}</div>
                <div className="stat-label">Accepted Terms</div>
              </div>
            )}
            {data.quality.terms_with_evidence != null && (
              <div className="stat-card">
                <div className="stat-value">{data.quality.terms_with_evidence}</div>
                <div className="stat-label">Terms with Evidence</div>
              </div>
            )}
            {data.quality.archive_with_lanes != null && (
              <div className="stat-card">
                <div className="stat-value">{data.quality.archive_with_lanes}</div>
                <div className="stat-label">Archive Docs Lane-Tagged</div>
              </div>
            )}
            {data.quality.biography_with_location != null && (
              <div className="stat-card">
                <div className="stat-value">{data.quality.biography_with_location}</div>
                <div className="stat-label">Bio Events with Location</div>
              </div>
            )}
            {data.quality.segments_with_works != null && (
              <div className="stat-card">
                <div className="stat-value">{data.quality.segments_with_works}</div>
                <div className="stat-label">Segments with Works</div>
              </div>
            )}
            {data.quality.archive_with_text != null && (
              <div className="stat-card">
                <div className="stat-value">{data.quality.archive_with_text}</div>
                <div className="stat-label">Archive Docs with Text</div>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  )
}

import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface WorkIndexEntry {
  slug: string
  title: string
  mention_count: number
  date_range: string
  work_link: string | null
  theological_headline: string
  has_writeup: boolean
}

interface WorksIndex {
  generated_from: string
  total_analyzed_entries: number
  works: WorkIndexEntry[]
}

export default function ExegesisWorks() {
  const { data, loading, error } = useData<WorksIndex>('exegesis/works/index.json')

  if (loading) return <div className="loading">Loading&hellip;</div>
  if (error || !data) return <div className="loading">Failed to load the works index.</div>

  return (
    <>
      <div className="hero-header">
        <h1>Works in the <em>Exegesis</em></h1>
        <p className="hero-subtitle">
          Philip K. Dick spent the last eight years of his life reading his own fiction back as scripture. These pages
          collect every passage in the <em>Exegesis</em> where he interprets one of his novels or stories &mdash; with a
          summary and analysis of each mention and the theological use he makes of it.
        </p>
      </div>

      <div className="detail-section">
        <p>
          Drawn from {data.total_analyzed_entries.toLocaleString()} analyzed <em>Exegesis</em> entries. Each mention is
          Lane B evidence &mdash; PKD theorizing about his own work, not established doctrine. Works are ordered by how
          often he returns to them.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1rem', marginTop: '1rem' }}>
        {data.works.map(w => (
          <Link
            key={w.slug}
            to={`/exegesis/works/${w.slug}`}
            className="detail-section"
            style={{ textDecoration: 'none', color: 'inherit', display: 'block' }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: '1rem' }}>
              <h2 style={{ margin: 0 }}>
                {w.title}
                {!w.has_writeup && (
                  <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginLeft: '0.6rem', fontWeight: 'normal', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
                    index only
                  </span>
                )}
              </h2>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--accent)', whiteSpace: 'nowrap' }}>
                {w.mention_count} mention{w.mention_count !== 1 ? 's' : ''}
              </span>
            </div>
            {w.theological_headline && (
              <p style={{ color: 'var(--text-secondary)', margin: '0.4rem 0 0.3rem', fontSize: '1rem' }}>
                {w.theological_headline}
              </p>
            )}
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.3rem' }}>
              {w.date_range}
              {w.work_link && (
                <>
                  <span style={{ margin: '0 0.5rem' }}>&middot;</span>
                  canonical work record available
                </>
              )}
            </div>
          </Link>
        ))}
      </div>

      <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--border-light)' }}>
        <Link to="/exegesis">&larr; Back to the Exegesis</Link>
      </div>
    </>
  )
}

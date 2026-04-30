import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface EssayMeta {
  slug: string
  title: string
  subtitle: string
  topic: string
  word_count: number
  primary_lanes: string[]
  key_sources: string[]
  date_drafted: string
}

interface EssayIndex {
  essays: EssayMeta[]
}

export default function Essays() {
  const { data, loading, error } = useData<EssayIndex>('essays/index.json')

  if (loading) return <div className="loading">Loading...</div>
  if (error || !data) return <div className="loading">Failed to load essays index.</div>

  return (
    <>
      <div className="hero-header">
        <h1>Essays</h1>
        <p className="hero-subtitle">
          Long-form pieces drawing on the corpus &mdash; Exegesis segments, archive documents, scholar profiles, and the
          dictionary &mdash; to argue something specific about Philip K. Dick.
        </p>
      </div>

      <div className="detail-section">
        <p>
          Each essay lists its primary <Link to="/archive">evidentiary lanes</Link> and the sources it leans on most
          heavily. Where the literature contains a registered dispute, the essay surfaces it rather than choosing a
          side.
        </p>
      </div>

      <div style={{display:'grid', gridTemplateColumns:'1fr', gap:'1.5rem', marginTop:'1rem'}}>
        {data.essays.map(e => (
          <Link
            key={e.slug}
            to={`/essays/${e.slug}`}
            className="detail-section"
            style={{textDecoration:'none', color:'inherit', display:'block'}}
          >
            <h2 style={{marginTop:0}}>{e.title}</h2>
            <p style={{color:'var(--text-muted)', margin:'0.25rem 0 0.75rem', fontSize:'1rem'}}>
              {e.subtitle}
            </p>
            <div style={{display:'flex', flexWrap:'wrap', gap:'0.5rem', alignItems:'center', fontSize:'0.85rem', color:'var(--text-muted)'}}>
              <span>{e.word_count.toLocaleString()} words</span>
              <span>&middot;</span>
              <span>Lanes: {e.primary_lanes.join(', ')}</span>
              <span>&middot;</span>
              <span>Drafted {e.date_drafted}</span>
            </div>
            <ul style={{marginTop:'0.5rem', fontSize:'0.85rem'}}>
              {e.key_sources.slice(0, 3).map(s => (
                <li key={s} style={{color:'var(--text-muted)'}}>{s}</li>
              ))}
              {e.key_sources.length > 3 && (
                <li style={{color:'var(--text-muted)', fontStyle:'italic'}}>
                  + {e.key_sources.length - 3} more source{e.key_sources.length - 3 === 1 ? '' : 's'}
                </li>
              )}
            </ul>
          </Link>
        ))}
      </div>
    </>
  )
}

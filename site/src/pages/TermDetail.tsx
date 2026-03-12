import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { useData } from '../hooks/useData'

interface TermData {
  term_id: string
  canonical_name: string
  slug: string
  status: string
  review_state: string
  primary_category: string
  thematic_categories: string[] | null
  mention_count: number
  definition: string
  interpretive_note: string
  card_description: string
  full_description: string
  first_appearance: string
  peak_usage_start: string
  peak_usage_end: string
  aliases: { text: string; type: string }[]
  linked_segments: {
    seg_id: string
    match_type: string
    confidence: number
    date_display: string
    summary: string
    title: string
  }[]
  related_terms: {
    name: string
    slug: string
    relation: string
    confidence: number
  }[]
  evidence: {
    text: string
    line_start: number
    line_end: number
    matched_alias: string
    confidence: string
    source_method: string
  }[]
}

export default function TermDetail() {
  const { slug } = useParams()
  const { data: term, loading, error } = useData<TermData>(`dictionary/terms/${slug}.json`)

  if (loading) return <div className="loading">Loading...</div>
  if (error || !term) {
    return (
      <div className="page-header">
        <h1>Term Not Found</h1>
        <p>{slug}</p>
        <Link to="/dictionary">Back to Dictionary</Link>
      </div>
    )
  }

  return (
    <>
      <div className="page-header">
        <h1>{term.canonical_name}</h1>
        <p>
          <span className={`badge badge-${term.status}`}>{term.status}</span>
          {' '}
          <span className="confidence-label">{term.review_state}</span>
          {' '}
          {term.primary_category && <span className="badge badge-category">{term.primary_category}</span>}
          <span style={{marginLeft:'1rem', color:'var(--text-muted)'}}>
            {term.mention_count.toLocaleString()} mentions
          </span>
        </p>
      </div>

      {term.aliases.length > 0 && (
        <div className="detail-section">
          <h2>Also Known As</h2>
          <p>{term.aliases.map(a => a.text).join(', ')}</p>
        </div>
      )}

      {term.first_appearance && (
        <div className="detail-section">
          <h2>Chronology</h2>
          <p>
            First appearance: <strong>{term.first_appearance}</strong>
            {term.peak_usage_start && (
              <span style={{marginLeft:'1.5rem'}}>
                Peak usage: <strong>{term.peak_usage_start}{term.peak_usage_end && term.peak_usage_end !== term.peak_usage_start ? `-${term.peak_usage_end}` : ''}</strong>
              </span>
            )}
          </p>
        </div>
      )}

      {term.full_description && (
        <div className="detail-section">
          <h2>Description</h2>
          <ReactMarkdown>{term.full_description}</ReactMarkdown>
        </div>
      )}

      {term.definition && !term.full_description && (
        <div className="detail-section">
          <h2>Definition</h2>
          <p>{term.definition}</p>
        </div>
      )}

      {term.related_terms.length > 0 && (
        <div className="detail-section">
          <h2>Related Terms</h2>
          <div style={{display:'flex', flexWrap:'wrap', gap:'0.5rem'}}>
            {term.related_terms.slice(0, 30).map((r, i) => (
              <Link
                key={i}
                to={`/dictionary/${r.slug}`}
                className="badge badge-category"
                style={{textDecoration:'none'}}
              >
                {r.name}
              </Link>
            ))}
          </div>
        </div>
      )}

      {term.linked_segments.length > 0 && (
        <div className="detail-section">
          <h2>Linked Segments ({term.linked_segments.length})</h2>
          {term.linked_segments.map((seg, i) => (
            <div key={i} className={`confidence-${seg.confidence}`} style={{marginBottom:'0.75rem'}}>
              <div style={{display:'flex', gap:'0.75rem', alignItems:'baseline'}}>
                <Link to={`/segments/${seg.seg_id}`} style={{fontWeight:600}}>
                  {seg.title || seg.seg_id}
                </Link>
                <span style={{color:'var(--text-muted)', fontSize:'0.85rem'}}>{seg.date_display}</span>
                <span className="confidence-label">{seg.match_type}</span>
              </div>
              {seg.summary && <p style={{fontSize:'0.85rem', color:'var(--text-secondary)', marginTop:'0.25rem'}}>{seg.summary}</p>}
            </div>
          ))}
        </div>
      )}

      {term.evidence.length > 0 && (
        <div className="detail-section">
          <h2>Evidence Passages</h2>
          {term.evidence.map((ev, i) => (
            <div key={i} style={{marginBottom:'1rem'}}>
              <div className="card-meta" style={{marginBottom:'0.25rem'}}>
                <span>Lines {ev.line_start}-{ev.line_end}</span>
                <span className="confidence-label">{ev.source_method}</span>
                {ev.matched_alias !== term.canonical_name && (
                  <span>matched: "{ev.matched_alias}"</span>
                )}
              </div>
              <div className="evidence-excerpt">{ev.text}</div>
            </div>
          ))}
        </div>
      )}

      <div style={{marginTop:'2rem', paddingTop:'1rem', borderTop:'1px solid var(--border-light)'}}>
        <Link to="/dictionary">Back to Dictionary</Link>
      </div>
    </>
  )
}

import { useParams, Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface SegmentData {
  seg_id: string
  doc_id: string
  title: string
  date_display: string
  date_confidence: string
  concise_summary: string
  key_claims: string[] | null
  recurring_concepts: string[] | null
  people_entities: string[] | null
  texts_works: string[] | null
  autobiographical: string[] | null
  theological_motifs: string[] | null
  symbols_images: string[] | null
  tensions: string[] | null
  evidence_quotes: string[] | null
  uncertainty_flags: string[] | null
  reading_excerpt: string
  word_count: number
}

// Segment detail is loaded from the year file; we search for the segment
// For now, we fetch all years and find the segment
export default function SegmentDetail() {
  const { id } = useParams()

  // Try to extract year from segment ID for efficient loading
  const yearMatch = id?.match(/^SEG_EXEG_(\d{4})/)
  const year = yearMatch ? yearMatch[1] : null

  const { data: segments, loading } = useData<SegmentData[]>(
    year ? `timeline/years/${year}.json` : 'timeline/index.json'
  )

  if (loading) return <div className="loading">Loading...</div>

  const seg = segments?.find(s => s.seg_id === id)

  if (!seg) {
    return (
      <div className="page-header">
        <h1>Segment Not Found</h1>
        <p>Could not locate segment {id}</p>
        <Link to="/timeline">Back to Timeline</Link>
      </div>
    )
  }

  return (
    <>
      <div className="page-header">
        <h1>{seg.title || seg.seg_id}</h1>
        <p>
          {seg.date_display}
          {seg.date_confidence && seg.date_confidence !== 'exact' && (
            <span className="badge badge-category" style={{marginLeft:'0.5rem'}}>
              {seg.date_confidence}
            </span>
          )}
          {seg.word_count && <span style={{marginLeft:'1rem', color:'var(--text-muted)'}}>{seg.word_count} words</span>}
        </p>
      </div>

      {seg.concise_summary && (
        <div className="detail-section">
          <h2>Summary</h2>
          <p>{seg.concise_summary}</p>
        </div>
      )}

      <Section title="Key Claims" items={seg.key_claims} />
      <Section title="Recurring Concepts" items={seg.recurring_concepts} linkTo="dictionary" />
      <Section title="People & Entities" items={seg.people_entities} />
      <Section title="Texts & Works Referenced" items={seg.texts_works} />
      <Section title="Autobiographical Events" items={seg.autobiographical} />
      <Section title="Theological & Philosophical Motifs" items={seg.theological_motifs} />
      <Section title="Symbols, Images & Metaphors" items={seg.symbols_images} />
      <Section title="Tensions & Contradictions" items={seg.tensions} />

      {seg.evidence_quotes && seg.evidence_quotes.length > 0 && (
        <div className="detail-section">
          <h2>Evidence Quotes</h2>
          {seg.evidence_quotes.map((q, i) => (
            <div key={i} className="evidence-excerpt">{q}</div>
          ))}
        </div>
      )}

      <Section title="Uncertainty Flags" items={seg.uncertainty_flags} />

      {seg.reading_excerpt && (
        <div className="detail-section">
          <h2>Reading Excerpt</h2>
          <div className="evidence-excerpt">{seg.reading_excerpt}</div>
        </div>
      )}

      <div style={{marginTop:'2rem', paddingTop:'1rem', borderTop:'1px solid var(--border-light)'}}>
        <Link to={year ? `/timeline/${year}` : '/timeline'}>Back to Timeline</Link>
      </div>
    </>
  )
}

function Section({ title, items, linkTo }: { title: string; items: string[] | null; linkTo?: string }) {
  if (!items || items.length === 0) return null

  return (
    <div className="detail-section">
      <h2>{title}</h2>
      <ul>
        {items.map((item, i) => (
          <li key={i}>
            {linkTo ? (
              <Link to={`/${linkTo}/${item.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`}>
                {item}
              </Link>
            ) : (
              item
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}

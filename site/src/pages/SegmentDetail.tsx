import { useParams, Link } from 'react-router-dom'
import { useData } from '../hooks/useData'
import { useMemo } from 'react'
import { formatSegmentTitle } from '../utils/formatTitle'

interface ArchiveSummary {
  doc_id: string
  slug: string
}

interface LinkedTerm {
  term_id: string
  name: string
  slug: string
  match_type: string
  confidence: number
  matched_text: string | null
}

interface LinkedName {
  name_id: string
  name: string
  slug: string
  match_type: string
  confidence: number
}

interface EvidenceExcerpt {
  text: string
  matched_alias: string
  term_id: string
  term_name: string
  term_slug: string
}

interface Neighbor {
  seg_id: string
  title: string
  position: number
}

interface SegmentData {
  seg_id: string
  doc_id: string
  title: string
  position: number | null
  date_start: string | null
  date_display: string
  date_confidence: string
  date_basis: string | null
  concise_summary: string | null
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
  reading_excerpt: string | null
  word_count: number
  raw_text: string | null
  raw_text_char_count: number | null
  linked_terms: LinkedTerm[]
  linked_names: LinkedName[]
  evidence_excerpts: EvidenceExcerpt[]
  neighbors: Neighbor[]
  document: {
    title: string
    doc_type: string
    author: string
    date_display: string
  } | null
}

const CONFIDENCE_LABELS: Record<number, string> = {
  1: 'exact text match',
  2: 'alias/summary match',
  3: 'fuzzy match',
  4: 'conceptual link',
  5: 'speculative',
}

export default function SegmentDetail() {
  const { id } = useParams()
  const { data: seg, loading, error } = useData<SegmentData>(`segments/${id}.json`)
  const { data: archiveIndex } = useData<ArchiveSummary[]>('archive/index.json')


  const docSlugMap = useMemo(() => {
    const map = new Map<string, string>()
    if (!archiveIndex) return map
    for (const entry of archiveIndex) {
      map.set(entry.doc_id, entry.slug)
    }
    return map
  }, [archiveIndex])

  if (loading) return <div className="loading">Loading...</div>

  if (error || !seg) {
    return (
      <div className="page-header">
        <h1>Segment Not Found</h1>
        <p>Could not locate segment {id}</p>
        <Link to="/timeline">Back to Timeline</Link>
      </div>
    )
  }

  // Separate linked terms by confidence
  const strongTerms = (seg.linked_terms || []).filter(t => t.confidence <= 2)
  const mediumTerms = (seg.linked_terms || []).filter(t => t.confidence === 3)
  const weakTerms = (seg.linked_terms || []).filter(t => t.confidence >= 4)

  const yearMatch = seg.date_start?.match(/^(\d{4})/)
  const year = yearMatch ? yearMatch[1] : null

  return (
    <>
      <div className="page-header">
        <h1>{formatSegmentTitle(seg.title, seg.seg_id)}</h1>
        <p>
          {seg.date_display}
          {seg.date_confidence && seg.date_confidence !== 'exact' && (
            <span className="badge badge-category" style={{marginLeft:'0.5rem'}}>
              {seg.date_confidence}
            </span>
          )}
          {seg.word_count && <span style={{marginLeft:'1rem', color:'var(--text-muted)'}}>{seg.word_count.toLocaleString()} words</span>}
        </p>
        {seg.document && (
          <p style={{fontSize:'0.85rem', color:'var(--text-muted)'}}>
            {seg.document.doc_type === 'exegesis_section' ? 'Exegesis' : seg.document.doc_type.replace(/_/g, ' ')}
            {seg.document.title && seg.document.title !== 'Letter' && ` \u2014 ${seg.document.title} section`}
          </p>
        )}
      </div>

      {/* Navigation between segments */}
      {seg.neighbors && seg.neighbors.length > 0 && (
        <div style={{display:'flex', justifyContent:'space-between', marginBottom:'1rem', fontSize:'0.85rem'}}>
          {seg.neighbors.find(n => n.position < (seg.position ?? 0))
            ? <Link to={`/segments/${seg.neighbors.find(n => n.position < (seg.position ?? 0))!.seg_id}`}>
                ← Previous chunk
              </Link>
            : <span />
          }
          {seg.neighbors.find(n => n.position > (seg.position ?? Infinity))
            ? <Link to={`/segments/${seg.neighbors.find(n => n.position > (seg.position ?? Infinity))!.seg_id}`}>
                Next chunk →
              </Link>
            : <span />
          }
        </div>
      )}

      {seg.concise_summary && (
        <div className="detail-section">
          <h2>Summary</h2>
          <p>{seg.concise_summary}</p>
        </div>
      )}

      {/* Raw Exegesis text hidden — verbatim PKD text not displayed */}

      <Section title="Key Claims" items={seg.key_claims} />
      <Section title="Recurring Concepts" items={seg.recurring_concepts} linkTo="dictionary" />
      <Section title="People & Entities" items={seg.people_entities} />
      <Section title="Texts & Works Referenced" items={seg.texts_works} />
      <Section title="Autobiographical Events" items={seg.autobiographical} />
      <Section title="Theological & Philosophical Motifs" items={seg.theological_motifs} />
      <Section title="Symbols, Images & Metaphors" items={seg.symbols_images} />
      <Section title="Tensions & Contradictions" items={seg.tensions} />

      {/* Evidence quotes hidden — verbatim PKD text not displayed */}

      <Section title="Uncertainty Flags" items={seg.uncertainty_flags} />

      {/* Reading excerpt hidden — verbatim PKD text not displayed */}

      {/* Linked Terms with confidence badges */}
      {(strongTerms.length > 0 || mediumTerms.length > 0 || weakTerms.length > 0) && (
        <div className="detail-section">
          <h2>Linked Terms ({seg.linked_terms.length})</h2>

          {strongTerms.length > 0 && (
            <div style={{marginBottom:'0.75rem'}}>
              <h3 style={{fontSize:'0.85rem', color:'var(--text-muted)', marginBottom:'0.5rem'}}>
                Text-confirmed ({strongTerms.length})
              </h3>
              <div style={{display:'flex', flexWrap:'wrap', gap:'0.4rem'}}>
                {strongTerms.map((t, i) => (
                  <Link key={i} to={`/dictionary/${t.slug}`}
                    className="badge badge-category"
                    style={{textDecoration:'none'}}
                    title={`${CONFIDENCE_LABELS[t.confidence]}${t.matched_text ? ': "' + t.matched_text + '"' : ''}`}
                  >
                    {t.name}
                  </Link>
                ))}
              </div>
            </div>
          )}

          {mediumTerms.length > 0 && (
            <div style={{marginBottom:'0.75rem'}}>
              <h3 style={{fontSize:'0.85rem', color:'var(--text-muted)', marginBottom:'0.5rem'}}>
                Fuzzy matches ({mediumTerms.length})
              </h3>
              <div style={{display:'flex', flexWrap:'wrap', gap:'0.4rem', opacity:0.85}}>
                {mediumTerms.map((t, i) => (
                  <Link key={i} to={`/dictionary/${t.slug}`}
                    className="badge badge-category"
                    style={{textDecoration:'none', opacity:0.8}}
                    title={`${CONFIDENCE_LABELS[t.confidence]}${t.matched_text ? ': "' + t.matched_text + '"' : ''}`}
                  >
                    {t.name}
                  </Link>
                ))}
              </div>
            </div>
          )}

          {weakTerms.length > 0 && (
            <div>
              <h3 style={{fontSize:'0.85rem', color:'var(--text-muted)', marginBottom:'0.5rem'}}>
                Conceptual ({weakTerms.length})
              </h3>
              <div style={{display:'flex', flexWrap:'wrap', gap:'0.4rem', opacity:0.7}}>
                {weakTerms.slice(0, 30).map((t, i) => (
                  <Link key={i} to={`/dictionary/${t.slug}`}
                    style={{
                      textDecoration:'none', fontSize:'0.8rem',
                      color:'var(--text-secondary)', borderBottom:'1px dotted var(--border-light)',
                    }}
                    title={CONFIDENCE_LABELS[t.confidence]}
                  >
                    {t.name}
                  </Link>
                ))}
                {weakTerms.length > 30 && (
                  <span style={{fontSize:'0.8rem', color:'var(--text-muted)'}}>
                    +{weakTerms.length - 30} more
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Linked Names */}
      {seg.linked_names && seg.linked_names.length > 0 && (
        <div className="detail-section">
          <h2>Names ({seg.linked_names.length})</h2>
          <div style={{display:'flex', flexWrap:'wrap', gap:'0.4rem'}}>
            {seg.linked_names.map((n, i) => (
              <Link key={i} to={`/names/${n.slug}`}
                className="badge badge-category"
                style={{textDecoration:'none'}}
              >
                {n.name}
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Evidence from dictionary terms */}
      {seg.evidence_excerpts && seg.evidence_excerpts.length > 0 && (
        <div className="detail-section">
          <h2>Evidence Linked to This Segment ({seg.evidence_excerpts.length})</h2>
          {seg.evidence_excerpts.map((ev, i) => (
            <div key={i} style={{marginBottom:'0.75rem'}}>
              <div style={{fontSize:'0.85rem', marginBottom:'0.25rem'}}>
                <Link to={`/dictionary/${ev.term_slug}`} style={{fontWeight:600}}>
                  {ev.term_name}
                </Link>
                {ev.matched_alias && ev.matched_alias !== ev.term_name && (
                  <span style={{color:'var(--text-muted)', marginLeft:'0.5rem'}}>
                    (matched: "{ev.matched_alias}")
                  </span>
                )}
              </div>
              <div className="evidence-excerpt" style={{fontSize:'0.85rem'}}>
                {ev.text}
              </div>
            </div>
          ))}
        </div>
      )}

      <div style={{marginTop:'2rem', paddingTop:'1rem', borderTop:'1px solid var(--border-light)', display:'flex', gap:'1rem'}}>
        <Link to={year ? `/timeline/${year}` : '/timeline'}>Back to Timeline</Link>
        {seg.doc_id && docSlugMap.get(seg.doc_id) && (
          <Link to={`/archive/${docSlugMap.get(seg.doc_id)}`}>View Document</Link>
        )}
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

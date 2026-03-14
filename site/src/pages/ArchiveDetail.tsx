import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { useData } from '../hooks/useData'
import EntityLayout from '../components/EntityLayout'

const LANE_LABELS: Record<string, string> = {
  A: 'Fiction', B: 'Exegesis', C: 'Scholarship', D: 'Synthesis', E: 'Primary'
}

interface ArchiveData {
  doc_id: string
  title: string
  slug: string
  author: string
  doc_type: string
  category: string
  date_display: string
  is_pkd_authored: boolean
  card_summary: string
  page_summary: string
  page_count: number
  ingest_level: string
  extraction_status: string
  evidentiary_lane: string | null
  source_reliability: string | null
  people_mentioned: string[]
  works_discussed: string[]
  linked_terms: string[]
  assets: { path: string; type: string; size_mb: number }[]
}

export default function ArchiveDetail() {
  const { slug } = useParams()
  const { data: doc, loading, error } = useData<ArchiveData>(`archive/docs/${slug}.json`)

  if (loading) return <div className="loading">Loading...</div>
  if (error || !doc) {
    return (
      <div className="page-header">
        <h1>Document Not Found</h1>
        <Link to="/archive">Back to Archive</Link>
      </div>
    )
  }

  const badges = [
    { label: doc.category },
    ...(doc.is_pkd_authored ? [{ label: 'PKD-Authored', className: 'badge-provisional' }] : []),
    ...(doc.evidentiary_lane ? [{ label: `Lane ${doc.evidentiary_lane}: ${LANE_LABELS[doc.evidentiary_lane] || doc.evidentiary_lane}` }] : []),
  ]

  const desc = [
    doc.author,
    doc.date_display !== 'Unknown' ? doc.date_display : null,
    doc.page_count ? `${doc.page_count} pages` : null,
  ].filter(Boolean).join(' \u2022 ')

  return (
    <EntityLayout
      title={doc.title}
      entityType="archive"
      entityId={doc.slug}
      badges={badges}
      description={desc || undefined}
      tags={[{ label: doc.category, to: `/tag/${encodeURIComponent(doc.category.toLowerCase())}` }]}
      backLink={{ label: 'Back to Archive', to: '/archive' }}
    >
      {doc.page_summary && (
        <div className="detail-section">
          <h2>Summary</h2>
          <ReactMarkdown>{doc.page_summary}</ReactMarkdown>
        </div>
      )}

      {!doc.page_summary && doc.card_summary && (
        <div className="detail-section">
          <h2>Summary</h2>
          <p>{doc.card_summary}</p>
        </div>
      )}

      {doc.people_mentioned && doc.people_mentioned.length > 0 && (
        <div className="detail-section">
          <h2>People Mentioned</h2>
          <div style={{display:'flex', flexWrap:'wrap', gap:'0.35rem'}}>
            {doc.people_mentioned.map(p => (
              <Link key={p} to={`/names/${p.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`} className="badge badge-category" style={{textDecoration:'none'}}>{p}</Link>
            ))}
          </div>
        </div>
      )}

      {doc.works_discussed && doc.works_discussed.length > 0 && (
        <div className="detail-section">
          <h2>Works Discussed</h2>
          <div style={{display:'flex', flexWrap:'wrap', gap:'0.35rem'}}>
            {doc.works_discussed.map(w => (
              <span key={w} className="badge badge-category">{w}</span>
            ))}
          </div>
        </div>
      )}

      {doc.linked_terms && doc.linked_terms.length > 0 && (
        <div className="detail-section">
          <h2>Linked Terms</h2>
          <div style={{display:'flex', flexWrap:'wrap', gap:'0.35rem'}}>
            {doc.linked_terms.map(t => (
              <Link key={t} to={`/dictionary/${t.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`} className="badge badge-category" style={{textDecoration:'none'}}>{t}</Link>
            ))}
          </div>
        </div>
      )}

      <div className="detail-section">
        <h2>Metadata</h2>
        <ul>
          <li>Document type: {doc.doc_type}</li>
          <li>Extraction level: {doc.ingest_level}</li>
          <li>Extraction status: {doc.extraction_status}</li>
          {doc.source_reliability && <li>Source reliability: {doc.source_reliability}</li>}
        </ul>
      </div>
    </EntityLayout>
  )
}

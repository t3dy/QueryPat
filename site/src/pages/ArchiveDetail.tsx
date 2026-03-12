import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { useData } from '../hooks/useData'

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

  return (
    <>
      <div className="page-header">
        <h1>{doc.title}</h1>
        <p>
          {doc.author && <span>{doc.author}</span>}
          {doc.date_display && doc.date_display !== 'Unknown' && (
            <span style={{marginLeft:'1rem'}}>{doc.date_display}</span>
          )}
          <span className="badge badge-category" style={{marginLeft:'1rem'}}>{doc.category}</span>
          {doc.is_pkd_authored && <span className="badge badge-provisional" style={{marginLeft:'0.5rem'}}>PKD-Authored</span>}
          {doc.page_count && <span style={{marginLeft:'1rem', color:'var(--text-muted)'}}>{doc.page_count} pages</span>}
        </p>
      </div>

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

      <div className="detail-section">
        <h2>Metadata</h2>
        <ul>
          <li>Document type: {doc.doc_type}</li>
          <li>Extraction level: {doc.ingest_level}</li>
          <li>Extraction status: {doc.extraction_status}</li>
        </ul>
      </div>

      <div style={{marginTop:'2rem', paddingTop:'1rem', borderTop:'1px solid var(--border-light)'}}>
        <Link to="/archive">Back to Archive</Link>
      </div>
    </>
  )
}

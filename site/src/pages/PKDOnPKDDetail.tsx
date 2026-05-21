import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { useData } from '../hooks/useData'
import EntityLayout from '../components/EntityLayout'

interface MentionExcerpt {
  match_text: string
  context_snippet: string
  mention_order: number
}

interface SourceDocument {
  doc_id: string
  doc_slug: string
  doc_title: string
  doc_type: string
  date_display: string
  mention_count: number
  excerpts: MentionExcerpt[]
}

interface PKDOnPKDRecord {
  work_id: string
  canonical_title: string
  slug: string
  author: string
  work_type: string
  category: string
  mention_count: number
  source_doc_count: number
  source_doc_types: Record<string, number>
  card_summary: string
  page_summary: string
  top_sources: SourceDocument[]
  source_documents: SourceDocument[]
}

const SOURCE_LABELS: Record<string, string> = {
  archive_pdf: 'Primary text',
  biography: 'Biography',
  exegesis_section: 'Exegesis',
  fan_publication: 'Fan publication',
  interview: 'Interview',
  letter: 'Letter',
  novel: 'Novel',
  scholarship: 'Scholarship',
  short_story: 'Short story',
  other: 'Other writing',
}

export default function PKDOnPKDDetail() {
  const { slug } = useParams()
  const { data: record, loading } = useData<PKDOnPKDRecord>(`pkd-on-pkd/${slug}.json`)

  if (loading) return <div className="loading">Loading PKD on PKD...</div>

  if (!record) {
    return (
      <div className="page-header">
        <h1>PKD on PKD Entry Not Found</h1>
        <Link to="/pkd-on-pkd">Back to PKD on PKD</Link>
      </div>
    )
  }

  return (
    <EntityLayout
      title={record.canonical_title}
      entityType="novel"
      entityId={record.work_id}
      badges={[
        { label: `${record.mention_count} mentions` },
        { label: `${record.source_doc_count} source docs`, className: 'badge-background' },
        { label: SOURCE_LABELS[record.work_type] || record.work_type },
      ]}
      description={`${record.author} - PKD on PKD catalog`}
      backLink={{ label: 'Back to PKD on PKD', to: '/pkd-on-pkd' }}
    >
      <div className="detail-section">
        <h2>Summary</h2>
        <ReactMarkdown>{record.page_summary || record.card_summary}</ReactMarkdown>
      </div>

      {record.top_sources?.length > 0 && (
        <div className="detail-section">
          <h2>Source Breakdown</h2>
          <ul>
            {record.top_sources.map(source => (
              <li key={source.doc_id}>
                <Link to={`/archive/${source.doc_slug}`}>{source.doc_title}</Link>
                {source.date_display && <span style={{ color: 'var(--text-muted)' }}> {source.date_display}</span>}
                <span style={{ color: 'var(--text-muted)' }}> ({source.mention_count} mention{source.mention_count === 1 ? '' : 's'})</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {record.source_documents?.length > 0 && (
        <div className="detail-section">
          <h2>Mentions by Source</h2>
          <div className="relation-block">
            {record.source_documents.map(source => (
              <div key={source.doc_id} style={{ marginBottom: '1rem' }}>
                <h4 style={{ marginBottom: '0.25rem' }}>
                  <Link to={`/archive/${source.doc_slug}`}>{source.doc_title}</Link>
                </h4>
                <div className="card-meta" style={{ marginBottom: '0.5rem' }}>
                  {source.date_display && <span>{source.date_display}</span>}
                  <span>{SOURCE_LABELS[source.doc_type] || source.doc_type}</span>
                  <span>{source.mention_count} mention{source.mention_count === 1 ? '' : 's'}</span>
                </div>
                <ul>
                  {source.excerpts.map(excerpt => (
                    <li key={`${source.doc_id}-${excerpt.mention_order}`}>
                      <span style={{ color: 'var(--text-muted)' }}>{excerpt.match_text}: </span>
                      {excerpt.context_snippet}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
    </EntityLayout>
  )
}

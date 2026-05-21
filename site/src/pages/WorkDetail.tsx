import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { useData } from '../hooks/useData'
import EntityLayout from '../components/EntityLayout'

interface RelatedDoc {
  doc_id: string
  title: string
  slug: string
  date_display: string
  doc_type: string
}

interface WorkRecord {
  work_id: string
  canonical_title: string
  slug: string
  author: string
  work_type: string
  category: string
  date_display: string
  date_start: string
  card_summary: string
  page_summary: string
  page_count: number
  source_count: number
  themes?: string[]
  related_docs: RelatedDoc[]
  first_doc?: { doc_id: string; slug: string; title: string }
}

interface ThemeIndex {
  theme_count: number
  fiction_work_count: number
  themes: {
    theme_id: string
    slug: string
    label: string
    description: string
    work_count: number
  }[]
}

const TYPE_LABELS: Record<string, string> = {
  novels: 'Novel',
  novellas: 'Novella',
  letters: 'Letter',
  short_stories: 'Short story',
  essays: 'Essay',
  interviews: 'Interview',
  biographies: 'Biography',
  fan_publications: 'Fan publication',
  newspaper: 'Newspaper',
  archive_pdf: 'Archive item',
  primary: 'Primary text',
}

const CATEGORY_LABELS: Record<string, string> = {
  interviews: 'Interviews',
  letters: 'Letters',
  newspaper: 'Newspaper',
  novels: 'Novels',
  primary: 'Primary texts',
  short_stories: 'Short stories',
}

export default function WorkDetail() {
  const { slug } = useParams()
  const { data: works, loading } = useData<WorkRecord[]>('works/index.json')
  const { data: themeIndex } = useData<ThemeIndex>('themes/index.json')

  if (loading || !themeIndex) return <div className="loading">Loading...</div>

  const work = works?.find(w => w.slug === slug)
  if (!work) {
    return (
      <div className="page-header">
        <h1>Work Not Found</h1>
        <Link to="/works">Back to Works</Link>
      </div>
    )
  }

  const themeMap = new Map(themeIndex.themes.map(theme => [theme.slug, theme]))

  return (
    <EntityLayout
      title={work.canonical_title}
      entityType="work"
      entityId={work.work_id}
      badges={[
        { label: CATEGORY_LABELS[work.category] || work.category },
        { label: TYPE_LABELS[work.work_type] || work.work_type },
        { label: `${work.source_count} linked docs`, className: 'badge-background' },
      ]}
      tags={(work.themes || []).map(slug => ({ label: themeMap.get(slug)?.label || slug.replace(/-/g, ' '), to: `/themes/${slug}` }))}
      description={`${work.author}${work.date_display ? ` - ${work.date_display}` : ''}${work.page_count ? ` - ${work.page_count} pp` : ''}`}
      backLink={{ label: 'Back to Works', to: '/works' }}
    >
      <div className="detail-section">
        <h2>Summary</h2>
        <ReactMarkdown>{work.page_summary || work.card_summary}</ReactMarkdown>
      </div>

      {work.category === 'novels' && (
        <div className="detail-section">
          <h2>PKD on PKD</h2>
          <p>
            <Link to={`/pkd-on-pkd/${work.slug}`}>Open the PKD on PKD catalog for this novel</Link>
          </p>
        </div>
      )}

      {work.related_docs && work.related_docs.length > 0 && (
        <div className="detail-section">
          <h2>Linked Archive Docs</h2>
          <ul>
            {work.related_docs.map(doc => (
              <li key={doc.doc_id}>
                <Link to={`/archive/${doc.slug}`}>{doc.title}</Link>
                {doc.date_display && <span style={{ color: 'var(--text-muted)' }}> {doc.date_display}</span>}
                <span style={{ color: 'var(--text-muted)' }}> ({TYPE_LABELS[doc.doc_type] || doc.doc_type})</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="detail-section">
        <h2>Metadata</h2>
        <ul>
          <li>Work type: {TYPE_LABELS[work.work_type] || work.work_type}</li>
          <li>Category: {CATEGORY_LABELS[work.category] || work.category}</li>
          <li>Linked documents: {work.source_count}</li>
          <li>First known record: {work.first_doc?.title || 'unknown'}</li>
        </ul>
      </div>
    </EntityLayout>
  )
}

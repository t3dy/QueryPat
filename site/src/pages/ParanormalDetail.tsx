import { Link, useParams } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { useData } from '../hooks/useData'
import ExploreFooter from '../components/ExploreFooter'
import BookmarkButton from '../components/BookmarkButton'
import type { ParanormalEntry } from './Paranormal'

interface ParanormalIndex {
  total: number
  entries: ParanormalEntry[]
}

const CATEGORY_COLORS: Record<string, string> = {
  'soviet-psychotronic': '#7a3c3c',
  'kozyrev-time-energy': '#3c5a7a',
  'precognition': '#5a3c7a',
  'esp-telepathy': '#3c7a5a',
  'valis-satellite': '#6b3500',
  'anamnesis': '#7a6030',
  'second-sight': '#4a5a3c',
  'spiritual-paranormal': '#3c4a6b',
  'mind-control': '#5a4a3c',
}

const CATEGORY_LABELS: Record<string, string> = {
  'soviet-psychotronic': 'Soviet Psychotronic',
  'kozyrev-time-energy': 'Kozyrev Time-Energy',
  'precognition': 'Precognition',
  'esp-telepathy': 'ESP & Telepathy',
  'valis-satellite': 'VALIS & Satellite',
  'anamnesis': 'Anamnesis',
  'second-sight': 'Second Sight & Prophecy',
  'spiritual-paranormal': 'Spiritual Paranormal',
  'mind-control': 'Mind Control & Subliminal',
}

export default function ParanormalDetail() {
  const { slug } = useParams()
  const { data, loading } = useData<ParanormalIndex>('paranormal/index.json')

  if (loading || !data) return <div className="loading">Loading…</div>

  const entry = data.entries.find(e => e.slug === slug)

  if (!entry) {
    return (
      <div className="detail-section">
        <p>Entry not found.</p>
        <Link to="/paranormal">&larr; All paranormal topics</Link>
      </div>
    )
  }

  const color = CATEGORY_COLORS[entry.category_slug] || 'var(--accent)'
  const related = data.entries.filter(e => entry.related_slugs.includes(e.slug))

  return (
    <article>
      <div className="hero-header" style={{ paddingBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '1rem' }}>
          <div>
            <span style={{
              display: 'inline-block',
              fontSize: '0.7rem',
              padding: '0.15rem 0.45rem',
              background: color,
              color: '#fff',
              borderRadius: '3px',
              textTransform: 'uppercase',
              letterSpacing: '0.04em',
              marginBottom: '0.5rem',
            }}>
              {CATEGORY_LABELS[entry.category_slug] || entry.category}
            </span>
            <h1 style={{ margin: 0 }}>{entry.title}</h1>
          </div>
          <BookmarkButton entityType="paranormal" entityId={entry.slug} title={entry.title} />
        </div>
        <p className="hero-subtitle" style={{ margin: '0.5rem 0 0' }}>
          {entry.card_summary}
        </p>
      </div>

      {entry.primary_quote && (
        <div className="detail-section" style={{
          borderLeft: '3px solid var(--accent)',
          paddingLeft: '1.25rem',
        }}>
          <p style={{ fontStyle: 'italic', fontSize: '1.05rem', margin: 0, lineHeight: 1.6 }}>
            "{entry.primary_quote}"
          </p>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: '0.4rem 0 0' }}>
            — PKD, <em>The Exegesis</em>
            {entry.primary_quote_line ? ` (${entry.primary_quote_line})` : ''}
          </p>
        </div>
      )}

      {entry.full_essay && (
        <div className="detail-section" style={{ lineHeight: 1.75 }}>
          <h2>Essay</h2>
          <div className="prose-content">
            <ReactMarkdown>{entry.full_essay}</ReactMarkdown>
          </div>
        </div>
      )}

      {entry.tags.length > 0 && (
        <div className="detail-section">
          <h2>Tags</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
            {entry.tags.map(tag => (
              <span key={tag} className="entity-tag">{tag}</span>
            ))}
          </div>
        </div>
      )}

      {related.length > 0 && (
        <div className="detail-section">
          <h2>Related entries</h2>
          <div style={{ display: 'grid', gap: '0.75rem' }}>
            {related.map(r => (
              <div key={r.slug} style={{
                borderLeft: '2px solid var(--border-light)',
                paddingLeft: '0.75rem',
              }}>
                <Link to={`/paranormal/${r.slug}`} style={{ fontWeight: 600 }}>
                  {r.title}
                </Link>
                <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', margin: '0.2rem 0 0' }}>
                  {r.card_summary}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      <ExploreFooter groups={[
        {
          section: 'PKD on the Paranormal', items: [
            { label: 'All 50 paranormal topics', to: '/paranormal' },
            { label: `${CATEGORY_LABELS[entry.category_slug] || entry.category} entries`, to: '/paranormal' },
          ],
        },
        {
          section: 'Companion pages', items: [
            { label: 'Theophanies & Visionary Experiences', to: '/theophanies' },
            { label: 'Dictionary of PKD terms', to: '/dictionary' },
            { label: 'Timeline 1974', to: '/timeline/1974' },
          ],
        },
      ]} />

      <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--border-light)' }}>
        <Link to="/paranormal">&larr; All paranormal topics</Link>
      </div>
    </article>
  )
}

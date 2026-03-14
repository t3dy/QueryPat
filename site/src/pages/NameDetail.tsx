import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { useData } from '../hooks/useData'
import { formatSegmentTitle } from '../utils/formatTitle'
import EntityLayout from '../components/EntityLayout'
import ExploreFooter from '../components/ExploreFooter'
import BacklinksPanel from '../components/BacklinksPanel'
import HoverPreview from '../components/HoverPreview'

interface NameData {
  name_id: string
  canonical_form: string
  slug: string
  entity_type: string
  source_type: string
  status: string
  review_state: string
  etymology: string | null
  origin_language: string | null
  allusion_type: string[] | null
  allusion_target: string | null
  wordplay_note: string | null
  symbolic_note: string | null
  card_description: string | null
  full_description: string | null
  mention_count: number
  first_work: string | null
  work_list: string[] | null
  aliases: { text: string; type: string }[]
  linked_segments: {
    seg_id: string
    match_type: string
    confidence: number
    matched_text: string
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
  reference?: {
    canonical_form: string
    domain: string
    brief: string
    etymology: string
    origin_language: string
    significance: string
    source_text: string
  }
}

const TYPE_LABELS: Record<string, string> = {
  character: 'Character',
  place: 'Place',
  organization: 'Organization',
  deity_figure: 'Deity / Figure',
  historical_person: 'Historical Person',
  other: 'Other',
}

export default function NameDetail() {
  const { slug } = useParams()
  const { data: name, loading, error } = useData<NameData>(`names/entities/${slug}.json`)

  if (loading) return <div className="loading">Loading...</div>
  if (error || !name) {
    return (
      <div className="page-header">
        <h1>Name Not Found</h1>
        <p>{slug}</p>
        <Link to="/names">Back to Names</Link>
      </div>
    )
  }

  const tags = (name.allusion_type || []).map(a => ({
    label: a,
    to: `/tag/${encodeURIComponent(a.toLowerCase())}`,
  }))

  const exploreGroups = [
    {
      section: 'In the Dictionary',
      items: (name.related_terms || []).slice(0, 3).map(r => ({ label: r.name, to: `/dictionary/${r.slug}` })),
      totalCount: (name.related_terms || []).length,
    },
    {
      section: 'In the Exegesis',
      items: (name.linked_segments || []).slice(0, 3).map(s => ({
        label: formatSegmentTitle(s.title, s.seg_id),
        to: `/segments/${s.seg_id}`,
      })),
      totalCount: (name.linked_segments || []).length,
    },
  ]

  const backlinkGroups = [
    {
      type: 'Exegesis Summaries',
      items: (name.linked_segments || []).map(s => ({
        label: formatSegmentTitle(s.title, s.seg_id),
        to: `/segments/${s.seg_id}`,
        date: s.date_display,
      })),
    },
    {
      type: 'Dictionary Terms',
      items: (name.related_terms || []).map(r => ({
        label: r.name,
        to: `/dictionary/${r.slug}`,
      })),
    },
  ]

  return (
    <EntityLayout
      title={name.canonical_form}
      entityType="name"
      entityId={name.slug}
      badges={[
        { label: TYPE_LABELS[name.entity_type] || name.entity_type },
        ...(name.source_type ? [{ label: name.source_type }] : []),
      ]}
      description={`${name.mention_count} mention${name.mention_count !== 1 ? 's' : ''} in the Exegesis`}
      tags={tags}
      backLink={{ label: 'Back to Names', to: '/names' }}
      footer={
        <>
          <ExploreFooter groups={exploreGroups} />
          <BacklinksPanel groups={backlinkGroups} />
        </>
      }
    >
      {name.aliases && name.aliases.length > 0 && (
        <div className="detail-section">
          <h2>Also Known As</h2>
          <p>{name.aliases.map(a => a.text).join(', ')}</p>
        </div>
      )}

      {(name.etymology || name.origin_language || name.allusion_type) && (
        <div className="detail-section">
          <h2>Etymology & Allusion</h2>
          {name.etymology && (
            <p><strong>Etymology:</strong> {name.etymology}
              {name.origin_language && <span> ({name.origin_language})</span>}
            </p>
          )}
          {name.allusion_type && name.allusion_type.length > 0 && (
            <p><strong>Allusion domains:</strong> {name.allusion_type.join(', ')}</p>
          )}
          {name.allusion_target && (
            <p><strong>Alludes to:</strong> {name.allusion_target}</p>
          )}
        </div>
      )}

      {(name.wordplay_note || name.symbolic_note) && (
        <div className="detail-section">
          <h2>Wordplay & Symbolism</h2>
          {name.wordplay_note && <p><strong>Wordplay:</strong> {name.wordplay_note}</p>}
          {name.symbolic_note && <p><strong>Symbolic charge:</strong> {name.symbolic_note}</p>}
        </div>
      )}

      {name.work_list && name.work_list.length > 0 && (
        <div className="detail-section">
          <h2>Works</h2>
          <p>{name.work_list.join(', ')}</p>
        </div>
      )}

      {name.reference && (
        <div className="detail-section">
          <h2>Reference: {name.reference.domain}</h2>
          <p><strong>{name.reference.canonical_form}</strong> — {name.reference.brief}</p>
          {name.reference.etymology && (
            <p><strong>Etymology:</strong> {name.reference.etymology} ({name.reference.origin_language})</p>
          )}
          {name.reference.significance && (
            <p><strong>PKD significance:</strong> {name.reference.significance}</p>
          )}
          {name.reference.source_text && (
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Source: {name.reference.source_text}</p>
          )}
        </div>
      )}

      {name.related_terms && name.related_terms.length > 0 && (
        <div className="detail-section">
          <h2>Related Dictionary Terms</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {name.related_terms.map((r, i) => (
              <HoverPreview key={i} to={`/dictionary/${r.slug}`} className="badge badge-category" style={{ textDecoration: 'none' }} title={r.relation}>
                {r.name}
              </HoverPreview>
            ))}
          </div>
        </div>
      )}

      {name.linked_segments && name.linked_segments.length > 0 && (
        <div className="detail-section">
          <h2>Linked Segments ({name.linked_segments.length})</h2>
          {name.linked_segments.map((seg, i) => (
            <div key={i} className={`confidence-${seg.confidence}`} style={{ marginBottom: '0.75rem' }}>
              <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'baseline' }}>
                <HoverPreview to={`/segments/${seg.seg_id}`} style={{ fontWeight: 600 }}>
                  {formatSegmentTitle(seg.title, seg.seg_id)}
                </HoverPreview>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>{seg.date_display}</span>
              </div>
              {seg.summary && (
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
                  {seg.summary}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {name.full_description && (
        <div className="detail-section">
          <h2>Full Description</h2>
          <ReactMarkdown>{name.full_description}</ReactMarkdown>
        </div>
      )}

      {name.card_description && !name.full_description && (
        <div className="detail-section">
          <h2>Description</h2>
          <p>{name.card_description}</p>
        </div>
      )}
    </EntityLayout>
  )
}

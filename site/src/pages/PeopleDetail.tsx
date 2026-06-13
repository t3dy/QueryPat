import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { useData } from '../hooks/useData'
import EntityLayout from '../components/EntityLayout'
import ExploreFooter from '../components/ExploreFooter'
import { BIOGRAPHY_CATEGORY_NAMES } from '../data/biographyTaxonomy'

interface PersonEvent {
  id: string
  date: string
  category: string
  event: string
  source: string
  importance: number
}

interface PersonDocument {
  doc_id: string
  title: string
  slug: string
  category: string
  date_display?: string
}

interface PersonScholar {
  scholar_id: string
  name: string
  role: string
  tier: number
  key_works: string[]
}

interface PersonRecord {
  person_id: string
  name: string
  slug: string
  relationship_categories: string[]
  relationship_to_pkd: string
  association_score: number
  card_summary: string
  page_summary: string
  first_year: number | null
  last_year: number | null
  evidence_counts: Record<string, number>
  biography_events: PersonEvent[]
  archive_documents: PersonDocument[]
  scholar_profiles: PersonScholar[]
  name_entry: { slug: string; mention_count: number; card_description?: string } | null
  review_state: string
}

function labelFor(value: string): string {
  const labels: Record<string, string> = {
    ...BIOGRAPHY_CATEGORY_NAMES,
    character_inspiration: 'Character inspiration',
    correspondent: 'Correspondent',
    fellow_sf_author: 'Fellow SF author',
    fan_scholar: 'Fan scholar',
    named_person: 'Named person',
    mentioned_in_document: 'Mentioned in documents',
    spouse_or_partner: 'Spouse or partner',
  }
  return labels[value] || value.replace(/_/g, ' ')
}

export default function PeopleDetail() {
  const { slug } = useParams()
  const { data: people, loading } = useData<PersonRecord[]>('people/pkd-knew.json')

  if (loading) return <div className="loading">Loading...</div>

  const person = people?.find(p => p.slug === slug)
  if (!person) {
    return (
      <div className="page-header">
        <h1>Person Not Found</h1>
        <Link to="/people">Back to People</Link>
      </div>
    )
  }

  const exploreGroups = [
    {
      section: 'Related Archive Docs',
      items: person.archive_documents.slice(0, 5).map(doc => ({
        label: doc.title,
        to: `/archive/${doc.slug}`,
      })),
      totalCount: person.archive_documents.length,
    },
    {
      section: 'Related Scholars',
      items: person.scholar_profiles.slice(0, 5).map(s => ({
        label: s.name,
        to: `/scholars#${s.scholar_id}`,
      })),
      totalCount: person.scholar_profiles.length,
    },
  ]

  return (
    <EntityLayout
      title={person.name}
      entityType="person"
      entityId={person.person_id}
      badges={[
        { label: person.relationship_to_pkd },
        { label: `score ${person.association_score}` },
        { label: person.review_state, className: 'badge-background' },
      ]}
      description={`First known association ${person.first_year || 'unknown'}${person.last_year && person.last_year !== person.first_year ? ` to ${person.last_year}` : ''}`}
      tags={(person.relationship_categories || []).map(cat => ({ label: labelFor(cat), to: `/people?q=${encodeURIComponent(cat)}` }))}
      backLink={{ label: 'Back to People', to: '/people' }}
      footer={<ExploreFooter groups={exploreGroups} />}
    >
      <div className="detail-section">
        <h2>Summary</h2>
        <ReactMarkdown>{person.page_summary || person.card_summary}</ReactMarkdown>
      </div>

      {person.biography_events.length > 0 && (
        <div className="detail-section">
          <h2>Biography Events</h2>
          <ul>
            {person.biography_events.map(ev => (
              <li key={ev.id}>
                <strong>{ev.date}</strong> {ev.event}
                <span style={{ color: 'var(--text-muted)' }}> ({ev.source})</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {person.archive_documents.length > 0 && (
        <div className="detail-section">
          <h2>Archive Documents</h2>
          <ul>
            {person.archive_documents.map(doc => (
              <li key={doc.doc_id}>
                <Link to={`/archive/${doc.slug}`}>{doc.title}</Link>
                {doc.date_display && <span style={{ color: 'var(--text-muted)' }}> {doc.date_display}</span>}
              </li>
            ))}
          </ul>
        </div>
      )}

      {person.scholar_profiles.length > 0 && (
        <div className="detail-section">
          <h2>Scholar Profiles</h2>
          <ul>
            {person.scholar_profiles.map(profile => (
              <li key={profile.scholar_id}>
                <Link to={`/scholars#${profile.scholar_id}`}>{profile.name}</Link>
                <span style={{ color: 'var(--text-muted)' }}> {profile.role}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {person.name_entry && (
        <div className="detail-section">
          <h2>Name Entry</h2>
          <p>
            <Link to={`/names/${person.name_entry.slug}`}>{person.name}</Link>
            {person.name_entry.mention_count ? ` - ${person.name_entry.mention_count} Exegesis mention(s)` : ''}
          </p>
          {person.name_entry.card_description && <p>{person.name_entry.card_description}</p>}
        </div>
      )}

      <div className="detail-section">
        <h2>Metadata</h2>
        <ul>
          <li>Relationship categories: {person.relationship_categories.join(', ')}</li>
          <li>Association score: {person.association_score}</li>
          <li>Evidence links: {Object.entries(person.evidence_counts).map(([k, v]) => `${k}=${v}`).join(', ')}</li>
        </ul>
      </div>
    </EntityLayout>
  )
}

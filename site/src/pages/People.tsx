import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'
import { BIOGRAPHY_CATEGORY_NAMES } from '../data/biographyTaxonomy'

interface EvidenceCounts {
  archive_documents?: number
  biography_events?: number
  names_index?: number
  scholar_profiles?: number
  [key: string]: number | undefined
}

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
  is_pkd_authored?: boolean
}

interface PersonScholar {
  scholar_id: string
  name: string
  role: string
  tier: number
  key_works: string[]
}

interface PersonNameEntry {
  name_id: string
  slug: string
  mention_count: number
  card_description?: string
  source_type?: string
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
  evidence_counts: EvidenceCounts
  biography_events: PersonEvent[]
  archive_documents: PersonDocument[]
  scholar_profiles: PersonScholar[]
  name_entry: PersonNameEntry | null
  review_state: string
}

type QualityMode = 'high' | 'all'

const CATEGORY_LABELS: Record<string, string> = {
  ...BIOGRAPHY_CATEGORY_NAMES,
  archive_documents: 'Archive documents',
  author: 'Author',
  biography_events: 'Biography events',
  doctor_or_therapist: 'Doctor or therapist',
  correspondent: 'Correspondent',
  family: 'Family',
  fan_scholar: 'Fan scholar',
  friend: 'Friend',
  fellow_sf_author: 'Fellow SF author',
  mentioned_in_document: 'Mentioned in documents',
  named_person: 'Named person',
  publishing: 'Publishing',
  scholar: 'Scholar',
  sf_community: 'SF community',
  spouse_or_partner: 'Spouse or partner',
  workplace: 'Workplace',
  reading: 'Reading',
  substance_use: 'Substance use',
  drug_use: 'Substance use',
  education: 'Education',
  health: 'Health',
  film_adaptation: 'Film adaptation',
  financial: 'Financial',
  lecture: 'Lecture',
  relationship: 'Relationship',
  residence: 'Residence',
  travel: 'Travel',
  character_inspiration: 'Character inspiration',
  legal: 'Legal',
  crime: 'Legal trouble',
  death: 'Death',
}

const SORT_LABELS: Record<string, string> = {
  association: 'Closest Association',
  evidence: 'Most Evidence',
  name: 'Name',
  first_year: 'First Year',
  biography: 'Biography Links',
  archive: 'Archive Links',
}

function labelFor(value: string): string {
  return CATEGORY_LABELS[value] || value.replace(/_/g, ' ')
}

function evidenceTotal(person: PersonRecord): number {
  return Object.values(person.evidence_counts || {}).reduce<number>((sum, value) => sum + (value || 0), 0)
}

function isHighQuality(person: PersonRecord): boolean {
  if ((person.evidence_counts.biography_events || 0) > 0) return true
  if ((person.evidence_counts.archive_documents || 0) > 0) return true
  if ((person.evidence_counts.scholar_profiles || 0) > 0) return true
  if ((person.relationship_categories || []).some(cat =>
    ['spouse_or_partner', 'family', 'correspondent', 'friend', 'editor', 'publisher', 'agent', 'fellow_sf_author', 'doctor_or_therapist', 'workplace', 'fan_scholar', 'character_inspiration'].includes(cat)
  )) return true
  return (person.association_score || 0) >= 24
}

export default function People() {
  const { data: people, loading } = useData<PersonRecord[]>('people/pkd-knew.json')
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('all')
  const [source, setSource] = useState('all')
  const [sortBy, setSortBy] = useState('association')
  const [quality, setQuality] = useState<QualityMode>('high')
  const [expandedId, setExpandedId] = useState<string | null>(null)

  const categories = useMemo(() => {
    if (!people) return []
    const counts = new Map<string, number>()
    for (const person of people) {
      for (const cat of person.relationship_categories || []) {
        counts.set(cat, (counts.get(cat) || 0) + 1)
      }
    }
    return Array.from(counts.entries()).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
  }, [people])

  const sources = useMemo(() => {
    if (!people) return []
    const counts = new Map<string, number>()
    for (const person of people) {
      for (const key of Object.keys(person.evidence_counts || {})) {
        counts.set(key, (counts.get(key) || 0) + 1)
      }
    }
    return Array.from(counts.entries()).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
  }, [people])

  const filtered = useMemo(() => {
    if (!people) return []
    const q = search.toLowerCase()
    const result = people.filter(person => {
      if (quality === 'high' && !isHighQuality(person)) return false
      if (category !== 'all' && !(person.relationship_categories || []).includes(category)) return false
      if (source !== 'all' && !person.evidence_counts?.[source]) return false
      if (!q) return true
      return (
        person.name.toLowerCase().includes(q) ||
        (person.card_summary || '').toLowerCase().includes(q) ||
        (person.page_summary || '').toLowerCase().includes(q) ||
        (person.relationship_categories || []).some(cat => cat.toLowerCase().includes(q)) ||
        (person.biography_events || []).some(event => event.event.toLowerCase().includes(q)) ||
        (person.archive_documents || []).some(doc => doc.title.toLowerCase().includes(q))
      )
    })

    return [...result].sort((a, b) => {
      if (sortBy === 'association') return (b.association_score || 0) - (a.association_score || 0) || a.name.localeCompare(b.name)
      if (sortBy === 'name') return a.name.localeCompare(b.name)
      if (sortBy === 'first_year') return (a.first_year || 9999) - (b.first_year || 9999)
      if (sortBy === 'biography') return (b.evidence_counts.biography_events || 0) - (a.evidence_counts.biography_events || 0)
      if (sortBy === 'archive') return (b.evidence_counts.archive_documents || 0) - (a.evidence_counts.archive_documents || 0)
      return evidenceTotal(b) - evidenceTotal(a) || a.name.localeCompare(b.name)
    })
  }, [people, search, category, source, sortBy, quality])

  if (loading) return <div className="loading">Loading people...</div>

  return (
    <>
      <div className="page-header">
        <h1>People PKD Knew</h1>
        <p>
          {people?.length} people and candidate people drawn from biography events, archive documents,
          scholar profiles, and indexed names ({filtered.length} shown).
        </p>
      </div>

      <div className="sidebar-layout">
        <div className="sidebar">
          <h3>Quality</h3>
          <ul>
            <li>
              <a href="#" className={quality === 'high' ? 'active' : ''} onClick={e => { e.preventDefault(); setQuality('high') }}>
                Encyclopedia grade
              </a>
            </li>
            <li>
              <a href="#" className={quality === 'all' ? 'active' : ''} onClick={e => { e.preventDefault(); setQuality('all') }}>
                All candidates
              </a>
            </li>
          </ul>

          <h3>Relationship</h3>
          <ul>
            <li>
              <a href="#" className={category === 'all' ? 'active' : ''} onClick={e => { e.preventDefault(); setCategory('all') }}>
                All ({people?.length || 0})
              </a>
            </li>
            {categories.map(([cat, count]) => (
              <li key={cat}>
                <a href="#" className={category === cat ? 'active' : ''} onClick={e => { e.preventDefault(); setCategory(cat) }}>
                  {labelFor(cat)}
                  <span style={{ float: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>{count}</span>
                </a>
              </li>
            ))}
          </ul>

          <h3 style={{ marginTop: '1.5rem' }}>Evidence Source</h3>
          <ul>
            <li>
              <a href="#" className={source === 'all' ? 'active' : ''} onClick={e => { e.preventDefault(); setSource('all') }}>
                All Sources
              </a>
            </li>
            {sources.map(([src, count]) => (
              <li key={src}>
                <a href="#" className={source === src ? 'active' : ''} onClick={e => { e.preventDefault(); setSource(src) }}>
                  {labelFor(src)}
                  <span style={{ float: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>{count}</span>
                </a>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <div className="toolbar-row">
            <input
              className="search-input"
              type="text"
              placeholder="Search people, events, documents..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <select className="filter-select" value={sortBy} onChange={e => setSortBy(e.target.value)} aria-label="Sort people">
              {Object.entries(SORT_LABELS).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </div>

          <div className="card-grid">
            {filtered.map(person => {
              const isExpanded = expandedId === person.person_id
              return (
                <div key={person.person_id} className="card" style={{ cursor: 'pointer' }} onClick={() => setExpandedId(isExpanded ? null : person.person_id)}>
                  <h3>{person.name}</h3>
                  <div className="card-meta">
                  {(person.relationship_categories || []).slice(0, 3).map(cat => (
                    <span key={cat} className="badge badge-category">{labelFor(cat)}</span>
                  ))}
                  <span>{evidenceTotal(person)} links</span>
                  <span>score {person.association_score}</span>
                  {person.first_year && <span>{person.first_year}{person.last_year && person.last_year !== person.first_year ? `-${person.last_year}` : ''}</span>}
                  <span className="confidence-label">{person.review_state}</span>
                </div>
                  <p style={{ marginTop: '0.5rem' }}>
                    <Link to={`/people/${person.slug}`} onClick={e => e.stopPropagation()}>
                      {person.card_summary}
                    </Link>
                  </p>

                  {isExpanded && (
                    <div style={{ marginTop: '1rem' }}>
                      <p>{person.page_summary}</p>

                      {person.biography_events.length > 0 && (
                        <div className="relation-block">
                          <h4>Biography Events</h4>
                          <ul>
                            {person.biography_events.map(event => (
                              <li key={event.id}>
                                <strong>{event.date}:</strong> {event.event}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {person.archive_documents.length > 0 && (
                        <div className="relation-block">
                          <h4>Archive Documents</h4>
                          <ul>
                            {person.archive_documents.map(doc => (
                              <li key={doc.doc_id}>
                                <Link to={`/archive/${doc.slug}`} onClick={e => e.stopPropagation()}>{doc.title}</Link>
                                {doc.date_display && doc.date_display !== 'Unknown' && <span className="backlinks-date"> {doc.date_display}</span>}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {person.scholar_profiles.length > 0 && (
                        <div className="relation-block">
                          <h4>Scholar/Fan-Scholar Profiles</h4>
                          <ul>
                            {person.scholar_profiles.map(profile => (
                              <li key={profile.scholar_id}>
                                <Link to={`/scholars#${profile.scholar_id}`} onClick={e => e.stopPropagation()}>{profile.name}</Link>
                                <span className="backlinks-date"> {profile.role}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {person.name_entry && (
                        <div className="relation-block">
                          <h4>Indexed Name Entry</h4>
                          <p>
                            <Link to={`/names/${person.name_entry.slug}`} onClick={e => e.stopPropagation()}>
                              {person.name}
                            </Link>
                            {person.name_entry.mention_count > 0 && ` - ${person.name_entry.mention_count} Exegesis mention(s)`}
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )
            })}
          </div>

          {filtered.length === 0 && (
            <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
              No people match the current filters.
            </p>
          )}
        </div>
      </div>
    </>
  )
}

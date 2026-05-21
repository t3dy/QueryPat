import { useState, useMemo } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface TopicSummary {
  topic_id: string
  canonical_name: string
  slug: string
  status: string
  priority: number
  card_description: string
  passage_count: number
  evidence_count: number
  contradiction_count: number
  first_appearance: string
  lane_distribution: { A: number; B: number; C: number }
  related_topics: string[]
}

interface StudyData {
  study_id: string
  study_label: string
  study_description: string
  featured_sections?: FeaturedSection[]
  topics: TopicSummary[]
}

interface FeaturedSection {
  title: string
  body: string[]
}

function LaneBar({ dist }: { dist: { A: number; B: number; C: number } }) {
  const total = dist.A + dist.B + dist.C
  if (total === 0) return null
  const pctA = (dist.A / total) * 100
  const pctB = (dist.B / total) * 100
  const pctC = (dist.C / total) * 100
  return (
    <div className="lane-bar" title={`Fiction: ${dist.A}, Exegesis: ${dist.B}, Scholarship: ${dist.C}`}>
      <div className="lane-bar-a" style={{ width: `${pctA}%` }} />
      <div className="lane-bar-b" style={{ width: `${pctB}%` }} />
      <div className="lane-bar-c" style={{ width: `${pctC}%` }} />
    </div>
  )
}

export default function StudyIndex() {
  const { studyId } = useParams<{ studyId: string }>()
  const { data: study, loading } = useData<StudyData>(
    studyId ? `studies/${studyId}/index.json` : null
  )
  const [search, setSearch] = useState('')

  const filtered = useMemo(() => {
    if (!study) return []
    let topics = [...study.topics]
    if (search) {
      const q = search.toLowerCase()
      topics = topics.filter(t =>
        t.canonical_name.toLowerCase().includes(q) ||
        (t.card_description || '').toLowerCase().includes(q)
      )
    }
    topics.sort((a, b) => {
      if (a.priority !== b.priority) return b.priority - a.priority
      return b.passage_count - a.passage_count
    })
    return topics
  }, [study, search])

  if (loading) return <div className="loading">Loading...</div>
  if (!study) return <div className="loading">Study not found.</div>

  return (
    <>
      <div className="page-header">
        <h1>{study.study_label}</h1>
        <p>
          {study.topics.length} topics ({filtered.length} shown)
        </p>
        {studyId === 'ai' && (
          <Link to="/studies/ai/scenes" className="badge badge-category" style={{ marginTop: '0.5rem', display: 'inline-block', textDecoration: 'none' }}>
            AI Scene Summaries &rarr;
          </Link>
        )}
      </div>

      {study.featured_sections && study.featured_sections.length > 0 && (
        <div className="detail-section">
          {study.featured_sections.map(section => (
            <div key={section.title} style={{ marginBottom: '1.5rem' }}>
              <h2>{section.title}</h2>
              {section.body.map((paragraph, index) => (
                <p key={index} style={{ fontSize: '0.95rem', lineHeight: 1.7 }}>
                  {paragraph}
                </p>
              ))}
            </div>
          ))}
        </div>
      )}

      <input
        className="search-input"
        type="text"
        placeholder="Filter topics..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />

      <div className="card-grid">
        {filtered.map(topic => (
          <div key={topic.topic_id} className="card">
            <h3>
              <Link to={`/studies/${studyId}/${topic.slug}`}>{topic.canonical_name}</Link>
            </h3>
            <div className="card-meta">
              <span>{topic.passage_count} passages</span>
              <span className={`badge badge-${topic.status}`}>{topic.status}</span>
              {topic.first_appearance && <span>First: {topic.first_appearance}</span>}
            </div>
            {topic.lane_distribution && (
              <LaneBar dist={topic.lane_distribution} />
            )}
            {topic.card_description && (
              <p style={{ marginTop: '0.5rem' }}>
                {topic.card_description.slice(0, 180)}
                {topic.card_description.length > 180 ? '...' : ''}
              </p>
            )}
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
          No topics match the current filter.
        </p>
      )}
    </>
  )
}

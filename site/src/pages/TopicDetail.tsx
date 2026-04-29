import { Link, useParams } from 'react-router-dom'
import { useData } from '../hooks/useData'
import EvidencePanel from '../components/studies/EvidencePanel'
import ContradictionCard from '../components/studies/ContradictionCard'
import TopicChronology from '../components/studies/TopicChronology'

interface RelatedDoc {
  doc_id: string
  title: string
  doc_type: string
  relevance: string
  passage_count: number
  slug: string
}

interface RelatedTerm {
  term_id: string
  canonical_name: string
  slug: string
  relation_type: string
}

interface RelatedName {
  name_id: string
  display_name: string
  slug: string
  relation_type: string
}

interface RelatedTopic {
  topic_id: string
  canonical_name: string
  slug: string
  study_id: string
}

interface TopicData {
  topic_id: string
  study_id: string
  canonical_name: string
  slug: string
  status: string
  definition: string | null
  pkd_relevance: string | null
  in_the_fiction: string | null
  in_the_exegesis: string | null
  intellectual_background: string | null
  scholarly_debate: string | null
  chronology_summary: string | null
  contradictions_summary: string | null
  related_thinkers: string[] | null
  editorial_notes: string | null
  open_questions: string[] | null
  passage_count: number
  evidence_count: number
  contradiction_count: number
  first_appearance: string
  peak_period_start: string
  peak_period_end: string
  evidence_packets: any[]
  contradictions: any[]
  chronology: any[]
  related_documents: RelatedDoc[]
  related_terms: RelatedTerm[]
  related_names: RelatedName[]
  related_topics: RelatedTopic[]
}

const DOSSIER_SECTIONS: { key: keyof TopicData; label: string }[] = [
  { key: 'definition', label: 'Definition' },
  { key: 'pkd_relevance', label: 'PKD Relevance' },
  { key: 'in_the_fiction', label: 'In the Fiction' },
  { key: 'in_the_exegesis', label: 'In the Exegesis' },
  { key: 'intellectual_background', label: 'Intellectual Background' },
  { key: 'scholarly_debate', label: 'Scholarly Debate' },
  { key: 'chronology_summary', label: 'Chronology Summary' },
  { key: 'contradictions_summary', label: 'Contradictions Summary' },
  { key: 'editorial_notes', label: 'Editorial Notes' },
]

export default function TopicDetail() {
  const { studyId, slug } = useParams<{ studyId: string; slug: string }>()
  const { data: topic, loading } = useData<TopicData>(
    studyId && slug ? `studies/${studyId}/topics/${slug}.json` : null
  )

  if (loading) return <div className="loading">Loading...</div>
  if (!topic) return <div className="loading">Topic not found.</div>

  return (
    <>
      <div className="page-header">
        <h1>{topic.canonical_name}</h1>
        <div className="card-meta">
          <span className={`badge badge-${topic.status}`}>{topic.status}</span>
          <span>{topic.passage_count} passages</span>
          <span>{topic.evidence_count} evidence packets</span>
          {topic.contradiction_count > 0 && (
            <span>{topic.contradiction_count} contradictions</span>
          )}
          {topic.first_appearance && <span>First: {topic.first_appearance}</span>}
          {topic.peak_period_start && (
            <span>Peak: {topic.peak_period_start}&#8211;{topic.peak_period_end}</span>
          )}
        </div>
      </div>

      {/* Dossier prose sections */}
      {DOSSIER_SECTIONS.map(({ key, label }) => {
        const value = topic[key]
        if (!value || typeof value !== 'string') return null
        return (
          <div key={key} className="detail-section">
            <h2>{label}</h2>
            <p style={{ fontSize: '0.92rem', lineHeight: 1.6 }}>{value}</p>
          </div>
        )
      })}

      {/* Related thinkers */}
      {topic.related_thinkers && topic.related_thinkers.length > 0 && (
        <div className="detail-section">
          <h2>Related Thinkers</h2>
          <div className="card-meta" style={{ gap: '0.4rem', flexWrap: 'wrap' }}>
            {topic.related_thinkers.map(t => (
              <span key={t} className="entity-tag">{t}</span>
            ))}
          </div>
        </div>
      )}

      {/* Open questions */}
      {topic.open_questions && topic.open_questions.length > 0 && (
        <div className="detail-section">
          <h2>Open Questions</h2>
          <ul>
            {topic.open_questions.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Evidence */}
      <EvidencePanel packets={topic.evidence_packets} />

      {/* Contradictions */}
      {topic.contradictions && topic.contradictions.length > 0 && (
        <div className="detail-section">
          <h2>Contradictions</h2>
          <div className="contradictions-list">
            {topic.contradictions.map((c: any) => (
              <ContradictionCard key={c.contradiction_id} contradiction={c} />
            ))}
          </div>
        </div>
      )}

      {/* Chronology */}
      <TopicChronology entries={topic.chronology} />

      {/* Related documents */}
      {topic.related_documents && topic.related_documents.length > 0 && (
        <div className="detail-section">
          <h2>Related Documents</h2>
          <ul>
            {topic.related_documents.map(doc => (
              <li key={doc.doc_id}>
                <Link to={`/archive/${doc.slug}`}>{doc.title}</Link>
                <span className="card-meta" style={{ display: 'inline-flex', marginLeft: '0.5rem' }}>
                  <span className="badge badge-category">{doc.doc_type}</span>
                  <span>{doc.passage_count} passages</span>
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Related terms */}
      {topic.related_terms && topic.related_terms.length > 0 && (
        <div className="detail-section">
          <h2>Related Terms</h2>
          <div className="card-meta" style={{ gap: '0.4rem', flexWrap: 'wrap' }}>
            {topic.related_terms.map(term => (
              <Link key={term.term_id} to={`/dictionary/${term.slug}`} className="entity-linked">
                {term.canonical_name}
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Related names */}
      {topic.related_names && topic.related_names.length > 0 && (
        <div className="detail-section">
          <h2>Related Names</h2>
          <div className="card-meta" style={{ gap: '0.4rem', flexWrap: 'wrap' }}>
            {topic.related_names.map(name => (
              <Link key={name.name_id} to={`/names/${name.slug}`} className="entity-linked">
                {name.display_name}
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Related topics */}
      {topic.related_topics && topic.related_topics.length > 0 && (
        <div className="detail-section">
          <h2>Related Topics</h2>
          <div className="card-meta" style={{ gap: '0.4rem', flexWrap: 'wrap' }}>
            {topic.related_topics.map(rt => (
              <Link
                key={rt.topic_id}
                to={`/studies/${rt.study_id}/${rt.slug}`}
                className="entity-linked"
              >
                {rt.canonical_name}
              </Link>
            ))}
          </div>
        </div>
      )}
    </>
  )
}

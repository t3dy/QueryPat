import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface StudySummary {
  study_id: string
  study_label: string
  study_description: string
  topic_count: number
  published_count: number
  total_passages: number
  total_evidence_packets: number
  total_contradictions: number
}

export default function StudiesIndex() {
  const { data: studies, loading } = useData<StudySummary[]>('studies/index.json')

  if (loading) return <div className="loading">Loading...</div>

  return (
    <>
      <div className="page-header">
        <h1>Studies</h1>
        <p>Thematic dossiers across Philip K. Dick's fiction, exegesis, and scholarship</p>
      </div>

      <div className="card-grid">
        {studies?.map(study => (
          <div key={study.study_id} className="card study-card">
            <h3>
              <Link to={`/studies/${study.study_id}`}>{study.study_label}</Link>
            </h3>
            <p style={{ marginTop: '0.4rem' }}>
              {study.study_description.slice(0, 200)}
              {study.study_description.length > 200 ? '...' : ''}
            </p>
            <div className="stats-grid" style={{ marginTop: '1rem', marginBottom: 0 }}>
              <div className="stat-card">
                <div className="stat-value">{study.topic_count}</div>
                <div className="stat-label">Topics</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{study.published_count}</div>
                <div className="stat-label">Published</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{study.total_passages.toLocaleString()}</div>
                <div className="stat-label">Passages</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{study.total_evidence_packets}</div>
                <div className="stat-label">Evidence</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </>
  )
}

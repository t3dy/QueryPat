import { Link } from 'react-router-dom'
import LaneBadge from './LaneBadge'

interface ContradictionPassage {
  passage_id: number
  lane: string
  doc_title: string
  passage_text: string
  source_mode: string
  seg_id?: string | null
  citation?: string | null
}

interface ContradictionData {
  contradiction_id: number
  summary: string
  explanation: string
  contradiction_type: string
  passage_a: ContradictionPassage
  passage_b: ContradictionPassage
}

interface ContradictionCardProps {
  contradiction: ContradictionData
}

export default function ContradictionCard({ contradiction }: ContradictionCardProps) {
  const typeLabel = contradiction.contradiction_type.replace(/_/g, ' ')

  return (
    <div className="contradiction-card card">
      <div className="card-meta" style={{ marginBottom: '0.5rem' }}>
        <span className="badge badge-category">{typeLabel}</span>
      </div>
      <p className="contradiction-summary">{contradiction.summary}</p>
      <div className="contradiction-sides">
        <div className="contradiction-side">
          <div className="card-meta" style={{ marginBottom: '0.3rem' }}>
            <LaneBadge lane={contradiction.passage_a.lane} />
            <span style={{ fontWeight: 600 }}>
              {contradiction.passage_a.citation || contradiction.passage_a.doc_title}
            </span>
            {contradiction.passage_a.seg_id && (
              <Link to={`/segments/${contradiction.passage_a.seg_id}`}>Read the entry &rarr;</Link>
            )}
          </div>
          <div className="evidence-excerpt">
            {contradiction.passage_a.passage_text.slice(0, 200)}
            {contradiction.passage_a.passage_text.length > 200 ? '...' : ''}
          </div>
        </div>
        <div className="contradiction-vs">vs.</div>
        <div className="contradiction-side">
          <div className="card-meta" style={{ marginBottom: '0.3rem' }}>
            <LaneBadge lane={contradiction.passage_b.lane} />
            <span style={{ fontWeight: 600 }}>
              {contradiction.passage_b.citation || contradiction.passage_b.doc_title}
            </span>
            {contradiction.passage_b.seg_id && (
              <Link to={`/segments/${contradiction.passage_b.seg_id}`}>Read the entry &rarr;</Link>
            )}
          </div>
          <div className="evidence-excerpt">
            {contradiction.passage_b.passage_text.slice(0, 200)}
            {contradiction.passage_b.passage_text.length > 200 ? '...' : ''}
          </div>
        </div>
      </div>
      {contradiction.explanation && (
        <p style={{ marginTop: '0.75rem', fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
          {contradiction.explanation}
        </p>
      )}
    </div>
  )
}

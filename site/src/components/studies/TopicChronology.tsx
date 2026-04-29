import { Link } from 'react-router-dom'

interface ChronologyEntry {
  year: string
  event_type: string
  summary: string
  doc_id: string
  doc_title: string
}

interface TopicChronologyProps {
  entries: ChronologyEntry[]
}

export default function TopicChronology({ entries }: TopicChronologyProps) {
  if (!entries || entries.length === 0) return null

  return (
    <div className="detail-section">
      <h2>Chronology</h2>
      <div className="chronology-list">
        {entries.map((entry, i) => (
          <div key={i} className="chronology-entry">
            <span className="chronology-year">{entry.year}</span>
            <span className="chronology-doc">
              {entry.doc_id ? (
                <Link to={`/archive/${entry.doc_title?.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')}`}>
                  {entry.doc_title}
                </Link>
              ) : (
                entry.doc_title
              )}
            </span>
            <span className="badge badge-category">{entry.event_type}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

import { Link } from 'react-router-dom'

interface ChronologyEntry {
  year: string
  date?: string | null
  event_type: string
  summary?: string
  doc_id: string
  doc_title: string
  doc_slug?: string | null
}

/** Document types that have their own page under /archive. */
const ARCHIVE_TYPES = new Set([
  'archive_pdf', 'scholarship', 'letter', 'interview', 'novel', 'biography', 'other',
])

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
            <span className="chronology-year">{entry.date || entry.year}</span>
            <span className="chronology-doc">
              {entry.doc_slug && ARCHIVE_TYPES.has(entry.event_type) ? (
                <Link to={`/archive/${entry.doc_slug}`}>{entry.doc_title}</Link>
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

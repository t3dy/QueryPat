import { Link } from 'react-router-dom'
import { useBookmarks } from '../hooks/useBookmarks'

interface Bookmark {
  entityType: string
  entityId: string
  title: string
  addedAt: string
}

const TYPE_LABELS: Record<string, string> = {
  term: 'Dictionary Terms',
  segment: 'Exegesis Summaries',
  name: 'Names',
  archive: 'Archive Documents',
  biography: 'Biography Events',
}

const TYPE_ORDER = ['term', 'segment', 'name', 'archive', 'biography']

function getLink(b: Bookmark): string {
  switch (b.entityType) {
    case 'term': return `/dictionary/${b.entityId}`
    case 'segment': return `/segments/${b.entityId}`
    case 'name': return `/names/${b.entityId}`
    case 'archive': return `/archive/${b.entityId}`
    case 'biography': return `/biography`
    default: return '/'
  }
}

export default function Bookmarks() {
  const { bookmarks, toggle } = useBookmarks()

  const grouped = TYPE_ORDER.map(type => ({
    type,
    label: TYPE_LABELS[type] || type,
    items: bookmarks.filter(b => b.entityType === type),
  })).filter(g => g.items.length > 0)

  return (
    <>
      <div className="page-header">
        <h1>My Bookmarks</h1>
        <p>Your saved items across the Knowledge Portal ({bookmarks.length} bookmarked)</p>
      </div>

      {bookmarks.length === 0 && (
        <p style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: '2rem 0' }}>
          No bookmarks yet. Click the star icon on any entity page to save it here.
        </p>
      )}

      {grouped.map(g => (
        <div key={g.type} className="detail-section">
          <h2>{g.label} ({g.items.length})</h2>
          {g.items.map(b => (
            <div key={`${b.entityType}-${b.entityId}`} className="card" style={{ marginBottom: '0.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <Link to={getLink(b)} style={{ fontWeight: 600 }}>{b.title}</Link>
                <div className="card-meta">
                  <span>{new Date(b.addedAt).toLocaleDateString()}</span>
                </div>
              </div>
              <button
                className="bookmark-btn bookmark-active"
                onClick={() => toggle(b.entityType, b.entityId, b.title)}
                title="Remove bookmark"
              >
                &#9733;
              </button>
            </div>
          ))}
        </div>
      ))}
    </>
  )
}

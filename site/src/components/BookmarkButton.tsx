import { useBookmarks } from '../hooks/useBookmarks'

interface BookmarkButtonProps {
  entityType: string
  entityId: string
  title: string
}

export default function BookmarkButton({ entityType, entityId, title }: BookmarkButtonProps) {
  const { toggle, isBookmarked } = useBookmarks()
  const active = isBookmarked(entityType, entityId)

  return (
    <button
      className={`bookmark-btn ${active ? 'bookmark-active' : ''}`}
      onClick={() => toggle(entityType, entityId, title)}
      title={active ? 'Remove bookmark' : 'Add bookmark'}
      aria-label={active ? 'Remove bookmark' : 'Add bookmark'}
    >
      {active ? '\u2605' : '\u2606'}
    </button>
  )
}

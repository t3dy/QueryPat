import { Link, useLocation } from 'react-router-dom'
import { formatSegmentTitle } from '../utils/formatTitle'

const SECTION_LABELS: Record<string, string> = {
  timeline: 'Timeline',
  dictionary: 'Dictionary',
  archive: 'Archive',
  segments: 'Exegesis',
  search: 'Search',
  biography: 'Biography',
  scholars: 'Scholars',
  names: 'Names',
  analytics: 'Analytics',
  tag: 'Tag',
  bookmarks: 'Bookmarks',
}

export default function Breadcrumbs() {
  const { pathname } = useLocation()
  const parts = pathname.split('/').filter(Boolean)

  if (parts.length === 0) return null

  const crumbs: { label: string; to: string }[] = [
    { label: 'Home', to: '/' },
  ]

  let path = ''
  for (let i = 0; i < parts.length; i++) {
    path += '/' + parts[i]
    const part = parts[i]

    if (i === 0) {
      crumbs.push({ label: SECTION_LABELS[part] || part, to: path })
    } else if (parts[0] === 'segments') {
      crumbs.push({ label: formatSegmentTitle(null, part), to: path })
    } else if (parts[0] === 'timeline') {
      crumbs.push({ label: part, to: path })
    } else {
      // Detail page slug — prettify
      const pretty = decodeURIComponent(part).replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
      crumbs.push({ label: pretty, to: path })
    }
  }

  return (
    <>
      {/* Desktop breadcrumbs */}
      <nav className="breadcrumbs breadcrumbs-desktop" aria-label="Breadcrumb">
        {crumbs.map((c, i) => (
          <span key={c.to}>
            {i > 0 && <span className="breadcrumb-sep">&rsaquo;</span>}
            {i === crumbs.length - 1 ? (
              <span className="breadcrumb-current">{c.label}</span>
            ) : (
              <Link to={c.to} className="breadcrumb-link">{c.label}</Link>
            )}
          </span>
        ))}
      </nav>
      {/* Mobile back link */}
      {crumbs.length >= 2 && (
        <nav className="breadcrumbs breadcrumbs-mobile" aria-label="Breadcrumb">
          <Link to={crumbs[crumbs.length - 2].to} className="breadcrumb-link">
            &lsaquo; {crumbs[crumbs.length - 2].label}
          </Link>
        </nav>
      )}
    </>
  )
}

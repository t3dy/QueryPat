import { Link } from 'react-router-dom'

interface ExploreItem {
  label: string
  to: string
}

interface ExploreGroup {
  section: string
  items: ExploreItem[]
  totalCount?: number
  seeAllTo?: string
}

interface ExploreFooterProps {
  groups: ExploreGroup[]
}

export default function ExploreFooter({ groups }: ExploreFooterProps) {
  const nonEmpty = groups.filter(g => g.items.length > 0)
  if (nonEmpty.length === 0) return null

  return (
    <div className="explore-footer">
      <h2 className="explore-footer-title">Explore Further</h2>
      <div className="explore-footer-grid">
        {nonEmpty.map(g => (
          <div key={g.section} className="explore-footer-group">
            <h3 className="explore-footer-section">
              {g.section}
              {g.totalCount && g.totalCount > g.items.length && (
                <span className="explore-footer-count"> ({g.totalCount} total)</span>
              )}
            </h3>
            <ul>
              {g.items.slice(0, 3).map((item, i) => (
                <li key={i}>
                  <Link to={item.to}>{item.label}</Link>
                </li>
              ))}
            </ul>
            {g.seeAllTo && g.totalCount && g.totalCount > 3 && (
              <Link to={g.seeAllTo} className="explore-footer-see-all">
                See all {g.totalCount} &rarr;
              </Link>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

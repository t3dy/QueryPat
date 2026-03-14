import { useState } from 'react'
import { Link } from 'react-router-dom'

interface BacklinkItem {
  label: string
  to: string
  date?: string
}

interface BacklinkGroup {
  type: string
  items: BacklinkItem[]
}

interface BacklinksPanelProps {
  groups: BacklinkGroup[]
}

const INITIAL_SHOW = 5

export default function BacklinksPanel({ groups }: BacklinksPanelProps) {
  const nonEmpty = groups.filter(g => g.items.length > 0)
  if (nonEmpty.length === 0) return null

  return (
    <div className="backlinks-panel">
      <h2 className="backlinks-title">What Links Here</h2>
      {nonEmpty.map(g => (
        <BacklinkGroupSection key={g.type} group={g} />
      ))}
    </div>
  )
}

function BacklinkGroupSection({ group }: { group: BacklinkGroup }) {
  const [expanded, setExpanded] = useState(false)
  const shown = expanded ? group.items : group.items.slice(0, INITIAL_SHOW)

  return (
    <div className="backlinks-group">
      <h3 className="backlinks-group-title">
        {group.type}
        <span className="backlinks-count">{group.items.length}</span>
      </h3>
      <ul>
        {shown.map((item, i) => (
          <li key={i}>
            <Link to={item.to}>{item.label}</Link>
            {item.date && <span className="backlinks-date">{item.date}</span>}
          </li>
        ))}
      </ul>
      {group.items.length > INITIAL_SHOW && (
        <button
          className="backlinks-toggle"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded
            ? 'Show fewer'
            : `Show all ${group.items.length}`
          }
        </button>
      )}
    </div>
  )
}

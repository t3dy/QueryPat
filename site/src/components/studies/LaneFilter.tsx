import { useState } from 'react'

interface LaneFilterProps {
  onChange: (activeLanes: string[]) => void
  /** Lanes actually present in the data; others are hidden. Defaults to A/B/C. */
  lanes?: string[]
}

const LANES = [
  { key: 'A', label: 'Fiction', className: 'lane-toggle lane-toggle-a' },
  { key: 'B', label: 'Exegesis', className: 'lane-toggle lane-toggle-b' },
  { key: 'C', label: 'Scholarship', className: 'lane-toggle lane-toggle-c' },
  { key: 'D', label: 'Biography', className: 'lane-toggle lane-toggle-d' },
  { key: 'E', label: 'Letters', className: 'lane-toggle lane-toggle-e' },
]

const DEFAULT_LANES = ['A', 'B', 'C']

export default function LaneFilter({ onChange, lanes }: LaneFilterProps) {
  const available = lanes && lanes.length > 0 ? lanes : DEFAULT_LANES
  const [active, setActive] = useState<Set<string>>(new Set(available))

  function toggle(lane: string) {
    setActive(prev => {
      const next = new Set(prev)
      if (next.has(lane)) {
        if (next.size > 1) next.delete(lane)
      } else {
        next.add(lane)
      }
      onChange(Array.from(next))
      return next
    })
  }

  return (
    <div className="lane-filter">
      {LANES.filter(l => available.includes(l.key)).map(l => (
        <button
          key={l.key}
          className={`${l.className}${active.has(l.key) ? ' active' : ''}`}
          onClick={() => toggle(l.key)}
        >
          {l.label}
        </button>
      ))}
    </div>
  )
}

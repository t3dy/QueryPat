import { useState } from 'react'

interface LaneFilterProps {
  onChange: (activeLanes: string[]) => void
}

const LANES = [
  { key: 'A', label: 'Fiction', className: 'lane-toggle lane-toggle-a' },
  { key: 'B', label: 'Exegesis', className: 'lane-toggle lane-toggle-b' },
  { key: 'C', label: 'Scholarship', className: 'lane-toggle lane-toggle-c' },
]

export default function LaneFilter({ onChange }: LaneFilterProps) {
  const [active, setActive] = useState<Set<string>>(new Set(['A', 'B', 'C']))

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
      {LANES.map(l => (
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

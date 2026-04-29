const LANE_CONFIG: Record<string, { label: string; className: string }> = {
  A: { label: 'Fiction', className: 'lane-badge lane-a' },
  B: { label: 'Exegesis', className: 'lane-badge lane-b' },
  C: { label: 'Scholarship', className: 'lane-badge lane-c' },
}

interface LaneBadgeProps {
  lane: string
}

export default function LaneBadge({ lane }: LaneBadgeProps) {
  const config = LANE_CONFIG[lane]
  if (!config) return null
  return <span className={config.className}>{config.label}</span>
}

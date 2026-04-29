import { Link } from 'react-router-dom'

interface Participant {
  label: string
  role: string
  name_id: string | null
  name_slug: string | null
}

const ROLE_CONFIG: Record<string, { label: string; className: string }> = {
  human:      { label: 'Human',      className: 'role-badge role-human' },
  android:    { label: 'Android',    className: 'role-badge role-android' },
  robot:      { label: 'Robot',      className: 'role-badge role-robot' },
  ai:         { label: 'AI',         className: 'role-badge role-ai' },
  simulation: { label: 'Simulation', className: 'role-badge role-simulation' },
  ambiguous:  { label: 'Ambiguous',  className: 'role-badge role-ambiguous' },
}

interface ParticipantListProps {
  participants: Participant[]
}

export default function ParticipantList({ participants }: ParticipantListProps) {
  if (!participants || participants.length === 0) return null

  return (
    <div className="participant-list">
      {participants.map((p) => {
        const role = ROLE_CONFIG[p.role] || { label: p.role, className: 'role-badge' }
        return (
          <div key={p.label} className="participant-item">
            {p.name_slug ? (
              <Link to={`/names/${p.name_slug}`} className="entity-linked">
                {p.label}
              </Link>
            ) : (
              <span>{p.label}</span>
            )}
            <span className={role.className}>{role.label}</span>
          </div>
        )
      })}
    </div>
  )
}

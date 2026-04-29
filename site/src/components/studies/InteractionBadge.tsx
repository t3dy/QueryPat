const INTERACTION_CONFIG: Record<string, { label: string; className: string }> = {
  empathy_testing:         { label: 'Empathy Testing',      className: 'interaction-badge interaction-empathy' },
  interrogation:           { label: 'Interrogation',        className: 'interaction-badge interaction-interrogation' },
  deception:               { label: 'Deception',            className: 'interaction-badge interaction-deception' },
  empathy_failure:         { label: 'Empathy Failure',      className: 'interaction-badge interaction-empathy' },
  bureaucratic_enforcement:{ label: 'Bureaucratic',         className: 'interaction-badge interaction-bureaucratic' },
  labor_replacement:       { label: 'Labor Replacement',    className: 'interaction-badge interaction-labor' },
  therapeutic_exchange:     { label: 'Therapeutic',          className: 'interaction-badge interaction-therapeutic' },
  romantic_ambiguity:      { label: 'Romantic Ambiguity',   className: 'interaction-badge interaction-romantic' },
  identity_uncertainty:    { label: 'Identity Uncertainty', className: 'interaction-badge interaction-identity' },
  suspicion:               { label: 'Suspicion',            className: 'interaction-badge interaction-suspicion' },
  surveillance:            { label: 'Surveillance',         className: 'interaction-badge interaction-surveillance' },
  memory_manipulation:     { label: 'Memory Manipulation',  className: 'interaction-badge interaction-memory' },
  revolt:                  { label: 'Revolt',               className: 'interaction-badge interaction-revolt' },
  companionship:           { label: 'Companionship',        className: 'interaction-badge interaction-companionship' },
  creation:                { label: 'Creation',             className: 'interaction-badge interaction-creation' },
  destruction:             { label: 'Destruction',          className: 'interaction-badge interaction-destruction' },
}

interface InteractionBadgeProps {
  type: string
}

export default function InteractionBadge({ type }: InteractionBadgeProps) {
  const config = INTERACTION_CONFIG[type]
  if (!config) return <span className="interaction-badge">{type.replace(/_/g, ' ')}</span>
  return <span className={config.className}>{config.label}</span>
}

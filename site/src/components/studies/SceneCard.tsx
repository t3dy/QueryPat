import { Link } from 'react-router-dom'
import InteractionBadge from './InteractionBadge'

interface SceneSummary {
  scene_id: string
  scene_label: string
  work_title: string
  interaction_type: string
  interaction_type_secondary: string | null
  participant_count: number
  participant_labels: string[]
  short_summary: string
  editorial_status: string
}

interface SceneCardProps {
  scene: SceneSummary
}

export default function SceneCard({ scene }: SceneCardProps) {
  const summaryTruncated = scene.short_summary && scene.short_summary.length > 200
    ? scene.short_summary.slice(0, 200) + '...'
    : scene.short_summary

  return (
    <div className="card">
      <h3>
        <Link to={`/studies/ai/scenes/${scene.scene_id}`}>
          {scene.scene_label}
        </Link>
      </h3>
      <div className="card-meta">
        <span className="scene-work-title">{scene.work_title}</span>
        <InteractionBadge type={scene.interaction_type} />
        {scene.interaction_type_secondary && (
          <InteractionBadge type={scene.interaction_type_secondary} />
        )}
      </div>
      {scene.participant_labels && scene.participant_labels.length > 0 && (
        <div className="scene-participants-preview">
          {scene.participant_labels.join(' · ')}
        </div>
      )}
      {summaryTruncated && (
        <p className="card-description">{summaryTruncated}</p>
      )}
    </div>
  )
}

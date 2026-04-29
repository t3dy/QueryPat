import { useParams, Link } from 'react-router-dom'
import { useData } from '../hooks/useData'
import InteractionBadge from '../components/studies/InteractionBadge'
import ParticipantList from '../components/studies/ParticipantList'

interface Participant {
  label: string
  role: string
  name_id: string | null
  name_slug: string | null
}

interface RelatedTopic {
  topic_id: string
  canonical_name: string
  slug: string
  study_id: string
  relevance: string
}

interface SceneData {
  scene_id: string
  scene_label: string
  work_id: string | null
  work_title: string
  doc_id: string | null
  page_start: number | null
  page_end: number | null
  interaction_type: string
  interaction_type_label: string
  interaction_type_secondary: string | null
  interaction_type_secondary_label: string | null
  short_summary: string
  significance: string | null
  source_excerpt: string | null
  participants: Participant[]
  related_topics: RelatedTopic[]
  editorial_status: string
}

export default function SceneDetail() {
  const { sceneId } = useParams<{ sceneId: string }>()
  const { data: scene, loading } = useData<SceneData>(
    sceneId ? `scenes/scenes/${sceneId}.json` : null
  )

  if (loading) return <div className="loading">Loading scene...</div>
  if (!scene) return <div className="loading">Scene not found</div>

  return (
    <div>
      <div className="page-header">
        <Link to="/studies/ai/scenes" className="back-link">&larr; All Scenes</Link>
        <h1>{scene.scene_label}</h1>
        <div className="card-meta">
          <span className="scene-work-title">{scene.work_title}</span>
          {scene.page_start && (
            <span className="scene-pages">
              pp. {scene.page_start}{scene.page_end && scene.page_end !== scene.page_start ? `–${scene.page_end}` : ''}
            </span>
          )}
          <span className={`badge badge-${scene.editorial_status}`}>
            {scene.editorial_status.replace(/-/g, ' ')}
          </span>
        </div>
      </div>

      <div className="detail-section">
        <h2>Interaction Type</h2>
        <div className="interaction-badges">
          <InteractionBadge type={scene.interaction_type} />
          {scene.interaction_type_secondary && (
            <InteractionBadge type={scene.interaction_type_secondary} />
          )}
        </div>
      </div>

      <div className="detail-section">
        <h2>Participants</h2>
        <ParticipantList participants={scene.participants} />
      </div>

      <div className="detail-section">
        <h2>Summary</h2>
        <p>{scene.short_summary}</p>
      </div>

      {scene.source_excerpt && (
        <div className="detail-section">
          <h2>Source Excerpt</h2>
          <blockquote className="scene-excerpt">
            {scene.source_excerpt}
          </blockquote>
          <p className="excerpt-attribution">— {scene.work_title}</p>
        </div>
      )}

      {scene.significance && (
        <div className="detail-section">
          <h2>Significance</h2>
          <p>{scene.significance}</p>
        </div>
      )}

      {scene.related_topics && scene.related_topics.length > 0 && (
        <div className="detail-section">
          <h2>Related AI Topics</h2>
          <div className="entity-tags">
            {scene.related_topics.map(t => (
              <Link
                key={t.topic_id}
                to={`/studies/${t.study_id}/${t.slug}`}
                className="entity-tag"
              >
                {t.canonical_name}
              </Link>
            ))}
          </div>
        </div>
      )}

      {scene.doc_id && (
        <div className="detail-section">
          <h2>Source Document</h2>
          <Link to={`/archive/${scene.doc_id}`} className="entity-linked">
            {scene.work_title}
          </Link>
        </div>
      )}
    </div>
  )
}

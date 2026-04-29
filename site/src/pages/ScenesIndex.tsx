import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'
import SceneCard from '../components/studies/SceneCard'

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

interface InteractionType {
  type_slug: string
  type_label: string
  type_description: string
  scene_count: number
}

interface WorkEntry {
  work_id: string
  work_title: string
  scene_count: number
}

interface ScenesData {
  total_scenes: number
  scenes: SceneSummary[]
  interaction_types: InteractionType[]
  works: WorkEntry[]
}

export default function ScenesIndex() {
  const { data, loading } = useData<ScenesData>('scenes/index.json')
  const [search, setSearch] = useState('')
  const [typeFilter, setTypeFilter] = useState<string | null>(null)
  const [workFilter, setWorkFilter] = useState<string | null>(null)

  const filtered = useMemo(() => {
    if (!data) return []
    let scenes = data.scenes

    if (search) {
      const q = search.toLowerCase()
      scenes = scenes.filter(s =>
        s.scene_label.toLowerCase().includes(q) ||
        s.work_title.toLowerCase().includes(q) ||
        s.participant_labels.some(p => p.toLowerCase().includes(q)) ||
        (s.short_summary && s.short_summary.toLowerCase().includes(q))
      )
    }

    if (typeFilter) {
      scenes = scenes.filter(s =>
        s.interaction_type === typeFilter ||
        s.interaction_type_secondary === typeFilter
      )
    }

    if (workFilter) {
      scenes = scenes.filter(s => s.work_title === workFilter)
    }

    return scenes
  }, [data, search, typeFilter, workFilter])

  if (loading) return <div className="loading">Loading scenes...</div>
  if (!data) return <div className="loading">No scene data found</div>

  return (
    <div>
      <div className="page-header">
        <h1>AI Scene Summaries</h1>
        <p className="page-subtitle">
          {data.total_scenes} scenes from PKD fiction dramatizing human-AI interaction
        </p>
        <Link to="/studies/ai" className="back-link">&larr; AI Topics</Link>
      </div>

      <div className="scene-filters">
        <input
          type="text"
          className="search-input"
          placeholder="Search scenes, works, participants..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />

        <div className="filter-row">
          <select
            className="filter-select"
            value={typeFilter || ''}
            onChange={e => setTypeFilter(e.target.value || null)}
          >
            <option value="">All interaction types</option>
            {data.interaction_types
              .filter(t => t.scene_count > 0)
              .map(t => (
                <option key={t.type_slug} value={t.type_slug}>
                  {t.type_label} ({t.scene_count})
                </option>
              ))}
          </select>

          <select
            className="filter-select"
            value={workFilter || ''}
            onChange={e => setWorkFilter(e.target.value || null)}
          >
            <option value="">All works</option>
            {data.works.map(w => (
              <option key={w.work_id} value={w.work_title}>
                {w.work_title} ({w.scene_count})
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="card-grid">
        {filtered.map(scene => (
          <SceneCard key={scene.scene_id} scene={scene} />
        ))}
      </div>

      {filtered.length === 0 && (
        <p className="no-results">No scenes match your filters.</p>
      )}
    </div>
  )
}

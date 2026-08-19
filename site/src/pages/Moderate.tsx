import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../community/auth-context'
import ContributionCard from '../community/ContributionCard'
import { KIND_LABEL, STATUS_LABEL, fetchRecent, type Contribution, type ContributionStatus } from '../lib/supabase'

const FILTERS: (ContributionStatus | 'all')[] = ['open', 'accepted', 'rejected', 'duplicate', 'all']

export default function Moderate() {
  const { enabled, loading: authLoading, isModerator } = useAuth()
  const [items, setItems] = useState<Contribution[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<ContributionStatus | 'all'>('open')
  const [kind, setKind] = useState<string>('all')

  const load = useCallback(async () => {
    setLoading(true)
    try {
      setItems(await fetchRecent(200, filter === 'all' ? undefined : filter))
    } catch {
      setItems([])
    } finally {
      setLoading(false)
    }
  }, [filter])

  useEffect(() => { if (enabled && isModerator) void load() }, [enabled, isModerator, load])

  if (!enabled) return <p className="cm-muted">Community features are switched off in this build.</p>
  if (authLoading) return <p className="cm-muted">Loading…</p>
  if (!isModerator) {
    return (
      <>
        <div className="page-header"><h1>Moderation</h1></div>
        <p className="cm-muted">
          This queue is for editors. <Link to="/account">Sign in</Link> with a moderator account to use it.
        </p>
      </>
    )
  }

  const shown = kind === 'all' ? items : items.filter(c => c.kind === kind)

  return (
    <>
      <div className="page-header">
        <h1>Moderation queue</h1>
        <p>Accept, decline, or mark duplicates. Accepted work is what the leaderboard weights most.</p>
      </div>

      <div className="cm-filters">
        {FILTERS.map(f => (
          <button
            key={f}
            className={`cm-btn cm-btn-sm ${filter === f ? 'cm-btn-primary' : ''}`}
            onClick={() => setFilter(f)}
          >
            {f === 'all' ? 'All' : STATUS_LABEL[f]}
          </button>
        ))}
        <select value={kind} onChange={e => setKind(e.target.value)}>
          <option value="all">All types</option>
          {Object.entries(KIND_LABEL).map(([k, label]) => <option key={k} value={k}>{label}</option>)}
        </select>
        <button className="cm-btn cm-btn-sm" onClick={() => void load()}>Refresh</button>
      </div>

      {loading && <p className="cm-muted">Loading…</p>}
      {!loading && shown.length === 0 && <p className="cm-muted">Nothing in this view.</p>}

      <div className="cm-list">
        {shown.map(c => (
          <ContributionCard
            key={c.id}
            contribution={c}
            showTarget
            onChange={next => setItems(prev => next ? prev.map(x => x.id === c.id ? next : x) : prev.filter(x => x.id !== c.id))}
          />
        ))}
      </div>
    </>
  )
}

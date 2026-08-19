import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import ContributionCard from '../community/ContributionCard'
import { useVotes } from '../community/useVotes'
import {
  KINDS, STATUS_LABEL, communityEnabled, fetchRecent,
  type Contribution, type ContributionKind, type ContributionStatus,
} from '../lib/supabase'

const STATUSES: (ContributionStatus | 'all')[] = ['all', 'open', 'accepted', 'rejected', 'duplicate']

export default function Community() {
  const [items, setItems] = useState<Contribution[]>([])
  const [loading, setLoading] = useState(communityEnabled)
  const [status, setStatus] = useState<ContributionStatus | 'all'>('all')
  const [kind, setKind] = useState<ContributionKind | 'all'>('all')
  const { counts, mine, handlerFor } = useVotes(items)

  const load = useCallback(async () => {
    if (!communityEnabled) return
    setLoading(true)
    try {
      setItems(await fetchRecent(
        100,
        status === 'all' ? undefined : status,
        kind === 'all' ? undefined : kind,
      ))
    } catch {
      setItems([])
    } finally {
      setLoading(false)
    }
  }, [status, kind])

  useEffect(() => { void load() }, [load])

  if (!communityEnabled) {
    return (
      <>
        <div className="page-header"><h1>Community</h1></div>
        <p className="cm-muted">Community features are switched off in this build.</p>
      </>
    )
  }

  return (
    <>
      <div className="page-header">
        <h1>Community Activity</h1>
        <p>
          Everything readers have flagged, corrected, sourced, or asked about, newest first.
          Follow any item through to its page to reply in context.
        </p>
      </div>

      <div className="card cm-explainer">
        <h3>How contributing works</h3>
        <p>
          Open any page and use <strong>Discuss this page</strong> in the corner — or highlight a
          passage and choose <strong>Comment on selection</strong> to anchor a note to that exact
          sentence. Pick the kind of contribution you're making: a comment, a correction, a
          suggested edit, suggested tags or metadata, or a relevant source.
        </p>
        <p>
          An editor reviews each one and marks it accepted or declined, with a note. Accepted work
          counts most on the <Link to="/leaderboard">leaderboard</Link>; declined and duplicate
          items count for nothing, so there's no advantage to volume alone.
        </p>
      </div>

      <div className="cm-filters">
        {STATUSES.map(s => (
          <button
            key={s}
            className={`cm-btn cm-btn-sm ${status === s ? 'cm-btn-primary' : ''}`}
            onClick={() => setStatus(s)}
          >
            {s === 'all' ? 'All' : STATUS_LABEL[s]}
          </button>
        ))}
        <select value={kind} onChange={e => setKind(e.target.value as ContributionKind | 'all')}>
          <option value="all">All types</option>
          {KINDS.map(k => <option key={k.value} value={k.value}>{k.label}</option>)}
        </select>
      </div>

      {loading && <p className="cm-muted">Loading…</p>}
      {!loading && items.length === 0 && (
        <p className="cm-muted">Nothing matches this view yet.</p>
      )}

      <div className="cm-list">
        {items.map(c => (
          <ContributionCard
            key={c.id}
            contribution={c}
            showTarget
            linkToThread
            voteCount={counts.get(c.id) ?? 0}
            voted={mine.has(c.id)}
            onToggleVote={handlerFor(c)}
            onChange={next => setItems(prev => next
              ? prev.map(x => (x.id === c.id ? next : x))
              : prev.filter(x => x.id !== c.id))}
          />
        ))}
      </div>
    </>
  )
}

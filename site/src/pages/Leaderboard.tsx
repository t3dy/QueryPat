import { useEffect, useState } from 'react'
import { fetchLeaderboard, communityEnabled, type LeaderboardRow } from '../lib/supabase'
import { timeAgo } from '../community/util'

type SortKey = 'score' | 'edits' | 'accepted' | 'total' | 'upvotes'

const COLUMNS: { key: SortKey; label: string; title: string }[] = [
  { key: 'score', label: 'Score', title: 'Accepted work ×5, open suggestions ×2, plus one per contribution and upvote' },
  { key: 'edits', label: 'Edits', title: 'Corrections, suggested edits, metadata, and sources' },
  { key: 'accepted', label: 'Accepted', title: 'Contributions an editor has marked accepted' },
  { key: 'total', label: 'Total', title: 'All contributions including plain comments' },
  { key: 'upvotes', label: 'Helpful', title: 'Upvotes received from other readers' },
]

export default function Leaderboard() {
  const [rows, setRows] = useState<LeaderboardRow[]>([])
  const [loading, setLoading] = useState(communityEnabled)
  const [sort, setSort] = useState<SortKey>('score')

  useEffect(() => {
    if (!communityEnabled) return
    fetchLeaderboard().then(setRows).catch(() => setRows([])).finally(() => setLoading(false))
  }, [])

  if (!communityEnabled) {
    return (
      <>
        <div className="page-header"><h1>Leaderboard</h1></div>
        <p className="cm-muted">Community features are switched off in this build.</p>
      </>
    )
  }

  const ranked = [...rows].filter(r => r.total > 0).sort((a, b) => b[sort] - a[sort])

  return (
    <>
      <div className="page-header">
        <h1>Contributor Leaderboard</h1>
        <p>Everyone who has helped correct, source, and sharpen the archive.</p>
      </div>

      {loading && <p className="cm-muted">Loading…</p>}
      {!loading && ranked.length === 0 && <p className="cm-muted">No contributions yet — be the first.</p>}

      {ranked.length > 0 && (
        <div className="cm-table-wrap">
          <table className="cm-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Contributor</th>
                {COLUMNS.map(c => (
                  <th key={c.key} title={c.title}>
                    <button
                      className={`cm-link-btn ${sort === c.key ? 'cm-voted' : ''}`}
                      onClick={() => setSort(c.key)}
                    >
                      {c.label}
                    </button>
                  </th>
                ))}
                <th>Last seen</th>
              </tr>
            </thead>
            <tbody>
              {ranked.map((r, i) => (
                <tr key={r.user_id}>
                  <td className="cm-rank">{i + 1}</td>
                  <td>
                    <strong>{r.display_name || r.username}</strong>
                    <span className="cm-muted"> @{r.username}</span>
                    {r.role !== 'member' && <span className="badge badge-accepted" style={{ marginLeft: '0.4rem' }}>{r.role}</span>}
                  </td>
                  {COLUMNS.map(c => <td key={c.key}>{r[c.key]}</td>)}
                  <td className="cm-muted">{r.last_contribution_at ? timeAgo(r.last_contribution_at) : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  )
}

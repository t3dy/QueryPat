import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../community/auth-context'
import { timeAgo } from '../community/util'
import { fetchLeaderboard, communityEnabled, type LeaderboardRow } from '../lib/supabase'

type SortKey = 'score' | 'edits' | 'accepted' | 'total' | 'replies' | 'pages' | 'upvotes'

const COLUMNS: { key: SortKey; label: string; title: string }[] = [
  { key: 'score', label: 'Score', title: 'Accepted work ×5, live suggestions ×3, comments and replies ×1, plus one per upvote received. Declined and duplicate work counts nothing.' },
  { key: 'edits', label: 'Edits', title: 'Corrections, suggested edits, metadata, and sources' },
  { key: 'accepted', label: 'Accepted', title: 'Contributions an editor has accepted' },
  { key: 'total', label: 'Total', title: 'Everything filed, including comments and replies' },
  { key: 'replies', label: 'Replies', title: 'Replies written in other contributors’ threads' },
  { key: 'pages', label: 'Pages', title: 'Distinct pages this person has worked on' },
  { key: 'upvotes', label: 'Helpful', title: 'Upvotes received from other readers' },
]

export default function Leaderboard() {
  const { profile } = useAuth()
  const [rows, setRows] = useState<LeaderboardRow[]>([])
  const [loading, setLoading] = useState(communityEnabled)
  const [error, setError] = useState(false)
  const [sort, setSort] = useState<SortKey>('score')

  useEffect(() => {
    if (!communityEnabled) return
    fetchLeaderboard()
      .then(setRows)
      .catch(() => setError(true))
      .finally(() => setLoading(false))
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
  const myIndex = profile ? ranked.findIndex(r => r.user_id === profile.id) : -1

  return (
    <>
      <div className="page-header">
        <h1>Contributor Leaderboard</h1>
        <p>
          Everyone who has helped correct, source, and sharpen the archive. Accepted work counts
          most; declined and duplicate work counts for nothing. See what people are working on in{' '}
          <Link to="/community">Community activity</Link>.
        </p>
      </div>

      {loading && <p className="cm-muted">Loading…</p>}
      {error && <p className="cm-muted">The leaderboard could not be loaded just now.</p>}
      {!loading && !error && ranked.length === 0 && (
        <p className="cm-muted">
          No contributions yet — <Link to="/account">sign in</Link> and be the first.
        </p>
      )}

      {myIndex >= 0 && (
        <p className="cm-standing">
          You’re <strong>#{myIndex + 1}</strong> of {ranked.length} with a score of{' '}
          <strong>{ranked[myIndex].score}</strong>.{' '}
          <Link to="/account">See your contributions →</Link>
        </p>
      )}

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
                      {c.label}{sort === c.key ? ' ↓' : ''}
                    </button>
                  </th>
                ))}
                <th>Last seen</th>
              </tr>
            </thead>
            <tbody>
              {ranked.map((r, i) => (
                <tr key={r.user_id} className={r.user_id === profile?.id ? 'cm-row-me' : ''}>
                  <td className="cm-rank">{i + 1}</td>
                  <td>
                    <Link to={`/u/${r.username}`}><strong>{r.display_name || r.username}</strong></Link>
                    {r.display_name && <span className="cm-muted"> @{r.username}</span>}
                    {r.role !== 'member' && (
                      <span className="badge badge-accepted" style={{ marginLeft: '0.4rem' }}>{r.role}</span>
                    )}
                  </td>
                  {COLUMNS.map(c => <td key={c.key}>{r[c.key]}</td>)}
                  <td className="cm-muted">{r.last_contribution_at ? timeAgo(r.last_contribution_at) : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {ranked.length > 0 && (
        <p className="cm-hint" style={{ marginTop: '1rem' }}>
          Hover a column heading to see how it’s counted. Click one to re-sort.
        </p>
      )}
    </>
  )
}

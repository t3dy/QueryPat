import { Link } from 'react-router-dom'
import type { LeaderboardRow } from '../lib/supabase'
import { plural } from './util'

/**
 * The same numbers the leaderboard ranks by, shown on a contributor's own
 * dashboard and on their public profile — so what someone sees about their
 * work always matches where they sit in the standings.
 */
export default function ContributorStats({
  row, rank, linkToLeaderboard = true,
}: {
  row: LeaderboardRow
  rank: number | null
  linkToLeaderboard?: boolean
}) {
  const tiles: { value: number | string; label: string; title: string }[] = [
    { value: row.score, label: 'Score', title: 'Accepted work ×5, live suggestions ×3, comments and replies ×1, plus one per upvote received' },
    { value: rank ? `#${rank}` : '—', label: 'Rank', title: 'Position on the leaderboard' },
    { value: row.accepted, label: 'Accepted', title: 'Contributions an editor has accepted' },
    { value: row.open_count, label: 'Awaiting review', title: 'Still open' },
    { value: row.edits, label: 'Edits & sources', title: 'Everything except plain comments' },
    { value: row.replies, label: 'Replies', title: 'Replies written in other threads' },
    { value: row.pages, label: 'Pages touched', title: 'Distinct pages contributed to' },
    { value: row.upvotes, label: 'Found helpful', title: 'Upvotes from other readers' },
  ]

  return (
    <>
      <div className="stats-grid">
        {tiles.map(t => (
          <div className="stat-card" key={t.label} title={t.title}>
            <div className="stat-value">{t.value}</div>
            <div className="stat-label">{t.label}</div>
          </div>
        ))}
      </div>
      <div className="cm-breakdown">
        <span title="Corrections">{plural(row.corrections, 'correction')}</span>
        <span title="Suggested edits">{plural(row.suggested_edits, 'suggested edit')}</span>
        <span title="Suggested tags and metadata">{plural(row.tags, 'tag suggestion')}</span>
        <span title="Sources offered">{plural(row.sources, 'source')}</span>
        {linkToLeaderboard && <Link to="/leaderboard">See the full leaderboard →</Link>}
      </div>
    </>
  )
}

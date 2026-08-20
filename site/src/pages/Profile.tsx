import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useAuth } from '../community/auth-context'
import ContributionCard from '../community/ContributionCard'
import ContributorStats from '../community/ContributorStats'
import ProfileDetails from '../community/ProfileDetails'
import { useVotes } from '../community/useVotes'
import { timeAgo } from '../community/util'
import {
  communityEnabled, fetchByAuthor, fetchProfileByUsername, fetchStanding,
  type Contribution, type LeaderboardRow, type Profile as ProfileRow,
} from '../lib/supabase'

export default function Profile() {
  const { username = '' } = useParams()
  const { user } = useAuth()
  const [profile, setProfile] = useState<ProfileRow | null>(null)
  const [standing, setStanding] = useState<{ row: LeaderboardRow; rank: number | null } | null>(null)
  const [items, setItems] = useState<Contribution[]>([])
  const [loading, setLoading] = useState(true)
  const [missing, setMissing] = useState(false)
  const { counts, mine, handlerFor } = useVotes(items)

  useEffect(() => {
    if (!communityEnabled) return
    let live = true
    setLoading(true)
    setMissing(false)
    void (async () => {
      try {
        const p = await fetchProfileByUsername(username)
        if (!live) return
        if (!p) { setMissing(true); return }
        setProfile(p)
        const [s, c] = await Promise.all([fetchStanding(username), fetchByAuthor(p.id)])
        if (!live) return
        setStanding(s)
        setItems(c)
      } catch {
        if (live) setMissing(true)
      } finally {
        if (live) setLoading(false)
      }
    })()
    return () => { live = false }
  }, [username])

  if (!communityEnabled) {
    return (
      <>
        <div className="page-header"><h1>Contributor</h1></div>
        <p className="cm-muted">Community features are switched off in this build.</p>
      </>
    )
  }

  if (loading) return <p className="cm-muted">Loading…</p>

  if (missing || !profile) {
    return (
      <>
        <div className="page-header"><h1>Contributor not found</h1></div>
        <p className="cm-muted">
          No contributor called <strong>@{username}</strong>.{' '}
          <Link to="/leaderboard">Back to the leaderboard</Link>.
        </p>
      </>
    )
  }

  const isMe = user?.id === profile.id

  return (
    <>
      <div className="page-header">
        <h1>{profile.display_name || profile.username}</h1>
        <p>
          @{profile.username}
          {profile.role !== 'member' && (
            <span className="badge badge-accepted" style={{ marginLeft: '0.5rem' }}>{profile.role}</span>
          )}
          <span className="cm-muted"> · contributing since {timeAgo(profile.created_at)}</span>
        </p>
        {profile.bio && <p style={{ marginTop: '0.4rem' }}>{profile.bio}</p>}
        {isMe && (
          <p style={{ marginTop: '0.5rem' }}>
            <Link to="/account">Edit your profile and manage your contributions →</Link>
          </p>
        )}
      </div>

      <ProfileDetails profile={profile} />

      {standing
        ? <ContributorStats row={standing.row} rank={standing.rank} />
        : <p className="cm-muted">No contributions yet.</p>}

      <h2 className="cm-section-title">Contributions</h2>
      {items.length === 0 && <p className="cm-muted">Nothing published yet.</p>}
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

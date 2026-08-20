import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../community/auth-context'
import ContributionCard from '../community/ContributionCard'
import ContributorStats from '../community/ContributorStats'
import ProfileDetails from '../community/ProfileDetails'
import ProfileEditor, { type ProfilePatch } from '../community/ProfileEditor'
import { useVotes } from '../community/useVotes'
import {
  KIND_LABEL, STATUS_LABEL, fetchByAuthor, fetchStanding,
  type Contribution, type ContributionStatus, type LeaderboardRow,
} from '../lib/supabase'

export default function Account() {
  const { enabled, loading, user, profile, signInWithEmail, signInWithOAuth, signOut, saveProfile } = useAuth()

  if (!enabled) {
    return (
      <>
        <div className="page-header"><h1>My Account</h1></div>
        <p className="cm-muted">
          Community features are switched off in this build — no Supabase credentials were configured.
          See <code>USERSNEXTSTEPS.md</code> in the repository for setup.
        </p>
      </>
    )
  }
  if (loading) return <p className="cm-muted">Loading…</p>
  if (!user) return <SignIn onEmail={signInWithEmail} onOAuth={signInWithOAuth} />
  if (!profile) {
    return <ClaimUsername onSave={saveProfile} email={user.email ?? ''} onSignOut={signOut} />
  }
  return <Dashboard onSignOut={signOut} onSave={saveProfile} />
}

// ── Signed out ──────────────────────────────────────────────────

function SignIn({
  onEmail, onOAuth,
}: {
  onEmail: (email: string) => Promise<void>
  onOAuth: (p: 'github' | 'google') => Promise<void>
}) {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setBusy(true); setError(null)
    try { await onEmail(email.trim()); setSent(true) }
    catch (err) { setError(err instanceof Error ? err.message : 'Sign-in failed.') }
    finally { setBusy(false) }
  }

  async function oauth(p: 'github' | 'google') {
    setError(null)
    try { await onOAuth(p) }
    catch (err) { setError(err instanceof Error ? err.message : `${p} sign-in is not enabled.`) }
  }

  return (
    <>
      <div className="page-header">
        <h1>Sign in</h1>
        <p>
          Contributors can leave comments, corrections, suggested edits, metadata, and sources on
          any page. See what others have been working on in{' '}
          <Link to="/community">Community activity</Link>.
        </p>
      </div>

      {sent ? (
        <div className="card cm-narrow">
          <h3>Check your inbox</h3>
          <p>We sent a sign-in link to <strong>{email}</strong>. Open it in this browser to finish signing in.</p>
          <p className="cm-hint" style={{ marginTop: '0.6rem' }}>
            Nothing after a minute or two? Check spam, then{' '}
            <button className="cm-link-btn" onClick={() => setSent(false)}>try another address</button>.
          </p>
        </div>
      ) : (
        <form className="card cm-narrow cm-form" onSubmit={submit}>
          <label className="cm-field">
            <span className="cm-label">Email address</span>
            <input
              type="email" value={email} required autoComplete="email"
              onChange={e => setEmail(e.target.value)} placeholder="you@example.com"
            />
            <span className="cm-hint">No password — we email you a one-time sign-in link.</span>
          </label>
          {error && <p className="cm-error">{error}</p>}
          <div className="cm-form-actions">
            <button className="cm-btn cm-btn-primary" disabled={busy || !email.trim()}>
              {busy ? 'Sending…' : 'Email me a link'}
            </button>
          </div>
          <div className="cm-oauth">
            <span className="cm-hint">Or use an existing account:</span>
            <div className="cm-form-actions">
              <button type="button" className="cm-btn" onClick={() => void oauth('github')}>GitHub</button>
              <button type="button" className="cm-btn" onClick={() => void oauth('google')}>Google</button>
            </div>
            <span className="cm-hint">
              These only work if the provider has been enabled in the project’s Supabase settings.
            </span>
          </div>
        </form>
      )}
    </>
  )
}

// ── Signed in, no profile yet ───────────────────────────────────

function ClaimUsername({
  onSave, email, onSignOut,
}: {
  onSave: (p: { username: string; display_name?: string | null }) => Promise<void>
  email: string
  onSignOut: () => Promise<void>
}) {
  const [username, setUsername] = useState('')
  const [displayName, setDisplayName] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const valid = /^[a-z0-9_]{3,24}$/.test(username)

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setBusy(true); setError(null)
    try { await onSave({ username, display_name: displayName.trim() || null }) }
    catch (err) { setError(err instanceof Error ? err.message : 'Could not save.') }
    finally { setBusy(false) }
  }

  return (
    <>
      <div className="page-header">
        <h1>Choose a username</h1>
        <p>
          Signed in as {email}. Your username is how your contributions are credited, and it becomes
          your public profile at <code>/u/your-name</code>.
        </p>
      </div>
      <form className="card cm-narrow cm-form" onSubmit={submit}>
        <label className="cm-field">
          <span className="cm-label">Username</span>
          <input
            value={username} required autoFocus
            onChange={e => setUsername(e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, ''))}
            placeholder="horselover_fat"
          />
          <span className="cm-hint">
            3–24 characters: lowercase letters, numbers, underscores.
            {username && !valid && ' — not valid yet'}
          </span>
        </label>
        <label className="cm-field">
          <span className="cm-label">Display name (optional)</span>
          <input value={displayName} onChange={e => setDisplayName(e.target.value)} maxLength={60} />
          <span className="cm-hint">Shown instead of your username, if you set one.</span>
        </label>
        {error && <p className="cm-error">{error}</p>}
        <div className="cm-form-actions">
          <button className="cm-btn cm-btn-primary" disabled={busy || !valid}>
            {busy ? 'Saving…' : 'Claim username'}
          </button>
          <button type="button" className="cm-btn" onClick={() => void onSignOut()}>Sign out</button>
        </div>
      </form>
    </>
  )
}

// ── Signed in dashboard ─────────────────────────────────────────

const FILTERS: (ContributionStatus | 'all')[] = ['all', 'open', 'accepted', 'rejected', 'duplicate']

function Dashboard({
  onSignOut, onSave,
}: {
  onSignOut: () => Promise<void>
  onSave: (p: ProfilePatch) => Promise<void>
}) {
  const { profile, isModerator } = useAuth()
  const [items, setItems] = useState<Contribution[]>([])
  const [standing, setStanding] = useState<{ row: LeaderboardRow; rank: number | null } | null>(null)
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<ContributionStatus | 'all'>('all')
  const [editing, setEditing] = useState(false)
  const { counts, mine, handlerFor } = useVotes(items)

  useEffect(() => {
    if (!profile) return
    let live = true
    void (async () => {
      try {
        const [c, s] = await Promise.all([fetchByAuthor(profile.id), fetchStanding(profile.username)])
        if (!live) return
        setItems(c)
        setStanding(s)
      } catch {
        if (live) setItems([])
      } finally {
        if (live) setLoading(false)
      }
    })()
    return () => { live = false }
  }, [profile])

  const shown = filter === 'all' ? items : items.filter(c => c.status === filter)
  const countFor = (f: ContributionStatus | 'all') =>
    f === 'all' ? items.length : items.filter(c => c.status === f).length

  return (
    <>
      <div className="page-header">
        <h1>{profile?.display_name || profile?.username}</h1>
        <p>
          <Link to={`/u/${profile?.username}`}>@{profile?.username}</Link>
          {profile?.role !== 'member' && (
            <span className="badge badge-accepted" style={{ marginLeft: '0.5rem' }}>{profile?.role}</span>
          )}
        </p>
        {profile?.bio && !editing && <p style={{ marginTop: '0.4rem' }}>{profile.bio}</p>}
      </div>

      {!editing && profile && <ProfileDetails profile={profile} />}

      {loading && <p className="cm-muted">Loading…</p>}

      {standing && <ContributorStats row={standing.row} rank={standing.rank} />}
      {!loading && !standing && (
        <p className="cm-muted">
          Nothing yet. Open any page, hit <em>Discuss this page</em>, or highlight a passage to
          anchor a correction to it — everything you file shows up here and on the leaderboard.
        </p>
      )}

      {!editing && profile && !profile.areas?.length && !profile.research_interests?.length && (
        <p className="cm-nudge">
          Your profile is bare. Tell people what you work on — the archive sections you know, your
          research interests, favourite works and themes — and it all becomes links on your public
          page at <Link to={`/u/${profile.username}`}>/u/{profile.username}</Link>.
        </p>
      )}

      <div className="cm-form-actions" style={{ margin: '1rem 0' }}>
        <button className="cm-btn" onClick={() => setEditing(v => !v)}>
          {editing ? 'Cancel' : 'Edit profile'}
        </button>
        <Link className="cm-btn" to="/community">Community activity</Link>
        <Link className="cm-btn" to="/leaderboard">Leaderboard</Link>
        {isModerator && <Link className="cm-btn" to="/moderate">Moderation queue</Link>}
        <button className="cm-btn" onClick={() => void onSignOut()}>Sign out</button>
      </div>

      {editing && profile && (
        <ProfileEditor
          profile={profile}
          onSave={async patch => { await onSave(patch); setEditing(false) }}
          onCancel={() => setEditing(false)}
        />
      )}

      <h2 className="cm-section-title">My contributions</h2>
      <div className="cm-filters">
        {FILTERS.map(f => (
          <button
            key={f}
            className={`cm-btn cm-btn-sm ${filter === f ? 'cm-btn-primary' : ''}`}
            onClick={() => setFilter(f)}
          >
            {f === 'all' ? 'All' : STATUS_LABEL[f]} ({countFor(f)})
          </button>
        ))}
      </div>

      {!loading && shown.length === 0 && (
        <p className="cm-muted">
          {items.length === 0
            ? 'Nothing here yet.'
            : `No ${STATUS_LABEL[filter as ContributionStatus].toLowerCase()} contributions.`}
        </p>
      )}

      <div className="cm-list">
        {shown.map(c => (
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

      {items.length > 0 && (
        <p className="cm-muted" style={{ marginTop: '1rem' }}>
          Types filed: {Object.entries(
            items.reduce<Record<string, number>>((acc, c) => {
              acc[c.kind] = (acc[c.kind] ?? 0) + 1
              return acc
            }, {}),
          ).map(([k, n]) => `${KIND_LABEL[k as keyof typeof KIND_LABEL]} ${n}`).join(' · ')}
        </p>
      )}
    </>
  )
}

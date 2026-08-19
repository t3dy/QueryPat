import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../community/auth-context'
import ContributionCard from '../community/ContributionCard'
import { KIND_LABEL, STATUS_LABEL, fetchMine, type Contribution, type ContributionStatus } from '../lib/supabase'

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
  if (!profile) return <ClaimUsername onSave={saveProfile} email={user.email ?? ''} />
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

  return (
    <>
      <div className="page-header">
        <h1>Sign in</h1>
        <p>Contributors can leave comments, corrections, suggested edits, metadata, and sources on any page.</p>
      </div>

      {sent ? (
        <div className="card cm-narrow">
          <h3>Check your inbox</h3>
          <p>We sent a sign-in link to <strong>{email}</strong>. Open it in this browser to finish signing in.</p>
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
              <button type="button" className="cm-btn" onClick={() => onOAuth('github')}>GitHub</button>
              <button type="button" className="cm-btn" onClick={() => onOAuth('google')}>Google</button>
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
  onSave, email,
}: {
  onSave: (p: { username: string; display_name?: string | null }) => Promise<void>
  email: string
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
        <p>Signed in as {email}. Your username is how your contributions are credited.</p>
      </div>
      <form className="card cm-narrow cm-form" onSubmit={submit}>
        <label className="cm-field">
          <span className="cm-label">Username</span>
          <input
            value={username} required autoFocus
            onChange={e => setUsername(e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, ''))}
            placeholder="horselover_fat"
          />
          <span className="cm-hint">3–24 characters: lowercase letters, numbers, underscores.</span>
        </label>
        <label className="cm-field">
          <span className="cm-label">Display name (optional)</span>
          <input value={displayName} onChange={e => setDisplayName(e.target.value)} maxLength={60} />
        </label>
        {error && <p className="cm-error">{error}</p>}
        <div className="cm-form-actions">
          <button className="cm-btn cm-btn-primary" disabled={busy || !valid}>
            {busy ? 'Saving…' : 'Claim username'}
          </button>
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
  onSave: (p: { display_name?: string | null; bio?: string | null }) => Promise<void>
}) {
  const { profile, isModerator } = useAuth()
  const [items, setItems] = useState<Contribution[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<ContributionStatus | 'all'>('all')
  const [editing, setEditing] = useState(false)
  const [displayName, setDisplayName] = useState(profile?.display_name ?? '')
  const [bio, setBio] = useState(profile?.bio ?? '')

  useEffect(() => {
    if (!profile) return
    fetchMine(profile.id).then(setItems).catch(() => setItems([])).finally(() => setLoading(false))
  }, [profile])

  const stats = useMemo(() => {
    const byKind = new Map<string, number>()
    let accepted = 0, edits = 0
    for (const c of items) {
      byKind.set(c.kind, (byKind.get(c.kind) ?? 0) + 1)
      if (c.status === 'accepted') accepted++
      if (c.kind !== 'comment') edits++
    }
    return { total: items.length, accepted, edits, byKind }
  }, [items])

  const shown = filter === 'all' ? items : items.filter(c => c.status === filter)

  return (
    <>
      <div className="page-header">
        <h1>{profile?.display_name || profile?.username}</h1>
        <p>
          @{profile?.username}
          {profile?.role !== 'member' && <span className="badge badge-accepted" style={{ marginLeft: '0.5rem' }}>{profile?.role}</span>}
        </p>
        {profile?.bio && !editing && <p style={{ marginTop: '0.4rem' }}>{profile.bio}</p>}
      </div>

      <div className="stats-grid">
        <div className="stat-card"><div className="stat-value">{stats.total}</div><div className="stat-label">Contributions</div></div>
        <div className="stat-card"><div className="stat-value">{stats.edits}</div><div className="stat-label">Edits &amp; sources</div></div>
        <div className="stat-card"><div className="stat-value">{stats.accepted}</div><div className="stat-label">Accepted</div></div>
        {[...stats.byKind].map(([kind, n]) => (
          <div className="stat-card" key={kind}>
            <div className="stat-value">{n}</div>
            <div className="stat-label">{KIND_LABEL[kind as keyof typeof KIND_LABEL]}</div>
          </div>
        ))}
      </div>

      <div className="cm-form-actions" style={{ margin: '1rem 0' }}>
        <button className="cm-btn" onClick={() => setEditing(v => !v)}>{editing ? 'Cancel' : 'Edit profile'}</button>
        <Link className="cm-btn" to="/leaderboard">Leaderboard</Link>
        {isModerator && <Link className="cm-btn" to="/moderate">Moderation queue</Link>}
        <button className="cm-btn" onClick={() => void onSignOut()}>Sign out</button>
      </div>

      {editing && (
        <form
          className="card cm-narrow cm-form"
          onSubmit={async e => { e.preventDefault(); await onSave({ display_name: displayName.trim() || null, bio: bio.trim() || null }); setEditing(false) }}
        >
          <label className="cm-field">
            <span className="cm-label">Display name</span>
            <input value={displayName} onChange={e => setDisplayName(e.target.value)} maxLength={60} />
          </label>
          <label className="cm-field">
            <span className="cm-label">Bio</span>
            <textarea value={bio} onChange={e => setBio(e.target.value)} maxLength={400} rows={3} />
          </label>
          <div className="cm-form-actions"><button className="cm-btn cm-btn-primary">Save</button></div>
        </form>
      )}

      <h2 className="cm-section-title">My contributions</h2>
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
      </div>

      {loading && <p className="cm-muted">Loading…</p>}
      {!loading && shown.length === 0 && (
        <p className="cm-muted">
          Nothing here yet. Open any page and use <em>Discuss this page</em>, or highlight a passage to
          anchor a correction to it.
        </p>
      )}
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

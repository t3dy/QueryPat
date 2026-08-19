import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  KIND_LABEL, PROPOSED_LABEL, STATUS_LABEL, deleteContribution, updateContribution,
  type Contribution, type ContributionStatus,
} from '../lib/supabase'
import { useAuth } from './auth-context'
import { pathLabel, permalink, timeAgo } from './util'

const STATUSES: ContributionStatus[] = ['open', 'accepted', 'rejected', 'duplicate']

interface Props {
  contribution: Contribution
  /** Show which page this belongs to (used on dashboards, not in-page threads). */
  showTarget?: boolean
  /** Link through to the page and open its thread at this comment. */
  linkToThread?: boolean
  /** Flash treatment when arrived at via a permalink. */
  highlighted?: boolean
  voteCount?: number
  voted?: boolean
  /** Absent when the reader is signed out or owns the contribution. */
  onToggleVote?: (id: number, on: boolean) => void
  onReply?: (id: number) => void
  /** Called with the updated row, or null when it was deleted. */
  onChange?: (next: Contribution | null) => void
  children?: React.ReactNode
}

export default function ContributionCard({
  contribution: c, showTarget, linkToThread, highlighted,
  voteCount = 0, voted = false, onToggleVote, onReply, onChange, children,
}: Props) {
  const { user, isModerator } = useAuth()
  const mine = user?.id === c.author_id
  const [editing, setEditing] = useState(false)
  const [body, setBody] = useState(c.body)
  const [proposed, setProposed] = useState(c.proposed_value ?? '')
  const [source, setSource] = useState(c.source_url ?? '')
  const [note, setNote] = useState(c.resolution_note ?? '')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [copied, setCopied] = useState(false)

  async function guard(fn: () => Promise<void>) {
    setBusy(true)
    setError(null)
    try { await fn() }
    catch (e) { setError(e instanceof Error ? e.message : 'That did not save.') }
    finally { setBusy(false) }
  }

  const saveEdit = () => guard(async () => {
    const patch = {
      body: body.trim(),
      proposed_value: proposed.trim() || null,
      source_url: source.trim() || null,
    }
    await updateContribution(c.id, patch)
    onChange?.({ ...c, ...patch })
    setEditing(false)
  })

  const setStatus = (status: ContributionStatus) => guard(async () => {
    const patch = { status, resolution_note: note.trim() || null }
    await updateContribution(c.id, patch)
    onChange?.({ ...c, ...patch })
  })

  const remove = () => {
    if (!confirm('Delete this contribution? This cannot be undone.')) return
    return guard(async () => {
      await deleteContribution(c.id)
      onChange?.(null)
    })
  }

  async function copyLink() {
    try {
      await navigator.clipboard.writeText(permalink(c.target_path, c.id))
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      setError('Could not copy the link.')
    }
  }

  const username = c.author?.username
  const authorName = c.author?.display_name || username || 'someone'
  const isReply = c.parent_id !== null
  const targetText = c.target_label || pathLabel(c.target_path)

  return (
    <article
      id={`cm-${c.id}`}
      className={`cm-card cm-kind-${c.kind} cm-status-${c.status} ${highlighted ? 'cm-highlighted' : ''}`}
    >
      <header className="cm-card-head">
        {!isReply && <span className={`cm-badge cm-badge-${c.kind}`}>{KIND_LABEL[c.kind]}</span>}
        {isReply && <span className="cm-badge">Reply</span>}
        {c.status !== 'open' && (
          <span className={`cm-badge cm-badge-status-${c.status}`}>{STATUS_LABEL[c.status]}</span>
        )}
        {username
          ? <Link className="cm-author" to={`/u/${username}`}>{authorName}</Link>
          : <span className="cm-author">{authorName}</span>}
        <time className="cm-time" dateTime={c.created_at}>{timeAgo(c.created_at)}</time>
      </header>

      {showTarget && (
        linkToThread
          ? <Link className="cm-target" to={`${c.target_path}?c=${c.id}`}>{targetText} →</Link>
          : <span className="cm-target">{targetText}</span>
      )}

      {c.quote && <blockquote className="cm-quote">“{c.quote}”</blockquote>}

      {editing ? (
        <div className="cm-form">
          <label className="cm-field">
            <span className="cm-label">Your note</span>
            <textarea value={body} onChange={e => setBody(e.target.value)} rows={4} maxLength={5000} />
          </label>
          {PROPOSED_LABEL[c.kind] && (
            <label className="cm-field">
              <span className="cm-label">{PROPOSED_LABEL[c.kind]}</span>
              <textarea value={proposed} onChange={e => setProposed(e.target.value)} rows={3} maxLength={5000} />
            </label>
          )}
          {(c.kind === 'source' || c.kind === 'correction') && (
            <label className="cm-field">
              <span className="cm-label">Source</span>
              <input value={source} onChange={e => setSource(e.target.value)} maxLength={500} />
            </label>
          )}
          <div className="cm-form-actions">
            <button className="cm-btn cm-btn-primary" onClick={saveEdit} disabled={busy || !body.trim()}>
              {busy ? 'Saving…' : 'Save'}
            </button>
            <button
              className="cm-btn"
              onClick={() => {
                setBody(c.body); setProposed(c.proposed_value ?? ''); setSource(c.source_url ?? '')
                setEditing(false)
              }}
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <p className="cm-body">{c.body}</p>
      )}

      {!editing && c.proposed_value && (
        <div className="cm-proposed">
          <span className="cm-label">{PROPOSED_LABEL[c.kind] ?? 'Proposed'}</span>
          <p>{c.proposed_value}</p>
        </div>
      )}

      {!editing && c.source_url && (
        <p className="cm-source">
          <span className="cm-label">Source</span>{' '}
          {/^https?:\/\//i.test(c.source_url)
            ? <a href={c.source_url} target="_blank" rel="noopener noreferrer">{c.source_url}</a>
            : c.source_url}
        </p>
      )}

      {c.resolution_note && (
        <p className="cm-resolution"><span className="cm-label">Editor’s note</span> {c.resolution_note}</p>
      )}

      {error && <p className="cm-error">{error}</p>}

      <footer className="cm-card-actions">
        {onToggleVote ? (
          <button
            className={`cm-link-btn ${voted ? 'cm-voted' : ''}`}
            onClick={() => onToggleVote(c.id, !voted)}
            title={voted ? 'Undo' : 'Mark this as helpful'}
          >
            ▲ Helpful{voteCount ? ` · ${voteCount}` : ''}
          </button>
        ) : voteCount > 0 && (
          <span className="cm-muted-inline" title="Readers who found this helpful">▲ {voteCount}</span>
        )}
        {onReply && <button className="cm-link-btn" onClick={() => onReply(c.id)}>Reply</button>}
        {mine && c.status === 'open' && !editing && (
          <button className="cm-link-btn" onClick={() => setEditing(true)}>Edit</button>
        )}
        {mine && c.status !== 'open' && (
          <span className="cm-muted-inline" title="Ruled on by an editor, so the wording is now fixed">Locked</span>
        )}
        <button className="cm-link-btn" onClick={copyLink}>{copied ? 'Link copied' : 'Copy link'}</button>
        {(mine || isModerator) && (
          <button className="cm-link-btn cm-danger" onClick={remove} disabled={busy}>Delete</button>
        )}
      </footer>

      {isModerator && (
        <div className="cm-mod">
          <input
            className="cm-mod-note"
            value={note}
            onChange={e => setNote(e.target.value)}
            placeholder="Editor’s note (shown to the contributor)"
            maxLength={1000}
          />
          <div className="cm-mod-buttons">
            {STATUSES.map(s => (
              <button
                key={s}
                className={`cm-btn cm-btn-sm ${c.status === s ? 'cm-btn-primary' : ''}`}
                disabled={busy}
                onClick={() => setStatus(s)}
              >
                {STATUS_LABEL[s]}
              </button>
            ))}
          </div>
        </div>
      )}

      {children}
    </article>
  )
}

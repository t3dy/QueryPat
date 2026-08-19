import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  KIND_LABEL, STATUS_LABEL, deleteContribution, updateContribution,
  type Contribution, type ContributionStatus,
} from '../lib/supabase'
import { useAuth } from './auth-context'
import { pathLabel, timeAgo } from './util'

const STATUSES: ContributionStatus[] = ['open', 'accepted', 'rejected', 'duplicate']

interface Props {
  contribution: Contribution
  /** Show which page this belongs to (used on dashboards, not in-page threads). */
  showTarget?: boolean
  voteCount?: number
  voted?: boolean
  onToggleVote?: (id: number, on: boolean) => void
  onReply?: (id: number) => void
  /** Called with the updated row, or null when it was deleted. */
  onChange?: (next: Contribution | null) => void
  children?: React.ReactNode
}

export default function ContributionCard({
  contribution: c, showTarget, voteCount = 0, voted = false,
  onToggleVote, onReply, onChange, children,
}: Props) {
  const { user, isModerator } = useAuth()
  const mine = user?.id === c.author_id
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState(c.body)
  const [note, setNote] = useState(c.resolution_note ?? '')
  const [busy, setBusy] = useState(false)

  async function saveEdit() {
    setBusy(true)
    try {
      await updateContribution(c.id, { body: draft.trim() })
      onChange?.({ ...c, body: draft.trim() })
      setEditing(false)
    } finally { setBusy(false) }
  }

  async function setStatus(status: ContributionStatus) {
    setBusy(true)
    try {
      await updateContribution(c.id, { status, resolution_note: note.trim() || null })
      onChange?.({ ...c, status, resolution_note: note.trim() || null })
    } finally { setBusy(false) }
  }

  async function remove() {
    if (!confirm('Delete this contribution?')) return
    setBusy(true)
    try {
      await deleteContribution(c.id)
      onChange?.(null)
    } finally { setBusy(false) }
  }

  const author = c.author?.display_name || c.author?.username || 'someone'

  return (
    <article className={`cm-card cm-kind-${c.kind} cm-status-${c.status}`}>
      <header className="cm-card-head">
        <span className={`cm-badge cm-badge-${c.kind}`}>{KIND_LABEL[c.kind]}</span>
        {c.status !== 'open' && (
          <span className={`cm-badge cm-badge-status-${c.status}`}>{STATUS_LABEL[c.status]}</span>
        )}
        <span className="cm-author">{author}</span>
        <time className="cm-time" dateTime={c.created_at}>{timeAgo(c.created_at)}</time>
      </header>

      {showTarget && (
        <Link className="cm-target" to={c.target_path}>
          {c.target_label || pathLabel(c.target_path)}
        </Link>
      )}

      {c.quote && <blockquote className="cm-quote">“{c.quote}”</blockquote>}

      {editing ? (
        <div className="cm-field">
          <textarea value={draft} onChange={e => setDraft(e.target.value)} rows={4} maxLength={5000} />
          <div className="cm-form-actions">
            <button className="cm-btn cm-btn-primary" onClick={saveEdit} disabled={busy || !draft.trim()}>Save</button>
            <button className="cm-btn" onClick={() => { setDraft(c.body); setEditing(false) }}>Cancel</button>
          </div>
        </div>
      ) : (
        <p className="cm-body">{c.body}</p>
      )}

      {c.proposed_value && (
        <div className="cm-proposed">
          <span className="cm-label">Proposed</span>
          <p>{c.proposed_value}</p>
        </div>
      )}

      {c.source_url && (
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

      <footer className="cm-card-actions">
        {onToggleVote && (
          <button
            className={`cm-link-btn ${voted ? 'cm-voted' : ''}`}
            onClick={() => onToggleVote(c.id, !voted)}
            title="Mark this as helpful"
          >
            ▲ {voteCount || ''} Helpful
          </button>
        )}
        {onReply && <button className="cm-link-btn" onClick={() => onReply(c.id)}>Reply</button>}
        {mine && c.status === 'open' && !editing && (
          <button className="cm-link-btn" onClick={() => setEditing(true)}>Edit</button>
        )}
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
            placeholder="Editor’s note (optional)"
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

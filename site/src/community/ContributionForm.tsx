import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  KINDS, PROPOSED_LABEL, createContribution,
  type Contribution, type ContributionKind,
} from '../lib/supabase'
import { useAuth } from './auth-context'

interface Props {
  targetPath: string
  targetLabel?: string | null
  targetSection?: string | null
  /** Text the reader highlighted on the page, if any. */
  quote?: string | null
  /** Called after a successful submit so the panel can drop the chip. */
  onClearQuote?: () => void
  parentId?: number | null
  placeholder?: string
  onCreated: (c: Contribution) => void
  onCancel?: () => void
}

export default function ContributionForm({
  targetPath, targetLabel, targetSection, quote, onClearQuote,
  parentId, placeholder, onCreated, onCancel,
}: Props) {
  const { user, profile } = useAuth()
  const [kind, setKind] = useState<ContributionKind>('comment')
  const [body, setBody] = useState('')
  const [proposed, setProposed] = useState('')
  const [sourceUrl, setSourceUrl] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  if (!user) {
    return (
      <p className="cm-signin-note">
        <Link to="/account">Sign in</Link> to leave a comment, correction, or suggested edit.
      </p>
    )
  }
  if (!profile) {
    return (
      <p className="cm-signin-note">
        Almost there — <Link to="/account">choose a username</Link> before contributing.
      </p>
    )
  }

  const proposedLabel = PROPOSED_LABEL[kind]
  const wantsSource = kind === 'source' || kind === 'correction'

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    if (!body.trim() || !profile) return
    setBusy(true)
    setError(null)
    try {
      const created = await createContribution(profile.id, {
        target_path: targetPath,
        target_label: targetLabel ?? null,
        target_section: targetSection ?? null,
        quote: quote ?? null,
        parent_id: parentId ?? null,
        kind,
        body: body.trim(),
        proposed_value: proposed.trim() || null,
        source_url: sourceUrl.trim() || null,
      })
      setBody(''); setProposed(''); setSourceUrl(''); setKind('comment')
      onClearQuote?.()
      onCreated(created)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not save that.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <form className="cm-form" onSubmit={submit}>
      {!parentId && (
        <label className="cm-field">
          <span className="cm-label">Type of contribution</span>
          <select value={kind} onChange={e => setKind(e.target.value as ContributionKind)}>
            {KINDS.map(k => <option key={k.value} value={k.value}>{k.label}</option>)}
          </select>
          <span className="cm-hint">{KINDS.find(k => k.value === kind)?.hint}</span>
        </label>
      )}

      <label className="cm-field">
        <span className="cm-label">{parentId ? 'Reply' : 'What would you like to say?'}</span>
        <textarea
          value={body}
          onChange={e => setBody(e.target.value)}
          rows={parentId ? 3 : 4}
          maxLength={5000}
          required
          placeholder={placeholder ?? 'Be specific — quote the passage you mean where you can.'}
        />
      </label>

      {!parentId && proposedLabel && (
        <label className="cm-field">
          <span className="cm-label">{proposedLabel}</span>
          <textarea
            value={proposed}
            onChange={e => setProposed(e.target.value)}
            rows={3}
            maxLength={5000}
            placeholder={
              kind === 'suggested_tag'
                ? 'e.g. tags: gnosticism, 2-3-74; date: 1974-03-20'
                : 'Paste the exact wording you would put in its place.'
            }
          />
        </label>
      )}

      {!parentId && wantsSource && (
        <label className="cm-field">
          <span className="cm-label">Source (URL or citation)</span>
          <input
            type="text"
            value={sourceUrl}
            onChange={e => setSourceUrl(e.target.value)}
            maxLength={500}
            placeholder="Sutin, Divine Invasions, p. 210 — or a link"
          />
        </label>
      )}

      {error && <p className="cm-error">{error}</p>}

      <div className="cm-form-actions">
        <button type="submit" className="cm-btn cm-btn-primary" disabled={busy || !body.trim()}>
          {busy ? 'Sending…' : parentId ? 'Reply' : 'Submit'}
        </button>
        {onCancel && (
          <button type="button" className="cm-btn" onClick={onCancel}>Cancel</button>
        )}
      </div>
    </form>
  )
}

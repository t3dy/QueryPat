import { useCallback, useEffect, useRef, useState } from 'react'
import { useLocation } from 'react-router-dom'
import {
  communityEnabled, fetchMyVotes, fetchThread, fetchVotes, toggleVote,
  type Contribution,
} from '../lib/supabase'
import { useAuth } from './auth-context'
import { normalizeQuote, pathLabel } from './util'
import ContributionCard from './ContributionCard'
import ContributionForm from './ContributionForm'

/** Minimum highlighted characters before we offer "comment on selection". */
const MIN_SELECTION = 8

export default function CommentsDock() {
  const { pathname } = useLocation()
  const { user } = useAuth()
  const [open, setOpen] = useState(false)
  const [items, setItems] = useState<Contribution[]>([])
  const [votes, setVotes] = useState<Map<number, number>>(new Map())
  const [myVotes, setMyVotes] = useState<Set<number>>(new Set())
  const [loading, setLoading] = useState(false)
  const [quote, setQuote] = useState<string | null>(null)
  const [replyTo, setReplyTo] = useState<number | null>(null)
  const [selection, setSelection] = useState<{ text: string; x: number; y: number } | null>(null)
  const panelRef = useRef<HTMLElement>(null)

  const [targetLabel, setTargetLabel] = useState(() => pathLabel(pathname))

  // The page heading is the most useful human label for a thread, but it only
  // exists once the route's data has resolved, so re-read it on a short delay.
  useEffect(() => {
    setTargetLabel(pathLabel(pathname))
    const t = setTimeout(() => {
      const h1 = document.querySelector('.app-main h1')?.textContent?.trim()
      if (h1) setTargetLabel(h1)
    }, 400)
    return () => clearTimeout(t)
  }, [pathname])

  const load = useCallback(async () => {
    if (!communityEnabled) return
    setLoading(true)
    try {
      const rows = await fetchThread(pathname)
      setItems(rows)
      const ids = rows.map(r => r.id)
      setVotes(await fetchVotes(ids))
      setMyVotes(user ? await fetchMyVotes(user.id, ids) : new Set())
    } catch {
      setItems([])
    } finally {
      setLoading(false)
    }
  }, [pathname, user])

  // Load the thread for whichever page we're on (cheap: one indexed query).
  useEffect(() => { void load() }, [load])

  // Close the drawer and drop any pending quote when the route changes.
  useEffect(() => { setOpen(false); setQuote(null); setReplyTo(null) }, [pathname])

  // Offer to anchor a comment to whatever the reader highlighted.
  useEffect(() => {
    if (!communityEnabled) return
    function onSelect() {
      const sel = window.getSelection()
      const text = sel?.toString() ?? ''
      if (!sel || sel.isCollapsed || text.trim().length < MIN_SELECTION) return setSelection(null)
      const node = sel.anchorNode
      const el = node instanceof Element ? node : node?.parentElement
      if (!el?.closest('.app-main') || el.closest('.cm-panel')) return setSelection(null)
      const rect = sel.getRangeAt(0).getBoundingClientRect()
      setSelection({ text: normalizeQuote(text), x: rect.left + rect.width / 2, y: rect.top })
    }
    document.addEventListener('selectionchange', onSelect)
    return () => document.removeEventListener('selectionchange', onSelect)
  }, [])

  // Escape closes the drawer.
  useEffect(() => {
    if (!open) return
    function onKey(e: KeyboardEvent) { if (e.key === 'Escape') setOpen(false) }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open])

  if (!communityEnabled) return null

  const roots = items.filter(c => c.parent_id === null)
  const repliesOf = (id: number) => items.filter(c => c.parent_id === id)
  const openCount = items.filter(c => c.status === 'open' && c.kind !== 'comment').length

  function applyChange(next: Contribution | null, id: number) {
    setItems(prev => next ? prev.map(c => (c.id === id ? next : c)) : prev.filter(c => c.id !== id && c.parent_id !== id))
  }

  async function vote(id: number, on: boolean) {
    if (!user) return
    setVotes(prev => new Map(prev).set(id, Math.max(0, (prev.get(id) ?? 0) + (on ? 1 : -1))))
    setMyVotes(prev => {
      const n = new Set(prev)
      if (on) n.add(id); else n.delete(id)
      return n
    })
    try { await toggleVote(user.id, id, on) } catch { void load() }
  }

  function startFromSelection() {
    if (!selection) return
    setQuote(selection.text)
    setReplyTo(null)
    setSelection(null)
    setOpen(true)
    window.getSelection()?.removeAllRanges()
    requestAnimationFrame(() => panelRef.current?.querySelector('textarea')?.focus())
  }

  return (
    <>
      {selection && !open && (
        <button
          className="cm-selection-btn"
          style={{ left: selection.x, top: Math.max(8, selection.y - 44) }}
          onClick={startFromSelection}
        >
          Comment on selection
        </button>
      )}

      <button
        className={`cm-fab ${open ? 'cm-fab-open' : ''}`}
        onClick={() => setOpen(o => !o)}
        aria-expanded={open}
        title="Community notes on this page"
      >
        {open ? 'Close' : 'Discuss this page'}
        {items.length > 0 && <span className="cm-fab-count">{items.length}</span>}
      </button>

      {open && (
        <aside className="cm-panel" ref={panelRef} aria-label="Community notes">
          <header className="cm-panel-head">
            <h2>Community notes</h2>
            <p className="cm-panel-target">{targetLabel}</p>
            {openCount > 0 && <p className="cm-panel-meta">{openCount} open suggestion{openCount === 1 ? '' : 's'}</p>}
            <button className="cm-close" onClick={() => setOpen(false)} aria-label="Close">×</button>
          </header>

          <div className="cm-panel-body">
            {loading && <p className="cm-muted">Loading…</p>}
            {!loading && roots.length === 0 && (
              <p className="cm-muted">
                No notes on this page yet. Highlight any passage to anchor a correction to it.
              </p>
            )}

            {roots.map(c => (
              <ContributionCard
                key={c.id}
                contribution={c}
                voteCount={votes.get(c.id) ?? 0}
                voted={myVotes.has(c.id)}
                onToggleVote={user ? vote : undefined}
                onReply={user ? id => setReplyTo(id === replyTo ? null : id) : undefined}
                onChange={next => applyChange(next, c.id)}
              >
                {repliesOf(c.id).map(r => (
                  <div className="cm-reply" key={r.id}>
                    <ContributionCard contribution={r} onChange={next => applyChange(next, r.id)} />
                  </div>
                ))}
                {replyTo === c.id && (
                  <ContributionForm
                    targetPath={pathname}
                    targetLabel={targetLabel}
                    parentId={c.id}
                    onCreated={created => { setItems(prev => [...prev, created]); setReplyTo(null) }}
                    onCancel={() => setReplyTo(null)}
                  />
                )}
              </ContributionCard>
            ))}
          </div>

          <div className="cm-panel-foot">
            {quote && (
              <div className="cm-quote cm-quote-draft">
                <span>“{quote}”</span>
                <button type="button" className="cm-link-btn" onClick={() => setQuote(null)}>remove</button>
              </div>
            )}
            <ContributionForm
              targetPath={pathname}
              targetLabel={targetLabel}
              quote={quote}
              onClearQuote={() => setQuote(null)}
              onCreated={created => setItems(prev => [...prev, created])}
            />
          </div>
        </aside>
      )}
    </>
  )
}

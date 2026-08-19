import { useCallback, useEffect, useRef, useState } from 'react'
import { useLocation, useSearchParams } from 'react-router-dom'
import { communityEnabled, fetchThread, type Contribution } from '../lib/supabase'
import { useAuth } from './auth-context'
import { useVotes } from './useVotes'
import { normalizeQuote, pathLabel, plural } from './util'
import ContributionCard from './ContributionCard'
import ContributionForm from './ContributionForm'

/** Minimum highlighted characters before we offer "comment on selection". */
const MIN_SELECTION = 8

type Filter = 'all' | 'suggestions' | 'comments' | 'open'

const FILTERS: { value: Filter; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'suggestions', label: 'Suggestions' },
  { value: 'comments', label: 'Comments' },
  { value: 'open', label: 'Unresolved' },
]

export default function CommentsDock() {
  const { pathname } = useLocation()
  const [params, setParams] = useSearchParams()
  const { user } = useAuth()
  const [open, setOpen] = useState(false)
  const [items, setItems] = useState<Contribution[]>([])
  const [loading, setLoading] = useState(false)
  const [quote, setQuote] = useState<string | null>(null)
  const [replyTo, setReplyTo] = useState<number | null>(null)
  const [filter, setFilter] = useState<Filter>('all')
  const [newest, setNewest] = useState(false)
  const [selection, setSelection] = useState<{ text: string; x: number; y: number } | null>(null)
  const panelRef = useRef<HTMLElement>(null)
  const { counts, mine, handlerFor } = useVotes(items)

  /** Set when the page was opened from a permalink like ?c=42. */
  const focusId = Number(params.get('c')) || null

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
      setItems(await fetchThread(pathname))
    } catch {
      setItems([])
    } finally {
      setLoading(false)
    }
  }, [pathname])

  // Load the thread for whichever page we're on (cheap: one indexed query).
  useEffect(() => { void load() }, [load])

  // Close the drawer and drop any pending quote when the route changes.
  useEffect(() => { setOpen(false); setQuote(null); setReplyTo(null); setFilter('all') }, [pathname])

  // Arriving on a permalink opens the drawer and scrolls to that contribution.
  useEffect(() => {
    if (!focusId || loading || !items.some(c => c.id === focusId)) return
    setOpen(true)
    const t = setTimeout(() => {
      document.getElementById(`cm-${focusId}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }, 120)
    return () => clearTimeout(t)
  }, [focusId, loading, items])

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

  const close = useCallback(() => {
    setOpen(false)
    if (params.has('c')) {
      const next = new URLSearchParams(params)
      next.delete('c')
      setParams(next, { replace: true })
    }
  }, [params, setParams])

  // Escape closes the drawer.
  useEffect(() => {
    if (!open) return
    function onKey(e: KeyboardEvent) { if (e.key === 'Escape') close() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, close])

  if (!communityEnabled) return null

  const roots = items.filter(c => c.parent_id === null)
  const repliesOf = (id: number) => items.filter(c => c.parent_id === id)
  const openSuggestions = items.filter(c => c.status === 'open' && c.kind !== 'comment').length

  const visible = roots
    .filter(c => {
      if (filter === 'suggestions') return c.kind !== 'comment'
      if (filter === 'comments') return c.kind === 'comment'
      if (filter === 'open') return c.status === 'open'
      return true
    })
    .sort((a, b) => newest
      ? b.created_at.localeCompare(a.created_at)
      : a.created_at.localeCompare(b.created_at))

  function applyChange(next: Contribution | null, id: number) {
    setItems(prev => next
      ? prev.map(c => (c.id === id ? next : c))
      : prev.filter(c => c.id !== id && c.parent_id !== id))
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
        onClick={() => (open ? close() : setOpen(true))}
        aria-expanded={open}
        title="Community notes on this page"
      >
        {open ? 'Close' : 'Discuss this page'}
        {items.length > 0 && (
          <span className={`cm-fab-count ${openSuggestions ? 'cm-fab-count-open' : ''}`}>
            {items.length}
          </span>
        )}
      </button>

      {open && (
        <aside className="cm-panel" ref={panelRef} role="dialog" aria-label="Community notes">
          <header className="cm-panel-head">
            <h2>Community notes</h2>
            <p className="cm-panel-target">{targetLabel}</p>
            <p className="cm-panel-meta">
              {items.length === 0 ? 'Nothing here yet' : plural(items.length, 'note')}
              {openSuggestions > 0 && ` · ${openSuggestions} unresolved`}
            </p>
            <button className="cm-close" onClick={close} aria-label="Close">×</button>
          </header>

          {roots.length > 1 && (
            <div className="cm-panel-filters">
              {FILTERS.map(f => (
                <button
                  key={f.value}
                  className={`cm-chip ${filter === f.value ? 'cm-chip-on' : ''}`}
                  onClick={() => setFilter(f.value)}
                >
                  {f.label}
                </button>
              ))}
              <button className="cm-link-btn cm-sort" onClick={() => setNewest(v => !v)}>
                Sort: {newest ? 'newest first' : 'oldest first'}
              </button>
            </div>
          )}

          <div className="cm-panel-body">
            {loading && <p className="cm-muted">Loading…</p>}
            {!loading && roots.length === 0 && (
              <p className="cm-muted">
                No notes on this page yet. Highlight any passage to anchor a correction to it.
              </p>
            )}
            {!loading && roots.length > 0 && visible.length === 0 && (
              <p className="cm-muted">Nothing matches this filter.</p>
            )}

            {visible.map(c => (
              <ContributionCard
                key={c.id}
                contribution={c}
                highlighted={c.id === focusId}
                voteCount={counts.get(c.id) ?? 0}
                voted={mine.has(c.id)}
                onToggleVote={handlerFor(c)}
                onReply={user ? id => setReplyTo(id === replyTo ? null : id) : undefined}
                onChange={next => applyChange(next, c.id)}
              >
                {repliesOf(c.id).map(r => (
                  <div className="cm-reply" key={r.id}>
                    <ContributionCard
                      contribution={r}
                      highlighted={r.id === focusId}
                      voteCount={counts.get(r.id) ?? 0}
                      voted={mine.has(r.id)}
                      onToggleVote={handlerFor(r)}
                      onChange={next => applyChange(next, r.id)}
                    />
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

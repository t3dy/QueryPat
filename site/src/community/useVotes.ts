import { useCallback, useEffect, useState } from 'react'
import { fetchMyVotes, fetchVotes, toggleVote, type Contribution } from '../lib/supabase'
import { useAuth } from './auth-context'

/**
 * Upvote counts for a list of contributions, plus which ones the signed-in
 * reader has already marked helpful. Updates optimistically and re-syncs if
 * the write fails.
 */
export function useVotes(items: Contribution[]) {
  const { user } = useAuth()
  const [counts, setCounts] = useState<Map<number, number>>(new Map())
  const [mine, setMine] = useState<Set<number>>(new Set())

  // Keyed on the id list so we refetch when the collection actually changes,
  // not on every render that produces a new array.
  const key = items.map(i => i.id).join(',')

  const sync = useCallback(async () => {
    const ids = key ? key.split(',').map(Number) : []
    if (!ids.length) {
      setCounts(new Map())
      setMine(new Set())
      return
    }
    try {
      setCounts(await fetchVotes(ids))
      setMine(user ? await fetchMyVotes(user.id, ids) : new Set())
    } catch {
      /* votes are decoration; a failure here should not break the list */
    }
  }, [key, user])

  useEffect(() => { void sync() }, [sync])

  const toggle = useCallback(async (id: number, on: boolean) => {
    if (!user) return
    setCounts(prev => new Map(prev).set(id, Math.max(0, (prev.get(id) ?? 0) + (on ? 1 : -1))))
    setMine(prev => {
      const next = new Set(prev)
      if (on) next.add(id); else next.delete(id)
      return next
    })
    try { await toggleVote(user.id, id, on) } catch { void sync() }
  }, [user, sync])

  /** You cannot upvote your own work — that would just inflate your score. */
  const handlerFor = useCallback(
    (c: Contribution) => (user && c.author_id !== user.id ? toggle : undefined),
    [user, toggle],
  )

  return { counts, mine, toggle, handlerFor }
}

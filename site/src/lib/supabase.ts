import { createClient, type SupabaseClient } from '@supabase/supabase-js'

const url = import.meta.env.VITE_SUPABASE_URL as string | undefined
const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined

/**
 * Community features are optional. When the two env vars are absent (local
 * builds, the GitHub Pages deploy) the whole layer stays dormant and the site
 * behaves exactly as it did before.
 */
export const communityEnabled = Boolean(url && anonKey)

export const supabase: SupabaseClient | null = communityEnabled
  ? createClient(url!, anonKey!, {
      auth: {
        persistSession: true,
        autoRefreshToken: true,
        detectSessionInUrl: true,
        // PKCE returns `?code=...` in the query string rather than the URL
        // fragment, which matters because this app uses a HashRouter.
        flowType: 'pkce',
      },
    })
  : null

/** Throws only if called behind a `communityEnabled` guard that was skipped. */
export function db(): SupabaseClient {
  if (!supabase) throw new Error('Supabase is not configured')
  return supabase
}

// ── Types ───────────────────────────────────────────────────────

export type ContributionKind =
  | 'comment'
  | 'correction'
  | 'suggested_edit'
  | 'suggested_tag'
  | 'source'

export type ContributionStatus = 'open' | 'accepted' | 'rejected' | 'duplicate'

export interface Profile {
  id: string
  username: string
  display_name: string | null
  bio: string | null
  role: 'member' | 'moderator' | 'admin'
  created_at: string
}

export interface Contribution {
  id: number
  author_id: string
  parent_id: number | null
  target_path: string
  target_label: string | null
  target_section: string | null
  quote: string | null
  kind: ContributionKind
  status: ContributionStatus
  body: string
  proposed_value: string | null
  source_url: string | null
  resolution_note: string | null
  created_at: string
  updated_at: string
  author?: Pick<Profile, 'username' | 'display_name'> | null
  vote_count?: number
}

export interface LeaderboardRow {
  user_id: string
  username: string
  display_name: string | null
  role: string
  total: number
  accepted: number
  open_count: number
  edits: number
  corrections: number
  suggested_edits: number
  tags: number
  sources: number
  upvotes: number
  score: number
  last_contribution_at: string | null
}

export const KINDS: { value: ContributionKind; label: string; hint: string }[] = [
  { value: 'comment', label: 'Comment', hint: 'A general remark or question about this page.' },
  { value: 'correction', label: 'Correction', hint: 'Something here is factually wrong. Say what it should be.' },
  { value: 'suggested_edit', label: 'Suggested edit', hint: 'Propose replacement wording for a passage.' },
  { value: 'suggested_tag', label: 'Suggested tag / metadata', hint: 'Propose tags, dates, or other structured metadata.' },
  { value: 'source', label: 'Relevant source', hint: 'Point to a citation, letter, interview, or scholarly work.' },
]

export const KIND_LABEL: Record<ContributionKind, string> = Object.fromEntries(
  KINDS.map(k => [k.value, k.label]),
) as Record<ContributionKind, string>

export const STATUS_LABEL: Record<ContributionStatus, string> = {
  open: 'Open',
  accepted: 'Accepted',
  rejected: 'Declined',
  duplicate: 'Duplicate',
}

/** Which kinds ask for a "proposed value" second field, and what to call it. */
export const PROPOSED_LABEL: Partial<Record<ContributionKind, string>> = {
  correction: 'Corrected text (optional)',
  suggested_edit: 'Proposed replacement text',
  suggested_tag: 'Proposed tags / metadata',
}

const SELECT_WITH_AUTHOR =
  '*, author:profiles!contributions_author_id_fkey(username, display_name)'

// ── Queries ─────────────────────────────────────────────────────

export async function fetchProfile(userId: string): Promise<Profile | null> {
  const { data } = await db().from('profiles').select('*').eq('id', userId).maybeSingle()
  return (data as Profile) ?? null
}

export async function fetchThread(targetPath: string): Promise<Contribution[]> {
  const { data, error } = await db()
    .from('contributions')
    .select(SELECT_WITH_AUTHOR)
    .eq('target_path', targetPath)
    .order('created_at', { ascending: true })
  if (error) throw error
  return (data ?? []) as Contribution[]
}

export async function fetchMine(userId: string): Promise<Contribution[]> {
  const { data, error } = await db()
    .from('contributions')
    .select(SELECT_WITH_AUTHOR)
    .eq('author_id', userId)
    .order('created_at', { ascending: false })
  if (error) throw error
  return (data ?? []) as Contribution[]
}

export async function fetchRecent(limit = 60, status?: ContributionStatus): Promise<Contribution[]> {
  let q = db()
    .from('contributions')
    .select(SELECT_WITH_AUTHOR)
    .order('created_at', { ascending: false })
    .limit(limit)
  if (status) q = q.eq('status', status)
  const { data, error } = await q
  if (error) throw error
  return (data ?? []) as Contribution[]
}

export async function fetchLeaderboard(): Promise<LeaderboardRow[]> {
  const { data, error } = await db()
    .from('leaderboard')
    .select('*')
    .order('score', { ascending: false })
    .limit(100)
  if (error) throw error
  return (data ?? []) as LeaderboardRow[]
}

export type NewContribution = Pick<Contribution, 'target_path' | 'kind' | 'body'> &
  Partial<Pick<Contribution,
    'target_label' | 'target_section' | 'quote' | 'proposed_value' | 'source_url' | 'parent_id'>>

export async function createContribution(authorId: string, input: NewContribution) {
  const { data, error } = await db()
    .from('contributions')
    .insert({ ...input, author_id: authorId })
    .select(SELECT_WITH_AUTHOR)
    .single()
  if (error) throw error
  return data as Contribution
}

export async function updateContribution(id: number, patch: Partial<Contribution>) {
  const { error } = await db().from('contributions').update(patch).eq('id', id)
  if (error) throw error
}

export async function deleteContribution(id: number) {
  const { error } = await db().from('contributions').delete().eq('id', id)
  if (error) throw error
}

export async function fetchVotes(ids: number[]): Promise<Map<number, number>> {
  const counts = new Map<number, number>()
  if (!ids.length) return counts
  const { data } = await db().from('contribution_votes').select('contribution_id').in('contribution_id', ids)
  for (const row of (data ?? []) as { contribution_id: number }[]) {
    counts.set(row.contribution_id, (counts.get(row.contribution_id) ?? 0) + 1)
  }
  return counts
}

export async function fetchMyVotes(userId: string, ids: number[]): Promise<Set<number>> {
  if (!ids.length) return new Set()
  const { data } = await db()
    .from('contribution_votes')
    .select('contribution_id')
    .eq('voter_id', userId)
    .in('contribution_id', ids)
  return new Set(((data ?? []) as { contribution_id: number }[]).map(r => r.contribution_id))
}

export async function toggleVote(userId: string, contributionId: number, on: boolean) {
  const table = db().from('contribution_votes')
  const { error } = on
    ? await table.insert({ contribution_id: contributionId, voter_id: userId })
    : await table.delete().eq('contribution_id', contributionId).eq('voter_id', userId)
  if (error) throw error
}

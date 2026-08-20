import { useEffect, useState } from 'react'

export interface Option {
  value: string
  label: string
  /** Optgroup heading, where the picker groups its choices. */
  group?: string
  /** Route this option points at, so a saved choice stays clickable. */
  to?: string
}

/**
 * The sections of the archive someone can say they work on. These mirror the
 * main nav, and each one links to the section it names.
 */
export const AREAS: Option[] = [
  { value: 'biography', label: 'Biography', to: '/biography' },
  { value: 'exegesis', label: 'The Exegesis', to: '/exegesis' },
  { value: 'works', label: 'Works & bibliography', to: '/works' },
  { value: 'themes', label: 'Themes', to: '/themes' },
  { value: 'dictionary', label: 'Dictionary of terms', to: '/dictionary' },
  { value: 'theophanies', label: 'Theophanies & 2-3-74', to: '/theophanies' },
  { value: 'essays', label: 'Essays', to: '/essays' },
  { value: 'studies', label: 'Studies (AI & psychology)', to: '/studies' },
  { value: 'archive', label: 'Archive documents', to: '/archive' },
  { value: 'people', label: 'People PKD knew', to: '/people' },
  { value: 'names', label: 'Names & sources', to: '/names' },
  { value: 'scholars', label: 'Scholarship & reception', to: '/scholars' },
  { value: 'pkd-on-pkd', label: 'PKD on PKD', to: '/pkd-on-pkd' },
  { value: 'timeline', label: 'Timeline', to: '/timeline' },
  { value: 'map', label: 'Places & the map', to: '/map' },
]

export const AREA_LABEL = new Map(AREAS.map(a => [a.value, a]))

export interface SiteVocab {
  works: Option[]
  themes: Option[]
  interests: Option[]
  loaded: boolean
}

const EMPTY: SiteVocab = { works: [], themes: [], interests: [], loaded: false }

const WORK_GROUPS: Record<string, string> = {
  novels: 'Novels',
  short_stories: 'Short stories & collections',
  primary: 'Primary sources',
  letters: 'Letters',
  interviews: 'Interviews',
  newspaper: 'Newspaper',
}

/** Built once per page load and shared by every picker. */
let cache: SiteVocab | null = null
let inflight: Promise<SiteVocab> | null = null

async function json<T>(path: string): Promise<T | null> {
  try {
    const r = await fetch(import.meta.env.BASE_URL + 'data/' + path)
    return r.ok ? ((await r.json()) as T) : null
  } catch {
    return null
  }
}

async function build(): Promise<SiteVocab> {
  type Work = { slug: string; canonical_title: string; category?: string }
  type Theme = { slug: string; label: string }
  type Term = { slug: string; canonical_name: string; mention_count?: number; primary_category?: string }
  type Essay = { slug: string; title: string; topic?: string }
  type Study = { study_id: string; study_label: string }

  const [works, themes, terms, essays, studies] = await Promise.all([
    json<Work[]>('works/index.json'),
    json<{ themes: Theme[] }>('themes/index.json'),
    json<Term[]>('dictionary/index.json'),
    json<{ essays: Essay[] }>('essays/index.json'),
    json<Study[]>('studies/index.json'),
  ])

  const workOptions: Option[] = (works ?? [])
    .map(w => ({
      value: w.slug,
      label: w.canonical_title,
      group: WORK_GROUPS[w.category ?? ''] ?? 'Other',
      to: `/works/${w.slug}`,
    }))
    .sort((a, b) => a.group!.localeCompare(b.group!) || a.label.localeCompare(b.label))

  const themeOptions: Option[] = (themes?.themes ?? [])
    .map(t => ({ value: t.slug, label: t.label, to: `/themes/${t.slug}` }))
    .sort((a, b) => a.label.localeCompare(b.label))

  // Research-interest suggestions come from the topics the site actually
  // covers: its study areas, its essay subjects, its themes, and the concepts
  // that carry the most weight in the Exegesis dictionary.
  const interests: Option[] = [
    ...(studies ?? []).map(s => ({
      value: s.study_label, label: s.study_label, group: 'Study areas', to: `/studies/${s.study_id}`,
    })),
    ...(essays?.essays ?? []).map(e => ({
      value: e.title, label: e.title, group: 'Essay subjects', to: `/essays/${e.slug}`,
    })),
    ...(themes?.themes ?? []).map(t => ({
      value: t.label, label: t.label, group: 'Themes', to: `/themes/${t.slug}`,
    })),
    ...(terms ?? [])
      .slice()
      .sort((a, b) => (b.mention_count ?? 0) - (a.mention_count ?? 0))
      .slice(0, 60)
      .map(t => ({
        value: t.canonical_name, label: t.canonical_name, group: 'Concepts in the Exegesis',
        to: `/dictionary/${t.slug}`,
      })),
  ]

  // Two sources can suggest the same word; first one in wins its link.
  const seen = new Set<string>()
  const deduped = interests.filter(o => {
    const k = o.value.toLowerCase()
    if (seen.has(k)) return false
    seen.add(k)
    return true
  })

  return { works: workOptions, themes: themeOptions, interests: deduped, loaded: true }
}

/**
 * Options for the profile pickers, read from the same JSON the site renders
 * from — so the choices on offer are always the archive's real contents.
 */
export function useSiteVocab(enabled = true): SiteVocab {
  const [vocab, setVocab] = useState<SiteVocab>(cache ?? EMPTY)

  useEffect(() => {
    if (!enabled || cache) return
    let live = true
    inflight ??= build()
    void inflight.then(v => {
      cache = v
      if (live) setVocab(v)
    })
    return () => { live = false }
  }, [enabled])

  return vocab
}

/** Resolve a stored slug back to its label and link, or fall back gracefully. */
export function lookup(options: Option[], value: string): Option {
  return (
    options.find(o => o.value === value) ?? {
      value,
      label: value.replace(/[-_]/g, ' ').replace(/^\w/, c => c.toUpperCase()),
    }
  )
}

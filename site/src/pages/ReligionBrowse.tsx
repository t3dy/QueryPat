import { useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface FindingRow {
  id: string
  lane: string
  corpus: string
  src: string
  title: string | null
  date: string | null
  dd: string | null
  decade: string | null
  m: string
  tier: string
  c: string
  st: string
  doc?: string
  rel?: number
  n?: string
  subs: string[]
}

interface SubsectionFile {
  subsection_id: string
  topic_id: string
  rows: FindingRow[]
}

interface IndexSubsection {
  subsection_id: string
  label: string
  browse_count: number
}

interface IndexTopic {
  topic_id: string
  canonical_name: string
  slug: string
  subsections?: IndexSubsection[]
}

interface StudyIndex {
  topics: IndexTopic[]
}

const LANE_LABEL: Record<string, string> = {
  A: "PKD's own words",
  C: 'Scholarship',
}

const RELEVANCE_LABEL: Record<number, string> = {
  1: 'direct engagement',
  2: 'used as a tool',
  3: 'passing mention',
  4: 'thematic parallel',
  5: 'false positive',
}

const PAGE_SIZE = 40
const DEFAULT_TOPIC = 'christianity'

function escapeRegExp(s: string) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/** The context, with the matched term marked. */
function Highlighted({ text, term }: { text: string; term: string }) {
  if (!term) return <>{text}</>
  const parts = text.split(new RegExp(`(${escapeRegExp(term)})`, 'i'))
  return (
    <>
      {parts.map((part, i) =>
        part.toLowerCase() === term.toLowerCase() ? <mark key={i}>{part}</mark> : <span key={i}>{part}</span>,
      )}
    </>
  )
}

export default function ReligionBrowse() {
  const [params, setParams] = useSearchParams()
  const { data: index, loading: indexLoading } = useData<StudyIndex>('studies/religion/index.json')

  const topics = useMemo(() => (index?.topics ?? []).filter(t => t.subsections && t.subsections.length), [index])
  const topicParam = params.get('topic') ?? DEFAULT_TOPIC
  const topic = topics.find(t => t.slug === topicParam) ?? topics[0]
  const subs = topic?.subsections ?? []
  const subParam = params.get('sub')
  const sub = subs.find(s => s.subsection_id === subParam) ?? subs[0]

  const { data: file, loading, error } = useData<SubsectionFile>(
    sub ? `studies/religion/findings/${sub.subsection_id}.json` : null,
  )

  const lane = params.get('lane') ?? 'all'
  const decade = params.get('decade') ?? 'all'
  const tier = params.get('tier') ?? 'all'
  const status = params.get('status') ?? 'all'
  const q = params.get('q') ?? ''
  const page = Math.max(1, Number(params.get('page') ?? '1'))

  // Which topic each subsection belongs to, for the cross-links on each finding.
  const topicOf = useMemo(() => {
    const m = new Map<string, IndexTopic>()
    for (const t of topics) for (const s of t.subsections ?? []) m.set(s.subsection_id, t)
    return m
  }, [topics])
  const labelOf = useMemo(() => {
    const m = new Map<string, string>()
    for (const t of topics) for (const s of t.subsections ?? []) m.set(s.subsection_id, s.label)
    return m
  }, [topics])

  const rows = file?.rows ?? []
  const decades = useMemo(
    () => Array.from(new Set(rows.map(r => r.decade).filter((d): d is string => !!d))).sort(),
    [rows],
  )

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase()
    return rows.filter(r => {
      if (lane !== 'all' && r.lane !== lane) return false
      if (decade !== 'all' && r.decade !== decade) return false
      if (tier !== 'all' && r.tier !== tier) return false
      if (status !== 'all' && r.st !== status) return false
      if (needle && !(r.c.toLowerCase().includes(needle) || r.m.toLowerCase().includes(needle))) return false
      return true
    })
  }, [rows, lane, decade, tier, status, q])

  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const current = Math.min(page, pageCount)
  const shown = filtered.slice((current - 1) * PAGE_SIZE, current * PAGE_SIZE)

  /** Set one or more params; any filter change returns to page 1. */
  function update(patch: Record<string, string | null>, resetPage = true) {
    const next = new URLSearchParams(params)
    for (const [k, v] of Object.entries(patch)) {
      if (v === null || v === '' || v === 'all') next.delete(k)
      else next.set(k, v)
    }
    if (resetPage) next.delete('page')
    setParams(next)
  }

  function chooseTopic(slug: string) {
    const first = topics.find(t => t.slug === slug)?.subsections?.[0]?.subsection_id ?? null
    update({ topic: slug, sub: first, decade: null, tier: null, status: null, lane: null, q: null })
  }

  if (indexLoading) return <div className="loading">Loading...</div>
  if (!index || !topic) return <div className="loading">Religion index not found.</div>

  return (
    <>
      <div className="page-header">
        <h1>Religion in PKD: browse</h1>
        <div className="card-meta">
          <span>Every mention in Dick's own words (lane A) and in scholarship (lane C), by subsection.</span>
        </div>
      </div>

      <div className="card-meta" style={{ gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
        <label>
          Tradition{' '}
          <select className="filter-select" value={topic.slug} onChange={e => chooseTopic(e.target.value)}>
            {topics.map(t => (
              <option key={t.topic_id} value={t.slug}>{t.canonical_name}</option>
            ))}
          </select>
        </label>
        <label>
          Subsection{' '}
          <select className="filter-select" value={sub?.subsection_id ?? ''}
                  onChange={e => update({ sub: e.target.value })}>
            {subs.map(s => (
              <option key={s.subsection_id} value={s.subsection_id}>
                {s.label} ({s.browse_count})
              </option>
            ))}
          </select>
        </label>
        <label>
          Lane{' '}
          <select className="filter-select" value={lane} onChange={e => update({ lane: e.target.value })}>
            <option value="all">All</option>
            <option value="A">PKD's own words</option>
            <option value="C">Scholarship</option>
          </select>
        </label>
        <label>
          Decade{' '}
          <select className="filter-select" value={decade} onChange={e => update({ decade: e.target.value })}>
            <option value="all">All</option>
            {decades.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        </label>
        <label>
          Match{' '}
          <select className="filter-select" value={tier} onChange={e => update({ tier: e.target.value })}>
            <option value="all">All</option>
            <option value="strong">Strong terms</option>
            <option value="weak">Weak terms (read these)</option>
          </select>
        </label>
        <label>
          Review{' '}
          <select className="filter-select" value={status} onChange={e => update({ status: e.target.value })}>
            <option value="all">All</option>
            <option value="unreviewed">Unreviewed</option>
            <option value="reviewed">Reviewed</option>
            <option value="excluded">Excluded</option>
          </select>
        </label>
      </div>

      <input
        className="search-input"
        type="text"
        placeholder="Search within this subsection..."
        value={q}
        onChange={e => update({ q: e.target.value })}
      />

      {sub && (
        <p className="card-meta">
          <Link to={`/studies/religion/${topic.slug}`}>{topic.canonical_name}</Link>
          {' · '}
          {sub.label}
          {' · '}
          {loading ? 'loading…' : `${filtered.length} of ${rows.length} findings`}
          {error && <span> — {error}</span>}
        </p>
      )}

      {shown.map(r => (
        <div key={r.id} className="card" id={r.id}>
          <div className="card-meta" style={{ gap: '0.5rem', flexWrap: 'wrap' }}>
            <span className={`lane-badge lane-${r.lane.toLowerCase()}`}>{LANE_LABEL[r.lane] ?? r.lane}</span>
            <span>{r.dd || r.date || 'undated'}</span>
            <span>{r.title}</span>
            {r.tier === 'weak' && <span>weak term</span>}
            {r.rel && <span title={RELEVANCE_LABEL[r.rel]}>relevance {r.rel}: {RELEVANCE_LABEL[r.rel]}</span>}
            <span>{r.st}</span>
          </div>
          <p style={{ fontSize: '0.92rem', lineHeight: 1.6 }}>
            <Highlighted text={r.c} term={r.m} />
          </p>
          {r.n && <p className="card-meta">Note: {r.n}</p>}
          <div className="card-meta" style={{ gap: '0.4rem', flexWrap: 'wrap' }}>
            <span>Also in:</span>
            {r.subs
              .filter(id => id !== sub?.subsection_id)
              .map(id => {
                const t = topicOf.get(id)
                return (
                  <button
                    key={id}
                    className="entity-linked"
                    onClick={() => update({ topic: t?.slug ?? topic.slug, sub: id, q: null })}
                  >
                    {labelOf.get(id) ?? id}
                  </button>
                )
              })}
            {r.subs.length <= 1 && <span>only here</span>}
          </div>
        </div>
      ))}

      {!loading && filtered.length === 0 && <p>No findings match these filters.</p>}

      {pageCount > 1 && (
        <div className="card-meta" style={{ gap: '1rem', marginTop: '1rem' }}>
          <button disabled={current <= 1} onClick={() => update({ page: String(current - 1) }, false)}>
            Previous
          </button>
          <span>Page {current} of {pageCount}</span>
          <button disabled={current >= pageCount} onClick={() => update({ page: String(current + 1) }, false)}>
            Next
          </button>
        </div>
      )}
    </>
  )
}

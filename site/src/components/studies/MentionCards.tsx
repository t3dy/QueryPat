import { useEffect, useMemo, useState } from 'react'
import { Link, useLocation, useSearchParams } from 'react-router-dom'
import LaneBadge from './LaneBadge'

export interface MentionCard {
  id: string
  citation: string
  date?: string | null
  source_type: string
  published_folio?: string | null
  seg_id?: string | null
  doc_id?: string | null
  lane: string
  register: string
  relevance: number
  concepts: string[]
  /** Editorial summary of the whole passage and its place in the work. */
  context: string
  /** Short verbatim quotation of the sentence the passage turns on. */
  pith: string
  speaker: string
  editorial_note?: string | null
  /** Date, and the evidence for it: stamp, edition, folder or record. */
  dated?: string | null
  dating_basis?: string | null
  /** The verbatim windowed excerpt this card summarises. */
  passage?: string | null
  /** Key of the browse group this card is shown under, when the topic has one. */
  group?: string | null
  /** Which group this card belongs to, when the topic supplies `mention_groups`. */
  group_key?: string | null
  /** True when `context` is machine-derived rather than editorially written. */
  context_derived?: boolean
  /** Register terms in the passage beyond this topic's own. */
  also_names?: string[]
}

/** A topic may supply its own grouping; see GROUPS for the default. */
export interface MentionGroup {
  key: string
  label: string
  blurb: string
}

/** A browsable value of the cards' `concepts`: a book, theme, edition or work. */
export interface BrowseFacet {
  label: string
  kind: string
  /** Portal page about this facet, e.g. /dictionary/acts. */
  link?: string
  /** Other concept spellings this facet also matches (e.g. Valis / VALIS). */
  aliases?: string[]
}

/** Per-topic browse configuration, authored with the dossier. */
export interface BrowseConfig {
  intro?: string
  /** Card groups; when absent the topic keeps its built-in grouping. */
  groups?: { key: string; label: string; blurb: string }[]
  facet_kinds: { kind: string; label: string }[]
  facets: BrowseFacet[]
}

interface Props {
  cards: MentionCard[]
  browse?: BrowseConfig | null
  /** Groups keyed to `card.group_key`. Omit to use the default grouping. */
  groups?: MentionGroup[] | null
  /** Heading and standfirst, when the default Burroughs wording is wrong. */
  heading?: string
  intro?: string
}

const LANE_LABELS: Record<string, string> = {
  A: 'Fiction', B: 'Exegesis', C: 'Scholarship', D: 'Biography', E: 'Letters & interviews',
}

/** Groups for the Burroughs dossier, which predates authored browse configs. */
const GROUPS: { key: string; label: string; blurb: string; match: (c: MentionCard) => boolean }[] = [
  {
    key: '1976',
    label: 'The Exegesis — 15 September 1976',
    blurb: 'The first reading of The Ticket That Exploded, and the modification Dick made the same day.',
    match: c => c.source_type === 'exegesis_segment' && (c.date || '').startsWith('1976'),
  },
  {
    key: '1978',
    label: 'The Exegesis — 10 October 1978',
    blurb: '"William Burroughs is correct" — alongside three incompatible readings in the same section.',
    match: c => c.source_type === 'exegesis_segment' && (c.date || '').startsWith('1978'),
  },
  {
    key: '1981',
    label: 'The Exegesis — 16 April 1981',
    blurb: 'The reversal, and the passages in the same sitting that refuse to hold it.',
    match: c => c.source_type === 'exegesis_segment' && (c.date || '').startsWith('1981'),
  },
  {
    key: 'published',
    label: 'The Exegesis — passages printed only in the 2011 edition',
    blurb: 'Four folios in the Jackson and Lethem selection that our folder transcriptions do not contain.',
    match: c => c.source_type === 'exegesis_published',
  },
  {
    key: 'letters',
    label: 'Letters',
    blurb: 'Eleven letters, 1976 to 1981. Dick explaining himself to someone else.',
    match: c => c.source_type === 'letter',
  },
  {
    key: 'interview',
    label: 'Interview and essay',
    blurb: 'Dick on the word virus in his own voice, and his own account of language as control.',
    match: c => c.source_type === 'interview',
  },
  {
    key: 'scholarship',
    label: 'Biography and scholarship',
    blurb: 'What Sutin, Lapoujade, Butler and Davis say — not Dick.',
    match: c => c.source_type === 'criticism',
  },
]

/** How a card's date was arrived at, spelled out for the badge's tooltip. */
const DATING_BASIS: Record<string, string> = {
  dateline: 'Dated from the letter’s own dateline',
  stamp: 'Dated from a date written on the page itself',
  edition: 'Dated by its position among dated entries in the published edition',
  folder: 'Dated from the archival folder’s position in the published edition',
  record: 'Dated from our container record only — nothing in the passage confirms it',
  publication: 'Year of publication of the secondary source, not of Dick’s remark',
}

function datingTitle(basis?: string | null): string | undefined {
  if (!basis) return undefined
  return DATING_BASIS[basis] ?? `Dated from the ${basis}`
}

export default function MentionCards({ cards, browse, groups, heading, intro }: Props) {
  const [openNote, setOpenNote] = useState<string | null>(null)
  const [openPassage, setOpenPassage] = useState<Set<string>>(new Set())
  const [params, setParams] = useSearchParams()
  // The site uses a HashRouter, so the in-page anchor is the router's hash
  // (#/studies/x/y?facet=Acts#card-ID), not window.location.hash.
  const { hash } = useLocation()
  const facet = params.get('facet')
  const lane = params.get('lane')

  function setFilters(changes: Record<string, string | null>) {
    const next = new URLSearchParams(params)
    for (const [k, v] of Object.entries(changes)) {
      if (v) next.set(k, v)
      else next.delete(k)
    }
    setParams(next, { replace: true, preventScrollReset: true })
  }

  function setFilter(key: 'facet' | 'lane', value: string | null) {
    setFilters({ [key]: value })
  }

  function togglePassage(id: string) {
    setOpenPassage(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  // Each facet label with the concept spellings it stands for.
  const facetSpellings = useMemo(() => {
    const m = new Map<string, string[]>()
    for (const f of browse?.facets || []) m.set(f.label, [f.label, ...(f.aliases || [])])
    return m
  }, [browse])
  const hasFacet = (c: MentionCard, label: string) =>
    (facetSpellings.get(label) || [label]).some(k => c.concepts.includes(k))

  const visible = useMemo(
    () =>
      (cards || []).filter(
        c => (!facet || hasFacet(c, facet)) && (!lane || c.lane === lane),
      ),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [cards, facet, lane, facetSpellings],
  )

  const grouped = useMemo(() => {
    // Grouping, in order of preference: the browse config's groups (card.group),
    // the topic's mention_groups (card.group_key), then the Burroughs defaults.
    const chosen = browse?.groups?.length
      ? browse.groups.map(g => ({ ...g, match: (c: MentionCard) => c.group === g.key }))
      : groups && groups.length > 0
        ? groups.map(g => ({ ...g, match: (c: MentionCard) => c.group_key === g.key }))
        : GROUPS
    return chosen
      .map(g => ({ ...g, items: visible.filter(g.match) }))
      .filter(g => g.items.length > 0)
  }, [visible, browse, groups])

  // Counts per facet and lane over all cards, for the browse chips.
  const facetCount = useMemo(() => {
    const m = new Map<string, number>()
    for (const f of browse?.facets || []) {
      m.set(f.label, (cards || []).filter(c => hasFacet(c, f.label)).length)
    }
    return m
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cards, facetSpellings])
  const laneCount = useMemo(() => {
    const m = new Map<string, number>()
    for (const c of cards || []) m.set(c.lane, (m.get(c.lane) || 0) + 1)
    return m
  }, [cards])
  // Concept spelling -> facet label, so a card's tag can switch on its facet.
  const facetOf = useMemo(() => {
    const m = new Map<string, string>()
    for (const [label, spellings] of facetSpellings) for (const k of spellings) m.set(k, label)
    return m
  }, [facetSpellings])

  // A link to #card-ID (from search or another page) opens on that card. If a
  // filter would hide it, the filter is dropped first. #mentions opens on the
  // browse panel itself.
  useEffect(() => {
    if (hash === '#mentions' && cards?.length) {
      const t = window.setTimeout(
        () => document.getElementById('mentions')?.scrollIntoView({ block: 'start' }), 50)
      return () => window.clearTimeout(t)
    }
    const m = hash.match(/^#card-(.+)$/)
    if (!m || !cards?.length) return
    const id = decodeURIComponent(m[1])
    const target = cards.find(c => c.id === id)
    if (!target) return
    if ((facet && !hasFacet(target, facet)) || (lane && target.lane !== lane)) {
      setFilters({ facet: null, lane: null })
      return
    }
    const t = window.setTimeout(() => {
      const el = document.getElementById(`card-${id}`)
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' })
        el.classList.add('mention-card-flash')
        window.setTimeout(() => el.classList.remove('mention-card-flash'), 1600)
      }
    }, 50)
    return () => window.clearTimeout(t)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cards, facet, lane, hash])

  if (!cards || cards.length === 0) return null

  const activeFacet = browse?.facets.find(f => f.label === facet)

  return (
    <div className="detail-section" id="mentions">
      <h2>{heading || 'Every mention, one by one'}</h2>
      <p style={{ fontSize: '0.9rem', lineHeight: 1.65, color: 'var(--text-secondary)' }}>
        {browse?.intro
          ? browse.intro.replace('{n}', String(cards.length))
          : intro || `${cards.length} passages in the archive refer to Burroughs or to his word virus.
        Each card summarises the whole passage and where it sits in the work, then quotes
        the sentence it turns on. Quotations are verbatim, including the transcription
        irregularities of the source; every one is machine-checked against the underlying
        text before it is published. Open any card to read the passage it summarises, or
        follow the link to the full entry it was cut from.`}
      </p>

      {browse && (
        <div className="facet-panel">
          {browse.facet_kinds.map(fk => {
            const items = browse.facets.filter(f => f.kind === fk.kind && facetCount.get(f.label))
            if (items.length === 0) return null
            return (
              <div key={fk.kind} className="facet-row">
                <span className="facet-row-label">{fk.label}</span>
                <div className="facet-chips">
                  {items.map(f => (
                    <button
                      key={f.label}
                      className={`facet-chip${facet === f.label ? ' active' : ''}`}
                      aria-pressed={facet === f.label}
                      onClick={() => setFilter('facet', facet === f.label ? null : f.label)}
                    >
                      {f.label}
                      <span className="facet-chip-count">{facetCount.get(f.label)}</span>
                    </button>
                  ))}
                </div>
              </div>
            )
          })}
          <div className="facet-row">
            <span className="facet-row-label">Kind of source</span>
            <div className="facet-chips">
              {['A', 'B', 'E', 'C', 'D'].filter(l => laneCount.get(l)).map(l => (
                <button
                  key={l}
                  className={`facet-chip${lane === l ? ' active' : ''}`}
                  aria-pressed={lane === l}
                  onClick={() => setFilter('lane', lane === l ? null : l)}
                >
                  {LANE_LABELS[l]}
                  <span className="facet-chip-count">{laneCount.get(l)}</span>
                </button>
              ))}
            </div>
          </div>
          {(facet || lane) && (
            <p className="facet-status">
              Showing {visible.length} of {cards.length} passages
              {facet && <> on <strong>{facet}</strong></>}
              {lane && <> from <strong>{LANE_LABELS[lane]}</strong></>}.
              {activeFacet?.link && (
                <> <Link to={activeFacet.link}>{facet} elsewhere in the portal &rarr;</Link></>
              )}{' '}
              <button className="facet-clear" onClick={() => setFilters({ facet: null, lane: null })}>
                Clear filters
              </button>
            </p>
          )}
        </div>
      )}

      {grouped.map(group => (
        <div key={group.key} className="mention-group">
          <h3 className="mention-group-heading">
            {group.label}
            <span className="mention-group-count">{group.items.length}</span>
          </h3>
          <p className="mention-group-blurb">{group.blurb}</p>

          <div className="mention-cards">
            {group.items.map(card => {
              const noteOpen = openNote === card.id
              const passageOpen = openPassage.has(card.id)
              return (
                <div key={card.id} id={`card-${card.id}`} className="mention-card">
                  <div className="mention-card-head">
                    <LaneBadge lane={card.lane} />
                    <span className="mention-card-cite">{card.citation}</span>
                    {card.published_folio && (
                      <span className="mention-card-folio">[{card.published_folio}]</span>
                    )}
                    {card.dated && (
                      <span className="mention-card-date"
                            title={datingTitle(card.dating_basis)}>
                        {card.dated}
                      </span>
                    )}
                  </div>

                  <p className="mention-card-context">
                    {card.context}
                    {card.context_derived && (
                      <span className="mention-card-derived"
                            title="Summarised from the sweep, not editorially written">
                        {' '}· derived
                      </span>
                    )}
                  </p>

                  <blockquote className="mention-card-pith">
                    <p>{card.pith}</p>
                    <cite>&mdash; {card.speaker}</cite>
                  </blockquote>

                  {card.passage && (
                    <div className="mention-card-passage-wrap">
                      <button
                        className="mention-card-passage-toggle"
                        aria-expanded={passageOpen}
                        onClick={() => togglePassage(card.id)}
                      >
                        {passageOpen ? '▲ Hide the passage' : '▼ Read the passage'}
                      </button>
                      {passageOpen && (
                        <div className="mention-card-passage">{card.passage}</div>
                      )}
                    </div>
                  )}

                  <div className="mention-card-foot">
                    {card.concepts.slice(0, 5).map(t => {
                      const f = facetOf.get(t)
                      return f ? (
                        <button
                          key={t}
                          className={`entity-tag${facet === f ? ' entity-tag-active' : ''}`}
                          title={`Show every passage on ${f}`}
                          onClick={() => setFilter('facet', facet === f ? null : f)}
                        >
                          {t}
                        </button>
                      ) : (
                        <span key={t} className="entity-tag">
                          {t}
                        </span>
                      )
                    })}
                    {card.seg_id && (
                      <Link to={`/segments/${card.seg_id}`} className="mention-card-link">
                        Read the full entry &rarr;
                      </Link>
                    )}
                    {card.editorial_note && (
                      <button
                        className="mention-card-note-toggle"
                        onClick={() => setOpenNote(noteOpen ? null : card.id)}
                      >
                        {noteOpen ? 'Hide editorial note' : 'Editorial note'}
                      </button>
                    )}
                  </div>

                  {noteOpen && card.editorial_note && (
                    <p className="mention-card-note">{card.editorial_note}</p>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}

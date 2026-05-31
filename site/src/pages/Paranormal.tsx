import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'
import ExploreFooter from '../components/ExploreFooter'

export interface ParanormalEntry {
  id: string
  slug: string
  title: string
  category: string
  category_slug: string
  card_summary: string
  primary_quote: string
  primary_quote_line: string
  tags: string[]
  related_slugs: string[]
  full_essay: string
}

interface ParanormalIndex {
  total: number
  entries: ParanormalEntry[]
}

const CATEGORY_LABELS: Record<string, string> = {
  'soviet-psychotronic': 'Soviet Psychotronic',
  'kozyrev-time-energy': 'Kozyrev Time-Energy',
  'precognition': 'Precognition',
  'esp-telepathy': 'ESP & Telepathy',
  'valis-satellite': 'VALIS & Satellite',
  'anamnesis': 'Anamnesis',
  'second-sight': 'Second Sight & Prophecy',
  'spiritual-paranormal': 'Spiritual Paranormal',
  'mind-control': 'Mind Control & Subliminal',
}

const CATEGORY_COLORS: Record<string, string> = {
  'soviet-psychotronic': '#7a3c3c',
  'kozyrev-time-energy': '#3c5a7a',
  'precognition': '#5a3c7a',
  'esp-telepathy': '#3c7a5a',
  'valis-satellite': '#6b3500',
  'anamnesis': '#7a6030',
  'second-sight': '#4a5a3c',
  'spiritual-paranormal': '#3c4a6b',
  'mind-control': '#5a4a3c',
}

export default function Paranormal() {
  const { data, loading } = useData<ParanormalIndex>('paranormal/index.json')
  const [categoryFilter, setCategoryFilter] = useState('all')
  const [search, setSearch] = useState('')

  const categories = useMemo(() => {
    if (!data) return []
    const counts = new Map<string, number>()
    for (const e of data.entries) {
      counts.set(e.category_slug, (counts.get(e.category_slug) || 0) + 1)
    }
    return Array.from(counts.entries()).sort((a, b) => b[1] - a[1])
  }, [data])

  const filtered = useMemo(() => {
    if (!data) return []
    const q = search.toLowerCase()
    return data.entries.filter(e => {
      if (categoryFilter !== 'all' && e.category_slug !== categoryFilter) return false
      if (!q) return true
      return (
        e.title.toLowerCase().includes(q) ||
        e.card_summary.toLowerCase().includes(q) ||
        e.primary_quote.toLowerCase().includes(q) ||
        e.tags.some(t => t.toLowerCase().includes(q))
      )
    })
  }, [data, categoryFilter, search])

  if (loading || !data) return <div className="loading">Loading...</div>

  return (
    <>
      <div className="hero-header">
        <h1>PKD on the Paranormal</h1>
        <p className="hero-subtitle">
          Fifty topics from the <em>Exegesis</em> in which Philip K. Dick seriously entertained
          paranormal explanations for his 2–3 February/March 1974 experiences — Soviet psychotronic weapons,
          Kozyrev's time-energy telepathy, precognition, ESP, VALIS, and more.
          Every entry is grounded in verbatim citation from the primary text.
        </p>
      </div>

      <div className="detail-section">
        <p>
          Dick never settled on one framework. He cycles through Soviet microwave beaming,
          Nikolai Kozyrev's time-energy telepathy theory, chronic precognition, anamnesis triggered
          by a transpersonal entity, VALIS as an orbiting intelligence, and many others —
          sometimes holding several simultaneously. This catalog maps that oscillation without
          adjudicating it. The paranormal is not contrasted here with the religious: Dick's
          frameworks constantly interpenetrate.
        </p>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
          All quotations drawn from <code>exegesis_ordered.txt</code> (the chronologically sorted full
          text). Line numbers refer to that file. Editorial method documented in{' '}
          <code>PARANORMAL_STYLE_GUIDE.md</code>.
        </p>
      </div>

      <div className="sidebar-layout">
        <div className="sidebar">
          <h3>Category</h3>
          <ul>
            <li>
              <a
                href="#"
                className={categoryFilter === 'all' ? 'active' : ''}
                onClick={e => { e.preventDefault(); setCategoryFilter('all') }}
              >
                All categories
                <span style={{ float: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                  {data.total}
                </span>
              </a>
            </li>
            {categories.map(([slug, count]) => (
              <li key={slug}>
                <a
                  href="#"
                  className={categoryFilter === slug ? 'active' : ''}
                  onClick={e => { e.preventDefault(); setCategoryFilter(slug) }}
                >
                  {CATEGORY_LABELS[slug] || slug}
                  <span style={{ float: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                    {count}
                  </span>
                </a>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <div className="toolbar-row">
            <input
              className="search-input"
              type="text"
              placeholder="Search topics, summaries, or quotes…"
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
              {filtered.length} of {data.total}
            </span>
          </div>

          <div className="card-grid">
            {filtered.map(entry => {
              const color = CATEGORY_COLORS[entry.category_slug] || 'var(--accent)'
              return (
                <div key={entry.id} className="card">
                  <div style={{ marginBottom: '0.35rem' }}>
                    <span style={{
                      fontSize: '0.7rem',
                      padding: '0.15rem 0.45rem',
                      background: color,
                      color: '#fff',
                      borderRadius: '3px',
                      textTransform: 'uppercase',
                      letterSpacing: '0.04em',
                    }}>
                      {CATEGORY_LABELS[entry.category_slug] || entry.category}
                    </span>
                  </div>
                  <h3>
                    <Link to={`/paranormal/${entry.slug}`}>{entry.title}</Link>
                  </h3>
                  <p style={{ marginTop: '0.4rem' }}>{entry.card_summary}</p>
                  {entry.primary_quote && (
                    <blockquote style={{
                      borderLeft: '2px solid var(--border)',
                      paddingLeft: '0.75rem',
                      margin: '0.75rem 0 0',
                      fontSize: '0.82rem',
                      color: 'var(--text-secondary)',
                      fontStyle: 'italic',
                    }}>
                      "{entry.primary_quote.length > 160
                        ? entry.primary_quote.slice(0, 157) + '…'
                        : entry.primary_quote}"
                    </blockquote>
                  )}
                  {entry.tags.length > 0 && (
                    <div className="card-meta" style={{ marginTop: '0.65rem' }}>
                      {entry.tags.slice(0, 3).map(tag => (
                        <span key={tag} className="badge badge-background">{tag}</span>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </div>

      <ExploreFooter groups={[
        {
          section: 'Related sections', items: [
            { label: 'Theophanies & Visionary Experiences', to: '/theophanies' },
            { label: 'The Exegesis landing', to: '/exegesis' },
            { label: 'Dictionary of PKD terms', to: '/dictionary' },
          ],
        },
        {
          section: 'Key people', items: [
            { label: 'People in the Exegesis', to: '/people' },
            { label: 'PKD scholars', to: '/scholars' },
          ],
        },
        {
          section: 'Timeline', items: [
            { label: '1974 (the year of 2-3-74)', to: '/timeline/1974' },
            { label: '1975', to: '/timeline/1975' },
            { label: '1980 (late Exegesis)', to: '/timeline/1980' },
          ],
        },
      ]} />
    </>
  )
}

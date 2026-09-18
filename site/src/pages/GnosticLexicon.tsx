import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface Exemplar {
  corpus: string
  lane: string
  source_id: string
  doc_id: string | null
  slug: string | null
  title: string | null
  date_display: string | null
  matched: string
  passage: string
}

interface Attestations {
  total: number
  pkd_text: number
  editor_annotation: number
  exegesis: number
  letters: number
  valis_trilogy: number
  scholarship: number
}

interface RegisterEntry {
  entry_id: string
  label: string
  slug: string
  category: string
  tradition: string
  greek: string | null
  gloss: string
  why_pkd: string
  key_sources: string[]
  status: 'attested' | 'annotation_only' | 'unattested'
  attestations: Attestations
  first_attested: string | null
  last_attested: string | null
  peak_year: string | null
  by_year: Record<string, number>
  by_year_rate: Record<string, number>
  exemplars: Exemplar[]
}

interface Register {
  entry_count: number
  by_category: Record<string, number>
  by_status: Record<string, number>
  corpus_coverage: Record<string, number>
  exegesis_folder_sizes: Record<string, number>
  chronology_caveat: string
  entries: RegisterEntry[]
}

const CATEGORY_LABEL: Record<string, string> = {
  concept: 'Concepts',
  teacher: 'Teachers & figures',
  heresiologist: 'Heresiologists & philosophers',
  text: 'Texts',
  scholar: 'Modern scholars',
  tradition: 'Traditions',
  pkd_coinage: "Dick's own coinages",
}

const STATUS_LABEL: Record<string, string> = {
  attested: 'In his own words',
  annotation_only: 'Editor annotation only',
  unattested: 'Never named',
}

const STATUS_CLASS: Record<string, string> = {
  attested: 'badge-accepted',
  annotation_only: 'badge-provisional',
  unattested: 'badge-background',
}

// Exegesis segments are addressed by seg_id; archive documents by slug.
// Anything else (chapter text files, letters) has no route and stays plain text.
function citeLink(x: Exemplar) {
  if (x.corpus === 'exegesis') {
    return <Link to={`/segments/${x.source_id}`}>{x.title || x.source_id}</Link>
  }
  if (x.corpus === 'scholarship' && x.slug) {
    return <Link to={`/archive/${x.slug}`}>{x.title || x.source_id}</Link>
  }
  return <>{x.title || x.source_id}</>
}

export default function GnosticLexicon() {
  const { data, loading, error } = useData<Register>('studies/gnosticism/register.json')
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('all')
  const [status, setStatus] = useState('all')
  const [sortBy, setSortBy] = useState('attestations')
  const [open, setOpen] = useState<string | null>(null)

  const categories = useMemo(() => {
    if (!data) return []
    return ['all', ...Object.keys(data.by_category).sort(
      (a, b) => (CATEGORY_LABEL[a] || a).localeCompare(CATEGORY_LABEL[b] || b))]
  }, [data])

  const filtered = useMemo(() => {
    if (!data) return []
    let rows = data.entries
    if (category !== 'all') rows = rows.filter(e => e.category === category)
    if (status !== 'all') rows = rows.filter(e => e.status === status)
    if (search) {
      const q = search.toLowerCase()
      rows = rows.filter(e =>
        e.label.toLowerCase().includes(q) ||
        e.gloss.toLowerCase().includes(q) ||
        e.tradition.toLowerCase().includes(q) ||
        e.key_sources.some(s => s.toLowerCase().includes(q)))
    }
    return [...rows].sort((a, b) => {
      if (sortBy === 'name') return a.label.localeCompare(b.label)
      if (sortBy === 'first') {
        return (a.first_attested || '9999').localeCompare(b.first_attested || '9999')
          || a.label.localeCompare(b.label)
      }
      if (sortBy === 'category') {
        return a.category.localeCompare(b.category) || a.label.localeCompare(b.label)
      }
      return b.attestations.pkd_text - a.attestations.pkd_text
        || a.label.localeCompare(b.label)
    })
  }, [data, search, category, status, sortBy])

  if (loading) return <div className="loading">Loading...</div>
  if (error || !data) return <div className="no-results">Could not load the register: {error}</div>

  return (
    <>
      <div className="page-header">
        <h1>The Gnostic Lexicon</h1>
        <p>
          Every Gnostic term, teacher, text, tradition and modern scholar this portal
          tracks across Philip K. Dick's Exegesis, correspondence and VALIS trilogy —
          with the evidence for each. {data.entry_count} entries, {filtered.length} shown.
        </p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{data.by_status.attested ?? 0}</div>
          <div className="stat-label">Attested in his own words</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.by_status.annotation_only ?? 0}</div>
          <div className="stat-label">Editor annotation only</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.by_status.unattested ?? 0}</div>
          <div className="stat-label">Never named by Dick</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.corpus_coverage.exegesis ?? 0}</div>
          <div className="stat-label">Exegesis segments swept</div>
        </div>
      </div>

      <p className="gl-caveat">
        An entry Dick never used is kept here, not dropped: <em>“he did not reach for
        this word”</em> is a finding about Dick, and this register is the only place it
        is recorded. Counts are raw occurrences and measure vocabulary, not importance.
        {' '}<Link to="/studies/gnosticism">Read the study →</Link>
      </p>

      <div className="sidebar-layout">
        <div className="sidebar">
          <h3>Categories</h3>
          <ul>
            {categories.map(c => (
              <li key={c}>
                <a
                  href="#"
                  className={category === c ? 'active' : ''}
                  onClick={e => { e.preventDefault(); setCategory(c) }}
                >
                  {c === 'all' ? 'All' : (CATEGORY_LABEL[c] || c)}
                  {c !== 'all' && (
                    <span style={{ opacity: 0.5, marginLeft: '0.25rem' }}>
                      ({data.by_category[c]})
                    </span>
                  )}
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
              placeholder="Search terms, glosses, sources..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <select className="filter-select" value={status}
                    onChange={e => setStatus(e.target.value)}>
              <option value="all">All evidence states</option>
              <option value="attested">In his own words</option>
              <option value="annotation_only">Editor annotation only</option>
              <option value="unattested">Never named</option>
            </select>
            <select className="filter-select" value={sortBy}
                    onChange={e => setSortBy(e.target.value)}>
              <option value="attestations">Sort: most used</option>
              <option value="name">Sort: A–Z</option>
              <option value="first">Sort: first attested</option>
              <option value="category">Sort: category</option>
            </select>
          </div>

          {filtered.length === 0 && <div className="no-results">No entries match.</div>}

          <table className="catalog-table gl-table">
            <thead>
              <tr>
                <th>Term</th>
                <th>Tradition</th>
                <th style={{ textAlign: 'right' }}>In his words</th>
                <th>Years</th>
                <th>Evidence</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(e => {
                const isOpen = open === e.entry_id
                return [
                  <tr
                    key={e.entry_id}
                    className={'gl-row' + (isOpen ? ' gl-row-open' : '')}
                    onClick={() => setOpen(isOpen ? null : e.entry_id)}
                  >
                    <td>
                      <span className="gl-caret">{isOpen ? '▾' : '▸'}</span>
                      <strong>{e.label}</strong>
                      {e.greek && <span className="gl-greek"> {e.greek}</span>}
                      <div className="gl-cat">{CATEGORY_LABEL[e.category] || e.category}</div>
                    </td>
                    <td>{e.tradition}</td>
                    <td style={{ textAlign: 'right' }}>
                      <strong>{e.attestations.pkd_text.toLocaleString()}</strong>
                      {e.attestations.editor_annotation > 0 && (
                        <div className="gl-sub">
                          +{e.attestations.editor_annotation.toLocaleString()} annot.
                        </div>
                      )}
                    </td>
                    <td>
                      {e.first_attested
                        ? (e.first_attested === e.last_attested
                            ? e.first_attested
                            : `${e.first_attested}–${e.last_attested}`)
                        : <span className="gl-sub">—</span>}
                    </td>
                    <td>
                      <span className={'badge ' + STATUS_CLASS[e.status]}>
                        {STATUS_LABEL[e.status]}
                      </span>
                    </td>
                  </tr>,
                  isOpen && (
                    <tr key={e.entry_id + '-detail'} className="gl-detail-row">
                      <td colSpan={5}>
                        <div className="gl-detail">
                          <p className="gl-gloss">{e.gloss}</p>
                          <p className="gl-why"><strong>In Dick:</strong> {e.why_pkd}</p>

                          {e.key_sources.length > 0 && (
                            <p className="gl-sources">
                              <strong>Sources:</strong> {e.key_sources.join(' · ')}
                            </p>
                          )}

                          {Object.keys(e.by_year_rate).length > 0 && (
                            <div className="gl-years">
                              <strong>Exegesis rate</strong>
                              <span className="gl-sub"> (hits per segment, by folder)</span>
                              <div className="gl-year-row">
                                {Object.entries(e.by_year_rate).map(([y, rate]) => (
                                  <span key={y} className="gl-year">
                                    <span className="gl-year-label">{y}</span>
                                    <span className="gl-year-val">{rate}</span>
                                    <span className="gl-sub">{e.by_year[y]} hits</span>
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          <div className="gl-corpora">
                            {([
                              ['Exegesis', e.attestations.exegesis],
                              ['VALIS trilogy', e.attestations.valis_trilogy],
                              ['Letters', e.attestations.letters],
                              ['Scholarship', e.attestations.scholarship],
                            ] as [string, number][]).filter(([, n]) => n > 0)
                              .map(([label, n]) => (
                                <span key={label} className="gl-chip">
                                  {label}: <strong>{n.toLocaleString()}</strong>
                                </span>
                              ))}
                          </div>

                          {e.exemplars.length > 0 ? (
                            <div className="gl-exemplars">
                              <strong>Attestations</strong>
                              {e.exemplars.map((x, i) => (
                                <blockquote key={i} className="gl-quote">
                                  <span className={'lane-badge lane-' + x.lane.toLowerCase()}>
                                    {x.lane}
                                  </span>
                                  <span className="gl-quote-text">{x.passage}</span>
                                  <cite>
                                    {citeLink(x)}
                                    {x.date_display ? ` — ${x.date_display}` : ''}
                                  </cite>
                                </blockquote>
                              ))}
                            </div>
                          ) : (
                            <p className="gl-none">
                              No occurrence anywhere in the corpus swept.
                            </p>
                          )}
                        </div>
                      </td>
                    </tr>
                  ),
                ]
              })}
            </tbody>
          </table>
        </div>
      </div>

      <p className="gl-caveat gl-footnote">{data.chronology_caveat}</p>
    </>
  )
}

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface WorkEntry {
  work_id: string
  canonical_title: string
  slug: string
  author: string
  work_type: string
  category: string
  date_display: string
  date_start: string
  card_summary: string
  page_count: number
  source_count: number
  themes?: string[]
  related_docs: { doc_id: string; title: string; slug: string; date_display: string; doc_type: string }[]
  first_doc?: { doc_id: string; slug: string; title: string }
}

interface ThemeIndex {
  theme_count: number
  fiction_work_count: number
  themes: {
    theme_id: string
    slug: string
    label: string
    description: string
    work_count: number
  }[]
}

const WORK_TYPE_LABELS: Record<string, string> = {
  novels: 'Novel',
  novellas: 'Novella',
  letters: 'Letter',
  short_stories: 'Short story',
  essays: 'Essay',
  interviews: 'Interview',
  biographies: 'Biography',
  fan_publications: 'Fan publication',
  newspaper: 'Newspaper',
  archive_pdf: 'Archive item',
  primary: 'Primary text',
}

const CATEGORY_LABELS: Record<string, string> = {
  interviews: 'Interviews',
  letters: 'Letters',
  newspaper: 'Newspaper',
  novels: 'Novels',
  primary: 'Primary texts',
  short_stories: 'Short stories',
}

export default function Works() {
  const { data: works, loading } = useData<WorkEntry[]>('works/index.json')
  const { data: themeIndex } = useData<ThemeIndex>('themes/index.json')
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('all')
  const [workType, setWorkType] = useState('all')
  const [theme, setTheme] = useState('all')
  const [sortBy, setSortBy] = useState('date')

  const themeOptions = useMemo(() => {
    return [...(themeIndex?.themes || [])].sort((a, b) => b.work_count - a.work_count || a.label.localeCompare(b.label))
  }, [themeIndex])

  const themeMap = useMemo(() => {
    const map = new Map<string, ThemeIndex['themes'][number]>()
    for (const t of themeOptions) map.set(t.slug, t)
    return map
  }, [themeOptions])

  const filtered = useMemo(() => {
    if (!works) return []
    let result = works
    if (category !== 'all') result = result.filter(entry => entry.category === category)
    if (workType !== 'all') result = result.filter(entry => entry.work_type === workType)
    if (theme !== 'all') result = result.filter(entry => (entry.themes || []).includes(theme))
    if (search) {
      const q = search.toLowerCase()
      result = result.filter(entry =>
        entry.canonical_title.toLowerCase().includes(q) ||
        entry.author.toLowerCase().includes(q) ||
        (entry.card_summary || '').toLowerCase().includes(q) ||
        (entry.themes || []).some(slug => (themeMap.get(slug)?.label || slug).toLowerCase().includes(q))
      )
    }
    return [...result].sort((a, b) => {
      if (sortBy === 'title') return a.canonical_title.localeCompare(b.canonical_title)
      if (sortBy === 'type') return a.work_type.localeCompare(b.work_type) || a.canonical_title.localeCompare(b.canonical_title)
      if (sortBy === 'pages') return (b.page_count || 0) - (a.page_count || 0) || a.canonical_title.localeCompare(b.canonical_title)
      if (sortBy === 'popularity') return (b.source_count || 0) - (a.source_count || 0) || a.canonical_title.localeCompare(b.canonical_title)
      return (b.date_start || '').localeCompare(a.date_start || '') || a.canonical_title.localeCompare(b.canonical_title)
    })
  }, [works, search, category, workType, theme, sortBy, themeMap])

  const categories = useMemo(() => {
    if (!works) return []
    return ['all', ...Array.from(new Set(works.map(entry => entry.category))).sort()]
  }, [works])

  const workTypes = useMemo(() => {
    if (!works) return []
    return ['all', ...Array.from(new Set(works.map(entry => entry.work_type))).sort()]
  }, [works])

  if (loading || !themeIndex) return <div className="loading">Loading works...</div>

  return (
    <>
      <div className="page-header">
        <h1>PKD Works</h1>
        <p>{filtered.length} canonical PKD works shown from the separate works table</p>
      </div>

      <div className="sidebar-layout">
        <div className="sidebar">
          <h3>Category</h3>
          <ul>
          {categories.map(c => (
            <li key={c}>
              <a href="#" className={category === c ? 'active' : ''} onClick={e => { e.preventDefault(); setCategory(c) }}>
                  {c === 'all' ? 'All Categories' : CATEGORY_LABELS[c] || c}
              </a>
            </li>
          ))}
          </ul>

          <h3 style={{ marginTop: '1.5rem' }}>Type</h3>
          <ul>
            {workTypes.map(t => (
              <li key={t}>
                <a href="#" className={workType === t ? 'active' : ''} onClick={e => { e.preventDefault(); setWorkType(t) }}>
                  {t === 'all' ? 'All Types' : WORK_TYPE_LABELS[t] || t}
                </a>
              </li>
            ))}
          </ul>

          <h3 style={{ marginTop: '1.5rem' }}>Theme</h3>
          <ul>
            <li>
              <a href="#" className={theme === 'all' ? 'active' : ''} onClick={e => { e.preventDefault(); setTheme('all') }}>
                All Themes
              </a>
            </li>
            {themeOptions.map(t => (
              <li key={t.slug}>
                <a href="#" className={theme === t.slug ? 'active' : ''} onClick={e => { e.preventDefault(); setTheme(t.slug) }}>
                  {t.label}
                  <span style={{ float: 'right', color: 'var(--text-muted)', fontSize: '0.8rem' }}>{t.work_count}</span>
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
              placeholder="Search canonical works..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <select className="filter-select" value={sortBy} onChange={e => setSortBy(e.target.value)} aria-label="Sort works">
              <option value="date">Newest First</option>
              <option value="title">Title</option>
              <option value="type">Type</option>
              <option value="pages">Page Count</option>
              <option value="popularity">Most Linked</option>
            </select>
          </div>

          <div className="card-grid">
            {filtered.map(work => (
              <div key={work.work_id} className="card">
                <h3>
                  <Link to={`/works/${work.slug}`}>{work.canonical_title}</Link>
                </h3>
                <div className="card-meta">
                  {work.date_display && <span>{work.date_display}</span>}
                  {work.page_count > 0 && <span>{work.page_count} pp</span>}
                  <span className="badge badge-category">{CATEGORY_LABELS[work.category] || work.category}</span>
                  <span>{WORK_TYPE_LABELS[work.work_type] || work.work_type}</span>
                  <span>{work.source_count} doc{work.source_count === 1 ? '' : 's'}</span>
                </div>
                <p style={{ marginTop: '0.5rem' }}>{work.card_summary}</p>
                {(work.themes || []).length > 0 && (
                  <div className="card-meta" style={{ marginTop: '0.75rem', gap: '0.35rem', flexWrap: 'wrap' }}>
                    {(work.themes || []).slice(0, 5).map(slug => (
                      <Link key={slug} to={`/themes/${slug}`} className="entity-linked">
                        {themeMap.get(slug)?.label || slug.replace(/-/g, ' ')}
                      </Link>
                    ))}
                  </div>
                )}
                {work.category === 'novels' && (
                  <p style={{ marginTop: '0.75rem' }}>
                    <Link to={`/pkd-on-pkd/${work.slug}`}>PKD on PKD</Link>
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}

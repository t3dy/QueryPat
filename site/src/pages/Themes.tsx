import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface ThemeWork {
  work_id: string
  canonical_title: string
  slug: string
  category: string
  work_type: string
  date_display: string | null
}

interface ThemeEntry {
  theme_id: string
  slug: string
  label: string
  description: string
  work_count: number
  works: ThemeWork[]
}

interface ThemeIndex {
  theme_count: number
  fiction_work_count: number
  themes: ThemeEntry[]
}

export default function Themes() {
  const { data: themeIndex, loading } = useData<ThemeIndex>('themes/index.json')
  const [search, setSearch] = useState('')

  const filtered = useMemo(() => {
    if (!themeIndex) return []
    let themes = [...themeIndex.themes]
    if (search) {
      const q = search.toLowerCase()
      themes = themes.filter(theme =>
        theme.label.toLowerCase().includes(q) ||
        (theme.description || '').toLowerCase().includes(q) ||
        theme.works.some(work => work.canonical_title.toLowerCase().includes(q))
      )
    }
    return themes.sort((a, b) => b.work_count - a.work_count || a.label.localeCompare(b.label))
  }, [themeIndex, search])

  if (loading) return <div className="loading">Loading themes...</div>
  if (!themeIndex) return <div className="loading">Themes not found.</div>

  return (
    <>
      <div className="page-header">
        <h1>Themes &amp; Topics</h1>
        <p>
          {themeIndex.theme_count} controlled themes across {themeIndex.fiction_work_count} fiction works.
        </p>
      </div>

      <input
        className="search-input"
        type="text"
        placeholder="Search themes or works..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />

      <div className="card-grid" style={{ marginTop: '1rem' }}>
        {filtered.map(theme => (
          <div key={theme.theme_id} className="card">
            <h3>
              <Link to={`/themes/${theme.slug}`}>{theme.label}</Link>
            </h3>
            <div className="card-meta">
              <span>{theme.work_count} work{theme.work_count === 1 ? '' : 's'}</span>
            </div>
            <p style={{ marginTop: '0.5rem' }}>{theme.description}</p>
            {theme.works.length > 0 && (
              <div className="card-meta" style={{ marginTop: '0.75rem', gap: '0.35rem', flexWrap: 'wrap' }}>
                {theme.works.slice(0, 5).map(work => (
                  <Link key={work.work_id} to={`/works/${work.slug}`} className="entity-linked">
                    {work.canonical_title}
                  </Link>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '3rem' }}>
          No themes match the current filter.
        </p>
      )}
    </>
  )
}

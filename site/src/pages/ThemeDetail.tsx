import { Link, useParams } from 'react-router-dom'
import { useEffect, useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'
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

export default function ThemeDetail() {
  const { slug } = useParams()
  const { data: themeIndex, loading } = useData<ThemeIndex>('themes/index.json')
  const [body, setBody] = useState<string | null>(null)
  const [bodyError, setBodyError] = useState<string | null>(null)
  const BASE = import.meta.env.BASE_URL + 'data/'

  const theme = useMemo(
    () => themeIndex?.themes.find(entry => entry.slug === slug),
    [themeIndex, slug]
  )

  useEffect(() => {
    if (!slug) return
    setBody(null)
    setBodyError(null)
    fetch(`${BASE}themes/essays/${slug}.md`)
      .then(r => {
        if (!r.ok) throw new Error(`Theme essay not found (${r.status})`)
        return r.text()
      })
      .then(setBody)
      .catch(e => setBodyError(e.message))
  }, [slug])

  if (loading) return <div className="loading">Loading...</div>
  if (!themeIndex || !theme) {
    return (
      <div className="page-header">
        <h1>Theme Not Found</h1>
        <Link to="/themes">Back to Themes</Link>
      </div>
    )
  }

  if (bodyError) {
    return (
      <div className="detail-section">
        <p>Could not load theme essay: {bodyError}</p>
        <p><Link to="/themes">&larr; Back to all themes</Link></p>
      </div>
    )
  }

  if (!body) return <div className="loading">Loading...</div>

  return (
    <>
      <div className="page-header">
        <h1>{theme.label}</h1>
        <p>{theme.work_count} fiction works tagged with this theme</p>
      </div>

      <article className="essay-body detail-section" style={{ maxWidth: 'none' }}>
        <ReactMarkdown
          components={{
            a: ({ href, children, ...props }) => {
              if (href && href.startsWith('/')) {
                return <Link to={href}>{children}</Link>
              }
              return <a href={href} target="_blank" rel="noreferrer" {...props}>{children}</a>
            },
          }}
        >
          {body}
        </ReactMarkdown>
      </article>

      <div className="detail-section">
        <h2>Tagged Works</h2>
        <div className="card-grid">
          {theme.works.map(work => (
            <div key={work.work_id} className="card">
              <h3>
                <Link to={`/works/${work.slug}`}>{work.canonical_title}</Link>
              </h3>
              <div className="card-meta">
                {work.date_display && <span>{work.date_display}</span>}
                <span className="badge badge-category">{work.category}</span>
                <span>{work.work_type.replace(/_/g, ' ')}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--border-light)' }}>
        <Link to="/themes">Back to Themes</Link>
      </div>
    </>
  )
}

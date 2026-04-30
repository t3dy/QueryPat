import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { useData } from '../hooks/useData'

interface EssayMeta {
  slug: string
  title: string
  subtitle: string
  topic: string
  word_count: number
  primary_lanes: string[]
  key_sources: string[]
  date_drafted: string
}

interface EssayIndex {
  essays: EssayMeta[]
}

const BASE = import.meta.env.BASE_URL + 'data/'

export default function EssayDetail() {
  const { slug } = useParams()
  const { data: index } = useData<EssayIndex>('essays/index.json')
  const [body, setBody] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!slug) return
    setBody(null)
    setError(null)
    fetch(`${BASE}essays/${slug}.md`)
      .then(r => {
        if (!r.ok) throw new Error(`Essay not found (${r.status})`)
        return r.text()
      })
      .then(setBody)
      .catch(e => setError(e.message))
  }, [slug])

  const meta = index?.essays.find(e => e.slug === slug)

  if (error) {
    return (
      <div className="detail-section">
        <p>Could not load essay: {error}</p>
        <p><Link to="/essays">&larr; Back to all essays</Link></p>
      </div>
    )
  }

  if (!body) return <div className="loading">Loading...</div>

  return (
    <article className="essay-body">
      {meta && (
        <div style={{marginBottom:'1.5rem', paddingBottom:'1rem', borderBottom:'1px solid var(--border, rgba(0,0,0,0.1))', fontSize:'0.85rem', color:'var(--text-muted)'}}>
          <div>
            <strong>Lanes:</strong> {meta.primary_lanes.join(', ')}
            <span style={{margin:'0 0.5rem'}}>&middot;</span>
            <strong>Words:</strong> {meta.word_count.toLocaleString()}
            <span style={{margin:'0 0.5rem'}}>&middot;</span>
            <strong>Drafted:</strong> {meta.date_drafted}
          </div>
        </div>
      )}
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
      <div style={{marginTop:'2rem', paddingTop:'1rem', borderTop:'1px solid var(--border, rgba(0,0,0,0.1))'}}>
        <Link to="/essays">&larr; All essays</Link>
      </div>
    </article>
  )
}

import { Link, useParams } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { useData } from '../hooks/useData'

interface Mention {
  entry_id: string
  folder_page: string
  date_range: string
  summary: string
  quotes: string[]
  claims: string[]
  gloss: string
}

interface WorkDoc {
  slug: string
  title: string
  work_link: string | null
  mention_count: number
  date_range: string
  intro: string
  theological_synthesis: string
  mentions: Mention[]
  see_also: { essays: string[]; themes: string[]; dictionary: string[] }
}

const mdComponents = {
  a: ({ href, children, ...props }: { href?: string; children?: React.ReactNode }) => {
    if (href && href.startsWith('/')) return <Link to={href}>{children}</Link>
    return <a href={href} target="_blank" rel="noreferrer" {...props}>{children}</a>
  },
}

function labelFromPath(p: string): string {
  const seg = p.split('/').filter(Boolean).pop() || p
  return seg.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

export default function ExegesisWorkDetail() {
  const { slug } = useParams()
  const { data, loading, error } = useData<WorkDoc>(slug ? `exegesis/works/${slug}.json` : null)

  if (loading) return <div className="loading">Loading&hellip;</div>
  if (error || !data) {
    return (
      <div className="detail-section">
        <p>Could not load this work: {error || 'not found'}.</p>
        <p><Link to="/exegesis/works">&larr; All works in the Exegesis</Link></p>
      </div>
    )
  }

  const seeAll = [
    ...(data.see_also?.essays || []),
    ...(data.see_also?.themes || []),
    ...(data.see_also?.dictionary || []),
  ]

  return (
    <>
      <div className="page-header">
        <h1>{data.title} in the <em>Exegesis</em></h1>
        <p>
          {data.mention_count} mention{data.mention_count !== 1 ? 's' : ''} &middot; {data.date_range}
          {data.work_link && (
            <> &middot; <Link to={data.work_link}>the novel &rarr;</Link></>
          )}
        </p>
      </div>

      {data.intro && (
        <article className="essay-body detail-section" style={{ maxWidth: 'none' }}>
          <ReactMarkdown components={mdComponents}>{data.intro}</ReactMarkdown>
        </article>
      )}

      {data.theological_synthesis && (
        <div className="detail-section">
          <h2>The theological reading</h2>
          <article className="essay-body" style={{ maxWidth: 'none' }}>
            <ReactMarkdown components={mdComponents}>{data.theological_synthesis}</ReactMarkdown>
          </article>
        </div>
      )}

      <div className="detail-section">
        <h2>Every mention</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: 0 }}>
          Each passage where PKD discusses <em>{data.title}</em>, in manuscript order. The quoted block is his own
          <em> Exegesis</em> text (Lane B); the note beneath it reads the passage.
        </p>

        {data.mentions.map(m => (
          <div
            key={m.entry_id}
            className="card"
            style={{ borderLeft: '4px solid var(--accent)', marginBottom: '1rem' }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: '1rem' }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--accent)' }}>
                {m.folder_page}
              </span>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{m.date_range}</span>
            </div>

            <blockquote
              style={{
                borderLeft: '2px solid var(--border-light)',
                padding: '0 0.9rem',
                margin: '0.6rem 0',
                color: 'var(--text-secondary)',
                fontSize: '0.9rem',
                lineHeight: 1.6,
              }}
            >
              <ReactMarkdown components={mdComponents}>{m.summary}</ReactMarkdown>
            </blockquote>

            {m.gloss ? (
              <div className="essay-body" style={{ maxWidth: 'none', fontSize: '0.95rem' }}>
                <ReactMarkdown components={mdComponents}>{m.gloss}</ReactMarkdown>
              </div>
            ) : (
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontStyle: 'italic', margin: '0.3rem 0 0' }}>
                Analysis pending.
              </p>
            )}

            {m.claims && m.claims.length > 0 && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.6rem' }}>
                {m.claims.map((c, i) => (
                  <span
                    key={i}
                    className="badge"
                    style={{ background: 'var(--bg-secondary)', color: 'var(--text-secondary)', border: '1px solid var(--border-light)', fontSize: '0.7rem' }}
                  >
                    {c}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {seeAll.length > 0 && (
        <div className="detail-section">
          <h2>See also</h2>
          <ul>
            {seeAll.map(p => (
              <li key={p}><Link to={p}>{labelFromPath(p)}</Link></li>
            ))}
          </ul>
        </div>
      )}

      <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--border-light)' }}>
        <Link to="/exegesis/works">&larr; All works in the Exegesis</Link>
      </div>
    </>
  )
}

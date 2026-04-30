import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface Analytics {
  totals: {
    documents: number
    segments: number
    terms_public: number
    terms_total: number
    evidence_packets: number
    archive_docs: number
    timeline_events: number
    names: number
  }
  top_terms: { name: string; count: number; category: string }[]
  segments_per_year: { year: string; count: number; bio_events?: number; has_content?: boolean }[]
}

interface BiographyIndex {
  total: number
}

interface Scholar {
  slug?: string
}

export default function Dashboard() {
  const { data, loading } = useData<Analytics>('analytics.json')
  const { data: bio } = useData<BiographyIndex>('biography/index.json')
  const { data: scholars } = useData<Scholar[]>('scholars.json')

  if (loading || !data) return <div className="loading">Loading...</div>

  const t = data.totals
  const bioCount = bio?.total ?? 646
  const scholarCount = scholars?.length ?? 119

  return (
    <>
      <div className="hero-header">
        <h1>Philip K. Dick Knowledge Portal</h1>
        <p className="hero-subtitle">
          A scholarly portal on Philip K. Dick (1928&ndash;1982): his fiction, his life, the
          {' '}<em>Exegesis</em>, and the scholarship around him.
        </p>
      </div>

      <div className="detail-section">
        <p>
          Philip K. Dick was an American science fiction novelist whose work moved from pulp magazines in the 1950s
          to the Library of America in the 21st century. Across forty-four novels and over a hundred short stories
          he wrote about counterfeit realities, drugs and altered states, theology, paranoia, and the unreliability of
          self. From February 1974 until his death in March 1982 he kept a private theological journal &mdash; the
          {' '}<em>Exegesis</em> &mdash; running to roughly 8,000 manuscript pages.
        </p>
        <p>
          This portal integrates biography, fiction, the <em>Exegesis</em>, letters and interviews, scholarly monographs
          and articles, and fan publications into one site. Every claim is sourced to an
          {' '}<Link to="/archive">evidentiary lane</Link>; interpretations are attributed to whoever holds them; and
          contradictions across sources are surfaced rather than silently adjudicated. Start anywhere &mdash; the entries
          cross-link to each other.
        </p>
      </div>

      <div className="stats-grid">
        <Link to="/biography" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{bioCount.toLocaleString()}</div>
          <div className="stat-label">Biography events</div>
        </Link>
        <Link to="/exegesis" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{t.segments.toLocaleString()}</div>
          <div className="stat-label"><em>Exegesis</em> segments</div>
        </Link>
        <Link to="/archive" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{t.archive_docs.toLocaleString()}</div>
          <div className="stat-label">Archive documents</div>
        </Link>
        <Link to="/names" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{(t.names ?? 592).toLocaleString()}</div>
          <div className="stat-label">Names &amp; characters</div>
        </Link>
        <Link to="/dictionary" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{t.terms_public.toLocaleString()}</div>
          <div className="stat-label">Dictionary terms</div>
        </Link>
        <Link to="/scholars" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{scholarCount.toLocaleString()}</div>
          <div className="stat-label">Scholar profiles</div>
        </Link>
      </div>

      <div className="detail-section" style={{marginTop:'1rem'}}>
        <h2>What's inside</h2>
        <ul style={{lineHeight:'1.7'}}>
          <li>
            <strong><Link to="/biography">Biography</Link></strong> &mdash; 646 life events with location, era, category,
            and reliability tier, drawn from the major biographies and primary sources.
          </li>
          <li>
            <strong><Link to="/timeline">Timeline</Link></strong> &mdash; chronological viewer for <em>Exegesis</em> segments
            and biography events together.
          </li>
          <li>
            <strong><Link to="/exegesis">The <em>Exegesis</em></Link></strong> &mdash; PKD's theological journal (1974&ndash;1982)
            with parsed segment summaries, recurring vocabulary, and editorial context.
          </li>
          <li>
            <strong><Link to="/theophanies">Theophanies &amp; Visionary Experiences</Link></strong> &mdash; the canonical
            visions PKD reported (1963&ndash;1981), each with his shifting interpretations beside the
            scholarship.
          </li>
          <li>
            <strong><Link to="/archive">Archive</Link></strong> &mdash; 228+ documents tagged by evidentiary lane:
            biographies, scholarship, interviews, letters, fan publications, newspapers, finding aids.
          </li>
          <li>
            <strong><Link to="/dictionary">Dictionary</Link></strong> &mdash; 310 terms covering theology, philosophy,
            and PKD's bespoke vocabulary, with evidence passages and cross-links.
          </li>
          <li>
            <strong><Link to="/names">Names</Link></strong> &mdash; 592 named entities: 191 fiction characters with
            etymology and wordplay, plus the historical, biblical, and mythological figures PKD invokes.
          </li>
          <li>
            <strong><Link to="/scholars">Scholars</Link></strong> &mdash; 119 PKD scholars across five tiers, with
            interpretive stances, key arguments, scholarly lineage, and disputes.
          </li>
          <li>
            <strong><Link to="/essays">Essays</Link></strong> &mdash; long-form arguments synthesizing the corpus
            (drugs, music, more queued), with lane sourcing and dispute registration.
          </li>
          <li>
            <strong><Link to="/studies">Studies</Link></strong> &mdash; topic-anchored studies that cut across the
            corpus (e.g., AI in PKD's fiction).
          </li>
        </ul>
      </div>

      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'2rem', marginTop:'1rem'}}>
        <div className="detail-section">
          <h2>Key concepts</h2>
          <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:'0.25rem 0 0.75rem'}}>
            The terms most frequently invoked across the corpus.
          </p>
          <ul>
            {data.top_terms.slice(0, 12).map(t => (
              <li key={t.name}>
                <Link to={`/dictionary/${t.name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`}>
                  {t.name}
                </Link>
                <span style={{color:'var(--text-muted)', marginLeft:'0.5rem'}}>
                  ({t.count.toLocaleString()})
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="detail-section">
          <h2>Browse by year</h2>
          <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:'0.25rem 0 0.75rem'}}>
            Philip K. Dick (1928&ndash;1982). Many years are unpopulated &mdash; publications and additional biography
            events are queued to fill them in.
          </p>
          {(() => {
            const decades = new Map<string, typeof data.segments_per_year>()
            for (const y of data.segments_per_year) {
              const dec = y.year.slice(0, 3) + '0s'
              if (!decades.has(dec)) decades.set(dec, [])
              decades.get(dec)!.push(y)
            }
            return Array.from(decades.entries()).map(([dec, years]) => (
              <div key={dec} style={{marginBottom:'0.75rem'}}>
                <div style={{fontWeight:600, fontSize:'0.85rem', color:'var(--text-muted)', marginBottom:'0.25rem'}}>{dec}</div>
                <div style={{display:'flex', flexWrap:'wrap', gap:'0.25rem'}}>
                  {years.map(y => {
                    const total = y.count + (y.bio_events || 0)
                    const hasContent = y.has_content || total > 0
                    return (
                      <Link
                        key={y.year}
                        to={hasContent ? `/timeline/${y.year}` : '#'}
                        style={{
                          display:'inline-block',
                          padding:'0.2rem 0.45rem',
                          fontSize:'0.8rem',
                          borderRadius:'4px',
                          textDecoration:'none',
                          background: y.count > 100 ? 'var(--accent)' : y.count > 0 ? 'var(--accent-muted, rgba(var(--accent-rgb, 100,100,200), 0.2))' : hasContent ? 'var(--bg-elevated, #f0f0f0)' : 'transparent',
                          color: y.count > 100 ? '#fff' : hasContent ? 'var(--text)' : 'var(--text-muted)',
                          opacity: hasContent ? 1 : 0.4,
                          cursor: hasContent ? 'pointer' : 'default',
                        }}
                        title={`${y.year}: ${y.count} Exegesis entries${y.bio_events ? `, ${y.bio_events} biography events` : ''}`}
                      >
                        {y.year.slice(2)}
                      </Link>
                    )
                  })}
                </div>
              </div>
            ))
          })()}
        </div>
      </div>
    </>
  )
}

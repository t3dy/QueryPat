import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'

interface Analytics {
  totals: {
    documents: number
    segments: number
    terms_public: number
    archive_docs: number
    names: number
  }
  top_terms: { name: string; count: number }[]
  segments_per_year: { year: string; count: number; bio_events?: number; theophanies?: number; has_content?: boolean }[]
}

interface TheophanyMeta {
  theophany_id: string
  slug: string
  name: string
  date_display: string
  importance: string
}

interface ArchiveDoc {
  doc_id: string
  slug: string
  title: string
  category: string
  evidentiary_lane?: string
}

interface Scholar {
  scholar_id: string
  name: string
  tier: string
  role: string
}

interface DictTerm {
  slug: string
  canonical_name: string
  category?: string
  segments_count?: number
}

const TIER_LABELS: Record<string, string> = {
  '1': 'Tier 1 — Major Biographers',
  '2': 'Tier 2 — Scholars & Critics',
  '3': 'Tier 3 — Editors & Curators',
  '4': 'Tier 4 — Associates',
  '5': 'Tier 5 — Media',
}

function pickRandom<T>(items: T[], n: number): T[] {
  if (!items || items.length === 0) return []
  const copy = [...items]
  const out: T[] = []
  for (let i = 0; i < Math.min(n, copy.length); i++) {
    const idx = Math.floor(Math.random() * copy.length)
    out.push(copy.splice(idx, 1)[0])
  }
  return out
}

export default function Browse() {
  const { data: analytics } = useData<Analytics>('analytics.json')
  const { data: theoIndex } = useData<{ theophanies: TheophanyMeta[] }>('theophanies/index.json')
  const { data: archive } = useData<ArchiveDoc[] | { documents: ArchiveDoc[] }>('archive/index.json')
  const { data: scholars } = useData<Scholar[]>('scholars.json')
  const { data: dictionary } = useData<{ terms: DictTerm[] } | DictTerm[]>('dictionary/index.json')

  const archiveList = (Array.isArray(archive) ? archive : archive?.documents) || []
  const dictList = (Array.isArray(dictionary) ? dictionary : (dictionary as any)?.terms) || []

  const [randomSeed, setRandomSeed] = useState(0)
  useEffect(() => {
    setRandomSeed(s => s + 1)
  }, [])

  // Force re-eval when randomSeed changes
  void randomSeed
  const randTheo = pickRandom(theoIndex?.theophanies || [], 3)
  const randDoc = pickRandom(archiveList as ArchiveDoc[], 4)
  const randScholar = pickRandom(scholars || [], 4)
  const randTerm = pickRandom(dictList as DictTerm[], 8)

  type YearEntry = { year: string; count: number; bio_events?: number; theophanies?: number; has_content?: boolean }
  const yearsByDecade = (analytics?.segments_per_year || []).reduce((acc, y) => {
    const dec = y.year.slice(0, 3) + '0s'
    if (!acc[dec]) acc[dec] = []
    acc[dec].push(y)
    return acc
  }, {} as Record<string, YearEntry[]>)

  return (
    <>
      <div className="hero-header">
        <h1>Browse</h1>
        <p className="hero-subtitle">
          A cross-section entry point. Jump to a year, a theophany, a scholar, an archive document,
          or a key term &mdash; or shuffle the dice and let the corpus surprise you.
        </p>
      </div>

      <div style={{display:'flex', justifyContent:'flex-end', marginBottom:'1rem'}}>
        <button
          onClick={() => setRandomSeed(s => s + 1)}
          style={{
            padding:'0.4rem 0.9rem', fontSize:'0.85rem',
            background:'var(--accent)', color:'#fff',
            border:'none', borderRadius:'4px', cursor:'pointer',
          }}
        >
          🎲 Reshuffle
        </button>
      </div>

      <div className="detail-section">
        <h2>By year</h2>
        <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:'0.25rem 0 0.75rem'}}>
          Years with biography events, theophanies, or <em>Exegesis</em> writings light up.
        </p>
        {Object.entries(yearsByDecade).map(([dec, years]) => (
          <div key={dec} style={{marginBottom:'0.75rem'}}>
            <div style={{fontWeight:600, fontSize:'0.85rem', color:'var(--text-muted)', marginBottom:'0.25rem'}}>{dec}</div>
            <div style={{display:'flex', flexWrap:'wrap', gap:'0.25rem'}}>
              {years.map(y => {
                const total = (y.count || 0) + (y.bio_events || 0) + (y.theophanies || 0)
                const hasContent = y.has_content || total > 0
                return (
                  <Link
                    key={y.year}
                    to={hasContent ? `/timeline/${y.year}` : '#'}
                    style={{
                      display:'inline-block', padding:'0.25rem 0.5rem',
                      fontSize:'0.8rem', borderRadius:'4px', textDecoration:'none',
                      background: y.count > 100 ? 'var(--accent)' : y.count > 0 ? 'rgba(192,154,77,0.2)' : hasContent ? 'rgba(192,154,77,0.08)' : 'transparent',
                      color: y.count > 100 ? '#fff' : hasContent ? 'var(--text)' : 'var(--text-muted)',
                      opacity: hasContent ? 1 : 0.35,
                      cursor: hasContent ? 'pointer' : 'default',
                      border: hasContent ? '1px solid rgba(192,154,77,0.3)' : '1px solid transparent',
                    }}
                    title={`${y.year}: ${y.count || 0} segments, ${y.bio_events || 0} bio events, ${y.theophanies || 0} theophanies`}
                  >
                    {y.year.slice(2)}
                  </Link>
                )
              })}
            </div>
          </div>
        ))}
      </div>

      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'1.5rem', marginTop:'1rem'}}>
        <div className="detail-section">
          <h2>Random theophanies</h2>
          <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:0}}>
            Three drawn from the canonical 15.
          </p>
          <ul style={{lineHeight:'1.6'}}>
            {randTheo.map(t => (
              <li key={t.theophany_id}>
                <Link to={`/theophanies/${t.slug}`}>{t.name}</Link>
                <span style={{color:'var(--text-muted)', marginLeft:'0.5rem', fontSize:'0.85rem'}}>
                  ({t.date_display})
                </span>
              </li>
            ))}
          </ul>
          <Link to="/theophanies" style={{fontSize:'0.85rem'}}>All theophanies &rarr;</Link>
        </div>

        <div className="detail-section">
          <h2>Random archive documents</h2>
          <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:0}}>
            Four drawn from {archiveList.length} archive entries.
          </p>
          <ul style={{lineHeight:'1.6'}}>
            {randDoc.map(d => (
              <li key={d.doc_id || d.slug}>
                <Link to={`/archive/${d.slug}`}>{d.title}</Link>
                <span style={{color:'var(--text-muted)', marginLeft:'0.5rem', fontSize:'0.85rem'}}>
                  {d.category}{d.evidentiary_lane ? ` · Lane ${d.evidentiary_lane}` : ''}
                </span>
              </li>
            ))}
          </ul>
          <Link to="/archive" style={{fontSize:'0.85rem'}}>All archive &rarr;</Link>
        </div>

        <div className="detail-section">
          <h2>Random scholars</h2>
          <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:0}}>
            Four drawn from 119 profiles.
          </p>
          <ul style={{lineHeight:'1.6'}}>
            {randScholar.map(s => (
              <li key={s.scholar_id}>
                <Link to="/scholars">{s.name}</Link>
                <span style={{color:'var(--text-muted)', marginLeft:'0.5rem', fontSize:'0.85rem'}}>
                  {s.role || TIER_LABELS[s.tier] || ''}
                </span>
              </li>
            ))}
          </ul>
          <Link to="/scholars" style={{fontSize:'0.85rem'}}>All scholars &rarr;</Link>
        </div>

        <div className="detail-section">
          <h2>Random dictionary terms</h2>
          <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:0}}>
            Eight drawn from 310 published terms.
          </p>
          <ul style={{lineHeight:'1.6', columnCount:2, columnGap:'1rem'}}>
            {randTerm.map(t => (
              <li key={t.slug}>
                <Link to={`/dictionary/${t.slug}`}>{t.canonical_name}</Link>
                {t.segments_count != null && t.segments_count > 0 && (
                  <span style={{color:'var(--text-muted)', marginLeft:'0.4rem', fontSize:'0.8rem'}}>
                    ({t.segments_count})
                  </span>
                )}
              </li>
            ))}
          </ul>
          <Link to="/dictionary" style={{fontSize:'0.85rem'}}>All dictionary &rarr;</Link>
        </div>
      </div>

      <div className="detail-section" style={{marginTop:'1rem'}}>
        <h2>Top concepts in the corpus</h2>
        <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:'0 0 0.5rem'}}>
          The terms PKD invokes most frequently across the <em>Exegesis</em> and the archive.
        </p>
        <div style={{display:'flex', flexWrap:'wrap', gap:'0.5rem'}}>
          {(analytics?.top_terms || []).slice(0, 30).map(t => {
            const slug = t.name.toLowerCase().replace(/[^a-z0-9]+/g, '-')
            return (
              <Link
                key={t.name}
                to={`/dictionary/${slug}`}
                style={{
                  padding:'0.3rem 0.6rem', fontSize:'0.85rem',
                  background:'rgba(192,154,77,0.12)', borderRadius:'12px',
                  textDecoration:'none', color:'inherit',
                  border:'1px solid rgba(192,154,77,0.2)',
                }}
              >
                {t.name} <span style={{color:'var(--text-muted)', fontSize:'0.8rem'}}>{t.count.toLocaleString()}</span>
              </Link>
            )
          })}
        </div>
      </div>

      <div className="detail-section" style={{marginTop:'1rem'}}>
        <h2>Cross-section paths</h2>
        <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:'0 0 0.75rem'}}>
          A few curated journeys through the corpus.
        </p>
        <ul style={{lineHeight:'1.7'}}>
          <li>
            <strong><Link to="/theophanies/2-3-74-cluster">The 2-3-74 cluster</Link></strong> &rarr;
            <Link to="/theophanies/fish-sign-2-20-74"> the Fish Sign </Link> &rarr;
            <Link to="/theophanies/pink-beam-1974"> the Pink Beam </Link> &rarr;
            <Link to="/dictionary/valis"> Valis </Link> &rarr;
            <Link to="/exegesis"> the Exegesis</Link>
          </li>
          <li>
            <strong><Link to="/essays/drugs-in-pkd">Drugs in PKD</Link></strong> &rarr;
            <Link to="/scholars"> Sutin / Anne Dick / Arnold </Link> &rarr;
            <Link to="/archive"> archive (lane D and C)</Link>
          </li>
          <li>
            <strong><Link to="/essays/music-in-pkd">Music in PKD</Link></strong> &rarr;
            <Link to="/dictionary"> Beethoven </Link> &rarr;
            <Link to="/theophanies/twin-sister-jane-1980"> Sister Jane </Link> &rarr;
            <Link to="/archive"> Erik Davis on Sonic Youth</Link>
          </li>
          <li>
            <strong><Link to="/theophanies/numbers-letters-gematria-1975">Gematria vision</Link></strong> &rarr;
            <Link to="/theophanies/abulafia-possession-1976"> Abulafia possession </Link> &rarr;
            <Link to="/theophanies/koine-greek-1974"> Koine Greek</Link>
          </li>
          <li>
            <strong><Link to="/timeline/1974">Year 1974</Link></strong> &rarr;
            <Link to="/timeline/1975"> 1975 </Link> &rarr;
            <Link to="/timeline/1976"> 1976</Link>
            &mdash; the heart of the Exegesis years
          </li>
        </ul>
      </div>
    </>
  )
}

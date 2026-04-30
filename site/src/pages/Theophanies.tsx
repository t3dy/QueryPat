import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'
import ExploreFooter from '../components/ExploreFooter'

interface TheophanyMeta {
  theophany_id: string
  name: string
  slug: string
  date_display: string
  date_start: string
  experience_type: string
  summary: string
  importance: string
  contested_status: string
  parent_theophany_id: string | null
  n_pkd_interpretations: number
  n_scholar_interpretations: number
  related_works: string[]
}

interface TheophanyIndex {
  total: number
  theophanies: TheophanyMeta[]
}

const IMPORTANCE_ORDER: Record<string, number> = { canonical: 0, major: 1, minor: 2 }

const EXPERIENCE_TYPE_LABELS: Record<string, string> = {
  vision: 'Vision',
  audition: 'Audition',
  possession: 'Possession',
  hypnagogic: 'Hypnagogic',
  dream: 'Dream',
  gnosis: 'Gnosis',
  anamnesis: 'Anamnesis',
  theophany: 'Theophany (cluster)',
  reading_event: 'Reading event',
  kabbalistic_transmission: 'Kabbalistic transmission',
  other: 'Other',
}

export default function Theophanies() {
  const { data, loading } = useData<TheophanyIndex>('theophanies/index.json')
  const [filterType, setFilterType] = useState<string>('all')
  const [filterImportance, setFilterImportance] = useState<string>('all')

  if (loading || !data) return <div className="loading">Loading...</div>

  const all = data.theophanies
  const types = Array.from(new Set(all.map(t => t.experience_type))).sort()

  const filtered = all.filter(t => {
    if (filterType !== 'all' && t.experience_type !== filterType) return false
    if (filterImportance !== 'all' && t.importance !== filterImportance) return false
    return true
  }).sort((a, b) => {
    const ic = (IMPORTANCE_ORDER[a.importance] ?? 9) - (IMPORTANCE_ORDER[b.importance] ?? 9)
    if (ic !== 0) return ic
    return (a.date_start || '').localeCompare(b.date_start || '')
  })

  return (
    <>
      <div className="hero-header">
        <h1>Theophanies &amp; Visionary Experiences</h1>
        <p className="hero-subtitle">
          The Greek word <em>theophania</em> names what Philip K. Dick said happened to him from 1963 onward.
          This catalog records every reported instance the corpus knows about &mdash; with PKD's changing
          interpretations and the contemporary scholarship arrayed beside them.
        </p>
      </div>

      <div className="detail-section">
        <p>
          Each entry is a maximally <Link to="/archive">Lane B</Link> claim: a self-report from inside
          an unreliable narrator about a state with no external witness. The portal records <em>that</em>
          PKD reported it, what evidence supports the report, and which scholars have read it as veridical,
          temporal-lobe, drug-induced, literary, or composite. We do not adjudicate ontology; we surface
          the chain of attribution. PKD reinterpreted the same vision dozens of times across the eight
          years of the Exegesis &mdash; that oscillation is the data.
        </p>
        <p style={{fontSize: '0.9rem', color: 'var(--text-muted)'}}>
          Schema and editorial method documented in <code>PKD_THEOPHANY_ONTOLOGY.md</code>. Coverage: {data.total} canonical
          and major theophanies seeded from the Exegesis, the major biographies, the Rickman interviews,
          and the published edition's apparatus. Scope expansion is queued.
        </p>
      </div>

      <div className="detail-section">
        <div style={{display:'flex', gap:'1rem', alignItems:'center', flexWrap:'wrap'}}>
          <span style={{fontWeight:600}}>Filter:</span>
          <label>
            Type:&nbsp;
            <select value={filterType} onChange={e => setFilterType(e.target.value)}>
              <option value="all">all</option>
              {types.map(t => <option key={t} value={t}>{EXPERIENCE_TYPE_LABELS[t] || t}</option>)}
            </select>
          </label>
          <label>
            Importance:&nbsp;
            <select value={filterImportance} onChange={e => setFilterImportance(e.target.value)}>
              <option value="all">all</option>
              <option value="canonical">canonical</option>
              <option value="major">major</option>
              <option value="minor">minor</option>
            </select>
          </label>
          <span style={{color:'var(--text-muted)', fontSize:'0.85rem'}}>
            {filtered.length} of {all.length}
          </span>
        </div>
      </div>

      <ExploreFooter groups={[
        { section: 'The Exegesis', items: [
          { label: 'Browse the Exegesis landing', to: '/exegesis' },
          { label: 'Timeline 1974 (the year of 2-3-74)', to: '/timeline/1974' },
          { label: 'Timeline 1975', to: '/timeline/1975' },
        ]},
        { section: 'Biography & sources', items: [
          { label: 'Biography events', to: '/biography' },
          { label: 'Scholars on PKD', to: '/scholars' },
          { label: 'Archive (228 documents)', to: '/archive' },
        ]},
        { section: 'Companion essays', items: [
          { label: 'Drugs in Philip K. Dick', to: '/essays/drugs-in-pkd' },
          { label: 'Music in Philip K. Dick', to: '/essays/music-in-pkd' },
        ]},
      ]} />

      <div style={{display:'grid', gridTemplateColumns:'1fr', gap:'1.25rem', marginTop:'1.5rem'}}>
        {filtered.map(t => (
          <Link
            key={t.theophany_id}
            to={`/theophanies/${t.slug}`}
            className="detail-section"
            style={{textDecoration:'none', color:'inherit', display:'block'}}
          >
            <div style={{display:'flex', alignItems:'center', flexWrap:'wrap', gap:'0.5rem'}}>
              <h2 style={{margin:0, fontSize:'1.2rem'}}>{t.name}</h2>
              {t.importance === 'canonical' && (
                <span style={{
                  fontSize:'0.7rem', padding:'0.15rem 0.4rem',
                  background:'var(--accent, #c09a4d)', color:'#fff',
                  borderRadius:'3px', textTransform:'uppercase'
                }}>canonical</span>
              )}
              {t.parent_theophany_id && (
                <span style={{fontSize:'0.7rem', color:'var(--text-muted)'}}>
                  child of {t.parent_theophany_id}
                </span>
              )}
            </div>
            <div style={{fontSize:'0.85rem', color:'var(--text-muted)', margin:'0.25rem 0'}}>
              <span>{t.date_display}</span>
              <span style={{margin:'0 0.5rem'}}>&middot;</span>
              <span>{EXPERIENCE_TYPE_LABELS[t.experience_type] || t.experience_type}</span>
              <span style={{margin:'0 0.5rem'}}>&middot;</span>
              <span>{t.n_pkd_interpretations} interpretation{t.n_pkd_interpretations === 1 ? '' : 's'} by PKD</span>
              <span style={{margin:'0 0.5rem'}}>&middot;</span>
              <span>{t.n_scholar_interpretations} scholar reading{t.n_scholar_interpretations === 1 ? '' : 's'}</span>
            </div>
            <p style={{margin:'0.5rem 0 0', fontSize:'0.95rem'}}>{t.summary}</p>
            {t.related_works && t.related_works.length > 0 && (
              <div style={{marginTop:'0.5rem', fontSize:'0.8rem', color:'var(--text-muted)'}}>
                Seeds: {t.related_works.map(w => <em key={w}>{w}</em>).reduce((acc, el, i) => i === 0 ? [el] : [...acc, ', ', el], [] as React.ReactNode[])}
              </div>
            )}
          </Link>
        ))}
      </div>
    </>
  )
}

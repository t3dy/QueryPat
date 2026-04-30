import { Link } from 'react-router-dom'
import { useData } from '../hooks/useData'
import ExploreFooter from '../components/ExploreFooter'

interface TimelineIndex {
  year: string
  count: number
  bio_events?: number
}

interface Analytics {
  totals: {
    segments: number
    segments_with_summary: number
    segments_with_raw_text: number
  }
  top_terms: { name: string; count: number; category: string }[]
}

const EXEG_TERMS = ['Christ', 'Valis', 'Tears', 'Acts', 'Christian', 'Ubik', 'Thomas', 'Spirit', 'Holy']

const EXEG_SCHOLARS: { name: string; note: string }[] = [
  { name: 'Pamela Jackson', note: 'Co-editor of the published Exegesis (HMH, 2011); 1999 UC Berkeley dissertation The World Philip K. Dick Made — the foundational academic engagement with the manuscript.' },
  { name: 'Jonathan Lethem', note: 'Co-editor of the published Exegesis (HMH, 2011); editor of the 2007 Library of America PKD volumes; sets the literary-rather-than-philosophical tonal register of the published edition.' },
  { name: 'Erik Davis', note: 'Annotator on the published Exegesis (2011); TechGnosis (1998) and High Weirdness (2019) place PKD within a comparative California-visionary frame alongside McKenna and Wilson.' },
  { name: 'Gabriel McKee', note: 'Pink Beams of Light from the God in the Gutter (2004) — first book-length theological reading, locating PKD within Gnostic, Christian-mystical, Process, and Jewish-mystical traditions.' },
  { name: 'Jeffrey J. Kripal', note: 'Annotator on the published Exegesis (2011); Mutants and Mystics (2011) and Authors of the Impossible (2010) frame PKD as exemplary American visionary religiosity.' },
  { name: 'Simon Critchley', note: 'Annotator on the published Exegesis (2011); chapter on PKD in How to Stop Living and Start Worrying (2010) — reads the Exegesis as sustained engagement with self and the limits of self-knowledge.' },
]

export default function Exegesis() {
  const { data: analytics } = useData<Analytics>('analytics.json')
  const { data: yearIndex } = useData<TimelineIndex[]>('timeline/index.json')

  const exegYears = (yearIndex || []).filter(y => y.count > 0)
  const totalSegments = analytics?.totals.segments ?? 1107
  const withSummary = analytics?.totals.segments_with_summary ?? 207
  const withRawText = analytics?.totals.segments_with_raw_text ?? 882

  return (
    <>
      <div className="hero-header">
        <h1>The <em>Exegesis</em></h1>
        <p className="hero-subtitle">
          Philip K. Dick's private theological notebook (1974&ndash;1982) &mdash; ~8,000 manuscript pages of speculation
          on the visionary experiences he called <em>2-3-74</em>.
        </p>
      </div>

      <div className="detail-section">
        <p>
          Beginning in February&ndash;March 1974, after a series of experiences he interpreted variously as religious
          revelation, mental illness, KGB intervention, and contact with an information satellite, PKD spent the last
          eight years of his life writing a continuously revised theological journal. He called it his
          {' '}<em>Exegesis</em>. He produced roughly 8,000 typed and handwritten pages, never published in his lifetime.
          A 944-page selection edited by Pamela Jackson and Jonathan Lethem appeared in 2011.
        </p>
        <p>
          This portal indexes the <em>Exegesis</em> at the segment level: chunks of text with parsed summaries, recurring
          concepts, biblical and philosophical references, and links into the dictionary and biography. Segments are
          Lane B evidence (PKD's self-report &mdash; one of five lanes used across the {' '}
          <Link to="/archive">archive</Link>): they show what he theorized about himself, not necessarily what was true.
        </p>
      </div>

      <div className="stats-grid">
        <Link to="/timeline" className="stat-card" style={{textDecoration:'none'}}>
          <div className="stat-value">{totalSegments.toLocaleString()}</div>
          <div className="stat-label">Total segments</div>
        </Link>
        <div className="stat-card">
          <div className="stat-value">{withSummary.toLocaleString()}</div>
          <div className="stat-label">With parsed summaries</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{withRawText.toLocaleString()}</div>
          <div className="stat-label">With raw text</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{exegYears.length}</div>
          <div className="stat-label">Years with segments</div>
        </div>
      </div>

      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'2rem', marginTop:'1rem'}}>
        <div className="detail-section">
          <h2>Browse by year</h2>
          <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:'0.25rem 0 0.75rem'}}>
            Currently four years are populated: 1975, 1976, 1978, 1981. PKD wrote across all eight years (1974&ndash;1982);
            the remaining segments are awaiting summary parsing.
          </p>
          <ul>
            {exegYears.map(y => (
              <li key={y.year}>
                <Link to={`/timeline/${y.year}`}>
                  {y.year}
                </Link>
                <span style={{color:'var(--text-muted)', marginLeft:'0.5rem'}}>
                  ({y.count.toLocaleString()} segments{y.bio_events ? `, ${y.bio_events} biography events` : ''})
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="detail-section">
          <h2>Recurring vocabulary</h2>
          <p style={{color:'var(--text-muted)', fontSize:'0.85rem', margin:'0.25rem 0 0.75rem'}}>
            The terms PKD returns to most often across the manuscript.
          </p>
          <ul>
            {EXEG_TERMS.map(name => {
              const term = analytics?.top_terms.find(t => t.name === name)
              const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-')
              return (
                <li key={name}>
                  <Link to={`/dictionary/${slug}`}>{name}</Link>
                  {term && (
                    <span style={{color:'var(--text-muted)', marginLeft:'0.5rem'}}>
                      ({term.count.toLocaleString()})
                    </span>
                  )}
                </li>
              )
            })}
          </ul>
        </div>
      </div>

      <ExploreFooter groups={[
        { section: 'Visionary experiences', items: [
          { label: 'The 2-3-74 cluster', to: '/theophanies/2-3-74-cluster' },
          { label: 'The Fish Sign (Feb 20, 1974)', to: '/theophanies/fish-sign-2-20-74' },
          { label: 'The Pink Beam', to: '/theophanies/pink-beam-1974' },
          { label: 'The AI Voice', to: '/theophanies/ai-voice-1974' },
        ], totalCount: 15, seeAllTo: '/theophanies' },
        { section: 'Companion reading', items: [
          { label: 'Drugs in PKD essay', to: '/essays/drugs-in-pkd' },
          { label: 'Music in PKD essay', to: '/essays/music-in-pkd' },
          { label: 'Pamela Jackson, Erik Davis, Lethem', to: '/scholars' },
        ]},
        { section: 'Browse', items: [
          { label: 'Timeline 1974', to: '/timeline/1974' },
          { label: 'Timeline 1975', to: '/timeline/1975' },
          { label: 'Timeline 1976', to: '/timeline/1976' },
          { label: 'Timeline 1981', to: '/timeline/1981' },
        ]},
      ]} />

      <div className="detail-section" style={{marginTop:'1rem'}}>
        <h2>Key scholars on the <em>Exegesis</em></h2>
        <ul>
          {EXEG_SCHOLARS.map(s => (
            <li key={s.name} style={{marginBottom:'0.4rem'}}>
              <Link to="/scholars">{s.name}</Link>
              <span style={{color:'var(--text-muted)', marginLeft:'0.5rem'}}>&mdash; {s.note}</span>
            </li>
          ))}
        </ul>
      </div>
    </>
  )
}

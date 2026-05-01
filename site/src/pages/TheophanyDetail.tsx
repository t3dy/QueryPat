import { Link, useParams } from 'react-router-dom'
import { useData } from '../hooks/useData'
import ExploreFooter from '../components/ExploreFooter'

interface PkdInterpretation {
  date: string
  source: string
  hypothesis_label: string
  interpretation: string
  lane: string
}

interface ScholarInterpretation {
  scholar_slug: string
  interpretation: string
  source_doc_id: string | null
  lane: string
}

interface PrimarySource {
  type: string
  doc_id?: string | null
  seg_id?: string | null
  letter_id?: string | null
  excerpt: string
}

interface Theophany {
  theophany_id: string
  name: string
  slug: string
  date_start: string
  date_end: string
  date_display: string
  date_confidence: string
  date_basis: string
  experience_type: string
  sensory_modality: string
  duration: string
  summary: string
  description: string
  pkd_interpretations: PkdInterpretation[]
  scholar_interpretations: ScholarInterpretation[]
  primary_sources: PrimarySource[]
  primary_quote: string | null
  related_theophany_ids: string[]
  related_works: string[]
  related_dictionary_terms: string[]
  related_names: string[]
  related_segments: string[]
  contested_status: string
  contradiction_zone: string
  pkd_doubt_evidence: string | null
  importance: string
  parent_theophany_id: string | null
}

const HYPOTHESIS_LABEL_MAP: Record<string, string> = {
  soviet_satellite: 'Soviet satellite (Lem-as-front)',
  cia_op: 'CIA disinformation',
  christian_revelation: 'Christian revelation',
  gnostic_demiurge: 'Gnostic demiurge',
  valis_information_satellite: 'VALIS information satellite',
  zebra_mimicry: 'Zebra mimicry',
  time_dysphasia: 'Time dysphasia (Rome overlay)',
  phil_from_future: 'Phil-from-future',
  jung_collective: 'Jungian collective unconscious',
  tle: 'Temporal-lobe epilepsy',
  drug_induced: 'Drug-induced',
  psychotic_break: 'Psychotic break',
  apostle_thomas_rebirth: 'Apostle Thomas rebirth',
  hellenistic_wisdom: 'Hellenistic wisdom (Sophia)',
  kabbalistic_gematria: 'Kabbalistic gematria',
  abulafia_possession: 'Abulafia possession',
  vedic_brahman: 'Vedantic Brahman',
  taoist_li: 'Taoist Li',
  process_theology: 'Process theology',
  evolutionary_consciousness: 'Evolutionary consciousness',
  evil_god: 'Evil god / Antichrist',
  valis_negative_polarity: 'VALIS negative polarity',
  literary_consolidation: 'Literary consolidation',
  twin_sister_jane: 'Twin sister Jane',
  sophia: 'Sophia / Hagia Sophia',
  phylogenic_anamnesis: 'Phylogenic anamnesis',
  phil_thomas_overlay: 'Phil/Thomas overlay',
  best_attested: 'Best attested',
  spiritual_precondition: 'Spiritual precondition',
  literary: 'Literary device',
  drug_dealers: 'Drug dealers',
  fbi: 'FBI',
  self_staged: 'Self-staged',
  subliminal_observation: 'Subliminal observation',
}

function laneBadge(lane: string) {
  const colors: Record<string, string> = {
    A: '#8B7355', B: '#9B6B9B', C: '#7B8FA1', D: '#6B8E6B', E: '#C09A4D',
  }
  return (
    <span style={{
      display:'inline-block', minWidth:'1.1rem', textAlign:'center',
      fontSize:'0.7rem', padding:'0.1rem 0.3rem',
      background: colors[lane] || '#999', color:'#fff',
      borderRadius:'3px', fontWeight:600
    }}>{lane}</span>
  )
}

export default function TheophanyDetail() {
  const { slug } = useParams()
  const { data, loading, error } = useData<Theophany>(slug ? `theophanies/${slug}.json` : null)

  if (loading) return <div className="loading">Loading...</div>
  if (error || !data) return (
    <div className="detail-section">
      <p>Theophany not found.</p>
      <Link to="/theophanies">&larr; All theophanies</Link>
    </div>
  )

  return (
    <article>
      <div className="hero-header" style={{paddingBottom:'1rem'}}>
        <h1>{data.name}</h1>
        <p className="hero-subtitle" style={{margin:'0.5rem 0 0'}}>
          {data.summary}
        </p>
      </div>

      <div className="detail-section">
        <div style={{fontSize:'0.85rem', color:'var(--text-muted)', display:'flex', flexWrap:'wrap', gap:'1rem'}}>
          <span><strong>Date:</strong> {data.date_display}</span>
          <span><strong>Type:</strong> {data.experience_type}</span>
          {data.sensory_modality && <span><strong>Modality:</strong> {data.sensory_modality}</span>}
          {data.duration && <span><strong>Duration:</strong> {data.duration}</span>}
          <span><strong>Importance:</strong> {data.importance}</span>
          <span><strong>Status:</strong> {data.contested_status}</span>
        </div>
        {data.date_basis && (
          <p style={{fontSize:'0.85rem', color:'var(--text-muted)', margin:'0.5rem 0 0'}}>
            Date basis: {data.date_basis}
          </p>
        )}
      </div>

      {data.description && (
        <div className="detail-section">
          <h2>Description</h2>
          <p>{data.description}</p>
        </div>
      )}

      {data.primary_quote && (
        <div className="detail-section" style={{borderLeft:'3px solid var(--accent)', paddingLeft:'1rem'}}>
          <p style={{fontStyle:'italic', fontSize:'1.1rem', margin:0}}>"{data.primary_quote}"</p>
          <p style={{fontSize:'0.8rem', color:'var(--text-muted)', margin:'0.25rem 0 0'}}>&mdash; PKD (canonical phrasing)</p>
        </div>
      )}

      {data.contradiction_zone && data.contradiction_zone.startsWith('yes') && (
        <div className="detail-section" style={{
          background:'rgba(155, 107, 155, 0.1)', borderLeft:'3px solid #9B6B9B', padding:'0.75rem 1rem'
        }}>
          <strong>Contradiction zone:</strong> {data.contradiction_zone}
          {data.pkd_doubt_evidence && (
            <p style={{margin:'0.5rem 0 0', fontSize:'0.9rem'}}>
              <strong>PKD's own doubt:</strong> {data.pkd_doubt_evidence}
            </p>
          )}
        </div>
      )}

      {data.pkd_interpretations && data.pkd_interpretations.length > 0 && (
        <div className="detail-section">
          <h2>PKD's interpretations over time</h2>
          <p style={{fontSize:'0.85rem', color:'var(--text-muted)'}}>
            How he read the same event across the years. Earlier readings are not retracted by later ones &mdash; they coexist in the corpus.
          </p>
          <div style={{display:'grid', gap:'0.75rem'}}>
            {data.pkd_interpretations.map((p, i) => (
              <div key={i} style={{borderLeft:'2px solid var(--border, rgba(0,0,0,0.1))', paddingLeft:'1rem'}}>
                <div style={{fontSize:'0.85rem', color:'var(--text-muted)', display:'flex', gap:'0.5rem', alignItems:'center'}}>
                  <span><strong>{p.date}</strong></span>
                  {laneBadge(p.lane)}
                  {p.hypothesis_label && (
                    <span style={{fontSize:'0.75rem', padding:'0.1rem 0.4rem', background:'rgba(192,154,77,0.15)', borderRadius:'3px'}}>
                      {HYPOTHESIS_LABEL_MAP[p.hypothesis_label] || p.hypothesis_label}
                    </span>
                  )}
                </div>
                <p style={{margin:'0.25rem 0 0'}}>{p.interpretation}</p>
                <p style={{fontSize:'0.75rem', color:'var(--text-muted)', margin:'0.25rem 0 0'}}>
                  Source: {p.source}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {data.scholar_interpretations && data.scholar_interpretations.length > 0 && (
        <div className="detail-section">
          <h2>Scholar readings</h2>
          <div style={{display:'grid', gap:'0.75rem'}}>
            {data.scholar_interpretations.map((s, i) => (
              <div key={i} style={{borderLeft:'2px solid var(--border, rgba(0,0,0,0.1))', paddingLeft:'1rem'}}>
                <div style={{fontSize:'0.85rem', display:'flex', gap:'0.5rem', alignItems:'center'}}>
                  <Link to="/scholars" style={{fontWeight:600}}>{s.scholar_slug}</Link>
                  {laneBadge(s.lane)}
                </div>
                <p style={{margin:'0.25rem 0 0'}}>{s.interpretation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {data.primary_sources && data.primary_sources.length > 0 && (
        <div className="detail-section">
          <h2>Primary sources</h2>
          <ul style={{paddingLeft:'1.25rem'}}>
            {data.primary_sources.map((s, i) => (
              <li key={i} style={{marginBottom:'0.5rem'}}>
                <strong>{s.type}:</strong> {s.excerpt}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="detail-section">
        <h2>Cross-links</h2>
        <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'1rem'}}>
          {data.related_works && data.related_works.length > 0 && (
            <div>
              <strong>Works seeded</strong>
              <ul style={{paddingLeft:'1.25rem', margin:'0.25rem 0'}}>
                {data.related_works.map(w => <li key={w}><em>{w}</em></li>)}
              </ul>
            </div>
          )}
          {data.related_dictionary_terms && data.related_dictionary_terms.length > 0 && (
            <div>
              <strong>Dictionary terms</strong>
              <ul style={{paddingLeft:'1.25rem', margin:'0.25rem 0'}}>
                {data.related_dictionary_terms.map(t => (
                  <li key={t}><Link to={`/dictionary/${t}`}>{t}</Link></li>
                ))}
              </ul>
            </div>
          )}
          {data.related_names && data.related_names.length > 0 && (
            <div>
              <strong>Named entities</strong>
              <ul style={{paddingLeft:'1.25rem', margin:'0.25rem 0'}}>
                {data.related_names.map(n => (
                  <li key={n}><Link to="/names">{n}</Link></li>
                ))}
              </ul>
            </div>
          )}
          {data.related_theophany_ids && data.related_theophany_ids.length > 0 && (
            <div>
              <strong>Related theophanies</strong>
              <ul style={{paddingLeft:'1.25rem', margin:'0.25rem 0'}}>
                {data.related_theophany_ids.map(t => (
                  <li key={t}><code style={{fontSize:'0.8rem'}}>{t}</code></li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {data.related_segments && data.related_segments.length > 0 && (
        <div className="detail-section">
          <h2>Where it surfaces in the <em>Exegesis</em></h2>
          <p style={{fontSize:'0.85rem', color:'var(--text-muted)'}}>
            {data.related_segments.length} segment{data.related_segments.length === 1 ? '' : 's'} from the
            parsed Exegesis match this theophany's vocabulary. Auto-linked by content scoring;
            spot-check before citation.
          </p>
          <ul style={{paddingLeft:'1.25rem', columnCount:2, columnGap:'1.5rem'}}>
            {data.related_segments.slice(0, 25).map(seg_id => (
              <li key={seg_id} style={{fontSize:'0.85rem'}}>
                <Link to={`/segments/${seg_id}`}>{seg_id.replace(/^SEG_EXEG_/, '')}</Link>
              </li>
            ))}
          </ul>
        </div>
      )}

      <ExploreFooter groups={[
        { section: 'Theophanies', items: [
          { label: 'All visionary experiences', to: '/theophanies' },
          ...(data.related_theophany_ids?.slice(0, 3).map(id => {
            const slug = id.toLowerCase().replace(/^theo_/, '').replace(/_/g, '-')
            return { label: id.replace(/^THEO_/, '').replace(/_/g, ' ').toLowerCase(), to: `/theophanies/${slug}` }
          }) || []),
        ]},
        { section: 'Where it surfaces', items: [
          ...(data.related_works || []).slice(0, 3).map(w => ({ label: w, to: '/archive' })),
          ...(data.related_dictionary_terms || []).slice(0, 3).map(t => ({ label: t, to: `/dictionary/${t}` })),
        ]},
        { section: 'Contextual reading', items: [
          { label: 'The Exegesis landing', to: '/exegesis' },
          { label: 'Drugs in PKD essay', to: '/essays/drugs-in-pkd' },
          { label: 'Scholars on PKD', to: '/scholars' },
          { label: `Timeline ${(data.date_start || '').slice(0, 4) || '1974'}`, to: `/timeline/${(data.date_start || '1974').slice(0, 4)}` },
        ]},
      ]} />

      <div style={{marginTop:'2rem', paddingTop:'1rem', borderTop:'1px solid var(--border, rgba(0,0,0,0.1))'}}>
        <Link to="/theophanies">&larr; All theophanies</Link>
      </div>
    </article>
  )
}

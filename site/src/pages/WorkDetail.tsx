import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { useData } from '../hooks/useData'
import EntityLayout from '../components/EntityLayout'

interface RelatedDoc {
  doc_id: string
  title: string
  slug: string
  date_display: string
  doc_type: string
}

interface WorkBiographyEvent {
  bio_id: number | string
  date: string
  category: string
  event: string
  source: string
  source_type?: string
}

interface ChapterSummary {
  chapter_number: number
  chapter_title: string
  locations: string[]
  themes: string[]
  characters: string[]
  artifact_id: string
  summary?: string
}

interface NamedNote {
  name: string
  role?: string
  note?: string
}

interface ReadingNotes {
  structure?: {
    form?: string
    movements?: string[]
    point_of_view?: string
    central_device?: string
    opening_technique?: string
    structural_irony?: string
  }
  characters?: NamedNote[]
  settings?: NamedNote[]
  motifs?: string[]
  significance?: string
  closing_note?: string
}

interface EvidenceItem {
  source?: string
  author?: string
  work?: string
  line?: number
  quote: string
  reading?: string
}

interface EvidenceBlock {
  lane?: string
  total_mentions?: number
  summary?: string
  evidence?: EvidenceItem[]
  gap_noted?: string
  archival_gap?: string
}

interface Contradiction {
  type?: string
  summary: string
  claim_a?: { lane?: string; source?: string; text?: string }
  claim_b?: { lane?: string; source?: string; text?: string }
  editorial_status?: string
  note?: string
}

interface DistinctiveTerm {
  label: string
  entity_id?: string
  count?: number
  distinctiveness?: number
  note?: string
}

interface WorkRecord {
  work_id: string
  canonical_title: string
  slug: string
  author: string
  work_type: string
  category: string
  date_display: string
  date_start: string
  card_summary: string
  page_summary: string
  page_count: number
  source_count: number
  word_count?: number
  themes?: string[]
  related_docs: RelatedDoc[]
  biography_events?: WorkBiographyEvent[]
  first_doc?: { doc_id: string; slug: string; title: string }
  chapter_summaries?: ChapterSummary[]
  all_locations?: string[]
  all_themes?: string[]
  all_characters_mentioned?: { name: string }[]
  has_reading_notes?: boolean
  reading?: ReadingNotes
  distinctive_terms?: DistinctiveTerm[]
  pkd_on_this_work?: EvidenceBlock
  criticism?: EvidenceBlock
  contradictions?: Contradiction[]
  open_questions?: string[]
  reading_provenance?: { status?: string; review_state?: string; note?: string }
  later_use?: string
  award?: string
  written?: string
  original_title?: string
  critical_caution?: string
  ending_correction?: string
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

const TYPE_LABELS: Record<string, string> = {
  novels: 'Novel',
  novel: 'Novel',
  novellas: 'Novella',
  novella: 'Novella',
  novelette: 'Novelette',
  letters: 'Letter',
  letter: 'Letter',
  short_story: 'Short story',
  short_stories: 'Collection',
  essays: 'Essay',
  essay: 'Essay',
  interviews: 'Interview',
  interview: 'Interview',
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
  short_stories: 'Short fiction',
}

const LANE_LABELS: Record<string, string> = {
  A: 'Lane A — fiction',
  B: 'Lane B — Exegesis',
  C: 'Lane C — scholarship',
  D: 'Lane D — synthesis',
  E: "Lane E — Dick's own testimony",
}

function Evidence({ items }: { items: EvidenceItem[] }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
      {items.map((item, i) => (
        <div key={i} style={{ borderLeft: '3px solid var(--accent)', paddingLeft: '1rem' }}>
          <blockquote style={{ margin: '0 0 0.4rem', fontStyle: 'italic' }}>&ldquo;{item.quote}&rdquo;</blockquote>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            {[item.author, item.work || item.source, item.line ? `l.${item.line}` : null].filter(Boolean).join(' · ')}
          </div>
          {item.reading && <p style={{ margin: '0.5rem 0 0', lineHeight: 1.6 }}>{item.reading}</p>}
        </div>
      ))}
    </div>
  )
}

export default function WorkDetail() {
  const { slug } = useParams()
  const { data: work, loading, error } = useData<WorkRecord>(slug ? `works/${slug}.json` : null)
  const { data: themeIndex } = useData<ThemeIndex>('themes/index.json')

  if (loading) return <div className="loading">Loading...</div>

  if (error || !work) {
    return (
      <div className="page-header">
        <h1>Work Not Found</h1>
        <Link to="/works">Back to Works</Link>
      </div>
    )
  }

  const themeMap = new Map((themeIndex?.themes || []).map(theme => [theme.slug, theme]))
  const reading = work.reading
  const structure = reading?.structure

  return (
    <EntityLayout
      title={work.canonical_title}
      entityType="work"
      entityId={work.work_id}
      badges={[
        { label: CATEGORY_LABELS[work.category] || work.category },
        { label: TYPE_LABELS[work.work_type] || work.work_type },
        ...(work.has_reading_notes ? [{ label: 'Close reading', className: 'badge-category' }] : []),
        ...(work.source_count ? [{ label: `${work.source_count} linked docs`, className: 'badge-background' }] : []),
      ]}
      tags={(work.themes || []).map(s => ({ label: themeMap.get(s)?.label || s.replace(/-/g, ' '), to: `/themes/${s}` }))}
      description={[
        work.author,
        work.date_display,
        work.page_count ? `${work.page_count} pp` : null,
        work.word_count ? `${work.word_count.toLocaleString()} words` : null,
      ].filter(Boolean).join(' — ')}
      backLink={{ label: 'Back to Works', to: '/works' }}
    >
      {work.ending_correction && (
        <div className="detail-section" style={{ borderLeft: '3px solid var(--accent)', paddingLeft: '1rem' }}>
          <h2>Correction</h2>
          <p>{work.ending_correction}</p>
        </div>
      )}

      <div className="detail-section">
        <h2>Summary</h2>
        <ReactMarkdown>{work.page_summary || work.card_summary}</ReactMarkdown>
        {(work.original_title || work.award || work.later_use || work.written) && (
          <ul style={{ marginTop: '1rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            {work.written && <li>Written: {work.written}</li>}
            {work.original_title && <li>Originally published as &ldquo;{work.original_title}&rdquo;</li>}
            {work.award && <li>{work.award}</li>}
            {work.later_use && <li>{work.later_use}</li>}
          </ul>
        )}
      </div>

      {structure && (
        <div className="detail-section">
          <h2>Structure</h2>
          {structure.form && <p>{structure.form}</p>}
          {structure.movements && structure.movements.length > 0 && (
            <ol style={{ lineHeight: 1.7 }}>
              {structure.movements.map((m, i) => <li key={i}>{m}</li>)}
            </ol>
          )}
          {structure.point_of_view && <p><strong>Point of view.</strong> {structure.point_of_view}</p>}
          {structure.central_device && <p><strong>Central device.</strong> {structure.central_device}</p>}
          {structure.opening_technique && <p><strong>Opening.</strong> {structure.opening_technique}</p>}
          {structure.structural_irony && <p><strong>Structural irony.</strong> {structure.structural_irony}</p>}
        </div>
      )}

      {reading?.characters && reading.characters.length > 0 && (
        <div className="detail-section">
          <h2>Characters</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {reading.characters.map(c => (
              <div key={c.name}>
                <strong>{c.name}</strong>
                {c.role && <span style={{ color: 'var(--text-muted)' }}> — {c.role}</span>}
                {c.note && <p style={{ margin: '0.25rem 0 0', lineHeight: 1.6 }}>{c.note}</p>}
              </div>
            ))}
          </div>
        </div>
      )}

      {reading?.settings && reading.settings.length > 0 && (
        <div className="detail-section">
          <h2>Settings</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {reading.settings.map(s => (
              <div key={s.name}>
                <strong>{s.name}</strong>
                {s.note && <p style={{ margin: '0.25rem 0 0', lineHeight: 1.6 }}>{s.note}</p>}
              </div>
            ))}
          </div>
        </div>
      )}

      {reading?.motifs && reading.motifs.length > 0 && (
        <div className="detail-section">
          <h2>Motifs</h2>
          <ul style={{ lineHeight: 1.7 }}>
            {reading.motifs.map((m, i) => <li key={i}>{m}</li>)}
          </ul>
        </div>
      )}

      {work.distinctive_terms && work.distinctive_terms.length > 0 && (
        <div className="detail-section">
          <h2>Distinctive Vocabulary</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Terms used far more here than across Dick&rsquo;s fiction as a whole, linked to the dictionary.
          </p>
          <ul style={{ lineHeight: 1.7 }}>
            {work.distinctive_terms.map(t => (
              <li key={t.label}>
                {t.entity_id
                  ? <Link to={`/dictionary/${t.entity_id}`}>{t.label}</Link>
                  : <strong>{t.label}</strong>}
                {t.distinctiveness && (
                  <span style={{ color: 'var(--text-muted)' }}> — {t.distinctiveness}× baseline</span>
                )}
                {t.note && <span> — {t.note}</span>}
              </li>
            ))}
          </ul>
        </div>
      )}

      {reading?.significance && (
        <div className="detail-section">
          <h2>Significance</h2>
          <p style={{ lineHeight: 1.7 }}>{reading.significance}</p>
          {reading.closing_note && (
            <p style={{ marginTop: '0.75rem', fontStyle: 'italic', color: 'var(--text-muted)' }}>{reading.closing_note}</p>
          )}
        </div>
      )}

      {work.critical_caution && (
        <div className="detail-section">
          <h2>A Caution on the Criticism</h2>
          <p>{work.critical_caution}</p>
        </div>
      )}

      {work.pkd_on_this_work && (work.pkd_on_this_work.evidence?.length || work.pkd_on_this_work.summary) && (
        <div className="detail-section">
          <h2>Dick on This Work</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            {LANE_LABELS[work.pkd_on_this_work.lane || 'E']}
            {work.pkd_on_this_work.total_mentions ? ` · ${work.pkd_on_this_work.total_mentions} mentions found` : ''}
          </p>
          {work.pkd_on_this_work.summary && <p>{work.pkd_on_this_work.summary}</p>}
          {work.pkd_on_this_work.evidence && <Evidence items={work.pkd_on_this_work.evidence} />}
          {(work.pkd_on_this_work.gap_noted || work.pkd_on_this_work.archival_gap) && (
            <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>
              <strong>Gap in the archive.</strong> {work.pkd_on_this_work.gap_noted || work.pkd_on_this_work.archival_gap}
            </p>
          )}
        </div>
      )}

      {work.criticism && work.criticism.evidence && work.criticism.evidence.length > 0 && (
        <div className="detail-section">
          <h2>Critical Reception</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            {LANE_LABELS[work.criticism.lane || 'C']}
            {work.criticism.total_mentions ? ` · ${work.criticism.total_mentions} mentions found` : ''}
          </p>
          <Evidence items={work.criticism.evidence} />
        </div>
      )}

      {work.contradictions && work.contradictions.length > 0 && (
        <div className="detail-section">
          <h2>Contradictions</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Held open on purpose. Disagreement between sources is evidence, not a defect to be tidied away.
          </p>
          {work.contradictions.map((c, i) => (
            <div key={i} style={{ borderLeft: '3px solid var(--accent)', paddingLeft: '1rem', marginBottom: '1.25rem' }}>
              <p style={{ margin: '0 0 0.6rem' }}><strong>{c.summary}</strong></p>
              {c.claim_a && (
                <p style={{ margin: '0 0 0.35rem' }}>
                  <span style={{ color: 'var(--text-muted)' }}>{c.claim_a.source} — </span>{c.claim_a.text}
                </p>
              )}
              {c.claim_b && (
                <p style={{ margin: '0 0 0.35rem' }}>
                  <span style={{ color: 'var(--text-muted)' }}>{c.claim_b.source} — </span>{c.claim_b.text}
                </p>
              )}
              {c.note && <p style={{ margin: '0.5rem 0 0', lineHeight: 1.6 }}>{c.note}</p>}
              {c.editorial_status && (
                <span className="badge badge-background" style={{ fontSize: '0.75rem' }}>
                  {c.editorial_status.replace(/_/g, ' ')}
                </span>
              )}
            </div>
          ))}
        </div>
      )}

      {work.open_questions && work.open_questions.length > 0 && (
        <div className="detail-section">
          <h2>Open Questions</h2>
          <ul style={{ lineHeight: 1.7 }}>
            {work.open_questions.map((q, i) => <li key={i}>{q}</li>)}
          </ul>
        </div>
      )}

      {work.chapter_summaries && work.chapter_summaries.length > 0 && (
        <div className="detail-section">
          <h2>Chapter Summaries</h2>
          <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>
            {work.chapter_summaries.length} chapters systematically read and preserved — no re-reading required.
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            {[...work.chapter_summaries].sort((a, b) => a.chapter_number - b.chapter_number).map(ch => (
              <div key={ch.chapter_number} style={{ borderLeft: '3px solid var(--accent)', paddingLeft: '1rem' }}>
                <h3 style={{ margin: '0 0 0.4rem', fontSize: '1rem' }}>
                  Chapter {ch.chapter_number}{ch.chapter_title ? `: ${ch.chapter_title}` : ''}
                </h3>
                {ch.summary && <p style={{ margin: '0 0 0.5rem', lineHeight: '1.6' }}>{ch.summary}</p>}
                <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.8rem', color: 'var(--text-muted)', flexWrap: 'wrap' }}>
                  {ch.locations?.length > 0 && (
                    <span><strong>Locations:</strong> {ch.locations.slice(0, 4).join(', ')}{ch.locations.length > 4 ? ` +${ch.locations.length - 4}` : ''}</span>
                  )}
                  {ch.characters?.length > 0 && (
                    <span><strong>Characters:</strong> {ch.characters.slice(0, 4).join(', ')}{ch.characters.length > 4 ? ` +${ch.characters.length - 4}` : ''}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {work.all_locations && work.all_locations.length > 0 && (
        <div className="detail-section">
          <h2>Locations Across All Chapters</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
            {work.all_locations.map(loc => (
              <span key={loc} className="badge badge-background" style={{ fontSize: '0.8rem' }}>{loc}</span>
            ))}
          </div>
        </div>
      )}

      {work.all_characters_mentioned && work.all_characters_mentioned.length > 0 && (
        <div className="detail-section">
          <h2>Characters Mentioned</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
            {work.all_characters_mentioned.map(c => (
              <span key={c.name} className="badge" style={{ fontSize: '0.8rem' }}>{c.name}</span>
            ))}
          </div>
        </div>
      )}

      {work.category === 'novels' && (
        <div className="detail-section">
          <h2>PKD on PKD</h2>
          <p>
            <Link to={`/pkd-on-pkd/${work.slug}`}>Open the PKD on PKD catalog for this novel</Link>
          </p>
        </div>
      )}

      {work.biography_events && work.biography_events.length > 0 && (
        <div className="detail-section">
          <h2>Biographical Timeline</h2>
          <p>Key biography and letter moments tied to this work.</p>
          <ul>
            {work.biography_events.map(ev => (
              <li key={`${work.slug}-${ev.bio_id}`}>
                <strong>{ev.date}</strong> {ev.event}
                <span style={{ color: 'var(--text-muted)' }}> ({ev.source || ev.source_type || ev.category})</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {work.related_docs && work.related_docs.length > 0 && (
        <div className="detail-section">
          <h2>Linked Archive Docs</h2>
          <ul>
            {work.related_docs.map(doc => (
              <li key={doc.doc_id}>
                <Link to={`/archive/${doc.slug}`}>{doc.title}</Link>
                {doc.date_display && <span style={{ color: 'var(--text-muted)' }}> {doc.date_display}</span>}
                <span style={{ color: 'var(--text-muted)' }}> ({TYPE_LABELS[doc.doc_type] || doc.doc_type})</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="detail-section">
        <h2>Metadata</h2>
        <ul>
          <li>Work type: {TYPE_LABELS[work.work_type] || work.work_type}</li>
          <li>Category: {CATEGORY_LABELS[work.category] || work.category}</li>
          <li>Linked documents: {work.source_count}</li>
          {work.first_doc && <li>First known record: {work.first_doc.title}</li>}
          {work.reading_provenance && (
            <li>
              Reading status: {work.reading_provenance.status} / {work.reading_provenance.review_state}
              {work.reading_provenance.note && (
                <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '0.25rem' }}>
                  {work.reading_provenance.note}
                </div>
              )}
            </li>
          )}
        </ul>
      </div>
    </EntityLayout>
  )
}

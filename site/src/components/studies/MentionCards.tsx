import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import LaneBadge from './LaneBadge'

export interface MentionCard {
  id: string
  citation: string
  date?: string | null
  source_type: string
  published_folio?: string | null
  seg_id?: string | null
  doc_id?: string | null
  lane: string
  register: string
  relevance: number
  concepts: string[]
  /** Editorial summary of the whole passage and its place in the work. */
  context: string
  /** Short verbatim quotation of the sentence the passage turns on. */
  pith: string
  speaker: string
  editorial_note?: string | null
}

interface Props {
  cards: MentionCard[]
}

const GROUPS: { key: string; label: string; blurb: string; match: (c: MentionCard) => boolean }[] = [
  {
    key: '1976',
    label: 'The Exegesis — 15 September 1976',
    blurb: 'The first reading of The Ticket That Exploded, and the modification Dick made the same day.',
    match: c => c.source_type === 'exegesis_segment' && (c.date || '').startsWith('1976'),
  },
  {
    key: '1978',
    label: 'The Exegesis — 10 October 1978',
    blurb: '"William Burroughs is correct" — alongside three incompatible readings in the same section.',
    match: c => c.source_type === 'exegesis_segment' && (c.date || '').startsWith('1978'),
  },
  {
    key: '1981',
    label: 'The Exegesis — 16 April 1981',
    blurb: 'The reversal, and the passages in the same sitting that refuse to hold it.',
    match: c => c.source_type === 'exegesis_segment' && (c.date || '').startsWith('1981'),
  },
  {
    key: 'published',
    label: 'The Exegesis — passages printed only in the 2011 edition',
    blurb: 'Four folios in the Jackson and Lethem selection that our folder transcriptions do not contain.',
    match: c => c.source_type === 'exegesis_published',
  },
  {
    key: 'letters',
    label: 'Letters',
    blurb: 'Eleven letters, 1976 to 1981. Dick explaining himself to someone else.',
    match: c => c.source_type === 'letter',
  },
  {
    key: 'interview',
    label: 'Interview and essay',
    blurb: 'Dick on the word virus in his own voice, and his own account of language as control.',
    match: c => c.source_type === 'interview',
  },
  {
    key: 'scholarship',
    label: 'Biography and scholarship',
    blurb: 'What Sutin, Lapoujade, Butler and Davis say — not Dick.',
    match: c => c.source_type === 'criticism',
  },
]

export default function MentionCards({ cards }: Props) {
  const [open, setOpen] = useState<string | null>(null)

  const grouped = useMemo(
    () =>
      GROUPS.map(g => ({ ...g, items: (cards || []).filter(g.match) })).filter(
        g => g.items.length > 0,
      ),
    [cards],
  )

  if (!cards || cards.length === 0) return null

  return (
    <div className="detail-section">
      <h2>Every mention, one by one</h2>
      <p style={{ fontSize: '0.9rem', lineHeight: 1.65, color: 'var(--text-secondary)' }}>
        {cards.length} passages in the archive refer to Burroughs or to his word virus.
        Each card summarises the whole passage and where it sits in the work, then quotes
        the sentence it turns on. Quotations are verbatim, including the transcription
        irregularities of the source; every one is machine-checked against the underlying
        text before it is published. Follow the link on any card to read the full entry.
      </p>

      {grouped.map(group => (
        <div key={group.key} className="mention-group">
          <h3 className="mention-group-heading">
            {group.label}
            <span className="mention-group-count">{group.items.length}</span>
          </h3>
          <p className="mention-group-blurb">{group.blurb}</p>

          <div className="mention-cards">
            {group.items.map(card => {
              const isOpen = open === card.id
              return (
                <div key={card.id} id={`card-${card.id}`} className="mention-card">
                  <div className="mention-card-head">
                    <LaneBadge lane={card.lane} />
                    <span className="mention-card-cite">{card.citation}</span>
                    {card.published_folio && (
                      <span className="mention-card-folio">[{card.published_folio}]</span>
                    )}
                  </div>

                  <p className="mention-card-context">{card.context}</p>

                  <blockquote className="mention-card-pith">
                    <p>{card.pith}</p>
                    <cite>&mdash; {card.speaker}</cite>
                  </blockquote>

                  <div className="mention-card-foot">
                    {card.concepts.slice(0, 5).map(t => (
                      <span key={t} className="entity-tag">
                        {t}
                      </span>
                    ))}
                    {card.seg_id && (
                      <Link to={`/segments/${card.seg_id}`} className="mention-card-link">
                        Read the full entry &rarr;
                      </Link>
                    )}
                    {card.editorial_note && (
                      <button
                        className="mention-card-note-toggle"
                        onClick={() => setOpen(isOpen ? null : card.id)}
                      >
                        {isOpen ? 'Hide editorial note' : 'Editorial note'}
                      </button>
                    )}
                  </div>

                  {isOpen && card.editorial_note && (
                    <p className="mention-card-note">{card.editorial_note}</p>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}

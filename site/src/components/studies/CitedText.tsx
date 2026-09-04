import { Fragment } from 'react'
import type { MentionCard } from './MentionCards'

interface Props {
  text: string
  cards: MentionCard[]
}

const CITE = /\{\{([A-Za-z0-9-]+)\}\}/g

/**
 * Renders dossier prose, turning {{finding-id}} markers into superscript links
 * to the mention card for that passage. The seeder refuses to build if a marker
 * does not resolve, so an unresolved one here means stale exported data.
 */
export default function CitedText({ text, cards }: Props) {
  const byId = new Map(cards.map(c => [c.id, c]))
  const parts: React.ReactNode[] = []
  let last = 0
  let n = 0

  for (const m of text.matchAll(CITE)) {
    const at = m.index ?? 0
    if (at > last) parts.push(text.slice(last, at))
    const card = byId.get(m[1])
    parts.push(
      <a
        key={`${m[1]}-${n++}`}
        href={`#card-${m[1]}`}
        className="cite-ref"
        title={card ? `${card.citation} — ${card.speaker}` : m[1]}
        onClick={e => {
          e.preventDefault()
          const el = document.getElementById(`card-${m[1]}`)
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' })
            el.classList.add('mention-card-flash')
            window.setTimeout(() => el.classList.remove('mention-card-flash'), 1600)
          }
        }}
      >
        {card ? sourceLabel(card) : m[1]}
      </a>,
    )
    last = at + m[0].length
  }
  if (last < text.length) parts.push(text.slice(last))

  return (
    <>
      {parts.map((p, i) => (
        <Fragment key={i}>{p}</Fragment>
      ))}
    </>
  )
}

/** Short human label: the folio if the passage was printed, else date or source. */
function sourceLabel(c: MentionCard): string {
  if (c.published_folio) return `[${c.published_folio}]`
  if (c.source_type === 'exegesis_segment' && c.date) {
    const [y, m, d] = c.date.split('-')
    return `[Exeg. ${d}.${m}.${y.slice(2)}]`
  }
  if (c.source_type === 'letter') return '[letter]'
  if (c.source_type === 'interview') return '[interview]'
  if (c.source_type === 'criticism') return '[scholarship]'
  return '[source]'
}

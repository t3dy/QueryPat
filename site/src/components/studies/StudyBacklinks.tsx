import { Link } from 'react-router-dom'
import { useData } from '../../hooks/useData'

/** One dossier that discusses the entity on the current page. */
interface StudyLink {
  study_id: string
  slug: string
  name: string
  description?: string | null
  relation?: string
  /** Browse facet of the dossier that corresponds to this entity, if any. */
  facet?: string | null
  /** Number of passages carrying that facet. */
  count?: number | null
  /** Mention cards cut from this segment or document. */
  cards?: string[]
}

type LinkKind = 'terms' | 'names' | 'segments' | 'documents' | 'works'
type LinksIndex = Record<LinkKind, Record<string, StudyLink[]>>

interface Props {
  kind: LinkKind
  /** Slug (terms, names, documents, works) or seg_id (segments). */
  id: string | undefined
}

/**
 * "Studied in depth": links from an entity page into the authored study
 * dossiers that discuss it, from studies/links.json. Renders nothing when no
 * dossier mentions the entity.
 */
export default function StudyBacklinks({ kind, id }: Props) {
  const { data } = useData<LinksIndex>('studies/links.json')
  const entries = id ? data?.[kind]?.[id] : undefined
  if (!entries || entries.length === 0) return null

  return (
    <aside className="study-backlinks">
      <h3>Studied in depth</h3>
      <ul>
        {entries.map(e => {
          const base = `/studies/${e.study_id}/${e.slug}`
          if (e.cards && e.cards.length > 0) {
            return (
              <li key={`${e.study_id}/${e.slug}`}>
                <Link to={`${base}#card-${e.cards[0]}`}>{e.name}</Link>{' '}
                <span className="study-backlinks-desc">
                  — {e.cards.length === 1 ? 'a passage from this source is' : `${e.cards.length} passages from this source are`}{' '}
                  discussed there.
                </span>
                {e.cards.length > 1 && (
                  <span className="study-backlinks-desc">
                    {' '}
                    {e.cards.map((c, i) => (
                      <span key={c}>
                        {i > 0 && ', '}
                        <Link to={`${base}#card-${c}`}>{i + 1}</Link>
                      </span>
                    ))}
                  </span>
                )}
              </li>
            )
          }
          const to = e.facet
            ? `${base}?facet=${encodeURIComponent(e.facet)}#mentions`
            : base
          return (
            <li key={`${e.study_id}/${e.slug}`}>
              <Link to={to}>{e.name}</Link>
              {e.facet && e.count ? (
                <span className="study-backlinks-desc">
                  {' '}— {e.count} passage{e.count === 1 ? '' : 's'} on {e.facet}
                </span>
              ) : e.description ? (
                <span className="study-backlinks-desc"> — {e.description}</span>
              ) : null}
            </li>
          )
        })}
      </ul>
    </aside>
  )
}

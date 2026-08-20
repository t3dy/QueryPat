import { Link } from 'react-router-dom'
import type { Profile } from '../lib/supabase'
import { AREA_LABEL, lookup, useSiteVocab, type Option } from './useSiteVocab'

function Tags({ items }: { items: Option[] }) {
  return (
    <div className="cm-chips">
      {items.map(o => (
        o.to
          ? <Link key={o.value} className="cm-chip-tag cm-chip-link" to={o.to}>{o.label}</Link>
          : <span key={o.value} className="cm-chip-tag">{o.label}</span>
      ))}
    </div>
  )
}

function Row({ label, items }: { label: string; items: Option[] }) {
  if (!items.length) return null
  return (
    <div className="cm-detail-row">
      <span className="cm-label">{label}</span>
      <Tags items={items} />
    </div>
  )
}

/**
 * The self-described half of a profile: where someone works in the archive,
 * what they read, what they're chasing. Everything that maps onto a page here
 * renders as a link into it.
 */
export default function ProfileDetails({ profile }: { profile: Profile }) {
  const vocab = useSiteVocab()

  const areas = (profile.areas ?? [])
    .map(v => AREA_LABEL.get(v) ?? { value: v, label: v })
  const themes = (profile.favorite_themes ?? []).map(v => lookup(vocab.themes, v))
  const works = (profile.favorite_works ?? []).map(v => lookup(vocab.works, v))
  const interests = (profile.research_interests ?? []).map(v => lookup(vocab.interests, v))

  const empty =
    !profile.affiliation && !profile.website &&
    !areas.length && !themes.length && !works.length && !interests.length

  if (empty) return null

  const site = profile.website?.trim()
  const href = site && (/^https?:\/\//i.test(site) ? site : `https://${site}`)

  return (
    <section className="cm-profile-details">
      {(profile.affiliation || href) && (
        <p className="cm-detail-line">
          {profile.affiliation}
          {profile.affiliation && href && ' · '}
          {href && <a href={href} target="_blank" rel="noopener noreferrer nofollow">{site}</a>}
        </p>
      )}
      <Row label="Works on" items={areas} />
      <Row label="Research interests" items={interests} />
      <Row label="Favourite themes" items={themes} />
      <Row label="Favourite works" items={works} />
    </section>
  )
}

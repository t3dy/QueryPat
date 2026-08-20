import { useState } from 'react'
import type { Profile } from '../lib/supabase'
import { AREAS, lookup, useSiteVocab, type Option } from './useSiteVocab'

export type ProfilePatch = Partial<Omit<Profile, 'id' | 'username' | 'role' | 'created_at'>>

interface Props {
  profile: Profile
  onSave: (patch: ProfilePatch) => Promise<void>
  onCancel: () => void
}

// ── Pickers ─────────────────────────────────────────────────────

function CheckboxGrid({
  options, selected, onToggle,
}: {
  options: Option[]
  selected: string[]
  onToggle: (value: string) => void
}) {
  return (
    <div className="cm-checkgrid">
      {options.map(o => (
        <label key={o.value} className="cm-check">
          <input
            type="checkbox"
            checked={selected.includes(o.value)}
            onChange={() => onToggle(o.value)}
          />
          <span>{o.label}</span>
        </label>
      ))}
    </div>
  )
}

/**
 * A dropdown that adds to a chip list — the workable shape for long option
 * sets like the 73 works, where a checkbox grid would swamp the page.
 */
function ChipPicker({
  options, selected, onAdd, onRemove, prompt, custom, max,
}: {
  options: Option[]
  selected: string[]
  onAdd: (value: string) => void
  onRemove: (value: string) => void
  prompt: string
  /** Also allow typing something that isn't in the list. */
  custom?: string
  max: number
}) {
  const [typed, setTyped] = useState('')
  const full = selected.length >= max
  const groups = [...new Set(options.map(o => o.group).filter(Boolean))] as string[]
  const available = options.filter(o => !selected.includes(o.value))

  function addTyped() {
    const v = typed.trim()
    if (!v || full || selected.some(s => s.toLowerCase() === v.toLowerCase())) return setTyped('')
    onAdd(v)
    setTyped('')
  }

  return (
    <>
      {selected.length > 0 && (
        <div className="cm-chips">
          {selected.map(v => (
            <span key={v} className="cm-chip-tag">
              {lookup(options, v).label}
              <button type="button" onClick={() => onRemove(v)} aria-label={`Remove ${v}`}>×</button>
            </span>
          ))}
        </div>
      )}

      <div className="cm-picker-row">
        <select
          value=""
          disabled={full || !options.length}
          onChange={e => { if (e.target.value) onAdd(e.target.value) }}
        >
          <option value="">{options.length ? prompt : 'Loading…'}</option>
          {groups.length
            ? groups.map(g => (
                <optgroup key={g} label={g}>
                  {available.filter(o => o.group === g).map(o => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </optgroup>
              ))
            : available.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>

        {custom && (
          <>
            <input
              type="text"
              value={typed}
              disabled={full}
              placeholder={custom}
              onChange={e => setTyped(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addTyped() } }}
            />
            <button type="button" className="cm-btn cm-btn-sm" onClick={addTyped} disabled={full || !typed.trim()}>
              Add
            </button>
          </>
        )}
      </div>
      {full && <span className="cm-hint">That’s the maximum of {max}. Remove one to add another.</span>}
    </>
  )
}

// ── The form ────────────────────────────────────────────────────

export default function ProfileEditor({ profile, onSave, onCancel }: Props) {
  const vocab = useSiteVocab()
  const [displayName, setDisplayName] = useState(profile.display_name ?? '')
  const [bio, setBio] = useState(profile.bio ?? '')
  const [affiliation, setAffiliation] = useState(profile.affiliation ?? '')
  const [website, setWebsite] = useState(profile.website ?? '')
  const [areas, setAreas] = useState<string[]>(profile.areas ?? [])
  const [themes, setThemes] = useState<string[]>(profile.favorite_themes ?? [])
  const [works, setWorks] = useState<string[]>(profile.favorite_works ?? [])
  const [interests, setInterests] = useState<string[]>(profile.research_interests ?? [])
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const toggle = (list: string[], set: (v: string[]) => void, value: string) =>
    set(list.includes(value) ? list.filter(v => v !== value) : [...list, value])

  const add = (list: string[], set: (v: string[]) => void, value: string) => {
    if (!list.includes(value)) set([...list, value])
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await onSave({
        display_name: displayName.trim() || null,
        bio: bio.trim() || null,
        affiliation: affiliation.trim() || null,
        website: website.trim() || null,
        areas,
        favorite_themes: themes,
        favorite_works: works,
        research_interests: interests,
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not save your profile.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <form className="card cm-form cm-profile-editor" onSubmit={submit}>
      <fieldset className="cm-fieldset">
        <legend>About you</legend>
        <label className="cm-field">
          <span className="cm-label">Display name</span>
          <input value={displayName} onChange={e => setDisplayName(e.target.value)} maxLength={60} />
          <span className="cm-hint">Shown instead of @{profile.username}, if you set one.</span>
        </label>
        <label className="cm-field">
          <span className="cm-label">Bio</span>
          <textarea value={bio} onChange={e => setBio(e.target.value)} maxLength={400} rows={3} />
          <span className="cm-hint">{bio.length}/400</span>
        </label>
        <label className="cm-field">
          <span className="cm-label">Affiliation</span>
          <input
            value={affiliation}
            onChange={e => setAffiliation(e.target.value)}
            maxLength={120}
            placeholder="University, journal, reading group — or “independent scholar”"
          />
        </label>
        <label className="cm-field">
          <span className="cm-label">Website</span>
          <input
            value={website}
            onChange={e => setWebsite(e.target.value)}
            maxLength={200}
            placeholder="https://…"
          />
        </label>
      </fieldset>

      <fieldset className="cm-fieldset">
        <legend>Parts of the archive you work on</legend>
        <span className="cm-hint">
          Tick the sections you know best. Others can see where your attention is, and it shows on
          your public profile as links into those sections.
        </span>
        <CheckboxGrid
          options={AREAS}
          selected={areas}
          onToggle={v => toggle(areas, setAreas, v)}
        />
      </fieldset>

      <fieldset className="cm-fieldset">
        <legend>Favourite themes</legend>
        <span className="cm-hint">The recurring preoccupations you find most interesting.</span>
        {vocab.loaded ? (
          <CheckboxGrid
            options={vocab.themes}
            selected={themes}
            onToggle={v => toggle(themes, setThemes, v)}
          />
        ) : (
          <span className="cm-muted">Loading themes…</span>
        )}
      </fieldset>

      <fieldset className="cm-fieldset">
        <legend>Favourite works</legend>
        <span className="cm-hint">
          Pick from the novels, stories, letters, and primary sources catalogued here.
        </span>
        <ChipPicker
          options={vocab.works}
          selected={works}
          onAdd={v => add(works, setWorks, v)}
          onRemove={v => setWorks(works.filter(x => x !== v))}
          prompt="Add a work…"
          max={40}
        />
      </fieldset>

      <fieldset className="cm-fieldset">
        <legend>Research interests</legend>
        <span className="cm-hint">
          Choose from the subjects this archive covers, or type your own.
        </span>
        <ChipPicker
          options={vocab.interests}
          selected={interests}
          onAdd={v => add(interests, setInterests, v)}
          onRemove={v => setInterests(interests.filter(x => x !== v))}
          prompt="Add a suggested interest…"
          custom="Or type your own…"
          max={40}
        />
      </fieldset>

      {error && <p className="cm-error">{error}</p>}

      <div className="cm-form-actions">
        <button className="cm-btn cm-btn-primary" disabled={busy}>
          {busy ? 'Saving…' : 'Save profile'}
        </button>
        <button type="button" className="cm-btn" onClick={onCancel} disabled={busy}>Cancel</button>
      </div>
    </form>
  )
}

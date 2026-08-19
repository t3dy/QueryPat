const UNITS: [Intl.RelativeTimeFormatUnit, number][] = [
  ['year', 31536000], ['month', 2592000], ['week', 604800],
  ['day', 86400], ['hour', 3600], ['minute', 60],
]

const rtf = new Intl.RelativeTimeFormat(undefined, { numeric: 'auto' })

export function timeAgo(iso: string): string {
  const seconds = (Date.now() - new Date(iso).getTime()) / 1000
  for (const [unit, size] of UNITS) {
    if (seconds >= size) return rtf.format(-Math.floor(seconds / size), unit)
  }
  return 'just now'
}

/** "/studies/ai/scenes/42" -> "Studies › Ai › Scenes › 42" */
export function pathLabel(path: string): string {
  const parts = path.split('/').filter(Boolean)
  if (!parts.length) return 'Dashboard'
  return parts
    .map(p => decodeURIComponent(p).replace(/[-_]/g, ' ').replace(/^\w/, c => c.toUpperCase()))
    .join(' › ')
}

/** "1 source" / "2 sources" — plural only when it should be. */
export function plural(n: number, one: string, many = one + 's'): string {
  return `${n} ${n === 1 ? one : many}`
}

/** Trim a pasted selection down to something storable. */
export function normalizeQuote(text: string, max = 1200): string {
  const clean = text.replace(/\s+/g, ' ').trim()
  return clean.length > max ? clean.slice(0, max - 1) + '…' : clean
}

/**
 * A shareable link to one contribution: the page it belongs to, plus a ?c=
 * marker the comments drawer picks up and scrolls to.
 */
export function permalink(targetPath: string, id: number): string {
  return `${window.location.origin}${import.meta.env.BASE_URL}#${targetPath}?c=${id}`
}

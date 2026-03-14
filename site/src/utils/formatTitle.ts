/**
 * Convert raw segment filenames like "1975-02-27_Claudia_01.txt"
 * or "U_Dorothy_69.txt" into human-readable titles like
 * "Letter to Claudia, Feb 27 1975 (part 1)" or "Letter to Dorothy (part 69)"
 */

const MONTH_NAMES = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]

export function formatSegmentTitle(raw: string | null | undefined, segId?: string): string {
  const src = raw || segId || ''
  // Strip .txt extension
  const name = src.replace(/\.txt$/i, '').replace(/^SEG_EXEG_/, '')

  // Pattern: YYYY-MM-DD_Recipient_NN or U_Recipient_NN or YYYY-MM-DD_SECTION_NNN_NN
  const dated = name.match(
    /^(\d{4})-(\d{2})-(\d{2})_([A-Za-z]+)_(\d+)$/
  )
  if (dated) {
    const [, year, month, day, recipient, part] = dated
    const monthName = MONTH_NAMES[parseInt(month, 10) - 1] || month
    if (recipient === 'SECTION') {
      return `Exegesis entry, ${monthName} ${parseInt(day, 10)} ${year}`
    }
    const partNum = parseInt(part, 10)
    const partStr = partNum > 1 ? ` (part ${partNum})` : ''
    return `Letter to ${recipient}, ${monthName} ${parseInt(day, 10)} ${year}${partStr}`
  }

  // Pattern: YYYY-MM-DD_SECTION_NNN_NN
  const sectionDated = name.match(
    /^(\d{4})-(\d{2})-(\d{2})_SECTION_(\d+)_(\d+)$/
  )
  if (sectionDated) {
    const [, year, month, day, , part] = sectionDated
    const monthName = MONTH_NAMES[parseInt(month, 10) - 1] || month
    const partNum = parseInt(part, 10)
    const partStr = partNum > 1 ? ` (part ${partNum})` : ''
    return `Exegesis entry, ${monthName} ${parseInt(day, 10)} ${year}${partStr}`
  }

  // Pattern: U_Recipient_NN (undated)
  const undated = name.match(/^U_([A-Za-z]+)_(\d+)$/)
  if (undated) {
    const [, recipient, part] = undated
    if (recipient === 'SECTION') {
      return `Exegesis entry (undated)`
    }
    const partNum = parseInt(part, 10)
    const partStr = partNum > 1 ? ` (part ${partNum})` : ''
    return `Letter to ${recipient}${partStr}`
  }

  // Fallback: clean up underscores and extensions
  return name.replace(/_/g, ' ').replace(/\s+/g, ' ').trim() || 'Untitled segment'
}

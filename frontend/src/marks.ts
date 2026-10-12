import type { Mention } from './api'

export type Segment = { text: string; mention?: Mention }

/**
 * Split the posting into plain text and marked skill mentions.
 *
 * Offsets from the backend count Unicode code points (Python string indexes), while
 * JavaScript strings index UTF-16 units, so slice an array of code points instead.
 */
export function segment(text: string, mentions: Mention[]): Segment[] {
  const chars = Array.from(text)
  const segments: Segment[] = []
  let cursor = 0

  for (const mention of [...mentions].sort((a, b) => a.start - b.start)) {
    // Skip anything that overlaps the previous mark or points past the text.
    if (mention.start < cursor || mention.end > chars.length || mention.end <= mention.start) {
      continue
    }
    if (mention.start > cursor) segments.push({ text: chars.slice(cursor, mention.start).join('') })
    segments.push({ text: chars.slice(mention.start, mention.end).join(''), mention })
    cursor = mention.end
  }
  if (cursor < chars.length) segments.push({ text: chars.slice(cursor).join('') })
  return segments
}

const MAX_TITLE_LENGTH = 100

/**
 * Split off the posting's first line as its title, so the marked sheet reads as a document.
 * Only a short first line without marks counts; anything else stays in the body.
 */
export function splitTitle(segments: Segment[]): { title: string | null; body: Segment[] } {
  const first = segments[0]
  const newline = first && !first.mention ? first.text.indexOf('\n') : -1
  const title = newline > 0 ? first.text.slice(0, newline) : ''
  if (title.trim() === '' || title.length > MAX_TITLE_LENGTH) {
    return { title: null, body: segments }
  }
  const rest = first.text.slice(newline + 1)
  return { title, body: rest ? [{ text: rest }, ...segments.slice(1)] : segments.slice(1) }
}

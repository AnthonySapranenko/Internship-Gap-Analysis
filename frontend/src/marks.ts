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

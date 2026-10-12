import { describe, expect, it } from 'vitest'
import { segment } from './marks'

const parts = (text: string, mentions: { skill: string; start: number; end: number }[]) =>
  segment(text, mentions).map((s) => (s.mention ? `[${s.text}]` : s.text))

describe('segment', () => {
  it('splits text around mentions in order', () => {
    expect(
      parts('Python and Git', [
        { skill: 'Git', start: 11, end: 14 },
        { skill: 'Python', start: 0, end: 6 },
      ]),
    ).toEqual(['[Python]', ' and ', '[Git]'])
  })

  it('counts code points, so emoji before a mention do not shift it', () => {
    // Python's offsets: "🚀 " is 2 code points but 3 UTF-16 units.
    expect(parts('🚀 SQL!', [{ skill: 'SQL', start: 2, end: 5 }])).toEqual(['🚀 ', '[SQL]', '!'])
  })

  it('ignores overlapping or out-of-range mentions', () => {
    expect(
      parts('React Native', [
        { skill: 'React Native', start: 0, end: 12 },
        { skill: 'React', start: 0, end: 5 },
        { skill: 'Go', start: 20, end: 22 },
      ]),
    ).toEqual(['[React Native]'])
  })
})

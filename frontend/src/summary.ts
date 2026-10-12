import type { AnalysisResult, RequirementLevel } from './api'

export const LEVEL_ORDER: RequirementLevel[] = ['required', 'preferred', 'unspecified']

/** How many requirements at each level are matched, skipping levels with none. */
export function summarize(result: AnalysisResult) {
  return LEVEL_ORDER.map((level) => {
    const atLevel = result.matches.filter((m) => m.requirement.level === level)
    return {
      level,
      total: atLevel.length,
      matched: atLevel.filter((m) => m.status === 'matched').length,
    }
  }).filter((row) => row.total > 0)
}

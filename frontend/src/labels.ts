import type { MatchStatus, RequirementLevel } from './api'

export const LEVEL_LABEL: Record<RequirementLevel, string> = {
  required: 'Required',
  preferred: 'Preferred',
  unspecified: 'Mentioned',
}

export const STATUS_LABEL: Record<MatchStatus, string> = {
  matched: 'Matched',
  missing: 'Missing',
  unlisted: 'Not listed',
}

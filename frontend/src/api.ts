// Types mirror backend/src/gap_analyzer/models.py.

export type Proficiency = 'none' | 'beginner' | 'intermediate' | 'advanced'
export type RequirementLevel = 'required' | 'preferred' | 'unspecified'
export type MatchStatus = 'matched' | 'missing' | 'unlisted'

export interface ProfileSkill {
  name: string
  proficiency: Proficiency | null
}

export interface Requirement {
  skill: string
  level: RequirementLevel
  evidence: string
}

export interface RequirementMatch {
  requirement: Requirement
  status: MatchStatus
  profile_skill: ProfileSkill | null
  explanation: string
}

/** Where a skill appears in the posting, as code point offsets. */
export interface Mention {
  skill: string
  start: number
  end: number
}

export interface AnalysisResult {
  matches: RequirementMatch[]
  mentions: Mention[]
}

export interface CatalogSkill {
  name: string
  category: string
  aliases: string[]
}

export class ApiError extends Error {}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response
  try {
    response = await fetch(path, init)
  } catch {
    throw new ApiError('Could not reach the server. Is the backend running?')
  }

  if (!response.ok) {
    let message = `Request failed (HTTP ${response.status}).`
    try {
      // FastAPI validation errors: { detail: [{ msg: "..." }, ...] }
      const body = (await response.json()) as { detail?: { msg: string }[] | string }
      if (Array.isArray(body.detail)) message = body.detail.map((d) => d.msg).join(' ')
      else if (typeof body.detail === 'string') message = body.detail
    } catch {
      // Keep the generic message.
    }
    throw new ApiError(message)
  }

  return (await response.json()) as T
}

export function fetchSkills(): Promise<CatalogSkill[]> {
  return request('/api/skills')
}

export function analyze(text: string, skills: ProfileSkill[]): Promise<AnalysisResult> {
  return request('/api/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ internship: { text }, profile: { skills } }),
  })
}

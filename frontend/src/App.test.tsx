import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { AnalysisResult, ProfileSkill } from './api'
import App from './App'

const POSTING = 'Requirements:\n- Python and Docker'

function requirement(skill: string, start: number) {
  return { skill, start, end: start + skill.length }
}

// A stand-in for the backend: Python and Docker are required; status follows the profile.
function fakeAnalyze(skills: ProfileSkill[]): AnalysisResult {
  const has = (name: string) => skills.some((s) => s.name === name)
  return {
    matches: ['Python', 'Docker'].map((skill) => ({
      requirement: { skill, level: 'required', evidence: 'Python and Docker' },
      status: has(skill) ? 'matched' : 'unlisted',
      profile_skill: has(skill) ? { name: skill, proficiency: null } : null,
      explanation: has(skill) ? `Your profile lists ${skill}.` : `${skill} is not in your profile.`,
    })),
    mentions: [requirement('Python', 16), requirement('Docker', 27)],
  }
}

let analyzeBodies: { profile: { skills: ProfileSkill[] } }[]

beforeEach(() => {
  analyzeBodies = []
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string, init?: RequestInit) => {
      if (url === '/api/skills') return Response.json([{ name: 'Python', category: 'language', aliases: [] }])
      const body = JSON.parse(String(init?.body))
      analyzeBodies.push(body)
      return Response.json(fakeAnalyze(body.profile.skills))
    }),
  )
})

describe('App', () => {
  it('analyzes a posting, highlights mentions, and re-files a skill the student has', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByRole('textbox', { name: 'Internship description' }), POSTING)
    await user.type(screen.getByLabelText('Add a skill'), 'Python{Enter}')
    await user.click(screen.getByRole('button', { name: 'Analyze' }))

    const dockerMark = await screen.findByRole('button', { name: /Docker: Docker, not listed/ })
    expect(screen.getByRole('button', { name: /Python: Python, matched/ })).toBeInTheDocument()

    await user.click(dockerMark)
    const dockerCard = screen.getByRole('button', { name: /^Docker/, expanded: true })
    expect(dockerCard).toBeInTheDocument()
    expect(screen.getByText('Docker is not in your profile.')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'I have this: add Docker' }))

    expect(await screen.findByRole('button', { name: /Docker: Docker, matched/ })).toBeInTheDocument()
    expect(analyzeBodies.at(-1)?.profile.skills.map((s) => s.name)).toEqual(['Python', 'Docker'])
    const matched = screen.getByRole('region', { name: /Matched/ })
    expect(within(matched).getByText('Docker')).toBeInTheDocument()
  })

  it('shows the server message when the analysis is rejected', async () => {
    vi.mocked(fetch).mockImplementation(async (url) =>
      url === '/api/skills'
        ? Response.json([])
        : Response.json({ detail: [{ msg: 'Value error, the description is empty' }] }, { status: 422 }),
    )
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByRole('textbox', { name: 'Internship description' }), 'x')
    await user.click(screen.getByRole('button', { name: 'Analyze' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('the description is empty')
  })

  it('flags results as out of date when skills change', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByRole('textbox', { name: 'Internship description' }), POSTING)
    await user.click(screen.getByRole('button', { name: 'Analyze' }))
    await screen.findByRole('button', { name: /Python: Python, not listed/ })

    await user.type(screen.getByLabelText('Add a skill'), 'Rust{Enter}')

    expect(screen.getByText(/Your skills changed since this analysis/)).toBeInTheDocument()
  })

  it('does not add the same skill twice', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.type(screen.getByLabelText('Add a skill'), 'Python{Enter}')
    await user.type(screen.getByLabelText('Add a skill'), 'python{Enter}')

    expect(screen.getByRole('status')).toHaveTextContent('python is already in your skills.')
    expect(screen.getAllByRole('button', { name: /^Remove/ })).toHaveLength(1)
  })
})

import { useEffect, useMemo, useState } from 'react'
import { analyze, fetchSkills, type AnalysisResult, type MatchStatus, type ProfileSkill } from './api'
import { AlertIcon, RefreshIcon } from './icons'
import { PostingSheet } from './PostingSheet'
import { Results } from './Results'
import { SAMPLE_POSTING } from './sample'
import { SkillsBar } from './SkillsBar'
import { load, save } from './storage'

const PROFICIENCIES = new Set([null, 'none', 'beginner', 'intermediate', 'advanced'])

type Analysis = { result: AnalysisResult; text: string; skills: string }

// Saved data may come from an older version of the app, so check its shape.
function loadSkills(): ProfileSkill[] {
  const saved = load<unknown>('gap.skills', [])
  if (!Array.isArray(saved)) return []
  return saved.filter(
    (s): s is ProfileSkill =>
      typeof s?.name === 'string' && s.name.trim() !== '' && PROFICIENCIES.has(s.proficiency),
  )
}

function loadDescription(): string {
  const saved = load<unknown>('gap.description', '')
  return typeof saved === 'string' ? saved : ''
}

function App() {
  const [description, setDescription] = useState(loadDescription)
  const [skills, setSkills] = useState<ProfileSkill[]>(loadSkills)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [analysis, setAnalysis] = useState<Analysis | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [editing, setEditing] = useState(false)
  const [selected, setSelected] = useState<string | null>(null)
  const [justFiled, setJustFiled] = useState<string | null>(null)

  useEffect(() => save('gap.description', description), [description])
  useEffect(() => save('gap.skills', skills), [skills])

  useEffect(() => {
    fetchSkills()
      .then((catalog) => setSuggestions(catalog.map((s) => s.name)))
      .catch(() => setSuggestions([])) // Suggestions are optional.
  }, [])

  async function runAnalysis(text: string, profile: ProfileSkill[], filed: string | null = null) {
    setLoading(true)
    setError(null)
    try {
      const result = await analyze(text, profile)
      setAnalysis({ result, text, skills: JSON.stringify(profile) })
      setEditing(false)
      setJustFiled(filed)
      setSelected((current) =>
        filed ?? (result.matches.some((m) => m.requirement.skill === current) ? current : null),
      )
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  function addSkillFromResults(name: string) {
    if (skills.some((s) => s.name.toLowerCase() === name.toLowerCase())) return
    const next = [...skills, { name, proficiency: null }]
    setSkills(next)
    void runAnalysis(description, next, name)
  }

  const textChanged = analysis !== null && analysis.text !== description
  const skillsChanged = analysis !== null && analysis.skills !== JSON.stringify(skills)
  const canAnalyze = description.trim().length > 0 && !loading

  const marked = useMemo(() => {
    if (!analysis || textChanged) return null
    const statusBySkill = new Map<string, MatchStatus>(
      analysis.result.matches.map((m) => [m.requirement.skill, m.status]),
    )
    return { mentions: analysis.result.mentions, statusBySkill }
  }, [analysis, textChanged])

  return (
    <div className="app">
      <header className="masthead">
        <div className="masthead-inner">
          <h1>Internship Skill Gap Analyzer</h1>
          <p>See what matches, what’s missing, and where each requirement comes from.</p>
        </div>
      </header>

      <form
        className="workspace"
        onSubmit={(e) => {
          e.preventDefault()
          if (canAnalyze) void runAnalysis(description, skills)
        }}
      >
        <div className="toolbar">
          <SkillsBar skills={skills} onChange={setSkills} suggestions={suggestions} />
          <button type="submit" className="button-primary" disabled={!canAnalyze}>
            {loading ? 'Analyzing…' : analysis ? 'Analyze again' : 'Analyze'}
          </button>
        </div>

        <div className="columns">
          <PostingSheet
            description={description}
            onChange={setDescription}
            onUseExample={() => {
              setDescription(SAMPLE_POSTING)
              setEditing(true)
            }}
            isExample={description === SAMPLE_POSTING}
            marked={marked}
            editing={editing}
            onEditingChange={setEditing}
            selected={selected}
            onSelect={setSelected}
          />

          <section className="results-column" aria-live="polite" aria-busy={loading}>
            {error && (
              <p className="notice notice-error" role="alert">
                <AlertIcon />
                {error}
              </p>
            )}
            {(textChanged || skillsChanged) && (
              <p className="notice notice-stale">
                <RefreshIcon />
                <span>
                  {textChanged ? 'The posting changed' : 'Your skills changed'} since this
                  analysis.
                </span>
                <button type="submit" className="button-link" disabled={!canAnalyze}>
                  Analyze again
                </button>
              </p>
            )}
            {analysis ? (
              <Results
                result={analysis.result}
                selected={selected}
                onSelect={setSelected}
                onAddSkill={addSkillFromResults}
                justFiled={justFiled}
              />
            ) : (
              !error && (
                <div className="results-empty">
                  <h2>How it works</h2>
                  <ol>
                    <li>Paste an internship posting on the left.</li>
                    <li>Add your skills above. Mark any you don’t have yet.</li>
                    <li>
                      Analyze. Every skill the posting mentions is highlighted where it appears,
                      and each one gets a card saying whether it matches your skills.
                    </li>
                  </ol>
                </div>
              )
            )}
          </section>
        </div>
      </form>

      <footer className="colophon">
        Results support career preparation. They are not hiring decisions, and a missing keyword
        doesn’t mean you lack the skill.
      </footer>
    </div>
  )
}

export default App

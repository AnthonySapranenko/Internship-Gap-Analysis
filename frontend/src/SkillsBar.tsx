import { useId, useState } from 'react'
import type { Proficiency, ProfileSkill } from './api'
import { CloseIcon, PlusIcon } from './icons'

const PROFICIENCY_OPTIONS: { value: Proficiency | ''; label: string }[] = [
  { value: '', label: 'Level not set' },
  { value: 'none', label: 'Don’t have it yet' },
  { value: 'beginner', label: 'Beginner' },
  { value: 'intermediate', label: 'Intermediate' },
  { value: 'advanced', label: 'Advanced' },
]

interface Props {
  skills: ProfileSkill[]
  onChange: (skills: ProfileSkill[]) => void
  suggestions: string[]
}

export function SkillsBar({ skills, onChange, suggestions }: Props) {
  const [draft, setDraft] = useState('')
  const [message, setMessage] = useState<string | null>(null)
  const inputId = useId()
  const listId = useId()
  const hintId = useId()

  function addSkill() {
    const name = draft.trim().replace(/\s+/g, ' ')
    if (!name) return
    if (skills.some((s) => s.name.toLowerCase() === name.toLowerCase())) {
      setMessage(`${name} is already in your skills.`)
      return
    }
    onChange([...skills, { name, proficiency: null }])
    setDraft('')
    setMessage(null)
  }

  function setLevel(index: number, proficiency: Proficiency | null) {
    onChange(skills.map((s, i) => (i === index ? { ...s, proficiency } : s)))
  }

  return (
    <section className="skills-bar" aria-labelledby={`${inputId}-heading`}>
      <div className="skills-bar-head">
        <h2 id={`${inputId}-heading`}>Your skills</h2>
        <p id={hintId} className="hint">
          Mark a skill “Don’t have it yet” to record a gap you already know about.
        </p>
      </div>

      <ul className="chips">
        {skills.map((skill, index) => (
          <li key={skill.name} className={`chip${skill.proficiency === 'none' ? ' chip-none' : ''}`}>
            <span className="chip-name">{skill.name}</span>
            <select
              className="chip-level"
              aria-label={`Level for ${skill.name}`}
              value={skill.proficiency ?? ''}
              onChange={(e) => setLevel(index, (e.target.value || null) as Proficiency | null)}
            >
              {PROFICIENCY_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <button
              type="button"
              className="chip-remove"
              aria-label={`Remove ${skill.name}`}
              onClick={() => onChange(skills.filter((_, i) => i !== index))}
            >
              <CloseIcon />
            </button>
          </li>
        ))}
        <li className="chip-add">
          <label htmlFor={inputId} className="visually-hidden">
            Add a skill
          </label>
          <input
            id={inputId}
            list={listId}
            value={draft}
            placeholder={skills.length ? 'Add a skill' : 'Add a skill, e.g. Python'}
            autoComplete="off"
            maxLength={100}
            aria-describedby={hintId}
            onChange={(e) => {
              setDraft(e.target.value)
              setMessage(null)
            }}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault()
                addSkill()
              }
            }}
          />
          <datalist id={listId}>
            {suggestions.map((name) => (
              <option key={name} value={name} />
            ))}
          </datalist>
          <button type="button" className="button-secondary" onClick={addSkill}>
            <PlusIcon />
            Add
          </button>
        </li>
      </ul>
      {message && (
        <p className="field-message" role="status">
          {message}
        </p>
      )}
    </section>
  )
}

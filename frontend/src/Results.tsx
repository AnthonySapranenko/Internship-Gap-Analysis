import { useEffect, useRef } from 'react'
import type { AnalysisResult, MatchStatus, RequirementMatch } from './api'
import { PlusIcon } from './icons'
import { LEVEL_LABEL, STATUS_LABEL } from './labels'
import { LEVEL_ORDER, summarize } from './summary'

const GROUPS: { status: MatchStatus; title: string; description: string }[] = [
  {
    status: 'missing',
    title: 'Gaps to work on',
    description: 'The posting asks for these, and you said you don’t have them yet.',
  },
  {
    status: 'unlisted',
    title: 'Not in your profile',
    description: 'Possible gaps, or skills you have but haven’t added.',
  },
  {
    status: 'matched',
    title: 'Matched',
    description: 'Skills from the posting that are in your profile.',
  },
]

function byLevel(a: RequirementMatch, b: RequirementMatch) {
  return LEVEL_ORDER.indexOf(a.requirement.level) - LEVEL_ORDER.indexOf(b.requirement.level)
}

interface Props {
  result: AnalysisResult
  selected: string | null
  onSelect: (skill: string | null) => void
  onAddSkill: (name: string) => void
  /** A skill just added from a result card; its card is marked as re-filed. */
  justFiled: string | null
}

export function Results({ result, selected, onSelect, onAddSkill, justFiled }: Props) {
  const listRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!selected) return
    const card = listRef.current?.querySelector<HTMLElement>(
      `[data-skill="${CSS.escape(selected)}"]`,
    )
    card?.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
  }, [selected])

  if (result.matches.length === 0) {
    return (
      <div className="results-empty">
        <h2>No recognized skills</h2>
        <p>
          The analyzer didn’t find any skills it knows in this posting. It only recognizes skills
          in its catalog, so a posting written in unusual terms can come back empty. Check that
          the qualifications sections were pasted too.
        </p>
      </div>
    )
  }

  return (
    <div className="results" ref={listRef}>
      <div className="results-head">
        <h2>Results</h2>
        <p className="summary">
          {summarize(result).map(({ level, total, matched }, index, rows) => (
            <span key={level} className="summary-item">
              {index === 0 && 'Matched: '}
              <strong className="num">{matched}</strong> of <span className="num">{total}</span>{' '}
              {LEVEL_LABEL[level].toLowerCase()}
              {index < rows.length - 1 ? ', ' : ''}
            </span>
          ))}
        </p>
        <ul className="legend" aria-label="Highlight colours">
          {GROUPS.map(({ status }) => (
            <li key={status}>
              <span className={`legend-swatch mark-${status}`} aria-hidden="true" />
              {STATUS_LABEL[status]}
            </li>
          ))}
        </ul>
      </div>

      {GROUPS.map(({ status, title, description }) => {
        const matches = result.matches.filter((m) => m.status === status).sort(byLevel)
        if (matches.length === 0) return null
        const headingId = `group-${status}`
        return (
          <section key={status} className={`stack stack-${status}`} aria-labelledby={headingId}>
            <div className="divider">
              <h3 id={headingId} className="divider-tab">
                {title} <span className="num divider-count">{matches.length}</span>
              </h3>
              <p className="divider-note">{description}</p>
            </div>
            <ul className="cards">
              {matches.map((match) => {
                const skill = match.requirement.skill
                const open = selected === skill
                const bodyId = `card-${status}-${skill.replace(/\W+/g, '-')}`
                return (
                  <li
                    key={skill}
                    data-skill={skill}
                    className={`card card-${status}${open ? ' card-open' : ''}${
                      justFiled === skill ? ' card-filed' : ''
                    }`}
                  >
                    <button
                      type="button"
                      className="card-head"
                      aria-expanded={open}
                      aria-controls={bodyId}
                      onClick={() => onSelect(open ? null : skill)}
                    >
                      <span className="card-skill">{skill}</span>
                      <span className="card-meta">
                        <span
                          className={`level-mark level-${match.requirement.level}`}
                          aria-hidden="true"
                        />
                        {LEVEL_LABEL[match.requirement.level]}
                        <span className="card-status">{STATUS_LABEL[status]}</span>
                      </span>
                    </button>
                    {open && (
                      <div id={bodyId} className="card-body">
                        <blockquote className="card-evidence">
                          <span className="visually-hidden">From the posting: </span>
                          {match.requirement.evidence}
                        </blockquote>
                        <p className="card-explanation">{match.explanation}</p>
                        {status === 'unlisted' && (
                          <button
                            type="button"
                            className="button-secondary"
                            onClick={() => onAddSkill(skill)}
                          >
                            <PlusIcon />I have this: add {skill}
                          </button>
                        )}
                      </div>
                    )}
                  </li>
                )
              })}
            </ul>
          </section>
        )
      })}
    </div>
  )
}

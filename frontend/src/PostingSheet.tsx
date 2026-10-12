import { useEffect, useId, useMemo, useRef } from 'react'
import type { MatchStatus, Mention } from './api'
import { STATUS_LABEL } from './labels'
import { segment } from './marks'

const MAX_DESCRIPTION_LENGTH = 50_000

interface Props {
  description: string
  onChange: (description: string) => void
  onUseExample: () => void
  /** Present when the posting has been analyzed and not edited since. */
  marked: { mentions: Mention[]; statusBySkill: Map<string, MatchStatus> } | null
  editing: boolean
  onEditingChange: (editing: boolean) => void
  selected: string | null
  onSelect: (skill: string) => void
}

export function PostingSheet({
  description,
  onChange,
  onUseExample,
  marked,
  editing,
  onEditingChange,
  selected,
  onSelect,
}: Props) {
  const textareaId = useId()
  const sheetRef = useRef<HTMLDivElement>(null)
  const showMarks = marked !== null && !editing

  const segments = useMemo(
    () => (marked ? segment(description, marked.mentions) : []),
    [description, marked],
  )

  // Bring the first mark of the selected skill into view inside the sheet.
  useEffect(() => {
    if (!showMarks || !selected) return
    const mark = sheetRef.current?.querySelector<HTMLElement>(
      `[data-skill="${CSS.escape(selected)}"]`,
    )
    mark?.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
  }, [selected, showMarks])

  return (
    <section className="posting" aria-labelledby={`${textareaId}-label`}>
      <div className="posting-head">
        <h2 id={`${textareaId}-label`}>
          {showMarks ? (
            'Internship description'
          ) : (
            <label htmlFor={textareaId}>Internship description</label>
          )}
        </h2>
        <div className="posting-actions">
          {showMarks ? (
            <button type="button" className="button-link" onClick={() => onEditingChange(true)}>
              Edit posting
            </button>
          ) : (
            <>
              {marked && (
                <button
                  type="button"
                  className="button-link"
                  onClick={() => onEditingChange(false)}
                >
                  Show highlights
                </button>
              )}
              <button type="button" className="button-link" onClick={onUseExample}>
                Use an example
              </button>
            </>
          )}
        </div>
      </div>

      {showMarks ? (
        <div ref={sheetRef} className="sheet sheet-marked" tabIndex={-1}>
          {segments.map((part, index) => {
            if (!part.mention) return <span key={index}>{part.text}</span>
            const skill = part.mention.skill
            const status = marked.statusBySkill.get(skill) ?? 'unlisted'
            return (
              <button
                key={index}
                type="button"
                className={`mark mark-${status}`}
                data-skill={skill}
                aria-pressed={selected === skill}
                aria-label={`${part.text}: ${skill}, ${STATUS_LABEL[status].toLowerCase()}`}
                onClick={() => onSelect(skill)}
              >
                {part.text}
              </button>
            )
          })}
        </div>
      ) : (
        <textarea
          id={textareaId}
          className="sheet sheet-input"
          value={description}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Paste the full posting here, including the qualifications sections."
          maxLength={MAX_DESCRIPTION_LENGTH}
          spellCheck={false}
        />
      )}
    </section>
  )
}

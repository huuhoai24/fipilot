import React from 'react'
import {
  Check,
  Circle,
  CircleDot,
  MessageSquareText,
  Mic,
} from 'lucide-react'
import { AI_INTERVIEWER_LABEL, type InterviewerPersona } from '@/lib/interviewerPersonas'
import type { ExperienceLevel, InterviewLanguage, InterviewMode } from '@/types'

interface InterviewPreparationScreenProps {
  candidateName: string
  mode: InterviewMode
  language: InterviewLanguage
  experienceLevel: ExperienceLevel
  questionCount: number
  persona: InterviewerPersona
  preparationReady: boolean
}

type PreparationStageState = 'complete' | 'active' | 'pending'

function PreparationStage({ label, state }: { label: string; state: PreparationStageState }) {
  return (
    <li className="flex items-center gap-3">
      {state === 'complete' ? (
        <Check className="h-4 w-4 shrink-0 text-success" aria-hidden="true" />
      ) : state === 'active' ? (
        <CircleDot className="h-4 w-4 shrink-0 animate-pulse text-accent" aria-hidden="true" />
      ) : (
        <Circle className="h-4 w-4 shrink-0 text-text-faint" aria-hidden="true" />
      )}
      <span className={state === 'active' ? 'text-sm font-semibold text-text-primary' : 'text-sm text-text-muted'}>
        {label}
      </span>
    </li>
  )
}

export function InterviewPreparationScreen({
  candidateName,
  mode,
  language,
  experienceLevel,
  questionCount,
  persona,
  preparationReady,
}: InterviewPreparationScreenProps) {
  const modeLabel = mode === 'voice' ? 'Speech' : 'Text'
  const languageLabel = language === 'vi' ? 'Vietnamese' : 'English'
  const ModeIcon = mode === 'voice' ? Mic : MessageSquareText
  const currentActivity = preparationReady
    ? 'Preparing the first question'
    : 'Preparing interview topics'

  const stages: Array<{ label: string; state: PreparationStageState }> = [
    { label: 'Preparing interview topics', state: preparationReady ? 'complete' : 'active' },
    { label: 'Personalizing your interview', state: preparationReady ? 'complete' : 'pending' },
    { label: 'Preparing the first question', state: preparationReady ? 'active' : 'pending' },
    { label: 'Interview ready', state: 'pending' },
  ]

  return (
    <section
      className="mx-auto flex min-h-[calc(100dvh-8rem)] w-full max-w-4xl items-center py-8"
      aria-labelledby="interview-preparation-title"
    >
      <div className="w-full">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-accent-soft text-accent">
            <ModeIcon className="h-6 w-6" aria-hidden="true" />
          </div>
          <div className="min-w-0">
            <p className="text-sm font-medium text-accent">Interview preparation</p>
            <h1 id="interview-preparation-title" className="mt-1 font-display text-2xl font-bold text-text-primary">
              Preparing your interview
            </h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-text-muted">
              FiPilot is preparing a personalized interview from your saved profile and settings.
            </p>
          </div>
        </div>

        <dl className="mt-8 grid gap-5 border-y border-border py-5 lg:grid-cols-4">
          <div>
            <dt className="text-xs font-medium text-text-faint">Candidate</dt>
            <dd className="mt-1 break-words text-sm font-semibold text-text-primary">{candidateName}</dd>
          </div>
          <div>
            <dt className="text-xs font-medium text-text-faint">Interview</dt>
            <dd className="mt-1 text-sm font-semibold capitalize text-text-primary">
              {experienceLevel} {modeLabel}
            </dd>
          </div>
          <div>
            <dt className="text-xs font-medium text-text-faint">Language</dt>
            <dd className="mt-1 text-sm font-semibold text-text-primary">{languageLabel}</dd>
          </div>
          <div>
            <dt className="text-xs font-medium text-text-faint">Questions</dt>
            <dd className="mt-1 text-sm font-semibold tabular-nums text-text-primary">{questionCount}</dd>
          </div>
        </dl>

        <div className="mt-8 grid gap-8 lg:grid-cols-[minmax(0,1fr)_18rem]">
          <div>
            <p className="text-sm font-semibold text-text-primary" role="status" aria-live="polite" aria-atomic="true">
              {currentActivity}
            </p>
            <ol className="mt-5 space-y-4">
              {stages.map((stage) => <PreparationStage key={stage.label} {...stage} />)}
            </ol>
            <p className="mt-5 text-sm leading-6 text-text-muted">
              You will enter the Interview Room automatically when the first question is ready.
            </p>
          </div>

          <aside className="border-t border-border pt-5 lg:border-l lg:border-t-0 lg:pl-6 lg:pt-0" aria-label="Your AI interviewer">
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-accent bg-accent-soft text-sm font-semibold text-accent" aria-hidden="true">
                {persona.avatar.initials}
              </span>
              <div className="min-w-0">
                <p className="break-words text-sm font-semibold text-text-primary">{persona.name}</p>
                <p className="mt-0.5 text-xs text-text-muted">{persona.role}</p>
              </div>
            </div>
            <p className="mt-3 text-xs font-medium text-accent">{AI_INTERVIEWER_LABEL}</p>
          </aside>
        </div>
      </div>
    </section>
  )
}

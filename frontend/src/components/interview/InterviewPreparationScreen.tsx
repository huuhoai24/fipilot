import React, { useEffect, useState } from 'react'
import {
  Check,
  CircleDot,
  ClipboardList,
  MessageSquareText,
  Mic,
} from 'lucide-react'
import type { ExperienceLevel, InterviewMode } from '@/types'

interface InterviewPreparationScreenProps {
  candidateName: string
  mode: InterviewMode
  experienceLevel: ExperienceLevel
  questionCount: number
  preparationReady: boolean
}

export function InterviewPreparationScreen({
  candidateName,
  mode,
  experienceLevel,
  questionCount,
  preparationReady,
}: InterviewPreparationScreenProps) {
  const [elapsedSeconds, setElapsedSeconds] = useState(0)
  const modeLabel = mode === 'voice' ? 'speech' : 'text'
  const ModeIcon = mode === 'voice' ? Mic : MessageSquareText
  const activity = preparationReady
    ? 'Opening the interview room'
    : 'Building the interview plan and first question'

  useEffect(() => {
    const timer = window.setInterval(() => {
      setElapsedSeconds((current) => current + 1)
    }, 1000)
    return () => window.clearInterval(timer)
  }, [])

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
            <p className="text-sm font-medium text-accent">
              Interview preparation
            </p>
            <h1
              id="interview-preparation-title"
              className="mt-1 text-2xl font-bold text-text-primary"
            >
              Preparing your {modeLabel} interview
            </h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-text-muted">
              The first question is being prepared from the saved candidate
              profile and interview settings.
            </p>
          </div>
        </div>

        <div className="mt-8 border-y border-border py-5">
          <dl className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <dt className="text-xs font-medium text-text-faint">Candidate</dt>
              <dd className="mt-1 truncate text-sm font-semibold text-text-primary">
                {candidateName}
              </dd>
            </div>
            <div>
              <dt className="text-xs font-medium text-text-faint">Mode</dt>
              <dd className="mt-1 text-sm font-semibold capitalize text-text-primary">
                {modeLabel}
              </dd>
            </div>
            <div>
              <dt className="text-xs font-medium text-text-faint">Level</dt>
              <dd className="mt-1 text-sm font-semibold capitalize text-text-primary">
                {experienceLevel}
              </dd>
            </div>
            <div>
              <dt className="text-xs font-medium text-text-faint">Questions</dt>
              <dd className="mt-1 text-sm font-semibold tabular-nums text-text-primary">
                {questionCount}
              </dd>
            </div>
          </dl>
        </div>

        <div className="mt-8 grid gap-8 lg:grid-cols-[minmax(0,1fr)_16rem]">
          <div>
            <div
              className="flex items-center justify-between gap-4 text-sm"
              role="status"
              aria-live="polite"
              aria-atomic="true"
            >
              <span className="font-semibold text-text-primary">{activity}</span>
              <span className="shrink-0 tabular-nums text-text-faint">
                Preparing - {elapsedSeconds}s
              </span>
            </div>
            <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-surface-raised">
              <div className="h-full w-2/3 animate-pulse rounded-full bg-accent" />
            </div>
            <p className="mt-3 text-sm leading-6 text-text-muted">
              You will enter the room automatically as soon as the session is
              ready.
            </p>
          </div>

          <ol className="space-y-4 border-l border-border pl-5">
            <li className="flex gap-3">
              <Check
                className="mt-0.5 h-4 w-4 shrink-0 text-success"
                aria-hidden="true"
              />
              <div>
                <div className="text-sm font-medium text-text-primary">
                  Candidate evidence ready
                </div>
                <div className="mt-0.5 text-xs text-text-faint">
                  CV profile loaded
                </div>
              </div>
            </li>
            <li className="flex gap-3">
              <CircleDot
                className="mt-0.5 h-4 w-4 shrink-0 animate-pulse text-accent"
                aria-hidden="true"
              />
              <div>
                <div className="text-sm font-medium text-text-primary">
                  Interview structure
                </div>
                <div className="mt-0.5 text-xs text-text-faint">
                  Topics and difficulty
                </div>
              </div>
            </li>
            <li className="flex gap-3">
              <ClipboardList
                className="mt-0.5 h-4 w-4 shrink-0 text-text-faint"
                aria-hidden="true"
              />
              <div>
                <div className="text-sm font-medium text-text-primary">
                  Opening question
                </div>
                <div className="mt-0.5 text-xs text-text-faint">
                  Evidence-based prompt
                </div>
              </div>
            </li>
          </ol>
        </div>
      </div>
    </section>
  )
}

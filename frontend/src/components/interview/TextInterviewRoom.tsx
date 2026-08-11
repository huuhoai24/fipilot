import React, { type FormEvent, type KeyboardEvent, useEffect, useRef, useState } from 'react'
import { CheckCircle2, FileText, History, Loader2, Send } from 'lucide-react'
import { BrandLogo } from '@/components/brand/BrandLogo'
import { Button } from '@/components/ui/Button'
import { AI_INTERVIEWER_LABEL, type InterviewerPersona } from '@/lib/interviewerPersonas'
import { cn, formatElapsed } from '@/lib/utils'
import type { V2InterviewSessionState, V2InterviewTurn } from '@/types'

interface InterviewProgress {
  current: number
  total: number
}

interface TextInterviewRoomProps {
  state: V2InterviewSessionState
  persona: InterviewerPersona
  progress: InterviewProgress
  answer: string
  pendingAnswer: string | null
  submitting: boolean
  startedAt?: string | null
  error: string | null
  onAnswerChange: (answer: string) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
  onViewReport: () => void
  onBackToHistory: () => void
}

interface TextInterviewRoomStatusProps {
  error?: string | null
  onBackToHistory: () => void
}

function questionText(turn: V2InterviewTurn): string {
  return typeof turn.question === 'string'
    ? turn.question
    : turn.question.question
}

function answerText(turn: V2InterviewTurn): string {
  return turn.answer?.trim() || turn.candidate_answer?.trim() || ''
}

function candidateInitial(name: string): string {
  return name.trim().charAt(0).toLocaleUpperCase() || 'C'
}

function interviewLabel(state: V2InterviewSessionState): string {
  const level = state.interview_config.experience_level
  const style = state.interview_config.interview_style
  return `${level.charAt(0).toUpperCase()}${level.slice(1)} ${style} interview`
}

function transitionText(state: V2InterviewSessionState): string | null {
  const current = state.current_turn
  if (!current || current.question_type === 'opening') return null

  const previous = state.completed_turns[state.completed_turns.length - 1]
  const vietnamese = state.interview_config.language === 'vi'
  if (current.question_type === 'follow_up' && previous?.question_type !== 'follow_up') {
    return vietnamese
      ? 'Tôi muốn tìm hiểu thêm một chút về phần này.'
      : "I'd like to explore that a little further."
  }
  if (
    previous
    && previous.topic.trim()
    && current.topic.trim()
    && previous.topic !== current.topic
  ) {
    return vietnamese
      ? 'Cảm ơn bạn. Chúng ta hãy chuyển sang một chủ đề khác.'
      : "Thanks. Let's move to another topic."
  }
  return null
}

function closingText(state: V2InterviewSessionState): string {
  const name = state.candidate_profile.name.trim()
  if (state.interview_config.language === 'vi') {
    const thanks = name ? `Cảm ơn ${name}.` : 'Cảm ơn bạn.'
    return `${thanks}\n\nĐó là tất cả các câu hỏi của buổi phỏng vấn hôm nay. Cảm ơn bạn đã dành thời gian.\n\nBuổi phỏng vấn của bạn hiện đã hoàn tất.`
  }
  const thanks = name ? `Thanks, ${name}.` : 'Thank you.'
  return `${thanks}\n\nThat's all the questions I have for today. Thank you for your time.\n\nYour interview is now complete.`
}

function RoomHeader({
  label,
  status = 'In progress',
  startedAt,
}: {
  label: string
  status?: 'Opening' | 'In progress' | 'Complete' | 'Unavailable'
  startedAt?: string | null
}) {
  return (
    <header className="sticky top-0 z-20 border-b border-border bg-surface">
      <div className="mx-auto flex h-16 w-full max-w-[1280px] items-center justify-between gap-4 px-4 sm:px-6 lg:px-10">
        <div className="flex items-center gap-3">
          <BrandLogo className="h-8 w-8" />
          <span className="font-display text-base font-semibold text-text-primary">
            Fi<span className="text-accent">pilot</span>
          </span>
        </div>
        <div className="flex min-w-0 items-center gap-4 text-sm">
          <span className="hidden truncate font-medium text-text-primary sm:block">
            {label}
          </span>
          <span
            className="flex shrink-0 items-center gap-2 text-text-muted"
            role="status"
          >
            <span className="h-2 w-2 rounded-full bg-accent" aria-hidden="true" />
            {status}
          </span>
          {startedAt && status !== 'Complete' && (
            <ElapsedInterviewTimer startedAt={startedAt} />
          )}
        </div>
      </div>
    </header>
  )
}

function ElapsedInterviewTimer({ startedAt }: { startedAt: string }) {
  const [, setTick] = useState(0)
  const validStart = Number.isFinite(Date.parse(startedAt))

  useEffect(() => {
    if (!validStart) return
    const timer = window.setInterval(() => setTick((tick) => tick + 1), 1_000)
    return () => window.clearInterval(timer)
  }, [startedAt, validStart])

  if (!validStart) return null
  return (
    <time
      aria-label="Elapsed interview time"
      className="shrink-0 border-l border-border pl-4 font-medium tabular-nums text-text-primary"
    >
      {formatElapsed(startedAt)}
    </time>
  )
}

function InterviewerAvatar({
  persona,
  size = 'message',
}: {
  persona: InterviewerPersona
  size?: 'message' | 'profile'
}) {
  const sizeClasses = size === 'profile'
    ? 'h-14 w-14 text-base'
    : 'h-10 w-10 text-sm'

  return (
    <div
      className={cn(
        'flex shrink-0 items-center justify-center overflow-hidden rounded-full border border-accent bg-accent-soft font-semibold text-accent',
        sizeClasses,
      )}
      aria-hidden="true"
    >
      {persona.avatar.src ? (
        <img src={persona.avatar.src} alt="" className="h-full w-full object-cover" />
      ) : (
        persona.avatar.initials
      )}
    </div>
  )
}

function CandidateAvatar({ name }: { name: string }) {
  return (
    <div
      className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-border bg-surface-raised text-sm font-semibold text-text-primary"
      aria-hidden="true"
    >
      {candidateInitial(name)}
    </div>
  )
}

const InterviewerMessage = React.forwardRef<HTMLLIElement, {
  persona: InterviewerPersona
  children: React.ReactNode
}>(
  ({ persona, children }, ref) => (
    <li ref={ref} className="grid max-w-4xl scroll-mb-80 grid-cols-[2.5rem_minmax(0,1fr)] items-start gap-3 sm:gap-4 md:scroll-mb-72">
      <InterviewerAvatar persona={persona} />
      <article className="min-w-0 rounded-lg border border-border bg-surface px-4 py-3 sm:px-5 sm:py-4">
        <p className="mb-1 text-sm font-semibold text-accent">{persona.name}</p>
        <div className="whitespace-pre-wrap break-words text-base leading-7 text-text-primary">
          {children}
        </div>
      </article>
    </li>
  ),
)
InterviewerMessage.displayName = 'InterviewerMessage'

function CandidateMessage({
  name,
  children,
}: {
  name: string
  children: React.ReactNode
}) {
  return (
    <li className="ml-auto grid max-w-4xl grid-cols-[minmax(0,1fr)_2.5rem] items-start gap-3 sm:gap-4">
      <article className="min-w-0 rounded-lg border border-accent bg-accent-soft px-4 py-3 sm:px-5 sm:py-4">
        <p className="mb-1 text-right text-sm font-semibold text-text-primary">{name}</p>
        <div className="whitespace-pre-wrap break-words text-base leading-7 text-text-primary">
          {children}
        </div>
      </article>
      <CandidateAvatar name={name} />
    </li>
  )
}

export function TextInterviewRoomStatus({
  error,
  onBackToHistory,
}: TextInterviewRoomStatusProps) {
  return (
    <div className="flex min-h-[100dvh] flex-col bg-bg">
      <a
        href="#main-content"
        className="fixed left-4 top-4 z-50 -translate-y-20 rounded-lg bg-accent px-4 py-2 text-sm font-medium text-accent-contrast transition-transform focus:translate-y-0"
      >
        Skip to main content
      </a>
      <RoomHeader label="Text interview" status={error ? 'Unavailable' : 'Opening'} />
      <main id="main-content" className="mx-auto flex w-full max-w-3xl flex-1 items-center px-4 py-10 sm:px-6">
        <section className="w-full border-y border-border py-8" aria-live="polite">
          {error ? (
            <>
              <h1 className="font-display text-2xl font-semibold text-text-primary">
                Interview unavailable
              </h1>
              <p role="alert" className="mt-3 max-w-2xl text-sm leading-6 text-danger">
                {error}
              </p>
              <Button className="mt-6" type="button" variant="secondary" onClick={onBackToHistory}>
                <History className="h-4 w-4" aria-hidden="true" />
                Back to history
              </Button>
            </>
          ) : (
            <div className="flex items-center gap-4" role="status">
              <Loader2 className="h-5 w-5 animate-spin text-accent" aria-hidden="true" />
              <div>
                <h1 className="font-display text-xl font-semibold text-text-primary">
                  Opening interview room
                </h1>
                <p className="mt-1 text-sm text-text-muted">Loading your conversation.</p>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export function TextInterviewRoom({
  state,
  persona,
  progress,
  answer,
  pendingAnswer,
  submitting,
  startedAt,
  error,
  onAnswerChange,
  onSubmit,
  onViewReport,
  onBackToHistory,
}: TextInterviewRoomProps) {
  const candidateName = state.candidate_profile.name || 'Candidate'
  const isFinished = !state.current_turn
  const phase = state.phase ?? (isFinished ? 'closing' : 'interviewing')
  const transition = transitionText(state)
  const currentQuestionRef = useRef<HTMLLIElement>(null)
  const composerRef = useRef<HTMLTextAreaElement>(null)
  const restoreComposerFocusRef = useRef(false)
  const shouldFollowConversationRef = useRef(true)
  const previousQuestionIdRef = useRef<string | null>(null)

  useEffect(() => {
    const questionId = state.current_turn?.turn_id ?? null
    const isInitialQuestion = previousQuestionIdRef.current === null
    previousQuestionIdRef.current = questionId
    if (!questionId || (!isInitialQuestion && !shouldFollowConversationRef.current)) return

    const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false
    currentQuestionRef.current?.scrollIntoView?.({
      behavior: isInitialQuestion || reduceMotion ? 'auto' : 'smooth',
      block: 'nearest',
    })
  }, [state.current_turn?.turn_id])

  useEffect(() => {
    const updateFollowPreference = () => {
      const distanceFromBottom = document.documentElement.scrollHeight
        - window.scrollY
        - window.innerHeight
      shouldFollowConversationRef.current = distanceFromBottom < 240
    }
    updateFollowPreference()
    window.addEventListener('scroll', updateFollowPreference, { passive: true })
    window.addEventListener('resize', updateFollowPreference)
    return () => {
      window.removeEventListener('scroll', updateFollowPreference)
      window.removeEventListener('resize', updateFollowPreference)
    }
  }, [])

  useEffect(() => {
    if (submitting || !restoreComposerFocusRef.current || !state.current_turn) return
    composerRef.current?.focus({ preventScroll: true })
    restoreComposerFocusRef.current = false
  }, [state.current_turn, submitting])

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    restoreComposerFocusRef.current = event.currentTarget.contains(document.activeElement)
    onSubmit(event)
  }

  const handleComposerKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key !== 'Enter' || (!event.ctrlKey && !event.metaKey)) return
    event.preventDefault()
    if (!submitting && answer.trim()) event.currentTarget.form?.requestSubmit()
  }

  return (
    <div className="flex min-h-[100dvh] flex-col bg-bg">
      <a
        href="#main-content"
        className="fixed left-4 top-4 z-50 -translate-y-20 rounded-lg bg-accent px-4 py-2 text-sm font-medium text-accent-contrast transition-transform focus:translate-y-0"
      >
        Skip to main content
      </a>
      <RoomHeader
        label={interviewLabel(state)}
        status={phase === 'opening' ? 'Opening' : isFinished ? 'Complete' : 'In progress'}
        startedAt={startedAt}
      />

      <main id="main-content" className="flex-1">
        <div className="mx-auto w-full max-w-5xl px-4 pb-8 pt-6 sm:px-6 lg:px-10">
          <section className="flex items-center gap-4 border-b border-border pb-6" aria-labelledby="interviewer-title">
            <InterviewerAvatar persona={persona} size="profile" />
            <div className="min-w-0">
              <p className="mb-1 text-xs font-medium text-text-muted">{AI_INTERVIEWER_LABEL}</p>
              <h1 id="interviewer-title" className="font-display text-2xl font-semibold tracking-tight text-text-primary sm:text-3xl">
                {persona.name}
              </h1>
              {persona.role !== AI_INTERVIEWER_LABEL && (
                <p className="mt-1 text-sm font-medium text-accent">{persona.role}</p>
              )}
              {persona.specialization && (
                <p className="mt-1 text-sm leading-6 text-text-primary">{persona.specialization}</p>
              )}
              <p className="mt-1 max-w-2xl text-sm leading-6 text-text-muted">
                {persona.shortDescription}
              </p>
            </div>
          </section>

          <section className="pt-6" aria-labelledby="conversation-title">
            <div className="mb-4 flex items-center justify-between gap-4">
              <h2 id="conversation-title" className="text-base font-semibold text-text-primary">
                Conversation
              </h2>
              <p className="shrink-0 text-sm tabular-nums text-text-muted">
                {phase === 'opening'
                  ? 'Opening'
                  : isFinished
                    ? 'Complete'
                    : `Question ${progress.current} of ${progress.total}`}
              </p>
            </div>

            <ol className="space-y-4" aria-live="polite">
              {state.opening_turn && (
                <>
                  <InterviewerMessage persona={persona}>
                    {questionText(state.opening_turn)}
                  </InterviewerMessage>
                  {answerText(state.opening_turn) && (
                    <CandidateMessage name={candidateName}>
                      {answerText(state.opening_turn)}
                    </CandidateMessage>
                  )}
                </>
              )}
              {state.completed_turns.flatMap((turn) => {
                const response = answerText(turn)
                return [
                  <InterviewerMessage key={`${turn.turn_id}-question`} persona={persona}>
                    {questionText(turn)}
                  </InterviewerMessage>,
                  response ? (
                    <CandidateMessage key={`${turn.turn_id}-answer`} name={candidateName}>
                      {response}
                    </CandidateMessage>
                  ) : null,
                ].filter((message): message is React.ReactElement => message !== null)
              })}
              {state.current_turn && (
                <InterviewerMessage ref={currentQuestionRef} persona={persona}>
                  {transition && (
                    <p className="mb-2 text-text-muted">{transition}</p>
                  )}
                  <p>{questionText(state.current_turn)}</p>
                </InterviewerMessage>
              )}
              {pendingAnswer && (
                <CandidateMessage name={candidateName}>
                  {pendingAnswer}
                </CandidateMessage>
              )}
              {submitting && pendingAnswer && (
                <InterviewerMessage persona={persona}>
                  <span className="flex items-center gap-2 text-sm text-text-muted" role="status">
                    <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                    {persona.name} is preparing the next question...
                  </span>
                </InterviewerMessage>
              )}
              {isFinished && (
                <InterviewerMessage persona={persona}>{closingText(state)}</InterviewerMessage>
              )}
            </ol>

            {isFinished && (
              <section className="mt-8 border-y border-border py-8" aria-labelledby="interview-complete-title">
                <div className="flex items-start gap-4">
                  <CheckCircle2 className="mt-1 h-6 w-6 shrink-0 text-accent" aria-hidden="true" />
                  <div>
                    <h2 id="interview-complete-title" className="text-xl font-semibold text-text-primary">
                      Interview complete
                    </h2>
                    <p className="mt-2 text-sm leading-6 text-text-muted">
                      Your answers are saved. Your report may take a moment to finish generating.
                    </p>
                    <div className="mt-6 flex flex-col gap-3 sm:flex-row">
                      <Button type="button" size="lg" onClick={onViewReport}>
                        <FileText className="h-4 w-4" aria-hidden="true" />
                        View report
                      </Button>
                      <Button type="button" size="lg" variant="secondary" onClick={onBackToHistory}>
                        <History className="h-4 w-4" aria-hidden="true" />
                        Back to history
                      </Button>
                    </div>
                  </div>
                </div>
              </section>
            )}
          </section>
        </div>
      </main>

      {!isFinished && (
        <footer className="sticky bottom-0 z-10 border-t border-border bg-surface">
          <div className="mx-auto w-full max-w-5xl px-4 py-4 sm:px-6 lg:px-10">
            {error && (
              <p role="alert" className="mb-3 rounded-lg border border-danger/30 bg-danger/10 px-4 py-3 text-sm text-danger">
                {error}
              </p>
            )}
            <form onSubmit={handleSubmit} aria-busy={submitting}>
              <label htmlFor="interview-answer" className="mb-2 block text-sm font-semibold text-text-primary">
                Your answer
              </label>
              <textarea
                ref={composerRef}
                id="interview-answer"
                rows={5}
                value={answer}
                onChange={(event) => onAnswerChange(event.target.value)}
                onKeyDown={handleComposerKeyDown}
                disabled={submitting}
                placeholder={submitting ? `Waiting for ${persona.name}...` : 'Type your answer here...'}
                aria-describedby="answer-composer-help"
                aria-invalid={Boolean(error)}
                maxLength={12000}
                className="min-h-32 w-full resize-y rounded-lg border border-border bg-surface-raised px-4 py-3 text-base leading-6 text-text-primary outline-none placeholder:text-text-faint focus:border-accent disabled:cursor-wait"
              />
              <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <p id="answer-composer-help" className="text-xs text-text-muted">
                  {submitting
                    ? 'Your answer is saved above while the next question is prepared.'
                    : 'Use Ctrl + Enter or Command + Enter to submit. Enter adds a new line.'}
                </p>
                <Button type="submit" size="lg" disabled={submitting || !answer.trim()} className="w-full disabled:opacity-60 sm:w-auto">
                  {submitting ? (
                    <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                  ) : (
                    <Send className="h-4 w-4" aria-hidden="true" />
                  )}
                  {submitting ? 'Submitting' : error ? 'Retry answer' : 'Submit answer'}
                </Button>
              </div>
            </form>
          </div>
        </footer>
      )}
    </div>
  )
}

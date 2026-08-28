import React, {
  type FormEvent,
  type KeyboardEvent,
  useLayoutEffect,
  useRef,
} from 'react'
import {
  CheckCircle2,
  FileText,
  History,
  Loader2,
  MessageSquare,
  Send,
} from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { type InterviewerPersona } from '@/lib/interviewerPersonas'
import type { V2InterviewSessionState, V2InterviewTurn } from '@/types'

interface InterviewProgress {
  current: number
  total: number
}

interface TextInterviewRoomProps {
  state: V2InterviewSessionState
  sessionId?: string
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

export interface TextInterviewRoomStatusProps {
  error?: string | null
  onBackToHistory: () => void
}

const COMPOSER_MIN_HEIGHT_PX = 140
const COMPOSER_MAX_HEIGHT_PX = 320

function questionText(turn: V2InterviewTurn): string {
  return typeof turn.question === 'string'
    ? turn.question
    : turn.question.question
}

function answerText(turn: V2InterviewTurn): string {
  return turn.answer?.trim() || turn.candidate_answer?.trim() || ''
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

export function TextInterviewRoomStatus({
  error,
  onBackToHistory,
}: TextInterviewRoomStatusProps) {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
      <div className="max-w-md space-y-4">
        <p role="alert" className="rounded-lg border border-danger/30 bg-danger/10 p-4 text-sm text-danger">
          {error || 'Interview session is unavailable.'}
        </p>
        <Button type="button" onClick={onBackToHistory}>
          <History className="h-4 w-4" aria-hidden="true" />
          Back to history
        </Button>
      </div>
    </div>
  )
}

export function TextInterviewRoom({
  state,
  persona: _persona,
  progress: _progress,
  answer,
  pendingAnswer,
  submitting,
  startedAt: _startedAt,
  error,
  onAnswerChange,
  onSubmit,
  onViewReport,
  onBackToHistory,
}: TextInterviewRoomProps) {
  const composerRef = useRef<HTMLTextAreaElement>(null)
  const restoreComposerFocusRef = useRef(false)
  const candidateName = state.candidate_profile.name || 'Candidate'
  const candidateRole = state.candidate_profile.recent_role || state.candidate_profile.specialization || 'AI Engineer'
  const candidateSkills = state.candidate_profile.skills || []
  const isFinished = !state.current_turn
  const activeTurn = state.current_turn || state.opening_turn

  useLayoutEffect(() => {
    const composer = composerRef.current
    if (!composer) return
    composer.style.height = 'auto'
    const contentHeight = Math.max(COMPOSER_MIN_HEIGHT_PX, composer.scrollHeight)
    composer.style.height = `${Math.min(contentHeight, COMPOSER_MAX_HEIGHT_PX)}px`
    composer.style.overflowY = contentHeight > COMPOSER_MAX_HEIGHT_PX ? 'auto' : 'hidden'
  }, [answer])

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    restoreComposerFocusRef.current = event.currentTarget.contains(document.activeElement)
    onSubmit(event)
  }

  const handleComposerKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key !== 'Enter' || (!event.ctrlKey && !event.metaKey)) return
    event.preventDefault()
    if (!submitting && answer.trim()) event.currentTarget.form?.requestSubmit()
  }

  const topicTitle = activeTurn?.topic?.trim() || 'Technical Interview Question'

  return (
    <div className="mx-auto max-w-6xl space-y-6 pb-12">
      {/* 2-Column Layout */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Left Column (2 spans): Topic, Current Question, Answer, Submit */}
        <div className="space-y-6 lg:col-span-2">
          {activeTurn && !isFinished && (
            <div className="space-y-3">
              {/* Topic Heading */}
              <h2 className="text-base font-bold text-text-primary sm:text-lg">
                {topicTitle}
              </h2>

              {/* Current Question Card */}
              <div className="rounded-2xl border border-[#d1fae5] bg-[#f0fdf4] p-6 shadow-xs dark:border-[#134e3a] dark:bg-[#062419]">
                <div className="flex items-center gap-2 text-emerald-700 dark:text-emerald-400 font-bold text-xs tracking-wider uppercase mb-3">
                  <MessageSquare className="h-4 w-4 shrink-0" aria-hidden="true" />
                  <span>CURRENT QUESTION</span>
                </div>

                <p className="text-base font-medium leading-relaxed text-text-primary sm:text-lg">
                  {questionText(activeTurn)}
                </p>
              </div>
            </div>
          )}

          {/* Pending Answer / Submitting indicator */}
          {pendingAnswer && (
            <div className="rounded-2xl border border-border bg-surface-raised p-4 text-sm text-text-primary italic">
              <span className="font-semibold not-italic text-accent block mb-1">Your submitted answer:</span>
              "{pendingAnswer}"
            </div>
          )}

          {submitting && pendingAnswer && (
            <div className="flex items-center gap-2 text-sm text-text-muted py-2" role="status">
              <Loader2 className="h-4 w-4 animate-spin text-accent" aria-hidden="true" />
              <span>Preparing the next question...</span>
            </div>
          )}

          {/* Finished State */}
          {isFinished && (
            <div className="rounded-2xl border border-accent/20 bg-accent/5 p-8 text-center">
              <CheckCircle2 className="mx-auto h-12 w-12 text-accent" aria-hidden="true" />
              <h3 className="mt-3 text-2xl font-bold text-text-primary">
                Interview complete
              </h3>
              <p className="mx-auto mt-2 max-w-lg text-sm text-text-muted whitespace-pre-line">
                {closingText(state)}
              </p>
              <div className="mt-6 flex flex-col justify-center gap-3 sm:flex-row">
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
          )}

          {/* Answer Composer */}
          {!isFinished && (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="interview-answer" className="block text-sm font-semibold text-text-primary mb-2">
                  Answer
                </label>

                {error && (
                  <p role="alert" className="mb-2 rounded-lg border border-danger/30 bg-danger/10 px-4 py-2.5 text-sm text-danger">
                    {error}
                  </p>
                )}

                <div className="rounded-2xl border border-border bg-[#f8fafc] p-4 shadow-xs dark:bg-surface-raised focus-within:border-accent focus-within:ring-2 focus-within:ring-[var(--color-focus)]">
                  <textarea
                    ref={composerRef}
                    id="interview-answer"
                    value={answer}
                    onChange={(event) => onAnswerChange(event.target.value)}
                    onKeyDown={handleComposerKeyDown}
                    disabled={submitting}
                    placeholder="Type your answer..."
                    aria-label="Your answer"
                    maxLength={12000}
                    className="w-full resize-none border-0 bg-transparent text-base leading-relaxed text-text-primary outline-none placeholder:text-text-muted disabled:cursor-wait disabled:text-text-muted"
                  />
                </div>
              </div>

              {/* Submit Button aligned to bottom right */}
              <div className="flex justify-end">
                <Button
                  type="submit"
                  size="md"
                  disabled={submitting || !answer.trim()}
                  aria-label={submitting ? 'Submitting' : error ? 'Retry answer' : 'Submit Answer'}
                  className="bg-[#78b3a4] hover:bg-[#669f91] text-white gap-2 px-6 py-2.5 rounded-xl font-medium shadow-xs"
                >
                  {submitting ? (
                    <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                  ) : (
                    <Send className="h-4 w-4" aria-hidden="true" />
                  )}
                  <span>{submitting ? 'Submitting...' : 'Submit Answer'}</span>
                </Button>
              </div>
            </form>
          )}
        </div>

        {/* Right Column (1 span): Candidate Profile Summary & Completed Turns */}
        <aside className="space-y-6 lg:col-span-1">
          {/* Top Card: Candidate Profile */}
          <div className="rounded-2xl border border-border bg-surface-raised p-5 shadow-xs">
            <h3 className="text-base font-bold text-text-primary">
              {candidateName}
            </h3>
            <p className="text-xs text-text-muted mt-0.5 mb-4">
              {candidateRole}
            </p>

            {candidateSkills.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {candidateSkills.map((skill) => (
                  <span
                    key={skill}
                    className="inline-flex items-center rounded-full bg-[#e6f4f1] px-3 py-1 text-xs font-medium text-[#2d7a6e] dark:bg-[#13352f] dark:text-[#5eead4]"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Bottom Card: Completed Turns */}
          <div className="rounded-2xl border border-border bg-surface-raised p-5 shadow-xs">
            <h3 className="text-sm font-bold text-text-primary mb-3">
              Completed Turns
            </h3>

            {state.completed_turns.length === 0 ? (
              <p className="text-xs text-text-muted">
                No completed turns yet.
              </p>
            ) : (
              <ol className="space-y-4 divide-y divide-border/60">
                {state.completed_turns.map((turn, index) => {
                  const response = answerText(turn)
                  return (
                    <li key={turn.turn_id} className={index > 0 ? 'pt-4' : ''}>
                      <div className="flex items-center justify-between gap-1 mb-1">
                        <span className="text-xs font-bold text-accent">
                          Turn {index + 1}
                        </span>
                        {turn.topic && (
                          <span className="text-[11px] text-text-muted truncate max-w-[130px]">
                            {turn.topic}
                          </span>
                        )}
                      </div>
                      <p className="text-xs font-medium text-text-primary line-clamp-2">
                        {questionText(turn)}
                      </p>
                      {response && (
                        <p className="mt-1.5 text-xs text-text-muted line-clamp-2 italic bg-surface p-2.5 rounded-lg border border-border/50">
                          "{response}"
                        </p>
                      )}
                    </li>
                  )
                })}
              </ol>
            )}
          </div>
        </aside>
      </div>
    </div>
  )
}

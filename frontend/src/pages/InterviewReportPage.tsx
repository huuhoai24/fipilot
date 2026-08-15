import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  AlertCircle,
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  ChevronDown,
  CircleCheckBig,
  History,
  Loader2,
  MessageSquarePlus,
  RefreshCw,
  Target,
} from 'lucide-react'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { Card, CardContent } from '@/components/ui/Card'
import { ApiError, api } from '@/lib/api'
import { cn } from '@/lib/utils'
import { getUserFacingError } from '@/lib/userFacingError'
import type {
  InterviewReport,
  V2InterviewSessionState,
  V2InterviewTurn,
} from '@/types'

type LoadPhase = 'loading' | 'generating' | 'ready' | 'incomplete' | 'error'

const coachingReplacements: Array<[RegExp, string]> = [
  [/(?:you|the candidate) may have exaggerated (?:your|their) experience/gi, 'Your answer did not demonstrate the experience described in your CV'],
  [/may have exaggerated experience/gi, 'did not demonstrate the experience described in the CV'],
  [/(?:you|the candidate) may be dishonest(?: about [^.!?]*)?/gi, 'Your answer did not provide enough detail to support the experience described'],
  [/major concern about authenticity/gi, 'large difference between the CV description and the depth demonstrated in the answer'],
]

function coachingText(value: string): string {
  return coachingReplacements.reduce(
    (text, [pattern, replacement]) => text.replace(pattern, replacement),
    value,
  )
}

function uniqueCoachingItems(items: string[]): string[] {
  const seen = new Set<string>()
  return items.flatMap((item) => {
    const normalized = coachingText(item).trim()
    const key = normalized.toLocaleLowerCase()
    if (!normalized || seen.has(key)) return []
    seen.add(key)
    return [normalized]
  })
}

function summarySentences(summary: string): string[] {
  return coachingText(summary).match(/[^.!?]+(?:[.!?]+|$)/g)?.map((sentence) => sentence.trim()).filter(Boolean) ?? []
}

function ScoreItem({ label, score }: { label: string; score: number }) {
  return (
    <div className="border-b border-border px-4 py-4 odd:border-r [&:nth-child(n+3)]:border-b-0 sm:border-b-0 sm:border-r sm:last:border-r-0 lg:px-6">
      <dt className="text-sm font-medium text-text-muted">{label}</dt>
      <dd className="mt-2 flex items-baseline gap-1">
        <span className="font-display text-3xl font-bold text-text-primary">{score.toFixed(1)}</span>
        <span className="text-sm text-text-faint">/10</span>
      </dd>
    </div>
  )
}

function questionText(turn: V2InterviewTurn): string {
  return typeof turn.question === 'string' ? turn.question : turn.question.question
}

function answerText(turn: V2InterviewTurn): string {
  return turn.answer?.trim() || turn.candidate_answer?.trim() || 'No answer was saved.'
}

function expectedSignals(turn: V2InterviewTurn): string[] {
  const answerPoints = typeof turn.question === 'string'
    ? []
    : turn.question.expected_answer_points ?? []
  return [...new Set([...(turn.expected_signal ?? []), ...answerPoints])]
}

function interviewIsComplete(state: V2InterviewSessionState): boolean {
  if (state.current_turn != null || state.pending_turn != null) return false
  if (state.phase === 'closing') return true
  return (
    state.completed_turns.length >= state.interview_config.question_count
  )
}

function FeedbackList({
  items,
  emptyText,
  icon: Icon,
  iconClassName,
}: {
  items: string[]
  emptyText: string
  icon: typeof CheckCircle2
  iconClassName: string
}) {
  const normalizedItems = uniqueCoachingItems(items)
  const visibleItems = normalizedItems.slice(0, 4)
  const hiddenItems = normalizedItems.slice(4)

  if (normalizedItems.length === 0) {
    return <p className="text-sm leading-6 text-text-faint">{emptyText}</p>
  }

  return (
    <>
      <ul className="space-y-3">
        {visibleItems.map((item, index) => (
          <li key={`${item}-${index}`} className="flex gap-3 text-sm leading-6 text-text-muted">
            <Icon className={cn('mt-1 h-4 w-4 shrink-0', iconClassName)} aria-hidden="true" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
      {hiddenItems.length > 0 && (
        <details className="mt-4 text-sm text-text-muted">
          <summary className="cursor-pointer font-medium text-text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent">
            Show {hiddenItems.length} more
          </summary>
          <ul className="mt-3 space-y-3 pl-1">
            {hiddenItems.map((item, index) => (
              <li key={`${item}-${index}`} className="flex gap-3 text-sm leading-6 text-text-muted">
                <Icon className={cn('mt-1 h-4 w-4 shrink-0', iconClassName)} aria-hidden="true" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </details>
      )}
    </>
  )
}

function QuestionReview({
  turn,
  index,
  expanded,
  onToggle,
}: {
  turn: V2InterviewTurn
  index: number
  expanded: boolean
  onToggle: () => void
}) {
  const evaluation = turn.evaluation
  const signals = expectedSignals(turn)
  const improvements = evaluation
    ? uniqueCoachingItems([...(evaluation.weaknesses ?? []), ...(evaluation.missing_concepts ?? [])])
    : []
  const panelId = `question-review-${turn.turn_id}`
  const triggerId = `question-review-trigger-${turn.turn_id}`

  return (
    <article className="border-b border-border last:border-b-0">
      <h3>
        <button
          id={triggerId}
          type="button"
          className="flex min-h-16 w-full items-center gap-4 px-4 py-4 text-left hover:bg-surface-raised sm:px-6"
          aria-expanded={expanded}
          aria-controls={panelId}
          onClick={onToggle}
        >
          <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-border bg-surface-raised text-xs font-semibold text-text-muted">
            {index + 1}
          </span>
          <span className="min-w-0 flex-1 text-sm font-semibold text-text-primary">
            Question {index + 1} <span className="font-normal text-text-faint">·</span> {turn.topic || 'General'}
          </span>
          {evaluation && (
            <span className="shrink-0 text-xs font-medium text-text-muted sm:text-sm">
              <span className="sr-only sm:not-sr-only">Score </span>{evaluation.overall_score.toFixed(1)}<span className="font-normal text-text-faint">/10</span>
            </span>
          )}
          <ChevronDown
            className={cn('h-5 w-5 shrink-0 text-text-faint', expanded && 'rotate-180')}
            aria-hidden="true"
          />
        </button>
      </h3>

      {expanded && (
        <div
          id={panelId}
          role="region"
          aria-labelledby={triggerId}
          className="border-t border-border px-4 py-6 sm:px-6"
        >
          <div className="grid gap-6 lg:grid-cols-[minmax(0,1.1fr)_minmax(18rem,0.9fr)]">
            <div className="space-y-6">
              <div>
                <h4 className="text-sm font-semibold text-text-primary">Question</h4>
                <p className="mt-2 text-sm leading-7 text-text-muted">{questionText(turn)}</p>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-text-primary">Your answer</h4>
                <blockquote className="mt-3 border-l-2 border-border pl-4 text-sm leading-7 text-text-muted">
                  {answerText(turn)}
                </blockquote>
              </div>

              {evaluation ? (
                <>
                  <div>
                    <h4 className="text-sm font-semibold text-text-primary">Coach feedback</h4>
                    <p className="mt-2 text-sm leading-7 text-text-muted">{coachingText(evaluation.feedback)}</p>
                  </div>
                  <div className="grid gap-5 sm:grid-cols-2">
                    <div>
                      <h4 className="mb-3 text-sm font-semibold text-text-primary">What worked</h4>
                      <FeedbackList
                        items={evaluation.strengths ?? []}
                        emptyText="No answer-specific strengths were recorded."
                        icon={CheckCircle2}
                        iconClassName="text-success"
                      />
                    </div>
                    <div>
                      <h4 className="mb-3 text-sm font-semibold text-text-primary">What to improve</h4>
                      <FeedbackList
                        items={improvements}
                        emptyText="No answer-specific improvements were recorded."
                        icon={Target}
                        iconClassName="text-warning"
                      />
                    </div>
                  </div>
                </>
              ) : (
                <p className="text-sm leading-6 text-text-faint">No detailed evaluation was saved for this answer.</p>
              )}
            </div>

            <aside className="self-start border-t border-border pt-5 lg:border-l lg:border-t-0 lg:pl-6 lg:pt-0" aria-labelledby={`${panelId}-signals`}>
              <h4 id={`${panelId}-signals`} className="text-sm font-semibold text-text-primary">
                What the interviewer was looking for
              </h4>
              {signals.length > 0 ? (
                <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-6 text-text-muted">
                  {signals.map((signal) => <li key={signal}>{signal}</li>)}
                </ul>
              ) : (
                <p className="mt-3 text-sm leading-6 text-text-faint">No expected signals were saved for this question.</p>
              )}
            </aside>
          </div>
        </div>
      )}
    </article>
  )
}

export function InterviewReportPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const [report, setReport] = useState<InterviewReport | null>(null)
  const [session, setSession] = useState<V2InterviewSessionState | null>(null)
  const [expandedTurnId, setExpandedTurnId] = useState<string | null>(null)
  const [phase, setPhase] = useState<LoadPhase>('loading')
  const [error, setError] = useState('')

  const loadReport = async () => {
    if (!sessionId) return
    setError('')
    setPhase('loading')

    try {
      const sessionResponse = await api.getV2InterviewSession(sessionId)
      setSession(sessionResponse.state)
      if (!interviewIsComplete(sessionResponse.state)) {
        setPhase('incomplete')
        return
      }
      setExpandedTurnId(sessionResponse.state.completed_turns[0]?.turn_id ?? null)
    } catch (sessionError) {
      setError(getUserFacingError(sessionError, 'The completed interview could not be loaded. Please try again.'))
      setPhase('error')
      return
    }

    try {
      const existing = await api.getInterviewReport(sessionId)
      setReport(existing.report)
      setPhase('ready')
      return
    } catch (loadError) {
      if (!(loadError instanceof ApiError) || loadError.status !== 404) {
        setError(getUserFacingError(loadError, 'The interview report could not be loaded. Please try again.'))
        setPhase('error')
        return
      }
    }

    setPhase('generating')
    try {
      const generated = await api.generateInterviewReport(sessionId)
      setReport(generated.report)
      setPhase('ready')
    } catch (generationError) {
      setError(getUserFacingError(generationError, 'The interview report could not be generated. Please try again.'))
      setPhase(generationError instanceof ApiError && generationError.status === 409 ? 'incomplete' : 'error')
    }
  }

  useEffect(() => {
    void loadReport()
  }, [sessionId])

  if (phase !== 'ready' || !report || !session) {
    return (
      <div className="mx-auto max-w-2xl py-12">
        <Card>
          <CardContent className="flex min-h-64 flex-col items-center justify-center text-center" aria-live="polite">
            {phase === 'loading' || phase === 'generating' ? (
              <>
                <Loader2 className="h-7 w-7 animate-spin text-accent" aria-hidden="true" />
                <h1 className="mt-4 text-lg font-semibold text-text-primary">
                  {phase === 'generating' ? 'Preparing your coaching report' : 'Checking interview completion'}
                </h1>
                <p className="mt-2 max-w-md text-sm text-text-muted">
                  {phase === 'generating'
                    ? 'FiPilot is reviewing your saved answers and evaluations.'
                    : 'FiPilot is confirming that the interview is complete.'}
                </p>
              </>
            ) : (
              <>
                <AlertCircle className="h-7 w-7 text-warning" aria-hidden="true" />
                <h1 className="mt-4 text-lg font-semibold text-text-primary">
                  {phase === 'incomplete' ? 'Interview still in progress' : 'Report unavailable'}
                </h1>
                <p className="mt-2 max-w-md text-sm text-text-muted">
                  {phase === 'incomplete'
                    ? 'Complete the remaining interview questions before opening coaching feedback.'
                    : error}
                </p>
                <div className="mt-6 flex w-full flex-col justify-center gap-2 sm:w-auto sm:flex-row">
                  {phase === 'incomplete' && sessionId ? (
                    <Button onClick={() => navigate(`/text-interview/${sessionId}`)}>Continue interview</Button>
                  ) : (
                    <Button onClick={() => void loadReport()}>
                      <RefreshCw className="h-4 w-4" aria-hidden="true" />
                      Try again
                    </Button>
                  )}
                  <Button variant="secondary" onClick={() => navigate('/interview-history')}>
                    Back to history
                  </Button>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>
    )
  }

  const strengths = report.strengths ?? []
  const weaknesses = report.weaknesses ?? []
  const skillAssessments = report.skill_assessments ?? []
  const demonstratedSkills = report.demonstrated_skills ?? []
  const missingSkills = report.missing_skills ?? []
  const recommendations = report.recommendations ?? []
  const learningPlan = report.learning_plan ?? []
  const sanitizedSummary = coachingText(report.summary)
  const sentences = summarySentences(report.summary)
  const summaryNeedsDisclosure = sentences.length > 4 || sanitizedSummary.length > 600
  const summaryPreview = summaryNeedsDisclosure ? sentences.slice(0, 3).join(' ') : sanitizedSummary
  const nextActions = uniqueCoachingItems([
    ...recommendations,
    ...learningPlan.map((item) => item.recommended_action),
  ]).slice(0, 5)

  return (
    <div className="mx-auto max-w-6xl space-y-8 pb-12">
      <header className="border-b border-border pb-6">
        <Button variant="ghost" size="sm" className="mb-5 -ml-3" onClick={() => navigate('/interview-history')}>
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          Interview history
        </Button>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div className="flex items-start gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full border border-accent bg-accent-soft">
              <CircleCheckBig className="h-6 w-6 text-accent" aria-hidden="true" />
            </div>
            <div>
              <h1 className="font-display text-3xl font-bold text-text-primary">Interview complete</h1>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-text-muted">
                Review what worked, where your answers can improve, and what to practice next.
              </p>
            </div>
          </div>
          <p className="pl-16 text-xs leading-5 text-text-faint sm:pl-0 sm:text-right">
            Practice coaching report<br />
            Generated {new Date(report.generated_at).toLocaleString()}
          </p>
        </div>
      </header>

      <section aria-labelledby="summary-heading">
        <div className="max-w-3xl">
          <h2 id="summary-heading" className="text-xl font-semibold text-text-primary">Overall coaching summary</h2>
          <p className="mt-3 text-base leading-8 text-text-muted">{summaryPreview}</p>
          {summaryNeedsDisclosure && (
            <details className="mt-3 text-sm text-text-muted">
              <summary className="cursor-pointer font-medium text-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent">
                Read full coaching summary
              </summary>
              <p className="mt-3 max-w-3xl leading-7">{sanitizedSummary}</p>
            </details>
          )}
        </div>
        <dl className="mt-6 grid grid-cols-2 overflow-hidden rounded-lg border border-border bg-surface sm:grid-cols-4">
          <ScoreItem label="Overall" score={report.overall_score} />
          <ScoreItem label="Technical" score={report.technical_score} />
          <ScoreItem label="Communication" score={report.communication_score} />
          <ScoreItem label="Correctness" score={report.correctness_score} />
        </dl>
        <p className="mt-2 text-xs text-text-faint">Scores use a 0–10 scale and summarize the saved answer evaluations.</p>
      </section>

      <section aria-labelledby="feedback-heading">
        <h2 id="feedback-heading" className="text-xl font-semibold text-text-primary">Your interview patterns</h2>
        <div className="mt-5 grid overflow-hidden rounded-lg border border-border bg-surface md:grid-cols-2 md:divide-x md:divide-border">
          <div className="border-b border-border p-5 md:border-b-0 md:p-6">
            <h3 className="mb-4 flex items-center gap-2 text-sm font-semibold text-text-primary">
              <CheckCircle2 className="h-4 w-4 text-success" aria-hidden="true" />
              Strengths
            </h3>
            <FeedbackList
              items={strengths}
              emptyText="No strengths were included in this report."
              icon={CheckCircle2}
              iconClassName="text-success"
            />
          </div>
          <div className="p-5 md:p-6">
            <h3 className="mb-4 flex items-center gap-2 text-sm font-semibold text-text-primary">
              <Target className="h-4 w-4 text-warning" aria-hidden="true" />
              Areas to improve
            </h3>
            <FeedbackList
              items={weaknesses}
              emptyText="No development areas were included in this report."
              icon={Target}
              iconClassName="text-warning"
            />
          </div>
        </div>
      </section>

      {(skillAssessments.length > 0 || demonstratedSkills.length > 0 || missingSkills.length > 0) && (
        <section aria-labelledby="skills-heading">
          <h2 id="skills-heading" className="text-xl font-semibold text-text-primary">Skills observed</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-text-muted">
            These observations come from the skills evaluated in your saved answers.
          </p>
          {(demonstratedSkills.length > 0 || missingSkills.length > 0) && (
            <dl className="mt-5 grid gap-4 border-y border-border py-5 sm:grid-cols-2">
              <div>
                <dt className="text-xs font-medium text-text-faint">Demonstrated</dt>
                <dd className="mt-2 flex flex-wrap gap-2">
                  {demonstratedSkills.length > 0
                    ? demonstratedSkills.map((skill) => <Badge key={skill} variant="success">{skill}</Badge>)
                    : <span className="text-sm text-text-faint">None recorded</span>}
                </dd>
              </div>
              <div>
                <dt className="text-xs font-medium text-text-faint">Evaluated but not yet demonstrated</dt>
                <dd className="mt-2 flex flex-wrap gap-2">
                  {missingSkills.length > 0
                    ? missingSkills.map((skill) => <Badge key={skill} variant="outline">{skill}</Badge>)
                    : <span className="text-sm text-text-faint">None recorded</span>}
                </dd>
              </div>
            </dl>
          )}
          {skillAssessments.length > 0 && (
            <details className="mt-4 rounded-lg border border-border bg-surface">
              <summary className="cursor-pointer px-4 py-4 text-sm font-semibold text-text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent sm:px-6">
                View detailed skill feedback ({skillAssessments.length})
              </summary>
              <div className="border-t border-border">
                {skillAssessments.map((assessment) => (
                  <article key={assessment.skill} className="grid gap-3 border-b border-border p-5 last:border-b-0 sm:grid-cols-[minmax(8rem,0.35fr)_minmax(0,1fr)] sm:p-6">
                    <div>
                      <h3 className="text-sm font-semibold text-text-primary">{assessment.skill}</h3>
                      <p className="mt-1 text-sm text-text-muted">{assessment.score.toFixed(1)}/10</p>
                    </div>
                    <div>
                      <p className="text-sm leading-6 text-text-muted">{coachingText(assessment.feedback)}</p>
                      {(assessment.evidence ?? []).length > 0 && (
                        <div className="mt-3 border-t border-border pt-3">
                          <p className="text-xs font-medium text-text-faint">Evidence from your answers</p>
                          <ul className="mt-2 list-disc space-y-1 pl-4 text-xs leading-5 text-text-muted">
                            {(assessment.evidence ?? []).map((item) => <li key={item}>{coachingText(item)}</li>)}
                          </ul>
                        </div>
                      )}
                    </div>
                  </article>
                ))}
              </div>
            </details>
          )}
        </section>
      )}

      <section aria-labelledby="questions-heading">
        <h2 id="questions-heading" className="text-xl font-semibold text-text-primary">Question-by-question review</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-text-muted">
          Compare each saved answer with its coaching feedback and the signals used during evaluation.
        </p>
        {session.completed_turns.length > 0 ? (
          <div className="mt-5 overflow-hidden rounded-lg border border-border bg-surface">
            {session.completed_turns.map((turn, index) => (
              <QuestionReview
                key={turn.turn_id}
                turn={turn}
                index={index}
                expanded={expandedTurnId === turn.turn_id}
                onToggle={() => setExpandedTurnId((current) => current === turn.turn_id ? null : turn.turn_id)}
              />
            ))}
          </div>
        ) : (
          <p className="mt-4 border-y border-border py-5 text-sm text-text-faint">
            No question-level review is available for this interview.
          </p>
        )}
      </section>

      <section aria-labelledby="next-steps-heading" className="border-t border-border pt-8">
        <div className="flex items-center gap-3">
          <BookOpen className="h-5 w-5 text-accent" aria-hidden="true" />
          <h2 id="next-steps-heading" className="text-xl font-semibold text-text-primary">Next steps</h2>
        </div>
        <div className="mt-5 max-w-3xl">
          <h3 className="text-sm font-semibold text-text-primary">Recommended practice</h3>
          {nextActions.length > 0 ? (
            <ol className="mt-3 space-y-3 text-sm leading-6 text-text-muted">
              {nextActions.map((item, index) => (
                <li key={`${item}-${index}`} className="flex gap-3">
                  <span className="font-semibold text-accent">{index + 1}.</span>
                  <span>{item}</span>
                </li>
              ))}
            </ol>
          ) : (
            <p className="mt-3 text-sm text-text-faint">No additional recommendations were included.</p>
          )}

          {learningPlan.length > 0 && (
            <details className="mt-5 border-y border-border py-4">
              <summary className="cursor-pointer text-sm font-semibold text-text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent">
                View learning plan details
              </summary>
              <div className="mt-3 divide-y divide-border">
                {learningPlan.map((item, index) => (
                  <article key={`${item.topic}-${index}`} className="py-4 first:pt-1">
                    <div className="flex flex-wrap items-baseline justify-between gap-2">
                      <h4 className="text-sm font-medium text-text-primary">{item.topic}</h4>
                      <span className="text-xs text-text-faint">Priority: {item.priority}</span>
                    </div>
                    <p className="mt-2 text-sm leading-6 text-text-muted">{coachingText(item.reason)}</p>
                    <p className="mt-2 text-sm font-medium leading-6 text-accent">
                      {coachingText(item.recommended_action)}
                    </p>
                  </article>
                ))}
              </div>
            </details>
          )}
        </div>

        <div className="mt-8 flex flex-col gap-3 border-t border-border pt-6 sm:flex-row">
          <Button onClick={() => navigate('/text-interview')}>
            <MessageSquarePlus className="h-4 w-4" aria-hidden="true" />
            Practice another interview
          </Button>
          <Button variant="secondary" onClick={() => navigate('/interview-history')}>
            <History className="h-4 w-4" aria-hidden="true" />
            Back to interview history
          </Button>
        </div>
      </section>
    </div>
  )
}

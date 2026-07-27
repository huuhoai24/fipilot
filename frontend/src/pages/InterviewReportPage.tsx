import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  AlertCircle,
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  Loader2,
  RefreshCw,
  Target,
} from 'lucide-react'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { ApiError, api } from '@/lib/api'
import type { HiringRecommendation, InterviewReport } from '@/types'

type LoadPhase = 'loading' | 'generating' | 'ready' | 'incomplete' | 'error'

const recommendationLabels: Record<HiringRecommendation, string> = {
  strong_hire: 'Strong Hire',
  hire: 'Hire',
  consider: 'Consider',
  no_hire: 'No Hire',
}

function ScoreItem({ label, score }: { label: string; score: number }) {
  return (
    <div className="border-b border-border px-5 py-6 last:border-b-0 sm:border-b-0 sm:border-r sm:last:border-r-0">
      <div className="text-xs font-semibold uppercase tracking-[0.14em] text-text-faint">{label}</div>
      <div className="mt-3 flex items-baseline gap-1">
        <span className="font-display text-4xl font-semibold tracking-tight-display text-text-primary">{score.toFixed(1)}</span>
        <span className="text-sm text-text-faint">/10</span>
      </div>
    </div>
  )
}

export function InterviewReportPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const [report, setReport] = useState<InterviewReport | null>(null)
  const [phase, setPhase] = useState<LoadPhase>('loading')
  const [error, setError] = useState('')

  const loadReport = async () => {
    if (!sessionId) return
    setError('')
    setPhase('loading')
    try {
      const existing = await api.getInterviewReport(sessionId)
      setReport(existing.report)
      setPhase('ready')
      return
    } catch (loadError) {
      if (!(loadError instanceof ApiError) || loadError.status !== 404) {
        setError(loadError instanceof Error ? loadError.message : 'Failed to load report')
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
      setError(generationError instanceof Error ? generationError.message : 'Failed to generate report')
      setPhase(generationError instanceof ApiError && generationError.status === 409 ? 'incomplete' : 'error')
    }
  }

  useEffect(() => {
    void loadReport()
  }, [sessionId])

  if (phase !== 'ready' || !report) {
    return (
      <div className="mx-auto max-w-2xl py-12">
        <Card>
          <CardContent className="flex min-h-64 flex-col items-center justify-center text-center">
            {phase === 'loading' || phase === 'generating' ? (
              <>
                <Loader2 className="h-7 w-7 animate-spin text-accent" />
                <h1 className="mt-4 text-lg font-semibold text-text-primary">
                  {phase === 'generating' ? 'Generating final report' : 'Loading interview report'}
                </h1>
                <p className="mt-1 text-sm text-text-muted">
                  {phase === 'generating' ? 'Reviewing all answers and evaluations.' : 'Checking for an existing report.'}
                </p>
              </>
            ) : (
              <>
                <AlertCircle className="h-7 w-7 text-warning" />
                <h1 className="mt-4 text-lg font-semibold text-text-primary">
                  {phase === 'incomplete' ? 'Interview not completed' : 'Report unavailable'}
                </h1>
                <p className="mt-2 max-w-md text-sm text-text-muted">{error}</p>
                <div className="mt-5 flex flex-wrap justify-center gap-2">
                  {phase === 'incomplete' && sessionId ? (
                    <Button onClick={() => navigate(`/text-interview/${sessionId}`)}>Continue Interview</Button>
                  ) : (
                    <Button onClick={() => void loadReport()}>
                      <RefreshCw className="h-4 w-4" />
                      Retry
                    </Button>
                  )}
                  <Button variant="secondary" onClick={() => navigate('/interview-history')}>
                    Back to History
                  </Button>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <Button variant="ghost" size="sm" className="mb-2 -ml-3" onClick={() => navigate('/interview-history')}>
            <ArrowLeft className="h-4 w-4" />
            Interview History
          </Button>
          <h1 className="font-display text-4xl font-semibold tracking-tight-display text-text-primary sm:text-5xl">Your interview report</h1>
          <p className="mt-3 text-sm text-text-muted">
            Generated {new Date(report.generated_at).toLocaleString()}
          </p>
        </div>
        <Badge variant={report.hiring_recommendation === 'no_hire' ? 'warning' : 'success'}>
          {recommendationLabels[report.hiring_recommendation]}
        </Badge>
      </div>

      <div className="hairline grid overflow-hidden rounded-[24px] border border-border bg-surface shadow-2xl shadow-black/10 sm:grid-cols-4">
        <ScoreItem label="Overall" score={report.overall_score} />
        <ScoreItem label="Technical" score={report.technical_score} />
        <ScoreItem label="Communication" score={report.communication_score} />
        <ScoreItem label="Correctness" score={report.correctness_score} />
      </div>

      <section className="rounded-[24px] border border-border bg-surface p-6 sm:p-8">
        <h2 className="font-display text-2xl font-semibold tracking-tight-display text-text-primary">What the interview showed</h2>
        <p className="mt-4 max-w-5xl text-base leading-8 text-text-muted">{report.summary}</p>
        <div className="mt-4 flex items-center gap-2 text-xs text-text-faint">
          <Target className="h-4 w-4 text-accent" />
          Confidence {Math.round(report.confidence_score * 100)}%
        </div>
      </section>

      <div className="grid gap-5 lg:grid-cols-2">
        <Card className="border-success/20">
          <CardHeader><CardTitle>Strengths</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            {report.strengths.map((item) => (
              <div key={item} className="flex gap-3 text-sm text-text-muted">
                <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-success" />
                <span>{item}</span>
              </div>
            ))}
          </CardContent>
        </Card>
        <Card className="border-warning/20">
          <CardHeader><CardTitle>Development Areas</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            {report.weaknesses.map((item) => (
              <div key={item} className="flex gap-3 text-sm text-text-muted">
                <Target className="mt-0.5 h-4 w-4 shrink-0 text-warning" />
                <span>{item}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <section>
        <div className="mb-3 flex items-center justify-between gap-3">
          <h2 className="font-display text-2xl font-semibold tracking-tight-display text-text-primary">Skill assessments</h2>
          <div className="flex flex-wrap justify-end gap-2">
            {report.demonstrated_skills.map((skill) => <Badge key={skill} variant="success">{skill}</Badge>)}
            {report.missing_skills.map((skill) => <Badge key={skill} variant="warning">{skill}</Badge>)}
          </div>
        </div>
        <div className="grid gap-3 lg:grid-cols-2">
          {report.skill_assessments.map((assessment) => (
            <Card key={assessment.skill} className="group transition-all duration-500 hover:-translate-y-1 hover:border-accent/30">
              <CardHeader>
                <CardTitle>{assessment.skill}</CardTitle>
                <Badge variant="accent">{assessment.score.toFixed(1)}/10</Badge>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-6 text-text-muted">{assessment.feedback}</p>
                {assessment.evidence.length > 0 && (
                  <ul className="mt-3 space-y-2 border-t border-border pt-3 text-xs leading-5 text-text-faint">
                    {assessment.evidence.map((item) => <li key={item}>{item}</li>)}
                  </ul>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.4fr)]">
        <Card>
          <CardHeader><CardTitle>Recommendations</CardTitle></CardHeader>
          <CardContent>
            <ol className="space-y-3 text-sm leading-6 text-text-muted">
              {report.recommendations.map((item, index) => <li key={item}>{index + 1}. {item}</li>)}
            </ol>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Learning Plan</CardTitle>
            <BookOpen className="h-4 w-4 text-accent" />
          </CardHeader>
          <CardContent className="divide-y divide-border p-0">
            {report.learning_plan.map((item) => (
              <div key={`${item.topic}-${item.priority}`} className="px-5 py-4">
                <div className="flex items-center justify-between gap-3">
                  <span className="text-sm font-medium text-text-primary">{item.topic}</span>
                  <Badge variant="accent">{item.priority}</Badge>
                </div>
                <p className="mt-2 text-sm text-text-muted">{item.reason}</p>
                <p className="mt-2 text-sm font-medium text-accent">{item.recommended_action}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

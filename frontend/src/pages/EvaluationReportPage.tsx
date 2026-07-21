import React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import {
  ArrowLeft,
  AlertTriangle,
  CheckCircle2,
  Download,
  Loader2,
  RotateCcw,
  ShieldAlert,
  Sparkles,
} from 'lucide-react'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { api } from '@/lib/api'
import { formatDate, recommendationLabel, scoreColor } from '@/lib/utils'

const recommendationVariant = {
  strong_hire: 'success',
  hire: 'success',
  consider: 'warning',
  reject: 'danger',
} as const

const difficultyLabel: Record<string, string> = {
  easy: 'Dễ',
  medium: 'Trung bình',
  hard: 'Khó',
}

const correctnessLabel: Record<string, string> = {
  Correct: 'Đúng',
  Partial: 'Một phần',
  Wrong: 'Sai',
}

const rubricLabel: Record<string, string> = {
  technical_accuracy: 'Độ chính xác kỹ thuật',
  depth: 'Độ sâu',
  clarity: 'Độ rõ ràng',
  relevance: 'Độ liên quan',
}

function getRecommendation(score: number, fallback?: string) {
  if (fallback) return fallback
  if (score >= 8) return 'strong_hire'
  if (score >= 7) return 'hire'
  if (score >= 5) return 'consider'
  return 'reject'
}

function asList(value: unknown): string[] {
  return Array.isArray(value) ? value.filter(Boolean).map(String) : []
}

export function EvaluationReportPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const sessionQuery = useQuery({
    queryKey: ['session', sessionId],
    queryFn: () => api.getSession(sessionId!),
    enabled: !!sessionId,
  })

  const reportQuery = useQuery({
    queryKey: ['report', sessionId],
    queryFn: () => api.getReport(sessionId!),
    enabled: !!sessionId,
    refetchInterval: (query) => {
      const status = query.state.data?.status
      return status === 'processing' || status === 'not_ready' ? 2500 : false
    },
  })

  const regenerateReport = async () => {
    if (!sessionId) return
    await api.endSession(sessionId)
    await queryClient.invalidateQueries({ queryKey: ['report', sessionId] })
    await queryClient.invalidateQueries({ queryKey: ['session', sessionId] })
  }

  const downloadReport = () => {
    const report = reportQuery.data?.report
    if (!report) return
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `evaluation-${sessionId}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  if (sessionQuery.isLoading || reportQuery.isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-accent" />
      </div>
    )
  }

  if (sessionQuery.isError || reportQuery.isError) {
    return (
      <div className="flex h-96 flex-col items-center justify-center gap-3 text-center">
        <AlertTriangle className="h-8 w-8 text-danger" />
        <div>
          <p className="text-sm font-medium text-text-primary">Không thể tải báo cáo</p>
          <p className="mt-1 text-sm text-text-muted">Vui lòng kiểm tra backend hoặc thử đánh giá lại phiên này.</p>
        </div>
        <Button variant="secondary" size="sm" onClick={regenerateReport}>
          <RotateCcw className="h-3.5 w-3.5" /> Đánh giá lại
        </Button>
      </div>
    )
  }

  const session = sessionQuery.data
  const reportResponse = reportQuery.data

  if (reportResponse?.status === 'processing' || reportResponse?.status === 'not_ready') {
    return (
      <div className="flex h-96 flex-col items-center justify-center gap-3 text-center">
        <Loader2 className="h-8 w-8 animate-spin text-accent" />
        <div>
          <p className="text-sm font-medium text-text-primary">Báo cáo đang được tạo</p>
          <p className="mt-1 text-sm text-text-muted">Trang sẽ tự cập nhật khi AI chấm xong.</p>
        </div>
      </div>
    )
  }

  const evaluation = reportResponse?.report
  if (!evaluation) {
    return (
      <div className="flex h-96 flex-col items-center justify-center gap-3 text-center">
        <AlertTriangle className="h-8 w-8 text-warning" />
        <div>
          <p className="text-sm font-medium text-text-primary">Chưa có dữ liệu đánh giá</p>
          <p className="mt-1 text-sm text-text-muted">Bạn có thể tạo lại report cho phiên này.</p>
        </div>
        <Button variant="secondary" size="sm" onClick={regenerateReport}>
          <RotateCcw className="h-3.5 w-3.5" /> Tạo report
        </Button>
      </div>
    )
  }

  const score = Number(evaluation.overall_score || 0)
  const maxScore = Number(evaluation.max_score || 10)
  const recommendation = getRecommendation(score, evaluation.hire_recommendation)
  const perQuestion = Array.isArray(evaluation.per_question) ? evaluation.per_question : []
  const strengths = asList(evaluation.strengths)
  const weaknesses = asList(evaluation.weaknesses)
  const improvementPlan = asList(evaluation.improvement_plan)
  const proctoring = evaluation.proctoring || session?.proctoring || {}
  const tabSwitchCount = Number(proctoring.tab_switch_count || 0)
  const windowBlurCount = Number(proctoring.window_blur_count || 0)

  return (
    <div className="space-y-6">
      <button
        onClick={() => navigate('/history')}
        className="flex items-center gap-1.5 text-sm text-text-muted transition-colors duration-150 hover:text-text-primary"
      >
        <ArrowLeft className="h-4 w-4" /> Quay lại History
      </button>

      <Card>
        <CardContent className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="font-display text-xl font-bold text-text-primary">
              {session?.candidate_name || 'Ứng viên'}
            </h1>
            <p className="text-sm text-text-muted">
              {session?.role || 'Interview'} · {session?.level || 'Level'} ·{' '}
              {session?.created_at ? formatDate(session.created_at, true) : 'Không rõ thời gian'}
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-xs text-text-muted">Tổng điểm</div>
              <div className={`font-mono text-2xl font-bold ${scoreColor(score, maxScore)}`}>
                {score.toFixed(1)} / {maxScore.toFixed(0)}
              </div>
            </div>
            <Badge variant={(recommendationVariant[recommendation as keyof typeof recommendationVariant] || 'default') as any} className="px-3 py-1 text-sm">
              {recommendationLabel(recommendation)}
            </Badge>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-accent" />
            <h2 className="text-sm font-semibold text-text-primary">Nhận xét chung</h2>
          </div>
          <p className="whitespace-pre-wrap text-sm leading-relaxed text-text-muted">
            {evaluation.final_feedback || 'AI chưa trả về nhận xét tổng quan.'}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <div className="mb-4 flex items-center gap-2">
            <ShieldAlert className="h-5 w-5 text-warning" />
            <h2 className="text-sm font-semibold text-text-primary">Giám sát trong lúc phỏng vấn</h2>
          </div>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <div className="rounded-lg border border-border bg-surface-raised p-3">
              <div className="text-xs uppercase text-text-muted">Chuyển tab</div>
              <div className="mt-1 font-mono text-xl font-bold text-text-primary">{tabSwitchCount}</div>
            </div>
            <div className="rounded-lg border border-border bg-surface-raised p-3">
              <div className="text-xs uppercase text-text-muted">Mất focus cửa sổ</div>
              <div className="mt-1 font-mono text-xl font-bold text-text-primary">{windowBlurCount}</div>
            </div>
            <div className="rounded-lg border border-border bg-surface-raised p-3">
              <div className="text-xs uppercase text-text-muted">Tổng cảnh báo</div>
              <div className="mt-1 font-mono text-xl font-bold text-text-primary">
                {Number(proctoring.total_events ?? tabSwitchCount + windowBlurCount)}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {evaluation.score_by_difficulty && (
        <Card>
          <CardContent>
            <h2 className="mb-4 text-sm font-semibold text-text-primary">Điểm theo độ khó</h2>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              {(['easy', 'medium', 'hard'] as const).map((difficulty) => {
                const value = Number(evaluation.score_by_difficulty[difficulty] || 0)
                return (
                  <div key={difficulty} className="rounded-lg border border-border bg-surface-raised p-3">
                    <div className="text-xs uppercase text-text-muted">{difficultyLabel[difficulty]}</div>
                    <div className={`mt-1 font-mono text-xl font-bold ${scoreColor(value)}`}>
                      {value.toFixed(1)}
                    </div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <Card>
          <CardContent>
            <div className="mb-4 flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-success" />
              <h2 className="text-sm font-semibold text-text-primary">Điểm mạnh</h2>
            </div>
            <ul className="space-y-2">
              {(strengths.length ? strengths : ['Chưa có điểm mạnh được ghi nhận.']).map((item, index) => (
                <li key={index} className="flex items-start gap-2 text-sm text-text-muted">
                  <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-success" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <div className="mb-4 flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-warning" />
              <h2 className="text-sm font-semibold text-text-primary">Cần cải thiện</h2>
            </div>
            <ul className="space-y-2">
              {(weaknesses.length ? weaknesses : ['Chưa có điểm yếu được ghi nhận.']).map((item, index) => (
                <li key={index} className="flex items-start gap-2 text-sm text-text-muted">
                  <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-warning" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>

      {perQuestion.length > 0 && (
        <Card>
          <CardContent>
            <h2 className="mb-4 text-sm font-semibold text-text-primary">Đánh giá từng câu</h2>
            <div className="space-y-3">
              {perQuestion.map((item: any, index: number) => {
                const itemScore = Number(item.score || 0)
                return (
                  <div key={`${item.question_id || index}`} className="rounded-lg border border-border bg-surface-raised p-4">
                    <div className="flex flex-wrap items-start justify-between gap-3">
                      <div className="min-w-0 flex-1">
                        <div className="text-xs text-text-muted">
                          Câu {item.question_id || index + 1} · {difficultyLabel[item.difficulty] || item.difficulty || 'Chuẩn'} · {correctnessLabel[item.correctness] || item.correctness || 'N/A'}
                        </div>
                        <p className="mt-1 text-sm font-medium text-text-primary">{item.question_text}</p>
                      </div>
                      <div className={`font-mono text-lg font-bold ${scoreColor(itemScore)}`}>
                        {itemScore.toFixed(1)}
                      </div>
                    </div>

                    {item.explanation && <p className="mt-3 text-sm text-text-muted">{item.explanation}</p>}

                    {item.rubric && Object.keys(item.rubric).length > 0 && (
                      <div className="mt-3 grid grid-cols-2 gap-2 text-xs md:grid-cols-4">
                        {Object.entries(item.rubric).map(([key, value]) => (
                          <div key={key} className="rounded-md border border-border bg-surface px-2 py-1.5">
                            <div className="text-text-muted">{rubricLabel[key] || key.replace(/_/g, ' ')}</div>
                            <div className="font-mono text-text-primary">{String(value)}/10</div>
                          </div>
                        ))}
                      </div>
                    )}

                    {asList(item.issues).length > 0 && (
                      <ul className="mt-3 space-y-1">
                        {asList(item.issues).map((issue, issueIndex) => (
                          <li key={issueIndex} className="text-xs text-warning">• {issue}</li>
                        ))}
                      </ul>
                    )}

                    {asList(item.keyword_hints).length > 0 && itemScore < 8 && (
                      <div className="mt-3 flex flex-wrap gap-1.5">
                        {asList(item.keyword_hints).map((keyword) => (
                          <span key={keyword} className="rounded-full border border-warning/30 bg-warning/10 px-2 py-1 text-xs text-warning">
                            {keyword}
                          </span>
                        ))}
                      </div>
                    )}

                    {item.suggestion && (
                      <div className="mt-3 rounded-md border border-accent/20 bg-accent-soft px-3 py-2 text-xs text-text-primary">
                        {item.suggestion}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {improvementPlan.length > 0 && (
        <Card>
          <CardContent>
            <h2 className="mb-4 text-sm font-semibold text-text-primary">Kế hoạch cải thiện</h2>
            <ol className="space-y-2">
              {improvementPlan.map((step, index) => (
                <li key={index} className="flex gap-3 text-sm text-text-muted">
                  <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-accent-soft text-xs font-semibold text-accent">
                    {index + 1}
                  </span>
                  <span>{step}</span>
                </li>
              ))}
            </ol>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardContent className="flex flex-wrap gap-2">
          <Button variant="secondary" size="sm" onClick={downloadReport}>
            <Download className="h-3.5 w-3.5" /> Xuất JSON
          </Button>
          <Button variant="outline" size="sm" onClick={regenerateReport} disabled={reportQuery.isFetching}>
            {reportQuery.isFetching ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <RotateCcw className="h-3.5 w-3.5" />}
            Đánh giá lại
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

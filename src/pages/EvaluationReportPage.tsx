import React from 'react'
import { useParams, useNavigate, Navigate } from 'react-router-dom'
import { Download, GitCompare, RotateCcw, ArrowLeft, CheckCircle2, AlertTriangle, Loader2 } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { mockSessions } from '@/data/mockData'
import { formatDate, scoreColor, recommendationLabel } from '@/lib/utils'
import { useAuthStore } from '@/store/useAuthStore'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function EvaluationReportPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const { currentUser } = useAuthStore()
  const isAdmin = currentUser?.role === 'admin'
  const session = mockSessions.find((s) => s.id === sessionId) ?? mockSessions[0]

  const { data, isLoading, isError } = useQuery({
    queryKey: ['report', sessionId],
    queryFn: () => api.getReport(sessionId!),
    enabled: !!sessionId
  })

  // Người dùng thường chỉ được xem report của phiên do chính họ tạo.
  if (!isAdmin && session.interviewer_email !== currentUser?.email) {
    return <Navigate to="/history" replace />
  }

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-accent" />
      </div>
    )
  }

  if (isError || !data || data.status !== 'success') {
    return (
      <div className="p-8 text-center text-danger">
        Không thể tải dữ liệu báo cáo hoặc phiên phỏng vấn chưa hoàn thành.
      </div>
    )
  }

  const evaluation = data.report
  const score = parseFloat(evaluation.overall_score) || 0
  
  const getRecommendation = (s: number) => {
    if (s >= 8) return 'strong_hire'
    if (s >= 7) return 'hire'
    if (s >= 5) return 'consider'
    return 'reject'
  }
  
  const recommendation = getRecommendation(score)
  
  const recommendationVariant = {
    strong_hire: 'success',
    hire: 'success',
    consider: 'warning',
    reject: 'danger',
  } as const

  return (
    <div className="space-y-6">
      <button
        onClick={() => navigate('/history')}
        className="flex items-center gap-1.5 text-sm text-text-muted hover:text-text-primary transition-colors duration-150"
      >
        <ArrowLeft className="h-4 w-4" /> Quay lại History
      </button>

      <Card>
        <CardContent className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="font-display text-xl font-bold tracking-tight-display text-text-primary">
              {session.candidate_name}
            </h1>
            <p className="text-sm text-text-muted">
              {session.template_title} · {formatDate(session.started_at, true)}
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-xs text-text-muted">Tổng điểm</div>
              <div className={`font-mono text-2xl font-bold ${scoreColor(score)}`}>
                {score.toFixed(1)} / 10
              </div>
            </div>
            <Badge variant={recommendationVariant[recommendation]} className="text-sm px-3 py-1">
              {recommendationLabel(recommendation)}
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* Summary */}
      <Card>
        <CardContent className="space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-text-primary mb-2">Nhận xét chung (Final Feedback)</h3>
            <p className="text-sm text-text-muted leading-relaxed whitespace-pre-wrap">{evaluation.final_feedback}</p>
          </div>
        </CardContent>
      </Card>

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardContent>
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle2 className="h-5 w-5 text-success" />
              <h3 className="text-sm font-semibold text-text-primary">Điểm mạnh</h3>
            </div>
            <ul className="space-y-2">
              {evaluation.strengths?.map((s: string, i: number) => (
                <li key={i} className="text-sm text-text-muted flex items-start gap-2">
                  <span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-success shrink-0" />
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent>
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="h-5 w-5 text-warning" />
              <h3 className="text-sm font-semibold text-text-primary">Điểm yếu cần cải thiện</h3>
            </div>
            <ul className="space-y-2">
              {evaluation.weaknesses?.map((w: string, i: number) => (
                <li key={i} className="text-sm text-text-muted flex items-start gap-2">
                  <span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-warning shrink-0" />
                  <span>{w}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>

      {/* Actions */}
      <Card>
        <CardContent className="flex flex-wrap gap-2">
          <Button variant="secondary" size="sm">
            <Download className="h-3.5 w-3.5" /> Xuất PDF
          </Button>
          <Button variant="secondary" size="sm">
            <GitCompare className="h-3.5 w-3.5" /> So sánh ứng viên
          </Button>
          <Button variant="outline" size="sm">
            <RotateCcw className="h-3.5 w-3.5" /> Đánh giá lại
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

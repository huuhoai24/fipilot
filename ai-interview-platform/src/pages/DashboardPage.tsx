import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Calendar, TrendingUp, FileStack, Clock3, ArrowRight, Play, X } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { dashboardStats } from '@/data/mockData'
import { scoreColor, scoreBarColor } from '@/lib/utils'
import { useAuthStore } from '@/store/useAuthStore'
import { useScheduleStore } from '@/store/useScheduleStore'
import { useActiveSessionStore } from '@/store/useActiveSessionStore'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function DashboardPage() {
  const navigate = useNavigate()
  const { currentUser } = useAuthStore()
  const { pending, removePending } = useScheduleStore()
  const startSession = useActiveSessionStore((s) => s.startSession)
  const isAdmin = currentUser?.role === 'admin'

  const { data: sessions = [] } = useQuery({
    queryKey: ['sessions'],
    queryFn: api.getSessions
  })

  const visibleSessions = isAdmin
    ? sessions
    : sessions.filter((s: any) => s.interviewer_email === currentUser?.email)

  const visiblePending = isAdmin
    ? pending
    : pending.filter((i) => i.interviewer_email === currentUser?.email)

  const recentEvaluations = visibleSessions.filter((s: any) => s.status === 'completed').slice(0, 4)
  const greetingName = currentUser?.username ?? dashboardStats.greetingName
  const pendingCount = visiblePending.length

  const statCards = [
    { label: 'Đang chờ phỏng vấn', value: pendingCount, icon: Calendar, accent: 'text-accent' },
    { label: 'Điểm trung bình tuần này', value: dashboardStats.avgScoreThisWeek.toFixed(1), icon: TrendingUp, accent: 'text-success' },
    { label: 'Bộ câu hỏi đang hoạt động', value: dashboardStats.activeTemplates, icon: FileStack, accent: 'text-text-primary' },
    { label: 'Đang chờ xem xét', value: dashboardStats.pendingReview, icon: Clock3, accent: 'text-warning' },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-1">
        <h1 className="font-display text-2xl font-bold tracking-tight-display text-text-primary">
          Chào buổi sáng, {greetingName} — {pendingCount} buổi phỏng vấn đang chờ
        </h1>
        <p className="text-sm text-text-muted">Đây là tổng quan hoạt động phỏng vấn của bạn.</p>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map(({ label, value, icon: Icon, accent }) => (
          <Card key={label} className="animate-fade-in">
            <CardContent className="flex items-center justify-between">
              <div>
                <div className="text-xs text-text-muted">{label}</div>
                <div className={`mt-1 font-display text-2xl font-bold tracking-tight-display ${accent}`}>{value}</div>
              </div>
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-raised">
                <Icon className="h-5 w-5 text-text-muted" />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Pending interviews */}
        <Card className="lg:col-span-2">
          <div className="flex items-center justify-between border-b border-border px-5 py-4">
            <h3 className="text-sm font-semibold text-text-primary">Buổi phỏng vấn đang chờ</h3>
            <Link to="/interview-flow" className="text-xs text-accent hover:underline flex items-center gap-1">
              Tạo mới <ArrowRight className="h-3 w-3" />
            </Link>
          </div>
          <div className="divide-y divide-border">
            {visiblePending.map((item) => (
              <div key={item.sessionId} className="flex items-center justify-between px-5 py-3.5">
                <div>
                  <div className="text-sm font-medium text-text-primary">{item.candidate}</div>
                  <div className="text-xs text-text-muted">{item.role}</div>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    size="sm"
                    variant="primary"
                    onClick={() => {
                      startSession({ sessionId: item.sessionId, candidateName: item.candidate })
                      removePending(item.sessionId)
                      navigate(`/interview-flow/session/${item.sessionId}`)
                    }}
                  >
                    <Play className="h-3.5 w-3.5" /> Bắt đầu
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => {
                      if (window.confirm(`Hủy buổi phỏng vấn với ${item.candidate}?`)) {
                        removePending(item.sessionId)
                      }
                    }}
                    className="hover:text-danger"
                  >
                    <X className="h-3.5 w-3.5" /> Hủy
                  </Button>
                </div>
              </div>
            ))}
            {visiblePending.length === 0 && (
              <div className="px-5 py-10 text-center text-sm text-text-muted">
                Không có buổi phỏng vấn nào đang chờ.
              </div>
            )}
          </div>
        </Card>

        {/* Recent evaluations */}
        <Card>
          <div className="border-b border-border px-5 py-4">
            <h3 className="text-sm font-semibold text-text-primary">Đánh giá gần đây</h3>
          </div>
          <div className="divide-y divide-border">
            {recentEvaluations.map((s: any) => (
              <Link
                key={s.id}
                to={`/history/${s.id}`}
                className="block px-5 py-3.5 hover:bg-surface-raised transition-colors duration-150"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-text-primary">{s.candidate_name}</span>
                  <span className={`font-mono text-sm font-semibold ${scoreColor(s.overall_score ?? 0)}`}>
                    {s.overall_score?.toFixed(1)}
                  </span>
                </div>
                <div className="mt-1.5 h-1.5 w-full overflow-hidden rounded-full bg-surface-raised">
                  <div
                    className={`h-full rounded-full ${scoreBarColor(s.overall_score ?? 0)}`}
                    style={{ width: `${((s.overall_score ?? 0) / 10) * 100}%` }}
                  />
                </div>
              </Link>
            ))}
            {recentEvaluations.length === 0 && (
              <div className="px-5 py-10 text-center text-sm text-text-muted">
                Chưa có đánh giá nào.
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  )
}

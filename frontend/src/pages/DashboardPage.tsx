import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  ArrowRight,
  CalendarCheck2,
  ClipboardCheck,
  Clock3,
  FileStack,
  Play,
  Search,
  TimerReset,
  TrendingUp,
  UserRoundCheck,
  X,
} from 'lucide-react'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { dashboardStats } from '@/data/mockData'
import { formatDate, scoreBarColor, scoreColor } from '@/lib/utils'
import { useAuthStore } from '@/store/useAuthStore'
import { useScheduleStore } from '@/store/useScheduleStore'
import { useActiveSessionStore } from '@/store/useActiveSessionStore'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

type SessionRow = {
  id: string
  candidate_name: string
  interviewer_email: string
  role: string
  level: number
  status: string
  started_at: string
  overall_score?: number
}

export function DashboardPage() {
  const navigate = useNavigate()
  const { currentUser } = useAuthStore()
  const { pending, removePending } = useScheduleStore()
  const startSession = useActiveSessionStore((s) => s.startSession)
  const isAdmin = currentUser?.role === 'admin'

  const { data: sessions = [] } = useQuery({
    queryKey: ['sessions'],
    queryFn: api.getSessions,
  })

  const visibleSessions: SessionRow[] = isAdmin
    ? sessions
    : sessions.filter((s: SessionRow) => s.interviewer_email === currentUser?.email)

  const visiblePending = isAdmin
    ? pending
    : pending.filter((i) => i.interviewer_email === currentUser?.email)

  const completed = visibleSessions.filter((s) => s.status === 'completed')
  const recentEvaluations = completed.slice(0, 5)
  const greetingName = currentUser?.username ?? dashboardStats.greetingName
  const pendingCount = visiblePending.length
  const averageScore =
    completed.length > 0
      ? completed.reduce((sum, s) => sum + (s.overall_score ?? 0), 0) / completed.length
      : dashboardStats.avgScoreThisWeek
  const interruptedCount = visibleSessions.filter((s) => s.status === 'interrupted').length

  const statCards = [
    {
      label: 'Đang chờ',
      value: pendingCount,
      detail: 'ứng viên sẵn sàng vào phòng',
      icon: CalendarCheck2,
      accent: 'text-accent',
    },
    {
      label: 'Điểm TB',
      value: averageScore.toFixed(1),
      detail: `${completed.length || 0} phiên đã chấm`,
      icon: TrendingUp,
      accent: 'text-success',
    },
    {
      label: 'Cần xem lại',
      value: interruptedCount + dashboardStats.pendingReview,
      detail: 'phiên gián đoạn hoặc thiếu review',
      icon: ClipboardCheck,
      accent: 'text-warning',
    },
    {
      label: 'Template',
      value: dashboardStats.activeTemplates,
      detail: 'bộ câu hỏi đang hoạt động',
      icon: FileStack,
      accent: 'text-text-primary',
    },
  ]

  return (
    <div className="space-y-5">
      <section className="grid gap-4 lg:grid-cols-[1.45fr_0.55fr]">
        <div className="border border-border bg-surface px-5 py-5 sm:px-6">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div className="min-w-0">
              <div className="mb-3 inline-flex items-center gap-2 rounded-md border border-border bg-surface-raised px-2.5 py-1 text-xs text-text-muted">
                <span className="h-1.5 w-1.5 rounded-full bg-accent" />
                Interview operations
              </div>
              <h1 className="max-w-3xl font-display text-2xl font-semibold leading-tight text-text-primary sm:text-3xl">
                Chào {greetingName}, hôm nay có {pendingCount} buổi phỏng vấn đang chờ xử lý.
              </h1>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-text-muted">
                Theo dõi queue, bắt đầu phiên mới và rà soát kết quả gần đây trong một màn hình làm việc gọn.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Link to="/history">
                <Button variant="secondary">
                  <Search className="h-4 w-4" /> Tra cứu kết quả
                </Button>
              </Link>
              <Link to="/interview-flow">
                <Button>
                  Tạo phiên mới <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </div>
          </div>
        </div>

        <Card>
          <CardContent className="flex h-full flex-col justify-between gap-5">
            <div>
              <div className="flex items-center gap-2 text-sm font-medium text-text-primary">
                <TimerReset className="h-4 w-4 text-accent" />
                Ca làm việc hiện tại
              </div>
              <p className="mt-2 text-sm leading-6 text-text-muted">
                Ưu tiên ứng viên đã có template match và CV đã trích xuất sạch trước.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="border border-border bg-surface-raised p-3">
                <div className="text-text-faint">Queue</div>
                <div className="mt-1 text-xl font-semibold text-text-primary">{pendingCount}</div>
              </div>
              <div className="border border-border bg-surface-raised p-3">
                <div className="text-text-faint">Completed</div>
                <div className="mt-1 text-xl font-semibold text-text-primary">{completed.length}</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      <section className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
        {statCards.map(({ label, value, detail, icon: Icon, accent }) => (
          <Card key={label}>
            <CardContent className="flex items-start justify-between gap-3 p-4">
              <div className="min-w-0">
                <div className="text-xs uppercase text-text-faint">{label}</div>
                <div className={`mt-2 font-mono text-2xl font-semibold ${accent}`}>{value}</div>
                <div className="mt-1 text-xs text-text-muted">{detail}</div>
              </div>
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-border bg-surface-raised">
                <Icon className="h-4 w-4 text-text-muted" />
              </div>
            </CardContent>
          </Card>
        ))}
      </section>

      <section className="grid grid-cols-1 gap-5 xl:grid-cols-[1fr_380px]">
        <Card>
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border px-5 py-4">
            <div>
              <h2 className="text-sm font-semibold text-text-primary">Queue phỏng vấn</h2>
              <p className="mt-1 text-xs text-text-muted">Bắt đầu nhanh hoặc hủy phiên chưa cần chạy.</p>
            </div>
            <Link to="/interview-flow" className="flex items-center gap-1 text-xs font-medium text-accent hover:text-accent-hover">
              Thêm ứng viên <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          <div className="divide-y divide-border">
            {visiblePending.map((item) => (
              <div key={item.sessionId} className="grid gap-3 px-5 py-4 md:grid-cols-[1fr_auto] md:items-center">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <div className="truncate text-sm font-semibold text-text-primary">{item.candidate}</div>
                    <span className="rounded-sm bg-accent-soft px-2 py-0.5 text-[11px] font-medium text-accent">
                      {item.role}
                    </span>
                  </div>
                  <div className="mt-1 flex flex-wrap items-center gap-3 text-xs text-text-muted">
                    <span className="flex items-center gap-1">
                      <Clock3 className="h-3.5 w-3.5" />
                      {formatDate(item.created_at, true)}
                    </span>
                    <span>{item.interviewer_email}</span>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2 md:justify-end">
                  <Button
                    size="sm"
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
              <div className="px-5 py-12 text-center">
                <UserRoundCheck className="mx-auto h-8 w-8 text-text-faint" />
                <div className="mt-3 text-sm font-medium text-text-primary">Queue đang trống</div>
                <p className="mt-1 text-sm text-text-muted">Tạo phiên mới sau khi tải CV và chọn template.</p>
              </div>
            )}
          </div>
        </Card>

        <Card>
          <div className="border-b border-border px-5 py-4">
            <h2 className="text-sm font-semibold text-text-primary">Kết quả gần đây</h2>
            <p className="mt-1 text-xs text-text-muted">Dùng để quyết định follow-up hoặc review sâu.</p>
          </div>
          <div className="divide-y divide-border">
            {recentEvaluations.map((s) => (
              <Link
                key={s.id}
                to={`/history/${s.id}`}
                className="block px-5 py-4 hover:bg-surface-raised"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="truncate text-sm font-semibold text-text-primary">{s.candidate_name}</div>
                    <div className="mt-1 text-xs text-text-muted">
                      L{s.level} {s.role.toUpperCase()} · {formatDate(s.started_at)}
                    </div>
                  </div>
                  <span className={`font-mono text-sm font-semibold ${scoreColor(s.overall_score ?? 0)}`}>
                    {s.overall_score?.toFixed(1)}
                  </span>
                </div>
                <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-surface-raised">
                  <div
                    className={`h-full ${scoreBarColor(s.overall_score ?? 0)}`}
                    style={{ width: `${((s.overall_score ?? 0) / 10) * 100}%` }}
                  />
                </div>
              </Link>
            ))}

            {recentEvaluations.length === 0 && (
              <div className="px-5 py-12 text-center text-sm text-text-muted">Chưa có đánh giá nào.</div>
            )}
          </div>
        </Card>
      </section>
    </div>
  )
}

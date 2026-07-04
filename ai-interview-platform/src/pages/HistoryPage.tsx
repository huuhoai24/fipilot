import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { Download, ChevronLeft, ChevronRight, Eye } from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Select, Input, Label } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import { formatDate, scoreColor } from '@/lib/utils'
import { useAuthStore } from '@/store/useAuthStore'
import type { SessionStatus } from '@/types'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'

const statusVariant: Record<SessionStatus, 'success' | 'warning' | 'danger' | 'default'> = {
  completed: 'success',
  interrupted: 'warning',
  no_show: 'danger',
  scheduled: 'default',
  in_progress: 'default',
}

const statusLabel: Record<SessionStatus, string> = {
  completed: 'Hoàn thành',
  interrupted: 'Bị ngắt',
  no_show: 'Không đến',
  scheduled: 'Đã lên lịch',
  in_progress: 'Đang diễn ra',
}

export function HistoryPage() {
  const { currentUser } = useAuthStore()
  const isAdmin = currentUser?.role === 'admin'

  const [roleFilter, setRoleFilter] = useState('all')
  const [minScore, setMinScore] = useState('0')
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const pageSize = 5

  const { data: sessions = [], isLoading } = useQuery({
    queryKey: ['sessions'],
    queryFn: api.getSessions
  })

  const visibleSessions = isAdmin
    ? sessions
    : sessions.filter((s: any) => s.interviewer_email === currentUser?.email)

  const filtered = visibleSessions.filter((s: any) => {
    if (roleFilter !== 'all' && s.role !== roleFilter) return false
    if ((s.overall_score ?? 0) < Number(minScore)) return false
    if (search && !s.candidate_name.toLowerCase().includes(search.toLowerCase())) return false
    return true
  })

  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize))
  const pageRows = filtered.slice((page - 1) * pageSize, page * pageSize)

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl font-bold tracking-tight-display text-text-primary">History</h1>
          <p className="mt-1 text-sm text-text-muted">
            {isAdmin
              ? 'Toàn bộ phiên phỏng vấn của tất cả tài khoản.'
              : 'Các phiên phỏng vấn bạn đã thực hiện.'}
          </p>
        </div>
        <Button variant="secondary">
          <Download className="h-4 w-4" /> Export CSV
        </Button>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-end gap-3">
        <div className="w-44">
          <Label>Vai trò</Label>
          <Select value={roleFilter} onChange={(e) => setRoleFilter(e.target.value)}>
            <option value="all">Tất cả</option>
            <option value="data-ai">Data-AI</option>
          </Select>
        </div>
        <div className="w-40">
          <Label>Điểm tối thiểu</Label>
          <Select value={minScore} onChange={(e) => setMinScore(e.target.value)}>
            <option value="0">Tất cả</option>
            <option value="6">≥ 6</option>
            <option value="7">≥ 7</option>
            <option value="8">≥ 8</option>
          </Select>
        </div>
        <div className="flex-1 min-w-[200px]">
          <Label>Tìm ứng viên</Label>
          <Input placeholder="Tên ứng viên…" value={search} onChange={(e) => setSearch(e.target.value)} />
        </div>
      </div>

      {/* Table */}
      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-surface-raised text-xs text-text-muted">
                <th className="px-5 py-3 text-left font-medium">Ngày</th>
                <th className="px-5 py-3 text-left font-medium">Ứng viên</th>
                {isAdmin && <th className="px-5 py-3 text-left font-medium">Người phỏng vấn</th>}
                <th className="px-5 py-3 text-left font-medium">Vai trò</th>
                <th className="px-5 py-3 text-left font-medium">Trạng thái</th>
                <th className="px-5 py-3 text-right font-medium">Điểm</th>
                <th className="px-5 py-3 text-right font-medium">Hành động</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {pageRows.map((s: any) => (
                <tr key={s.id} className="hover:bg-surface-raised transition-colors duration-150">
                  <td className="px-5 py-3 text-text-muted font-mono text-xs">{formatDate(s.started_at)}</td>
                  <td className="px-5 py-3 font-medium text-text-primary">{s.candidate_name}</td>
                  {isAdmin && (
                    <td className="px-5 py-3 text-text-muted text-xs">{s.interviewer_email}</td>
                  )}
                  <td className="px-5 py-3 text-text-muted">L{s.level} {s.role.toUpperCase()}</td>
                  <td className="px-5 py-3">
                    <Badge variant={(statusVariant[s.status as SessionStatus] || 'default') as any}>
                      {statusLabel[s.status as SessionStatus] || s.status}
                    </Badge>
                  </td>
                  <td className="px-5 py-3 text-right font-mono font-semibold">
                    {s.overall_score !== undefined ? (
                      <span className={scoreColor(s.overall_score)}>{s.overall_score.toFixed(1)}</span>
                    ) : (
                      <span className="text-text-faint">—</span>
                    )}
                  </td>
                  <td className="px-5 py-3 text-right">
                    <div className="flex justify-end gap-1.5">
                      <Link to={`/history/${s.id}`}>
                        <Button variant="ghost" size="sm">
                          <Eye className="h-3.5 w-3.5" /> Xem
                        </Button>
                      </Link>
                      <Button variant="ghost" size="sm">
                        <Download className="h-3.5 w-3.5" /> Export
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
              {pageRows.length === 0 && (
                <tr>
                  <td colSpan={isAdmin ? 7 : 6} className="px-5 py-10 text-center text-text-muted">
                    Không có phiên phỏng vấn phù hợp với bộ lọc.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between border-t border-border px-5 py-3">
          <Button variant="ghost" size="sm" disabled={page === 1} onClick={() => setPage((p) => p - 1)}>
            <ChevronLeft className="h-4 w-4" /> Trước
          </Button>
          <span className="text-xs text-text-muted">
            Trang {page} / {totalPages}
          </span>
          <Button variant="ghost" size="sm" disabled={page === totalPages} onClick={() => setPage((p) => p + 1)}>
            Sau <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </Card>
    </div>
  )
}

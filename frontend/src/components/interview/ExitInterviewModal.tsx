import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AlertTriangle, Award, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { useUIStore } from '@/store/useAppStore'
import { api } from '@/lib/api'

export function ExitInterviewModal() {
  const navigate = useNavigate()
  const [finishing, setFinishing] = useState(false)
  const {
    confirmExitOpen,
    setConfirmExitOpen,
    activeInterview,
    setActiveInterview,
    pendingNavigation,
    setPendingNavigation,
  } = useUIStore()

  if (!confirmExitOpen) return null

  const handleStay = () => {
    if (finishing) return
    setConfirmExitOpen(false)
    setPendingNavigation(null)
  }

  const handleStopAndReport = async () => {
    const sessionId = activeInterview?.sessionId
    if (!sessionId) {
      setActiveInterview(null)
      setConfirmExitOpen(false)
      setPendingNavigation(null)
      navigate('/interview-history')
      return
    }

    setFinishing(true)
    try {
      await api.endV2Interview(sessionId)
    } catch {
      // If end endpoint fails, still proceed to report/history gracefully
    } finally {
      setActiveInterview(null)
      setConfirmExitOpen(false)
      setPendingNavigation(null)
      setFinishing(false)
      navigate(`/text-interview/${sessionId}/report`)
    }
  }

  const handleLeaveWithoutReport = () => {
    if (finishing) return
    const target = pendingNavigation || '/text-interview'
    setActiveInterview(null)
    setConfirmExitOpen(false)
    setPendingNavigation(null)
    navigate(target)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="exit-interview-title"
        className="w-full max-w-md rounded-2xl border border-border bg-surface-raised p-6 shadow-xl"
      >
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-amber-500/10 text-amber-500">
            <AlertTriangle className="h-6 w-6" aria-hidden="true" />
          </div>

          <div className="min-w-0 flex-1">
            <h3 id="exit-interview-title" className="text-lg font-bold text-text-primary">
              Buổi phỏng vấn đang diễn ra
            </h3>
            <p className="mt-2 text-sm leading-relaxed text-text-muted">
              Bạn đang trong buổi phỏng vấn. Nếu bạn rời khỏi bây giờ, bạn có thể chọn dừng phỏng vấn để hệ thống chấm điểm và xuất báo cáo cho các câu đã trả lời.
            </p>
          </div>
        </div>

        <div className="mt-6 flex flex-col-reverse gap-2.5 sm:flex-row sm:justify-end">
          <Button
            type="button"
            variant="outline"
            disabled={finishing}
            onClick={handleStay}
            className="w-full sm:w-auto"
          >
            Ở lại phỏng vấn
          </Button>

          <Button
            type="button"
            variant="secondary"
            disabled={finishing}
            onClick={handleLeaveWithoutReport}
            className="w-full text-xs text-text-muted hover:text-danger sm:w-auto"
          >
            Rời khỏi
          </Button>

          <Button
            type="button"
            disabled={finishing}
            onClick={() => void handleStopAndReport()}
            className="w-full gap-2 bg-[#78b3a4] hover:bg-[#669f91] text-white sm:w-auto"
          >
            {finishing ? (
              <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
            ) : (
              <Award className="h-4 w-4" aria-hidden="true" />
            )}
            <span>{finishing ? 'Đang chấm điểm...' : 'Dừng & Chấm điểm'}</span>
          </Button>
        </div>
      </div>
    </div>
  )
}

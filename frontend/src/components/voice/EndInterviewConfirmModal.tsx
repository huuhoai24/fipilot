import React from 'react'
import { AlertCircle } from 'lucide-react'

interface EndInterviewConfirmModalProps {
  isOpen: boolean
  onCancel: () => void
  onConfirm: () => void
}

export function EndInterviewConfirmModal({
  isOpen,
  onCancel,
  onConfirm,
}: EndInterviewConfirmModalProps) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm">
      <div
        className="w-full max-w-md rounded-2xl border border-white/10 bg-[#16181e] p-6 text-white shadow-2xl animate-fade-in"
        role="dialog"
        aria-modal="true"
        aria-labelledby="end-dialog-title"
      >
        <div className="flex items-center gap-3 text-red-400">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-red-500/10 border border-red-500/20">
            <AlertCircle className="h-5 w-5" />
          </div>
          <h2 id="end-dialog-title" className="text-lg font-semibold text-white">
            End Voice Interview?
          </h2>
        </div>

        <p className="mt-3 text-sm text-white/70">
          Are you sure you want to end this interview session? Your responses will be saved, and your final performance report will be generated.
        </p>

        <div className="mt-6 flex items-center justify-end gap-3 pt-4 border-t border-white/10">
          <button
            type="button"
            onClick={onCancel}
            className="rounded-lg px-4 py-2 text-sm font-medium text-white/70 hover:bg-white/10 hover:text-white transition-colors"
          >
            Continue Interview
          </button>
          <button
            type="button"
            onClick={onConfirm}
            className="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-500 transition-colors shadow-lg shadow-red-600/20"
          >
            End Interview
          </button>
        </div>
      </div>
    </div>
  )
}

import React from 'react'
import { BrainCircuit, Loader2, Mic, Volume2, Zap } from 'lucide-react'
import { cn } from '@/lib/utils'
import { VoiceInterviewState } from '@/types'

interface VoiceMicrophoneButtonProps {
  state: VoiceInterviewState
  disabled?: boolean
  onClick?: () => void
}

const buttonLabels: Record<VoiceInterviewState, string> = {
  [VoiceInterviewState.IDLE]: 'Sẵn sàng',
  [VoiceInterviewState.AI_THINKING]: 'AI đang suy nghĩ câu hỏi...',
  [VoiceInterviewState.AI_SPEAKING]: 'AI đang đọc câu hỏi (vui lòng nghe)',
  [VoiceInterviewState.WAITING_FOR_USER]: 'Bắt đầu trả lời',
  [VoiceInterviewState.USER_SPEAKING]: 'Dừng & nộp câu trả lời',
  [VoiceInterviewState.TRANSCRIBING]: 'Đang nhận dạng câu trả lời...',
  [VoiceInterviewState.EVALUATING]: 'Đang chấm điểm & đánh giá...',
  [VoiceInterviewState.INTERRUPTED]: 'Đã dừng nói',
}

export function VoiceMicrophoneButton({
  state,
  disabled = false,
  onClick,
}: VoiceMicrophoneButtonProps) {
  const isListening = state === VoiceInterviewState.USER_SPEAKING
  const isProcessing = state === VoiceInterviewState.EVALUATING
    || state === VoiceInterviewState.AI_THINKING
    || state === VoiceInterviewState.TRANSCRIBING
  const isReady = state === VoiceInterviewState.WAITING_FOR_USER
  const isSpeaking = state === VoiceInterviewState.AI_SPEAKING
  const isButtonDisabled = disabled || !onClick || isSpeaking || isProcessing

  const Icon = isListening
    ? Mic
    : state === VoiceInterviewState.AI_THINKING
      ? BrainCircuit
      : state === VoiceInterviewState.INTERRUPTED
        ? Zap
        : isProcessing
          ? Loader2
          : isSpeaking
            ? Volume2
            : isReady
              ? Mic
              : Mic

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative flex h-36 w-36 items-center justify-center sm:h-40 sm:w-40">
        {isListening && (
          <span
            className="absolute inset-3 animate-pulse-ring rounded-full border border-danger/50"
            aria-hidden="true"
          />
        )}
        <button
          type="button"
          onClick={onClick}
          disabled={isButtonDisabled}
          aria-label={buttonLabels[state]}
          aria-pressed={isListening}
          className={cn(
            'relative flex h-28 w-28 items-center justify-center rounded-full border shadow-lg transition-all sm:h-32 sm:w-32',
            'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-focus',
            isListening && 'border-danger bg-danger text-white hover:scale-[1.03] cursor-pointer',
            state === VoiceInterviewState.IDLE && 'border-accent bg-accent text-accent-contrast hover:scale-[1.03] hover:bg-accent-hover cursor-pointer',
            isReady && 'border-accent bg-[#78b3a4] text-white hover:bg-[#669f91] hover:scale-[1.03] cursor-pointer',
            isProcessing && 'cursor-not-allowed border-border bg-surface-raised text-text-muted opacity-80',
            isSpeaking && 'cursor-not-allowed border-accent/40 bg-accent-soft/50 text-accent opacity-80',
            disabled && 'cursor-not-allowed opacity-50'
          )}
        >
          <Icon className={cn('h-10 w-10 sm:h-12 sm:w-12', isProcessing && 'animate-spin')} />
        </button>
      </div>
      <span className={cn(
        'text-sm font-semibold',
        isListening ? 'text-danger animate-pulse' : isSpeaking ? 'text-accent' : 'text-text-primary'
      )}>
        {buttonLabels[state]}
      </span>
    </div>
  )
}

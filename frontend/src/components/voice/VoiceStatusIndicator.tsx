import React from 'react'
import { BrainCircuit, Loader2, Mic, Radio, Volume2, Zap } from 'lucide-react'
import { VoiceInterviewState } from '@/types'

interface VoiceStatusIndicatorProps {
  state: VoiceInterviewState
  elapsedSeconds: number
}

function formatElapsed(seconds: number): string {
  const minutes = Math.floor(seconds / 60)
  const remainder = seconds % 60
  return `${minutes.toString().padStart(2, '0')}:${remainder.toString().padStart(2, '0')}`
}

export function VoiceStatusIndicator({ state, elapsedSeconds }: VoiceStatusIndicatorProps) {
  const content = {
    [VoiceInterviewState.IDLE]: {
      icon: Radio,
      title: 'Sẵn sàng',
      detail: 'Microphone tắt cho đến khi bạn bấm bắt đầu trả lời.',
      color: 'text-text-muted',
    },
    [VoiceInterviewState.WAITING_FOR_USER]: {
      icon: Radio,
      title: 'Sẵn sàng trả lời',
      detail: 'Bấm nút micro ở trên khi bạn đã sẵn sàng nói.',
      color: 'text-accent',
    },
    [VoiceInterviewState.USER_SPEAKING]: {
      icon: Mic,
      title: 'Đang ghi âm câu trả lời',
      detail: `${formatElapsed(elapsedSeconds)} - Bấm lại nút micro khi bạn đã trả lời xong.`,
      color: 'text-danger',
    },
    [VoiceInterviewState.EVALUATING]: {
      icon: Loader2,
      title: 'Đang đánh giá câu trả lời...',
      detail: 'Hệ thống đang chấm điểm và chuẩn bị câu hỏi tiếp theo.',
      color: 'text-warning',
    },
    [VoiceInterviewState.TRANSCRIBING]: {
      icon: Loader2,
      title: 'Đang nhận dạng giọng nói...',
      detail: 'Hệ thống đang chuyển đổi câu trả lời thành văn bản.',
      color: 'text-warning',
    },
    [VoiceInterviewState.AI_THINKING]: {
      icon: BrainCircuit,
      title: 'AI đang suy nghĩ...',
      detail: 'AI đang chuẩn bị câu hỏi tiếp theo.',
      color: 'text-warning',
    },
    [VoiceInterviewState.AI_SPEAKING]: {
      icon: Volume2,
      title: 'AI đang đọc câu hỏi',
      detail: 'Vui lòng lắng nghe AI đọc hết câu trước khi bấm trả lời.',
      color: 'text-accent',
    },
    [VoiceInterviewState.INTERRUPTED]: {
      icon: Zap,
      title: 'Interrupted',
      detail: 'Switching to your answer.',
      color: 'text-warning',
    },
  }[state]
  const Icon = content.icon

  return (
    <div
      className="flex min-h-16 items-center justify-center gap-3 text-center"
      role="status"
      aria-live="polite"
      aria-atomic="true"
    >
      <Icon
        className={`h-5 w-5 shrink-0 ${content.color} ${
          state === VoiceInterviewState.EVALUATING
          || state === VoiceInterviewState.AI_THINKING
          || state === VoiceInterviewState.TRANSCRIBING
            ? 'animate-spin'
            : ''
        }`}
        aria-hidden="true"
      />
      <div className="text-left">
        <div className="text-sm font-semibold text-text-primary">{content.title}</div>
        <div className="mt-0.5 text-xs text-text-muted">{content.detail}</div>
      </div>
    </div>
  )
}

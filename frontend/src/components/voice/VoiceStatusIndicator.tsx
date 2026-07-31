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
      title: 'Ready',
      detail: 'The microphone stays off until you start your answer.',
      color: 'text-text-muted',
    },
    [VoiceInterviewState.WAITING_FOR_USER]: {
      icon: Radio,
      title: 'Ready for your answer',
      detail: 'Press the microphone button when you are ready to speak.',
      color: 'text-accent',
    },
    [VoiceInterviewState.USER_SPEAKING]: {
      icon: Mic,
      title: 'Recording your answer',
      detail: `${formatElapsed(elapsedSeconds)} - pauses are okay; press Stop when finished.`,
      color: 'text-danger',
    },
    [VoiceInterviewState.EVALUATING]: {
      icon: Loader2,
      title: 'Evaluating your response...',
      detail: 'Preparing the next interview decision.',
      color: 'text-warning',
    },
    [VoiceInterviewState.TRANSCRIBING]: {
      icon: Loader2,
      title: 'Understanding your answer...',
      detail: 'Speech recognition is finalizing the transcript.',
      color: 'text-warning',
    },
    [VoiceInterviewState.AI_THINKING]: {
      icon: BrainCircuit,
      title: 'AI interviewer is thinking',
      detail: 'Selecting the next question.',
      color: 'text-warning',
    },
    [VoiceInterviewState.AI_SPEAKING]: {
      icon: Volume2,
      title: 'AI interviewer speaking',
      detail: 'Speak naturally to interrupt and answer.',
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

import React from 'react'
import { BrainCircuit, Loader2, Mic, Radio, Volume2, Zap } from 'lucide-react'
import { cn } from '@/lib/utils'
import { VoiceInterviewState } from '@/types'

interface VoiceMicrophoneButtonProps {
  state: VoiceInterviewState
  disabled?: boolean
  onClick?: () => void
}

const buttonLabels: Record<VoiceInterviewState, string> = {
  [VoiceInterviewState.IDLE]: 'Start speaking',
  [VoiceInterviewState.AI_THINKING]: 'AI interviewer is thinking',
  [VoiceInterviewState.AI_SPEAKING]: 'AI interviewer is speaking',
  [VoiceInterviewState.WAITING_FOR_USER]: 'Waiting for your answer',
  [VoiceInterviewState.USER_SPEAKING]: 'Listening to your answer',
  [VoiceInterviewState.TRANSCRIBING]: 'Transcribing answer',
  [VoiceInterviewState.EVALUATING]: 'Evaluating answer',
  [VoiceInterviewState.INTERRUPTED]: 'AI speech interrupted',
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
              ? Radio
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
          disabled={disabled || !onClick}
          aria-label={buttonLabels[state]}
          aria-pressed={isListening}
          className={cn(
            'relative flex h-28 w-28 items-center justify-center rounded-full border shadow-lg transition-transform sm:h-32 sm:w-32',
            'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-focus',
            isListening && 'border-danger bg-danger text-white hover:scale-[1.03]',
            state === VoiceInterviewState.IDLE && 'border-accent bg-accent text-white hover:scale-[1.03] hover:bg-accent-hover',
            isReady && 'border-accent bg-accent-soft text-accent',
            isProcessing && 'cursor-not-allowed border-border bg-surface-raised text-text-muted',
            isSpeaking && 'cursor-not-allowed border-accent/40 bg-accent-soft text-accent',
            disabled && 'cursor-not-allowed opacity-50'
          )}
        >
          <Icon className={cn('h-10 w-10 sm:h-12 sm:w-12', isProcessing && 'animate-spin')} />
        </button>
      </div>
      <span className="text-sm font-semibold text-text-primary">{buttonLabels[state]}</span>
    </div>
  )
}

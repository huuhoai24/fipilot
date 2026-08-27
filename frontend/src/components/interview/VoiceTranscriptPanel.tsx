import { useEffect, useRef, useState } from 'react'
import { Send } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/Button'
import { SpeakerGlyph } from '@/components/voice/SpeakerGlyph'
import { VoiceInterviewState } from '@/types'
import type { V2InterviewTurn } from '@/types'

interface VoiceTranscriptPanelProps {
  completedTurns: V2InterviewTurn[]
  currentQuestion: string
  questionStreaming: boolean
  interimTranscript: string
  voiceState: VoiceInterviewState
  canAnswer: boolean
  onSendText: (text: string) => void
}

function questionText(turn?: V2InterviewTurn | null): string {
  if (!turn) return ''
  return typeof turn.question === 'string' ? turn.question : turn.question.question
}

function listeningStatus(voiceState: VoiceInterviewState): string | null {
  switch (voiceState) {
    case VoiceInterviewState.USER_SPEAKING:
      return 'Đang ghi âm câu trả lời'
    case VoiceInterviewState.AI_SPEAKING:
      return 'Nhà phỏng vấn AI đang nói'
    case VoiceInterviewState.TRANSCRIBING:
      return 'Đang hiểu câu trả lời của bạn...'
    case VoiceInterviewState.EVALUATING:
      return 'Đang đánh giá câu trả lời...'
    case VoiceInterviewState.WAITING_FOR_USER:
      return 'Sẵn sàng cho câu trả lời'
    default:
      return null
  }
}

export function VoiceTranscriptPanel({
  completedTurns,
  currentQuestion,
  questionStreaming,
  interimTranscript,
  voiceState,
  canAnswer,
  onSendText,
}: VoiceTranscriptPanelProps) {
  const [draft, setDraft] = useState('')
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    setDraft(interimTranscript)
  }, [interimTranscript])

  const submit = () => {
    const text = draft.trim()
    if (!text || !canAnswer) return
    onSendText(text)
    setDraft('')
  }

  const aiSpeaking = voiceState === VoiceInterviewState.AI_SPEAKING
  const thinking = voiceState === VoiceInterviewState.AI_THINKING
  const status = listeningStatus(voiceState)

  return (
    <div className="flex h-[340px] w-full flex-col">
      <div
        ref={scrollRef}
        className="flex-1 space-y-4 overflow-y-auto rounded-2xl border border-white/10 bg-[#0f1117] p-4"
        aria-live="polite"
      >
        {completedTurns.length === 0 && !currentQuestion && (
          <p className="text-center text-sm text-white/40">
            Nhà phỏng vấn sẽ sớm bắt đầu nói.
          </p>
        )}

        {completedTurns.map((turn, index) => (
          <div key={turn.turn_id || index} className="space-y-2">
            <div className="flex items-start gap-2">
              <span className="mt-1 shrink-0 rounded-full bg-accent/15 p-1.5 text-accent">
                <SpeakerGlyph />
              </span>
              <div className="rounded-2xl rounded-tl-sm bg-white/5 px-4 py-2.5 text-[15px] leading-relaxed text-white/90">
                {questionText(turn)}
              </div>
            </div>
            {turn.answer ? (
              <div className="flex justify-end">
                <div className="max-w-[85%] rounded-2xl rounded-tr-sm bg-accent/15 px-4 py-2.5 text-[15px] leading-relaxed text-white">
                  {turn.answer}
                </div>
              </div>
            ) : null}
          </div>
        ))}

        {currentQuestion && (
          <div className="flex items-start gap-2">
            <span className="mt-1 shrink-0 rounded-full bg-accent/15 p-1.5 text-accent">
              <SpeakerGlyph />
            </span>
            <div className="rounded-2xl rounded-tl-sm bg-white/5 px-4 py-2.5 text-[15px] leading-relaxed text-white/90">
              {currentQuestion}
              {questionStreaming && (
                <span className="ml-0.5 inline-block h-4 w-0.5 animate-pulse bg-accent align-middle" />
              )}
            </div>
          </div>
        )}

        {interimTranscript && (
          <div className="flex justify-end">
            <div className="max-w-[85%] rounded-2xl rounded-tr-sm bg-blue-500/15 px-4 py-2.5 text-[15px] italic leading-relaxed text-blue-100">
              {interimTranscript}
            </div>
          </div>
        )}

        {status && (
          <div className="flex items-center gap-2 text-sm text-white/70" role="status">
            <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" aria-hidden="true" />
            {status}
          </div>
        )}
      </div>

      <div className="mt-3 flex items-end gap-2">
        <textarea
          aria-label="Nhập câu trả lời"
          disabled={!canAnswer}
          readOnly={!canAnswer}
          rows={2}
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault()
              submit()
            }
          }}
          placeholder={
            aiSpeaking
              ? 'Nhà phỏng vấn đang nói…'
              : voiceState === VoiceInterviewState.USER_SPEAKING
                ? 'Đang nghe… bạn có thể nói hoặc gõ'
                : thinking
                  ? 'Đang chuẩn bị câu hỏi tiếp theo…'
                  : 'Nhập câu trả lời của bạn…'
          }
          className="min-h-[44px] flex-1 resize-none rounded-xl border border-white/10 bg-[#0f1117] px-3 py-2.5 text-sm text-white placeholder:text-white/35 focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent disabled:opacity-50"
        />
        <Button
          type="button"
          disabled={!canAnswer || !draft.trim()}
          onClick={submit}
          className={cn('h-[44px] shrink-0')}
        >
          <Send className="h-4 w-4" />
          Gửi
        </Button>
      </div>
    </div>
  )
}

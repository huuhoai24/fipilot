import React, { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import {
  Captions,
  CaptionsOff,
  MessageSquare,
  Mic,
  MicOff,
  User,
  Video,
  VideoOff,
} from 'lucide-react'
import { VoiceInterviewState } from '@/types'
import type { V2InterviewTurn } from '@/types'
import styles from './V1InterviewStage.module.css'

const V1_GREETING =
  'Xin chào, rất vui được gặp bạn. Rất hoan nghênh bạn đã tham gia buổi phỏng vấn. ' +
  'Tôi là người phỏng vấn AI của bạn ngày hôm nay. Chúng ta sẽ lần lượt trao đổi ' +
  'qua từng câu hỏi một.'

function questionText(turn?: V2InterviewTurn | null): string {
  if (!turn || !turn.question) return ''
  return typeof turn.question === 'string' ? turn.question : (turn.question.question || '')
}

function SpeakerGlyph() {
  return (
    <span className={styles.speakerGlyph} aria-hidden="true">
      <i />
      <i />
      <i />
      <i />
      <i />
      <i />
    </span>
  )
}

function V1Waveform({ active }: { active: boolean }) {
  const rays = Array.from({ length: 31 }, (_, index) => index)
  const contours = [0, 1, 2, 3, 4, 5]

  return (
    <svg
      className={`${styles.waveform} ${active ? styles.waveformActive : ''}`}
      viewBox="0 0 1440 190"
      preserveAspectRatio="none"
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="ai-wave-fade" x1="0" x2="1">
          <stop offset="0" stopColor="#77f8f0" stopOpacity=".16" />
          <stop offset=".5" stopColor="#a1fff9" stopOpacity=".75" />
          <stop offset="1" stopColor="#77f8f0" stopOpacity=".16" />
        </linearGradient>
      </defs>
      <g className={styles.waveRays}>
        {rays.map((ray) => {
          const x = ray * 48
          return <path key={ray} d={`M720 82 L${x} 190`} />
        })}
      </g>
      <g className={styles.waveContours}>
        {contours.map((contour) => {
          const y = 80 + contour * 18
          const arch = 20 + contour * 3
          return <path key={contour} d={`M0 ${y + 52} Q360 ${y - arch} 720 ${y} T1440 ${y + 52}`} />
        })}
      </g>
      <path
        className={styles.waveCrest}
        d="M0 126 C80 110 112 127 174 108 C232 91 287 112 351 93 C415 77 480 101 540 84 C606 64 649 91 708 73 C762 58 821 91 882 72 C945 58 1008 92 1062 79 C1125 65 1196 103 1262 91 C1324 82 1381 112 1440 104"
      />
    </svg>
  )
}

function V1SelfView({
  videoRef,
  active,
  name,
}: {
  videoRef: React.RefObject<HTMLVideoElement>
  active: boolean
  name?: string
}) {
  const internalRef = useRef<HTMLVideoElement>(null)
  // Use forwarded ref from parent if provided, otherwise internal
  const combinedRef = (videoRef as React.RefObject<HTMLVideoElement>) ?? internalRef

  return (
    <div className={styles.selfView} aria-label="Self view">
      <video
        ref={combinedRef}
        className={styles.selfViewVideo}
        autoPlay
        muted
        playsInline
        style={{ display: active ? 'block' : 'none' }}
      />
      {!active ? (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 12,
            textAlign: 'center',
            padding: 24,
            transform: 'scaleX(-1)',
          }}
        >
          <div
            style={{
              display: 'flex',
              height: 80,
              width: 80,
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: '9999px',
              border: '1px solid rgba(255,255,255,0.1)',
              background: 'rgba(255,255,255,0.08)',
              color: 'rgba(255,255,255,0.8)',
            }}
          >
            <User style={{ width: 40, height: 40 }} />
          </div>
          <span style={{ fontSize: 14, fontWeight: 600, color: 'rgba(255,255,255,0.9)' }}>
            {name || 'Ứng viên'}
          </span>
          <span style={{ fontSize: 12, color: 'rgba(255,255,255,0.4)' }}>Camera đã tắt</span>
        </div>
      ) : null}
      {!active ? <div className={styles.selfViewGlow} aria-hidden="true" /> : null}
      {active ? <div className={styles.selfViewGlow} aria-hidden="true" style={{ opacity: 0.15 }} /> : null}
      <div className={styles.signalBadge} aria-label="Strong connection">
        <i />
        <i />
        <i />
        <i />
      </div>
      {active ? (
        <div
          style={{
            position: 'absolute',
            bottom: 8,
            left: 8,
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            borderRadius: 8,
            border: '1px solid rgba(255,255,255,0.12)',
            background: 'rgba(0,0,0,0.72)',
            padding: '4px 8px',
            transform: 'scaleX(-1)',
          }}
        >
          <span style={{ width: 6, height: 6, borderRadius: 999, background: '#20d761' }} />
          <span style={{ fontSize: 10, fontWeight: 600, color: '#fff', letterSpacing: 0.3 }}>Trực tiếp</span>
        </div>
      ) : null}
    </div>
  )
}

interface V1TranscriptProps {
  completedTurns: V2InterviewTurn[]
  currentQuestion: string
  greetingComplete: boolean
  questionStreaming: boolean
  interimTranscript: string
  onGreetingComplete: () => void
  voiceState: VoiceInterviewState
}

function V1Greeting({ complete, onComplete }: { complete: boolean; onComplete: () => void }) {
  const [visibleText, setVisibleText] = useState('')
  const completedRef = useRef(false)

  useEffect(() => {
    const audio = new Audio('/audio/interview-greeting.wav')
    audio.preload = 'auto'
    audio.volume = 1
    let animationFrame: number | null = null
    let typewriterTimer: number | null = null
    let completionTimer: number | null = null
    let visibleCharacterCount = 0
    let audioStarted = false

    const setVisibleCharacterCount = (count: number) => {
      const nextCount = Math.max(
        visibleCharacterCount,
        Math.max(0, Math.min(V1_GREETING.length, count)),
      )
      if (nextCount === visibleCharacterCount) return
      visibleCharacterCount = nextCount
      setVisibleText(V1_GREETING.slice(0, nextCount))
    }
    const syncTextToAudio = () => {
      if (!Number.isFinite(audio.duration) || audio.duration <= 0) return
      const progress = Math.min(1, audio.currentTime / audio.duration)
      setVisibleCharacterCount(Math.floor(progress * V1_GREETING.length))
      if (!audio.ended) animationFrame = requestAnimationFrame(syncTextToAudio)
    }

    const complete = () => {
      if (completedRef.current) return
      completedRef.current = true
      setVisibleCharacterCount(V1_GREETING.length)
      // Let the completed greeting remain readable before moving to question one.
      completionTimer = window.setTimeout(onComplete, 900)
    }
    const startTypewriter = () => {
      if (typewriterTimer !== null) return
      let index = 0
      typewriterTimer = window.setInterval(() => {
        index += 1
        setVisibleCharacterCount(index)
        if (index >= V1_GREETING.length) {
          if (typewriterTimer !== null) window.clearInterval(typewriterTimer)
          typewriterTimer = null
          if (!audioStarted) complete()
        }
      }, 40)
    }
    const play = () => {
      if (
        !audioStarted
        && visibleCharacterCount > 0
        && Number.isFinite(audio.duration)
        && audio.duration > 0
      ) {
        audio.currentTime = (visibleCharacterCount / V1_GREETING.length) * audio.duration
      }
      void audio.play().catch(startTypewriter)
    }
    const replayFromUserGesture = () => {
      if (completedRef.current) return
      play()
    }

    const handlePlaying = () => {
      audioStarted = true
      if (typewriterTimer !== null) window.clearInterval(typewriterTimer)
      typewriterTimer = null
      if (animationFrame !== null) cancelAnimationFrame(animationFrame)
      syncTextToAudio()
    }
    audio.addEventListener('playing', handlePlaying)
    audio.addEventListener('ended', complete)
    audio.addEventListener('error', complete)
    document.addEventListener('pointerdown', replayFromUserGesture, { once: true })
    document.addEventListener('keydown', replayFromUserGesture, { once: true })
    startTypewriter()
    play()

    return () => {
      if (animationFrame !== null) cancelAnimationFrame(animationFrame)
      if (typewriterTimer !== null) window.clearInterval(typewriterTimer)
      if (completionTimer !== null) window.clearTimeout(completionTimer)
      audio.pause()
      audio.removeEventListener('playing', handlePlaying)
      audio.removeEventListener('ended', complete)
      audio.removeEventListener('error', complete)
      document.removeEventListener('pointerdown', replayFromUserGesture)
      document.removeEventListener('keydown', replayFromUserGesture)
    }
  }, [onComplete])

  return (
    <div className={`${styles.transcriptMessage} ${complete ? styles.olderMessage : styles.currentMessage}`}>
      <SpeakerGlyph />
      <p>{visibleText}</p>
    </div>
  )
}

function listeningStatusText(voiceState: VoiceInterviewState): string | null {
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

function V1ChatComposer({
  open,
  canAnswer,
  interimTranscript,
  onSendText,
}: {
  open: boolean
  canAnswer: boolean
  interimTranscript: string
  onSendText: (text: string) => void
}) {
  const [draft, setDraft] = useState('')
  useEffect(() => {
    if (open) setDraft(interimTranscript)
  }, [interimTranscript, open])

  if (!open || typeof document === 'undefined') return null

  const submitFromDraft = (value?: string) => {
    const text = (value ?? draft).trim()
    if (!text || !canAnswer) return
    onSendText(text)
    setDraft('')
  }

  return createPortal(
    <form
      className={styles.chatComposer}
      onSubmit={(event) => {
        event.preventDefault()
        submitFromDraft()
      }}
    >
      <textarea
        aria-label="Nhập câu trả lời"
        autoFocus
        disabled={!canAnswer}
        readOnly={!canAnswer}
        onChange={(event) => setDraft(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault()
            submitFromDraft()
          }
        }}
        placeholder={
          !canAnswer
            ? 'Đang chuẩn bị câu hỏi tiếp theo...'
            : 'Nhập câu trả lời của bạn...'
        }
        rows={3}
        value={draft}
      />
      <span>Enter để gửi · Shift + Enter để xuống dòng</span>
    </form>,
    document.body,
  )
}

function V1Transcript({
  completedTurns,
  currentQuestion,
  greetingComplete,
  questionStreaming,
  interimTranscript,
  onGreetingComplete,
  voiceState,
}: V1TranscriptProps) {
  const statusText = listeningStatusText(voiceState)
  const thinking = voiceState === VoiceInterviewState.AI_THINKING
  // Keep the same two-message stack as v1: the preceding reply and the current question.
  const allMessages: Array<{ id: string; text: string; isQuestion: boolean; isCurrent: boolean }> = []

  // Add completed turns (each as Q)
  completedTurns.forEach((turn, idx) => {
    const q = questionText(turn)
    if (q) {
      allMessages.push({ id: turn.turn_id || `q-${idx}`, text: q, isQuestion: true, isCurrent: false })
    }
    const answerText = turn.candidate_answer || turn.answer
    if (answerText) {
      allMessages.push({ id: `${turn.turn_id}-a`, text: answerText, isQuestion: false, isCurrent: false })
    }
  })

  // Add current question as last
  if (currentQuestion) {
    allMessages.push({ id: 'current-q', text: currentQuestion, isQuestion: true, isCurrent: true })
  }

  const showGreetingAsPrevious =
    greetingComplete && completedTurns.length === 0 && allMessages.length > 0
  const displayMessages = showGreetingAsPrevious
    ? allMessages.slice(-1)
    : allMessages.slice(-2)

  return (
    <>
      <div className={styles.transcript} aria-live="polite">
        <div className={styles.transcriptStack}>
          {!import.meta.env.VITEST ? (
            <V1Greeting complete={greetingComplete} onComplete={onGreetingComplete} />
          ) : null}
          {greetingComplete && displayMessages.length === 0 && import.meta.env.VITEST ? (
            <div className={styles.transcriptMessage}>
              <SpeakerGlyph />
              <p style={{ color: '#9091a8', fontStyle: 'italic' }}>Nhà phỏng vấn sẽ sớm bắt đầu nói.</p>
            </div>
          ) : null}
          {greetingComplete && displayMessages.map((msg, index) => {
            const isCurrent = index === displayMessages.length - 1 && msg.isCurrent && msg.isQuestion
            const isOlder = !isCurrent && index < displayMessages.length - 1
            return (
              <div
                key={msg.id}
                className={`${styles.transcriptMessage} ${isCurrent ? styles.currentMessage : ''} ${isOlder ? styles.olderMessage : ''}`}
              >
                {msg.isQuestion ? <SpeakerGlyph /> : null}
                <p>
                  {msg.text}
                  {isCurrent && questionStreaming ? (
                    <span
                      style={{
                        display: 'inline-block',
                        width: 2,
                        height: 14,
                        marginLeft: 2,
                        background: '#20d761',
                        verticalAlign: 'middle',
                        animation: 'pulse 1s infinite',
                      }}
                      aria-hidden="true"
                    />
                  ) : null}
                </p>
              </div>
            )
          })}
        </div>

        {interimTranscript ? (
          <div style={{ marginTop: 12, display: 'flex', justifyContent: 'flex-end' }}>
            <div
              style={{
                maxWidth: '85%',
                borderRadius: '16px 16px 4px 16px',
                background: 'rgba(59,130,246,0.15)',
                padding: '10px 14px',
                fontSize: 14,
                fontStyle: 'italic',
                color: '#bfdbfe',
                textAlign: 'left',
              }}
            >
              {interimTranscript}
            </div>
          </div>
        ) : null}

        {statusText ? (
          <div className={styles.listeningStatus} role="status">
            <span aria-hidden="true" />
            {statusText}
          </div>
        ) : null}
        {thinking && !statusText ? (
          <div className={styles.listeningStatus} role="status">
            <span aria-hidden="true" />
            Đang chuẩn bị câu hỏi tiếp theo...
          </div>
        ) : null}
      </div>
    </>
  )
}

interface V1InterviewStageProps {
  session: import('@/types').V2InterviewSessionState
  voiceState: VoiceInterviewState
  isConnected: boolean
  isComplete: boolean
  speaking: boolean
  transcript: string
  currentQuestionText: string
  greetingComplete: boolean
  questionStreaming: boolean
  captionsActive: boolean
  cameraActive: boolean
  chatActive: boolean
  microphoneActive: boolean
  videoRef: React.RefObject<HTMLVideoElement>
  onSendText: (text: string) => void
  onGreetingComplete: () => void
  onToggleMicrophone: () => void
  onToggleCamera: () => void
  onToggleCaptions: () => void
  onToggleChat: () => void
}

export function V1InterviewStage({
  session,
  voiceState,
  speaking,
  transcript,
  currentQuestionText,
  greetingComplete,
  questionStreaming,
  captionsActive,
  cameraActive,
  chatActive,
  microphoneActive,
  videoRef,
  onSendText,
  onGreetingComplete,
  onToggleMicrophone,
  onToggleCamera,
  onToggleCaptions,
  onToggleChat,
}: V1InterviewStageProps) {
  const transcriptVisible = captionsActive
  const onlyTranscript = transcriptVisible && !cameraActive
  const onlyCamera = cameraActive && !transcriptVisible
  // Let candidates draft while the interviewer is still reading the question.
  // The answer remains locked only once the current turn is being processed.
  const canAnswer =
    voiceState !== VoiceInterviewState.AI_THINKING &&
    voiceState !== VoiceInterviewState.TRANSCRIBING &&
    voiceState !== VoiceInterviewState.EVALUATING

  const currentQuestion =
    !greetingComplete
      ? ''
      : questionStreaming
        ? currentQuestionText
        : currentQuestionText || questionText(session.current_turn)

  return (
    <div className={styles.stage}>
      <V1Waveform active={speaking} />
      <div
        className={`${styles.conversation} ${onlyTranscript ? styles.onlyTranscript : ''} ${onlyCamera ? styles.onlyCamera : ''}`}
      >
        {transcriptVisible ? (
          <V1Transcript
            completedTurns={session.completed_turns}
            currentQuestion={currentQuestion}
            greetingComplete={greetingComplete}
            questionStreaming={questionStreaming}
            interimTranscript={transcript}
            onGreetingComplete={onGreetingComplete}
            voiceState={voiceState}
          />
        ) : null}
        {cameraActive || true ? (
          // Always render selfView if transcriptVisible false it will be centered via onlyCamera
          // If camera off, show placeholder (handled inside)
          <V1SelfView videoRef={videoRef} active={cameraActive} name={session.candidate_profile?.name || 'Ứng viên'} />
        ) : null}
      </div>

      {/* Media tray - exact v1 MediaControls inside stage */}
      <div className={styles.mediaTray} role="toolbar" aria-label="Điều khiển phỏng vấn">
        <button
          className={`${styles.mediaButton} ${!microphoneActive ? styles.mediaButtonDisabled : ''}`}
          type="button"
          onClick={onToggleMicrophone}
          aria-label={microphoneActive ? 'Tắt microphone' : 'Bật microphone'}
          title={microphoneActive ? 'Tắt microphone' : 'Bật microphone'}
          aria-pressed={!microphoneActive}
        >
          {microphoneActive ? <Mic aria-hidden="true" /> : <MicOff aria-hidden="true" />}
        </button>
        <button
          className={`${styles.mediaButton} ${!cameraActive ? styles.mediaButtonDisabled : ''}`}
          type="button"
          onClick={onToggleCamera}
          aria-label={cameraActive ? 'Tắt camera' : 'Bật camera'}
          title={cameraActive ? 'Tắt camera' : 'Bật camera'}
          aria-pressed={!cameraActive}
        >
          {cameraActive ? <Video aria-hidden="true" /> : <VideoOff aria-hidden="true" />}
        </button>
        <button
          className={`${styles.mediaButton} ${styles.transcriptButton} ${!captionsActive ? styles.mediaButtonDisabled : ''}`}
          type="button"
          onClick={onToggleCaptions}
          aria-label={captionsActive ? 'Ẩn phụ đề' : 'Hiện phụ đề'}
          title={captionsActive ? 'Ẩn phụ đề' : 'Hiện phụ đề'}
          aria-pressed={!captionsActive}
        >
          {captionsActive ? <Captions aria-hidden="true" /> : <CaptionsOff aria-hidden="true" />}
        </button>
        <button
          className={`${styles.mediaButton} ${styles.chatButton} ${chatActive ? styles.mediaButtonActive : ''}`}
          type="button"
          onClick={onToggleChat}
          aria-label={chatActive ? 'Đóng trả lời văn bản' : 'Trả lời bằng văn bản'}
          title={chatActive ? 'Đóng trả lời văn bản' : 'Trả lời bằng văn bản'}
          aria-pressed={chatActive}
        >
          <MessageSquare aria-hidden="true" />
        </button>
      </div>

      {/* v1: chatComposer via portal to body, independent of captions */}
      <V1ChatComposer
        open={chatActive}
        canAnswer={canAnswer}
        interimTranscript={transcript}
        onSendText={onSendText}
      />
    </div>
  )
}

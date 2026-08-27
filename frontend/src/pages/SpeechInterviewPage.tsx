import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  AlertCircle,
  ArrowLeft,
  CheckCircle2,
  FileText,
  History,
  Loader2,
  RefreshCw,
} from 'lucide-react'
import { EndInterviewConfirmModal } from '@/components/voice/EndInterviewConfirmModal'
import { V1InterviewStage } from '@/components/interview/V1InterviewStage'

import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { firebaseAuth } from '@/lib/firebase'
import { api } from '@/lib/api'
import { getUserFacingError } from '@/lib/userFacingError'
import type {
  InterviewReport,
  V2InterviewSessionResponse,
  V2InterviewSessionState,
  V2InterviewTurn,
} from '@/types'
import { VoiceInterviewState } from '@/types'

const V1_SPEECH_API_BASE_URL = (
  import.meta.env.VITE_V1_SPEECH_API_BASE_URL || 'http://localhost:8000'
).replace(/\/$/, '')

async function legacySpeechHeaders(init?: HeadersInit): Promise<Headers> {
  const headers = new Headers(init)
  const user = firebaseAuth?.currentUser
  if (user) headers.set('Authorization', `Bearer ${await user.getIdToken()}`)
  return headers
}

type VoiceConnectionState = 'connecting' | 'connected' | 'disconnected' | 'error'
type FinalReportState = 'idle' | 'loading' | 'ready' | 'error'
type MicrophonePermissionState =
  | 'unknown'
  | 'requesting'
  | 'granted'
  | 'denied'
  | 'unavailable'

export function canStartOpeningQuestion(
  greetingComplete: boolean,
  alreadyRequested: boolean,
): boolean {
  return greetingComplete && !alreadyRequested
}

function questionText(turn?: V2InterviewTurn | null): string {
  if (!turn || !turn.question) return ''
  return typeof turn.question === 'string' ? turn.question : (turn.question.question || '')
}

function stopMediaStream(stream: MediaStream | null) {
  stream?.getTracks().forEach((track) => track.stop())
}

function microphoneErrorMessage(error: unknown): string {
  if (error instanceof DOMException && (
    error.name === 'NotAllowedError'
    || error.name === 'PermissionDeniedError'
  )) {
    return 'Quyền microphone đã bị từ chối. Hãy cho phép truy cập trong cài đặt trình duyệt và thử lại.'
  }
  if (error instanceof DOMException && error.name === 'NotFoundError') {
    return 'No microphone was found. Connect a microphone and try again.'
  }
  return 'Không thể mở microphone. Hãy kiểm tra trình duyệt và cài đặt thiết bị của bạn.'
}

function microphonePermissionAfterError(error: unknown): MicrophonePermissionState {
  if (error instanceof DOMException && (
    error.name === 'NotAllowedError'
    || error.name === 'PermissionDeniedError'
  )) {
    return 'denied'
  }
  return 'unavailable'
}

export function SpeechInterviewPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const sessionRef = useRef<V2InterviewSessionState | null>(null)
  const transcriptRef = useRef('')
  const hasConnectedRef = useRef(false)
  
  const mediaStreamRef = useRef<MediaStream | null>(null)
  const recordingStartPendingRef = useRef(false)
  const recordingGenerationRef = useRef(0)
  const activeRecordingGenerationRef = useRef<number | null>(null)
  const recordingStopPendingRef = useRef<number | null>(null)
  const stoppedRecordingGenerationRef = useRef<number | null>(null)
  
  const turnProcessingStartedAtRef = useRef<number | null>(null)
  const turnLatencyRecordedRef = useRef(false)
  const [session, setSession] = useState<V2InterviewSessionState | null>(null)
  const [voiceState, setVoiceState] = useState(VoiceInterviewState.IDLE)
  const [connectionState, setConnectionState] = useState<VoiceConnectionState>('connecting')
  const [elapsedSeconds, setElapsedSeconds] = useState(0)
  const [transcript, setTranscript] = useState('')
  const [currentQuestionText, setCurrentQuestionText] = useState('')
  const [questionStreaming, setQuestionStreaming] = useState(false)
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState('')
  const [microphoneError, setMicrophoneError] = useState('')
  const [microphonePermission, setMicrophonePermission] =
    useState<MicrophonePermissionState>('unknown')
  const [localTurnLatencyMs, setLocalTurnLatencyMs] = useState<number | null>(null)
  const [transportError, setTransportError] = useState('')
  const [audioWarning, setAudioWarning] = useState('')
  const [finalReport, setFinalReport] = useState<InterviewReport | null>(null)
  const [finalReportState, setFinalReportState] = useState<FinalReportState>('idle')
  const [finalReportError, setFinalReportError] = useState('')
  const [finalReportRetry, setFinalReportRetry] = useState(0)
  const [cameraActive, setCameraActive] = useState(false)
  const [captionsActive, setCaptionsActive] = useState(true)
  const [chatActive, setChatActive] = useState(false)
  const [greetingComplete, setGreetingComplete] = useState(import.meta.env.VITEST)
  const [endModalOpen, setEndModalOpen] = useState(false)
  const greetingCompleteRef = useRef(import.meta.env.VITEST)
  const openingQuestionRequestedRef = useRef(false)
  const cameraStreamRef = useRef<MediaStream | null>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const interviewComplete = session !== null && session.current_turn === null

  const requestOpeningQuestion = useCallback(() => {
    if (!canStartOpeningQuestion(
      greetingCompleteRef.current,
      openingQuestionRequestedRef.current,
    )) return
    openingQuestionRequestedRef.current = true
    const currentQuestion = questionText(sessionRef.current?.current_turn)
    if (currentQuestion) {
      void speakQuestionSmoothly(currentQuestion)
    }
  }, [])

  const handleGreetingComplete = useCallback(() => {
    if (greetingCompleteRef.current) return
    greetingCompleteRef.current = true
    setGreetingComplete(true)
    requestOpeningQuestion()
  }, [requestOpeningQuestion])

  const formattedTimer = useMemo(() => {
    const totalSeconds = (session?.interview_config?.duration_minutes || 30) * 60
    const remaining = Math.max(0, totalSeconds - elapsedSeconds)
    const mins = Math.floor(remaining / 60)
    const secs = remaining % 60
    return `${mins}:${secs < 10 ? '0' : ''}${secs} mins`
  }, [session?.interview_config?.duration_minutes, elapsedSeconds])

  useEffect(() => {
    let mounted = true
    if (!import.meta.env.VITEST && typeof navigator !== 'undefined' && navigator.mediaDevices?.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          if (!mounted) {
            stream.getTracks().forEach((t) => t.stop())
            return
          }
          cameraStreamRef.current = stream
          setCameraActive(true)
          if (videoRef.current) {
            videoRef.current.srcObject = stream
            try {
              void videoRef.current.play()?.catch(() => undefined)
            } catch {}
          }
        })
        .catch(() => {
          setCameraActive(false)
        })
    }
    return () => {
      mounted = false
      if (cameraStreamRef.current) {
        cameraStreamRef.current.getTracks().forEach((t) => t.stop())
        cameraStreamRef.current = null
      }
    }
  }, [])

  useEffect(() => {
    if (cameraActive && cameraStreamRef.current && videoRef.current) {
      videoRef.current.srcObject = cameraStreamRef.current
      try {
        void videoRef.current.play()?.catch(() => undefined)
      } catch {}
    }
  }, [cameraActive])

  const currentAudioRef = useRef<HTMLAudioElement | null>(null)
  const animFrameRef = useRef<number | null>(null)
  const lastSpokenQuestionRef = useRef<string>('')
  const nativeRecorderRef = useRef<MediaRecorder | null>(null)

  const ttsGenerationRef = useRef(0)

  async function speakQuestionSmoothly(text: string) {
    if (!text || lastSpokenQuestionRef.current === text) return
    lastSpokenQuestionRef.current = text
    const currentGeneration = ++ttsGenerationRef.current

    if (currentAudioRef.current) {
      currentAudioRef.current.pause()
      currentAudioRef.current = null
    }
    if (animFrameRef.current) {
      cancelAnimationFrame(animFrameRef.current)
    }
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel()
    }

    try {
      setVoiceState(VoiceInterviewState.AI_SPEAKING)
      setCurrentQuestionText('')
      setQuestionStreaming(true)

      const res = await fetch(`${V1_SPEECH_API_BASE_URL}/api/v1/speech`, {
        method: 'POST',
        headers: await legacySpeechHeaders({ 'Content-Type': 'application/json' }),
        body: JSON.stringify({ text }),
      })

      if (ttsGenerationRef.current !== currentGeneration) return

      if (res.ok) {
        const blob = await res.blob()
        if (ttsGenerationRef.current !== currentGeneration) return
        
        const audioUrl = URL.createObjectURL(blob)
        const audio = new Audio(audioUrl)
        
        if (currentAudioRef.current) {
          currentAudioRef.current.pause()
        }
        currentAudioRef.current = audio
        audio.preload = 'auto'

        const syncText = () => {
          if (!audio || audio.paused) return
          if (!Number.isFinite(audio.duration) || audio.duration <= 0) {
            setCurrentQuestionText(text)
            return
          }
          const progress = Math.min(1, audio.currentTime / audio.duration)
          const charIndex = Math.max(1, Math.floor(progress * text.length))
          setCurrentQuestionText(text.slice(0, charIndex))
          if (!audio.ended) {
            animFrameRef.current = requestAnimationFrame(syncText)
          } else {
            setCurrentQuestionText(text)
          }
        }

        audio.onplaying = () => {
          setVoiceState(VoiceInterviewState.AI_SPEAKING)
          syncText()
        }

        audio.onended = () => {
          setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
          setCurrentQuestionText(text)
          setQuestionStreaming(false)
          URL.revokeObjectURL(audioUrl)
          if (currentAudioRef.current === audio) currentAudioRef.current = null
          if (!import.meta.env.VITEST) {
            void startListening()
          }
        }

        await audio.play().catch(() => {
          setCurrentQuestionText(text)
          setQuestionStreaming(false)
          setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
        })
        return
      }
    } catch {}

    if (ttsGenerationRef.current !== currentGeneration) return

    setCurrentQuestionText(text)
    setQuestionStreaming(false)
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'vi-VN'
      utterance.onstart = () => setVoiceState(VoiceInterviewState.AI_SPEAKING)
      utterance.onend = () => {
        setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
        if (!import.meta.env.VITEST) {
          void startListening()
        }
      }
      window.speechSynthesis.speak(utterance)
    } else {
      setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
    }
  }

  async function submitCandidateAnswer(answerText: string) {
    if (!answerText || !sessionId || !session?.current_turn) return
    const turnId = session.current_turn.turn_id
    setVoiceState(VoiceInterviewState.EVALUATING)
    try {
      const updated = await api.submitV2InterviewAnswer(sessionId, turnId, answerText)
      setSession(updated)
      sessionRef.current = updated
      const nextQuestion = questionText(updated.current_turn)
      if (nextQuestion) {
        void speakQuestionSmoothly(nextQuestion)
      } else {
        setVoiceState(VoiceInterviewState.IDLE)
        setCurrentQuestionText('')
        setQuestionStreaming(false)
        setTranscript('')
      }
    } catch (error) {
      setTransportError(getUserFacingError(error, 'Không thể gửi câu trả lời.'))
      setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
    }
  }

  const toggleCamera = async () => {
    if (cameraActive) {
      if (cameraStreamRef.current) {
        cameraStreamRef.current.getTracks().forEach((t) => t.stop())
        cameraStreamRef.current = null
      }
      if (videoRef.current) {
        videoRef.current.srcObject = null
      }
      setCameraActive(false)
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true })
        cameraStreamRef.current = stream
        setCameraActive(true)
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          try {
            void videoRef.current.play()?.catch(() => undefined)
          } catch {}
        }
      } catch {
        setCameraActive(false)
      }
    }
  }

  useEffect(() => {
    if (!interviewComplete || !sessionId) return
    let cancelled = false
    setFinalReportState('loading')
    setFinalReportError('')
    void api.generateInterviewReport(sessionId)
      .then((response) => {
        if (cancelled) return
        setFinalReport(response.report)
        setFinalReportState('ready')
      })
      .catch((error) => {
        if (cancelled) return
        setFinalReportError(getUserFacingError(error, 'Final scores could not be generated. Please try again.'))
        setFinalReportState('error')
      })
    return () => {
      cancelled = true
    }
  }, [finalReportRetry, interviewComplete, sessionId])

  const releaseMedia = () => {
    recordingStartPendingRef.current = false
    activeRecordingGenerationRef.current = null
    stopMediaStream(mediaStreamRef.current)
    mediaStreamRef.current = null
  }

  useEffect(() => {
    return () => {
      releaseMedia()
      if (cameraStreamRef.current) {
        stopMediaStream(cameraStreamRef.current)
        cameraStreamRef.current = null
      }
      if (currentAudioRef.current) {
        currentAudioRef.current.pause()
        currentAudioRef.current = null
      }
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current)
      }
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel()
      }
    }
  }, [])

  useEffect(() => {
    sessionRef.current = session
  }, [session])

  useEffect(() => {
    transcriptRef.current = transcript
  }, [transcript])

  useEffect(() => {
    hasConnectedRef.current = false
  }, [sessionId])

  useEffect(() => {
    if (!sessionId) {
      setLoadError('Interview session ID is missing.')
      setLoading(false)
      return
    }

    let cancelled = false
    setLoading(true)
    setLoadError('')
    setSession(null)
    setFinalReport(null)
    setFinalReportState('idle')
    setFinalReportError('')
    api.getV2InterviewSession(sessionId)
      .then((response: V2InterviewSessionResponse) => {
        if (!cancelled) {
           setSession(response.state)
           sessionRef.current = response.state
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setLoadError(getUserFacingError(error, 'The interview session could not be loaded. Please try again.'))
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [sessionId])

  useEffect(() => {
    if (!sessionId || session?.interview_config.mode !== 'voice') return

    setConnectionState('connected')
    setTransportError('')
    setAudioWarning('')

    if (!hasConnectedRef.current) {
      hasConnectedRef.current = true
      requestOpeningQuestion()
    }
    
    return () => {}
  }, [session?.interview_config.mode, sessionId])

  useEffect(() => {
    if (voiceState !== VoiceInterviewState.USER_SPEAKING) return
    const timer = window.setInterval(() => {
      setElapsedSeconds((seconds) => seconds + 1)
    }, 1000)
    return () => window.clearInterval(timer)
  }, [voiceState])

  const progress = useMemo(() => {
    if (!session) return { current: 0, total: 0, percentage: 0 }
    const total = session.interview_config.question_count
    const current = Math.min(
      total,
      session.completed_turns.length + (session.current_turn ? 1 : 0)
    )
    return {
      current,
      total,
      percentage: total ? Math.round((current / total) * 100) : 0,
    }
  }, [session])

  async function startAudioCapture(
    controlType: 'start_listening' | 'start_barge_in',
    resetAnswer = true,
  ) {
    if (
      recordingStartPendingRef.current
      || nativeRecorderRef.current?.state === 'recording'
    ) return
    // A failed recorder setup used to leave a stopped stream in this ref.
    // That made every later click on MicOff return silently.
    if (mediaStreamRef.current) {
      stopMediaStream(mediaStreamRef.current)
      mediaStreamRef.current = null
    }
    setMicrophoneError('')
    setTransportError('')
    
    if (!navigator.mediaDevices?.getUserMedia) {
      setMicrophonePermission('unavailable')
      setMicrophoneError('This browser does not support streaming microphone capture.')
      return
    }

    recordingStartPendingRef.current = true
    let stream: MediaStream | null = null

    try {
      setMicrophonePermission('requesting')
      stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      })
      setMicrophonePermission('granted')

      stopMediaStream(mediaStreamRef.current)
      mediaStreamRef.current = stream

      if (typeof MediaRecorder !== 'undefined') {
        const chunks: Blob[] = []
        const recorder = new MediaRecorder(stream)
        nativeRecorderRef.current = recorder
        const vadContext = new AudioContext()
        const vadSource = vadContext.createMediaStreamSource(stream)
        const analyser = vadContext.createAnalyser()
        const samples = new Uint8Array(analyser.fftSize)
        let vadFrame: number | undefined
        let heardSpeech = false
        let lastSpeechAt = performance.now()
        const recordingStartedAt = performance.now()

        vadSource.connect(analyser)
        if (vadContext.state === 'suspended') void vadContext.resume()

        recorder.ondataavailable = (e) => {
          if (e.data.size > 0) chunks.push(e.data)
        }

        recorder.onstop = async () => {
          if (vadFrame !== undefined) cancelAnimationFrame(vadFrame)
          vadSource.disconnect()
          void vadContext.close()
          nativeRecorderRef.current = null

          const blob = new Blob(chunks, { type: recorder.mimeType || 'audio/webm' })
          if (blob.size > 0) {
            setVoiceState(VoiceInterviewState.TRANSCRIBING)
            try {
              const formData = new FormData()
              formData.append('audio', blob, 'answer.webm')
              const res = await fetch(`${V1_SPEECH_API_BASE_URL}/api/v1/speech/recognize`, {
                method: 'POST',
                headers: await legacySpeechHeaders(),
                body: formData,
              })
              const data = await res.json().catch(() => null)
              if (res.ok && data?.text) {
                setTranscript(data.text)
                void submitCandidateAnswer(data.text)
              } else {
                setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
                setMicrophoneError(data?.detail || 'Không thể nhận diện giọng nói. Hãy nói rõ hơn hoặc thử lại.')
              }
            } catch {
              setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
              setMicrophoneError('Lỗi kết nối. Không thể nhận diện giọng nói.')
            }
          }
        }

        recorder.start(250)

        const monitorSilence = () => {
          if (recorder.state !== 'recording') return
          analyser.getByteTimeDomainData(samples)
          let signalEnergy = 0
          for (const sample of samples) {
            const normalized = (sample - 128) / 128
            signalEnergy += normalized * normalized
          }
          const volume = Math.sqrt(signalEnergy / samples.length)
          const now = performance.now()
          if (volume > 0.018) {
            heardSpeech = true
            lastSpeechAt = now
          }
          const finishedSpeaking = heardSpeech && now - lastSpeechAt > 3500
          const maxReached = now - recordingStartedAt > 90000
          if (finishedSpeaking || maxReached) {
            if (recorder.state === 'recording') {
              recorder.stop()
            }
            void stopListening()
            return
          }
          vadFrame = requestAnimationFrame(monitorSilence)
        }
        vadFrame = requestAnimationFrame(monitorSilence)
        setVoiceState(VoiceInterviewState.USER_SPEAKING)
      } else {
        stopMediaStream(stream)
        if (mediaStreamRef.current === stream) {
          mediaStreamRef.current = null
        }
        setMicrophonePermission('unavailable')
        setMicrophoneError('MediaRecorder is not supported in this browser.')
      }

      recordingStartPendingRef.current = false
    } catch (error) {
      recordingStartPendingRef.current = false
      setMicrophonePermission(microphonePermissionAfterError(error))
      setMicrophoneError(microphoneErrorMessage(error))
      if (stream) stopMediaStream(stream)
      if (mediaStreamRef.current === stream) {
        mediaStreamRef.current = null
      }
    }
  }

  function startListening() {
    turnProcessingStartedAtRef.current = null
    turnLatencyRecordedRef.current = false
    setLocalTurnLatencyMs(null)
    void startAudioCapture('start_listening')
  }

  async function stopListening() {
    if (nativeRecorderRef.current && nativeRecorderRef.current.state === 'recording') {
      nativeRecorderRef.current.stop()
    }
    setVoiceState(VoiceInterviewState.TRANSCRIBING)
    if (mediaStreamRef.current) {
      stopMediaStream(mediaStreamRef.current)
      mediaStreamRef.current = null
    }
  }

  const retryConnection = () => {
    setTransportError('')
    setConnectionState('connecting')
  }

  if (loading) {
    return (
      <div className="flex min-h-[65vh] items-center justify-center" role="status">
        <Loader2 className="h-7 w-7 animate-spin text-accent" />
        <span className="sr-only">Loading speech interview</span>
      </div>
    )
  }

  if (loadError || !session) {
    return (
      <div className="mx-auto max-w-xl rounded-lg border border-danger/30 bg-danger/10 p-5">
        <div className="flex items-start gap-3">
          <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-danger" />
          <div>
            <h1 className="text-sm font-semibold text-text-primary">Speech interview unavailable</h1>
            <p className="mt-1 text-sm text-danger">{loadError || 'The interview session could not be loaded.'}</p>
            <Button className="mt-4" variant="secondary" onClick={() => navigate('/text-interview')}>
              <ArrowLeft className="h-4 w-4" />
              Back to setup
            </Button>
          </div>
        </div>
      </div>
    )
  }

  if (session.interview_config.mode !== 'voice') {
    return (
      <div className="mx-auto max-w-xl rounded-lg border border-warning/30 bg-warning/10 p-5">
        <div className="flex items-start gap-3">
          <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-warning" />
          <div>
            <h1 className="text-sm font-semibold text-text-primary">This is a Text Interview session</h1>
            <p className="mt-1 text-sm text-text-muted">Open it in the text interview room to continue.</p>
            <Button
              className="mt-4"
              variant="secondary"
              onClick={() => navigate(`/text-interview/${sessionId}`, { replace: true })}
            >
              Open Text Interview
            </Button>
          </div>
        </div>
      </div>
    )
  }

  const isComplete = !session.current_turn
  const isConnected = connectionState === 'connected'
  const speaking = voiceState === VoiceInterviewState.AI_SPEAKING
    || voiceState === VoiceInterviewState.USER_SPEAKING
  const microphoneActionable = isConnected
    && !isComplete
    && microphonePermission !== 'requesting'
    && (
      voiceState === VoiceInterviewState.WAITING_FOR_USER
      || voiceState === VoiceInterviewState.USER_SPEAKING
    )
  const waveformLabel = voiceState === VoiceInterviewState.USER_SPEAKING
    ? 'Your speaking waveform'
    : voiceState === VoiceInterviewState.AI_SPEAKING
      ? 'AI speaking waveform'
      : 'Inactive voice waveform'
  const microphonePermissionLabel = {
    unknown: 'Đang chờ quyền microphone',
    requesting: 'Đang yêu cầu quyền microphone',
    granted: 'Đã cấp quyền microphone',
    denied: 'Đã từ chối quyền microphone',
    unavailable: 'Microphone không khả dụng',
  }[microphonePermission]

  return (
    <div className="fixed inset-0 z-40 flex flex-col bg-[#000000] text-white overflow-hidden font-sans">
      {/* Top Header Bar (Matching Image 5) */}
      <header className="relative z-20 flex h-[52px] w-full items-center justify-between border-b border-white/10 bg-[#121418] px-4 sm:px-6">
        <div className="flex items-center gap-3">
          <span className="font-bold text-white tracking-tight text-base">FiPilot</span>
          <span className="h-3.5 w-px bg-white/20" aria-hidden="true" />
          <span className="text-sm text-white/80 font-medium truncate max-w-xs sm:max-w-md">
            {session.candidate_profile.specialization || session.candidate_profile.recent_role || 'AI Fluency Mock Interview'}
          </span>
          <span className="hidden sm:inline-block text-[11px] font-medium text-white/60 border border-white/10 rounded-md px-2 py-0.5">
            Question {progress.current} of {progress.total}
          </span>
          <Badge variant={isConnected ? 'success' : connectionState === 'connecting' ? 'warning' : 'danger'} className="text-[10px] py-0.5 px-2">
            {connectionState === 'connecting' ? 'Đang kết nối' : isConnected ? 'Đã kết nối thời gian thực' : 'Đã ngắt kết nối'}
          </Badge>
        </div>

        <div className="flex items-center gap-4">
          <span className="text-sm font-mono text-white/90">{formattedTimer}</span>
          <button
            type="button"
            onClick={() => setEndModalOpen(true)}
            className="rounded-lg bg-red-600 px-4 py-1.5 text-xs font-semibold text-white transition-colors hover:bg-red-500 shadow-md shadow-red-600/20"
          >
            End Interview
          </button>
        </div>
      </header>

      {/* Main Studio Stage - Ported from fipilot-v1 InterviewStage (giữ header hiện tại) */}
      <main className="relative flex flex-1 flex-col overflow-hidden bg-black">
        {isComplete ? (
          <div className="relative z-10 flex flex-1 items-center justify-center p-6">
            <div className="max-w-xl rounded-2xl border border-white/10 bg-[#161820] p-6 text-center shadow-2xl">
              <CheckCircle2 className="mx-auto h-12 w-12 text-success" />
              <h2 className="mt-3 text-2xl font-bold text-white">Phỏng vấn hoàn tất</h2>
              <p className="mt-1 text-sm text-white/70">Tuyệt vời! Phiên phỏng vấn của bạn đã kết thúc.</p>

              {finalReportState === 'loading' && (
                <div className="mt-4 flex items-center justify-center gap-2 text-sm text-accent" role="status">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Đang tính điểm cuối
                </div>
              )}

              {finalReport && (
                <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
                  {[
                    ['Overall', finalReport.overall_score],
                    ['Technical', finalReport.technical_score],
                    ['Communication', finalReport.communication_score],
                    ['Correctness', finalReport.correctness_score],
                  ].map(([label, score]) => (
                    <div key={label} className="rounded-xl border border-white/10 bg-white/5 p-3 text-center">
                      <p className="text-xs text-white/50">{label}</p>
                      <p className="mt-1 font-display text-xl font-bold text-white">
                        {(score as number).toFixed(1)}
                        <span className="text-xs text-white/40">/10</span>
                      </p>
                    </div>
                  ))}
                </div>
              )}

              {finalReportState === 'error' && (
                <div className="mt-4 rounded-lg border border-danger/30 bg-danger/10 p-3 text-left">
                  <p className="text-xs text-danger" role="alert">{finalReportError}</p>
                  <button
                    type="button"
                    onClick={() => setFinalReportRetry((v) => v + 1)}
                    className="mt-2 flex items-center gap-1 text-xs font-semibold text-accent hover:underline"
                  >
                    <RefreshCw className="h-3 w-3" /> Thử lại chấm điểm
                  </button>
                </div>
              )}

              <div className="mt-6 flex flex-wrap justify-center gap-3">
                <Button
                  disabled={finalReportState === 'loading'}
                  onClick={() => navigate(`/text-interview/${sessionId}/report`)}
                >
                  <FileText className="h-4 w-4 mr-1.5" />
                  Xem báo cáo cuối
                </Button>
                <Button variant="secondary" onClick={() => navigate('/interview-history')}>
                  <History className="h-4 w-4 mr-1.5" />
                  Quay lại lịch sử
                </Button>
              </div>
            </div>
          </div>
        ) : (
          <V1InterviewStage
            session={session}
            voiceState={voiceState}
            isConnected={isConnected}
            isComplete={isComplete}
            speaking={speaking}
            transcript={transcript}
            currentQuestionText={currentQuestionText}
            greetingComplete={greetingComplete}
            questionStreaming={questionStreaming}
            captionsActive={captionsActive}
            cameraActive={cameraActive}
            chatActive={chatActive}
            microphoneActive={voiceState === VoiceInterviewState.USER_SPEAKING}
            videoRef={videoRef}
            onSendText={(text) => void submitCandidateAnswer(text)}
            onGreetingComplete={handleGreetingComplete}
            onToggleMicrophone={
              voiceState === VoiceInterviewState.USER_SPEAKING
                ? () => void stopListening()
                : () => void startListening()
            }
            onToggleCamera={toggleCamera}
            onToggleCaptions={() => setCaptionsActive(!captionsActive)}
            onToggleChat={() => setChatActive(!chatActive)}
          />
        )}

        {import.meta.env.DEV && (
          <div className="pointer-events-none absolute bottom-2 left-2 z-30 space-y-1 text-left text-[11px] text-white/40">
            {localTurnLatencyMs !== null && <p>Latency: {Math.round(localTurnLatencyMs)} ms</p>}
          </div>
        )}

        {/* Accessible Waveform for screen reader / tests */}
        <div className="sr-only" role="img" aria-label={waveformLabel}>
          {speaking && <span className="animate-pulse" />}
        </div>

        {/* Connection / transport status banners */}
        {(transportError || microphoneError || audioWarning) && (
          <div className="pointer-events-none absolute inset-x-0 top-2 z-30 mx-auto flex w-full max-w-2xl flex-col gap-1 px-4">
            {transportError && (
              <div className="rounded-lg border border-danger/30 bg-danger/10 px-3 py-2 text-xs text-danger" role="alert">
                <span>{transportError}</span>
                <button type="button" onClick={retryConnection} className="ml-2 font-semibold underline hover:text-danger/80">
                  Kết nối lại
                </button>
              </div>
            )}
            {microphoneError && (
              <div className="rounded-lg border border-danger/30 bg-danger/10 px-3 py-2 text-xs text-danger" role="alert">
                <span>{microphoneError}</span>
                <button type="button" onClick={() => void startListening()} className="ml-2 font-semibold underline hover:text-danger/80">
                  Thử lại
                </button>
              </div>
            )}
            {audioWarning && (
              <div className="rounded-lg border border-amber-400/30 bg-amber-400/10 px-3 py-2 text-xs text-amber-300" role="status">
                {audioWarning}
              </div>
            )}
          </div>
        )}

        <p className="sr-only" role="status" aria-live="polite">
          {microphonePermissionLabel}
        </p>

        <div className="sr-only">
          <button
            type="button"
            disabled={!microphoneActionable}
            onClick={
              voiceState === VoiceInterviewState.USER_SPEAKING
                ? () => void stopListening()
                : () => void startListening()
            }
            aria-label={
              voiceState === VoiceInterviewState.USER_SPEAKING
                ? 'Dừng và gửi câu trả lời'
                : voiceState === VoiceInterviewState.AI_SPEAKING
                  ? 'Nhà phỏng vấn AI đang nói'
                  : voiceState === VoiceInterviewState.WAITING_FOR_USER
                    ? 'Bắt đầu trả lời'
                    : voiceState === VoiceInterviewState.TRANSCRIBING
                      ? 'Đang hiểu câu trả lời của bạn...'
                      : voiceState === VoiceInterviewState.EVALUATING
                        ? 'Đang đánh giá câu trả lời...'
                        : 'Sẵn sàng'
            }
          >
            {voiceState === VoiceInterviewState.USER_SPEAKING
              ? 'Dừng và gửi câu trả lời'
              : voiceState === VoiceInterviewState.AI_SPEAKING
                ? 'Nhà phỏng vấn AI đang nói'
                : voiceState === VoiceInterviewState.WAITING_FOR_USER
                  ? 'Bắt đầu trả lời'
                  : voiceState === VoiceInterviewState.TRANSCRIBING
                    ? 'Đang hiểu câu trả lời của bạn...'
                    : voiceState === VoiceInterviewState.EVALUATING
                      ? 'Đang đánh giá câu trả lời...'
                      : 'Sẵn sàng'}
          </button>
        </div>
      </main>

      <EndInterviewConfirmModal
        isOpen={endModalOpen}
        onCancel={() => setEndModalOpen(false)}
        onConfirm={() => {
          setEndModalOpen(false)
          void stopListening()
          navigate(`/text-interview/${sessionId}/report`)
        }}
      />
    </div>
  )
}

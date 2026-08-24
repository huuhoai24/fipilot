import React, { useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  AlertCircle,
  ArrowLeft,
  CheckCircle2,
  FileText,
  History,
  Loader2,
  RefreshCw,
  Signal,
  User,
  X,
} from 'lucide-react'
import { FloatingMediaControls } from '@/components/voice/FloatingMediaControls'
import { SpeechWaveform } from '@/components/voice/SpeechWaveform'
import { EndInterviewConfirmModal } from '@/components/voice/EndInterviewConfirmModal'

import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { firebaseAuth } from '@/lib/firebase'
import { api } from '@/lib/api'
import { PcmAudioPlayer } from '@/lib/pcmAudioPlayer'
import { getUserFacingError } from '@/lib/userFacingError'
import type {
  InterviewReport,
  V2InterviewSessionResponse,
  V2InterviewSessionState,
  V2InterviewTurn,
} from '@/types'
import { VoiceInterviewState } from '@/types'

const MAX_PENDING_CHUNKS = 8
const MAX_CLIENT_CHUNK_BYTES = 256 * 1024
const MAX_SOCKET_BUFFERED_BYTES = 2 * 1024 * 1024
const MAX_RECONNECT_ATTEMPTS = 3
const AUTH_SUBPROTOCOL = 'firebase-auth'

type VoiceConnectionState = 'connecting' | 'connected' | 'disconnected' | 'error'
type FinalReportState = 'idle' | 'loading' | 'ready' | 'error'
type MicrophonePermissionState =
  | 'unknown'
  | 'requesting'
  | 'granted'
  | 'denied'
  | 'unavailable'

interface VoiceServerEvent {
  type:
    | 'connected'
    | 'state'
    | 'transcript_partial'
    | 'transcript_final'
    | 'audio_ack'
    | 'audio_dropped'
    | 'processing'
    | 'question'
    | 'question_start'
    | 'question_delta'
    | 'question_complete'
    | 'tts_start'
    | 'audio_format'
    | 'tts_complete'
    | 'tts_cancelled'
    | 'completed'
    | 'error'
  value?: VoiceInterviewState
  text?: string
  sequence?: number
  dropped?: number
  stage?: 'evaluation'
  code?: string
  message?: string
  sample_rate?: number
  format?: 'pcm'
}

function questionText(turn?: V2InterviewTurn | null): string {
  if (!turn) return ''
  return typeof turn.question === 'string' ? turn.question : turn.question.question
}

function stopMediaStream(stream: MediaStream | null) {
  stream?.getTracks().forEach((track) => track.stop())
}

function microphoneErrorMessage(error: unknown): string {
  if (error instanceof DOMException && (
    error.name === 'NotAllowedError'
    || error.name === 'PermissionDeniedError'
  )) {
    return 'Microphone permission was denied. Allow access in your browser settings and try again.'
  }
  if (error instanceof DOMException && error.name === 'NotFoundError') {
    return 'No microphone was found. Connect a microphone and try again.'
  }
  return 'The microphone could not be opened. Check your browser and device settings.'
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

function isVoiceState(value: unknown): value is VoiceInterviewState {
  return Object.values(VoiceInterviewState).includes(value as VoiceInterviewState)
}

export function SpeechInterviewPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const mountedRef = useRef(true)
  const websocketRef = useRef<WebSocket | null>(null)
  const sessionRef = useRef<V2InterviewSessionState | null>(null)
  const transcriptRef = useRef('')
  const hasConnectedRef = useRef(false)
  const playbackRef = useRef<PcmAudioPlayer | null>(null)
  const playbackQueueRef = useRef<Promise<void>>(Promise.resolve())
  const ttsActiveRef = useRef(false)
  const mediaStreamRef = useRef<MediaStream | null>(null)
  const audioContextRef = useRef<AudioContext | null>(null)
  const audioSourceRef = useRef<MediaStreamAudioSourceNode | null>(null)
  const audioWorkletRef = useRef<AudioWorkletNode | null>(null)
  const recordingStartPendingRef = useRef(false)
  const recordingGenerationRef = useRef(0)
  const activeRecordingGenerationRef = useRef<number | null>(null)
  const recordingStopPendingRef = useRef<number | null>(null)
  const stoppedRecordingGenerationRef = useRef<number | null>(null)
  const sendQueueRef = useRef<Promise<void>>(Promise.resolve())
  const pendingChunksRef = useRef(0)
  const sequenceRef = useRef(0)
  const turnProcessingStartedAtRef = useRef<number | null>(null)
  const turnLatencyRecordedRef = useRef(false)
  const [session, setSession] = useState<V2InterviewSessionState | null>(null)
  const [voiceState, setVoiceState] = useState(VoiceInterviewState.IDLE)
  const [connectionState, setConnectionState] = useState<VoiceConnectionState>('connecting')
  const [reconnectNonce, setReconnectNonce] = useState(0)
  const [elapsedSeconds, setElapsedSeconds] = useState(0)
  const [acknowledgedChunks, setAcknowledgedChunks] = useState(0)
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
  const [endModalOpen, setEndModalOpen] = useState(false)
  const cameraStreamRef = useRef<MediaStream | null>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const interviewComplete = session !== null && session.current_turn === null

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

  const speakQuestionSmoothly = async (text: string) => {
    if (!text || lastSpokenQuestionRef.current === text) return
    lastSpokenQuestionRef.current = text

    if (currentAudioRef.current) {
      currentAudioRef.current.pause()
      currentAudioRef.current = null
    }
    if (animFrameRef.current) {
      cancelAnimationFrame(animFrameRef.current)
    }

    try {
      setVoiceState(VoiceInterviewState.AI_SPEAKING)
      setCurrentQuestionText('')
      setQuestionStreaming(true)

      const res = await fetch('http://localhost:8000/api/v1/speech', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      })

      if (res.ok) {
        const blob = await res.blob()
        const audioUrl = URL.createObjectURL(blob)
        const audio = new Audio(audioUrl)
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
          currentAudioRef.current = null
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

  const submitCandidateAnswer = async (answerText: string) => {
    if (!answerText || !sessionId || !session?.current_turn) return
    const turnId = session.current_turn.turn_id
    setVoiceState(VoiceInterviewState.EVALUATING)
    try {
      const updated = await api.submitV2InterviewAnswer(sessionId, turnId, answerText)
      setSession(updated.state)
      setTranscript('')
    } catch (err) {
      setTransportError(getUserFacingError(err, 'Could not evaluate answer. Please retry.'))
      setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
    }
  }

  useEffect(() => {
    const q = session?.current_turn ? questionText(session.current_turn) : ''
    if (q && !import.meta.env.VITEST && session?.interview_config.mode === 'voice') {
      void speakQuestionSmoothly(q)
    }
  }, [session?.current_turn])

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
    const startWasPending = recordingStartPendingRef.current
    recordingGenerationRef.current += 1
    recordingStartPendingRef.current = false
    activeRecordingGenerationRef.current = null
    if (audioWorkletRef.current) {
      audioWorkletRef.current.port.onmessage = null
      audioWorkletRef.current.disconnect()
    }
    audioWorkletRef.current = null
    audioSourceRef.current?.disconnect()
    audioSourceRef.current = null
    const audioContext = audioContextRef.current
    audioContextRef.current = null
    if (audioContext && audioContext.state !== 'closed') void audioContext.close()
    stopMediaStream(mediaStreamRef.current)
    mediaStreamRef.current = null
    if (startWasPending && mountedRef.current) {
      setMicrophonePermission('unknown')
    }
  }

  const releasePlayback = () => {
    ttsActiveRef.current = false
    const player = playbackRef.current
    playbackRef.current = null
    playbackQueueRef.current = Promise.resolve()
    if (player) void player.close()
  }

  const ensurePlayback = (): PcmAudioPlayer => {
    if (!playbackRef.current) {
      playbackRef.current = new PcmAudioPlayer()
    }
    return playbackRef.current
  }

  const queuePlayback = (operation: () => void | Promise<void>) => {
    playbackQueueRef.current = playbackQueueRef.current
      .catch(() => undefined)
      .then(operation)
      .catch(() => {
        if (mountedRef.current) {
          ttsActiveRef.current = false
          setVoiceState(VoiceInterviewState.IDLE)
          setTransportError('AI speech playback could not continue.')
        }
      })
  }

  useEffect(() => {
    mountedRef.current = true
    return () => {
      mountedRef.current = false
      releaseMedia()
      releasePlayback()
      if (cameraStreamRef.current) {
        stopMediaStream(cameraStreamRef.current)
        cameraStreamRef.current = null
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
        if (!cancelled) setSession(response.state)
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

    let disposed = false
    let reconnectTimer: number | undefined
    let reconnectAttempts = 0

    const connect = async (forceRefresh = false) => {
      if (disposed) return
      setConnectionState('connecting')
      setTransportError('')

      const user = firebaseAuth.currentUser
      if (!user) {
        setConnectionState('error')
        setTransportError('Authentication is required to open the voice connection.')
        return
      }

      try {
        const token = await user.getIdToken(forceRefresh)
        if (disposed) return
        const socket = new WebSocket(
          api.getVoiceInterviewWebSocketUrl(sessionId),
          [AUTH_SUBPROTOCOL, token]
        )
        socket.binaryType = 'arraybuffer'
        websocketRef.current = socket

        socket.onopen = () => {
          if (!disposed) reconnectAttempts = 0
        }
        socket.onmessage = (message) => {
          if (disposed) return
          if (message.data instanceof ArrayBuffer) {
            const payload = message.data
            if (
              ttsActiveRef.current
              && turnProcessingStartedAtRef.current !== null
              && !turnLatencyRecordedRef.current
            ) {
              turnLatencyRecordedRef.current = true
              setLocalTurnLatencyMs(
                Math.max(0, performance.now() - turnProcessingStartedAtRef.current)
              )
            }
            const player = ensurePlayback()
            queuePlayback(() => {
              player.enqueue(payload)
            })
            return
          }
          if (typeof message.data !== 'string') return
          try {
            const event = JSON.parse(message.data) as VoiceServerEvent
            if (event.type === 'connected') {
              setConnectionState('connected')
              setTransportError('')
              setAudioWarning('')
              const reconnecting = hasConnectedRef.current
              if (!reconnecting) {
                socket.send(JSON.stringify({ type: 'speak_question' }))
              }
              if (reconnecting) {
                void api.getV2InterviewSession(sessionId)
                  .then((response: V2InterviewSessionResponse) => {
                    if (disposed) return
                    const previous = sessionRef.current
                    const next = response.state
                    const advanced = Boolean(
                      previous
                      && (
                        next.completed_turns.length > previous.completed_turns.length
                        || next.current_turn?.turn_id !== previous.current_turn?.turn_id
                      )
                    )
                    setSession(next)
                    if (advanced) {
                      setCurrentQuestionText(questionText(next.current_turn))
                      setQuestionStreaming(false)
                      setTranscript('')
                      setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
                    }
                  })
                  .catch(() => {
                    if (!disposed) {
                      setTransportError('Reconnected, but interview state could not refresh.')
                    }
                  })
              }
              hasConnectedRef.current = true
            } else if (event.type === 'state' && isVoiceState(event.value)) {
              setVoiceState(event.value)
              if (
                event.value === VoiceInterviewState.TRANSCRIBING
                || event.value === VoiceInterviewState.EVALUATING
                || event.value === VoiceInterviewState.AI_THINKING
              ) {
                if (event.value === VoiceInterviewState.TRANSCRIBING) {
                  turnProcessingStartedAtRef.current ??= performance.now()
                  turnLatencyRecordedRef.current = false
                  setLocalTurnLatencyMs(null)
                }
                releaseMedia()
              } else if (
                event.value === VoiceInterviewState.USER_SPEAKING
                && ttsActiveRef.current
              ) {
                releasePlayback()
                setTranscript('')
                setElapsedSeconds(0)
              }
            } else if (
              (event.type === 'transcript_partial' || event.type === 'transcript_final')
              && typeof event.text === 'string'
            ) {
              setTranscript(event.text)
            } else if (event.type === 'audio_ack') {
              setAcknowledgedChunks((count) => count + 1)
            } else if (event.type === 'audio_dropped') {
              setAudioWarning(
                'Some audio was skipped because recognition fell behind. Try speaking in shorter turns.'
              )
            } else if (event.type === 'processing' && event.stage === 'evaluation') {
              setVoiceState(VoiceInterviewState.EVALUATING)
            } else if (event.type === 'question_start') {
              setCurrentQuestionText('')
              setQuestionStreaming(true)
              setVoiceState(VoiceInterviewState.AI_THINKING)
            } else if (event.type === 'question_delta' && typeof event.text === 'string') {
              setCurrentQuestionText((current) => current + event.text)
            } else if (event.type === 'question_complete' && typeof event.text === 'string') {
              setCurrentQuestionText(event.text)
              setQuestionStreaming(false)
              setTranscript('')
              if (!ttsActiveRef.current) {
                setVoiceState(VoiceInterviewState.IDLE)
              }
              void api.getV2InterviewSession(sessionId)
                .then((response: V2InterviewSessionResponse) => {
                  if (!disposed) {
                    setSession(response.state)
                    setCurrentQuestionText('')
                  }
                })
                .catch(() => {
                  if (!disposed) {
                    setTransportError('The next question arrived, but interview progress could not refresh.')
                  }
                })
            } else if (event.type === 'tts_start') {
              ttsActiveRef.current = true
              const player = ensurePlayback()
              player.beginStream()
              queuePlayback(() => player.prepare())
              setVoiceState(VoiceInterviewState.AI_SPEAKING)
              void startAudioCapture('start_barge_in', false)
            } else if (
              event.type === 'audio_format'
              && typeof event.sample_rate === 'number'
              && event.format === 'pcm'
            ) {
              const player = ensurePlayback()
              queuePlayback(() => {
                player.configure(event.sample_rate!, event.format!)
              })
            } else if (event.type === 'tts_complete') {
              const player = ensurePlayback()
              queuePlayback(async () => {
                await player.markStreamComplete()
                if (!disposed && mountedRef.current) {
                  ttsActiveRef.current = false
                  releaseMedia()
                  sendControl('playback_complete')
                }
              })
            } else if (event.type === 'tts_cancelled') {
              releasePlayback()
              setTranscript('')
              setElapsedSeconds(0)
              setVoiceState(VoiceInterviewState.INTERRUPTED)
            } else if (event.type === 'question' && typeof event.text === 'string') {
              setCurrentQuestionText(event.text)
              setQuestionStreaming(false)
              setTranscript('')
              setVoiceState(VoiceInterviewState.IDLE)
              releasePlayback()
              void api.getV2InterviewSession(sessionId)
                .then((response: V2InterviewSessionResponse) => {
                  if (!disposed) {
                    setSession(response.state)
                    setCurrentQuestionText('')
                  }
                })
                .catch(() => {
                  if (!disposed) {
                    setTransportError('The next question arrived, but interview progress could not refresh.')
                  }
                })
            } else if (event.type === 'completed') {
              setSession((current) => (
                current ? { ...current, current_turn: null } : current
              ))
              setCurrentQuestionText('')
              setQuestionStreaming(false)
              setTranscript('')
              setVoiceState(VoiceInterviewState.IDLE)
              releasePlayback()
              void api.getV2InterviewSession(sessionId)
                .then((response: V2InterviewSessionResponse) => {
                  if (!disposed) setSession(response.state)
                })
                .catch(() => {
                  if (!disposed) {
                    setTransportError('The interview completed, but final progress could not refresh.')
                  }
                })
            } else if (event.type === 'error') {
              if (
                event.message?.toLowerCase().includes('audio could not be generated') ||
                event.message?.toLowerCase().includes('tts')
              ) {
                const questionToSpeak =
                  currentQuestionText || questionText(sessionRef.current?.current_turn)
                if (questionToSpeak) {
                  void speakQuestionSmoothly(questionToSpeak)
                }
                setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
              } else {
                setTransportError(event.message || 'The voice server rejected a message.')
              }
              if (
                event.code === 'answer_not_ready'
                || event.code === 'answer_evaluation_failed'
                || event.code === 'empty_answer'
                || event.code === 'invalid_session_state'
              ) {
                setCurrentQuestionText('')
                setQuestionStreaming(false)
                setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
              }
            }
          } catch {
            setTransportError('The voice server returned an invalid event.')
          }
        }
        socket.onerror = () => {
          if (!disposed) setTransportError('The realtime voice connection encountered an error.')
        }
        socket.onclose = (event) => {
          if (websocketRef.current === socket) websocketRef.current = null

          setVoiceState(VoiceInterviewState.IDLE)
          const retryable = event.code === 1001
            || event.code === 1006
            || event.code === 1009
            || event.code === 1011
          if (retryable && reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
            reconnectAttempts += 1
            setConnectionState('connecting')
            reconnectTimer = window.setTimeout(
              () => void connect(event.code === 1006),
              Math.min(1000 * 2 ** (reconnectAttempts - 1), 4000)
            )
          } else {
            setConnectionState(event.code >= 4400 ? 'error' : 'disconnected')
            if (!event.reason && event.code >= 4400) {
              setTransportError('The voice connection was rejected.')
            } else if (event.reason) {
              setTransportError(event.reason)
            }
          }
        }
      } catch {
        if (!disposed) {
          setConnectionState('error')
          setTransportError('Unable to authenticate the realtime voice connection.')
        }
      }
    }

    void connect()
    return () => {
      disposed = true
      if (reconnectTimer !== undefined) window.clearTimeout(reconnectTimer)
      const socket = websocketRef.current
      websocketRef.current = null
      if (socket && socket.readyState < WebSocket.CLOSING) socket.close(1000, 'Page closed.')
      releaseMedia()
      releasePlayback()
    }
  }, [reconnectNonce, session?.interview_config.mode, sessionId])

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

  const sendControl = (
    type:
      | 'start_listening'
      | 'stop_listening'
      | 'start_barge_in'
      | 'playback_complete'
      | 'speak_question'
  ): boolean => {
    const socket = websocketRef.current
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      setTransportError('The voice connection is not ready.')
      return false
    }
    socket.send(JSON.stringify({ type }))
    return true
  }

  const queueAudioChunk = (payload: ArrayBuffer) => {
    if (!payload.byteLength) return
    if (payload.byteLength > MAX_CLIENT_CHUNK_BYTES || pendingChunksRef.current >= MAX_PENDING_CHUNKS) {
      setTransportError('Audio transport is overloaded. Reconnect and try again.')
      websocketRef.current?.close(1009, 'Client audio backpressure limit reached.')
      return
    }

    pendingChunksRef.current += 1
    const sequence = sequenceRef.current++
    sendQueueRef.current = sendQueueRef.current
      .catch(() => undefined)
      .then(async () => {
        const socket = websocketRef.current
        if (!socket || socket.readyState !== WebSocket.OPEN) return
        if (socket.bufferedAmount > MAX_SOCKET_BUFFERED_BYTES) {
          throw new Error('WebSocket backpressure limit reached.')
        }
        if (!mountedRef.current || socket.readyState !== WebSocket.OPEN) return
        socket.send(JSON.stringify({
          type: 'audio_chunk',
          sequence,
          encoding: 'pcm_s16le',
          sample_rate: 16000,
        }))
        socket.send(payload)
      })
      .catch(() => {
        if (mountedRef.current) {
          setTransportError('Audio transport could not keep up. Reconnecting is required.')
          websocketRef.current?.close(1009, 'Audio transport backpressure.')
        }
      })
      .finally(() => {
        pendingChunksRef.current = Math.max(0, pendingChunksRef.current - 1)
      })
  }

  const startAudioCapture = async (
    controlType: 'start_listening' | 'start_barge_in',
    resetAnswer = true,
  ) => {
    if (recordingStartPendingRef.current || mediaStreamRef.current) return
    setMicrophoneError('')
    setTransportError('')
    const activeSocket = websocketRef.current
    if (!activeSocket || activeSocket.readyState !== WebSocket.OPEN) {
      setTransportError('Wait for the realtime connection before starting.')
      return
    }
    if (
      !navigator.mediaDevices?.getUserMedia
      || typeof AudioContext === 'undefined'
      || typeof AudioWorkletNode === 'undefined'
    ) {
      setMicrophonePermission('unavailable')
      setMicrophoneError('This browser does not support streaming microphone capture.')
      return
    }

    const recordingGeneration = recordingGenerationRef.current + 1
    recordingGenerationRef.current = recordingGeneration
    recordingStartPendingRef.current = true
    let stream: MediaStream | null = null
    let audioContext: AudioContext | null = null
    let source: MediaStreamAudioSourceNode | null = null
    let worklet: AudioWorkletNode | null = null

    const isCurrentRecordingStart = () => (
      mountedRef.current
      && recordingGenerationRef.current === recordingGeneration
    )
    const releaseOwnedMedia = () => {
      if (activeRecordingGenerationRef.current === recordingGeneration) {
        activeRecordingGenerationRef.current = null
      }
      if (worklet && audioWorkletRef.current === worklet) {
        worklet.port.onmessage = null
        worklet.disconnect()
        audioWorkletRef.current = null
      }
      if (source && audioSourceRef.current === source) {
        source.disconnect()
        audioSourceRef.current = null
      }
      if (audioContext && audioContextRef.current === audioContext) {
        audioContextRef.current = null
        if (audioContext.state !== 'closed') void audioContext.close()
      }
      if (stream && mediaStreamRef.current === stream) {
        mediaStreamRef.current = null
        stopMediaStream(stream)
      }
    }

    try {
      setMicrophonePermission('requesting')
      stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      })
      if (!isCurrentRecordingStart()) {
        stopMediaStream(stream)
        return
      }
      setMicrophonePermission('granted')

      stopMediaStream(mediaStreamRef.current)
      mediaStreamRef.current = stream

      if (!import.meta.env.VITEST && typeof MediaRecorder !== 'undefined') {
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
              const res = await fetch('http://localhost:8000/api/v1/speech/recognize', {
                method: 'POST',
                body: formData,
              })
              const data = await res.json().catch(() => null)
              if (data?.text) {
                setTranscript(data.text)
                void submitCandidateAnswer(data.text)
              } else {
                setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
              }
            } catch {
              setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
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
      }

      audioContext = new AudioContext({ sampleRate: 16000 })
      audioContextRef.current = audioContext
      await audioContext.audioWorklet.addModule('/pcm-worklet.js')
      if (!isCurrentRecordingStart()) {
        releaseOwnedMedia()
        return
      }
      if (audioContext.sampleRate !== 16000) {
        throw new Error('The browser did not provide a 16 kHz audio context.')
      }
      source = audioContext.createMediaStreamSource(stream)
      worklet = new AudioWorkletNode(audioContext, 'pcm16-capture')
      audioSourceRef.current = source
      audioWorkletRef.current = worklet
      worklet.port.onmessage = (event: MessageEvent<ArrayBuffer>) => {
        if (event.data instanceof ArrayBuffer) queueAudioChunk(event.data)
      }
      sequenceRef.current = 0
      sendQueueRef.current = Promise.resolve()
      pendingChunksRef.current = 0
      setAcknowledgedChunks(0)
      if (resetAnswer) {
        setElapsedSeconds(0)
        setTranscript('')
      }

      if (!sendControl(controlType)) {
        recordingGenerationRef.current += 1
        recordingStartPendingRef.current = false
        releaseOwnedMedia()
        return
      }
      activeRecordingGenerationRef.current = recordingGeneration
      source.connect(worklet)
      worklet.connect(audioContext.destination)
      await audioContext.resume()
      if (!isCurrentRecordingStart()) {
        releaseOwnedMedia()
        return
      }
      await ensurePlayback().prepare()
      if (!isCurrentRecordingStart()) releaseOwnedMedia()
    } catch (error) {
      const isCurrent = isCurrentRecordingStart()
      releaseOwnedMedia()
      if (isCurrent) {
        recordingGenerationRef.current += 1
        recordingStartPendingRef.current = false
        setMicrophonePermission(microphonePermissionAfterError(error))
        setMicrophoneError(microphoneErrorMessage(error))
      }
    } finally {
      if (recordingGenerationRef.current === recordingGeneration) {
        recordingStartPendingRef.current = false
      }
    }
  }

  const startListening = () => {
    turnProcessingStartedAtRef.current = null
    turnLatencyRecordedRef.current = false
    setLocalTurnLatencyMs(null)
    void startAudioCapture('start_listening')
  }

  const stopListening = async () => {
    if (nativeRecorderRef.current && nativeRecorderRef.current.state === 'recording') {
      nativeRecorderRef.current.stop()
    }
    if (voiceState !== VoiceInterviewState.USER_SPEAKING) return
    const recordingGeneration = activeRecordingGenerationRef.current
    if (recordingGeneration === null) {
      if (recordingStartPendingRef.current) {
        setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
        releaseMedia()
      }
      return
    }
    if (
      recordingStopPendingRef.current === recordingGeneration
      || stoppedRecordingGenerationRef.current === recordingGeneration
    ) {
      return
    }
    recordingStopPendingRef.current = recordingGeneration
    stoppedRecordingGenerationRef.current = recordingGeneration
    turnProcessingStartedAtRef.current = performance.now()
    turnLatencyRecordedRef.current = false
    setLocalTurnLatencyMs(null)
    setVoiceState(VoiceInterviewState.TRANSCRIBING)
    releaseMedia()
    try {
      await sendQueueRef.current.catch(() => undefined)
      if (
        !sendControl('stop_listening')
        && activeRecordingGenerationRef.current === null
      ) {
        setVoiceState(VoiceInterviewState.WAITING_FOR_USER)
      }
    } finally {
      if (recordingStopPendingRef.current === recordingGeneration) {
        recordingStopPendingRef.current = null
      }
    }
  }

  const retryConnection = () => {
    setTransportError('')
    setConnectionState('connecting')
    setReconnectNonce((value) => value + 1)
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
    unknown: 'Microphone access pending',
    requesting: 'Requesting microphone access',
    granted: 'Microphone access granted',
    denied: 'Microphone access denied',
    unavailable: 'Microphone unavailable',
  }[microphonePermission]

  const waveformMode = voiceState === VoiceInterviewState.USER_SPEAKING
    ? 'user'
    : voiceState === VoiceInterviewState.AI_SPEAKING
      ? 'ai'
      : 'idle'

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
            {connectionState === 'connecting' ? 'Connecting' : isConnected ? 'Realtime connected' : 'Disconnected'}
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

      {/* Main Studio Stage */}
      <main className="relative flex flex-1 flex-col items-center justify-center p-6 text-center">

        {/* Slide-over Chat / Transcript Drawer if chatActive */}
        {chatActive && (
          <div className="absolute inset-y-0 right-0 z-40 w-80 sm:w-96 border-l border-white/10 bg-[#14171f] p-4 text-left shadow-2xl flex flex-col">
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <h3 className="text-sm font-semibold text-white">Interview Transcript</h3>
              <button
                type="button"
                onClick={() => setChatActive(false)}
                className="rounded p-1 text-white/60 hover:bg-white/10 hover:text-white"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto py-3 space-y-3 text-xs">
              {session.completed_turns.map((turn, i) => (
                <div key={turn.turn_id || i} className="space-y-1">
                  <p className="font-semibold text-accent">Q{i + 1}: {questionText(turn)}</p>
                  <p className="text-white/80 bg-white/5 p-2 rounded-lg">{turn.answer}</p>
                </div>
              ))}
              {session.current_turn && (
                <div className="space-y-1">
                  <p className="font-semibold text-accent">Current Q: {questionText(session.current_turn)}</p>
                  {transcript && <p className="text-blue-300 italic bg-blue-500/10 p-2 rounded-lg">{transcript}</p>}
                </div>
              )}
              {import.meta.env.DEV && (
                <div className="pt-3 border-t border-white/10 text-[11px] text-white/40 space-y-1">
                  {localTurnLatencyMs !== null && <p>Latency: {Math.round(localTurnLatencyMs)} ms</p>}
                  {acknowledgedChunks > 0 && <p>Audio chunks: {acknowledgedChunks}</p>}
                </div>
              )}
            </div>
          </div>
        )}

        {isComplete ? (
          /* Completion & Scoring Screen */
          <div className="relative z-10 max-w-xl rounded-2xl border border-white/10 bg-[#161820] p-6 text-center shadow-2xl">
            <CheckCircle2 className="mx-auto h-12 w-12 text-success" />
            <h2 className="mt-3 text-2xl font-bold text-white">Interview complete</h2>
            <p className="mt-1 text-sm text-white/70">Great job! Your interview session is complete.</p>

            {finalReportState === 'loading' && (
              <div className="mt-4 flex items-center justify-center gap-2 text-sm text-accent" role="status">
                <Loader2 className="h-4 w-4 animate-spin" />
                Calculating final scores
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
                  className="mt-2 text-xs font-semibold text-accent hover:underline flex items-center gap-1"
                >
                  <RefreshCw className="h-3 w-3" /> Retry scores
                </button>
              </div>
            )}

            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <Button
                disabled={finalReportState === 'loading'}
                onClick={() => navigate(`/text-interview/${sessionId}/report`)}
              >
                <FileText className="h-4 w-4 mr-1.5" />
                View Final Report
              </Button>
              <Button variant="secondary" onClick={() => navigate('/interview-history')}>
                <History className="h-4 w-4 mr-1.5" />
                Back to History
              </Button>
            </div>
          </div>
        ) : (
          /* Live Subtitle / Question Stage + Right Candidate Camera (Matching Layout) */
          <div className="relative z-10 w-full max-w-7xl px-4 sm:px-8 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center min-h-[calc(100vh-220px)]">
            {/* Left: AI Question & Subtitles */}
            <div className="lg:col-span-7 space-y-6 text-left">
              {captionsActive && (
                <div className="space-y-4">
                  {/* 3 Green Dots Indicator */}
                  <div className="flex items-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-accent animate-pulse" />
                    <span className="h-2 w-2 rounded-full bg-accent animate-pulse delay-100" />
                    <span className="h-2 w-2 rounded-full bg-accent animate-pulse delay-200" />
                  </div>

                  {/* Subtitle Text */}
                  <p className="text-xl sm:text-2xl lg:text-3xl font-medium leading-relaxed tracking-tight text-white/95 transition-all">
                    {questionStreaming
                      ? currentQuestionText
                      : currentQuestionText || questionText(session.current_turn)}
                    {questionStreaming && (
                      <span className="ml-1 inline-block h-6 w-0.5 animate-pulse bg-accent align-middle" />
                    )}
                  </p>

                  {/* Live Candidate Speech Transcript */}
                  <div className="sr-only">
                    <label htmlFor="voice-transcript-hidden">Interview answer transcript</label>
                    <textarea
                      id="voice-transcript-hidden"
                      readOnly
                      value={transcript}
                      aria-label="Interview answer transcript"
                    />
                  </div>

                  {transcript && (
                    <div className="rounded-xl border border-blue-500/20 bg-blue-500/10 p-3.5 text-sm text-blue-200 animate-fade-in">
                      <span className="font-semibold text-blue-300 mr-1.5">You:</span>
                      {transcript}
                    </div>
                  )}

                  {/* Status Messages */}
                  {voiceState === VoiceInterviewState.WAITING_FOR_USER && (
                    <p className="text-xs font-medium text-accent animate-pulse">
                      Ready for your answer
                    </p>
                  )}
                  {voiceState === VoiceInterviewState.USER_SPEAKING && (
                    <p className="text-xs font-medium text-accent animate-pulse">
                      Recording your answer
                    </p>
                  )}
                  {voiceState === VoiceInterviewState.TRANSCRIBING && (
                    <p className="text-xs font-medium text-accent animate-pulse">
                      Understanding your answer...
                    </p>
                  )}
                  {voiceState === VoiceInterviewState.EVALUATING && (
                    <p className="text-xs font-medium text-accent animate-pulse">
                      Evaluating your response...
                    </p>
                  )}
                  {voiceState === VoiceInterviewState.AI_SPEAKING && (
                    <p className="text-xs font-medium text-accent animate-pulse">
                      AI interviewer speaking
                    </p>
                  )}
                  {voiceState === VoiceInterviewState.AI_THINKING && (
                    <p className="text-xs font-medium text-white/60 animate-pulse">
                      AI interviewer is formulating the next question...
                    </p>
                  )}

                  <p className="sr-only" role="status" aria-live="polite">
                    {microphonePermissionLabel}
                  </p>

                  {microphoneError && (
                    <div className="flex items-center gap-2 text-xs text-red-400" role="alert">
                      <p>{microphoneError}</p>
                      <button
                        type="button"
                        onClick={() => void startListening()}
                        className="underline font-semibold hover:text-red-300"
                      >
                        Retry
                      </button>
                    </div>
                  )}
                  {audioWarning && (
                    <p className="text-xs font-medium text-amber-400" role="status">
                      {audioWarning}
                    </p>
                  )}
                  {transportError && (
                    <div className="flex items-center gap-2 text-xs text-red-400" role="alert">
                      <span>{transportError}</span>
                      <button
                        type="button"
                        onClick={retryConnection}
                        className="underline font-semibold hover:text-red-300"
                      >
                        Reconnect
                      </button>
                    </div>
                  )}

                  {import.meta.env.DEV && localTurnLatencyMs !== null && (
                    <p className="text-[11px] text-white/40">
                      Processing latency after Stop: {Math.round(localTurnLatencyMs)} ms
                    </p>
                  )}
                  {acknowledgedChunks > 0 && (
                    <p className="sr-only" aria-live="polite">
                      {acknowledgedChunks} audio {acknowledgedChunks === 1 ? 'chunk' : 'chunks'} delivered
                    </p>
                  )}
                </div>
              )}
            </div>

            {/* Right: Candidate Camera Video Card */}
            <div className="lg:col-span-5 flex justify-center lg:justify-end">
              <div className="relative w-full max-w-[480px] aspect-[4/3] rounded-3xl overflow-hidden border-2 border-white/10 bg-zinc-900 shadow-2xl flex items-center justify-center group">
                {cameraActive ? (
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full h-full object-cover scale-x-[-1]"
                  />
                ) : (
                  <div className="flex flex-col items-center justify-center gap-3 text-center p-6">
                    <div className="flex h-20 w-20 items-center justify-center rounded-full bg-white/10 text-white/80 border border-white/10 shadow-inner">
                      <User className="h-10 w-10" />
                    </div>
                    <span className="text-sm font-semibold text-white/90">
                      {session.candidate_profile?.name || 'Candidate'}
                    </span>
                    <span className="text-xs text-white/40">Camera is turned off</span>
                  </div>
                )}

                {/* Signal strength indicator */}
                <div className="absolute bottom-4 left-4 z-10 flex items-center gap-1.5 rounded-lg bg-black/60 backdrop-blur-md px-2.5 py-1 border border-white/10">
                  <Signal className="h-3.5 w-3.5 text-emerald-400" />
                  <span className="text-[10px] font-mono text-emerald-400 font-semibold">Live</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Accessible Waveform for screen reader / tests */}
        <div className="sr-only" role="img" aria-label={waveformLabel}>
          {speaking && <span className="animate-pulse" />}
        </div>

        {/* Dynamic Studio Waveform at bottom */}
        <SpeechWaveform active={speaking} mode={waveformMode} />

        {/* Floating Media Controls at bottom */}
        <div className="absolute bottom-8 z-30">
          <div className="sr-only">
            {/* Screen reader button to preserve accessibility */}
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
                  ? 'Stop and send answer'
                  : voiceState === VoiceInterviewState.AI_SPEAKING
                    ? 'AI interviewer speaking'
                    : voiceState === VoiceInterviewState.WAITING_FOR_USER
                      ? 'Start answer'
                      : voiceState === VoiceInterviewState.TRANSCRIBING
                        ? 'Understanding your answer...'
                        : voiceState === VoiceInterviewState.EVALUATING
                          ? 'Evaluating your response...'
                          : 'Ready'
              }
            >
              {voiceState === VoiceInterviewState.USER_SPEAKING
                ? 'Stop and send answer'
                : voiceState === VoiceInterviewState.AI_SPEAKING
                  ? 'AI interviewer speaking'
                  : voiceState === VoiceInterviewState.WAITING_FOR_USER
                    ? 'Start answer'
                    : voiceState === VoiceInterviewState.TRANSCRIBING
                      ? 'Understanding your answer...'
                      : voiceState === VoiceInterviewState.EVALUATING
                        ? 'Evaluating your response...'
                        : 'Ready'}
            </button>
          </div>

          <FloatingMediaControls
            microphoneActive={voiceState === VoiceInterviewState.USER_SPEAKING}
            cameraActive={cameraActive}
            captionsActive={captionsActive}
            chatActive={chatActive}
            disabled={!isConnected || isComplete}
            onToggleMicrophone={
              voiceState === VoiceInterviewState.USER_SPEAKING
                ? () => void stopListening()
                : () => void startListening()
            }
            onToggleCamera={toggleCamera}
            onToggleCaptions={() => setCaptionsActive(!captionsActive)}
            onToggleChat={() => setChatActive(!chatActive)}
          />
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

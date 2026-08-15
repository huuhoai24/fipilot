import React, { useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  AlertCircle,
  ArrowLeft,
  Bot,
  CheckCircle2,
  FileText,
  History,
  Loader2,
  Mic,
  RefreshCw,
  RotateCcw,
  UserRound,
  Wifi,
  WifiOff,
} from 'lucide-react'
import { TranscriptPreview } from '@/components/voice/TranscriptPreview'
import { VoiceMicrophoneButton } from '@/components/voice/VoiceMicrophoneButton'
import { VoiceStatusIndicator } from '@/components/voice/VoiceStatusIndicator'
import { VoiceWaveformPlaceholder } from '@/components/voice/VoiceWaveformPlaceholder'
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
  const interviewComplete = session !== null && session.current_turn === null

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
              setTransportError(event.message || 'The voice server rejected a message.')
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
          releaseMedia()
          releasePlayback()
          if (disposed) return
          setCurrentQuestionText('')
          setQuestionStreaming(false)
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

  return (
    <div className="mx-auto max-w-6xl space-y-5">
      <header className="flex flex-col gap-3 border-b border-border pb-5 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="flex items-center gap-2 text-xs font-medium uppercase text-text-faint">
            <Mic className="h-4 w-4 text-accent" />
            Voice Interview
          </div>
          <h1 className="mt-2 font-display text-2xl font-bold text-text-primary">AI Interviewer</h1>
          <p className="mt-1 text-sm text-text-muted">
            Interviewing {session.candidate_profile.name}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant={isConnected ? 'success' : connectionState === 'connecting' ? 'warning' : 'danger'}>
            {isConnected ? <Wifi className="h-3.5 w-3.5" /> : <WifiOff className="h-3.5 w-3.5" />}
            {connectionState === 'connecting' ? 'Connecting' : isConnected ? 'Realtime connected' : 'Disconnected'}
          </Badge>
          <Badge variant="accent">Question {progress.current} of {progress.total}</Badge>
          <Badge variant="default">Session {sessionId}</Badge>
        </div>
      </header>

      <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_320px]">
        <main className="space-y-5">
          <section
            className="rounded-lg border border-border bg-surface px-5 py-6 text-center sm:px-8 sm:py-8"
            aria-labelledby="current-voice-question"
          >
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-accent-soft">
              <Bot className="h-6 w-6 text-accent" aria-hidden="true" />
            </div>
            <h2 id="current-voice-question" className="mt-4 text-xs font-medium uppercase text-text-faint">
              Current Question
            </h2>
            {isComplete ? (
              <div className="mt-4">
                <CheckCircle2 className="mx-auto h-7 w-7 text-success" />
                <p className="mt-3 text-lg font-semibold text-text-primary">Interview complete</p>
                {finalReportState === 'loading' && (
                  <div className="mt-5 flex items-center justify-center gap-2 text-sm text-text-muted" role="status">
                    <Loader2 className="h-4 w-4 animate-spin text-accent" />
                    Calculating final scores
                  </div>
                )}
                {finalReport && (
                  <div className="mx-auto mt-6 grid max-w-3xl overflow-hidden rounded-lg border border-border bg-surface-raised sm:grid-cols-4">
                    {[
                      ['Overall', finalReport.overall_score],
                      ['Technical', finalReport.technical_score],
                      ['Communication', finalReport.communication_score],
                      ['Correctness', finalReport.correctness_score],
                    ].map(([label, score]) => (
                      <div
                        key={label}
                        className="border-b border-border px-4 py-4 text-left last:border-b-0 sm:border-b-0 sm:border-r sm:last:border-r-0"
                      >
                        <div className="text-xs font-medium uppercase text-text-faint">{label}</div>
                        <div className="mt-2 flex items-baseline gap-1">
                          <span className="font-display text-2xl font-bold text-text-primary">
                            {(score as number).toFixed(1)}
                          </span>
                          <span className="text-xs text-text-faint">/10</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                {finalReportState === 'error' && (
                  <div className="mx-auto mt-5 max-w-xl rounded-lg border border-danger/30 bg-danger/10 p-4 text-left">
                    <p className="text-sm text-danger" role="alert">{finalReportError}</p>
                    <Button
                      type="button"
                      size="sm"
                      variant="danger"
                      className="mt-3"
                      onClick={() => setFinalReportRetry((value) => value + 1)}
                    >
                      <RefreshCw className="h-4 w-4" />
                      Retry scores
                    </Button>
                  </div>
                )}
                <div className="mt-6 flex flex-wrap justify-center gap-2">
                  <Button
                    type="button"
                    disabled={finalReportState === 'loading'}
                    onClick={() => navigate(`/text-interview/${sessionId}/report`)}
                  >
                    <FileText className="h-4 w-4" />
                    View Final Report
                  </Button>
                  <Button type="button" variant="secondary" onClick={() => navigate('/interview-history')}>
                    <History className="h-4 w-4" />
                    Back to History
                  </Button>
                </div>
              </div>
            ) : (
              <p className="mx-auto mt-4 max-w-3xl text-lg font-medium leading-8 text-text-primary sm:text-xl">
                {questionStreaming
                  ? currentQuestionText
                  : currentQuestionText || questionText(session.current_turn)}
                {questionStreaming && (
                  <span
                    className="ml-1 inline-block h-5 w-0.5 animate-pulse bg-accent align-middle"
                    aria-hidden="true"
                  />
                )}
              </p>
            )}
          </section>

          <section className="rounded-lg border border-border bg-surface px-4 py-6 sm:px-8">
            <VoiceWaveformPlaceholder
              active={speaking}
              label={waveformLabel}
            />
            <VoiceMicrophoneButton
              state={voiceState}
              disabled={!microphoneActionable}
              onClick={
                voiceState === VoiceInterviewState.USER_SPEAKING
                  ? () => void stopListening()
                  : startListening
              }
            />
            <VoiceStatusIndicator state={voiceState} elapsedSeconds={elapsedSeconds} />
            <p
              className="text-center text-xs text-text-faint"
              role="status"
              aria-live="polite"
            >
              {microphonePermissionLabel}
            </p>
            {import.meta.env.DEV && localTurnLatencyMs !== null && (
              <p className="mt-1 text-center text-xs text-text-faint">
                Processing latency after Stop: {Math.round(localTurnLatencyMs)} ms
              </p>
            )}
            {acknowledgedChunks > 0 && (
              <p className="text-center text-xs text-text-faint" aria-live="polite">
                {acknowledgedChunks} audio {acknowledgedChunks === 1 ? 'chunk' : 'chunks'} delivered
              </p>
            )}

            {microphoneError && (
              <div
                className="mx-auto mt-3 flex max-w-xl items-start justify-between gap-3 rounded-lg border border-danger/30 bg-danger/10 p-3"
                role="alert"
              >
                <p className="text-sm leading-6 text-danger">{microphoneError}</p>
                <Button type="button" size="sm" variant="danger" onClick={() => void startListening()}>
                  <RotateCcw className="h-4 w-4" />
                  Retry
                </Button>
              </div>
            )}

            {audioWarning && (
              <div
                className="mx-auto mt-3 max-w-xl rounded-lg border border-warning/30 bg-warning/10 p-3"
                role="status"
              >
                <p className="text-sm leading-6 text-warning">{audioWarning}</p>
              </div>
            )}

            {transportError && (
              <div
                className="mx-auto mt-3 flex max-w-xl items-start justify-between gap-3 rounded-lg border border-danger/30 bg-danger/10 p-3"
                role="alert"
              >
                <p className="text-sm leading-6 text-danger">{transportError}</p>
                {connectionState !== 'connected' && (
                  <Button type="button" size="sm" variant="danger" onClick={retryConnection}>
                    <RefreshCw className="h-4 w-4" />
                    Reconnect
                  </Button>
                )}
              </div>
            )}
          </section>

          <div className="rounded-lg border border-border bg-surface p-5">
            <TranscriptPreview
              transcript={transcript}
              editable={false}
            />
          </div>
        </main>

        <aside className="space-y-5">
          <section className="rounded-lg border border-border bg-surface p-5" aria-labelledby="voice-progress-title">
            <h2 id="voice-progress-title" className="text-sm font-semibold text-text-primary">
              Interview Progress
            </h2>
            <div className="mt-4 flex items-center justify-between text-xs text-text-muted">
              <span>{session.completed_turns.length} answered</span>
              <span>{progress.percentage}%</span>
            </div>
            <div className="mt-2 h-2 overflow-hidden rounded-full bg-surface-raised">
              <div
                className="h-full bg-accent transition-[width] duration-300"
                style={{ width: `${progress.percentage}%` }}
              />
            </div>
          </section>

          <section className="rounded-lg border border-border bg-surface p-5" aria-labelledby="voice-candidate-title">
            <div className="flex items-start gap-3">
              <UserRound className="mt-0.5 h-5 w-5 shrink-0 text-accent" aria-hidden="true" />
              <div className="min-w-0">
                <h2 id="voice-candidate-title" className="break-words text-sm font-semibold text-text-primary">
                  {session.candidate_profile.name}
                </h2>
                <p className="mt-1 break-words text-xs text-text-muted">
                  {session.candidate_profile.specialization || session.candidate_profile.recent_role || 'Candidate'}
                </p>
              </div>
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              {session.candidate_profile.skills.slice(0, 6).map((skill) => (
                <Badge key={skill} variant="default">{skill}</Badge>
              ))}
            </div>
          </section>
        </aside>
      </div>
    </div>
  )
}

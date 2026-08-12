import { useCallback, useEffect, useRef, useState } from 'react'
import { api } from '@/lib/api'
import { firebaseAuth } from '@/lib/firebase'

const AUTH_SUBPROTOCOL = 'firebase-auth'
const MAX_PENDING_CHUNKS = 8
const MAX_CLIENT_CHUNK_BYTES = 256 * 1024
const MAX_SOCKET_BUFFERED_BYTES = 2 * 1024 * 1024
const CONNECTION_TIMEOUT_MS = 8_000
const TRANSCRIPTION_TIMEOUT_MS = 60_000

export const MAX_SPEECH_INPUT_SECONDS = 120

export type SpeechInputStatus =
  | 'idle'
  | 'requesting'
  | 'recording'
  | 'processing'
  | 'error'

interface UseSpeechInputOptions {
  sessionId?: string
  disabled: boolean
  onTranscript: (transcript: string) => void
  onRecordingStart?: () => void
}

interface SpeechServerEvent {
  type: 'connected' | 'state' | 'transcript_partial' | 'transcript_final' | 'error'
  value?: string
  text?: string
  code?: string
}

function stopMediaStream(stream: MediaStream | null) {
  stream?.getTracks().forEach((track) => track.stop())
}

function permissionMessage(error: unknown): string | null {
  if (
    error instanceof DOMException
    && (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError')
  ) {
    return 'Microphone access is blocked. Allow microphone access in your browser or type your answer instead.'
  }
  if (error instanceof DOMException && error.name === 'NotFoundError') {
    return 'No microphone was found. Connect one or type your answer instead.'
  }
  return null
}

export function useSpeechInput({
  sessionId,
  disabled,
  onTranscript,
  onRecordingStart,
}: UseSpeechInputOptions) {
  const [status, setStatus] = useState<SpeechInputStatus>('idle')
  const [elapsedSeconds, setElapsedSeconds] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const mountedRef = useRef(true)
  const statusRef = useRef<SpeechInputStatus>('idle')
  const streamRef = useRef<MediaStream | null>(null)
  const audioContextRef = useRef<AudioContext | null>(null)
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null)
  const workletRef = useRef<AudioWorkletNode | null>(null)
  const socketRef = useRef<WebSocket | null>(null)
  const intentionalCloseRef = useRef(false)
  const sendQueueRef = useRef<Promise<void>>(Promise.resolve())
  const pendingChunksRef = useRef(0)
  const sequenceRef = useRef(0)
  const recordingStartedAtRef = useRef(0)
  const finalReceivedRef = useRef(false)
  const transcriptionTimerRef = useRef<number | null>(null)
  const stopRecordingRef = useRef<(limitReached?: boolean) => void>(() => undefined)
  const onTranscriptRef = useRef(onTranscript)

  useEffect(() => {
    onTranscriptRef.current = onTranscript
  }, [onTranscript])

  const updateStatus = useCallback((next: SpeechInputStatus) => {
    statusRef.current = next
    if (mountedRef.current) setStatus(next)
  }, [])

  const clearTranscriptionTimer = useCallback(() => {
    if (transcriptionTimerRef.current !== null) {
      window.clearTimeout(transcriptionTimerRef.current)
      transcriptionTimerRef.current = null
    }
  }, [])

  const releaseMedia = useCallback(() => {
    if (workletRef.current) {
      workletRef.current.port.onmessage = null
      workletRef.current.disconnect()
    }
    workletRef.current = null
    sourceRef.current?.disconnect()
    sourceRef.current = null
    const audioContext = audioContextRef.current
    audioContextRef.current = null
    if (audioContext && audioContext.state !== 'closed') void audioContext.close()
    stopMediaStream(streamRef.current)
    streamRef.current = null
  }, [])

  const closeSocket = useCallback(() => {
    const socket = socketRef.current
    socketRef.current = null
    intentionalCloseRef.current = true
    if (socket && socket.readyState < WebSocket.CLOSED) socket.close()
  }, [])

  const fail = useCallback((message: string) => {
    clearTranscriptionTimer()
    releaseMedia()
    closeSocket()
    if (!mountedRef.current) return
    setError(message)
    setNotice(null)
    updateStatus('error')
  }, [clearTranscriptionTimer, closeSocket, releaseMedia, updateStatus])

  const complete = useCallback((transcript: string) => {
    const normalized = transcript.trim()
    if (!normalized) {
      fail('We could not hear enough speech. Record again or type your answer instead.')
      return
    }
    releaseMedia()
    finalReceivedRef.current = true
    onTranscriptRef.current(normalized)
    if (!mountedRef.current) return
    setError(null)
    setNotice('Transcript added. Review and edit it before sending.')
  }, [fail, releaseMedia])

  const queueAudioChunk = useCallback((payload: ArrayBuffer) => {
    if (!payload.byteLength) return
    if (
      payload.byteLength > MAX_CLIENT_CHUNK_BYTES
      || pendingChunksRef.current >= MAX_PENDING_CHUNKS
    ) {
      fail('Recording could not continue. Record again or type your answer instead.')
      return
    }
    pendingChunksRef.current += 1
    const sequence = sequenceRef.current++
    sendQueueRef.current = sendQueueRef.current
      .catch(() => undefined)
      .then(() => {
        const socket = socketRef.current
        if (!socket || socket.readyState !== WebSocket.OPEN) return
        if (socket.bufferedAmount > MAX_SOCKET_BUFFERED_BYTES) {
          throw new Error('Speech input backpressure limit reached')
        }
        socket.send(JSON.stringify({
          type: 'audio_chunk',
          sequence,
          encoding: 'pcm_s16le',
          sample_rate: 16_000,
        }))
        socket.send(payload)
      })
      .catch(() => {
        fail('Recording could not continue. Record again or type your answer instead.')
      })
      .finally(() => {
        pendingChunksRef.current = Math.max(0, pendingChunksRef.current - 1)
      })
  }, [fail])

  const stopRecording = useCallback((limitReached = false) => {
    if (statusRef.current !== 'recording') return
    updateStatus('processing')
    if (limitReached) {
      setNotice('The 2-minute recording limit was reached. Transcribing your answer now.')
    }
    releaseMedia()
    void sendQueueRef.current
      .catch(() => undefined)
      .then(() => {
        if (statusRef.current !== 'processing') return
        const socket = socketRef.current
        if (!socket || socket.readyState !== WebSocket.OPEN) {
          fail('Speech input lost its connection. Record again or type your answer instead.')
          return
        }
        socket.send(JSON.stringify({ type: 'stop_listening' }))
        clearTranscriptionTimer()
        transcriptionTimerRef.current = window.setTimeout(() => {
          fail('Transcription took too long. Record again or type your answer instead.')
        }, TRANSCRIPTION_TIMEOUT_MS)
      })
  }, [clearTranscriptionTimer, fail, releaseMedia, updateStatus])

  useEffect(() => {
    stopRecordingRef.current = stopRecording
  }, [stopRecording])

  const startRecording = useCallback(async () => {
    if (
      disabled
      || !sessionId
      || statusRef.current === 'requesting'
      || statusRef.current === 'recording'
      || statusRef.current === 'processing'
    ) return
    if (
      !navigator.mediaDevices?.getUserMedia
      || typeof AudioContext === 'undefined'
      || typeof AudioWorkletNode === 'undefined'
      || typeof WebSocket === 'undefined'
    ) {
      fail('Speech input is not supported in this browser. Type your answer instead.')
      return
    }

    setError(null)
    setNotice(null)
    setElapsedSeconds(0)
    onRecordingStart?.()
    updateStatus('requesting')
    intentionalCloseRef.current = false
    finalReceivedRef.current = false

    try {
      const user = firebaseAuth.currentUser
      const [stream, token] = await Promise.all([
        navigator.mediaDevices.getUserMedia({
          audio: {
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true,
          },
        }),
        user ? user.getIdToken() : Promise.resolve(null),
      ])
      if (!mountedRef.current) {
        stopMediaStream(stream)
        return
      }
      streamRef.current = stream

      const audioContext = new AudioContext({ sampleRate: 16_000 })
      audioContextRef.current = audioContext
      await audioContext.audioWorklet.addModule('/pcm-worklet.js')
      if (audioContext.sampleRate !== 16_000) {
        throw new Error('Unsupported microphone sample rate')
      }

      const socket = token
        ? new WebSocket(api.getSpeechInputWebSocketUrl(sessionId), [AUTH_SUBPROTOCOL, token])
        : new WebSocket(api.getSpeechInputWebSocketUrl(sessionId))
      socket.binaryType = 'arraybuffer'
      socketRef.current = socket
      await new Promise<void>((resolve, reject) => {
        const timeout = window.setTimeout(
          () => reject(new Error('Speech input connection timed out')),
          CONNECTION_TIMEOUT_MS,
        )
        socket.onopen = () => {
          window.clearTimeout(timeout)
          resolve()
        }
        socket.onerror = () => {
          window.clearTimeout(timeout)
          reject(new Error('Speech input connection failed'))
        }
        socket.onclose = () => {
          window.clearTimeout(timeout)
          reject(new Error('Speech input connection closed'))
        }
      })
      if (!mountedRef.current) return

      socket.onmessage = (message) => {
        if (typeof message.data !== 'string') return
        try {
          const event = JSON.parse(message.data) as SpeechServerEvent
          if (event.type === 'transcript_final' && typeof event.text === 'string') {
            complete(event.text)
          } else if (event.type === 'state' && event.value === 'WAITING_FOR_USER') {
            if (finalReceivedRef.current) {
              clearTranscriptionTimer()
              closeSocket()
              updateStatus('idle')
            } else if (statusRef.current === 'processing') {
              fail('We could not hear enough speech. Record again or type your answer instead.')
            }
          } else if (event.type === 'error') {
            fail('Transcription failed. Record again or type your answer instead.')
          }
        } catch {
          fail('Transcription failed. Record again or type your answer instead.')
        }
      }
      socket.onerror = () => {
        if (!intentionalCloseRef.current) {
          fail('Speech input lost its connection. Record again or type your answer instead.')
        }
      }
      socket.onclose = () => {
        if (!intentionalCloseRef.current && statusRef.current !== 'idle') {
          fail('Speech input lost its connection. Record again or type your answer instead.')
        }
      }

      const source = audioContext.createMediaStreamSource(stream)
      const worklet = new AudioWorkletNode(audioContext, 'pcm16-capture')
      sourceRef.current = source
      workletRef.current = worklet
      worklet.port.onmessage = (event: MessageEvent<ArrayBuffer>) => {
        if (event.data instanceof ArrayBuffer) queueAudioChunk(event.data)
      }
      sequenceRef.current = 0
      pendingChunksRef.current = 0
      sendQueueRef.current = Promise.resolve()
      socket.send(JSON.stringify({ type: 'start_listening' }))
      source.connect(worklet)
      worklet.connect(audioContext.destination)
      await audioContext.resume()
      recordingStartedAtRef.current = Date.now()
      updateStatus('recording')
    } catch (startError) {
      fail(
        permissionMessage(startError)
          ?? 'Speech input could not start. Check your microphone or type your answer instead.',
      )
    }
  }, [clearTranscriptionTimer, closeSocket, complete, disabled, fail, onRecordingStart, queueAudioChunk, sessionId, updateStatus])

  useEffect(() => {
    if (status !== 'recording') return
    const tick = () => {
      const elapsed = Math.min(
        MAX_SPEECH_INPUT_SECONDS,
        Math.floor((Date.now() - recordingStartedAtRef.current) / 1_000),
      )
      setElapsedSeconds(elapsed)
      if (elapsed >= MAX_SPEECH_INPUT_SECONDS) {
        stopRecordingRef.current(true)
      }
    }
    const timer = window.setInterval(tick, 250)
    return () => window.clearInterval(timer)
  }, [status])

  useEffect(() => {
    if (!disabled || statusRef.current === 'idle' || statusRef.current === 'error') return
    releaseMedia()
    closeSocket()
    clearTranscriptionTimer()
    updateStatus('idle')
  }, [clearTranscriptionTimer, closeSocket, disabled, releaseMedia, updateStatus])

  useEffect(() => () => {
    mountedRef.current = false
    clearTranscriptionTimer()
    releaseMedia()
    closeSocket()
  }, [clearTranscriptionTimer, closeSocket, releaseMedia])

  return {
    status,
    elapsedSeconds,
    error,
    notice,
    startRecording,
    stopRecording: () => stopRecording(false),
  }
}

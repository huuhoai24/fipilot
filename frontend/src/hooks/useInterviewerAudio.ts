import { useCallback, useEffect, useRef, useState } from 'react'
import { api } from '@/lib/api'
import { firebaseAuth } from '@/lib/firebase'
import { PcmAudioPlayer } from '@/lib/pcmAudioPlayer'

const AUTH_SUBPROTOCOL = 'firebase-auth'
const CONNECTION_TIMEOUT_MS = 8_000

export type InterviewerAudioRequest =
  | { key: string; turnId: string; messageKind?: never }
  | { key: string; turnId?: never; messageKind: 'closing' }

export type InterviewerAudioStatus = 'available' | 'preparing' | 'playing' | 'error'

interface UseInterviewerAudioOptions {
  sessionId?: string
  request: InterviewerAudioRequest | null
}

interface PlaybackServerEvent {
  type: 'connected' | 'tts_start' | 'audio_format' | 'tts_complete' | 'tts_cancelled' | 'error'
  sample_rate?: number
  format?: 'pcm'
}

type NavigatorWithActivation = Navigator & {
  userActivation?: { hasBeenActive: boolean }
}

export function useInterviewerAudio({
  sessionId,
  request,
}: UseInterviewerAudioOptions) {
  const [status, setStatus] = useState<InterviewerAudioStatus>('available')
  const [hasPlayed, setHasPlayed] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const mountedRef = useRef(true)
  const socketRef = useRef<WebSocket | null>(null)
  const playerRef = useRef<PcmAudioPlayer | null>(null)
  const playbackQueueRef = useRef<Promise<void>>(Promise.resolve())
  const generationRef = useRef(0)
  const autoAttemptedKeyRef = useRef<string | null>(null)
  const startPlaybackRef = useRef<(autoplay?: boolean) => Promise<void>>(async () => undefined)

  const closeResources = useCallback((notifyServer: boolean) => {
    generationRef.current += 1
    const socket = socketRef.current
    socketRef.current = null
    if (socket) {
      if (notifyServer && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: 'stop_playback' }))
      }
      if (socket.readyState < WebSocket.CLOSED) socket.close()
    }
    const player = playerRef.current
    playerRef.current = null
    playbackQueueRef.current = Promise.resolve()
    if (player) void player.close()
  }, [])

  const fail = useCallback((generation: number) => {
    if (generation !== generationRef.current) return
    closeResources(false)
    if (!mountedRef.current) return
    setStatus('error')
    setError('Audio unavailable')
  }, [closeResources])

  const startPlayback = useCallback(async (autoplay = false) => {
    if (!sessionId || !request || status === 'preparing' || status === 'playing') return
    closeResources(false)
    const generation = generationRef.current
    setError(null)
    setStatus('preparing')

    const player = new PcmAudioPlayer()
    playerRef.current = player
    try {
      await player.prepare()
    } catch {
      closeResources(false)
      if (!mountedRef.current) return
      setStatus('available')
      if (!autoplay) setError('Audio unavailable')
      return
    }
    if (!mountedRef.current || generation !== generationRef.current) return

    try {
      const user = firebaseAuth.currentUser
      const token = user ? await user.getIdToken() : null
      if (!mountedRef.current || generation !== generationRef.current) return
      const socket = token
        ? new WebSocket(
          api.getInterviewerAudioWebSocketUrl(sessionId),
          [AUTH_SUBPROTOCOL, token],
        )
        : new WebSocket(api.getInterviewerAudioWebSocketUrl(sessionId))
      socket.binaryType = 'arraybuffer'
      socketRef.current = socket
      let closedIntentionally = false
      const timeout = window.setTimeout(() => fail(generation), CONNECTION_TIMEOUT_MS)

      socket.onopen = () => window.clearTimeout(timeout)
      socket.onmessage = (message) => {
        if (generation !== generationRef.current) return
        if (message.data instanceof ArrayBuffer) {
          playbackQueueRef.current = playbackQueueRef.current
            .then(() => {
              if (generation !== generationRef.current) return
              player.enqueue(message.data)
              if (mountedRef.current) setStatus('playing')
            })
            .catch(() => fail(generation))
          return
        }
        if (typeof message.data !== 'string') return
        try {
          const event = JSON.parse(message.data) as PlaybackServerEvent
          if (event.type === 'connected') {
            socket.send(JSON.stringify(request.turnId
              ? { type: 'speak_interviewer', turn_id: request.turnId }
              : { type: 'speak_interviewer', message_kind: request.messageKind }))
          } else if (event.type === 'tts_start') {
            player.beginStream()
          } else if (
            event.type === 'audio_format'
            && typeof event.sample_rate === 'number'
            && event.format === 'pcm'
          ) {
            playbackQueueRef.current = playbackQueueRef.current
              .then(() => player.configure(event.sample_rate!, event.format!))
              .catch(() => fail(generation))
          } else if (event.type === 'tts_complete') {
            playbackQueueRef.current = playbackQueueRef.current
              .then(() => player.markStreamComplete())
              .then(() => {
                if (!mountedRef.current || generation !== generationRef.current) return
                closedIntentionally = true
                socketRef.current = null
                if (socket.readyState < WebSocket.CLOSED) socket.close()
                if (playerRef.current === player) {
                  playerRef.current = null
                  void player.close()
                }
                setHasPlayed(true)
                setStatus('available')
              })
              .catch(() => fail(generation))
          } else if (event.type === 'tts_cancelled') {
            closedIntentionally = true
            closeResources(false)
            if (mountedRef.current) {
              setHasPlayed(true)
              setStatus('available')
            }
          } else if (event.type === 'error') {
            fail(generation)
          }
        } catch {
          fail(generation)
        }
      }
      socket.onerror = () => fail(generation)
      socket.onclose = () => {
        window.clearTimeout(timeout)
        if (!closedIntentionally && generation === generationRef.current) {
          fail(generation)
        }
      }
    } catch {
      fail(generation)
    }
  }, [closeResources, fail, request, sessionId, status])

  useEffect(() => {
    startPlaybackRef.current = startPlayback
  }, [startPlayback])

  const stopPlayback = useCallback(() => {
    closeResources(true)
    if (!mountedRef.current) return
    setHasPlayed(true)
    setStatus('available')
  }, [closeResources])

  useEffect(() => {
    closeResources(true)
    setError(null)
    setHasPlayed(false)
    setStatus('available')
    if (!sessionId || !request || autoAttemptedKeyRef.current === request.key) return
    autoAttemptedKeyRef.current = request.key
    const activation = (navigator as NavigatorWithActivation).userActivation
    if (activation?.hasBeenActive) {
      void startPlaybackRef.current(true)
    }
  }, [closeResources, request?.key, sessionId])

  useEffect(() => {
    mountedRef.current = true
    return () => {
      mountedRef.current = false
      closeResources(true)
    }
  }, [closeResources])

  return {
    status,
    hasPlayed,
    error,
    startPlayback: () => startPlayback(false),
    stopPlayback,
  }
}

import React, { FormEvent, useCallback, useEffect, useRef, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { AlertTriangle, Mic, MoreHorizontal, PhoneOff, Send, WifiOff } from 'lucide-react'
import { api } from '@/lib/api'
import { useActiveSessionStore } from '@/store/useActiveSessionStore'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'
const SILENCE_AUTO_STOP_MS = 6000
const MIN_AUTO_STOP_MS = 8000

type Message = {
  id: string
  sender: string
  text: string
}

type PendingAiMessage = {
  text: string
  status?: string
  has_audio?: boolean
  revealed?: boolean
}

const normalizeMessageText = (text: string) => text.replace(/\s+/g, ' ').trim()
const getMessageKey = (sender: string, text: string) => {
  const normalized = normalizeMessageText(text)
  return normalized ? `${sender}:${normalized}` : ''
}

export function InterviewSessionPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const startSession = useActiveSessionStore((s) => s.startSession)
  const endActiveSession = useActiveSessionStore((s) => s.endSession)

  const [candidateName, setCandidateName] = useState('Bạn')
  const [role, setRole] = useState('Candidate')
  const [status, setStatus] = useState('Connecting...')
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [typedAnswer, setTypedAnswer] = useState('')
  const [isEnding, setIsEnding] = useState(false)
  const [proctorWarning, setProctorWarning] = useState<string | null>(null)
  const [proctorCounts, setProctorCounts] = useState({ tab_switch_count: 0, window_blur_count: 0 })
  const [canAnswer, setCanAnswer] = useState(false)

  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimerRef = useRef<number | null>(null)
  const shouldReconnectRef = useRef(true)
  const pendingAiRef = useRef<PendingAiMessage | null>(null)
  const revealTimerRef = useRef<number | null>(null)
  const messageSeqRef = useRef(0)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const mediaStreamRef = useRef<MediaStream | null>(null)
  const silenceTimerRef = useRef<number | null>(null)
  const recordingStartedAtRef = useRef(0)
  const lastVoiceAtRef = useRef(0)
  const audioContextRef = useRef<AudioContext | null>(null)
  const audioSourceRef = useRef<AudioBufferSourceNode | null>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const endedRef = useRef(false)
  const recentMessageKeysRef = useRef<Map<string, number>>(new Map())
  const pendingAudioMessageKeysRef = useRef<Set<string>>(new Set())
  const lastProctorEventRef = useRef(0)

  const scrollToBottom = () => {
    setTimeout(() => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 80)
  }

  const finishIfEnded = useCallback((nextStatus?: string) => {
    if (nextStatus !== 'ENDED' || !sessionId || endedRef.current) return
    endedRef.current = true
    endActiveSession(sessionId)
    window.setTimeout(() => navigate(`/history/${sessionId}`), 1800)
  }, [endActiveSession, navigate, sessionId])

  const reportProctoringViolation = useCallback((eventType: 'tab_hidden' | 'window_blur', reason: string) => {
    if (!sessionId || endedRef.current) return

    const now = Date.now()
    if (now - lastProctorEventRef.current < 1200) return
    lastProctorEventRef.current = now

    const message = eventType === 'tab_hidden'
      ? 'Cảnh báo: hệ thống phát hiện bạn vừa chuyển tab trong lúc phỏng vấn.'
      : 'Cảnh báo: hệ thống phát hiện cửa sổ phỏng vấn vừa mất focus.'

    setProctorWarning(message)
    window.setTimeout(() => setProctorWarning(null), 6000)
    setProctorCounts((prev) => ({
      tab_switch_count: prev.tab_switch_count + (eventType === 'tab_hidden' ? 1 : 0),
      window_blur_count: prev.window_blur_count + (eventType === 'window_blur' ? 1 : 0),
    }))

    api.recordProctoringEvent(sessionId, {
      event_type: eventType,
      reason,
      occurred_at: new Date().toISOString(),
      visible: document.visibilityState === 'visible',
      focus_state: document.hasFocus() ? 'focused' : 'blurred',
    })
      .then((res) => {
        const summary = res?.proctoring
        if (summary) {
          setProctorCounts({
            tab_switch_count: Number(summary.tab_switch_count || 0),
            window_blur_count: Number(summary.window_blur_count || 0),
          })
        }
      })
      .catch((error) => console.error('Failed to record proctoring event:', error))
  }, [sessionId])

  const rememberRecentMessage = useCallback((sender: string, text: string, windowMs = 8000) => {
    const key = getMessageKey(sender, text)
    if (!key) return true

    const now = Date.now()
    const lastSeenAt = recentMessageKeysRef.current.get(key)
    if (lastSeenAt && now - lastSeenAt < windowMs) return false

    recentMessageKeysRef.current.set(key, now)
    recentMessageKeysRef.current.forEach((seenAt, seenKey) => {
      if (now - seenAt > 60000) recentMessageKeysRef.current.delete(seenKey)
    })
    return true
  }, [])

  const revealAiText = useCallback((text: string, nextStatus?: string, durationMs = 1600) => {
    if (!rememberRecentMessage('AI', text)) {
      finishIfEnded(nextStatus)
      return
    }

    if (revealTimerRef.current) {
      window.clearInterval(revealTimerRef.current)
      revealTimerRef.current = null
    }

    const messageId = `ai-${Date.now()}-${messageSeqRef.current++}`
    setMessages((prev) => [...prev, { id: messageId, sender: 'AI', text: '' }])

    const cleanText = text || ''
    const totalChars = cleanText.length
    if (totalChars === 0) {
      finishIfEnded(nextStatus)
      return
    }

    const intervalMs = Math.max(18, Math.floor(durationMs / Math.max(totalChars, 1)))
    let cursor = 0
    revealTimerRef.current = window.setInterval(() => {
      cursor = Math.min(totalChars, cursor + Math.max(1, Math.ceil(totalChars / Math.max(durationMs / 55, 1))))
      setMessages((prev) => prev.map((msg, idx) => (
        msg.id === messageId ? { ...msg, text: cleanText.slice(0, cursor) } : msg
      )))
      scrollToBottom()

      if (cursor >= totalChars && revealTimerRef.current) {
        window.clearInterval(revealTimerRef.current)
        revealTimerRef.current = null
        if (nextStatus !== 'ENDED') setCanAnswer(true)
        finishIfEnded(nextStatus)
      }
    }, intervalMs)
  }, [finishIfEnded, rememberRecentMessage])

  useEffect(() => {
    if (!sessionId) return
    let cancelled = false

    api.getSession(sessionId)
      .then((session) => {
        if (cancelled) return
        setCandidateName(session.candidate_name || 'Bạn')
        setRole(session.role || 'Candidate')
        setStatus(session.status || 'Connecting...')
        if (session.proctoring) {
          setProctorCounts({
            tab_switch_count: Number(session.proctoring.tab_switch_count || 0),
            window_blur_count: Number(session.proctoring.window_blur_count || 0),
          })
        }
        const historyMessages = (session.messages || []).map((msg: any) => ({
          id: String(msg.id || `history-${messageSeqRef.current++}`),
          sender: msg.role === 'ai' ? 'AI' : (msg.sender || session.candidate_name || 'Bạn'),
          text: msg.text || '',
        }))
        const lastMessage = historyMessages[historyMessages.length - 1]
        setCanAnswer(session.status !== 'ENDED' && lastMessage?.sender === 'AI')
        const recentKeys = new Set(recentMessageKeysRef.current.keys())
        const pendingAudioKeys = new Set(pendingAudioMessageKeysRef.current)
        setMessages((prev) => {
          const existingKeys = new Set(prev.map((msg) => getMessageKey(msg.sender, msg.text)).filter(Boolean))
          const incoming = historyMessages.filter((msg: Message) => {
            const key = getMessageKey(msg.sender, msg.text)
            if (!key || existingKeys.has(key) || recentKeys.has(key) || pendingAudioKeys.has(key)) return false
            existingKeys.add(key)
            return true
          })
          return prev.length ? [...incoming, ...prev] : incoming
        })
        historyMessages.forEach((msg: Message) => rememberRecentMessage(msg.sender, msg.text, 0))
        startSession({ sessionId, candidateName: session.candidate_name || 'Candidate' })
        if (session.status === 'ENDED') {
          endedRef.current = true
        }
        scrollToBottom()
      })
      .catch(() => {
        setStatus('Session unavailable')
      })

    return () => {
      cancelled = true
    }
  }, [rememberRecentMessage, sessionId, startSession])

  useEffect(() => {
    const startVideo = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        if (videoRef.current) videoRef.current.srcObject = stream
      } catch (err) {
        console.error('Error accessing webcam', err)
      }
    }
    startVideo()

    return () => {
      const stream = videoRef.current?.srcObject as MediaStream | null
      stream?.getTracks().forEach((track) => track.stop())
    }
  }, [])

  useEffect(() => {
    if (!sessionId) return

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'hidden') {
        reportProctoringViolation('tab_hidden', 'Document visibility changed to hidden')
      }
    }

    const handleBlur = () => {
      if (document.visibilityState === 'visible') {
        reportProctoringViolation('window_blur', 'Window lost focus')
      }
    }

    document.addEventListener('visibilitychange', handleVisibilityChange)
    window.addEventListener('blur', handleBlur)
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange)
      window.removeEventListener('blur', handleBlur)
    }
  }, [reportProctoringViolation, sessionId])

  const playDecodedAudio = async (arrayBuffer: ArrayBuffer, pending: PendingAiMessage | null) => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)()
    }
    const ctx = audioContextRef.current
    if (ctx.state === 'suspended') await ctx.resume()

    try {
      const decodedData = await ctx.decodeAudioData(arrayBuffer.slice(0))
      const durationMs = Math.max(1200, decodedData.duration * 1000)

      const source = ctx.createBufferSource()
      source.buffer = decodedData
      try { audioSourceRef.current?.stop() } catch {}
      audioSourceRef.current = source
      source.connect(ctx.destination)
      source.onended = () => {
        setIsSpeaking(false)
        if (pending?.status !== 'ENDED') setCanAnswer(true)
      }
      setIsSpeaking(true)
      setCanAnswer(false)
      source.start(0)
      if (pending?.text && !pending.revealed) {
        pendingAudioMessageKeysRef.current.delete(getMessageKey('AI', pending.text))
        revealAiText(pending.text, pending.status, durationMs)
      }
    } catch (error) {
      console.error('Audio playback error:', error)
      setIsSpeaking(false)
      if (pending?.text) {
        pendingAudioMessageKeysRef.current.delete(getMessageKey('AI', pending.text))
        revealAiText(pending.text, pending.status, 1400)
      }
    }
  }

  const connectWebSocket = useCallback(() => {
    if (!sessionId || endedRef.current) return
    const existingWs = wsRef.current
    if (existingWs && (existingWs.readyState === WebSocket.OPEN || existingWs.readyState === WebSocket.CONNECTING)) return

    const ws = new WebSocket(`${WS_URL}/interview/${sessionId}`)
    wsRef.current = ws
    setStatus((prev) => prev === 'Disconnected' ? 'Reconnecting...' : 'Connecting...')

    ws.onopen = () => {
      if (wsRef.current !== ws) return
      setStatus('Connected')
    }

    ws.onmessage = async (event) => {
      if (wsRef.current !== ws) return

      if (typeof event.data === 'string') {
        let data: any
        try {
          data = JSON.parse(event.data)
        } catch (error) {
          console.error('Invalid websocket payload:', error)
          return
        }
        if (data.status) setStatus(data.status)

        if (data.sender && data.sender !== 'AI') {
          if (!rememberRecentMessage(data.sender, data.text || '')) return
          setMessages((prev) => [...prev, { id: `user-${Date.now()}-${messageSeqRef.current++}`, sender: data.sender, text: data.text || '' }])
          scrollToBottom()
          return
        }

        if (data.text) {
          setCanAnswer(false)
          if (data.retry_answer) setCanAnswer(true)
          if (data.has_audio) {
            pendingAudioMessageKeysRef.current.add(getMessageKey('AI', data.text))
            pendingAiRef.current = data
          } else {
            pendingAudioMessageKeysRef.current.delete(getMessageKey('AI', data.text))
            pendingAiRef.current = null
            revealAiText(data.text, data.status, 1400)
          }
        }
      } else {
        const pending = pendingAiRef.current
        pendingAiRef.current = null
        const arrayBuffer = await event.data.arrayBuffer()
        await playDecodedAudio(arrayBuffer, pending)
      }
    }

    ws.onclose = (event) => {
      if (wsRef.current !== ws) return
      if (event.code === 4000) return
      if (endedRef.current || !shouldReconnectRef.current) return
      setStatus('Disconnected')
      reconnectTimerRef.current = window.setTimeout(connectWebSocket, 1200)
    }

    ws.onerror = () => {
      if (wsRef.current !== ws) return
      setStatus('Connection issue')
    }
  }, [rememberRecentMessage, revealAiText, sessionId])

  useEffect(() => {
    shouldReconnectRef.current = true
    connectWebSocket()

    return () => {
      shouldReconnectRef.current = false
      if (reconnectTimerRef.current) window.clearTimeout(reconnectTimerRef.current)
      if (revealTimerRef.current) window.clearInterval(revealTimerRef.current)
      wsRef.current?.close()
      audioSourceRef.current?.stop()
      audioContextRef.current?.close()
    }
  }, [connectWebSocket])

  const stopRecording = useCallback(() => {
    if (silenceTimerRef.current) {
      window.clearInterval(silenceTimerRef.current)
      silenceTimerRef.current = null
    }
    if (mediaRecorderRef.current?.state === 'recording') {
      mediaRecorderRef.current.stop()
    }
    setIsListening(false)
  }, [])

  const startRecording = async () => {
    if (!canAnswer || isSpeaking) {
      alert('Vui lòng đợi AI mở màn hoặc hỏi xong rồi mới trả lời.')
      return
    }
    if (wsRef.current?.readyState !== WebSocket.OPEN) {
      alert('Kết nối phỏng vấn chưa sẵn sàng. Hệ thống đang thử kết nối lại.')
      return
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      })
      mediaStreamRef.current = stream

      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm'
      const recorder = new MediaRecorder(stream, { mimeType })
      mediaRecorderRef.current = recorder
      const audioChunks: BlobPart[] = []

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunks.push(event.data)
      }

      recorder.onstop = () => {
        stream.getTracks().forEach((track) => track.stop())
        const audioBlob = new Blob(audioChunks, { type: mimeType })
        if (audioBlob.size > 0 && wsRef.current?.readyState === WebSocket.OPEN) {
          setCanAnswer(false)
          wsRef.current.send(audioBlob)
        }
      }

      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext
      const ctx = new AudioCtx()
      const source = ctx.createMediaStreamSource(stream)
      const analyser = ctx.createAnalyser()
      analyser.fftSize = 512
      source.connect(analyser)
      const data = new Uint8Array(analyser.frequencyBinCount)

      recordingStartedAtRef.current = Date.now()
      lastVoiceAtRef.current = Date.now()
      silenceTimerRef.current = window.setInterval(() => {
        analyser.getByteFrequencyData(data)
        const avg = data.reduce((sum, value) => sum + value, 0) / data.length
        const now = Date.now()
        if (avg > 8) lastVoiceAtRef.current = now
        if (now - recordingStartedAtRef.current > MIN_AUTO_STOP_MS && now - lastVoiceAtRef.current > SILENCE_AUTO_STOP_MS) {
          stopRecording()
          ctx.close()
        }
      }, 400)

      recorder.start(1000)
      setIsListening(true)
    } catch (error) {
      console.error('Microphone access denied or error:', error)
      alert('Không truy cập được microphone. Bạn có thể nhập câu trả lời bằng ô text bên phải.')
    }
  }

  const toggleRecording = () => {
    if (isListening) stopRecording()
    else startRecording()
  }

  const sendTextAnswer = (event: FormEvent) => {
    event.preventDefault()
    const text = typedAnswer.trim()
    if (!text || !canAnswer || isSpeaking || wsRef.current?.readyState !== WebSocket.OPEN) return
    setCanAnswer(false)
    wsRef.current.send(JSON.stringify({ text }))
    setTypedAnswer('')
  }

  const endInterview = async () => {
    if (!sessionId || isEnding) return
    setIsEnding(true)
    setStatus('ENDING')
    endedRef.current = true
    shouldReconnectRef.current = false
    stopRecording()
    try { wsRef.current?.close() } catch {}
    try { audioSourceRef.current?.stop() } catch {}
    try {
      await api.endSession(sessionId)
      endActiveSession(sessionId)
      navigate(`/history/${sessionId}`)
    } catch (err) {
      console.error(err)
      endedRef.current = false
      shouldReconnectRef.current = true
      alert('Lỗi kết nối khi đánh giá.')
      setIsEnding(false)
    }
  }

  return (
    <div className="relative h-[calc(100vh-6rem)] w-full bg-slate-900 flex overflow-hidden font-sans rounded-[1.5rem]">
      {proctorWarning && (
        <div className="absolute left-1/2 top-16 z-30 w-[min(560px,calc(100%-2rem))] -translate-x-1/2 rounded-lg border border-amber-300/60 bg-amber-50 px-4 py-3 text-amber-900 shadow-2xl">
          <div className="flex items-start gap-3">
            <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0" />
            <div>
              <p className="text-sm font-semibold">{proctorWarning}</p>
              <p className="mt-1 text-xs">
                Số lần chuyển tab: {proctorCounts.tab_switch_count} · Mất focus cửa sổ: {proctorCounts.window_blur_count}
              </p>
            </div>
          </div>
        </div>
      )}
      <div className="absolute top-0 left-0 right-0 p-4 flex justify-between items-center z-10 text-white">
        <div className="text-sm font-medium opacity-70">
          {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} | {role} Interview
        </div>
        <div className="flex space-x-3 text-sm items-center">
          <span className={`w-2 h-2 rounded-full ${status === 'Connected' || status === 'INTERVIEWING' ? 'bg-emerald-500' : 'bg-red-500'}`} />
          <span className="opacity-70">{status}</span>
          <span className="rounded-full border border-white/15 px-2 py-0.5 text-xs opacity-80">
            Tab: {proctorCounts.tab_switch_count} · Window: {proctorCounts.window_blur_count}
          </span>
          {status === 'Disconnected' || status === 'Connection issue' ? <WifiOff className="h-4 w-4 opacity-70" /> : null}
        </div>
      </div>

      <div className="flex-grow relative bg-gray-900 rounded-[2rem] m-6 mt-12 overflow-hidden border border-gray-800 shadow-2xl flex items-center justify-center">
        <video ref={videoRef} autoPlay playsInline muted className="absolute inset-0 w-full h-full object-cover transform scale-x-[-1]" />

        <div className="absolute bottom-8 left-8 flex items-center space-x-2 bg-black/30 backdrop-blur-md px-4 py-2 rounded-full border border-white/10 shadow-lg z-10">
          <span className="text-white font-medium drop-shadow-md text-sm">{candidateName}</span>
          {isListening && (
            <span className="flex space-x-1 opacity-80">
              <span className="w-1 h-3 bg-white rounded-full animate-pulse" />
              <span className="w-1 h-4 bg-white rounded-full animate-pulse delay-75" />
              <span className="w-1 h-2 bg-white rounded-full animate-pulse delay-150" />
            </span>
          )}
        </div>

        <div className="absolute bottom-8 right-8 w-56 h-56 bg-[#2d2f33] rounded-[2rem] overflow-hidden shadow-2xl border border-gray-700 flex flex-col items-center justify-center z-10">
          <div className="w-24 h-24 rounded-full overflow-hidden border-[3px] border-gray-600 mb-3 relative bg-slate-800">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Alex&backgroundColor=b6e3f4" alt="AI Avatar" className="w-full h-full object-cover" />
            {isSpeaking && <div className="absolute inset-0 bg-indigo-500/20 animate-pulse rounded-full" />}
          </div>
          <div className="text-white font-medium text-sm flex items-center space-x-1">
            <span>Alex</span>
          </div>
          {!isSpeaking && <MoreHorizontal className="w-4 h-4 text-white/50 mt-1" />}
        </div>

        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex items-center space-x-4 z-10">
          <button
            onClick={toggleRecording}
            disabled={status === 'ENDED' || (!isListening && (!canAnswer || isSpeaking))}
            className={`flex items-center space-x-2 px-6 py-3 rounded-full text-white font-medium text-sm transition-all shadow-lg backdrop-blur-md ${
              isListening ? 'bg-red-500/90 border border-red-400' : 'bg-indigo-500/90 hover:bg-indigo-500 border border-indigo-400/50'
            }`}
          >
            <Mic className="h-4 w-4" />
            <span>{isListening ? 'Dừng và gửi' : 'Bắt đầu trả lời'}</span>
          </button>

          <button
            onClick={endInterview}
            disabled={isEnding}
            className="bg-black/40 backdrop-blur-md hover:bg-red-500/90 text-white p-3 rounded-full transition-all border border-white/10 shadow-lg disabled:opacity-50"
            title="Kết thúc phỏng vấn"
          >
            <PhoneOff className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="w-[400px] bg-white m-6 ml-0 mt-12 rounded-[2rem] shadow-xl flex flex-col overflow-hidden relative">
        <div className="p-5 flex justify-center items-center">
          <h2 className="font-semibold text-gray-800 text-sm">Live Transcript</h2>
        </div>

        <div className="flex-grow p-6 overflow-y-auto space-y-6 flex flex-col pb-32">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center text-gray-400 text-sm text-center px-4">
              Nội dung hội thoại sẽ hiển thị ở đây...
            </div>
          ) : (
            messages.map((msg, idx) => {
              const isAI = msg.sender === 'AI' || msg.sender === 'Alex'
              return (
                <div key={idx} className="flex flex-col">
                  <div className="text-xs text-gray-500 mb-1.5 ml-1">{isAI ? 'Alex' : candidateName}</div>
                  <div className={`p-4 rounded-[1.25rem] text-[15px] leading-relaxed max-w-[90%] ${
                    isAI
                      ? 'bg-[#f4f4f5] text-gray-800 self-start rounded-tl-sm'
                      : 'bg-indigo-500 text-white self-end rounded-tr-sm shadow-sm'
                  }`}>
                    <ReactMarkdown components={{
                      p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />,
                      strong: ({ node, ...props }) => <strong className="font-semibold" {...props} />,
                    }}>
                      {msg.text}
                    </ReactMarkdown>
                  </div>
                </div>
              )
            })
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={sendTextAnswer} className="absolute bottom-0 left-0 right-0 border-t border-gray-200 bg-white p-4">
          <div className="flex gap-2">
            <input
              value={typedAnswer}
              onChange={(event) => setTypedAnswer(event.target.value)}
              className="min-w-0 flex-1 rounded-full border border-gray-300 px-4 py-2 text-sm outline-none focus:border-indigo-500"
              placeholder="Nhập câu trả lời nếu không dùng mic..."
              disabled={status === 'ENDED' || !canAnswer || isSpeaking}
            />
            <button
              type="submit"
              disabled={!typedAnswer.trim() || status === 'ENDED' || !canAnswer || isSpeaking}
              className="rounded-full bg-indigo-500 p-2.5 text-white disabled:opacity-40"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

import React from 'react'
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { SpeechInterviewPage } from '@/pages/SpeechInterviewPage'
import type { V2InterviewSessionResponse } from '@/types'

const mocks = vi.hoisted(() => ({
  getSession: vi.fn(),
  generateReport: vi.fn(),
  getToken: vi.fn(),
  getWebSocketUrl: vi.fn(() => 'ws://voice.test/api/v2/voice/interview/session-1'),
}))

vi.mock('@/lib/api', () => ({
  api: {
    getV2InterviewSession: mocks.getSession,
    generateInterviewReport: mocks.generateReport,
    getVoiceInterviewWebSocketUrl: mocks.getWebSocketUrl,
  },
}))

vi.mock('@/lib/firebase', () => ({
  firebaseAuth: {
    currentUser: {
      getIdToken: mocks.getToken,
    },
  },
}))

class FakeWebSocket {
  static readonly CONNECTING = 0
  static readonly OPEN = 1
  static readonly CLOSING = 2
  static readonly CLOSED = 3
  static instances: FakeWebSocket[] = []

  readonly url: string
  readonly protocols: string[]
  readyState = FakeWebSocket.CONNECTING
  bufferedAmount = 0
  sent: Array<string | ArrayBuffer> = []
  closeCalls: Array<{ code?: number; reason?: string }> = []
  onopen: ((event: Event) => void) | null = null
  onmessage: ((event: MessageEvent) => void) | null = null
  onerror: ((event: Event) => void) | null = null
  onclose: ((event: CloseEvent) => void) | null = null

  constructor(url: string, protocols: string[]) {
    this.url = url
    this.protocols = protocols
    FakeWebSocket.instances.push(this)
  }

  send(data: string | ArrayBuffer) {
    this.sent.push(data)
  }

  close(code?: number, reason?: string) {
    this.closeCalls.push({ code, reason })
    this.readyState = FakeWebSocket.CLOSED
    this.onclose?.({ code: code ?? 1000, reason: reason ?? '' } as CloseEvent)
  }

  open() {
    this.readyState = FakeWebSocket.OPEN
    this.onopen?.(new Event('open'))
  }

  serverEvent(payload: object) {
    this.onmessage?.(new MessageEvent('message', { data: JSON.stringify(payload) }))
  }

  serverBinary(payload: ArrayBuffer) {
    this.onmessage?.(new MessageEvent('message', { data: payload }))
  }
}

class FakeAudioNode {
  connect = vi.fn()
  disconnect = vi.fn()
}

class FakeAudioWorkletNode extends FakeAudioNode {
  static instances: FakeAudioWorkletNode[] = []
  port = {
    onmessage: null as ((event: MessageEvent<ArrayBuffer>) => void) | null,
  }

  constructor() {
    super()
    FakeAudioWorkletNode.instances.push(this)
  }

  emitChunk(data: ArrayBuffer) {
    this.port.onmessage?.({ data } as MessageEvent<ArrayBuffer>)
  }
}

class FakePlaybackBuffer {
  readonly duration: number
  readonly copyToChannel = vi.fn()

  constructor(length: number, sampleRate: number) {
    this.duration = length / sampleRate
  }
}

class FakePlaybackSource extends FakeAudioNode {
  static instances: FakePlaybackSource[] = []
  buffer: FakePlaybackBuffer | null = null
  onended: (() => void) | null = null
  start = vi.fn()
  stop = vi.fn()

  constructor() {
    super()
    FakePlaybackSource.instances.push(this)
  }

  finish() {
    this.onended?.()
  }
}

class FakeAudioContext {
  static instances: FakeAudioContext[] = []
  sampleRate = 16000
  state: AudioContextState = 'suspended'
  currentTime = 0
  destination = {} as AudioDestinationNode
  source = new FakeAudioNode()
  audioWorklet = {
    addModule: vi.fn().mockResolvedValue(undefined),
  }
  close = vi.fn(async () => {
    this.state = 'closed'
  })
  resume = vi.fn(async () => {
    this.state = 'running'
  })
  createMediaStreamSource = vi.fn(() => this.source as unknown as MediaStreamAudioSourceNode)
  createBuffer = vi.fn((_channels: number, length: number, sampleRate: number) => (
    new FakePlaybackBuffer(length, sampleRate) as unknown as AudioBuffer
  ))
  createBufferSource = vi.fn(() => (
    new FakePlaybackSource() as unknown as AudioBufferSourceNode
  ))

  constructor() {
    FakeAudioContext.instances.push(this)
  }
}

const voiceSession: V2InterviewSessionResponse = {
  session_id: 'session-1',
  state: {
    candidate_profile: {
      name: 'Voice Candidate',
      skills: ['Python'],
      skill_evidence: [],
      projects: [],
      experiences: [],
      confidence: 1,
      confidence_score: 1,
    },
    interview_config: {
      mode: 'voice',
      language: 'en',
      experience_level: 'junior',
      duration_minutes: 30,
      interview_style: 'technical',
      question_count: 2,
      objective: 'Transport test',
    },
    interview_plan: {
      duration_minutes: 30,
      rounds: [],
      coverage_goals: [],
      risk_areas: [],
      planner_summary: '',
    },
    current_turn: {
      turn_id: 'turn-1',
      question: 'Explain dependency injection.',
      status: 'created',
      difficulty: 'medium',
      topic: 'FastAPI',
      expected_signal: [],
    },
    completed_turns: [],
    current_question_index: 0,
  },
}

const nextVoiceSession: V2InterviewSessionResponse = {
  ...voiceSession,
  state: {
    ...voiceSession.state,
    current_turn: {
      turn_id: 'turn-2',
      question: 'How do you test an async API?',
      status: 'created',
      difficulty: 'medium',
      topic: 'Testing',
      expected_signal: [],
    },
    completed_turns: [
      {
        ...voiceSession.state.current_turn!,
        answer: 'I built and deployed a YOLOv8 service.',
        candidate_answer: 'I built and deployed a YOLOv8 service.',
        status: 'evaluated',
      },
    ],
    current_question_index: 1,
  },
}

const completedVoiceSession: V2InterviewSessionResponse = {
  ...nextVoiceSession,
  state: {
    ...nextVoiceSession.state,
    current_turn: null,
    completed_turns: [
      ...nextVoiceSession.state.completed_turns,
      nextVoiceSession.state.current_turn!,
    ],
  },
}

function renderPage() {
  return render(
    <MemoryRouter initialEntries={['/speech-interview/session-1']}>
      <Routes>
        <Route path="/speech-interview/:sessionId" element={<SpeechInterviewPage />} />
      </Routes>
    </MemoryRouter>
  )
}

async function connectServer(): Promise<FakeWebSocket> {
  await waitFor(() => expect(FakeWebSocket.instances).toHaveLength(1))
  const socket = FakeWebSocket.instances[0]
  act(() => {
    socket.open()
    socket.serverEvent({ type: 'connected', session_id: 'session-1' })
    socket.serverEvent({ type: 'state', value: 'WAITING_FOR_USER' })
  })
  await screen.findByText('Realtime connected')
  return socket
}

describe('SpeechInterviewPage realtime transport', () => {
  const stopTrack = vi.fn()
  const stream = {
    getTracks: () => [{ stop: stopTrack }],
  } as unknown as MediaStream
  const getUserMedia = vi.fn()

  beforeEach(() => {
    FakeWebSocket.instances = []
    FakeAudioContext.instances = []
    FakeAudioWorkletNode.instances = []
    FakePlaybackSource.instances = []
    mocks.getSession.mockResolvedValue(voiceSession)
    mocks.generateReport.mockResolvedValue({ session_id: 'session-1' })
    mocks.getToken.mockResolvedValue('firebase-token')
    getUserMedia.mockResolvedValue(stream)
    stopTrack.mockClear()
    Object.defineProperty(window, 'WebSocket', {
      configurable: true,
      value: FakeWebSocket,
    })
    Object.defineProperty(globalThis, 'WebSocket', {
      configurable: true,
      value: FakeWebSocket,
    })
    Object.defineProperty(window, 'AudioContext', {
      configurable: true,
      value: FakeAudioContext,
    })
    Object.defineProperty(globalThis, 'AudioContext', {
      configurable: true,
      value: FakeAudioContext,
    })
    Object.defineProperty(window, 'AudioWorkletNode', {
      configurable: true,
      value: FakeAudioWorkletNode,
    })
    Object.defineProperty(globalThis, 'AudioWorkletNode', {
      configurable: true,
      value: FakeAudioWorkletNode,
    })
    Object.defineProperty(navigator, 'mediaDevices', {
      configurable: true,
      value: { getUserMedia },
    })
  })

  afterEach(() => {
    cleanup()
    vi.clearAllMocks()
  })

  it('records only after Start and submits only after Stop', async () => {
    renderPage()
    const socket = await connectServer()

    expect(socket.sent).toContain(JSON.stringify({ type: 'speak_question' }))
    expect(getUserMedia).not.toHaveBeenCalled()
    expect(socket.sent).not.toContain(JSON.stringify({ type: 'start_listening' }))

    fireEvent.click(screen.getByRole('button', { name: 'Start answer' }))
    await waitFor(() => expect(getUserMedia).toHaveBeenCalledWith({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
      },
    }))
    await waitFor(() => {
      expect(socket.sent).toContain(JSON.stringify({ type: 'start_listening' }))
    })
    expect(screen.getByText('Microphone access granted')).toBeInTheDocument()

    act(() => socket.serverEvent({ type: 'state', value: 'USER_SPEAKING' }))
    expect(screen.getByText('Recording your answer')).toBeInTheDocument()
    expect(
      screen
        .getByRole('img', { name: 'Your speaking waveform' })
        .querySelector('.animate-pulse')
    ).toBeInTheDocument()

    const audioPayload = new Uint8Array([1, 2, 3, 4]).buffer
    act(() => {
      FakeAudioWorkletNode.instances[0].emitChunk(audioPayload)
    })
    await waitFor(() => {
      expect(socket.sent).toContain(JSON.stringify({
        type: 'audio_chunk',
        sequence: 0,
        encoding: 'pcm_s16le',
        sample_rate: 16000,
      }))
      expect(socket.sent).toContain(audioPayload)
    })
    act(() => socket.serverEvent({ type: 'audio_ack', sequence: 0, bytes_received: 4 }))
    expect(screen.getByText('1 audio chunk delivered')).toBeInTheDocument()

    act(() => socket.serverEvent({ type: 'audio_dropped', dropped: 1 }))
    expect(screen.getByText(/Some audio was skipped/)).toBeInTheDocument()

    act(() => {
      socket.serverEvent({
        type: 'transcript_partial',
        text: 'I built a YOLO',
        language: 'en',
        confidence: 0.72,
      })
    })
    expect(screen.getByRole('textbox', { name: 'Interview answer transcript' }))
      .toHaveValue('I built a YOLO')

    expect(socket.sent).not.toContain(JSON.stringify({ type: 'stop_listening' }))
    fireEvent.click(screen.getByRole('button', { name: 'Stop and send answer' }))
    await waitFor(() => {
      expect(socket.sent).toContain(JSON.stringify({ type: 'stop_listening' }))
    })
    act(() => socket.serverEvent({ type: 'state', value: 'TRANSCRIBING' }))
    expect(screen.getAllByText('Understanding your answer...')).toHaveLength(2)
    expect(stopTrack).toHaveBeenCalled()

    act(() => {
      socket.serverEvent({
        type: 'transcript_final',
        text: 'I built a YOLOv8 detection service.',
        language: 'en',
        confidence: 0.91,
      })
      socket.serverEvent({ type: 'state', value: 'EVALUATING' })
      socket.serverEvent({ type: 'processing', stage: 'evaluation' })
    })
    const transcript = screen.getByRole('textbox', { name: 'Interview answer transcript' })
    expect(transcript).toHaveValue('I built a YOLOv8 detection service.')
    expect(transcript).toHaveAttribute('readonly')
    expect(socket.sent).not.toContainEqual(expect.stringContaining('confirm_answer'))
    expect(screen.getAllByText('Evaluating your response...')).toHaveLength(2)

    mocks.getSession.mockResolvedValueOnce(nextVoiceSession)
    act(() => socket.serverEvent({ type: 'question_start' }))
    expect(screen.queryByText('Explain dependency injection.')).not.toBeInTheDocument()

    act(() => {
      socket.serverEvent({
        type: 'question_delta',
        text: 'How do you test',
      })
    })
    expect(screen.getByText('How do you test')).toBeInTheDocument()

    act(() => {
      socket.serverEvent({
        type: 'question_delta',
        text: ' an async API?',
      })
    })
    expect(await screen.findByText('How do you test an async API?')).toBeInTheDocument()

    act(() => {
      socket.serverEvent({ type: 'tts_start' })
      socket.serverEvent({
        type: 'audio_format',
        sample_rate: 24000,
        format: 'pcm',
      })
      socket.serverBinary(new Int16Array([100, 200, 300, 400]).buffer)
      socket.serverBinary(new Int16Array([500, 600, 700, 800]).buffer)
    })
    expect(screen.getAllByText('AI interviewer speaking')).toHaveLength(2)
    expect(screen.getByRole('button', { name: 'AI interviewer speaking' })).toBeDisabled()
    expect(screen.getByRole('img', { name: 'AI speaking waveform' })).toBeInTheDocument()
    expect(screen.getByText(/Processing latency after Stop:/)).toBeInTheDocument()
    await waitFor(() => {
      expect(socket.sent).toContain(JSON.stringify({ type: 'start_barge_in' }))
    })
    await waitFor(() => expect(FakePlaybackSource.instances).toHaveLength(2))
    expect(FakePlaybackSource.instances[1].start).toHaveBeenCalledWith(4 / 24000)

    act(() => {
      socket.serverEvent({
        type: 'question_complete',
        text: 'How do you test an async API?',
      })
    })
    expect(screen.getAllByText('AI interviewer speaking')).toHaveLength(2)
    act(() => socket.serverEvent({ type: 'tts_complete' }))
    expect(screen.getAllByText('AI interviewer speaking')).toHaveLength(2)
    act(() => {
      FakePlaybackSource.instances.forEach((source) => source.finish())
    })
    await waitFor(() => {
      expect(socket.sent).toContain(JSON.stringify({ type: 'playback_complete' }))
    })
    act(() => socket.serverEvent({ type: 'state', value: 'WAITING_FOR_USER' }))
    expect(await screen.findAllByText('Ready for your answer')).toHaveLength(1)
    await waitFor(() => expect(mocks.getSession).toHaveBeenCalledTimes(2))
    expect(screen.getByRole('textbox', { name: 'Interview answer transcript' })).toHaveValue('')
  })

  it('renders interview completion after the server completes evaluation', async () => {
    renderPage()
    const socket = await connectServer()
    mocks.generateReport.mockResolvedValueOnce({
      session_id: 'session-1',
      report: {
        overall_score: 8.4,
        technical_score: 8.7,
        communication_score: 8.1,
        correctness_score: 8.3,
      },
    })

    act(() => {
      socket.serverEvent({
        type: 'transcript_final',
        text: 'My final answer.',
      })
      socket.serverEvent({ type: 'state', value: 'EVALUATING' })
      socket.serverEvent({ type: 'processing', stage: 'evaluation' })
    })
    mocks.getSession.mockResolvedValueOnce(completedVoiceSession)
    act(() => socket.serverEvent({ type: 'completed' }))

    expect(screen.getByText('Interview complete')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Ready' })).toBeDisabled()
    await waitFor(() => expect(mocks.getSession).toHaveBeenCalledTimes(2))
    expect(mocks.generateReport).toHaveBeenCalledWith('session-1')
    expect(await screen.findByText('8.4')).toBeInTheDocument()
    expect(screen.getByText('8.7')).toBeInTheDocument()
    expect(screen.getByText('8.1')).toBeInTheDocument()
    expect(screen.getByText('8.3')).toBeInTheDocument()
  })

  it('loads final scores when reopening a completed speech interview', async () => {
    mocks.getSession.mockResolvedValue(completedVoiceSession)
    mocks.generateReport.mockResolvedValueOnce({
      session_id: 'session-1',
      report: {
        overall_score: 7.9,
        technical_score: 8.2,
        communication_score: 7.6,
        correctness_score: 7.8,
      },
    })

    renderPage()

    expect(await screen.findByText('Interview complete')).toBeInTheDocument()
    expect(await screen.findByText('7.9')).toBeInTheDocument()
    expect(mocks.generateReport).toHaveBeenCalledWith('session-1')
    expect(screen.getByRole('button', { name: 'View Final Report' })).toBeEnabled()
  })

  it('cancels buffered AI audio and keeps microphone capture on barge-in', async () => {
    renderPage()
    const socket = await connectServer()

    act(() => {
      socket.serverEvent({ type: 'state', value: 'EVALUATING' })
      socket.serverEvent({ type: 'tts_start' })
      socket.serverEvent({
        type: 'audio_format',
        sample_rate: 24000,
        format: 'pcm',
      })
      socket.serverBinary(new Int16Array([100, 200, 300, 400]).buffer)
    })
    await waitFor(() => {
      expect(socket.sent).toContain(JSON.stringify({ type: 'start_barge_in' }))
      expect(FakePlaybackSource.instances).toHaveLength(1)
    })

    act(() => {
      socket.serverEvent({ type: 'tts_cancelled' })
      socket.serverEvent({ type: 'state', value: 'INTERRUPTED' })
      socket.serverEvent({ type: 'state', value: 'USER_SPEAKING' })
    })

    expect(await screen.findByText('Recording your answer')).toBeInTheDocument()
    expect(FakePlaybackSource.instances[0].stop).toHaveBeenCalled()
    expect(screen.getByRole('button', { name: 'Stop and send answer' })).toBeEnabled()
  })

  it('shows a safe permission error when microphone access is denied', async () => {
    getUserMedia.mockRejectedValueOnce(new DOMException('denied', 'NotAllowedError'))
    renderPage()
    await connectServer()

    fireEvent.click(screen.getByRole('button', { name: 'Start answer' }))
    expect(await screen.findByText(/Microphone permission was denied/)).toBeInTheDocument()
    expect(screen.getByText('Microphone access denied')).toBeInTheDocument()
  })

  it('reconnects without opening the microphone automatically', async () => {
    renderPage()
    const firstSocket = await connectServer()
    act(() => {
      firstSocket.serverEvent({
        type: 'transcript_partial',
        text: 'Partial answer before disconnect.',
      })
    })

    act(() => firstSocket.close(1006, 'Connection lost.'))
    await waitFor(
      () => expect(FakeWebSocket.instances).toHaveLength(2),
      { timeout: 2500 }
    )

    mocks.getSession.mockResolvedValueOnce(voiceSession)
    const secondSocket = FakeWebSocket.instances[1]
    act(() => {
      secondSocket.open()
      secondSocket.serverEvent({ type: 'connected', session_id: 'session-1' })
      secondSocket.serverEvent({ type: 'state', value: 'WAITING_FOR_USER' })
    })

    expect(secondSocket.sent).not.toContain(JSON.stringify({ type: 'start_listening' }))
    expect(secondSocket.sent).not.toContain(JSON.stringify({ type: 'speak_question' }))
    expect(screen.getByRole('button', { name: 'Start answer' })).toBeEnabled()
  })

  it('closes transport resources when the page unmounts', async () => {
    const view = renderPage()
    const socket = await connectServer()
    fireEvent.click(screen.getByRole('button', { name: 'Start answer' }))
    await waitFor(() => expect(FakeAudioContext.instances[0]?.state).toBe('running'))

    act(() => socket.serverEvent({ type: 'state', value: 'USER_SPEAKING' }))
    view.unmount()

    expect(stopTrack).toHaveBeenCalled()
    expect(FakeAudioContext.instances[0].close).toHaveBeenCalled()
    expect(socket.closeCalls).toContainEqual({ code: 1000, reason: 'Page closed.' })
  })
})

import React from 'react'
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { TextInterviewRoom } from '@/components/interview/TextInterviewRoom'
import { resolveInterviewerPersona } from '@/lib/interviewerPersonas'
import type { V2InterviewSessionState } from '@/types'

const boundary = vi.hoisted(() => ({
  getIdToken: vi.fn(),
  getInterviewerAudioWebSocketUrl: vi.fn(),
  getSpeechInputWebSocketUrl: vi.fn(),
}))

vi.mock('@/lib/firebase', () => ({
  firebaseAuth: { currentUser: { getIdToken: boundary.getIdToken } },
}))

vi.mock('@/lib/api', () => ({
  api: {
    getInterviewerAudioWebSocketUrl: boundary.getInterviewerAudioWebSocketUrl,
    getSpeechInputWebSocketUrl: boundary.getSpeechInputWebSocketUrl,
  },
}))

class FakeWebSocket {
  static readonly CONNECTING = 0
  static readonly OPEN = 1
  static readonly CLOSED = 3
  static instances: FakeWebSocket[] = []

  readonly sent: unknown[] = []
  readyState = FakeWebSocket.CONNECTING
  binaryType = ''
  onopen: ((event: Event) => void) | null = null
  onmessage: ((event: MessageEvent) => void) | null = null
  onerror: ((event: Event) => void) | null = null
  onclose: ((event: CloseEvent) => void) | null = null

  constructor(public readonly url: string, public readonly protocols?: string[]) {
    FakeWebSocket.instances.push(this)
  }

  send(payload: unknown) {
    this.sent.push(payload)
  }

  close() {
    this.readyState = FakeWebSocket.CLOSED
  }

  open() {
    this.readyState = FakeWebSocket.OPEN
    this.onopen?.(new Event('open'))
  }

  emitJson(payload: object) {
    this.onmessage?.(new MessageEvent('message', { data: JSON.stringify(payload) }))
  }

  emitAudio(payload = new Int16Array([100, 200, 300, 400]).buffer) {
    this.onmessage?.(new MessageEvent('message', { data: payload }))
  }
}

class FakeAudioNode {
  connect = vi.fn()
  disconnect = vi.fn()
}

class FakeAudioSource extends FakeAudioNode {
  static instances: FakeAudioSource[] = []
  buffer: AudioBuffer | null = null
  onended: (() => void) | null = null
  start = vi.fn()
  stop = vi.fn()

  constructor() {
    super()
    FakeAudioSource.instances.push(this)
  }

  finish() {
    this.onended?.()
  }
}

class FakeAudioContext {
  static instances: FakeAudioContext[] = []
  sampleRate = 16_000
  state: AudioContextState = 'suspended'
  currentTime = 0
  destination = {} as AudioDestinationNode
  audioWorklet = { addModule: vi.fn().mockResolvedValue(undefined) }
  resume = vi.fn(async () => { this.state = 'running' })
  close = vi.fn(async () => { this.state = 'closed' })
  createBuffer = vi.fn((_channels: number, length: number, sampleRate: number) => ({
    duration: length / sampleRate,
    copyToChannel: vi.fn(),
  } as unknown as AudioBuffer))
  createBufferSource = vi.fn(() => new FakeAudioSource() as unknown as AudioBufferSourceNode)
  createMediaStreamSource = vi.fn(() => new FakeAudioNode() as unknown as MediaStreamAudioSourceNode)

  constructor() {
    FakeAudioContext.instances.push(this)
  }
}

class FakeAudioWorkletNode extends FakeAudioNode {
  port = { onmessage: null as ((event: MessageEvent<ArrayBuffer>) => void) | null }
}

const stopTrack = vi.fn()
const getUserMedia = vi.fn().mockResolvedValue({
  getTracks: () => [{ stop: stopTrack }],
} as unknown as MediaStream)

const activeState: V2InterviewSessionState = {
  candidate_profile: {
    name: 'Trieu Vo',
    skills: ['FastAPI'],
    skill_evidence: [],
    projects: [],
    experiences: [],
    confidence: 0.9,
    confidence_score: 0.9,
  },
  interview_config: {
    mode: 'text',
    language: 'en',
    experience_level: 'middle',
    duration_minutes: 30,
    interview_style: 'technical',
    question_count: 3,
    objective: 'Assess backend engineering',
  },
  interview_plan: {
    duration_minutes: 30,
    rounds: [],
    coverage_goals: [],
    risk_areas: [],
    planner_summary: '',
  },
  phase: 'interviewing',
  current_turn: {
    turn_id: 'turn-current',
    question: 'How do you keep an API reliable?',
    status: 'created',
    difficulty: 'medium',
    topic: 'Reliability',
    question_type: 'follow_up',
    expected_signal: [],
  },
  completed_turns: [{
    turn_id: 'turn-complete',
    question: 'Tell me about your backend experience.',
    answer: 'Private candidate response.',
    candidate_answer: 'Private candidate response.',
    status: 'evaluated',
    difficulty: 'medium',
    topic: 'Background',
    expected_signal: [],
  }],
  current_question_index: 1,
}

function renderRoom(state = activeState, initialAnswer = '', strict = false) {
  function Harness({ roomState }: { roomState: V2InterviewSessionState }) {
    const [answer, setAnswer] = React.useState(initialAnswer)
    return (
      <TextInterviewRoom
        state={roomState}
        sessionId="session-42"
        persona={resolveInterviewerPersona('technical')}
        progress={{ current: 2, total: 3 }}
        answer={answer}
        pendingAnswer={null}
        submitting={false}
        error={null}
        onAnswerChange={setAnswer}
        onSubmit={(event) => event.preventDefault()}
        onViewReport={vi.fn()}
        onBackToHistory={vi.fn()}
      />
    )
  }
  const room = <Harness roomState={state} />
  const view = render(strict ? <React.StrictMode>{room}</React.StrictMode> : room)
  return {
    ...view,
    setState: (next: V2InterviewSessionState) => view.rerender(
      strict
        ? <React.StrictMode><Harness roomState={next} /></React.StrictMode>
        : <Harness roomState={next} />,
    ),
  }
}

async function beginPlayback() {
  fireEvent.click(screen.getByRole('button', { name: 'Play interviewer audio' }))
  await waitFor(() => expect(FakeWebSocket.instances).toHaveLength(1))
  const socket = FakeWebSocket.instances[0]
  act(() => {
    socket.open()
    socket.emitJson({ type: 'connected' })
  })
  await waitFor(() => expect(socket.sent).toContain(JSON.stringify({
    type: 'speak_interviewer',
    turn_id: 'turn-current',
  })))
  act(() => {
    socket.emitJson({ type: 'tts_start' })
    socket.emitJson({ type: 'audio_format', sample_rate: 24_000, format: 'pcm' })
    socket.emitAudio()
  })
  await waitFor(() => expect(FakeAudioSource.instances).toHaveLength(1))
  return socket
}

beforeEach(() => {
  vi.clearAllMocks()
  FakeWebSocket.instances = []
  FakeAudioSource.instances = []
  FakeAudioContext.instances = []
  boundary.getIdToken.mockResolvedValue('firebase-token')
  boundary.getInterviewerAudioWebSocketUrl.mockReturnValue(
    'ws://localhost/api/v2/voice/interview/session-42?purpose=playback',
  )
  boundary.getSpeechInputWebSocketUrl.mockReturnValue(
    'ws://localhost/api/v2/voice/interview/session-42?purpose=transcription',
  )
  vi.stubGlobal('WebSocket', FakeWebSocket)
  vi.stubGlobal('AudioContext', FakeAudioContext)
  vi.stubGlobal('AudioWorkletNode', FakeAudioWorkletNode)
  Object.defineProperty(navigator, 'mediaDevices', {
    configurable: true,
    value: { getUserMedia },
  })
  Object.defineProperty(navigator, 'userActivation', {
    configurable: true,
    value: { hasBeenActive: false, isActive: false },
  })
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe('Text Interview interviewer audio', () => {
  it('renders interviewer text before an autoplay request can finish', async () => {
    let resolveToken: (token: string) => void = () => undefined
    boundary.getIdToken.mockReturnValueOnce(new Promise((resolve) => { resolveToken = resolve }))
    Object.defineProperty(navigator, 'userActivation', {
      configurable: true,
      value: { hasBeenActive: true, isActive: false },
    })

    renderRoom()

    expect(screen.getByText('How do you keep an API reliable?')).toBeInTheDocument()
    expect(FakeWebSocket.instances).toHaveLength(0)
    resolveToken('firebase-token')
    await waitFor(() => expect(FakeWebSocket.instances).toHaveLength(1))
  })

  it('lets the candidate stop playback while audio is still preparing', async () => {
    let resolveToken: (token: string) => void = () => undefined
    boundary.getIdToken.mockReturnValueOnce(new Promise((resolve) => { resolveToken = resolve }))
    renderRoom()

    fireEvent.click(screen.getByRole('button', { name: 'Play interviewer audio' }))
    const stop = await screen.findByRole('button', { name: 'Stop interviewer audio' })
    expect(stop).toBeEnabled()
    fireEvent.click(stop)

    resolveToken('firebase-token')
    await act(async () => undefined)
    expect(FakeWebSocket.instances).toHaveLength(0)
  })

  it('plays and replays only the current interviewer dialogue', async () => {
    renderRoom()
    const firstSocket = await beginPlayback()

    expect(screen.getByRole('button', { name: 'Stop interviewer audio' })).toBeEnabled()
    expect(firstSocket.sent.join(' ')).not.toContain('Private candidate response')
    act(() => {
      firstSocket.emitJson({ type: 'tts_complete' })
      FakeAudioSource.instances[0].finish()
    })
    expect(await screen.findByRole('button', { name: 'Replay interviewer question' })).toBeEnabled()

    fireEvent.click(screen.getByRole('button', { name: 'Replay interviewer question' }))
    await waitFor(() => expect(FakeWebSocket.instances).toHaveLength(2))
    expect(firstSocket.readyState).toBe(FakeWebSocket.CLOSED)
  })

  it('keeps playback available under the application StrictMode root', async () => {
    renderRoom(activeState, '', true)

    const socket = await beginPlayback()

    expect(socket.sent).toContain(JSON.stringify({
      type: 'speak_interviewer',
      turn_id: 'turn-current',
    }))
  })

  it('stops interviewer playback before microphone recording starts', async () => {
    renderRoom()
    const playbackSocket = await beginPlayback()

    fireEvent.click(screen.getByRole('button', { name: 'Start recording' }))

    await waitFor(() => expect(getUserMedia).toHaveBeenCalledOnce())
    expect(FakeAudioSource.instances[0].stop).toHaveBeenCalledOnce()
    expect(playbackSocket.sent).toContain(JSON.stringify({ type: 'stop_playback' }))
  })

  it('keeps text answering available when interviewer audio fails', async () => {
    renderRoom(activeState, 'Typed answer remains.')
    const socket = await beginPlayback()

    act(() => socket.emitJson({ type: 'error', code: 'tts_failed', message: 'Internal model path' }))

    expect(await screen.findByText('Audio unavailable')).toBeInTheDocument()
    expect(screen.queryByText(/model path/i)).not.toBeInTheDocument()
    expect(screen.getByLabelText('Your answer')).toHaveValue('Typed answer remains.')
    expect(screen.getByLabelText('Your answer')).toBeEnabled()
  })

  it('cleans obsolete playback on a new interviewer message and on unmount', async () => {
    const view = renderRoom()
    const socket = await beginPlayback()
    const nextState = {
      ...activeState,
      current_turn: {
        ...activeState.current_turn!,
        turn_id: 'turn-next',
        question: 'Describe your retry strategy.',
      },
    }

    view.setState(nextState)

    await waitFor(() => expect(FakeAudioSource.instances[0].stop).toHaveBeenCalledOnce())
    expect(socket.readyState).toBe(FakeWebSocket.CLOSED)
    expect(screen.getByText('Describe your retry strategy.')).toBeInTheDocument()
    view.unmount()
    expect(FakeAudioContext.instances[0].close).toHaveBeenCalled()
  })

  it.each([
    ['opening', { ...activeState, phase: 'opening' as const, current_turn: { ...activeState.current_turn!, turn_id: 'opening-turn', question_type: 'opening' as const } }, { type: 'speak_interviewer', turn_id: 'opening-turn' }],
    ['follow-up', activeState, { type: 'speak_interviewer', turn_id: 'turn-current' }],
    ['closing', { ...activeState, phase: 'closing' as const, current_turn: null }, { type: 'speak_interviewer', message_kind: 'closing' }],
  ])('uses the same playback control for %s dialogue', async (_label, state, expected) => {
    renderRoom(state as V2InterviewSessionState)
    fireEvent.click(screen.getByRole('button', { name: 'Play interviewer audio' }))
    await waitFor(() => expect(FakeWebSocket.instances).toHaveLength(1))
    const socket = FakeWebSocket.instances[0]
    act(() => {
      socket.open()
      socket.emitJson({ type: 'connected' })
    })
    await waitFor(() => expect(socket.sent).toContain(JSON.stringify(expected)))
  })
})

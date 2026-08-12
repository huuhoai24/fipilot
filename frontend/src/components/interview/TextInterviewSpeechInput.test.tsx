import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { TextInterviewRoom } from '@/components/interview/TextInterviewRoom'
import { resolveInterviewerPersona } from '@/lib/interviewerPersonas'
import type { V2InterviewSessionState } from '@/types'

const boundary = vi.hoisted(() => ({
  getIdToken: vi.fn(),
  getSpeechInputWebSocketUrl: vi.fn(),
}))

vi.mock('@/lib/firebase', () => ({
  firebaseAuth: {
    currentUser: { getIdToken: boundary.getIdToken },
  },
}))

vi.mock('@/lib/api', () => ({
  api: {
    getSpeechInputWebSocketUrl: boundary.getSpeechInputWebSocketUrl,
  },
}))

class MockWebSocket {
  static readonly CONNECTING = 0
  static readonly OPEN = 1
  static readonly CLOSED = 3
  static instances: MockWebSocket[] = []

  readonly sent: unknown[] = []
  readyState = MockWebSocket.CONNECTING
  onopen: ((event: Event) => void) | null = null
  onmessage: ((event: MessageEvent) => void) | null = null
  onerror: ((event: Event) => void) | null = null
  onclose: ((event: CloseEvent) => void) | null = null

  constructor(public readonly url: string, public readonly protocols?: string[]) {
    MockWebSocket.instances.push(this)
    queueMicrotask(() => {
      this.readyState = MockWebSocket.OPEN
      this.onopen?.(new Event('open'))
    })
  }

  send(payload: unknown) {
    this.sent.push(payload)
  }

  close() {
    this.readyState = MockWebSocket.CLOSED
  }

  emitJson(payload: object) {
    this.onmessage?.(new MessageEvent('message', { data: JSON.stringify(payload) }))
  }
}

const stopTrack = vi.fn()
const disconnectSource = vi.fn()
const fakeStream = {
  getTracks: () => [{ stop: stopTrack }],
} as unknown as MediaStream

class MockAudioContext {
  readonly sampleRate = 16_000
  readonly state = 'running'
  readonly destination = {}
  readonly audioWorklet = { addModule: vi.fn().mockResolvedValue(undefined) }
  createMediaStreamSource = vi.fn(() => ({ connect: vi.fn(), disconnect: disconnectSource }))
  resume = vi.fn().mockResolvedValue(undefined)
  close = vi.fn().mockResolvedValue(undefined)
}

class MockAudioWorkletNode {
  readonly port = { onmessage: null as ((event: MessageEvent<ArrayBuffer>) => void) | null }
  connect = vi.fn()
  disconnect = vi.fn()
}

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
    turn_id: 'turn-1',
    question: 'How do you keep an API reliable?',
    status: 'created',
    difficulty: 'medium',
    topic: 'Reliability',
    expected_signal: [],
  },
  completed_turns: [],
  current_question_index: 0,
}

function renderSpeechInput(initialAnswer = '') {
  const submit = vi.fn((event: React.FormEvent<HTMLFormElement>) => event.preventDefault())

  function Harness() {
    const [answer, setAnswer] = React.useState(initialAnswer)
    return (
      <TextInterviewRoom
        state={activeState}
        sessionId="session-42"
        persona={resolveInterviewerPersona('technical')}
        progress={{ current: 1, total: 3 }}
        answer={answer}
        pendingAnswer={null}
        submitting={false}
        error={null}
        onAnswerChange={setAnswer}
        onSubmit={submit}
        onViewReport={vi.fn()}
        onBackToHistory={vi.fn()}
      />
    )
  }

  render(<Harness />)
  return { submit }
}

beforeEach(() => {
  vi.clearAllMocks()
  MockWebSocket.instances = []
  boundary.getIdToken.mockResolvedValue('firebase-token')
  boundary.getSpeechInputWebSocketUrl.mockReturnValue(
    'ws://localhost/api/v2/voice/interview/session-42?purpose=transcription',
  )
  Object.defineProperty(navigator, 'mediaDevices', {
    configurable: true,
    value: { getUserMedia: vi.fn().mockResolvedValue(fakeStream) },
  })
  vi.stubGlobal('WebSocket', MockWebSocket)
  vi.stubGlobal('AudioContext', MockAudioContext)
  vi.stubGlobal('AudioWorkletNode', MockAudioWorkletNode)
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe('TextInterviewRoom speech input', () => {
  it('records, transcribes, preserves typed text, and leaves submission to the candidate', async () => {
    const { submit } = renderSpeechInput('Typed introduction.')

    fireEvent.click(screen.getByRole('button', { name: 'Start recording' }))
    expect(await screen.findByRole('button', { name: 'Stop recording' })).toBeEnabled()
    expect(boundary.getSpeechInputWebSocketUrl).toHaveBeenCalledWith('session-42')
    expect(MockWebSocket.instances[0].protocols).toEqual(['firebase-auth', 'firebase-token'])
    expect(screen.getByRole('status', { name: 'Recording in progress' })).toHaveTextContent(
      'Recording 00:00',
    )

    fireEvent.click(screen.getByRole('button', { name: 'Stop recording' }))
    expect(await screen.findByText('Transcribing...')).toBeInTheDocument()
    expect(screen.getByLabelText('Your answer')).toHaveValue('Typed introduction.')

    MockWebSocket.instances[0].emitJson({
      type: 'transcript_final',
      text: 'Speech transcript.',
    })
    MockWebSocket.instances[0].emitJson({
      type: 'state',
      value: 'WAITING_FOR_USER',
    })

    await waitFor(() => {
      expect(screen.getByLabelText('Your answer')).toHaveValue(
        'Typed introduction. Speech transcript.',
      )
    })
    expect(submit).not.toHaveBeenCalled()
    expect(screen.getByRole('button', { name: 'Submit answer' })).toBeEnabled()

    fireEvent.change(screen.getByLabelText('Your answer'), {
      target: { value: 'Edited final answer.' },
    })
    expect(screen.getByLabelText('Your answer')).toHaveValue('Edited final answer.')
  })

  it('keeps text input available when microphone permission is blocked', async () => {
    const getUserMedia = vi.fn().mockRejectedValue(
      new DOMException('Permission denied by browser', 'NotAllowedError'),
    )
    Object.defineProperty(navigator, 'mediaDevices', {
      configurable: true,
      value: { getUserMedia },
    })
    renderSpeechInput('Typed answer remains.')

    fireEvent.click(screen.getByRole('button', { name: 'Start recording' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Microphone access is blocked. Allow microphone access in your browser or type your answer instead.',
    )
    expect(getUserMedia).toHaveBeenCalledOnce()
    expect(screen.getByLabelText('Your answer')).toBeEnabled()
    expect(screen.getByLabelText('Your answer')).toHaveValue('Typed answer remains.')
    expect(screen.getByRole('button', { name: 'Record again' })).toBeEnabled()
  })

  it('keeps the draft recoverable after a safe transcription failure', async () => {
    renderSpeechInput('Typed draft.')
    fireEvent.click(screen.getByRole('button', { name: 'Start recording' }))
    fireEvent.click(await screen.findByRole('button', { name: 'Stop recording' }))

    MockWebSocket.instances[0].emitJson({
      type: 'error',
      code: 'provider_internal_failure',
      message: 'Raw provider model failed',
    })

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Transcription failed. Record again or type your answer instead.',
    )
    expect(screen.queryByText(/provider|model failed/i)).not.toBeInTheDocument()
    expect(screen.getByLabelText('Your answer')).toHaveValue('Typed draft.')
    expect(screen.getByLabelText('Your answer')).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Record again' })).toBeEnabled()
  })

  it('stops at the documented two-minute limit and tells the candidate', async () => {
    renderSpeechInput()
    fireEvent.click(screen.getByRole('button', { name: 'Start recording' }))
    expect(await screen.findByRole('button', { name: 'Stop recording' })).toBeEnabled()

    const limitReachedAt = Date.now() + 120_000
    const dateNow = vi.spyOn(Date, 'now').mockReturnValue(limitReachedAt)
    try {
      await waitFor(() => {
        expect(screen.getByRole('status', { name: 'Transcribing answer' })).toHaveTextContent(
          'Transcribing...',
        )
      })
      expect(screen.getByText(/2-minute recording limit was reached/i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'Submit answer' })).toBeDisabled()
    } finally {
      dateNow.mockRestore()
    }
  })
})

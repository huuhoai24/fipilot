import React, { act } from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { TextInterviewPage } from '@/pages/TextInterviewPage'
import { api } from '@/lib/api'
import type { V2InterviewSessionResponse, V2InterviewSessionState } from '@/types'

vi.mock('@/lib/api', () => ({
  api: {
    checkHealth: vi.fn(),
    generateInterviewReport: vi.fn(),
    getV2InterviewSession: vi.fn(),
    prepareV2Interview: vi.fn(),
    startV2Interview: vi.fn(),
    submitV2InterviewAnswer: vi.fn(),
    uploadResume: vi.fn(),
  },
}))

function activeState(overrides: Partial<V2InterviewSessionState> = {}): V2InterviewSessionState {
  return {
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
      expected_signal: ['Private expected signal'],
    },
    completed_turns: [],
    current_question_index: 0,
    ...overrides,
  }
}

function sessionResponse(state = activeState()): V2InterviewSessionResponse {
  return {
    session_id: 'session-42',
    started_at: '2026-08-11T03:00:00Z',
    state,
  }
}

function renderActiveInterview() {
  return render(
    <MemoryRouter initialEntries={['/text-interview/session-42']}>
      <Routes>
        <Route path="/text-interview/:sessionId" element={<TextInterviewPage mode="text" />} />
      </Routes>
    </MemoryRouter>,
  )
}

beforeEach(() => {
  vi.clearAllMocks()
  window.localStorage.clear()
  vi.mocked(api.checkHealth).mockResolvedValue({ status: 'ok' })
  vi.mocked(api.getV2InterviewSession).mockResolvedValue(sessionResponse())
})

afterEach(() => {
  cleanup()
})

describe('TextInterviewPage answer interaction', () => {
  it('posts an answer once when duplicate submit events occur in the same tick', async () => {
    vi.mocked(api.submitV2InterviewAnswer).mockReturnValue(new Promise(() => undefined))
    renderActiveInterview()

    const composer = await screen.findByLabelText('Your answer')
    fireEvent.change(composer, { target: { value: 'Use bounded queues and backpressure.' } })
    const form = composer.closest('form') as HTMLFormElement

    act(() => {
      form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }))
      form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }))
    })

    expect(api.submitV2InterviewAnswer).toHaveBeenCalledTimes(1)
    expect(screen.getByText('Use bounded queues and backpressure.')).toBeInTheDocument()
    expect(screen.getByText('Sarah Nguyen is preparing the next question...')).toBeInTheDocument()
    expect(composer).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Submitting' })).toBeDisabled()
  })

  it('restores a failed answer for a safe retry without exposing internal errors', async () => {
    vi.mocked(api.submitV2InterviewAnswer)
      .mockRejectedValueOnce(new Error('LangGraph node interview_evaluator failed'))
      .mockResolvedValueOnce(sessionResponse(activeState({
        current_turn: {
          turn_id: 'turn-2',
          question: 'How would you verify recovery?',
          status: 'created',
          difficulty: 'medium',
          topic: 'Reliability',
          expected_signal: ['Private recovery signal'],
        },
        completed_turns: [{
          turn_id: 'turn-1',
          question: 'How do you keep an API reliable?',
          answer: 'Use bounded queues and backpressure.',
          status: 'evaluated',
          difficulty: 'medium',
          topic: 'Reliability',
          expected_signal: ['Private expected signal'],
        }],
        current_question_index: 1,
      })))
    renderActiveInterview()

    const composer = await screen.findByLabelText('Your answer')
    composer.focus()
    fireEvent.change(composer, { target: { value: 'Use bounded queues and backpressure.' } })
    fireEvent.click(screen.getByRole('button', { name: 'Submit answer' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Your answer could not be submitted. Please try again.',
    )
    expect(screen.queryByText(/LangGraph|interview_evaluator/i)).not.toBeInTheDocument()
    expect(composer).toHaveValue('Use bounded queues and backpressure.')
    expect(composer).toHaveFocus()

    fireEvent.click(screen.getByRole('button', { name: 'Retry answer' }))

    expect(await screen.findByText('How would you verify recovery?')).toBeInTheDocument()
    await waitFor(() => expect(composer).toHaveFocus())
    expect(composer).toHaveValue('')
    expect(screen.queryByText('Private recovery signal')).not.toBeInTheDocument()
  })
})

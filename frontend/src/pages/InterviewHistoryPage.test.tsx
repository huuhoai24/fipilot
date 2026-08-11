import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { InterviewHistoryPage } from '@/pages/InterviewHistoryPage'

const mocks = vi.hoisted(() => ({
  listInterviewSessions: vi.fn(),
}))

vi.mock('@/lib/api', () => ({
  api: {
    listInterviewSessions: mocks.listInterviewSessions,
  },
}))

function CurrentPath() {
  return <div data-testid="current-path">{useLocation().pathname}</div>
}

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

describe('InterviewHistoryPage session continuation', () => {
  it('shows a retryable connection message without exposing fetch internals', async () => {
    mocks.listInterviewSessions.mockRejectedValue(new TypeError('Failed to fetch'))

    render(
      <MemoryRouter initialEntries={['/interview-history']}>
        <InterviewHistoryPage />
      </MemoryRouter>,
    )

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'We could not load your interview history. Check your connection and try again.',
    )
    expect(screen.queryByText('Failed to fetch')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Try again' })).toBeEnabled()
  })

  it('opens an in-progress voice session in Speech Interview', async () => {
    mocks.listInterviewSessions.mockResolvedValue({
      items: [{
        session_id: 'voice-session',
        candidate_id: 'candidate-1',
        status: 'in_progress',
        mode: 'voice',
        language: 'vi',
        experience_level: 'junior',
        question_count: 5,
        answered_question_count: 2,
        overall_score: null,
        started_at: '2026-07-28T00:00:00Z',
        completed_at: null,
      }],
      total: 1,
      limit: 10,
      offset: 0,
    })

    render(
      <MemoryRouter initialEntries={['/interview-history']}>
        <Routes>
          <Route path="/interview-history" element={<InterviewHistoryPage />} />
          <Route path="*" element={<CurrentPath />} />
        </Routes>
      </MemoryRouter>,
    )

    const continueButton = await screen.findByRole('button', { name: /continue interview/i })
    fireEvent.click(continueButton)

    await waitFor(() => {
      expect(screen.getByTestId('current-path')).toHaveTextContent(
        '/speech-interview/voice-session',
      )
    })
  })

  it('keeps an in-progress text session in Text Interview', async () => {
    mocks.listInterviewSessions.mockResolvedValue({
      items: [{
        session_id: 'text-session',
        candidate_id: 'candidate-1',
        status: 'in_progress',
        mode: 'text',
        language: 'en',
        experience_level: 'middle',
        question_count: 5,
        answered_question_count: 1,
        overall_score: null,
        started_at: '2026-07-28T00:00:00Z',
        completed_at: null,
      }],
      total: 1,
      limit: 10,
      offset: 0,
    })

    render(
      <MemoryRouter initialEntries={['/interview-history']}>
        <Routes>
          <Route path="/interview-history" element={<InterviewHistoryPage />} />
          <Route path="*" element={<CurrentPath />} />
        </Routes>
      </MemoryRouter>,
    )

    fireEvent.click(
      await screen.findByRole('button', { name: /continue interview/i }),
    )

    await waitFor(() => {
      expect(screen.getByTestId('current-path')).toHaveTextContent(
        '/text-interview/text-session',
      )
    })
  })
})

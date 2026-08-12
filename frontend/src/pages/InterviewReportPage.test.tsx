import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { InterviewReportPage } from '@/pages/InterviewReportPage'
import { ApiError } from '@/lib/api'

const mocks = vi.hoisted(() => ({
  generateInterviewReport: vi.fn(),
  getInterviewReport: vi.fn(),
  getV2InterviewSession: vi.fn(),
}))

vi.mock('@/lib/api', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/lib/api')>()
  return {
    ...actual,
    api: mocks,
  }
})

const completedSession = {
  session_id: 'session-42',
  state: {
    candidate_profile: {
      candidate_id: 'candidate-7',
      name: 'Trieu Nguyen',
      skills: ['FastAPI'],
      skill_evidence: [],
      projects: [],
      experiences: [],
      confidence: 0.9,
      confidence_score: 0.9,
    },
    interview_config: {
      mode: 'text' as const,
      language: 'en' as const,
      experience_level: 'middle' as const,
      duration_minutes: 30,
      interview_style: 'technical' as const,
      question_count: 2,
      objective: 'Assess backend engineering',
    },
    interview_plan: {
      duration_minutes: 30,
      rounds: [],
      coverage_goals: [],
      risk_areas: [],
      planner_summary: '',
    },
    phase: 'closing' as const,
    current_turn: null,
    pending_turn: null,
    completed_turns: [
      {
        turn_id: 'turn-1',
        question: 'How would you keep an API reliable under load?',
        answer: 'I would add backpressure and isolate queues.',
        candidate_answer: 'I would add backpressure and isolate queues.',
        status: 'evaluated' as const,
        difficulty: 'hard' as const,
        topic: 'Reliability',
        expected_signal: ['Backpressure', 'Queue isolation'],
        evaluation: {
          turn_id: 'turn-1',
          overall_score: 8.5,
          technical_score: 9,
          communication_score: 8,
          correctness_score: 8.5,
          strengths: ['Connected overload controls to system boundaries.'],
          weaknesses: ['Did not cover retry budgets.'],
          missing_concepts: ['Retry budgets'],
          follow_up_needed: false,
          feedback: 'A strong answer; make the failure policy more explicit.',
        },
      },
      {
        turn_id: 'turn-2',
        question: {
          question: 'How do you test dependency injection?',
          language: 'en' as const,
          topic: 'FastAPI',
          difficulty: 'medium' as const,
          reasoning: '',
          expected_answer_points: ['Dependency overrides'],
          follow_up_questions: [],
        },
        answer: 'I override the provider in an integration test.',
        status: 'evaluated' as const,
        difficulty: 'medium' as const,
        topic: 'FastAPI',
        expected_signal: [],
        evaluation: null,
      },
    ],
    current_question_index: 2,
  },
}

const report = {
  id: 'report-1',
  session_id: 'session-42',
  overall_score: 8.2,
  technical_score: 8.6,
  communication_score: 7.8,
  correctness_score: 8.1,
  summary: 'You showed strong practical judgment and communicated your tradeoffs clearly.',
  strengths: ['Used concrete production examples.', 'Explained tradeoffs clearly.'],
  weaknesses: ['Make failure policies more explicit.'],
  demonstrated_skills: ['FastAPI', 'Reliability'],
  missing_skills: ['Retry strategy'],
  skill_assessments: [{
    skill: 'Reliability',
    score: 8.5,
    evidence: ['Described backpressure and queue isolation.'],
    feedback: 'Good systems thinking grounded in a real operating constraint.',
  }],
  recommendations: ['Practice naming failure thresholds and rollback criteria.'],
  learning_plan: [{
    topic: 'Retry design',
    priority: 'High',
    reason: 'The answer did not define a retry budget.',
    recommended_action: 'Write a retry policy for one production API.',
  }],
  hiring_recommendation: 'hire' as const,
  confidence_score: 0.89,
  generated_at: '2026-08-11T03:00:00Z',
}

function CurrentPath() {
  return <div data-testid="current-path">{useLocation().pathname}</div>
}

function renderPage() {
  return render(
    <MemoryRouter initialEntries={['/text-interview/session-42/report']}>
      <Routes>
        <Route path="/text-interview/:sessionId/report" element={<InterviewReportPage />} />
        <Route path="*" element={<CurrentPath />} />
      </Routes>
    </MemoryRouter>,
  )
}

beforeEach(() => {
  vi.clearAllMocks()
  mocks.getV2InterviewSession.mockResolvedValue(completedSession)
  mocks.getInterviewReport.mockResolvedValue({ session_id: 'session-42', report })
})

afterEach(() => {
  cleanup()
})

describe('InterviewReportPage coaching report', () => {
  it('renders saved aggregate scores and completed-answer coaching', async () => {
    renderPage()

    expect(await screen.findByRole('heading', { level: 1, name: 'Interview complete' })).toBeInTheDocument()
    expect(screen.getByText('8.2')).toBeInTheDocument()
    expect(screen.getByText('You showed strong practical judgment and communicated your tradeoffs clearly.')).toBeInTheDocument()
    expect(screen.getByText('Used concrete production examples.')).toBeInTheDocument()
    expect(screen.getByText('Make failure policies more explicit.')).toBeInTheDocument()
    expect(screen.getByText('Good systems thinking grounded in a real operating constraint.')).toBeInTheDocument()
    expect(screen.queryByText('Hire')).not.toBeInTheDocument()

    const firstQuestion = screen.getByRole('button', { name: /question 1.*reliability/i })
    expect(firstQuestion).toHaveAttribute('aria-expanded', 'true')
    expect(firstQuestion).toHaveAttribute('aria-controls', 'question-review-turn-1')
    expect(screen.getByRole('region', { name: /question 1.*reliability/i })).toBeInTheDocument()
    expect(screen.getByText('How would you keep an API reliable under load?')).toBeInTheDocument()
    expect(screen.getByText('I would add backpressure and isolate queues.')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'What the interviewer was looking for' })).toBeInTheDocument()
    expect(screen.getByText('Backpressure')).toBeInTheDocument()
    expect(screen.getByText('A strong answer; make the failure policy more explicit.')).toBeInTheDocument()

    const secondQuestion = screen.getByRole('button', { name: /question 2.*fastapi/i })
    expect(secondQuestion).toHaveAttribute('aria-expanded', 'false')
    secondQuestion.focus()
    expect(secondQuestion).toHaveFocus()
    fireEvent.click(secondQuestion)
    expect(secondQuestion).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByText('Dependency overrides')).toBeInTheDocument()
    expect(screen.getByText('No detailed evaluation was saved for this answer.')).toBeInTheDocument()
  })

  it('reframes harsh legacy wording as specific practice coaching without changing scores', async () => {
    mocks.getInterviewReport.mockResolvedValue({
      session_id: 'session-42',
      report: {
        ...report,
        overall_score: 2.1,
        summary: 'You may have exaggerated your experience. This creates a major concern about authenticity.',
        weaknesses: ['You may be dishonest about the project depth.'],
      },
    })

    renderPage()

    expect(await screen.findByText('2.1')).toBeInTheDocument()
    expect(screen.queryByText(/exaggerated|dishonest|authenticity/i)).not.toBeInTheDocument()
    expect(screen.getByText(/did not demonstrate the experience described in your CV/i)).toBeInTheDocument()
    expect(screen.getByText(/did not provide enough detail to support the experience described/i)).toBeInTheDocument()
  })

  it('keeps long summaries and detailed learning data available through disclosure', async () => {
    mocks.getInterviewReport.mockResolvedValue({
      session_id: 'session-42',
      report: {
        ...report,
        summary: 'First coaching point. Second coaching point. Third coaching point. Fourth coaching point. Fifth coaching point.',
        recommendations: [
          'Practice action one.',
          'Practice action two.',
          'Practice action three.',
          'Practice action four.',
          'Practice action five.',
          'Practice action six.',
        ],
      },
    })

    renderPage()

    expect((await screen.findAllByText(/First coaching point.*Third coaching point/))[0]).toBeInTheDocument()
    expect(screen.getByText('Read full coaching summary')).toBeInTheDocument()
    expect(screen.getByText('View learning plan details')).toBeInTheDocument()
    expect(screen.getByText('Practice action five.')).toBeInTheDocument()
    expect(screen.queryByText('Practice action six.')).not.toBeInTheDocument()
  })

  it('keeps the report unavailable while an interview is active', async () => {
    mocks.getV2InterviewSession.mockResolvedValue({
      ...completedSession,
      state: {
        ...completedSession.state,
        phase: 'interviewing',
        current_question_index: 1,
        current_turn: {
          turn_id: 'turn-active',
          question: 'Private active question',
          status: 'created',
          difficulty: 'medium',
          topic: 'Private topic',
          expected_signal: ['Private expected signal'],
        },
      },
    })

    renderPage()

    expect(await screen.findByRole('heading', { name: 'Interview still in progress' })).toBeInTheDocument()
    expect(screen.queryByText('Private expected signal')).not.toBeInTheDocument()
    expect(mocks.getInterviewReport).not.toHaveBeenCalled()
    expect(mocks.generateInterviewReport).not.toHaveBeenCalled()

    fireEvent.click(screen.getByRole('button', { name: 'Continue interview' }))
    await waitFor(() => {
      expect(screen.getByTestId('current-path')).toHaveTextContent('/text-interview/session-42')
    })
  })

  it('handles missing optional coaching detail without breaking the report', async () => {
    mocks.getV2InterviewSession.mockResolvedValue({
      ...completedSession,
      state: { ...completedSession.state, completed_turns: [] },
    })
    mocks.getInterviewReport.mockResolvedValue({
      session_id: 'session-42',
      report: {
        ...report,
        strengths: undefined,
        weaknesses: undefined,
        demonstrated_skills: undefined,
        missing_skills: undefined,
        skill_assessments: undefined,
        recommendations: undefined,
        learning_plan: undefined,
      },
    })

    renderPage()

    expect(await screen.findByRole('heading', { level: 1, name: 'Interview complete' })).toBeInTheDocument()
    expect(screen.getByText('No strengths were included in this report.')).toBeInTheDocument()
    expect(screen.getByText('No development areas were included in this report.')).toBeInTheDocument()
    expect(screen.getByText('No question-level review is available for this interview.')).toBeInTheDocument()
    expect(screen.getByText('No additional recommendations were included.')).toBeInTheDocument()
  })

  it('generates a report only after the completed session is confirmed', async () => {
    mocks.getInterviewReport.mockRejectedValue(new ApiError('Not found', 404))
    mocks.generateInterviewReport.mockResolvedValue({ session_id: 'session-42', report })

    renderPage()

    expect(await screen.findByRole('heading', { level: 1, name: 'Interview complete' })).toBeInTheDocument()
    expect(mocks.getV2InterviewSession).toHaveBeenCalledWith('session-42')
    expect(mocks.generateInterviewReport).toHaveBeenCalledWith('session-42')
  })
})

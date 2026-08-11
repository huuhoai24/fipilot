import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { TextInterviewPage } from '@/pages/TextInterviewPage'
import { api } from '@/lib/api'

vi.mock('@/lib/api', () => ({
  api: {
    checkHealth: vi.fn(),
    getV2InterviewSession: vi.fn(),
    uploadResume: vi.fn(),
    prepareV2Interview: vi.fn(),
    generateInterviewReport: vi.fn(),
    startV2Interview: vi.fn(),
    submitV2InterviewAnswer: vi.fn(),
  },
}))

beforeEach(() => {
  vi.clearAllMocks()
  window.localStorage.clear()
  vi.mocked(api.checkHealth).mockResolvedValue({ status: 'ok' })
  vi.mocked(api.prepareV2Interview).mockResolvedValue({
    status: 'ready',
    profile_version: 1,
  })
})

afterEach(() => {
  cleanup()
})

describe('TextInterviewPage interview mode', () => {
  it('presents an active session as a focused conversation without evaluation data', async () => {
    vi.mocked(api.submitV2InterviewAnswer).mockReturnValue(new Promise(() => undefined))
    vi.mocked(api.getV2InterviewSession).mockResolvedValue({
      session_id: 'session-42',
      state: {
        candidate_profile: {
          name: 'Tran Thi B',
          recent_role: 'Platform engineer',
          skills: ['Kubernetes'],
          skill_evidence: [],
          projects: [],
          experiences: [],
          confidence: 0.92,
          confidence_score: 0.92,
        },
        interview_config: {
          mode: 'text',
          language: 'en',
          experience_level: 'senior',
          duration_minutes: 30,
          interview_style: 'technical',
          question_count: 4,
          objective: 'Assess system design',
        },
        interview_plan: {
          duration_minutes: 30,
          rounds: [],
          coverage_goals: [],
          risk_areas: [],
          planner_summary: '',
        },
        completed_turns: [{
          turn_id: 'turn-1',
          question: 'Tell me about a system you scaled.',
          answer: 'I separated the write path and added backpressure.',
          candidate_answer: 'I separated the write path and added backpressure.',
          status: 'evaluated',
          difficulty: 'medium',
          topic: 'System design',
          expected_signal: ['Backpressure and queue isolation'],
          evaluation: {
            turn_id: 'turn-1',
            overall_score: 8,
            technical_score: 8,
            communication_score: 8,
            correctness_score: 8,
            strengths: ['Private strength'],
            weaknesses: ['Private weakness'],
            missing_concepts: [],
            follow_up_needed: false,
            feedback: 'Private evaluator feedback',
          },
        }],
        current_turn: {
          turn_id: 'turn-2',
          question: {
            question: 'How did you detect and recover from overload?',
            language: 'en',
            topic: 'Reliability',
            difficulty: 'hard',
            reasoning: 'Private hidden AI reasoning',
            expected_answer_points: ['Expected private signal'],
            follow_up_questions: [],
          },
          status: 'created',
          difficulty: 'hard',
          topic: 'Reliability',
          expected_signal: ['Expected private signal'],
        },
        current_question_index: 1,
      },
    })

    render(
      <MemoryRouter initialEntries={['/text-interview/session-42']}>
        <Routes>
          <Route path="/text-interview/:sessionId" element={<TextInterviewPage mode="text" />} />
        </Routes>
      </MemoryRouter>,
    )

    expect(await screen.findByRole('heading', { level: 1, name: 'Sarah Nguyen' })).toBeInTheDocument()
    expect(screen.getByText('AI Virtual Interviewer')).toBeInTheDocument()
    expect(screen.getByText('Tell me about a system you scaled.')).toBeInTheDocument()
    expect(screen.getByText('I separated the write path and added backpressure.')).toBeInTheDocument()
    expect(screen.getByText('How did you detect and recover from overload?')).toBeInTheDocument()
    expect(screen.getByText('Question 2 of 4')).toBeInTheDocument()
    const answerComposer = screen.getByLabelText('Your answer')
    expect(answerComposer).toBeInTheDocument()

    expect(screen.queryByText('Expected private signal')).not.toBeInTheDocument()
    expect(screen.queryByText('Private evaluator feedback')).not.toBeInTheDocument()
    expect(screen.queryByText('Private strength')).not.toBeInTheDocument()
    expect(screen.queryByText('Private weakness')).not.toBeInTheDocument()
    expect(screen.queryByText('Private hidden AI reasoning')).not.toBeInTheDocument()
    expect(screen.queryByText('Kubernetes')).not.toBeInTheDocument()
    expect(screen.queryByText('session-42')).not.toBeInTheDocument()
    expect(screen.queryByText('8/10')).not.toBeInTheDocument()

    fireEvent.change(answerComposer, { target: { value: 'I used queue-depth alarms and a circuit breaker.' } })
    fireEvent.keyDown(answerComposer, { key: 'Enter', ctrlKey: true })

    await waitFor(() => {
      expect(api.submitV2InterviewAnswer).toHaveBeenCalledWith(
        'session-42',
        'I used queue-depth alarms and a circuit breaker.',
      )
    })
    expect(screen.getByText('I used queue-depth alarms and a circuit breaker.')).toBeInTheDocument()
    expect(
      screen.getByText('Sarah Nguyen is preparing the next question...'),
    ).toBeInTheDocument()
    expect(screen.queryByText(/evaluating|score|retrieval/i)).not.toBeInTheDocument()
  })

  it('allows Question Count to be cleared and replaced while editing', () => {
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    const questionCount = screen.getByLabelText('Question Count')

    fireEvent.change(questionCount, { target: { value: '' } })

    expect(questionCount).toHaveValue(null)

    fireEvent.change(questionCount, { target: { value: '7' } })

    expect(questionCount).toHaveValue(7)
  })

  it('allows Duration to be cleared and replaced while editing', () => {
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )
    const duration = screen.getByLabelText('Duration')

    fireEvent.change(duration, { target: { value: '' } })
    expect(duration).toHaveValue(null)

    fireEvent.change(duration, { target: { value: '25' } })
    expect(duration).toHaveValue(25)
  })

  it('blocks an empty numeric setting and submits a valid replacement value', async () => {
    vi.mocked(api.uploadResume).mockResolvedValue({
      candidate_id: 'candidate-1',
      confidence_score: 0.92,
      profile: {
        name: 'Tran Thi B',
        skills: ['FastAPI'],
        skill_evidence: [],
        projects: [],
        experiences: [],
        confidence: 0.92,
        confidence_score: 0.92,
      },
    })
    vi.mocked(api.startV2Interview).mockReturnValue(new Promise(() => undefined))
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )
    const file = new File(['resume'], 'resume.pdf', { type: 'application/pdf' })
    fireEvent.change(screen.getByLabelText('Resume file'), { target: { files: [file] } })
    fireEvent.click(screen.getByRole('button', { name: 'Upload and Analyze' }))
    await screen.findByText('Candidate profile is ready. Review it before starting the interview.')

    const questionCount = screen.getByLabelText('Question Count')
    const startButton = screen.getByRole('button', { name: 'Start' })
    fireEvent.change(questionCount, { target: { value: '' } })

    expect(questionCount).toHaveAttribute('aria-invalid', 'true')
    expect(startButton).toBeDisabled()
    fireEvent.submit(startButton.closest('form') as HTMLFormElement)
    expect(api.startV2Interview).not.toHaveBeenCalled()

    fireEvent.change(questionCount, { target: { value: '7' } })
    expect(startButton).toBeEnabled()
    fireEvent.click(startButton)

    await waitFor(() => {
      expect(api.startV2Interview).toHaveBeenCalledWith(
        expect.objectContaining({
          interview_config: expect.objectContaining({ question_count: 7 }),
        }),
      )
    })
  })

  it('persists valid interview settings across a page remount', () => {
    const firstRender = render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    fireEvent.change(screen.getByLabelText('Language'), { target: { value: 'en' } })
    fireEvent.change(screen.getByLabelText('Experience Level'), { target: { value: 'senior' } })
    fireEvent.change(screen.getByLabelText('Interview Style'), { target: { value: 'mixed' } })
    fireEvent.change(screen.getByLabelText('Duration'), { target: { value: '45' } })
    fireEvent.change(screen.getByLabelText('Question Count'), { target: { value: '7' } })
    fireEvent.change(screen.getByLabelText('Objective'), { target: { value: 'Assess system design' } })
    firstRender.unmount()

    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    expect(screen.getByLabelText('Language')).toHaveValue('en')
    expect(screen.getByLabelText('Experience Level')).toHaveValue('senior')
    expect(screen.getByLabelText('Interview Style')).toHaveValue('mixed')
    expect(screen.getByLabelText('Duration')).toHaveValue(45)
    expect(screen.getByLabelText('Question Count')).toHaveValue(7)
    expect(screen.getByLabelText('Objective')).toHaveValue('Assess system design')
    expect(window.localStorage.getItem('ai-interview:text-settings:v1')).not.toBeNull()
  })

  it('ignores malformed persisted interview settings', () => {
    window.localStorage.setItem('ai-interview:text-settings:v1', JSON.stringify({
      language: 'invalid',
      durationMinutes: 'forever',
      questionCount: 0,
      objective: 42,
    }))

    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    expect(screen.getByLabelText('Language')).toHaveValue('vi')
    expect(screen.getByLabelText('Duration')).toHaveValue(30)
    expect(screen.getByLabelText('Question Count')).toHaveValue(10)
    expect(screen.getByLabelText('Objective')).toHaveValue(
      'Evaluate technical knowledge and practical experience',
    )
  })

  it('clears selected resume state when the file input is cleared', () => {
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )
    const fileInput = screen.getByLabelText('Resume file')
    const uploadButton = screen.getByRole('button', { name: 'Upload and Analyze' })
    const file = new File(['resume'], 'resume.pdf', { type: 'application/pdf' })

    fireEvent.change(fileInput, { target: { files: [file] } })
    expect(uploadButton).toBeEnabled()

    fireEvent.change(fileInput, { target: { files: [] } })
    expect(uploadButton).toBeDisabled()
  })

  it('removes an analyzed resume and its stale candidate profile together', async () => {
    vi.mocked(api.uploadResume).mockResolvedValue({
      candidate_id: 'candidate-1',
      confidence_score: 0.92,
      profile: {
        name: 'Tran Thi B',
        skills: ['FastAPI'],
        skill_evidence: [],
        projects: [],
        experiences: [],
        confidence: 0.92,
        confidence_score: 0.92,
      },
    })
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )
    const fileInput = screen.getByLabelText('Resume file') as HTMLInputElement
    const file = new File(['resume'], 'resume.pdf', { type: 'application/pdf' })

    fireEvent.change(fileInput, { target: { files: [file] } })
    fireEvent.click(screen.getByRole('button', { name: 'Upload and Analyze' }))
    await screen.findByText('Candidate profile is ready. Review it before starting the interview.')

    fireEvent.click(screen.getByRole('button', { name: 'Remove resume' }))

    expect(fileInput.value).toBe('')
    expect(screen.queryByText('Extracted Candidate Profile')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Upload and Analyze' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Start' })).toBeDisabled()
  })

  it('checks backend health and reports an unavailable service specifically', async () => {
    vi.mocked(api.checkHealth).mockRejectedValue(
      Object.assign(new Error('Request failed'), { category: 'BACKEND_UNREACHABLE' }),
    )

    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Backend service is unavailable. Please check the API connection.',
    )
    expect(api.checkHealth).toHaveBeenCalledOnce()
  })

  it('classifies a resume upload authentication failure', async () => {
    vi.mocked(api.uploadResume).mockRejectedValue(
      Object.assign(new Error('Request failed'), { category: 'AUTH_FAILURE' }),
    )
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )
    const file = new File(['resume'], 'resume.pdf', { type: 'application/pdf' })

    fireEvent.change(screen.getByLabelText('Resume file'), { target: { files: [file] } })
    fireEvent.click(screen.getByRole('button', { name: 'Upload and Analyze' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Your session could not be verified. Please sign in again.',
    )
    expect(screen.getByRole('button', { name: 'Upload and Analyze' })).toBeEnabled()
  })

  it('keeps the page heading and session summary in sync when the route mode changes', () => {
    const { rerender } = render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    expect(screen.getByRole('heading', { level: 1, name: 'Text Interview' })).toBeInTheDocument()
    expect(screen.getByText('Text', { selector: 'span' })).toBeInTheDocument()
    expect(screen.getByLabelText('Language')).toBeInTheDocument()
    expect(screen.queryByText('Set up my interview')).not.toBeInTheDocument()

    rerender(
      <MemoryRouter>
        <TextInterviewPage mode="voice" />
      </MemoryRouter>,
    )

    expect(screen.getByRole('heading', { level: 1, name: 'Speech Interview' })).toBeInTheDocument()
    expect(screen.getByText('Speech', { selector: 'span' })).toBeInTheDocument()
    expect(screen.queryByText('Choose Interview Mode')).not.toBeInTheDocument()
  })

  it('prepares the first question after resume analysis for both interview modes', async () => {
    vi.mocked(api.uploadResume).mockResolvedValue({
      candidate_id: 'candidate-1',
      confidence_score: 0.92,
      profile: {
        name: 'Tran Thi B',
        skills: ['FastAPI'],
        skill_evidence: [],
        projects: [],
        experiences: [],
        confidence: 0.92,
        confidence_score: 0.92,
      },
    })
    vi.mocked(api.prepareV2Interview).mockResolvedValue({
      status: 'ready',
      profile_version: 1,
    })
    const { unmount } = render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )
    const file = new File(['resume'], 'resume.pdf', { type: 'application/pdf' })

    fireEvent.change(screen.getByLabelText('Resume file'), {
      target: { files: [file] },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Upload and Analyze' }))

    await waitFor(() => {
      expect(api.prepareV2Interview).toHaveBeenCalledWith(
        expect.objectContaining({
          candidate_id: 'candidate-1',
          interview_config: expect.objectContaining({ mode: 'text' }),
        }),
      )
    }, { timeout: 2500 })

    unmount()
    render(
      <MemoryRouter>
        <TextInterviewPage mode="voice" />
      </MemoryRouter>,
    )
    fireEvent.change(screen.getByLabelText('Resume file'), {
      target: { files: [file] },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Upload and Analyze' }))

    await waitFor(() => {
      expect(api.prepareV2Interview).toHaveBeenCalledWith(
        expect.objectContaining({
          candidate_id: 'candidate-1',
          interview_config: expect.objectContaining({ mode: 'voice' }),
        }),
      )
    }, { timeout: 2500 })
  })

  it('shows a non-resume rejection without rendering an extracted profile', async () => {
    vi.mocked(api.uploadResume).mockRejectedValue(
      new Error(
        'This document does not appear to be a resume. Upload a CV or resume that summarizes your experience, skills, and education.',
      ),
    )
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )
    const report = new File(
      ['capstone report'],
      'AI_Interview_Platform_Capstone_Report.docx',
      {
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      },
    )

    fireEvent.change(screen.getByLabelText('Resume file'), {
      target: { files: [report] },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Upload and Analyze' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'This document does not appear to be a resume.',
    )
    expect(screen.getByRole('button', { name: 'Upload and Analyze' })).toBeEnabled()
    expect(screen.queryByText('Extracted Candidate Profile')).not.toBeInTheDocument()
    expect(api.prepareV2Interview).not.toHaveBeenCalled()
  })

  it('shows an informative preparation workspace while start is pending', async () => {
    vi.mocked(api.uploadResume).mockResolvedValue({
      candidate_id: 'candidate-1',
      confidence_score: 0.92,
      profile: {
        name: 'Tran Thi B',
        skills: ['FastAPI'],
        skill_evidence: [],
        projects: [],
        experiences: [],
        confidence: 0.92,
        confidence_score: 0.92,
      },
    })
    vi.mocked(api.startV2Interview).mockReturnValue(new Promise(() => undefined))
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )
    const file = new File(['resume'], 'resume.pdf', { type: 'application/pdf' })

    fireEvent.change(screen.getByLabelText('Resume file'), {
      target: { files: [file] },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Upload and Analyze' }))
    await screen.findByText('Candidate profile is ready. Review it before starting the interview.')
    fireEvent.click(screen.getByRole('button', { name: 'Start' }))

    expect(
      await screen.findByRole('heading', {
        level: 1,
        name: 'Preparing your text interview',
      }),
    ).toBeInTheDocument()
    expect(screen.getByText('Tran Thi B')).toBeInTheDocument()
    expect(screen.getByText('Building the interview plan and first question')).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent('Preparing')
  })
})

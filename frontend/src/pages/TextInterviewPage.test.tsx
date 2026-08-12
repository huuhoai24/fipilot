import React, { act } from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom'
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

const basicUploadResponse = {
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
}

async function uploadBasicProfile() {
  const file = new File(['resume'], 'resume.pdf', { type: 'application/pdf' })
  fireEvent.change(screen.getByLabelText('Resume file'), { target: { files: [file] } })
  fireEvent.click(screen.getByRole('button', { name: 'Upload and analyze' }))
  await screen.findByText('Profile ready. Review the summary and choose your interview settings.')
}

function CurrentPath() {
  return <div data-testid="current-path">{useLocation().pathname}</div>
}

beforeEach(() => {
  vi.clearAllMocks()
  window.localStorage.clear()
  vi.mocked(api.checkHealth).mockResolvedValue({ status: 'ok' })
  vi.mocked(api.uploadResume).mockResolvedValue(basicUploadResponse)
  vi.mocked(api.prepareV2Interview).mockResolvedValue({
    status: 'ready',
    profile_version: 1,
  })
})

afterEach(() => {
  cleanup()
})

describe('TextInterviewPage interview mode', () => {
  it('guides a fresh resume through clear analysis stages without internal terminology', async () => {
    vi.mocked(api.uploadResume).mockReturnValue(new Promise(() => undefined))
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    expect(screen.getByRole('heading', { level: 1, name: 'Prepare your interview' })).toBeInTheDocument()
    const file = new File(['resume'], 'resume.pdf', { type: 'application/pdf' })
    fireEvent.change(screen.getByLabelText('Resume file'), { target: { files: [file] } })
    fireEvent.click(screen.getByRole('button', { name: 'Upload and analyze' }))

    expect(await screen.findByText('Reading your CV')).toBeInTheDocument()
    expect(screen.getByText('Understanding your experience and projects')).toBeInTheDocument()
    expect(screen.getByText('Building your interview profile')).toBeInTheDocument()
    expect(screen.queryByText(/\b(gemini|llm|rag|embeddings?|agents?)\b/i)).not.toBeInTheDocument()
  })

  it('shows a concise cached profile result and the four primary interview settings', async () => {
    vi.mocked(api.uploadResume).mockResolvedValue({
      candidate_id: 'candidate-1',
      confidence_score: 0.92,
      profile: {
        name: 'Vo Quang Trieu',
        specialization: 'AI / Machine Learning',
        years_experience: 2,
        skills: ['Python', 'PyTorch', 'LangGraph', 'RAG', 'CUDA', 'FastAPI'],
        skill_evidence: [],
        projects: [
          { name: 'Vision API', description: '', technologies: [], role: '' },
          { name: 'Agent platform', description: '', technologies: [], role: '' },
          { name: 'Search service', description: '', technologies: [], role: '' },
        ],
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

    const file = new File(['resume'], 'resume.pdf', { type: 'application/pdf' })
    fireEvent.change(screen.getByLabelText('Resume file'), { target: { files: [file] } })
    fireEvent.click(screen.getByRole('button', { name: 'Upload and analyze' }))

    expect(await screen.findByRole('heading', { name: 'Vo Quang Trieu' })).toBeInTheDocument()
    expect(screen.getByText('AI / Machine Learning')).toBeInTheDocument()
    expect(screen.getByText('2 years')).toBeInTheDocument()
    expect(screen.getByText('3 detected')).toBeInTheDocument()
    expect(screen.getByText('Python · PyTorch · LangGraph · RAG · CUDA')).toBeInTheDocument()
    expect(screen.queryByText('FastAPI')).not.toBeInTheDocument()
    expect(screen.queryByText(/confidence/i)).not.toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'View full profile' })).toHaveAttribute(
      'href',
      '/candidate-profile/candidate-1',
    )
    expect(screen.getByLabelText('Interview type')).toBeInTheDocument()
    expect(screen.getByLabelText('Difficulty')).toBeInTheDocument()
    expect(screen.getByLabelText('Language')).toBeInTheDocument()
    expect(screen.getByLabelText('Number of questions')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Start Interview' })).toBeEnabled()
  })

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

  it('allows Number of questions to be cleared and replaced while editing', async () => {
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    await uploadBasicProfile()
    const questionCount = screen.getByLabelText('Number of questions')

    fireEvent.change(questionCount, { target: { value: '' } })

    expect(questionCount).toHaveValue(null)

    fireEvent.change(questionCount, { target: { value: '7' } })

    expect(questionCount).toHaveValue(7)
  })

  it('allows Duration to be cleared and replaced while editing', async () => {
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )
    await uploadBasicProfile()
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
    fireEvent.click(screen.getByRole('button', { name: 'Upload and analyze' }))
    await screen.findByText('Profile ready. Review the summary and choose your interview settings.')

    const questionCount = screen.getByLabelText('Number of questions')
    const startButton = screen.getByRole('button', { name: 'Start Interview' })
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

  it('starts only one session when duplicate form submissions occur in the same tick', async () => {
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
    fireEvent.click(screen.getByRole('button', { name: 'Upload and analyze' }))
    await screen.findByText('Profile ready. Review the summary and choose your interview settings.')

    const startForm = screen.getByRole('button', { name: 'Start Interview' }).closest('form') as HTMLFormElement
    act(() => {
      startForm.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }))
      startForm.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }))
    })

    expect(api.startV2Interview).toHaveBeenCalledTimes(1)
  })

  it('persists valid interview settings across a page remount', async () => {
    const firstRender = render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    await uploadBasicProfile()
    fireEvent.change(screen.getByLabelText('Language'), { target: { value: 'en' } })
    fireEvent.change(screen.getByLabelText('Difficulty'), { target: { value: 'senior' } })
    fireEvent.change(screen.getByLabelText('Interview type'), { target: { value: 'mixed' } })
    fireEvent.change(screen.getByLabelText('Duration'), { target: { value: '45' } })
    fireEvent.change(screen.getByLabelText('Number of questions'), { target: { value: '7' } })
    fireEvent.change(screen.getByLabelText('Objective'), { target: { value: 'Assess system design' } })
    firstRender.unmount()

    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    await uploadBasicProfile()
    expect(screen.getByLabelText('Language')).toHaveValue('en')
    expect(screen.getByLabelText('Difficulty')).toHaveValue('senior')
    expect(screen.getByLabelText('Interview type')).toHaveValue('mixed')
    expect(screen.getByLabelText('Duration')).toHaveValue(45)
    expect(screen.getByLabelText('Number of questions')).toHaveValue(7)
    expect(screen.getByLabelText('Objective')).toHaveValue('Assess system design')
    expect(window.localStorage.getItem('ai-interview:text-settings:v1')).not.toBeNull()
  })

  it('ignores malformed persisted interview settings', async () => {
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

    await uploadBasicProfile()
    expect(screen.getByLabelText('Language')).toHaveValue('vi')
    expect(screen.getByLabelText('Duration')).toHaveValue(30)
    expect(screen.getByLabelText('Number of questions')).toHaveValue(10)
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
    const file = new File(['resume'], 'resume.pdf', { type: 'application/pdf' })

    fireEvent.change(fileInput, { target: { files: [file] } })
    const uploadButton = screen.getByRole('button', { name: 'Upload and analyze' })
    expect(uploadButton).toBeEnabled()

    fireEvent.change(fileInput, { target: { files: [] } })
    expect(screen.queryByRole('button', { name: 'Upload and analyze' })).not.toBeInTheDocument()
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
    fireEvent.click(screen.getByRole('button', { name: 'Upload and analyze' }))
    await screen.findByText('Profile ready. Review the summary and choose your interview settings.')

    fireEvent.click(screen.getByRole('button', { name: 'Choose another CV' }))

    expect(fileInput.value).toBe('')
    expect(screen.queryByRole('heading', { name: 'Tran Thi B' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Upload and analyze' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Start Interview' })).not.toBeInTheDocument()
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
      'FiPilot is temporarily unavailable. Please try again.',
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
    fireEvent.click(screen.getByRole('button', { name: 'Upload and analyze' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Your session could not be verified. Please sign in again.',
    )
    expect(screen.getByRole('button', { name: 'Try analysis again' })).toBeEnabled()
  })

  it('keeps the guided setup copy in sync when the route mode changes', () => {
    const { rerender } = render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    expect(screen.getByRole('heading', { level: 1, name: 'Prepare your interview' })).toBeInTheDocument()
    expect(screen.getByText(/start a text interview/i)).toBeInTheDocument()
    expect(screen.queryByLabelText('Language')).not.toBeInTheDocument()

    rerender(
      <MemoryRouter>
        <TextInterviewPage mode="voice" />
      </MemoryRouter>,
    )

    expect(screen.getByRole('heading', { level: 1, name: 'Prepare your interview' })).toBeInTheDocument()
    expect(screen.getByText(/start a speech interview/i)).toBeInTheDocument()
  })

  it('prepares the reusable interview blueprint after resume analysis for both modes', async () => {
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
    fireEvent.click(screen.getByRole('button', { name: 'Upload and analyze' }))

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
    fireEvent.click(screen.getByRole('button', { name: 'Upload and analyze' }))

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
    fireEvent.click(screen.getByRole('button', { name: 'Upload and analyze' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'This document does not appear to be a resume.',
    )
    expect(screen.getByRole('button', { name: 'Try analysis again' })).toBeEnabled()
    expect(screen.queryByRole('heading', { name: 'Tran Thi B' })).not.toBeInTheDocument()
    expect(api.prepareV2Interview).not.toHaveBeenCalled()
  })

  it('transitions directly into the Interview Room when preparation succeeds', async () => {
    vi.mocked(api.startV2Interview).mockResolvedValue({
      session_id: 'session-ready',
      started_at: '2026-08-11T03:00:00Z',
      state: {
        candidate_profile: basicUploadResponse.profile,
        interview_config: {
          mode: 'text',
          language: 'vi',
          experience_level: 'junior',
          duration_minutes: 30,
          interview_style: 'technical',
          question_count: 10,
          objective: 'Evaluate technical knowledge and practical experience',
        },
        interview_plan: {
          duration_minutes: 30,
          rounds: [],
          coverage_goals: [],
          risk_areas: [],
          planner_summary: '',
        },
        phase: 'interviewing',
        completed_turns: [],
        current_turn: {
          turn_id: 'turn-1',
          question: 'Tell me about your recent work.',
          status: 'created',
          difficulty: 'medium',
          topic: 'Background',
          expected_signal: [],
        },
        pending_turn: null,
        current_question_index: 0,
      },
    })
    render(
      <MemoryRouter initialEntries={['/text-interview']}>
        <Routes>
          <Route path="/text-interview" element={<TextInterviewPage mode="text" />} />
          <Route path="*" element={<CurrentPath />} />
        </Routes>
      </MemoryRouter>,
    )

    await uploadBasicProfile()
    fireEvent.click(screen.getByRole('button', { name: 'Start Interview' }))

    await waitFor(() => {
      expect(screen.getByTestId('current-path')).toHaveTextContent('/text-interview/session-ready')
    })
  })

  it('keeps preparation failures concise and allows the user to retry', async () => {
    vi.mocked(api.startV2Interview).mockRejectedValueOnce(
      Object.assign(new Error('model provider timeout'), { category: 'SERVER_ERROR' }),
    )
    render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    await uploadBasicProfile()
    fireEvent.click(screen.getByRole('button', { name: 'Start Interview' }))

    const preparationError = await screen.findByRole('alert')
    expect(preparationError).toHaveTextContent(
      'The interview could not be started. Please try again.',
    )
    expect(preparationError).not.toHaveTextContent(/provider|model|langgraph|api/i)

    vi.mocked(api.startV2Interview).mockReturnValue(new Promise(() => undefined))
    fireEvent.click(screen.getByRole('button', { name: 'Start Interview' }))
    expect(api.startV2Interview).toHaveBeenCalledTimes(2)
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
    fireEvent.click(screen.getByRole('button', { name: 'Upload and analyze' }))
    await screen.findByText('Profile ready. Review the summary and choose your interview settings.')
    fireEvent.click(screen.getByRole('button', { name: 'Start Interview' }))

    expect(
      await screen.findByRole('heading', {
        level: 1,
        name: 'Preparing your interview',
      }),
    ).toBeInTheDocument()
    expect(screen.getByText('Tran Thi B')).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent('Preparing interview topics')
    expect(screen.getByText('Preparing the first question')).toBeInTheDocument()
    expect(screen.getByText('Sarah Nguyen')).toBeInTheDocument()
    expect(screen.getByText('AI Virtual Interviewer')).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent('Preparing')
  })
})

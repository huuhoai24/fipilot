import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { TextInterviewPage } from '@/pages/TextInterviewPage'
import { api } from '@/lib/api'

vi.mock('@/lib/api', () => ({
  api: {
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
  vi.mocked(api.prepareV2Interview).mockResolvedValue({
    status: 'ready',
    profile_version: 1,
  })
})

afterEach(() => {
  cleanup()
})

describe('TextInterviewPage interview mode', () => {
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

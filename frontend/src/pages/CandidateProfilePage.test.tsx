import React from 'react'
import { cleanup, render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { CandidateProfilePage } from '@/pages/CandidateProfilePage'
import { ApiError } from '@/lib/api'

const mocks = vi.hoisted(() => ({
  getCandidateProfile: vi.fn(),
}))

vi.mock('@/lib/api', () => ({
  ApiError: class MockApiError extends Error {
    constructor(
      message: string,
      public readonly status: number,
    ) {
      super(message)
    }
  },
  api: {
    getCandidateProfile: mocks.getCandidateProfile,
  },
}))

afterEach(() => {
  cleanup()
  vi.clearAllMocks()
})

describe('CandidateProfilePage', () => {
  it('loads and displays the owned saved profile in the approved section order', async () => {
    mocks.getCandidateProfile.mockResolvedValue({
      etag: '"1"',
      readiness: {
        is_ready: true,
        issues: [],
      },
      profile: {
        candidate_id: 'candidate-7',
        profile_version: 1,
        name: 'Nguyễn Minh Anh',
        years_experience: 1.5,
        recent_role: 'Backend Engineering Intern',
        specialization: 'Backend systems',
        skills: ['Python', 'FastAPI'],
        skill_evidence: [
          {
            skill: 'FastAPI',
            evidence: ['Built authenticated interview APIs.'],
            source_section: 'Projects',
          },
        ],
        projects: [
          {
            name: 'Campus Interview Practice API',
            description: 'Created interview sessions for university students.',
            technologies: ['Python', 'FastAPI'],
          },
        ],
        experiences: [],
        education: [
          {
            institution: 'Ho Chi Minh City University of Technology',
            degree: 'Bachelor of Engineering',
            field_of_study: 'Computer Science',
          },
        ],
        confidence: 0.82,
        confidence_score: 0.82,
      },
    })

    render(
      <MemoryRouter initialEntries={['/candidate-profile/candidate-7']}>
        <Routes>
          <Route
            path="/candidate-profile/:candidateId"
            element={<CandidateProfilePage />}
          />
        </Routes>
      </MemoryRouter>,
    )

    expect(
      await screen.findByRole('heading', { level: 1, name: 'Candidate Profile' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { name: 'Interview ready' }),
    ).toBeInTheDocument()
    expect(
      screen.queryByRole('button', { name: /Start (text|speech) interview/ }),
    ).not.toBeInTheDocument()
    expect(mocks.getCandidateProfile).toHaveBeenCalledWith('candidate-7')

    const sectionHeadings = screen
      .getAllByRole('heading', { level: 2 })
      .map((heading) => heading.textContent)
    expect(sectionHeadings.slice(-5)).toEqual([
      'Identity and current role',
      'Skills and skill evidence',
      'Projects',
      'Work experience',
      'Education',
    ])
    expect(screen.getByText('Nguyễn Minh Anh')).toBeInTheDocument()
    expect(screen.getByText('Campus Interview Practice API')).toBeInTheDocument()
    expect(screen.queryByText(/Resume source:/)).not.toBeInTheDocument()
    expect(
      screen.getByText('Ho Chi Minh City University of Technology'),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        'No work experience is saved. Students and interns can still prepare from skills, projects, or education.',
      ),
    ).toBeInTheDocument()
  })

  it('keeps legacy education readable without inventing structured fields', async () => {
    mocks.getCandidateProfile.mockResolvedValue({
      etag: '"1"',
      readiness: {
        is_ready: false,
        issues: [
          {
            code: 'missing_interviewable_evidence',
            origin: 'interview_readiness',
            field_path: 'skill_evidence',
          },
        ],
      },
      profile: {
        candidate_id: 'candidate-legacy',
        profile_version: 1,
        name: 'Lê Thu Hà',
        skills: ['Python'],
        skill_evidence: [],
        projects: [],
        experiences: [],
        education:
          'B.Eng. Computer Science, Ho Chi Minh City University of Technology, expected 2026.',
        confidence: 0.71,
        confidence_score: 0.71,
      },
    })

    render(
      <MemoryRouter initialEntries={['/candidate-profile/candidate-legacy']}>
        <Routes>
          <Route
            path="/candidate-profile/:candidateId"
            element={<CandidateProfilePage />}
          />
        </Routes>
      </MemoryRouter>,
    )

    expect(await screen.findByText('Legacy education')).toBeInTheDocument()
    expect(
      screen.getByText(
        'B.Eng. Computer Science, Ho Chi Minh City University of Technology, expected 2026.',
      ),
    ).toBeInTheDocument()
    expect(screen.queryByText('Institution not provided')).not.toBeInTheDocument()
  })

  it('offers the resume task when the owned profile cannot be found', async () => {
    mocks.getCandidateProfile.mockRejectedValue(
      new ApiError('Candidate Profile not found.', 404),
    )

    render(
      <MemoryRouter initialEntries={['/candidate-profile/missing']}>
        <Routes>
          <Route
            path="/candidate-profile/:candidateId"
            element={<CandidateProfilePage />}
          />
        </Routes>
      </MemoryRouter>,
    )

    expect(
      await screen.findByRole('heading', {
        level: 1,
        name: 'Candidate Profile not found',
      }),
    ).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Choose resume' })).toHaveAttribute(
      'href',
      '/text-interview',
    )
  })

  it('shows backend readiness issues and focuses the related saved field', async () => {
    mocks.getCandidateProfile.mockResolvedValue({
      etag: '"1"',
      readiness: {
        is_ready: false,
        issues: [
          {
            code: 'fallback_name',
            origin: 'interview_readiness',
            field_path: 'name',
          },
          {
            code: 'missing_skills',
            origin: 'interview_readiness',
            field_path: 'skills',
          },
          {
            code: 'missing_interviewable_evidence',
            origin: 'interview_readiness',
            field_path: 'skill_evidence',
          },
        ],
      },
      profile: {
        candidate_id: 'candidate-incomplete',
        profile_version: 1,
        name: 'Candidate',
        skills: [],
        skill_evidence: [],
        projects: [],
        experiences: [],
        education: null,
        confidence: 0.5,
        confidence_score: 0.5,
      },
    })

    render(
      <MemoryRouter initialEntries={['/candidate-profile/candidate-incomplete']}>
        <Routes>
          <Route
            path="/candidate-profile/:candidateId"
            element={<CandidateProfilePage />}
          />
        </Routes>
      </MemoryRouter>,
    )

    expect(
      await screen.findByRole('heading', { name: 'Complete your profile' }),
    ).toBeInTheDocument()
    expect(
      screen.getAllByText('Replace “Candidate” with your full name.'),
    ).toHaveLength(1)

    screen
      .getByRole('link', {
        name: 'Replace “Candidate” with your full name.',
      })
      .click()

    expect(document.activeElement).toBe(
      document.getElementById('profile-field-name'),
    )
  })

  it('focuses the exact saved nested entry for a validity issue', async () => {
    mocks.getCandidateProfile.mockResolvedValue({
      etag: '"1"',
      readiness: {
        is_ready: false,
        issues: [
          {
            code: 'empty_nested_entry',
            origin: 'profile_validity',
            field_path: 'projects.0',
          },
        ],
      },
      profile: {
        candidate_id: 'candidate-invalid-project',
        profile_version: 1,
        name: 'Nguyễn Minh Anh',
        skills: ['Python'],
        skill_evidence: [],
        projects: [
          {
            name: '',
            description: '',
            technologies: [],
          },
        ],
        experiences: [],
        education: null,
        confidence: 0.5,
        confidence_score: 0.5,
      },
    })

    render(
      <MemoryRouter
        initialEntries={['/candidate-profile/candidate-invalid-project']}
      >
        <Routes>
          <Route
            path="/candidate-profile/:candidateId"
            element={<CandidateProfilePage />}
          />
        </Routes>
      </MemoryRouter>,
    )

    const issueLink = await screen.findByRole('link', {
      name: 'Complete or remove this entry.',
    })
    issueLink.click()

    expect(document.activeElement).toBe(
      document.getElementById('profile-field-projects-0'),
    )
  })

  it('announces loading and gives an expired session a sign-in recovery action', async () => {
    let rejectLoad: ((reason?: unknown) => void) | undefined
    mocks.getCandidateProfile.mockReturnValue(
      new Promise((_resolve, reject) => {
        rejectLoad = reject
      }),
    )

    render(
      <MemoryRouter initialEntries={['/candidate-profile/candidate-7']}>
        <Routes>
          <Route
            path="/candidate-profile/:candidateId"
            element={<CandidateProfilePage />}
          />
        </Routes>
      </MemoryRouter>,
    )

    expect(screen.getByRole('status')).toHaveTextContent(
      'Loading Candidate Profile',
    )
    rejectLoad?.(new ApiError('Authentication expired.', 401))

    expect(
      await screen.findByRole('heading', { name: 'Sign in to continue' }),
    ).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Sign in again' })).toHaveAttribute(
      'href',
      '/',
    )
  })

  it('keeps a service failure actionable with an explicit retry', async () => {
    mocks.getCandidateProfile.mockRejectedValue(
      new ApiError('Profile service is temporarily unavailable.', 503),
    )

    render(
      <MemoryRouter initialEntries={['/candidate-profile/candidate-7']}>
        <Routes>
          <Route
            path="/candidate-profile/:candidateId"
            element={<CandidateProfilePage />}
          />
        </Routes>
      </MemoryRouter>,
    )

    expect(
      await screen.findByText('Profile service is temporarily unavailable.'),
    ).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Try again' })).toBeInTheDocument()
  })
})

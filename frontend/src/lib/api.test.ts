import { afterEach, describe, expect, it, vi } from 'vitest'

const mocks = vi.hoisted(() => ({
  getIdToken: vi.fn(),
}))

vi.mock('@/lib/firebase', () => ({
  firebaseAuth: {
    currentUser: {
      getIdToken: mocks.getIdToken,
    },
  },
}))

import { api } from '@/lib/api'

afterEach(() => {
  vi.unstubAllGlobals()
  vi.clearAllMocks()
})

describe('Candidate Profile API adapter', () => {
  it('loads the owned profile with Firebase authentication and an encoded resource path', async () => {
    mocks.getIdToken.mockResolvedValue('firebase-token')
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: new Headers({ ETag: '"1"' }),
      json: async () => ({
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
          candidate_id: 'candidate/7',
          profile_version: 1,
          name: 'Nguyễn Minh Anh',
          skills: ['Python'],
          skill_evidence: [],
          projects: [],
          experiences: [],
          confidence: 0.8,
          confidence_score: 0.8,
        },
      }),
    })
    vi.stubGlobal('fetch', fetchMock)

    const response = await api.getCandidateProfile('candidate/7')

    expect(response.profile.name).toBe('Nguyễn Minh Anh')
    expect(response.profile.candidate_id).toBe('candidate/7')
    expect(response.readiness).toEqual({
      is_ready: false,
      issues: [
        {
          code: 'missing_interviewable_evidence',
          origin: 'interview_readiness',
          field_path: 'skill_evidence',
        },
      ],
    })
    expect(response.etag).toBe('"1"')
    expect(fetchMock).toHaveBeenCalledOnce()
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit]
    expect(new URL(url).pathname).toBe(
      '/api/v2/candidates/candidate%2F7/profile',
    )
    expect(new Headers(init.headers).get('Authorization')).toBe(
      'Bearer firebase-token',
    )
  })

  it('preserves a structured API error code, message, and issues', async () => {
    mocks.getIdToken.mockResolvedValue('firebase-token')
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      status: 404,
      headers: new Headers(),
      json: async () => ({
        error: {
          code: 'candidate_profile_not_found',
          message: 'Candidate Profile not found.',
          retryable: false,
          issues: [{ code: 'missing_name', path: ['name'] }],
        },
      }),
    }))

    const request = api.getCandidateProfile('missing')

    await expect(request).rejects.toMatchObject({
      message: 'Candidate Profile not found.',
      status: 404,
      code: 'candidate_profile_not_found',
      issues: [{ code: 'missing_name', path: ['name'] }],
    })
  })

  it('refreshes Firebase authentication once and retains the response ETag', async () => {
    mocks.getIdToken
      .mockResolvedValueOnce('expired-token')
      .mockResolvedValueOnce('refreshed-token')
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: false,
        status: 401,
        headers: new Headers(),
        json: async () => ({}),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        headers: new Headers({ ETag: '"2"' }),
        json: async () => ({
          readiness: {
            is_ready: true,
            issues: [],
          },
          profile: {
            candidate_id: 'candidate-7',
            profile_version: 2,
            name: 'Nguyễn Minh Anh',
            skills: ['Python'],
            skill_evidence: [],
            projects: [],
            experiences: [],
            confidence: 0.8,
            confidence_score: 0.8,
          },
        }),
      })
    vi.stubGlobal('fetch', fetchMock)

    const result = await api.getCandidateProfile('candidate-7')

    expect(result.etag).toBe('"2"')
    expect(mocks.getIdToken).toHaveBeenNthCalledWith(1, false)
    expect(mocks.getIdToken).toHaveBeenNthCalledWith(2, true)
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })
})

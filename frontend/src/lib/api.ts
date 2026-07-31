import type {
  CandidateProfileReadResult,
  CandidateProfileResponse,
  InterviewHistoryResponse,
  InterviewMode,
  InterviewReportResponse,
  ResumeUploadResponse,
  V2InterviewPreparationResponse,
  V2InterviewSessionResponse,
} from '@/types'
import { firebaseAuth } from '@/lib/firebase'

const configuredApiUrl = import.meta.env.VITE_API_BASE_URL
const API_ROOT_URL = configuredApiUrl
  ? configuredApiUrl.replace(/\/api\/?$/, '').replace(/\/$/, '')
  : import.meta.env.DEV
    ? 'http://127.0.0.1:8000'
    : ''

function voiceWebSocketUrl(sessionId: string | number): string {
  const baseUrl = API_ROOT_URL || window.location.origin
  const url = new URL(`/api/v2/voice/interview/${encodeURIComponent(String(sessionId))}`, baseUrl)
  url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
  return url.toString()
}

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly code = 'request_failed',
    public readonly issues: unknown[] = [],
    public readonly retryable = false,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

async function requestJsonResponse<T>(
  url: string,
  init?: RequestInit,
  refreshedToken = false
): Promise<{ data: T; response: Response }> {
  const user = firebaseAuth.currentUser
  if (!user) throw new ApiError('Authentication is required. Please sign in again.', 401)

  const token = await user.getIdToken(refreshedToken)
  const headers = new Headers(init?.headers)
  headers.set('Authorization', `Bearer ${token}`)
  const response = await fetch(url, { ...init, headers })
  if (response.status === 401 && !refreshedToken) {
    return requestJsonResponse<T>(url, init, true)
  }
  if (!response.ok) {
    const body: unknown = await response.json().catch(() => ({}))
    const structuredError = isRecord(body) && isRecord(body.error)
      ? body.error
      : undefined
    const message = response.status === 401
      ? 'Authentication expired or is invalid. Please sign in again.'
      : typeof structuredError?.message === 'string'
        ? structuredError.message
        : isRecord(body) && typeof body.detail === 'string'
          ? body.detail
          : 'Request failed'
    throw new ApiError(
      message,
      response.status,
      typeof structuredError?.code === 'string'
        ? structuredError.code
        : 'request_failed',
      Array.isArray(structuredError?.issues) ? structuredError.issues : [],
      structuredError?.retryable === true,
    )
  }
  return {
    data: await response.json() as T,
    response,
  }
}

async function requestJson<T>(
  url: string,
  init?: RequestInit,
): Promise<T> {
  return (await requestJsonResponse<T>(url, init)).data
}

export interface StartV2InterviewData {
  candidate_id: string
  interview_config: {
    mode?: InterviewMode
    language: 'vi' | 'en'
    experience_level: 'intern' | 'junior' | 'middle' | 'senior'
    duration_minutes?: number
    interview_style?: 'technical' | 'behavioral' | 'mixed'
    question_count?: number
    objective?: string
    interviewer_personality?: 'professional' | 'friendly' | 'challenging' | 'supportive'
  }
}

async function uploadResume(file: File): Promise<ResumeUploadResponse> {
  const formData = new FormData()
  formData.append('file', file)
  return requestJson<ResumeUploadResponse>(`${API_ROOT_URL}/api/v2/resume/upload`, {
    method: 'POST',
    body: formData,
  })
}

const reportGenerationRequests = new Map<
  string,
  Promise<InterviewReportResponse>
>()

function generateInterviewReport(
  sessionId: string | number
): Promise<InterviewReportResponse> {
  const key = String(sessionId)
  const existing = reportGenerationRequests.get(key)
  if (existing) return existing

  const request = requestJson<InterviewReportResponse>(
    `${API_ROOT_URL}/api/v2/interview/${encodeURIComponent(key)}/report`,
    { method: 'POST' },
  )
  reportGenerationRequests.set(key, request)
  void request.then(
    () => {
      if (reportGenerationRequests.get(key) === request) {
        reportGenerationRequests.delete(key)
      }
    },
    () => {
      if (reportGenerationRequests.get(key) === request) {
        reportGenerationRequests.delete(key)
      }
    },
  )
  return request
}

export const api = {
  uploadResume,
  uploadV2Resume: uploadResume,
  getVoiceInterviewWebSocketUrl: voiceWebSocketUrl,

  getCandidateProfile: async (
    candidateId: string | number
  ): Promise<CandidateProfileReadResult> => {
    const result = await requestJsonResponse<CandidateProfileResponse>(
      `${API_ROOT_URL}/api/v2/candidates/${encodeURIComponent(String(candidateId))}/profile`
    )
    const etag = result.response.headers.get('ETag')
    if (!etag) {
      throw new ApiError(
        'Candidate Profile response did not include a Profile Version.',
        502,
        'invalid_profile_response',
      )
    }
    return { ...result.data, etag }
  },

  startV2Interview: async (data: StartV2InterviewData): Promise<V2InterviewSessionResponse> => {
    return requestJson(`${API_ROOT_URL}/api/v2/interview/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
  },

  prepareV2Interview: async (
    data: StartV2InterviewData
  ): Promise<V2InterviewPreparationResponse> => {
    return requestJson(`${API_ROOT_URL}/api/v2/interview/prepare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
  },

  submitV2InterviewAnswer: async (
    sessionId: string | number,
    answer: string
  ): Promise<V2InterviewSessionResponse> => {
    return requestJson(`${API_ROOT_URL}/api/v2/interview/${sessionId}/answer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answer }),
    })
  },

  getV2InterviewSession: async (sessionId: string | number): Promise<V2InterviewSessionResponse> => {
    return requestJson(`${API_ROOT_URL}/api/v2/interview/${sessionId}`)
  },

  generateInterviewReport,

  getInterviewReport: async (sessionId: string | number): Promise<InterviewReportResponse> => {
    return requestJson(`${API_ROOT_URL}/api/v2/interview/${sessionId}/report`)
  },

  listInterviewSessions: async (params: {
    candidate_id?: string
    limit?: number
    offset?: number
  } = {}): Promise<InterviewHistoryResponse> => {
    const search = new URLSearchParams()
    if (params.candidate_id) search.set('candidate_id', params.candidate_id)
    if (params.limit !== undefined) search.set('limit', String(params.limit))
    if (params.offset !== undefined) search.set('offset', String(params.offset))
    const query = search.toString()
    return requestJson(`${API_ROOT_URL}/api/v2/interviews${query ? `?${query}` : ''}`)
  },
}

import type {
  InterviewHistoryResponse,
  InterviewMode,
  InterviewReportResponse,
  ResumeUploadResponse,
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
  constructor(message: string, public readonly status: number) {
    super(message)
    this.name = 'ApiError'
  }
}

async function requestJson<T>(
  url: string,
  init?: RequestInit,
  refreshedToken = false
): Promise<T> {
  const user = firebaseAuth.currentUser
  if (!user) throw new ApiError('Authentication is required. Please sign in again.', 401)

  const token = await user.getIdToken(refreshedToken)
  const headers = new Headers(init?.headers)
  headers.set('Authorization', `Bearer ${token}`)
  const response = await fetch(url, { ...init, headers })
  if (response.status === 401 && !refreshedToken) {
    return requestJson<T>(url, init, true)
  }
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    const message = response.status === 401
      ? 'Authentication expired or is invalid. Please sign in again.'
      : error.detail || 'Request failed'
    throw new ApiError(message, response.status)
  }
  return response.json() as Promise<T>
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

export const api = {
  uploadResume,
  uploadV2Resume: uploadResume,
  getVoiceInterviewWebSocketUrl: voiceWebSocketUrl,

  startV2Interview: async (data: StartV2InterviewData): Promise<V2InterviewSessionResponse> => {
    return requestJson(`${API_ROOT_URL}/api/v2/interview/start`, {
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

  generateInterviewReport: async (sessionId: string | number): Promise<InterviewReportResponse> => {
    return requestJson(`${API_ROOT_URL}/api/v2/interview/${sessionId}/report`, {
      method: 'POST',
    })
  },

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

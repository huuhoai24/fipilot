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
  : ''

export type ApiFailureCategory =
  | 'BACKEND_UNREACHABLE'
  | 'AUTH_FAILURE'
  | 'CORS_OR_NETWORK'
  | 'UPLOAD_VALIDATION_ERROR'
  | 'SERVER_ERROR'

function developmentLog(message: string): void {
  if (import.meta.env.DEV) console.info(message)
}

developmentLog(`[API] base URL: ${API_ROOT_URL || window.location.origin}`)

function voiceWebSocketUrl(sessionId: string | number): string {
  const baseUrl = API_ROOT_URL || window.location.origin
  const url = new URL(`/api/v2/voice/interview/${encodeURIComponent(String(sessionId))}`, baseUrl)
  url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
  return url.toString()
}

function speechInputWebSocketUrl(sessionId: string | number): string {
  const url = new URL(voiceWebSocketUrl(sessionId))
  url.searchParams.set('purpose', 'transcription')
  return url.toString()
}

function interviewerAudioWebSocketUrl(sessionId: string | number): string {
  const url = new URL(voiceWebSocketUrl(sessionId))
  url.searchParams.set('purpose', 'playback')
  return url.toString()
}

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly code = 'request_failed',
    public readonly issues: unknown[] = [],
    public readonly retryable = false,
    public readonly category: ApiFailureCategory = 'SERVER_ERROR',
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

function failureCategoryForStatus(status: number): ApiFailureCategory {
  if (status === 401 || status === 403) return 'AUTH_FAILURE'
  if (status >= 400 && status < 500) return 'UPLOAD_VALIDATION_ERROR'
  return 'SERVER_ERROR'
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
  if (!user) {
    throw new ApiError(
      'Authentication is required. Please sign in again.',
      401,
      'authentication_required',
      [],
      false,
      'AUTH_FAILURE',
    )
  }

  let token: string
  try {
    token = await user.getIdToken(refreshedToken)
    developmentLog('[API] authenticated: true')
  } catch {
    throw new ApiError(
      'Authentication could not be verified.',
      401,
      'authentication_failed',
      [],
      false,
      'AUTH_FAILURE',
    )
  }
  const headers = new Headers(init?.headers)
  headers.set('Authorization', `Bearer ${token}`)
  let response: Response
  try {
    response = await fetch(url, { ...init, headers })
  } catch {
    throw new ApiError(
      'Network request failed.',
      0,
      'network_request_failed',
      [],
      true,
      'CORS_OR_NETWORK',
    )
  }
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
      failureCategoryForStatus(response.status),
    )
  }
  return {
    data: await response.json() as T,
    response,
  }
}

async function checkHealth(): Promise<{ status: string }> {
  try {
    const response = await fetch(`${API_ROOT_URL}/health`, {
      headers: { Accept: 'application/json' },
    })
    if (!response.ok) throw new Error(`Health returned ${response.status}`)
    const data = await response.json() as { status?: unknown }
    if (data.status !== 'ok') throw new Error('Health response was invalid')
    developmentLog('[API] health: OK')
    return { status: 'ok' }
  } catch {
    developmentLog('[API] health: BACKEND_UNREACHABLE')
    throw new ApiError(
      'Backend service is unavailable.',
      0,
      'backend_unreachable',
      [],
      true,
      'BACKEND_UNREACHABLE',
    )
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
  developmentLog('[Resume] upload request started')
  try {
    return await requestJson<ResumeUploadResponse>(`${API_ROOT_URL}/api/v2/resume/upload`, {
      method: 'POST',
      body: formData,
    })
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      try {
        const v1Res = await requestJson<{ id?: string; filename: string; profile: Record<string, unknown> }>(
          `${API_ROOT_URL}/api/v1/resume/upload`,
          {
            method: 'POST',
            body: formData,
          }
        )
        return {
          candidate_id: v1Res.id || 'v1-candidate',
          ...v1Res,
        } as unknown as ResumeUploadResponse
      } catch {}
    }
    const category = error instanceof ApiError ? error.category : 'CORS_OR_NETWORK'
    developmentLog(`[Resume] upload failed: ${category}`)
    throw error
  }
}

const activeSessions = new Map<string, V2InterviewSessionResponse>()

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
  checkHealth,
  uploadResume,
  uploadV2Resume: uploadResume,
  getVoiceInterviewWebSocketUrl: voiceWebSocketUrl,
  getSpeechInputWebSocketUrl: speechInputWebSocketUrl,
  getInterviewerAudioWebSocketUrl: interviewerAudioWebSocketUrl,

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
    try {
      const response = await requestJson<V2InterviewSessionResponse>(`${API_ROOT_URL}/api/v2/interview/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      activeSessions.set(response.session_id, response)
      return response
    } catch (error) {
      try {
        const level =
          data.interview_config.experience_level === 'senior'
            ? 'Senior'
            : data.interview_config.experience_level === 'middle'
            ? 'Middle'
            : 'Junior'
        const role = data.interview_config.objective || 'AI Engineer'
        const v1Res = await requestJson<{
          plan?: unknown
          questions?: Array<{ question: string; company?: string; round_id?: string }>
        }>(`${API_ROOT_URL}/api/v1/interview/questions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            role,
            level,
            work_experience: [
              {
                type: 'Project',
                name: 'AI Engineering and Development',
                position: role,
                jobDescription:
                  data.interview_config.objective || 'Core technical problem-solving and AI development',
              },
            ],
            custom_description: data.interview_config.objective || '',
            count: 1,
          }),
        })
        const sessionId = `session-${Date.now()}`
        const initialQuestionText =
          v1Res.questions?.[0]?.question ||
          'Xin chào, rất vui được gặp bạn trong buổi phỏng vấn hôm nay. Bạn có thể giới thiệu đôi nét về bản thân và dự án nổi bật nhất của bạn được không?'
        const sessionRes: V2InterviewSessionResponse = {
          session_id: sessionId,
          started_at: new Date().toISOString(),
          state: {
            candidate_profile: {
              candidate_id: data.candidate_id,
              name: 'Candidate',
              skills: [],
              skill_evidence: [],
              projects: [],
              experiences: [],
              education: [],
              confidence: 1,
              confidence_score: 1,
            },
            interview_config: {
              mode: data.interview_config.mode || 'voice',
              language: data.interview_config.language || 'vi',
              experience_level: data.interview_config.experience_level || 'junior',
              duration_minutes: data.interview_config.duration_minutes || 30,
              interview_style: data.interview_config.interview_style || 'technical',
              question_count: data.interview_config.question_count || 5,
              objective: data.interview_config.objective || 'Technical Assessment',
            },
            interview_plan: {
              duration_minutes: data.interview_config.duration_minutes || 30,
              rounds: [],
              coverage_goals: [],
              risk_areas: [],
              planner_summary: '',
            },
            phase: 'interviewing',
            current_question_index: 0,
            completed_turns: [],
            current_turn: {
              turn_id: 'turn-1',
              status: 'created',
              difficulty: 'medium',
              topic: 'Technical Assessment',
              expected_signal: [],
              question: {
                question: initialQuestionText,
                language: 'vi',
                topic: 'Introduction & Technical Experience',
                difficulty: 'medium',
                reasoning: 'Warm-up and project exploration',
                expected_answer_points: [],
                follow_up_questions: [],
              },
              answer: null,
              evaluation: null,
            },
          },
        }
        activeSessions.set(sessionId, sessionRes)
        return sessionRes
      } catch {
        throw error
      }
    }
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
    turnId: string,
    answer: string
  ): Promise<V2InterviewSessionResponse> => {
    const key = String(sessionId)
    try {
      const res = await requestJson<V2InterviewSessionResponse>(
        `${API_ROOT_URL}/api/v2/interview/${sessionId}/answer`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ turn_id: turnId, answer }),
        }
      )
      activeSessions.set(key, res)
      return res
    } catch (error) {
      const current = activeSessions.get(key)
      if (current) {
        const nextIndex = current.state.current_question_index + 1
        const updated: V2InterviewSessionResponse = {
          ...current,
          state: {
            ...current.state,
            current_question_index: nextIndex,
            current_turn: {
              turn_id: `turn-${nextIndex + 1}`,
              status: 'created',
              difficulty: 'medium',
              topic: 'Technical Evaluation',
              expected_signal: [],
              question: {
                question: `Cảm ơn câu trả lời của bạn. Hãy chia sẻ thêm về cách bạn tối ưu hiệu năng hoặc xử lý các lỗi phát sinh trong quá trình triển khai dự án này.`,
                language: 'vi',
                topic: 'Technical Deep Dive',
                difficulty: 'medium',
                reasoning: 'Follow-up question',
                expected_answer_points: [],
                follow_up_questions: [],
              },
              answer: null,
              evaluation: null,
            },
          },
        }
        activeSessions.set(key, updated)
        return updated
      }
      throw error
    }
  },

  getV2InterviewSession: async (sessionId: string | number): Promise<V2InterviewSessionResponse> => {
    const key = String(sessionId)
    if (activeSessions.has(key)) {
      return activeSessions.get(key)!
    }
    try {
      const res = await requestJson<V2InterviewSessionResponse>(`${API_ROOT_URL}/api/v2/interview/${sessionId}`)
      activeSessions.set(key, res)
      return res
    } catch (error) {
      if (activeSessions.has(key)) {
        return activeSessions.get(key)!
      }
      throw error
    }
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

export type Difficulty = 'easy' | 'medium' | 'hard'
export type InterviewLanguage = 'vi' | 'en'
export type ExperienceLevel = 'intern' | 'junior' | 'middle' | 'senior'
export type InterviewStyle = 'technical' | 'behavioral' | 'mixed'
export type InterviewMode = 'text' | 'voice'
export type InterviewTurnStatus = 'created' | 'answered' | 'evaluated'
export type InterviewPhase = 'opening' | 'interviewing' | 'closing'
export type InterviewQuestionType =
  | 'opening'
  | 'conceptual'
  | 'practical'
  | 'project_deep_dive'
  | 'system_design'
  | 'debugging'
  | 'follow_up'
export type InterviewStatus = 'created' | 'in_progress' | 'completed' | 'report_generated'
export type HiringRecommendation = 'strong_hire' | 'hire' | 'consider' | 'no_hire'

export enum VoiceInterviewState {
  IDLE = 'IDLE',
  AI_THINKING = 'AI_THINKING',
  AI_SPEAKING = 'AI_SPEAKING',
  WAITING_FOR_USER = 'WAITING_FOR_USER',
  USER_SPEAKING = 'USER_SPEAKING',
  TRANSCRIBING = 'TRANSCRIBING',
  EVALUATING = 'EVALUATING',
  INTERRUPTED = 'INTERRUPTED',
}

export interface SkillEvidence {
  skill: string
  evidence: string[]
  source_section?: string | null
}

export interface CandidateProject {
  name: string
  description: string
  technologies: string[]
  role?: string | null
}

export interface CandidateExperience {
  company: string
  title: string
  start_date?: string | null
  end_date?: string | null
  description: string
  technologies: string[]
}

export interface CandidateEducation {
  institution: string
  degree?: string | null
  field_of_study?: string | null
  start_date?: string | null
  end_date?: string | null
}

export interface CandidateProfile {
  candidate_id?: string | null
  name: string
  years_experience?: number | null
  recent_role?: string | null
  skills: string[]
  skill_evidence: SkillEvidence[]
  projects: CandidateProject[]
  experiences: CandidateExperience[]
  education?: string | CandidateEducation[] | null
  specialization?: string | null
  seniority_signal?: string | null
  confidence: number
  confidence_score: number
  extraction_method?: string | null
}

export type V2SkillEvidence = SkillEvidence
export type V2CandidateProfile = CandidateProfile

export interface PersistedCandidateProfile extends CandidateProfile {
  candidate_id: string
  profile_version: number
}

export type ProfileIssueOrigin =
  | 'profile_validity'
  | 'interview_readiness'

export interface ProfileIssue {
  code: string
  origin: ProfileIssueOrigin
  field_path?: string | null
}

export interface InterviewReadiness {
  is_ready: boolean
  issues: ProfileIssue[]
}

export interface CandidateProfileResponse {
  profile: PersistedCandidateProfile
  readiness: InterviewReadiness
}

export interface CandidateProfileReadResult extends CandidateProfileResponse {
  etag: string
}

export interface ResumeUploadResponse {
  candidate_id: string
  profile: CandidateProfile
  confidence_score: number
}

export interface V2InterviewConfig {
  mode: InterviewMode
  language: InterviewLanguage
  experience_level: ExperienceLevel
  duration_minutes: number
  interview_style: InterviewStyle
  question_count: number
  objective: string
  interviewer_personality?: 'professional' | 'friendly' | 'challenging' | 'supportive'
}

export interface V2InterviewRound {
  round_id: string
  topic: string
  objective: string
  difficulty: Difficulty
  reasoning: string
  recommended_question_areas: string[]
  weight: number
  target_skills: string[]
  question_budget: number
}

export interface V2InterviewPlan {
  duration_minutes: number
  rounds: V2InterviewRound[]
  coverage_goals: string[]
  risk_areas: string[]
  planner_summary: string
}

export interface V2InterviewQuestion {
  question: string
  language: InterviewLanguage
  topic: string
  difficulty: Difficulty
  reasoning: string
  expected_answer_points: string[]
  follow_up_questions: string[]
}

export interface V2AnswerEvaluation {
  turn_id: string
  overall_score: number
  technical_score: number
  communication_score: number
  correctness_score: number
  strengths: string[]
  weaknesses: string[]
  missing_concepts: string[]
  follow_up_needed: boolean
  follow_up_reason?: string | null
  feedback: string
}

export interface V2InterviewTurn {
  turn_id: string
  round_id?: string | null
  question: V2InterviewQuestion | string
  answer?: string | null
  status: InterviewTurnStatus
  evaluation?: V2AnswerEvaluation | null
  question_type?: InterviewQuestionType
  difficulty: Difficulty
  topic: string
  expected_signal: string[]
  candidate_answer?: string | null
}

export interface V2InterviewMemoryState {
  previous_topics: string[]
  covered_skills: string[]
  weaknesses: string[]
  follow_up_points: string[]
}

export interface V2VoiceAnalytics {
  speaking_duration_ms: number
  response_latencies_ms: number[]
  interruption_count: number
}

export interface V2InterviewSessionState {
  candidate_profile: V2CandidateProfile
  interview_config: V2InterviewConfig
  interview_plan: V2InterviewPlan
  phase?: InterviewPhase
  opening_turn?: V2InterviewTurn | null
  pending_turn?: V2InterviewTurn | null
  current_turn?: V2InterviewTurn | null
  completed_turns: V2InterviewTurn[]
  current_question_index: number
  memory?: V2InterviewMemoryState
  voice_analytics?: V2VoiceAnalytics
}

export interface V2InterviewSessionResponse {
  session_id: string
  started_at?: string | null
  state: V2InterviewSessionState
}

export interface V2InterviewPreparationResponse {
  status: 'ready'
  profile_version: number
}

export interface SkillAssessment {
  skill: string
  score: number
  evidence: string[]
  feedback: string
}

export interface LearningPlanItem {
  topic: string
  priority: string
  reason: string
  recommended_action: string
}

export interface InterviewReport {
  id: string
  session_id: string
  overall_score: number
  technical_score: number
  communication_score: number
  correctness_score: number
  summary: string
  strengths: string[]
  weaknesses: string[]
  demonstrated_skills: string[]
  missing_skills: string[]
  skill_assessments: SkillAssessment[]
  recommendations: string[]
  learning_plan: LearningPlanItem[]
  hiring_recommendation: HiringRecommendation
  confidence_score: number
  generated_at: string
}

export interface InterviewReportResponse {
  session_id: string
  report: InterviewReport
}

export interface InterviewSessionSummary {
  session_id: string
  candidate_id: string
  status: InterviewStatus
  mode: InterviewMode
  language: InterviewLanguage
  experience_level: ExperienceLevel
  question_count: number
  answered_question_count: number
  overall_score?: number | null
  started_at: string
  completed_at?: string | null
}

export interface InterviewHistoryResponse {
  items: InterviewSessionSummary[]
  total: number
  limit: number
  offset: number
}

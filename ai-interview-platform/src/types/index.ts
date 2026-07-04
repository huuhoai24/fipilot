// Core domain types — mirrors Section 3 data models in the spec.

export type Difficulty = 'easy' | 'medium' | 'hard'
export type Language = 'vi' | 'en'
export type Role = 'data-ai' | 'backend' | 'frontend' | 'mobile' | 'devops'
export type SessionStatus = 'completed' | 'interrupted' | 'no_show' | 'scheduled' | 'in_progress'
export type HireRecommendation = 'strong_hire' | 'hire' | 'consider' | 'reject'

export interface DifficultyMix {
  easy: number
  medium: number
  hard: number
}

export interface InterviewConfig {
  id: string
  name: string
  role: Role
  level: number
  duration_minutes: number
  difficulty_mix: DifficultyMix
  voice_enabled: boolean
  avatar_enabled: boolean
  auto_evaluate: boolean
  scoring_rubric: string
  language: Language
  created_by: string
  created_at: string
}

export interface QnAQuestion {
  id: string
  difficulty: Difficulty
  question: string
  sample_answer: string
  tags: string[]
  score_weight: number
}

export interface QnATemplate {
  id: string
  title: string
  role: Role
  level: number
  version: string
  questions: QnAQuestion[]
  used_count: number
  last_used_at: string | null
  created_by: string
  updated_at: string
}

export interface TemplateMatch {
  template_id: string
  title: string
  score: number
  question_count: number
  difficulty_mix: DifficultyMix
  duration_minutes: number
}

export interface CandidateProfile {
  candidate_name: string
  years_experience: number
  skills: string[]
  education: string
  recent_role: string
  inferred_level: number
  role_fit: Role
  confidence: number
}

export interface TranscriptEntry {
  question_id: string
  question_text: string
  answer_text: string
  answer_audio_url?: string
  duration_ms: number
  difficulty: Difficulty
  score?: number
}

export interface InterviewSession {
  id: string
  candidate_id: string
  candidate_name: string
  template_id: string
  template_title: string
  config_id: string
  role: Role
  level: number
  interviewer_email: string
  started_at: string
  ended_at: string | null
  status: SessionStatus
  transcript: TranscriptEntry[]
  overall_score?: number
}

export interface PerQuestionEvaluation {
  question_id: string
  question_text: string
  difficulty: Difficulty
  score: number
  issues: string[]
  suggestion: string
}

export interface InterviewEvaluation {
  session_id: string
  overall_score: number
  max_score: number
  score_by_difficulty: Record<Difficulty, number>
  per_question: PerQuestionEvaluation[]
  summary: string
  hire_recommendation: HireRecommendation
  generated_at: string
}

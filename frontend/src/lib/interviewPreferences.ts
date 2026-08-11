import type { ExperienceLevel, InterviewLanguage, InterviewStyle } from '@/types'

export interface InterviewPreferences {
  language: InterviewLanguage
  experienceLevel: ExperienceLevel
  interviewStyle: InterviewStyle
  durationMinutes: number
  questionCount: number
  objective: string
}

export const defaultInterviewPreferences: InterviewPreferences = {
  language: 'vi',
  experienceLevel: 'junior',
  interviewStyle: 'technical',
  durationMinutes: 30,
  questionCount: 10,
  objective: 'Evaluate technical knowledge and practical experience',
}

export const INTERVIEW_PREFERENCES_STORAGE_KEY = 'ai-interview:text-settings:v1'
const LEGACY_STORAGE_KEY = 'interview-preferences'

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function isIntegerInRange(value: unknown, minimum: number, maximum = Number.MAX_SAFE_INTEGER): value is number {
  return typeof value === 'number'
    && Number.isInteger(value)
    && value >= minimum
    && value <= maximum
}

function normalizeInterviewPreferences(value: unknown): InterviewPreferences {
  if (!isRecord(value)) return { ...defaultInterviewPreferences }

  return {
    language: value.language === 'vi' || value.language === 'en'
      ? value.language
      : defaultInterviewPreferences.language,
    experienceLevel: value.experienceLevel === 'intern'
      || value.experienceLevel === 'junior'
      || value.experienceLevel === 'middle'
      || value.experienceLevel === 'senior'
      ? value.experienceLevel
      : defaultInterviewPreferences.experienceLevel,
    interviewStyle: value.interviewStyle === 'technical'
      || value.interviewStyle === 'behavioral'
      || value.interviewStyle === 'mixed'
      ? value.interviewStyle
      : defaultInterviewPreferences.interviewStyle,
    durationMinutes: isIntegerInRange(value.durationMinutes, 5, 180)
      ? value.durationMinutes
      : defaultInterviewPreferences.durationMinutes,
    questionCount: isIntegerInRange(value.questionCount, 1)
      ? value.questionCount
      : defaultInterviewPreferences.questionCount,
    objective: typeof value.objective === 'string'
      ? value.objective
      : defaultInterviewPreferences.objective,
  }
}

export function loadInterviewPreferences(): InterviewPreferences {
  try {
    const stored = localStorage.getItem(INTERVIEW_PREFERENCES_STORAGE_KEY)
      ?? localStorage.getItem(LEGACY_STORAGE_KEY)
    if (!stored) return { ...defaultInterviewPreferences }
    return normalizeInterviewPreferences(JSON.parse(stored) as unknown)
  } catch {
    return { ...defaultInterviewPreferences }
  }
}

export function saveInterviewPreferences(preferences: InterviewPreferences): void {
  try {
    localStorage.setItem(
      INTERVIEW_PREFERENCES_STORAGE_KEY,
      JSON.stringify(normalizeInterviewPreferences(preferences)),
    )
  } catch {
    // Storage may be unavailable or full; settings remain usable for this page lifetime.
  }
}

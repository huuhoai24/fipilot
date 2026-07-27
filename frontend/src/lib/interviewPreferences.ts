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

const STORAGE_KEY = 'interview-preferences'

export function loadInterviewPreferences(): InterviewPreferences {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}') as Partial<InterviewPreferences>
    return { ...defaultInterviewPreferences, ...saved }
  } catch {
    return defaultInterviewPreferences
  }
}

export function saveInterviewPreferences(preferences: InterviewPreferences): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(preferences))
}

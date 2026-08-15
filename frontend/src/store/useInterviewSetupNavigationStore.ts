import { create } from 'zustand'
import type {
  CandidateProfile,
  ExperienceLevel,
  InterviewLanguage,
  InterviewStyle,
} from '@/types'

export type InterviewSetupRoute = '/text-interview' | '/speech-interview'

export interface InterviewSetupSnapshot {
  candidateId: string
  uploadedCandidateProfile: CandidateProfile
  selectedResumeFile: File | null
  language: InterviewLanguage
  experienceLevel: ExperienceLevel
  interviewStyle: InterviewStyle
  durationInput: string
  questionCountInput: string
  objective: string
  preparationStatus: 'idle' | 'preparing' | 'ready'
}

interface InterviewSetupNavigationState {
  setups: Record<string, InterviewSetupSnapshot>
  rememberSetup: (
    route: InterviewSetupRoute,
    snapshot: InterviewSetupSnapshot,
  ) => void
}

export function interviewSetupKey(
  route: InterviewSetupRoute,
  candidateId: string,
) {
  return `${route}:${candidateId}`
}

export const useInterviewSetupNavigationStore =
  create<InterviewSetupNavigationState>((set) => ({
    setups: {},
    rememberSetup: (route, snapshot) => set((state) => ({
      setups: {
        ...state.setups,
        [interviewSetupKey(route, snapshot.candidateId)]: snapshot,
      },
    })),
  }))

import { create } from 'zustand'

interface UIState {
  sidebarCollapsed: boolean
  toggleSidebar: () => void
  userMenuOpen: boolean
  toggleUserMenu: () => void
  closeUserMenu: () => void
}

export const useUIStore = create<UIState>((set) => ({
  sidebarCollapsed: false,
  toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),
  userMenuOpen: false,
  toggleUserMenu: () => set((s) => ({ userMenuOpen: !s.userMenuOpen })),
  closeUserMenu: () => set({ userMenuOpen: false }),
}))

interface WizardState {
  step: number
  candidateProfile: import('@/types').CandidateProfile | null
  selectedTemplateId: string | null
  setStep: (step: number) => void
  setCandidateProfile: (profile: import('@/types').CandidateProfile) => void
  setSelectedTemplateId: (id: string) => void
  reset: () => void
}

export const useWizardStore = create<WizardState>((set) => ({
  step: 1,
  candidateProfile: null,
  selectedTemplateId: null,
  setStep: (step) => set({ step }),
  setCandidateProfile: (candidateProfile) => set({ candidateProfile }),
  setSelectedTemplateId: (selectedTemplateId) => set({ selectedTemplateId }),
  reset: () => set({ step: 1, candidateProfile: null, selectedTemplateId: null }),
}))

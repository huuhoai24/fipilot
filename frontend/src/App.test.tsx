import React from 'react'
import { cleanup, render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { Outlet } from 'react-router-dom'
import App from '@/App'

vi.mock('@/contexts/AuthContext', () => ({
  AuthProvider: ({ children }: { children: React.ReactNode }) => children,
}))

vi.mock('@/components/auth/ProtectedRoute', () => ({
  ProtectedRoute: () => <Outlet />,
}))

vi.mock('@/components/layout/AppLayout', () => ({
  AppLayout: () => (
    <div data-testid="dashboard-shell">
      <Outlet />
    </div>
  ),
}))

vi.mock('@/pages/TextInterviewPage', () => ({
  TextInterviewPage: () => <div data-testid="text-interview-page" />,
}))
vi.mock('@/pages/SpeechInterviewPage', () => ({ SpeechInterviewPage: () => null }))
vi.mock('@/pages/InterviewHistoryPage', () => ({ InterviewHistoryPage: () => null }))
vi.mock('@/pages/InterviewReportPage', () => ({ InterviewReportPage: () => null }))
vi.mock('@/pages/SettingsPage', () => ({ SettingsPage: () => null }))
vi.mock('@/pages/CandidateProfilePage', () => ({ CandidateProfilePage: () => null }))
vi.mock('@/pages/LandingPage', () => ({ LandingPage: () => null }))

afterEach(() => {
  cleanup()
  window.history.replaceState({}, '', '/')
})

describe('application route shells', () => {
  it('opens an active text interview outside the dashboard shell', () => {
    window.history.replaceState({}, '', '/text-interview/session-42')

    render(<App />)

    expect(screen.getByTestId('text-interview-page')).toBeInTheDocument()
    expect(screen.queryByTestId('dashboard-shell')).not.toBeInTheDocument()
  })

  it('keeps text interview setup inside the dashboard shell', () => {
    window.history.replaceState({}, '', '/text-interview')

    render(<App />)

    expect(screen.getByTestId('text-interview-page')).toBeInTheDocument()
    expect(screen.getByTestId('dashboard-shell')).toBeInTheDocument()
  })
})

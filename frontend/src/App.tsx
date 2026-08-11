import React from 'react'
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AppLayout } from '@/components/layout/AppLayout'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import { AuthProvider } from '@/contexts/AuthContext'
import { TextInterviewPage } from '@/pages/TextInterviewPage'
import { SpeechInterviewPage } from '@/pages/SpeechInterviewPage'
import { InterviewHistoryPage } from '@/pages/InterviewHistoryPage'
import { InterviewReportPage } from '@/pages/InterviewReportPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { CandidateProfilePage } from '@/pages/CandidateProfilePage'
import { LandingPage } from '@/pages/LandingPage'

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<Navigate to="/" replace />} />
            <Route element={<ProtectedRoute />}>
              <Route path="/text-interview/:sessionId" element={<TextInterviewPage mode="text" />} />
              <Route element={<AppLayout />}>
                <Route path="/text-interview" element={<TextInterviewPage mode="text" />} />
                <Route path="/text-interview/:sessionId/report" element={<InterviewReportPage />} />
                <Route path="/speech-interview" element={<TextInterviewPage mode="voice" />} />
                <Route path="/speech-interview/:sessionId" element={<SpeechInterviewPage />} />
                <Route path="/interview-history" element={<InterviewHistoryPage />} />
                <Route path="/settings" element={<SettingsPage />} />
                <Route path="/candidate-profile/:candidateId" element={<CandidateProfilePage />} />
                <Route path="*" element={<Navigate to="/text-interview" replace />} />
              </Route>
            </Route>
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

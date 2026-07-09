import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AppLayout } from '@/components/layout/AppLayout'
import { AdminRoute } from '@/components/AdminRoute'
import { AuthPage } from '@/pages/AuthPage'
import { DashboardPage } from '@/pages/DashboardPage'
import { InterviewFlowPage } from '@/pages/InterviewFlowPage'
import { InterviewSessionPage } from '@/pages/InterviewSessionPage'
import { TemplateManagerPage } from '@/pages/TemplateManagerPage'
import { HistoryPage } from '@/pages/HistoryPage'
import { EvaluationReportPage } from '@/pages/EvaluationReportPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { useAuthStore } from '@/store/useAuthStore'

const queryClient = new QueryClient()

export default function App() {
  const currentUser = useAuthStore((s) => s.currentUser)

  if (!currentUser) {
    return (
      <QueryClientProvider client={queryClient}>
        <AuthPage />
      </QueryClientProvider>
    )
  }

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/interview-flow" element={<InterviewFlowPage />} />
            <Route path="/interview-flow/session/:sessionId" element={<InterviewSessionPage />} />
            <Route
              path="/templates"
              element={
                <AdminRoute>
                  <TemplateManagerPage />
                </AdminRoute>
              }
            />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/history/:sessionId" element={<EvaluationReportPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

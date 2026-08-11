// THROWAWAY RENDER HARNESS: renders production components with deterministic boundaries.
import React from 'react'
import { createRoot } from 'react-dom/client'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { AppLayout } from '@/components/layout/AppLayout'
import { CandidateProfilePage } from '@/pages/CandidateProfilePage'
import '@/index.css'

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <MemoryRouter initialEntries={['/candidate-profile/candidate-review-7']}>
      <Routes>
        <Route element={<AppLayout />}>
          <Route
            path="/candidate-profile/:candidateId"
            element={<CandidateProfilePage />}
          />
        </Route>
      </Routes>
    </MemoryRouter>
  </React.StrictMode>,
)

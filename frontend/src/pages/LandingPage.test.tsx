import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { LandingPage } from '@/pages/LandingPage'

const auth = vi.hoisted(() => ({
  user: null as { uid: string } | null,
  loading: false,
  signInWithGoogle: vi.fn<() => Promise<void>>(),
}))

vi.mock('@/contexts/AuthContext', () => ({
  useAuth: () => ({
    user: auth.user,
    loading: auth.loading,
    signInWithGoogle: auth.signInWithGoogle,
  }),
}))

function renderLandingPage() {
  return render(
    <MemoryRouter initialEntries={['/']}>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/text-interview" element={<div>Interview workspace</div>} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('LandingPage', () => {
  afterEach(cleanup)

  beforeEach(() => {
    auth.user = null
    auth.loading = false
    auth.signInWithGoogle.mockReset()
    auth.signInWithGoogle.mockResolvedValue()
  })

  it('signs a visitor in from the landing page and opens the workspace', async () => {
    renderLandingPage()

    expect(screen.getByRole('heading', { level: 1, name: 'Fipilot' })).toBeTruthy()
    expect(screen.getByRole('link', { name: 'Fipilot home' }).querySelector('img')?.getAttribute('src')).toBe(
      '/fipilot-logo.svg',
    )
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))

    await waitFor(() => expect(auth.signInWithGoogle).toHaveBeenCalledTimes(1))
    expect(await screen.findByText('Interview workspace')).toBeTruthy()
  })

  it('shows a safe error when Google sign-in fails', async () => {
    auth.signInWithGoogle.mockRejectedValue(new Error('Popup was closed.'))
    renderLandingPage()

    fireEvent.click(screen.getByRole('button', { name: 'Start an interview' }))

    expect((await screen.findByRole('alert')).textContent).toContain('Popup was closed.')
  })

  it('opens the workspace directly for an authenticated candidate', () => {
    auth.user = { uid: 'user-1' }
    renderLandingPage()

    expect(screen.getByRole('link', { name: 'Open workspace' }).getAttribute('href')).toBe('/text-interview')
    expect(screen.getByRole('link', { name: 'Start an interview' }).getAttribute('href')).toBe('/text-interview')
  })

  it('provides the how-it-works video with Vietnamese captions', () => {
    renderLandingPage()

    const video = screen.getByLabelText('How Fipilot works')
    expect(video.querySelector('source')?.getAttribute('src')).toBe('/fipilot-how-it-works.mp4')
    expect(video.querySelector('track')?.getAttribute('src')).toBe('/fipilot-how-it-works.vi.vtt')
  })
})

import React from 'react'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { SettingsPage } from '@/pages/SettingsPage'

beforeEach(() => {
  localStorage.clear()
})

afterEach(() => {
  cleanup()
})

describe('SettingsPage', () => {
  it('keeps first-deploy controls while persisting current interview preferences', () => {
    render(
      <MemoryRouter>
        <SettingsPage />
      </MemoryRouter>,
    )

    fireEvent.change(screen.getByLabelText('Language'), {
      target: { value: 'en' },
    })
    fireEvent.change(screen.getByLabelText('Interview Style'), {
      target: { value: 'mixed' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Save preferences' }))

    expect(screen.getByRole('status')).toHaveTextContent(
      'Preferences saved on this device.',
    )
    expect(JSON.parse(localStorage.getItem('interview-preferences') ?? '{}')).toMatchObject({
      language: 'en',
      interviewStyle: 'mixed',
    })
  })
})

import React from 'react'
import { cleanup, render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { TextInterviewPage } from '@/pages/TextInterviewPage'

vi.mock('@/lib/api', () => ({
  api: {
    getV2InterviewSession: vi.fn(),
    uploadResume: vi.fn(),
    startV2Interview: vi.fn(),
    submitV2InterviewAnswer: vi.fn(),
  },
}))

afterEach(() => {
  cleanup()
})

describe('TextInterviewPage interview mode', () => {
  it('keeps the page heading and session summary in sync when the route mode changes', () => {
    const { rerender } = render(
      <MemoryRouter>
        <TextInterviewPage mode="text" />
      </MemoryRouter>,
    )

    expect(screen.getByRole('heading', { level: 1, name: 'Text Interview' })).toBeInTheDocument()
    expect(screen.getByText('Text', { selector: 'span' })).toBeInTheDocument()
    expect(screen.getByLabelText('Language')).toBeInTheDocument()
    expect(screen.queryByText('Set up my interview')).not.toBeInTheDocument()

    rerender(
      <MemoryRouter>
        <TextInterviewPage mode="voice" />
      </MemoryRouter>,
    )

    expect(screen.getByRole('heading', { level: 1, name: 'Speech Interview' })).toBeInTheDocument()
    expect(screen.getByText('Speech', { selector: 'span' })).toBeInTheDocument()
    expect(screen.queryByText('Choose Interview Mode')).not.toBeInTheDocument()
  })
})

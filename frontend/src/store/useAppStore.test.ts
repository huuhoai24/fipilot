import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('useUIStore theme', () => {
  beforeEach(() => {
    localStorage.clear()
    document.documentElement.className = ''
    vi.resetModules()
  })

  it('uses light theme when the candidate has no saved preference', async () => {
    const { useUIStore } = await import('@/store/useAppStore')

    expect(useUIStore.getState().theme).toBe('light')
    expect(document.documentElement.classList.contains('light')).toBe(true)
    expect(document.documentElement.dataset.theme).toBe('light')
  })

  it('keeps an explicitly saved dark preference', async () => {
    localStorage.setItem('theme', 'dark')

    const { useUIStore } = await import('@/store/useAppStore')

    expect(useUIStore.getState().theme).toBe('dark')
    expect(document.documentElement.classList.contains('dark')).toBe(true)
    expect(document.documentElement.dataset.theme).toBe('dark')
  })

  it('keeps the selected website theme independent from browser preference', async () => {
    localStorage.setItem('theme', 'light')
    vi.stubGlobal('matchMedia', vi.fn().mockReturnValue({ matches: true }))

    const { useUIStore } = await import('@/store/useAppStore')

    expect(useUIStore.getState().theme).toBe('light')
    expect(document.documentElement.className).toBe('light')
    expect(document.documentElement.dataset.theme).toBe('light')
  })
})

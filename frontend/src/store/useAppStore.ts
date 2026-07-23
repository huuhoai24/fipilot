import { create } from 'zustand'

type Theme = 'dark' | 'light'

function getInitialTheme(): Theme {
  try {
    const saved = localStorage.getItem('theme') as Theme | null
    if (saved === 'light' || saved === 'dark') return saved
  } catch {}
  return 'dark'
}

function applyTheme(theme: Theme) {
  const html = document.documentElement
  html.classList.remove('dark', 'light')
  html.classList.add(theme)
  try { localStorage.setItem('theme', theme) } catch {}
}

interface UIState {
  sidebarCollapsed: boolean
  toggleSidebar: () => void
  userMenuOpen: boolean
  toggleUserMenu: () => void
  closeUserMenu: () => void
  theme: Theme
  toggleTheme: () => void
  setTheme: (t: Theme) => void
}

export const useUIStore = create<UIState>((set, get) => {
  const initial = getInitialTheme()
  // Áp dụng ngay khi store khởi tạo (trước khi component nào mount)
  if (typeof document !== 'undefined') applyTheme(initial)

  return {
    sidebarCollapsed: false,
    toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),
    userMenuOpen: false,
    toggleUserMenu: () => set((s) => ({ userMenuOpen: !s.userMenuOpen })),
    closeUserMenu: () => set({ userMenuOpen: false }),
    theme: initial,
    toggleTheme: () => {
      const next: Theme = get().theme === 'dark' ? 'light' : 'dark'
      applyTheme(next)
      set({ theme: next })
    },
    setTheme: (t: Theme) => {
      applyTheme(t)
      set({ theme: t })
    },
  }
})

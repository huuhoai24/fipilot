import React, { useState } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { History, Loader2, LogOut, MessageSquareText, Mic, Settings } from 'lucide-react'
import { Sidebar } from './Sidebar'
import { useUIStore } from '@/store/useAppStore'
import { useAuth } from '@/contexts/AuthContext'
import { cn } from '@/lib/utils'

export function AppLayout() {
  const { sidebarCollapsed } = useUIStore()
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [loggingOut, setLoggingOut] = useState(false)
  const [logoutError, setLogoutError] = useState('')
  const mobileNav = [
    { to: '/text-interview', label: 'Text', icon: MessageSquareText },
    { to: '/speech-interview', label: 'Speech', icon: Mic },
    { to: '/interview-history', label: 'History', icon: History },
    { to: '/settings', label: 'Settings', icon: Settings },
  ]

  const handleLogout = async () => {
    if (loggingOut) return
    setLoggingOut(true)
    setLogoutError('')
    try {
      await logout()
      navigate('/login', { replace: true })
    } catch {
      setLogoutError('Could not sign out. Please try again.')
      setLoggingOut(false)
    }
  }

  return (
    <div className="relative min-h-screen overflow-x-hidden bg-bg">
      <a
        href="#main-content"
        className="fixed left-4 top-4 z-50 -translate-y-20 rounded-xl bg-accent px-4 py-2 text-sm font-semibold text-[#07110d] transition-transform focus:translate-y-0"
      >
        Skip to main content
      </a>
      <div className="ambient-grid pointer-events-none fixed inset-0 opacity-40" aria-hidden="true" />
      <div
        className="pointer-events-none fixed -right-32 top-12 h-96 w-96 rounded-full bg-accent/10 blur-[120px]"
        aria-hidden="true"
      />
      <Sidebar />
      <header className="glass-panel sticky top-2 z-30 mx-2 mt-2 rounded-2xl border border-border px-3 py-2 shadow-xl shadow-black/10 md:hidden">
        <div className="mb-2.5 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-accent">
              <Mic className="h-4 w-4 text-[#07110d]" />
            </div>
            <span className="font-display text-sm font-bold tracking-tight-display text-text-primary">
              Interview<span className="text-accent">OS</span>
            </span>
          </div>
          <div className="flex min-w-0 items-center gap-2">
            <span className="max-w-[32vw] truncate text-xs text-text-muted">{user?.displayName || user?.email}</span>
            <button
              type="button"
              onClick={() => void handleLogout()}
              disabled={loggingOut}
              className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-border text-text-muted transition-colors hover:border-danger/40 hover:bg-danger/10 hover:text-danger disabled:cursor-wait disabled:opacity-50"
              aria-label={loggingOut ? 'Signing out' : 'Sign out'}
              title={loggingOut ? 'Signing out' : 'Sign out'}
            >
              {loggingOut
                ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                : <LogOut className="h-4 w-4" aria-hidden="true" />}
            </button>
          </div>
        </div>
        {logoutError && (
          <p role="alert" className="mb-2 rounded-lg bg-danger/10 px-3 py-2 text-xs text-danger">
            {logoutError}
          </p>
        )}
        <nav className="flex gap-1 overflow-x-auto" aria-label="Primary navigation">
          {mobileNav.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                cn(
                  'flex h-9 shrink-0 items-center gap-1.5 rounded-xl px-3 text-xs font-semibold',
                  isActive ? 'bg-accent-soft text-accent' : 'text-text-muted hover:bg-surface-raised hover:text-text-primary'
                )
              }
            >
              <Icon className="h-3.5 w-3.5" />
              {label}
            </NavLink>
          ))}
        </nav>
      </header>
      <main
        id="main-content"
        className={cn(
          'relative z-10 min-h-screen w-full max-w-full overflow-x-hidden transition-[margin] duration-300 max-md:ml-0 md:w-auto',
          sidebarCollapsed ? 'md:ml-24' : 'md:ml-[18.5rem]'
        )}
      >
        <div className="mx-auto max-w-[1500px] px-4 py-8 sm:px-6 lg:px-10 lg:py-10">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

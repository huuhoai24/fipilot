import React, { useState } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { History, Loader2, LogOut, MessageSquareText, Mic, Settings } from 'lucide-react'
import { Sidebar } from './Sidebar'
import { BrandLogo } from '@/components/brand/BrandLogo'
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
    <div className="min-h-screen bg-bg">
      <a
        href="#main-content"
        className="fixed left-4 top-4 z-50 -translate-y-20 rounded-md bg-accent px-4 py-2 text-sm font-medium text-accent-contrast transition-transform focus:translate-y-0"
      >
        Skip to main content
      </a>
      <Sidebar />
      <header className="sticky top-0 z-30 border-b border-border bg-surface/95 px-3 py-2 backdrop-blur md:hidden">
        <div className="mb-2 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BrandLogo className="h-8 w-8" />
            <span className="text-sm font-semibold text-text-primary">
              Fi<span className="text-accent">pilot</span>
            </span>
          </div>
          <div className="flex min-w-0 items-center gap-2">
            <span className="max-w-[30vw] truncate text-xs text-text-muted">{user?.displayName || user?.email}</span>
            <button
              type="button"
              onClick={() => void handleLogout()}
              disabled={loggingOut}
              className="flex h-11 w-11 shrink-0 items-center justify-center rounded-md text-text-muted hover:bg-surface-raised hover:text-danger disabled:cursor-wait disabled:opacity-50"
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
          <p role="alert" className="mb-2 rounded-md bg-danger/10 px-3 py-2 text-xs text-danger">
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
                  'flex h-9 shrink-0 items-center gap-1.5 rounded-md px-3 text-xs font-medium',
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
          'min-h-screen transition-[margin] duration-150 max-md:ml-0',
          sidebarCollapsed ? 'md:ml-16' : 'md:ml-60'
        )}
      >
        <div className="mx-auto max-w-[1440px] px-4 py-4 sm:px-6 lg:px-8 lg:py-6">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

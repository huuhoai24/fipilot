import React from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { History, MessageSquareText, Mic, Settings } from 'lucide-react'
import { Sidebar } from './Sidebar'
import { useUIStore } from '@/store/useAppStore'
import { useAuth } from '@/contexts/AuthContext'
import { cn } from '@/lib/utils'

export function AppLayout() {
  const { sidebarCollapsed } = useUIStore()
  const { user } = useAuth()
  const mobileNav = [
    { to: '/text-interview', label: 'Text', icon: MessageSquareText },
    { to: '/speech-interview', label: 'Speech', icon: Mic },
    { to: '/interview-history', label: 'History', icon: History },
    { to: '/settings', label: 'Settings', icon: Settings },
  ]

  return (
    <div className="min-h-screen bg-bg">
      <Sidebar />
      <header className="sticky top-0 z-30 border-b border-border bg-surface/95 px-3 py-2 backdrop-blur md:hidden">
        <div className="mb-2 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-md bg-accent">
              <Mic className="h-4 w-4 text-white" />
            </div>
            <span className="text-sm font-semibold text-text-primary">
              Interview<span className="text-accent">OS</span>
            </span>
          </div>
          <span className="max-w-[38vw] truncate text-xs text-text-muted">{user?.displayName || user?.email}</span>
        </div>
        <nav className="flex gap-1 overflow-x-auto">
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

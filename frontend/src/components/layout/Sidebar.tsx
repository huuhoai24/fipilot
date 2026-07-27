import React from 'react'
import { NavLink } from 'react-router-dom'
import {
  ChevronsLeft,
  ChevronsRight,
  ChevronDown,
  History,
  MessageSquareText,
  Mic,
  Moon,
  Settings,
  Sun,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useAuth } from '@/contexts/AuthContext'
import { useUIStore } from '@/store/useAppStore'
import { UserMenu } from './UserMenu'

const navItems = [
  { to: '/text-interview', label: 'Text Interview', icon: MessageSquareText },
  { to: '/speech-interview', label: 'Speech Interview', icon: Mic },
  { to: '/interview-history', label: 'Interview History', icon: History },
  { to: '/settings', label: 'Settings', icon: Settings },
]

export function Sidebar() {
  const { sidebarCollapsed, toggleSidebar, userMenuOpen, toggleUserMenu, theme, toggleTheme } = useUIStore()
  const { user } = useAuth()
  const displayName = user?.displayName || user?.email || 'Member'
  const displayRole = 'Member'
  const initial = displayName.charAt(0).toUpperCase()

  return (
    <aside
      className={cn(
        'glass-panel fixed left-4 top-4 z-40 hidden h-[calc(100vh-2rem)] flex-col overflow-hidden rounded-[24px] border border-border shadow-2xl shadow-black/20 transition-[width] duration-300 md:flex',
        sidebarCollapsed ? 'w-16' : 'w-[260px]'
      )}
    >
      <div className={cn('flex h-[76px] items-center gap-3 border-b border-border px-5', sidebarCollapsed && 'justify-center px-0')}>
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-accent shadow-lg shadow-accent/10">
          <Mic className="h-4 w-4 text-[#07110d]" />
        </div>
        {!sidebarCollapsed && (
          <span className="font-display text-base font-bold tracking-tight-display text-text-primary">
            Interview<span className="text-accent">OS</span>
          </span>
        )}
      </div>

      <nav className="flex-1 space-y-1.5 overflow-y-auto px-3 py-5" aria-label="Primary navigation">
        {navItems.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                'group relative flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-semibold transition-all duration-300',
                isActive
                  ? 'bg-accent text-[#07110d] shadow-lg shadow-accent/10'
                  : 'text-text-muted hover:translate-x-0.5 hover:bg-surface-raised hover:text-text-primary',
                sidebarCollapsed && 'justify-center px-0'
              )
            }
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <span className="absolute left-0 top-1/2 h-5 w-[3px] -translate-y-1/2 rounded-full bg-[#07110d]/50" />
                )}
                <Icon className="h-[18px] w-[18px] shrink-0" />
                {!sidebarCollapsed && <span>{label}</span>}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      <button
        onClick={toggleSidebar}
        className="flex items-center gap-2 border-t border-border px-4 py-3.5 text-xs font-medium text-text-faint transition-colors duration-200 hover:bg-surface-raised hover:text-text-muted"
      >
        {sidebarCollapsed ? (
          <ChevronsRight className="mx-auto h-4 w-4" />
        ) : (
          <>
            <ChevronsLeft className="h-4 w-4" />
            <span>Collapse</span>
          </>
        )}
      </button>

      <div className={cn('border-t border-border', sidebarCollapsed ? 'flex justify-center px-0 py-3' : 'px-4 py-3')}>
        {sidebarCollapsed ? (
          <button
            onClick={toggleTheme}
            title={theme === 'dark' ? 'Switch to Light' : 'Switch to Dark'}
            className="flex h-8 w-8 items-center justify-center rounded-lg text-text-muted transition-colors duration-150 hover:bg-surface-raised hover:text-text-primary"
          >
            {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </button>
        ) : (
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs text-text-muted">
              {theme === 'dark' ? <Moon className="h-3.5 w-3.5" /> : <Sun className="h-3.5 w-3.5" />}
              <span>Theme</span>
            </div>
            <button
              onClick={toggleTheme}
              role="switch"
              aria-checked={theme === 'light'}
              className={cn(
                'relative flex h-6 w-[88px] items-center rounded-full border p-0.5 transition-colors duration-200',
                theme === 'dark' ? 'border-border bg-surface-raised' : 'border-accent/40 bg-accent-soft'
              )}
            >
              <span className={cn('flex-1 text-center text-[10px] font-medium', theme === 'dark' ? 'text-accent' : 'text-text-faint')}>
                Dark
              </span>
              <span className={cn('flex-1 text-center text-[10px] font-medium', theme === 'light' ? 'text-accent' : 'text-text-faint')}>
                Light
              </span>
              <span
                className={cn(
                  'absolute top-0.5 h-5 w-[42px] rounded-full bg-accent shadow transition-transform duration-200',
                  theme === 'light' ? 'translate-x-[42px]' : 'translate-x-0'
                )}
              />
            </button>
          </div>
        )}
      </div>

      <div className="relative border-t border-border">
        <button
          type="button"
          onClick={toggleUserMenu}
          data-user-menu-trigger
          aria-haspopup="menu"
          aria-expanded={userMenuOpen}
          aria-controls={userMenuOpen ? 'account-menu' : undefined}
          className={cn(
            'flex w-full items-center gap-2.5 px-4 py-2.5 text-left transition-colors duration-200',
            userMenuOpen ? 'bg-surface-raised' : 'hover:bg-surface-raised',
            sidebarCollapsed && 'justify-center px-0'
          )}
        >
          {user?.photoURL ? (
            <img className="h-8 w-8 shrink-0 rounded-full object-cover" src={user.photoURL} alt="" referrerPolicy="no-referrer" />
          ) : (
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent/20 text-xs font-semibold text-accent">
              {initial}
            </div>
          )}
          {!sidebarCollapsed && (
            <>
              <div className="min-w-0 flex-1">
                <div className="truncate text-[13px] font-semibold text-text-primary">{displayName}</div>
                <div className="truncate text-[11px] text-text-faint">{displayRole}</div>
              </div>
              <ChevronDown
                className={cn(
                  'h-3.5 w-3.5 shrink-0 text-text-faint transition-transform duration-150',
                  userMenuOpen && 'rotate-180'
                )}
              />
            </>
          )}
        </button>
        <UserMenu sidebarCollapsed={sidebarCollapsed} />
      </div>
    </aside>
  )
}

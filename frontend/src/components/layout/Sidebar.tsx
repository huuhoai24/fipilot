import React from 'react'
import { NavLink, useNavigate, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  Mic,
  FileText,
  History,
  ChevronsLeft,
  ChevronsRight,
  ChevronDown,
  Circle,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useUIStore } from '@/store/useAppStore'
import { useAuthStore } from '@/store/useAuthStore'
import { useActiveSessionStore } from '@/store/useActiveSessionStore'
import { UserMenu } from './UserMenu'

const navItem = (to: string, label: string, icon: any) => ({ to, label, icon })

export function Sidebar() {
  const { sidebarCollapsed, toggleSidebar, userMenuOpen, toggleUserMenu } = useUIStore()
  const { currentUser } = useAuthStore()
  const sessions = useActiveSessionStore((s) => s.sessions)
  const navigate = useNavigate()
  const location = useLocation()
  const isAdmin = currentUser?.role === 'admin'

  const runningSessions = Object.values(sessions)

  const baseNavItems = [
    navItem('/', 'Dashboard', LayoutDashboard),
    navItem('/interview-flow', 'Interview Flow', Mic),
  ]
  const navItems = isAdmin
    ? [...baseNavItems, navItem('/templates', 'Templates', FileText), navItem('/history', 'History', History)]
    : [...baseNavItems, navItem('/history', 'History', History)]

  const displayName = currentUser?.username ?? 'Guest'
  const displayRole = currentUser?.role === 'admin' ? 'Admin' : 'Member'
  const initial = displayName.charAt(0).toUpperCase()

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 z-40 flex h-screen flex-col border-r border-border bg-surface transition-[width] duration-150',
        sidebarCollapsed ? 'w-16' : 'w-60'
      )}
    >
      {/* Logo */}
      <div className={cn('flex h-16 items-center gap-2.5 border-b border-border px-4', sidebarCollapsed && 'justify-center px-0')}>
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-accent">
          <Mic className="h-4 w-4 text-white" />
        </div>
        {!sidebarCollapsed && (
          <span className="font-display text-sm font-bold tracking-tight-display text-text-primary">
            Interview<span className="text-accent">AI</span>
          </span>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        {navItems.map(({ to, label, icon: Icon }) => (
          <React.Fragment key={to}>
            <NavLink
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                cn(
                  'group relative flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors duration-150',
                  isActive
                    ? 'bg-accent-soft text-accent'
                    : 'text-text-muted hover:bg-surface-raised hover:text-text-primary',
                  sidebarCollapsed && 'justify-center px-0'
                )
              }
            >
              {({ isActive }) => (
                <>
                  {isActive && (
                    <span className="absolute left-0 top-1/2 h-5 w-[3px] -translate-y-1/2 rounded-full bg-accent" />
                  )}
                  <Icon className="h-[18px] w-[18px] shrink-0" />
                  {!sidebarCollapsed && <span>{label}</span>}
                </>
              )}
            </NavLink>

            {/* Danh sách phiên đang chạy — chỉ hiện ngay dưới mục Interview Flow */}
            {to === '/interview-flow' && !sidebarCollapsed && runningSessions.length > 0 && (
              <div className="ml-3 mt-1 space-y-0.5 border-l border-border pl-3">
                {runningSessions.map((s) => {
                  const sessionPath = `/interview-flow/session/${s.sessionId}`
                  const isActive = location.pathname === sessionPath
                  return (
                    <button
                      key={s.sessionId}
                      onClick={() => navigate(sessionPath)}
                      className={cn(
                        'flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-xs transition-colors duration-150',
                        isActive
                          ? 'bg-accent-soft text-accent'
                          : 'text-text-muted hover:bg-surface-raised hover:text-text-primary'
                      )}
                    >
                      <Circle
                        className={cn(
                          'h-1.5 w-1.5 shrink-0 fill-current',
                          s.paused ? 'text-text-faint' : 'text-danger animate-pulse'
                        )}
                      />
                      <span className="truncate">{s.candidateName}</span>
                    </button>
                  )
                })}
              </div>
            )}
          </React.Fragment>
        ))}
      </nav>

      {/* Collapse toggle */}
      <button
        onClick={toggleSidebar}
        className="flex items-center gap-2 border-t border-border px-3 py-3 text-xs text-text-faint hover:text-text-muted transition-colors duration-150"
      >
        {sidebarCollapsed ? (
          <ChevronsRight className="mx-auto h-4 w-4" />
        ) : (
          <>
            <ChevronsLeft className="h-4 w-4" />
            <span>Thu gọn</span>
          </>
        )}
      </button>

      {/* User — click to open Settings / Sign out popover */}
      <div className="relative border-t border-border">
        <button
          onClick={toggleUserMenu}
          className={cn(
            'flex w-full items-center gap-2.5 px-4 py-3 text-left transition-colors duration-150',
            userMenuOpen ? 'bg-surface-raised' : 'hover:bg-surface-raised',
            sidebarCollapsed && 'justify-center px-0'
          )}
        >
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent/20 text-xs font-semibold text-accent">
            {initial}
          </div>
          {!sidebarCollapsed && (
            <>
              <div className="min-w-0 flex-1">
                <div className="truncate text-xs font-medium text-text-primary">{displayName}</div>
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

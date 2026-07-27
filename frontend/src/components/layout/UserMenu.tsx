import React, { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Loader2, LogOut, Settings } from 'lucide-react'
import { useUIStore } from '@/store/useAppStore'
import { useAuth } from '@/contexts/AuthContext'
import { cn } from '@/lib/utils'

interface UserMenuProps {
  sidebarCollapsed: boolean
}

export function UserMenu({ sidebarCollapsed }: UserMenuProps) {
  const navigate = useNavigate()
  const { userMenuOpen, closeUserMenu } = useUIStore()
  const { logout } = useAuth()
  const ref = useRef<HTMLDivElement>(null)
  const [loggingOut, setLoggingOut] = useState(false)
  const [logoutError, setLogoutError] = useState('')

  useEffect(() => {
    if (!userMenuOpen) {
      setLogoutError('')
      return
    }
    const onClickOutside = (e: MouseEvent) => {
      const target = e.target as Element
      const clickedTrigger = target.closest('[data-user-menu-trigger]')
      if (ref.current && !ref.current.contains(target) && !clickedTrigger) {
        closeUserMenu()
      }
    }
    const onEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') closeUserMenu()
    }
    document.addEventListener('mousedown', onClickOutside)
    document.addEventListener('keydown', onEscape)
    return () => {
      document.removeEventListener('mousedown', onClickOutside)
      document.removeEventListener('keydown', onEscape)
    }
  }, [userMenuOpen, closeUserMenu])

  if (!userMenuOpen) return null

  const handleSettings = () => {
    closeUserMenu()
    navigate('/settings')
  }

  const handleLogout = async () => {
    if (loggingOut) return
    setLoggingOut(true)
    setLogoutError('')
    try {
      await logout()
      closeUserMenu()
      navigate('/login', { replace: true })
    } catch {
      setLogoutError('Could not sign out. Please try again.')
      setLoggingOut(false)
    }
  }

  return (
    <div
      ref={ref}
      id="account-menu"
      role="menu"
      aria-label="Account menu"
      className={cn(
        'fixed z-50 w-56 rounded-lg border border-border bg-surface-raised py-1.5 shadow-2xl shadow-black/40 animate-fade-in',
        'bottom-3'
      )}
      style={{ left: sidebarCollapsed ? '72px' : '248px' }}
    >
      <button
        type="button"
        role="menuitem"
        onClick={handleSettings}
        className="flex min-h-11 w-full items-center gap-2.5 px-3.5 py-2.5 text-sm text-text-primary hover:bg-surface transition-colors duration-150"
      >
        <Settings className="h-4 w-4 text-text-muted" aria-hidden="true" />
        Settings
      </button>
      <div className="my-1 border-t border-border" />
      <button
        type="button"
        role="menuitem"
        onClick={() => void handleLogout()}
        disabled={loggingOut}
        className="flex min-h-11 w-full items-center gap-2.5 px-3.5 py-2.5 text-sm text-danger hover:bg-danger/10 transition-colors duration-150 disabled:cursor-wait disabled:opacity-50"
      >
        {loggingOut
          ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
          : <LogOut className="h-4 w-4" aria-hidden="true" />}
        {loggingOut ? 'Signing out' : 'Sign out'}
      </button>
      {logoutError && (
        <p role="alert" className="border-t border-danger/20 bg-danger/10 px-3.5 py-2.5 text-xs leading-5 text-danger">
          {logoutError}
        </p>
      )}
    </div>
  )
}

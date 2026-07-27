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
      className="fixed bottom-3 z-50 w-56 animate-fade-in overflow-hidden rounded-xl border border-border bg-surface-raised shadow-[0_24px_70px_rgba(3,8,6,0.45)]"
      style={{ left: sidebarCollapsed ? '88px' : '284px' }}
    >
      <button
        type="button"
        role="menuitem"
        onClick={handleSettings}
        className="flex h-[52px] w-full items-center gap-3 px-4 text-sm font-medium text-text-primary transition-colors duration-200 hover:bg-accent-soft active:bg-accent-soft"
      >
        <Settings className="h-[18px] w-[18px] text-text-muted" aria-hidden="true" />
        Settings
      </button>
      <div className="border-t border-border" aria-hidden="true" />
      <button
        type="button"
        role="menuitem"
        onClick={() => void handleLogout()}
        disabled={loggingOut}
        className="flex h-[52px] w-full items-center gap-3 px-4 text-sm font-medium text-danger transition-colors duration-200 hover:bg-danger/10 active:bg-danger/15 disabled:cursor-wait disabled:opacity-50"
      >
        {loggingOut
          ? <Loader2 className="h-[18px] w-[18px] animate-spin" aria-hidden="true" />
          : <LogOut className="h-[18px] w-[18px]" aria-hidden="true" />}
        {loggingOut ? 'Signing out' : 'Sign out'}
      </button>
      {logoutError && (
        <p role="alert" className="border-t border-danger/20 bg-danger/10 px-4 py-2.5 text-xs leading-5 text-danger">
          {logoutError}
        </p>
      )}
    </div>
  )
}

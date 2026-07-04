import React, { useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { Settings, LogOut } from 'lucide-react'
import { useUIStore } from '@/store/useAppStore'
import { useAuthStore } from '@/store/useAuthStore'
import { cn } from '@/lib/utils'

interface UserMenuProps {
  sidebarCollapsed: boolean
}

export function UserMenu({ sidebarCollapsed }: UserMenuProps) {
  const navigate = useNavigate()
  const { userMenuOpen, closeUserMenu } = useUIStore()
  const { logout } = useAuthStore()
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!userMenuOpen) return
    const onClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
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

  const handleLogout = () => {
    closeUserMenu()
    logout()
  }

  return (
    <div
      ref={ref}
      className={cn(
        'fixed z-50 w-56 rounded-lg border border-border bg-surface-raised py-1.5 shadow-2xl shadow-black/40 animate-fade-in',
        'bottom-3'
      )}
      style={{ left: sidebarCollapsed ? '72px' : '248px' }}
    >
      <button
        onClick={handleSettings}
        className="flex w-full items-center gap-2.5 px-3.5 py-2.5 text-sm text-text-primary hover:bg-surface transition-colors duration-150"
      >
        <Settings className="h-4 w-4 text-text-muted" />
        Settings
      </button>
      <div className="my-1 border-t border-border" />
      <button
        onClick={handleLogout}
        className="flex w-full items-center gap-2.5 px-3.5 py-2.5 text-sm text-danger hover:bg-danger/10 transition-colors duration-150"
      >
        <LogOut className="h-4 w-4" />
        Sign out
      </button>
    </div>
  )
}

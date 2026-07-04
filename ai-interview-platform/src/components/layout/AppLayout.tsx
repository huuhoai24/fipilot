import React from 'react'
import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { useUIStore } from '@/store/useAppStore'
import { cn } from '@/lib/utils'

export function AppLayout() {
  const { sidebarCollapsed } = useUIStore()

  return (
    <div className="min-h-screen bg-bg">
      <Sidebar />
      <main
        className={cn(
          'min-h-screen transition-[margin] duration-150',
          sidebarCollapsed ? 'ml-16' : 'ml-60'
        )}
      >
        <div className="mx-auto max-w-[1400px] px-6 py-6 lg:px-10 lg:py-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

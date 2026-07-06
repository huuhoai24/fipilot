import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '@/store/useAuthStore'

export function AdminRoute({ children }: { children: React.ReactNode }) {
  const currentUser = useAuthStore((s) => s.currentUser)
  if (currentUser?.role !== 'admin') {
    return <Navigate to="/" replace />
  }
  return <>{children}</>
}

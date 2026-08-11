import React from 'react'
import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { Loader2 } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

export function ProtectedRoute() {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-bg">
        <Loader2 className="h-7 w-7 animate-spin text-accent" />
      </div>
    )
  }
  if (!user) {
    return <Navigate to="/" replace state={{ from: location.pathname }} />
  }
  return <Outlet />
}

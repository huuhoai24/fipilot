import React, { useState } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { AlertCircle, Loader2, LogIn } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { BrandLogo } from '@/components/brand/BrandLogo'
import { useAuth } from '@/contexts/AuthContext'

export function LoginPage() {
  const { user, loading, signInWithGoogle } = useAuth()
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const location = useLocation()
  const navigate = useNavigate()

  if (!loading && user) return <Navigate to="/text-interview" replace />

  const handleGoogleSignIn = async () => {
    setSubmitting(true)
    setError('')
    try {
      await signInWithGoogle()
      const destination = (location.state as { from?: string } | null)?.from
      navigate(destination || '/text-interview', { replace: true })
    } catch (signInError) {
      setError(signInError instanceof Error ? signInError.message : 'Google sign-in failed.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-bg px-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center gap-3">
          <BrandLogo className="h-12 w-12" />
          <span className="font-display text-lg font-bold text-text-primary">
            Fi<span className="text-accent">pilot</span>
          </span>
        </div>
        <div className="rounded-lg border border-border bg-surface p-6">
          <h1 className="text-center text-lg font-semibold text-text-primary">Sign in</h1>
          <p className="mt-2 text-center text-sm text-text-muted">
            Continue with the Google account that owns your interviews.
          </p>
          {error && (
            <div className="mt-5 flex items-start gap-2 rounded-lg border border-danger/30 bg-danger/10 px-3 py-2.5 text-xs text-danger">
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
          <Button className="mt-6 w-full" onClick={() => void handleGoogleSignIn()} disabled={submitting || loading}>
            {submitting || loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <LogIn className="h-4 w-4" />}
            Continue with Google
          </Button>
        </div>
      </div>
    </div>
  )
}

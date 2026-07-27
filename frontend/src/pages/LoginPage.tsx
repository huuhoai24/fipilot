import React, { useState } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import {
  AlertCircle,
  Check,
  Loader2,
  LogIn,
  MessageSquareText,
  Mic,
  ShieldCheck,
} from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { useAuth } from '@/contexts/AuthContext'

const benefits = [
  'Questions based on your real CV',
  'Text and realtime speech practice',
  'Clear feedback after every session',
]

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
    <main id="main-content" className="relative min-h-screen overflow-x-hidden bg-bg px-4 py-4 sm:px-6 lg:px-8">
      <div className="ambient-grid pointer-events-none absolute inset-0 opacity-35" aria-hidden="true" />

      <nav className="glass-panel relative z-10 mx-auto flex max-w-[1440px] items-center justify-between rounded-2xl border border-border px-4 py-3 shadow-lg shadow-black/10 sm:px-5">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-accent">
            <Mic className="h-5 w-5 text-[#07110d]" aria-hidden="true" />
          </div>
          <span className="font-display text-base font-bold tracking-tight-display text-text-primary">
            Interview<span className="text-accent">OS</span>
          </span>
        </div>
        <div className="flex items-center gap-2 text-xs font-medium text-text-muted">
          <ShieldCheck className="h-4 w-4 text-accent" aria-hidden="true" />
          <span className="hidden sm:inline">Secure candidate workspace</span>
        </div>
      </nav>

      <section className="relative z-10 mx-auto grid min-h-[calc(100vh-6rem)] max-w-[1440px] items-center gap-10 py-10 lg:grid-cols-[minmax(0,.92fr)_minmax(440px,1.08fr)] lg:gap-16">
        <div className="animate-fade-in min-w-0 py-4 lg:py-12">
          <p className="flex items-center gap-2 text-sm font-semibold text-accent">
            <MessageSquareText className="h-4 w-4" aria-hidden="true" />
            Practice built around your experience
          </p>
          <h1 className="mt-6 max-w-3xl font-display text-[clamp(3.2rem,6vw,6.4rem)] font-semibold leading-[0.92] tracking-[-0.06em] text-text-primary">
            Prepare for the interview that matters.
          </h1>
          <p className="mt-7 max-w-xl text-balance text-lg leading-8 text-text-muted">
            Turn your CV into focused interview practice that adapts to what you say and shows you what to improve next.
          </p>

          {error && (
            <div role="alert" className="mt-6 flex max-w-xl items-start gap-2 rounded-xl border border-danger/30 bg-danger/10 px-4 py-3 text-sm text-danger">
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
              <span>{error}</span>
            </div>
          )}

          <Button
            className="mt-9 w-full sm:w-auto"
            size="lg"
            onClick={() => void handleGoogleSignIn()}
            disabled={submitting || loading}
          >
            {submitting || loading
              ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
              : <LogIn className="h-4 w-4" aria-hidden="true" />}
            Continue with Google
          </Button>

          <ul className="mt-10 max-w-xl divide-y divide-border border-y border-border">
            {benefits.map((benefit) => (
              <li key={benefit} className="flex items-center gap-3 py-3.5 text-sm text-text-muted">
                <Check className="h-4 w-4 shrink-0 text-accent" aria-hidden="true" />
                {benefit}
              </li>
            ))}
          </ul>
        </div>

        <figure className="animate-fade-in relative mx-auto w-full max-w-[680px] overflow-hidden rounded-[28px] border border-border bg-surface shadow-2xl shadow-black/30 lg:ml-auto">
          <div className="aspect-[4/5] sm:aspect-[5/4] lg:aspect-[4/5]">
            <img
              src="https://images.pexels.com/photos/5899254/pexels-photo-5899254.jpeg?cs=srgb&fm=jpg&auto=compress&w=1500"
              alt="Candidate speaking on a video call while using a laptop and headphones"
              className="h-full w-full object-cover object-center grayscale-[15%] contrast-[1.04]"
            />
          </div>
          <div className="absolute inset-0 bg-gradient-to-t from-[#07110d]/90 via-transparent to-transparent" aria-hidden="true" />
          <figcaption className="absolute inset-x-0 bottom-0 p-6 sm:p-8">
            <p className="max-w-md font-display text-2xl font-semibold leading-tight text-white">
              Practice your reasoning, not a script.
            </p>
            <p className="mt-2 max-w-md text-sm leading-6 text-white/70">
              Follow-up questions respond to the evidence and trade-offs in every answer.
            </p>
          </figcaption>
        </figure>
      </section>
    </main>
  )
}

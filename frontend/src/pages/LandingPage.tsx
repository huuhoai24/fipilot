import React, { useState } from 'react'
import {
  AlertCircle,
  ArrowRight,
  BarChart3,
  Check,
  FileSearch,
  Keyboard,
  Loader2,
  MessageSquareText,
  Moon,
  Sun,
  Volume2,
} from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { Button, ButtonLink } from '@/components/ui/Button'
import { BrandLogo } from '@/components/brand/BrandLogo'
import { useAuth } from '@/contexts/AuthContext'
import { useUIStore } from '@/store/useAppStore'

const workflow = [
  {
    icon: FileSearch,
    title: 'Review your profile',
    description: 'Upload your resume, inspect the extracted evidence, and correct it before the interview starts.',
  },
  {
    icon: MessageSquareText,
    title: 'Choose the conversation',
    description: 'Set your level and objective, then practice through text or a live voice session.',
  },
  {
    icon: BarChart3,
    title: 'Learn from the report',
    description: 'Review your scores, demonstrated strengths, and the areas that need a stronger answer.',
  },
]

const interviewModes = [
  {
    icon: Keyboard,
    title: 'Text interview',
    description: 'Write considered answers while the next question adapts to your interview progress.',
  },
  {
    icon: Volume2,
    title: 'Speech interview',
    description: 'Answer naturally with realtime transcription and a spoken AI interviewer.',
  },
]

export function LandingPage() {
  const { user, loading, signInWithGoogle } = useAuth()
  const { theme, toggleTheme } = useUIStore()
  const navigate = useNavigate()
  const [signingIn, setSigningIn] = useState(false)
  const [signInError, setSignInError] = useState('')

  const handleWorkspaceAccess = async () => {
    if (user) {
      navigate('/text-interview')
      return
    }

    setSigningIn(true)
    setSignInError('')
    try {
      await signInWithGoogle()
      navigate('/text-interview', { replace: true })
    } catch (error) {
      setSignInError(error instanceof Error ? error.message : 'Google sign-in failed.')
    } finally {
      setSigningIn(false)
    }
  }

  return (
    <div className="min-h-[100dvh] bg-bg text-text-primary">
      <a
        href="#main-content"
        className="sr-only z-50 rounded-lg bg-surface px-4 py-3 text-sm font-semibold text-text-primary focus:not-sr-only focus:fixed focus:left-4 focus:top-4"
      >
        Skip to main content
      </a>

      <header className="border-b border-border bg-surface">
        <div className="mx-auto flex h-[72px] max-w-[1280px] items-center justify-between gap-6 px-4 md:px-6 lg:px-10">
          <Link to="/" className="flex shrink-0 items-center gap-3" aria-label="Fipilot home">
            <BrandLogo className="h-10 w-10" />
            <span className="font-display text-lg font-bold">
              Fi<span className="text-accent">pilot</span>
            </span>
          </Link>

          <nav aria-label="Landing page" className="hidden items-center gap-8 md:flex">
            <a className="text-sm font-medium text-text-muted hover:text-text-primary" href="#how-it-works">
              How it works
            </a>
            <a className="text-sm font-medium text-text-muted hover:text-text-primary" href="#interview-modes">
              Interview modes
            </a>
            <a className="text-sm font-medium text-text-muted hover:text-text-primary" href="#feedback">
              Feedback
            </a>
          </nav>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={toggleTheme}
              className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-border bg-surface text-text-muted hover:border-accent hover:text-accent"
              aria-label={theme === 'light' ? 'Use dark theme' : 'Use light theme'}
              title={theme === 'light' ? 'Use dark theme' : 'Use light theme'}
            >
              {theme === 'light' ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
            </button>
            {user ? (
              <ButtonLink to="/text-interview" variant="outline" className="hidden sm:inline-flex">
                Open workspace
              </ButtonLink>
            ) : (
              <Button
                type="button"
                variant="outline"
                className="hidden sm:inline-flex"
                onClick={() => void handleWorkspaceAccess()}
                disabled={loading || signingIn}
              >
                {signingIn && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
                {signingIn ? 'Signing in' : 'Sign in'}
              </Button>
            )}
          </div>
        </div>
      </header>

      <main id="main-content">
        <section className="relative isolate min-h-[620px] overflow-hidden lg:min-h-[calc(100dvh-112px)] lg:max-h-[760px]">
          <img
            src="/interview-hero.png"
            alt="A software engineer practicing a voice interview at a laptop"
            className="absolute inset-0 h-full w-full object-cover object-[66%_center]"
            loading="eager"
          />
          <div className="absolute inset-0 bg-black/55" aria-hidden="true" />
          <div className="relative mx-auto flex min-h-[620px] max-w-[1280px] items-center px-4 py-16 md:px-6 lg:min-h-[calc(100dvh-112px)] lg:max-h-[760px] lg:px-10">
            <div className="max-w-[600px] text-white">
              <p className="mb-4 text-sm font-semibold text-[#8af0ce]">CV-driven interview practice</p>
              <h1 className="font-display text-5xl font-semibold leading-[1.05] md:text-6xl">
                Fipilot
              </h1>
              <p className="mt-6 max-w-[560px] text-lg leading-8 text-white/85">
                Practice interviews grounded in your CV, in text or voice, then review evidence-based feedback.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                {user ? (
                  <ButtonLink to="/text-interview" size="lg" treatment="restrained">
                    Start an interview
                    <ArrowRight className="h-4 w-4" aria-hidden="true" />
                  </ButtonLink>
                ) : (
                  <Button
                    type="button"
                    size="lg"
                    treatment="restrained"
                    onClick={() => void handleWorkspaceAccess()}
                    disabled={loading || signingIn}
                  >
                    {signingIn ? (
                      <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                    ) : (
                      <ArrowRight className="h-4 w-4" aria-hidden="true" />
                    )}
                    {signingIn ? 'Signing in' : 'Start an interview'}
                  </Button>
                )}
                <a
                  href="#how-it-works"
                  className="inline-flex h-12 items-center justify-center rounded-lg border border-white/55 bg-black/15 px-6 text-sm font-medium text-white hover:border-white hover:bg-black/25"
                >
                  Explore the process
                </a>
              </div>
              {signInError && (
                <div
                  role="alert"
                  className="mt-5 flex max-w-[560px] items-start gap-2 rounded-lg border border-red-300/60 bg-black/45 px-4 py-3 text-sm text-white"
                >
                  <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-red-200" aria-hidden="true" />
                  <span>{signInError}</span>
                </div>
              )}
            </div>
          </div>
        </section>

        <section id="how-it-works" className="scroll-mt-8 border-b border-border bg-surface">
          <div className="mx-auto max-w-[1280px] px-4 py-16 md:px-6 lg:px-10 lg:py-20">
            <div className="max-w-[680px]">
              <h2 className="text-3xl font-semibold leading-10 md:text-4xl">From resume to useful practice</h2>
              <p id="how-it-works-summary" className="mt-4 text-base leading-7 text-text-muted">
                Your saved Candidate Profile gives every interview a clear starting point and keeps the session focused on evidence you can discuss.
              </p>
            </div>
            <video
              className="mt-10 aspect-video w-full rounded-lg border border-border bg-black object-cover"
              controls
              preload="metadata"
              poster="/interview-hero.png"
              aria-label="How Fipilot works"
              aria-describedby="how-it-works-summary"
            >
              <source src="/fipilot-how-it-works.mp4" type="video/mp4" />
              <track
                kind="captions"
                src="/fipilot-how-it-works.vi.vtt"
                srcLang="vi"
                label="Vietnamese"
              />
              Your browser does not support video playback.
            </video>
            <div className="mt-12 grid gap-8 md:grid-cols-3 md:gap-0 md:divide-x md:divide-border">
              {workflow.map(({ icon: Icon, title, description }) => (
                <article key={title} className="md:px-8 md:first:pl-0 md:last:pr-0">
                  <Icon className="h-6 w-6 text-accent" aria-hidden="true" />
                  <h3 className="mt-5 text-lg font-semibold">{title}</h3>
                  <p className="mt-3 text-sm leading-6 text-text-muted">{description}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section id="interview-modes" className="scroll-mt-8 bg-bg">
          <div className="mx-auto grid max-w-[1280px] gap-12 px-4 py-16 md:px-6 lg:grid-cols-[0.8fr_1.2fr] lg:px-10 lg:py-20">
            <div className="max-w-[480px]">
              <h2 className="text-3xl font-semibold leading-10 md:text-4xl">Practice in the format that challenges you</h2>
              <p className="mt-4 text-base leading-7 text-text-muted">
                Use text to sharpen the substance of an answer, then move to speech when delivery and response time matter.
              </p>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              {interviewModes.map(({ icon: Icon, title, description }) => (
                <article key={title} className="rounded-lg border border-border bg-surface p-6">
                  <Icon className="h-6 w-6 text-accent" aria-hidden="true" />
                  <h3 className="mt-8 text-xl font-semibold">{title}</h3>
                  <p className="mt-3 text-sm leading-6 text-text-muted">{description}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section id="feedback" className="scroll-mt-8 border-y border-border bg-surface">
          <div className="mx-auto grid max-w-[1280px] gap-10 px-4 py-16 md:px-6 lg:grid-cols-2 lg:px-10 lg:py-20">
            <div>
              <h2 className="max-w-[520px] text-3xl font-semibold leading-10 md:text-4xl">
                Questions stay connected to your background
              </h2>
            </div>
            <div className="space-y-6">
              {[
                'Candidate evidence is reviewed before an interview starts.',
                'Follow-up questions respond to the progress of the session.',
                'The final report separates strengths from areas to improve.',
              ].map((item) => (
                <div key={item} className="flex gap-4 border-b border-border pb-6 last:border-b-0 last:pb-0">
                  <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-accent-soft text-accent">
                    <Check className="h-4 w-4" aria-hidden="true" />
                  </span>
                  <p className="text-base leading-7 text-text-muted">{item}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-bg">
        <div className="mx-auto flex max-w-[1280px] flex-col gap-4 px-4 py-8 text-sm text-text-muted md:flex-row md:items-center md:justify-between md:px-6 lg:px-10">
          <span className="font-semibold text-text-primary">Fipilot</span>
          <span>Focused interview practice for technical candidates.</span>
        </div>
      </footer>
    </div>
  )
}

import React from 'react'
import {
  Award,
  CheckCircle2,
  Clock,
  FileText,
  Mic,
  Sparkles,
  User,
  Video,
} from 'lucide-react'

interface SpeechLandingViewProps {
  roleTitle?: string
  candidateName?: string
  onStartClick: () => void
  disabled?: boolean
}

export function SpeechLandingView({
  roleTitle = 'AI Fluency & Technical Interview',
  candidateName,
  onStartClick,
  disabled = false,
}: SpeechLandingViewProps) {
  return (
    <div className="relative min-h-[580px] w-full overflow-hidden rounded-2xl border border-white/10 bg-[#12141a] p-6 sm:p-10 text-white shadow-2xl">
      {/* Background glow */}
      <div
        className="pointer-events-none absolute -right-20 -top-20 h-96 w-96 rounded-full bg-accent/10 blur-3xl"
        aria-hidden="true"
      />
      <div
        className="pointer-events-none absolute -bottom-20 -left-20 h-96 w-96 rounded-full bg-blue-500/5 blur-3xl"
        aria-hidden="true"
      />

      <div className="relative z-10 grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        {/* Left Column: Information & CTA */}
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-accent/30 bg-accent/10 px-3 py-1 text-xs font-medium text-accent">
            <Sparkles className="h-3.5 w-3.5" />
            AI-Powered Voice Practice
          </div>

          <h1 className="mt-3 font-display text-3xl font-bold tracking-tight sm:text-4xl text-white">
            {roleTitle}
          </h1>
          <p className="mt-2 text-base text-white/70">
            Practice realistic, interactive voice interviews grounded in your experience.
          </p>

          <div className="mt-8 space-y-5">
            <div className="flex items-start gap-3.5">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-white/10 bg-white/5 text-accent">
                <FileText className="h-4 w-4" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-white">Focus on projects and experience</h3>
                <p className="mt-0.5 text-xs text-white/60">
                  Discuss your hands-on achievements, technical choices, and practical problem-solving.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3.5">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-white/10 bg-white/5 text-accent">
                <Mic className="h-4 w-4" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-white">A realistic, voice-based interview</h3>
                <p className="mt-0.5 text-xs text-white/60">
                  Build confidence by speaking naturally with low-latency streaming AI dialogue.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3.5">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-white/10 bg-white/5 text-accent">
                <Award className="h-4 w-4" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-white">Demonstrate domain depth</h3>
                <p className="mt-0.5 text-xs text-white/60">
                  Showcase your ability to evaluate trade-offs, follow-ups, and architectural patterns.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3.5">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-white/10 bg-white/5 text-accent">
                <CheckCircle2 className="h-4 w-4" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-white">Improve with actionable feedback</h3>
                <p className="mt-0.5 text-xs text-white/60">
                  Receive structured scoring on communication, technical accuracy, and key growth areas.
                </p>
              </div>
            </div>
          </div>

          <div className="mt-8">
            <button
              type="button"
              onClick={onStartClick}
              disabled={disabled}
              className="inline-flex items-center gap-2 rounded-xl bg-accent px-6 py-3 text-sm font-semibold text-slate-950 shadow-lg shadow-accent/20 transition-all hover:bg-accent-hover hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Start voice interview
            </button>
          </div>
        </div>

        {/* Right Column: Preview Hero Studio Card */}
        <div className="flex justify-center">
          <div className="w-full max-w-md rounded-2xl border border-white/10 bg-[#161820] p-4 shadow-2xl">
            {/* Mock Header */}
            <div className="flex items-center justify-between border-b border-white/10 pb-3 text-xs text-white/50">
              <span className="flex items-center gap-1.5 font-medium">
                <span className="h-2 w-2 rounded-full bg-accent animate-pulse" />
                Live Studio Session
              </span>
              <span className="flex items-center gap-1">
                <Clock className="h-3.5 w-3.5" />
                30:00
              </span>
            </div>

            {/* Mock Room Layout */}
            <div className="mt-4 grid grid-cols-2 gap-3 aspect-[16/10]">
              {/* User Side */}
              <div className="relative flex flex-col items-center justify-center rounded-xl border border-white/5 bg-[#101217] p-4">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-white/10 text-white/70">
                  <User className="h-8 w-8" />
                </div>
                <span className="mt-2 text-xs font-medium text-white/80 truncate max-w-[120px]">
                  {candidateName || 'Candidate'}
                </span>
                <div className="mt-3 flex items-center gap-2 text-white/40">
                  <div className="flex h-6 w-6 items-center justify-center rounded-full bg-white/5">
                    <Mic className="h-3 w-3" />
                  </div>
                  <div className="flex h-6 w-6 items-center justify-center rounded-full bg-white/5">
                    <Video className="h-3 w-3" />
                  </div>
                </div>
              </div>

              {/* AI Interviewer Side with Listening Effect */}
              <div className="relative flex flex-col items-center justify-center overflow-hidden rounded-xl border border-blue-500/20 bg-gradient-to-b from-blue-600/20 to-blue-900/30 p-4">
                {/* Concentric rings */}
                <div className="relative flex items-center justify-center">
                  <div className="absolute h-24 w-24 rounded-full border border-blue-400/20 animate-ping" />
                  <div className="absolute h-18 w-18 rounded-full border border-blue-400/30 animate-pulse" />
                  <div className="flex h-14 w-14 items-center justify-center rounded-full bg-blue-500/30 text-blue-300 shadow-lg shadow-blue-500/20">
                    <Mic className="h-6 w-6 text-blue-200" />
                  </div>
                </div>
                <span className="mt-3 text-[11px] font-semibold tracking-wider text-blue-300">
                  LISTENING...
                </span>
              </div>
            </div>

            {/* Bottom Subtle Status */}
            <div className="mt-4 rounded-lg bg-black/30 p-2.5 text-center text-xs text-white/50">
              Interactive voice turn-taking with real-time feedback
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  AlertCircle,
  CheckCircle2,
  ClipboardCheck,
  FileText,
  FileUp,
  Loader2,
  Mic,
  Sparkles,
  User,
  Video,
} from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { DeviceSettingsModal } from '@/components/voice/DeviceSettingsModal'
import { ResumeUploadModal } from '@/components/resume/ResumeUploadModal'
import { InterviewFocusModal } from '@/components/resume/InterviewFocusModal'
import { api } from '@/lib/api'
import { getUserFacingError } from '@/lib/userFacingError'
import type { CandidateProfile, ExperienceLevel } from '@/types'

const benefits = [
  {
    icon: FileText,
    title: 'Focus on projects and experience',
    description:
      'Discuss your experience with AI tools, how you use AI in your work, and your understanding of AI concepts.',
  },
  {
    icon: Mic,
    title: 'A realistic, voice-based interview',
    description:
      'Build confidence by speaking naturally, just like you would in a real interview.',
  },
  {
    icon: Sparkles,
    title: 'Demonstrate AI fluency',
    description:
      'Show how you stay current with AI trends, evaluate tools, and apply AI effectively in real-world scenarios.',
  },
  {
    icon: ClipboardCheck,
    title: 'Improve with clear, actionable feedback',
    description:
      'Get specific feedback on your clarity, depth of examples, and how well you communicate your AI experience.',
  },
]

export function SpeechLandingPage() {
  const navigate = useNavigate()
  const [profile, setProfile] = useState<CandidateProfile | null>(null)
  const [starting, setStarting] = useState(false)
  const [error, setError] = useState('')
  const [isListeningPreview, setIsListeningPreview] = useState(true)

  // Step Modals
  const [step1Open, setStep1Open] = useState(false)
  const [step2Open, setStep2Open] = useState(false)
  const [deviceSettingsOpen, setDeviceSettingsOpen] = useState(false)

  // Interview chosen config
  const [interviewConfig, setInterviewConfig] = useState<{
    roleTitle: string
    roleId: string
    experienceLevel: ExperienceLevel
    objective?: string
    durationMinutes: number
    questionCount: number
  } | null>(null)

  const handleStartFlow = () => {
    if (!profile) {
      setStep1Open(true)
    } else {
      setStep2Open(true)
    }
  }

  const handleStep1Continue = (analyzedProfile: CandidateProfile) => {
    setProfile(analyzedProfile)
    setStep1Open(false)
    setStep2Open(true)
  }

  const handleStep2Continue = (config: {
    roleTitle: string
    roleId: string
    experienceLevel: ExperienceLevel
    objective?: string
    durationMinutes: number
    questionCount: number
  }) => {
    setInterviewConfig(config)
    setStep2Open(false)
    setDeviceSettingsOpen(true)
  }

  const handleFinalStartInterview = async () => {
    if (!profile) return

    setStarting(true)
    setError('')
    try {
      const candidateId = profile.candidate_id ? String(profile.candidate_id) : ''
      const level = interviewConfig?.experienceLevel || 'junior'
      const response = await api.startV2Interview({
        candidate_id: candidateId,
        interview_config: {
          mode: 'voice',
          language: 'vi',
          experience_level: level,
          duration_minutes: interviewConfig?.durationMinutes || 30,
          question_count: interviewConfig?.questionCount || 5,
          interview_style: 'technical',
          objective: interviewConfig?.objective,
        },
      })
      navigate(`/speech-interview/${response.session_id}`)
    } catch (err) {
      setError(getUserFacingError(err, 'Failed to start voice interview session.'))
      setStarting(false)
    }
  }

  return (
    <div className="min-h-full py-4 px-2 sm:px-6 max-w-6xl mx-auto transition-colors duration-200">
      {error && (
        <div role="alert" className="mb-6 flex items-center gap-3 rounded-xl border border-danger/30 bg-danger/10 p-4 text-sm text-danger">
          <AlertCircle className="h-5 w-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center min-h-[calc(100vh-140px)]">
        {/* Left Column: Information & Benefits */}
        <div className="lg:col-span-7 space-y-8">
          <div>
            <h1 className="text-3xl sm:text-4xl lg:text-[42px] font-bold tracking-tight text-text-primary font-display leading-tight">
              AI Fluency
            </h1>
            <p className="mt-3 text-lg sm:text-xl text-text-muted font-normal">
              Practice with AI-powered voice interviews
            </p>
          </div>

          {/* Benefit Cards List */}
          <div className="space-y-4">
            {benefits.map((b, idx) => {
              const Icon = b.icon
              return (
                <div
                  key={idx}
                  className="flex items-start gap-4 pb-4 border-b border-border last:border-b-0 transition-colors"
                >
                  <div className="mt-1 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-surface-raised border border-border text-accent">
                    <Icon className="h-4 w-4" />
                  </div>
                  <div className="space-y-1">
                    <h2 className="text-sm sm:text-base font-bold text-text-primary">
                      {b.title}
                    </h2>
                    <p className="text-xs sm:text-sm text-text-muted leading-relaxed">
                      {b.description}
                    </p>
                  </div>
                </div>
              )
            })}
          </div>

          {/* CTA Buttons */}
          <div className="pt-2 flex flex-wrap items-center gap-4">
            <Button
              size="lg"
              onClick={handleStartFlow}
              disabled={starting}
              className="bg-[#13813a] hover:bg-[#0e612c] text-white font-bold px-8 py-3.5 h-auto text-base rounded-xl shadow-lg shadow-[#13813a]/20 transition-all hover:scale-[1.02]"
            >
              {starting ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin mr-2" />
                  Starting session...
                </>
              ) : profile ? (
                'Start AI Interview'
              ) : (
                'Try for free'
              )}
            </Button>

            {profile ? (
              <Button
                type="button"
                variant="outline"
                onClick={() => setStep1Open(true)}
                className="rounded-xl border-border hover:bg-surface-raised"
              >
                <FileUp className="h-4 w-4 mr-2" />
                Upload new CV
              </Button>
            ) : null}

            {profile && (
              <span className="text-xs text-text-muted flex items-center gap-1.5">
                <CheckCircle2 className="h-4 w-4 text-success shrink-0" />
                Profile loaded: {profile.name}
              </span>
            )}
          </div>
        </div>

        {/* Right Column: Interactive Preview Hero Card */}
        <div className="lg:col-span-5 flex justify-center">
          <Card className="w-full max-w-md overflow-hidden rounded-2xl border border-border bg-surface shadow-2xl transition-all">
            {/* Mock Header */}
            <div className="flex items-center justify-between border-b border-border/80 bg-surface-raised/50 px-4 py-3 text-xs text-text-muted">
              <span className="font-medium text-text-primary">FiPilot AI Studio</span>
              <div className="flex items-center gap-2 font-mono">
                <span>⏱ 30:00</span>
                <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              </div>
            </div>

            {/* Stage Preview */}
            <div className="p-6 grid grid-cols-2 gap-4 items-center bg-gradient-to-b from-surface/50 to-surface-raised/80 min-h-[260px]">
              {/* Left PIP Self View Card */}
              <div className="flex flex-col items-center justify-center rounded-2xl border border-border/80 bg-surface-raised p-5 text-center shadow-inner h-44">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-surface border border-border text-text-muted mb-3 shadow-sm">
                  <User className="h-8 w-8 text-text-muted/70" />
                </div>
                <span className="text-xs font-semibold text-text-primary truncate max-w-[120px]">
                  {profile?.name || 'Candidate'}
                </span>
                <div className="mt-2 flex items-center gap-2 text-text-muted/60">
                  <Mic className="h-3 w-3" />
                  <Video className="h-3 w-3" />
                </div>
              </div>

              {/* Right Active Listening Card */}
              <button
                type="button"
                onClick={() => setIsListeningPreview(!isListeningPreview)}
                className="relative flex flex-col items-center justify-center rounded-2xl bg-blue-600 text-white p-5 text-center shadow-xl shadow-blue-500/25 h-44 transition-transform hover:scale-[1.03] focus:outline-none"
              >
                {/* Pulsing concentric rings */}
                {isListeningPreview && (
                  <>
                    <span className="absolute inset-4 rounded-full border border-white/20 animate-ping opacity-75 pointer-events-none" />
                    <span className="absolute inset-8 rounded-full border border-white/30 animate-pulse pointer-events-none" />
                  </>
                )}

                <div className="relative z-10 flex h-14 w-14 items-center justify-center rounded-full bg-white/20 text-white mb-3 backdrop-blur-sm shadow-inner">
                  <Mic className="h-7 w-7 text-white" />
                </div>
                <span className="relative z-10 text-xs font-extrabold tracking-wider uppercase text-white/90">
                  {isListeningPreview ? 'Listening...' : 'Click to test'}
                </span>
              </button>
            </div>

            {/* Bottom Caption */}
            <div className="border-t border-border/60 bg-surface-raised/40 p-3 text-center text-xs text-text-muted font-medium">
              Interactive voice turn-taking with real-time feedback
            </div>
          </Card>
        </div>
      </div>

      {/* Step 1: Resume Upload & Extraction Review Modal */}
      <ResumeUploadModal
        isOpen={step1Open}
        onClose={() => setStep1Open(false)}
        onContinue={handleStep1Continue}
      />

      {/* Step 2: Choose Interview Focus & Level Modal */}
      <InterviewFocusModal
        isOpen={step2Open}
        profile={profile}
        onBack={() => {
          setStep2Open(false)
          setStep1Open(true)
        }}
        onClose={() => setStep2Open(false)}
        onContinue={handleStep2Continue}
      />

      {/* Step 3: Audio & Camera Settings Modal */}
      <DeviceSettingsModal
        isOpen={deviceSettingsOpen}
        onClose={() => setDeviceSettingsOpen(false)}
        onStart={async () => {
          setDeviceSettingsOpen(false)
          await handleFinalStartInterview()
        }}
      />
    </div>
  )
}

import React, { FormEvent, useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  ArrowRight,
  CheckCircle2,
  Circle,
  FileText,
  Loader2,
  Upload,
} from 'lucide-react'
import { Button, ButtonLink } from '@/components/ui/Button'
import { Card, CardContent, CardHeader } from '@/components/ui/Card'
import { Input, Label, Select, Textarea } from '@/components/ui/Input'
import { InterviewPreparationScreen } from '@/components/interview/InterviewPreparationScreen'
import {
  TextInterviewRoom,
  TextInterviewRoomStatus,
} from '@/components/interview/TextInterviewRoom'
import { resolveInterviewerPersona } from '@/lib/interviewerPersonas'
import { api } from '@/lib/api'
import {
  loadInterviewPreferences,
  saveInterviewPreferences,
} from '@/lib/interviewPreferences'
import {
  getInterviewAnswerError,
  getResumeUploadError,
  getUserFacingError,
} from '@/lib/userFacingError'
import type {
  CandidateProfile,
  ExperienceLevel,
  InterviewMode,
  InterviewLanguage,
  InterviewStyle,
  V2InterviewSessionResponse,
  V2InterviewSessionState,
} from '@/types'

const MAX_RESUME_BYTES = 10 * 1024 * 1024
const RESUME_EXTENSIONS = new Set(['pdf', 'docx'])
const RESUME_MIME_TYPES = new Set([
  'application/pdf',
  'application/x-pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
])

type ResumeUploadStatus = 'idle' | 'uploading' | 'success' | 'error'
type BackendAvailability = 'unknown' | 'checking' | 'reachable' | 'unreachable'

function parseIntegerSetting(value: string, minimum: number, maximum = Number.MAX_SAFE_INTEGER): number | null {
  if (value.trim() === '') return null
  const parsed = Number(value)
  return Number.isInteger(parsed) && parsed >= minimum && parsed <= maximum
    ? parsed
    : null
}

function validateResumeFile(file: File): string | null {
  const extension = file.name.split('.').pop()?.toLowerCase() ?? ''
  if (!RESUME_EXTENSIONS.has(extension)) {
    return 'Choose a PDF or DOCX resume.'
  }
  if (file.type && !RESUME_MIME_TYPES.has(file.type)) {
    return 'The selected file type does not match a PDF or DOCX document.'
  }
  if (file.size === 0) return 'The selected file is empty.'
  if (file.size > MAX_RESUME_BYTES) return 'The resume must be 10 MB or smaller.'
  return null
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function CandidateProfilePreview({
  profile,
  candidateId,
}: {
  profile: CandidateProfile
  candidateId: string
}) {
  const role = profile.specialization || profile.recent_role || 'Candidate profile'
  const topSkills = profile.skills.slice(0, 5)

  return (
    <section className="rounded-lg border border-border bg-surface p-5 sm:p-6" aria-labelledby="candidate-summary-title">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
        <div className="min-w-0">
          <p className="text-sm font-medium text-accent">Candidate profile</p>
          <h2 id="candidate-summary-title" className="mt-1 break-words font-display text-2xl font-bold text-text-primary">
            {profile.name}
          </h2>
          <p className="mt-1 break-words text-sm text-text-muted">{role}</p>
        </div>
        <ButtonLink to={`/candidate-profile/${candidateId}`} variant="outline" size="sm" className="self-start">
          View full profile
        </ButtonLink>
      </div>

      <dl className="mt-6 grid gap-5 border-t border-border pt-5 lg:grid-cols-[0.7fr_1.6fr_0.7fr]">
        <div>
          <dt className="text-xs font-medium text-text-faint">Experience</dt>
          <dd className="mt-1 text-sm font-semibold text-text-primary">
            {profile.years_experience != null ? `${profile.years_experience} years` : 'Not specified'}
          </dd>
        </div>
        <div className="min-w-0">
          <dt className="text-xs font-medium text-text-faint">Top skills</dt>
          <dd className="mt-1 break-words text-sm font-semibold leading-6 text-text-primary">
            {topSkills.length > 0 ? topSkills.join(' · ') : 'No skills detected'}
          </dd>
        </div>
        <div>
          <dt className="text-xs font-medium text-text-faint">Projects</dt>
          <dd className="mt-1 text-sm font-semibold text-text-primary">{profile.projects.length} detected</dd>
        </div>
      </dl>
    </section>
  )
}

const resumeAnalysisStages = [
  'Reading your CV',
  'Understanding your experience and projects',
  'Building your interview profile',
]

function ResumeAnalysisStatus() {
  return (
    <div id="resume-upload-status" role="status" aria-live="polite" aria-atomic="true">
      <p className="flex items-center gap-2 text-sm font-semibold text-text-primary">
        <Loader2 className="h-4 w-4 shrink-0 animate-spin text-accent" aria-hidden="true" />
        Analyzing your CV
      </p>
      <ol className="mt-3 space-y-3">
        {resumeAnalysisStages.map((stage) => (
          <li key={stage} className="flex items-center gap-3 text-sm text-text-muted">
            <Circle className="h-4 w-4 shrink-0 text-text-faint" aria-hidden="true" />
            <span>{stage}</span>
          </li>
        ))}
      </ol>
      <p className="mt-4 text-xs leading-5 text-text-faint">
        Fresh CV analysis can take 20–30 seconds. Keep this page open while FiPilot prepares your profile.
      </p>
    </div>
  )
}

interface TextInterviewPageProps {
  mode?: InterviewMode
}

export function TextInterviewPage({
  mode = 'text',
}: TextInterviewPageProps) {
  const preferences = useMemo(() => loadInterviewPreferences(), [])
  const { sessionId: routeSessionId } = useParams()
  const navigate = useNavigate()
  const resumeInputRef = useRef<HTMLInputElement>(null)
  const startInFlightRef = useRef(false)
  const submissionInFlightRef = useRef(false)
  const [candidateId, setCandidateId] = useState('')
  const [uploadedCandidateProfile, setUploadedCandidateProfile] = useState<CandidateProfile | null>(null)
  const interviewMode = mode
  const [selectedResumeFile, setSelectedResumeFile] = useState<File | null>(null)
  const [resumeUploadStatus, setResumeUploadStatus] = useState<ResumeUploadStatus>('idle')
  const [isDraggingResume, setIsDraggingResume] = useState(false)
  const [uploadError, setUploadError] = useState<string | null>(null)
  const [backendAvailability, setBackendAvailability] = useState<BackendAvailability>('unknown')
  const [connectivityError, setConnectivityError] = useState<string | null>(null)
  const [language, setLanguage] = useState<InterviewLanguage>(preferences.language)
  const [experienceLevel, setExperienceLevel] = useState<ExperienceLevel>(preferences.experienceLevel)
  const [interviewStyle, setInterviewStyle] = useState<InterviewStyle>(preferences.interviewStyle)
  const [durationInput, setDurationInput] = useState(String(preferences.durationMinutes))
  const [questionCountInput, setQuestionCountInput] = useState(String(preferences.questionCount))
  const [objective, setObjective] = useState(preferences.objective)
  const [sessionId, setSessionId] = useState(routeSessionId ?? '')
  const [interviewStartedAt, setInterviewStartedAt] = useState<string | null>(null)
  const [state, setState] = useState<V2InterviewSessionState | null>(null)
  const [answer, setAnswer] = useState('')
  const [pendingAnswer, setPendingAnswer] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [starting, setStarting] = useState(false)
  const [showPreparationScreen, setShowPreparationScreen] = useState(false)
  const [preparationStatus, setPreparationStatus] = useState<
    'idle' | 'preparing' | 'ready'
  >('idle')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const uploading = resumeUploadStatus === 'uploading'
  const durationMinutes = useMemo(() => parseIntegerSetting(durationInput, 5, 180), [durationInput])
  const questionCount = useMemo(() => parseIntegerSetting(questionCountInput, 1), [questionCountInput])
  const settingsAreValid = durationMinutes !== null && questionCount !== null

  const checkBackendAvailability = useCallback(async () => {
    setBackendAvailability('checking')
    setConnectivityError(null)
    try {
      await api.checkHealth()
      setBackendAvailability('reachable')
    } catch (healthError) {
      setBackendAvailability('unreachable')
      setConnectivityError(getUserFacingError(
        healthError,
        'FiPilot is temporarily unavailable. Please try again.',
      ))
    }
  }, [])

  useEffect(() => {
    void checkBackendAvailability()
  }, [checkBackendAvailability])

  useEffect(() => {
    if (!settingsAreValid || durationMinutes === null || questionCount === null) return
    saveInterviewPreferences({
      language,
      experienceLevel,
      interviewStyle,
      durationMinutes,
      questionCount,
      objective,
    })
  }, [
    durationMinutes,
    experienceLevel,
    interviewStyle,
    language,
    objective,
    questionCount,
    settingsAreValid,
  ])

  useEffect(() => {
    if (!routeSessionId) return
    let cancelled = false
    setLoading(true)
    setError(null)
    api.getV2InterviewSession(routeSessionId)
      .then((response: V2InterviewSessionResponse) => {
        if (cancelled) return
        setSessionId(response.session_id)
        setInterviewStartedAt(response.started_at ?? null)
        setState(response.state)
      })
      .catch((err) => {
        if (!cancelled) setError(getUserFacingError(err, 'The interview could not be loaded. Please try again.'))
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [routeSessionId])

  const progress = useMemo(() => {
    if (!state) return { current: 0, total: questionCount ?? 0 }
    const total = state.interview_config.question_count || questionCount || 0
    const current = Math.min(
      total,
      state.completed_turns.length + (state.current_turn ? 1 : 0)
    )
    return { current, total }
  }, [questionCount, state])

  const isFinished = Boolean(state && !state.current_turn)
  const interviewStartData = useMemo(() => {
    if (durationMinutes === null || questionCount === null) return null
    return {
      candidate_id: candidateId.trim(),
      interview_config: {
        mode: interviewMode,
        language,
        experience_level: experienceLevel,
        duration_minutes: durationMinutes,
        interview_style: interviewStyle,
        question_count: questionCount,
        objective,
      },
    }
  }, [
    candidateId,
    durationMinutes,
    experienceLevel,
    interviewMode,
    interviewStyle,
    language,
    objective,
    questionCount,
  ])

  useEffect(() => {
    if (!uploadedCandidateProfile || !interviewStartData?.candidate_id || state) return

    let active = true
    setPreparationStatus('idle')
    const timer = window.setTimeout(() => {
      setPreparationStatus('preparing')
      void api.prepareV2Interview(interviewStartData)
        .then(() => {
          if (active) setPreparationStatus('ready')
        })
        .catch(() => {
          if (active) setPreparationStatus('idle')
        })
    }, 800)
    return () => {
      active = false
      window.clearTimeout(timer)
    }
  }, [interviewStartData, state, uploadedCandidateProfile])

  useEffect(() => {
    if (!starting) {
      setShowPreparationScreen(false)
      return
    }
    const timer = window.setTimeout(() => setShowPreparationScreen(true), 250)
    return () => window.clearTimeout(timer)
  }, [starting])

  useEffect(() => {
    if (!isFinished || !sessionId) return
    void api.generateInterviewReport(sessionId).catch(() => undefined)
  }, [isFinished, sessionId])

  const acceptResume = (file: File | null): boolean => {
    setError(null)
    setUploadError(null)
    setResumeUploadStatus('idle')
    setCandidateId('')
    setUploadedCandidateProfile(null)

    if (!file) {
      setSelectedResumeFile(null)
      return true
    }

    const validationError = validateResumeFile(file)
    if (validationError) {
      setSelectedResumeFile(null)
      setResumeUploadStatus('error')
      setUploadError(validationError)
      return false
    }

    setSelectedResumeFile(file)
    if (backendAvailability === 'unreachable') void checkBackendAvailability()
    return true
  }

  const selectResume = (event: React.ChangeEvent<HTMLInputElement>) => {
    const accepted = acceptResume(event.target.files?.[0] ?? null)
    if (!accepted) event.target.value = ''
  }

  const dropResume = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    setIsDraggingResume(false)
    if (uploading || loading) return
    acceptResume(event.dataTransfer.files?.[0] ?? null)
  }

  const removeResume = () => {
    if (resumeInputRef.current) resumeInputRef.current.value = ''
    setSelectedResumeFile(null)
    setUploadedCandidateProfile(null)
    setCandidateId('')
    setUploadError(null)
    setResumeUploadStatus('idle')
    setPreparationStatus('idle')
  }

  const uploadSelectedResume = async () => {
    if (!selectedResumeFile || uploading || uploadedCandidateProfile) return
    setResumeUploadStatus('uploading')
    setError(null)
    setUploadError(null)
    setCandidateId('')
    setUploadedCandidateProfile(null)
    try {
      const response = await api.uploadResume(selectedResumeFile)
      setCandidateId(response.candidate_id)
      setUploadedCandidateProfile(response.profile)
      setResumeUploadStatus('success')
    } catch (err) {
      setUploadError(getResumeUploadError(err))
      setResumeUploadStatus('error')
    }
  }

  const startInterview = async (event: FormEvent) => {
    event.preventDefault()
    if (
      !candidateId.trim()
      || !interviewStartData
      || !settingsAreValid
      || startInFlightRef.current
    ) return
    startInFlightRef.current = true
    setStarting(true)
    setLoading(true)
    setError(null)
    try {
      const response: V2InterviewSessionResponse = await api.startV2Interview(
        interviewStartData,
      )
      setSessionId(response.session_id)
      setInterviewStartedAt(response.started_at ?? null)
      setState(response.state)
      const interviewPath = interviewMode === 'voice'
        ? `/speech-interview/${response.session_id}`
        : `/text-interview/${response.session_id}`
      navigate(interviewPath, { replace: true })
    } catch (err) {
      setError(getUserFacingError(err, 'The interview could not be started. Please try again.'))
    } finally {
      startInFlightRef.current = false
      setStarting(false)
      setLoading(false)
    }
  }

  const submitAnswer = async (event: FormEvent) => {
    event.preventDefault()
    const text = answer.trim()
    if (!sessionId || !text || submissionInFlightRef.current || !state?.current_turn) return
    submissionInFlightRef.current = true
    setSubmitting(true)
    setPendingAnswer(text)
    setAnswer('')
    setError(null)
    try {
      const response: V2InterviewSessionResponse = await api.submitV2InterviewAnswer(sessionId, text)
      setInterviewStartedAt((current) => response.started_at ?? current)
      setState(response.state)
      setPendingAnswer(null)
    } catch (err) {
      setPendingAnswer(null)
      setAnswer(text)
      setError(getInterviewAnswerError(err))
    } finally {
      submissionInFlightRef.current = false
      setSubmitting(false)
    }
  }

  if (showPreparationScreen && uploadedCandidateProfile && !state) {
    return (
      <InterviewPreparationScreen
        candidateName={uploadedCandidateProfile.name}
        mode={interviewMode}
        language={language}
        experienceLevel={experienceLevel}
        questionCount={questionCount ?? preferences.questionCount}
        persona={resolveInterviewerPersona(interviewStyle)}
        preparationReady={preparationStatus === 'ready'}
      />
    )
  }

  if (routeSessionId && !state) {
    return (
      <TextInterviewRoomStatus
        error={error}
        onBackToHistory={() => navigate('/interview-history')}
      />
    )
  }

  if (routeSessionId && state) {
    return (
      <TextInterviewRoom
        state={state}
        sessionId={sessionId}
        persona={resolveInterviewerPersona(state.interview_config.interview_style)}
        progress={progress}
        answer={answer}
        pendingAnswer={pendingAnswer}
        submitting={submitting}
        startedAt={interviewStartedAt}
        error={error}
        onAnswerChange={setAnswer}
        onSubmit={submitAnswer}
        onViewReport={() => navigate(`/text-interview/${sessionId}/report`)}
        onBackToHistory={() => navigate('/interview-history')}
      />
    )
  }

  return (
    <div className="mx-auto max-w-5xl space-y-8 pb-10">
      <header>
        <h1 className="font-display text-3xl font-bold tracking-tight-display text-text-primary">
          Prepare your interview
        </h1>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-text-muted">
          Upload your CV, review the profile FiPilot creates, choose your settings, and start when you are ready.
          {' '}This setup will start a {interviewMode === 'voice' ? 'speech' : 'text'} interview.
        </p>
      </header>

      {error && (
        <div role="alert" className="rounded-lg border border-danger/30 bg-danger/10 px-4 py-3 text-sm text-danger">
          {error}
        </div>
      )}

      {!state ? (
        <div className="space-y-5">
          <Card className="shadow-none">
            <CardHeader>
              <div>
                <h2 className="text-lg font-semibold text-text-primary">Upload your CV</h2>
                <p className="mt-1 text-sm leading-6 text-text-muted">
                  FiPilot uses your CV to personalize interview questions.
                </p>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <Label htmlFor="resume-file" className="sr-only">Resume file</Label>
              <input
                ref={resumeInputRef}
                id="resume-file"
                type="file"
                accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                onChange={selectResume}
                disabled={uploading || loading}
                aria-describedby="resume-upload-status"
                tabIndex={-1}
                className="sr-only"
              />

              {!uploadedCandidateProfile && (
                <div
                  className={`rounded-lg border border-dashed px-5 py-7 text-center transition-colors duration-150 ${
                    isDraggingResume ? 'border-accent bg-accent-soft' : 'border-border bg-surface-raised'
                  }`}
                  onDragEnter={(event) => {
                    event.preventDefault()
                    if (!uploading && !loading) setIsDraggingResume(true)
                  }}
                  onDragOver={(event) => event.preventDefault()}
                  onDragLeave={() => setIsDraggingResume(false)}
                  onDrop={dropResume}
                >
                  <Upload className="mx-auto h-6 w-6 text-accent" aria-hidden="true" />
                  <p className="mt-3 text-sm font-semibold text-text-primary">Choose a CV or drag it here</p>
                  <p id="resume-file-help" className="mt-1 text-xs text-text-faint">PDF or DOCX, up to 10 MB</p>
                  <Button
                    type="button"
                    variant={selectedResumeFile ? 'secondary' : 'primary'}
                    className="mt-4"
                    onClick={() => resumeInputRef.current?.click()}
                    disabled={uploading || loading}
                  >
                    Choose CV
                  </Button>
                </div>
              )}

              {selectedResumeFile && (
                <div className="flex min-w-0 flex-col gap-3 rounded-lg border border-border bg-surface-raised px-3 py-3 sm:flex-row sm:items-center">
                  <div className="flex min-w-0 flex-1 items-center gap-2">
                    <FileText className="h-4 w-4 shrink-0 text-accent" aria-hidden="true" />
                    <span className="min-w-0 flex-1 truncate text-sm text-text-primary" title={selectedResumeFile.name}>
                      {selectedResumeFile.name}
                    </span>
                    <span className="shrink-0 text-xs text-text-faint">{formatFileSize(selectedResumeFile.size)}</span>
                  </div>
                  <Button type="button" variant="ghost" size="sm" onClick={removeResume} disabled={uploading || loading}>
                    {uploadedCandidateProfile ? 'Choose another CV' : 'Remove CV'}
                  </Button>
                </div>
              )}

              {connectivityError && (
                <div role="alert" className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-danger/30 bg-danger/10 px-3 py-3 text-sm text-danger">
                  <span>{connectivityError}</span>
                  <Button type="button" variant="outline" size="sm" onClick={() => void checkBackendAvailability()} disabled={backendAvailability === 'checking'}>
                    Retry connection
                  </Button>
                </div>
              )}

              {uploading ? (
                <ResumeAnalysisStatus />
              ) : uploadedCandidateProfile ? (
                <p id="resume-upload-status" role="status" className="flex items-center gap-2 text-sm text-success">
                  <CheckCircle2 className="h-4 w-4 shrink-0" aria-hidden="true" />
                  Profile ready. Review the summary and choose your interview settings.
                </p>
              ) : (
                <p id="resume-upload-status" className="text-sm text-text-muted">
                  Start by choosing the CV you want to practice with.
                </p>
              )}

              {uploadError && (
                <div role="alert" className="rounded-lg border border-danger/30 bg-danger/10 px-3 py-3 text-sm text-danger">
                  {uploadError}
                </div>
              )}

              {selectedResumeFile && !uploadedCandidateProfile && !uploading && (
                <Button
                  type="button"
                  size="lg"
                  onClick={() => void uploadSelectedResume()}
                  disabled={loading || backendAvailability === 'unreachable'}
                  className="w-full sm:w-auto"
                >
                  <Upload className="h-4 w-4" aria-hidden="true" />
                  {resumeUploadStatus === 'error' ? 'Try analysis again' : 'Upload and analyze'}
                </Button>
              )}
            </CardContent>
          </Card>

          {uploadedCandidateProfile && (
            <CandidateProfilePreview profile={uploadedCandidateProfile} candidateId={candidateId} />
          )}

          {uploadedCandidateProfile && (
          <form onSubmit={startInterview}>
            <Card className="shadow-none">
              <CardHeader>
                <div>
                  <h2 className="text-lg font-semibold text-text-primary">Choose interview settings</h2>
                  <p className="mt-1 text-sm leading-6 text-text-muted">Use the options supported by this interview mode.</p>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid gap-4 lg:grid-cols-2">
                  <div>
                    <Label htmlFor="interview-style">Interview type</Label>
                    <Select
                      id="interview-style"
                      value={interviewStyle}
                      onChange={(event) => setInterviewStyle(event.target.value as InterviewStyle)}
                      disabled={loading || uploading}
                    >
                      <option value="technical">Technical</option>
                      <option value="behavioral">Behavioral</option>
                      <option value="mixed">Mixed</option>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="interview-experience-level">Difficulty</Label>
                    <Select
                      id="interview-experience-level"
                      value={experienceLevel}
                      onChange={(event) => setExperienceLevel(event.target.value as ExperienceLevel)}
                      disabled={loading || uploading}
                    >
                      <option value="intern">Intern</option>
                      <option value="junior">Junior</option>
                      <option value="middle">Middle</option>
                      <option value="senior">Senior</option>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="interview-language">Language</Label>
                    <Select
                      id="interview-language"
                      value={language}
                      onChange={(event) => setLanguage(event.target.value as InterviewLanguage)}
                      disabled={loading || uploading}
                    >
                      <option value="vi">Vietnamese</option>
                      <option value="en">English</option>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="interview-question-count">Number of questions</Label>
                    <Input
                      id="interview-question-count"
                      type="number"
                      min={1}
                      required
                      value={questionCountInput}
                      onChange={(event) => setQuestionCountInput(event.target.value)}
                      disabled={loading || uploading}
                      aria-invalid={questionCount === null}
                      aria-describedby={questionCount === null ? 'interview-question-count-error' : 'interview-duration-estimate'}
                    />
                    {questionCount === null && (
                      <p id="interview-question-count-error" className="mt-1.5 text-xs text-danger">
                        Enter a whole number of at least 1.
                      </p>
                    )}
                  </div>
                </div>

                {questionCount !== null && durationMinutes !== null && (
                  <p id="interview-duration-estimate" className="border-y border-border py-3 text-sm font-medium text-text-primary">
                    {questionCount} questions <span className="text-text-faint">·</span> about {durationMinutes} minutes
                  </p>
                )}

                <details className="border-b border-border pb-4">
                  <summary className="cursor-pointer text-sm font-medium text-text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent">
                    More options
                  </summary>
                  <div className="mt-4 grid gap-4 lg:grid-cols-2">
                    <div>
                      <Label htmlFor="interview-duration">Duration</Label>
                      <Input
                        id="interview-duration"
                        type="number"
                        min={5}
                        max={180}
                        required
                        value={durationInput}
                        onChange={(event) => setDurationInput(event.target.value)}
                        disabled={loading || uploading}
                        aria-invalid={durationMinutes === null}
                        aria-describedby={durationMinutes === null ? 'interview-duration-error' : undefined}
                      />
                      {durationMinutes === null && (
                        <p id="interview-duration-error" className="mt-1.5 text-xs text-danger">Enter a whole number from 5 to 180.</p>
                      )}
                    </div>
                    <div>
                      <Label htmlFor="interview-objective">Objective</Label>
                      <Textarea id="interview-objective" rows={3} value={objective} onChange={(event) => setObjective(event.target.value)} disabled={loading || uploading} />
                    </div>
                  </div>
                </details>

                <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
                  <p className="max-w-2xl text-sm leading-6 text-text-muted">
                    Your AI interviewer will ask questions based on your CV and adapt follow-up questions to your answers.
                  </p>
                  <Button type="submit" size="lg" disabled={loading || uploading || !settingsAreValid} className="w-full shrink-0 sm:w-auto">
                    {starting ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <ArrowRight className="h-4 w-4" aria-hidden="true" />}
                    {starting ? 'Preparing interview' : 'Start Interview'}
                  </Button>
                </div>
              </CardContent>
            </Card>

          </form>
          )}
        </div>
      ) : null}
    </div>
  )
}

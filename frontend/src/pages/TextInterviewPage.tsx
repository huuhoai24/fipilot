import React, { FormEvent, useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  ArrowRight,
  BriefcaseBusiness,
  CheckCircle2,
  ClipboardList,
  FileText,
  FolderKanban,
  GraduationCap,
  Loader2,
  Upload,
  UserRound,
} from 'lucide-react'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
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
import { getResumeUploadError, getUserFacingError } from '@/lib/userFacingError'
import type {
  CandidateEducation,
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

function educationLabel(education: CandidateEducation): string {
  return [education.degree, education.field_of_study, education.institution]
    .filter(Boolean)
    .join(' - ')
}

function CandidateProfilePreview({
  profile,
  confidenceScore,
}: {
  profile: CandidateProfile
  confidenceScore: number
}) {
  const educationItems = Array.isArray(profile.education)
    ? profile.education.map(educationLabel).filter(Boolean)
    : profile.education
      ? [profile.education]
      : []
  const evidenceItems = profile.skill_evidence.filter(
    (item) => item.skill || item.evidence.length > 0
  )

  return (
    <Card>
      <CardHeader>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <CardTitle>Extracted Candidate Profile</CardTitle>
          <Badge variant="success">{Math.round(confidenceScore * 100)}% confidence</Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex items-start gap-3">
          <UserRound className="mt-0.5 h-5 w-5 shrink-0 text-accent" />
          <div className="min-w-0">
            <div className="break-words text-sm font-semibold text-text-primary">{profile.name}</div>
            {(profile.specialization || profile.recent_role) && (
              <div className="mt-1 break-words text-sm text-text-muted">
                {[profile.specialization, profile.recent_role].filter(Boolean).join(' / ')}
              </div>
            )}
            {profile.years_experience != null && (
              <div className="mt-1 text-xs text-text-faint">
                {profile.years_experience} years of experience
              </div>
            )}
          </div>
        </div>

        {profile.skills.length > 0 && (
          <section aria-labelledby="profile-skills-title">
            <h3 id="profile-skills-title" className="mb-2 text-xs font-medium uppercase text-text-faint">
              Skills
            </h3>
            <div className="flex flex-wrap gap-2">
              {profile.skills.map((skill) => <Badge key={skill} variant="accent">{skill}</Badge>)}
            </div>
          </section>
        )}

        {profile.projects.length > 0 && (
          <section aria-labelledby="profile-projects-title">
            <div className="mb-3 flex items-center gap-2">
              <FolderKanban className="h-4 w-4 text-accent" />
              <h3 id="profile-projects-title" className="text-xs font-medium uppercase text-text-faint">
                Projects
              </h3>
            </div>
            <div className="divide-y divide-border">
              {profile.projects.map((project, index) => (
                <div key={`${project.name}-${index}`} className="py-3 first:pt-0 last:pb-0">
                  {(project.name || project.role) && (
                    <div className="break-words text-sm font-medium text-text-primary">
                      {[project.name, project.role].filter(Boolean).join(' / ')}
                    </div>
                  )}
                  {project.description && (
                    <p className="mt-1 break-words text-sm leading-6 text-text-muted">{project.description}</p>
                  )}
                  {project.technologies.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1.5">
                      {project.technologies.map((technology) => (
                        <Badge key={technology} variant="default">{technology}</Badge>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {profile.experiences.length > 0 && (
          <section aria-labelledby="profile-experience-title">
            <div className="mb-3 flex items-center gap-2">
              <BriefcaseBusiness className="h-4 w-4 text-accent" />
              <h3 id="profile-experience-title" className="text-xs font-medium uppercase text-text-faint">
                Experience
              </h3>
            </div>
            <div className="divide-y divide-border">
              {profile.experiences.map((experience, index) => (
                <div key={`${experience.company}-${experience.title}-${index}`} className="py-3 first:pt-0 last:pb-0">
                  <div className="break-words text-sm font-medium text-text-primary">
                    {[experience.title, experience.company].filter(Boolean).join(' / ')}
                  </div>
                  {(experience.start_date || experience.end_date) && (
                    <div className="mt-1 text-xs text-text-faint">
                      {[experience.start_date, experience.end_date].filter(Boolean).join(' - ')}
                    </div>
                  )}
                  {experience.description && (
                    <p className="mt-1 break-words text-sm leading-6 text-text-muted">{experience.description}</p>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {educationItems.length > 0 && (
          <section aria-labelledby="profile-education-title">
            <div className="mb-3 flex items-center gap-2">
              <GraduationCap className="h-4 w-4 text-accent" />
              <h3 id="profile-education-title" className="text-xs font-medium uppercase text-text-faint">
                Education
              </h3>
            </div>
            <ul className="space-y-2 text-sm text-text-muted">
              {educationItems.map((item, index) => <li key={`${item}-${index}`} className="break-words">{item}</li>)}
            </ul>
          </section>
        )}

        {evidenceItems.length > 0 && (
          <section aria-labelledby="profile-evidence-title">
            <h3 id="profile-evidence-title" className="mb-3 text-xs font-medium uppercase text-text-faint">
              Skill Evidence
            </h3>
            <div className="space-y-3">
              {evidenceItems.map((item, index) => (
                <div key={`${item.skill}-${index}`}>
                  {item.skill && <div className="text-sm font-medium text-text-primary">{item.skill}</div>}
                  {item.evidence.length > 0 && (
                    <p className="mt-1 break-words text-sm leading-6 text-text-muted">
                      {item.evidence.slice(0, 2).join(' ')}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}
      </CardContent>
    </Card>
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
  const [candidateId, setCandidateId] = useState('')
  const [uploadedCandidateProfile, setUploadedCandidateProfile] = useState<CandidateProfile | null>(null)
  const [profileConfidence, setProfileConfidence] = useState(0)
  const interviewMode = mode
  const [selectedResumeFile, setSelectedResumeFile] = useState<File | null>(null)
  const [resumeUploadStatus, setResumeUploadStatus] = useState<ResumeUploadStatus>('idle')
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
        'Backend service is unavailable. Please check the API connection.',
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

  const selectResume = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null
    setError(null)
    setUploadError(null)
    setResumeUploadStatus('idle')
    setCandidateId('')
    setUploadedCandidateProfile(null)
    setProfileConfidence(0)

    if (!file) {
      setSelectedResumeFile(null)
      return
    }

    const validationError = validateResumeFile(file)
    if (validationError) {
      setSelectedResumeFile(null)
      setResumeUploadStatus('error')
      setUploadError(validationError)
      event.target.value = ''
      return
    }

    setSelectedResumeFile(file)
    if (backendAvailability === 'unreachable') void checkBackendAvailability()
  }

  const removeResume = () => {
    if (resumeInputRef.current) resumeInputRef.current.value = ''
    setSelectedResumeFile(null)
    setUploadedCandidateProfile(null)
    setCandidateId('')
    setProfileConfidence(0)
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
    setProfileConfidence(0)
    try {
      const response = await api.uploadResume(selectedResumeFile)
      setCandidateId(response.candidate_id)
      setUploadedCandidateProfile(response.profile)
      setProfileConfidence(response.confidence_score)
      setResumeUploadStatus('success')
    } catch (err) {
      setUploadError(getResumeUploadError(err))
      setResumeUploadStatus('error')
    }
  }

  const startInterview = async (event: FormEvent) => {
    event.preventDefault()
    if (!candidateId.trim() || !interviewStartData || !settingsAreValid) return
    setStarting(true)
    setLoading(true)
    setError(null)
    try {
      const response: V2InterviewSessionResponse = await api.startV2Interview(
        interviewStartData,
      )
      setSessionId(response.session_id)
      setState(response.state)
      const interviewPath = interviewMode === 'voice'
        ? `/speech-interview/${response.session_id}`
        : `/text-interview/${response.session_id}`
      navigate(interviewPath, { replace: true })
    } catch (err) {
      setError(getUserFacingError(err, 'The interview could not be started. Please try again.'))
    } finally {
      setStarting(false)
      setLoading(false)
    }
  }

  const submitAnswer = async (event: FormEvent) => {
    event.preventDefault()
    const text = answer.trim()
    if (!sessionId || !text || submitting || !state?.current_turn) return
    setSubmitting(true)
    setPendingAnswer(text)
    setAnswer('')
    setError(null)
    try {
      const response: V2InterviewSessionResponse = await api.submitV2InterviewAnswer(sessionId, text)
      setState(response.state)
      setPendingAnswer(null)
    } catch (err) {
      setPendingAnswer(null)
      setAnswer(text)
      setError(getUserFacingError(err, 'Your answer could not be submitted. Please try again.'))
    } finally {
      setSubmitting(false)
    }
  }

  if (showPreparationScreen && uploadedCandidateProfile && !state) {
    return (
      <InterviewPreparationScreen
        candidateName={uploadedCandidateProfile.name}
        mode={interviewMode}
        experienceLevel={experienceLevel}
        questionCount={questionCount ?? preferences.questionCount}
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
        persona={resolveInterviewerPersona(state.interview_config.interview_style)}
        progress={progress}
        answer={answer}
        pendingAnswer={pendingAnswer}
        submitting={submitting}
        error={error}
        onAnswerChange={setAnswer}
        onSubmit={submitAnswer}
        onViewReport={() => navigate(`/text-interview/${sessionId}/report`)}
        onBackToHistory={() => navigate('/interview-history')}
      />
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="font-display text-2xl font-bold tracking-tight-display text-text-primary">
            {interviewMode === 'voice' ? 'Speech Interview' : 'Text Interview'}
          </h1>
          <p className="mt-1 text-sm text-text-muted">
            {interviewMode === 'voice'
              ? 'CV-driven conversational interview with realtime speech.'
              : 'CV-driven interview room using adaptive V2 APIs.'}
          </p>
        </div>
        {sessionId && (
          <Badge variant={isFinished ? 'success' : 'accent'}>
            {isFinished ? 'Completed' : `Session ${sessionId}`}
          </Badge>
        )}
      </div>

      {error && (
        <div className="rounded-lg border border-danger/30 bg-danger/10 px-4 py-3 text-sm text-danger">
          {error}
        </div>
      )}

      {!state ? (
        <div className="space-y-5">
          <Card>
            <CardHeader>
              <CardTitle>Candidate Profile</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-[minmax(0,1fr)_auto] md:items-end">
                <div className="min-w-0">
                  <Label htmlFor="resume-file">Resume file</Label>
                  <Input
                    ref={resumeInputRef}
                    id="resume-file"
                    type="file"
                    accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    onChange={selectResume}
                    disabled={uploading || loading}
                    aria-describedby="resume-file-help resume-upload-status"
                    className="file:mr-3 file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-text-primary"
                  />
                  <p id="resume-file-help" className="mt-1.5 text-xs text-text-faint">
                    PDF or DOCX, up to 10 MB.
                  </p>
                </div>
                <Button
                  type="button"
                  onClick={() => void uploadSelectedResume()}
                  disabled={
                    !selectedResumeFile
                    || uploading
                    || loading
                    || backendAvailability === 'unreachable'
                    || Boolean(uploadedCandidateProfile)
                  }
                  className="w-full md:w-auto"
                >
                  {uploading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : uploadedCandidateProfile ? (
                    <CheckCircle2 className="h-4 w-4" />
                  ) : (
                    <Upload className="h-4 w-4" />
                  )}
                  {uploading ? 'Analyzing...' : uploadedCandidateProfile ? 'Analyzed' : 'Upload and Analyze'}
                </Button>
              </div>

              {selectedResumeFile && (
                <div className="flex min-w-0 items-center gap-2 rounded-lg border border-border bg-surface-raised px-3 py-2.5">
                  <FileText className="h-4 w-4 shrink-0 text-accent" />
                  <span className="min-w-0 flex-1 truncate text-sm text-text-primary">{selectedResumeFile.name}</span>
                  <span className="shrink-0 text-xs text-text-faint">{formatFileSize(selectedResumeFile.size)}</span>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={removeResume}
                    disabled={uploading || loading}
                  >
                    Remove resume
                  </Button>
                </div>
              )}

              {connectivityError && (
                <div role="alert" className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-danger/30 bg-danger/10 px-3 py-2.5 text-sm text-danger">
                  <span>{connectivityError}</span>
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => void checkBackendAvailability()}
                    disabled={backendAvailability === 'checking'}
                  >
                    Retry connection
                  </Button>
                </div>
              )}

              <div id="resume-upload-status" aria-live="polite" aria-atomic="true">
                {uploading ? (
                  <p className="text-sm text-text-muted">Uploading and extracting the candidate profile...</p>
                ) : uploadedCandidateProfile ? (
                  <p className="flex items-center gap-2 text-sm text-success">
                    <CheckCircle2 className="h-4 w-4 shrink-0" />
                    Candidate profile is ready. Review it before starting the interview.
                  </p>
                ) : (
                  <p className="text-sm text-text-muted">
                    No candidate profile is loaded. Upload your CV to begin.
                  </p>
                )}
              </div>

              {uploadError && (
                <div role="alert" className="rounded-lg border border-danger/30 bg-danger/10 px-3 py-2.5 text-sm text-danger">
                  {uploadError}
                </div>
              )}
            </CardContent>
          </Card>

          {uploadedCandidateProfile && (
            <CandidateProfilePreview profile={uploadedCandidateProfile} confidenceScore={profileConfidence} />
          )}

          <form onSubmit={startInterview} className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_320px]">
            <Card>
              <CardHeader>
                <CardTitle>Interview Setup</CardTitle>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="grid gap-4 md:grid-cols-2">
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
                    <Label htmlFor="interview-experience-level">Experience Level</Label>
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
                    <Label htmlFor="interview-style">Interview Style</Label>
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
                      <p id="interview-duration-error" className="mt-1.5 text-xs text-danger">
                        Enter a whole number from 5 to 180.
                      </p>
                    )}
                  </div>
                  <div>
                    <Label htmlFor="interview-question-count">Question Count</Label>
                    <Input
                      id="interview-question-count"
                      type="number"
                      min={1}
                      required
                      value={questionCountInput}
                      onChange={(event) => setQuestionCountInput(event.target.value)}
                      disabled={loading || uploading}
                      aria-invalid={questionCount === null}
                      aria-describedby={questionCount === null ? 'interview-question-count-error' : undefined}
                    />
                    {questionCount === null && (
                      <p id="interview-question-count-error" className="mt-1.5 text-xs text-danger">
                        Enter a whole number of at least 1.
                      </p>
                    )}
                  </div>
                </div>
                <div>
                  <Label htmlFor="interview-objective">Objective</Label>
                  <Textarea
                    id="interview-objective"
                    rows={3}
                    value={objective}
                    onChange={(event) => setObjective(event.target.value)}
                    disabled={loading || uploading}
                  />
                </div>
                <div className="flex justify-end">
                  <Button
                    type="submit"
                    disabled={loading || uploading || !candidateId || !uploadedCandidateProfile || !settingsAreValid}
                  >
                    {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4" />}
                    Start
                  </Button>
                </div>
              </CardContent>
            </Card>

            <div className="rounded-lg border border-border bg-surface px-5 py-4">
              <div className="flex items-center gap-2 text-sm font-semibold text-text-primary">
                <ClipboardList className="h-4 w-4 text-accent" />
                Session Setup
              </div>
              <div className="mt-4 space-y-3 text-sm text-text-muted">
                <div className="flex justify-between gap-3">
                  <span>Mode</span>
                  <span className="font-medium text-text-primary">
                    {interviewMode === 'text' ? 'Text' : 'Speech'}
                  </span>
                </div>
                <div className="flex justify-between gap-3">
                  <span>Candidate</span>
                  <span className="max-w-[180px] truncate font-medium text-text-primary">
                    {uploadedCandidateProfile?.name ?? 'CV required'}
                  </span>
                </div>
                <div className="flex justify-between gap-3">
                  <span>Language</span>
                  <span className="font-medium text-text-primary">{language.toUpperCase()}</span>
                </div>
                <div className="flex justify-between gap-3">
                  <span>Level</span>
                  <span className="font-medium text-text-primary capitalize">{experienceLevel}</span>
                </div>
                <div className="flex justify-between gap-3">
                  <span>Questions</span>
                  <span className="font-medium text-text-primary">{questionCount ?? '—'}</span>
                </div>
                <div className="flex justify-between gap-3">
                  <span>Minutes</span>
                  <span className="font-medium text-text-primary">{durationMinutes ?? '—'}</span>
                </div>
              </div>
            </div>
          </form>
        </div>
      ) : null}
    </div>
  )
}

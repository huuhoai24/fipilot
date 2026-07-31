import React, { FormEvent, useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  ArrowRight,
  BriefcaseBusiness,
  CheckCircle2,
  ClipboardList,
  FileText,
  FolderKanban,
  GraduationCap,
  History,
  Loader2,
  MessageSquareText,
  Send,
  Upload,
  UserRound,
} from 'lucide-react'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Input, Label, Select, Textarea } from '@/components/ui/Input'
import { InterviewPreparationScreen } from '@/components/interview/InterviewPreparationScreen'
import { api } from '@/lib/api'
import { loadInterviewPreferences } from '@/lib/interviewPreferences'
import type {
  CandidateEducation,
  CandidateProfile,
  ExperienceLevel,
  InterviewMode,
  InterviewLanguage,
  InterviewStyle,
  V2InterviewQuestion,
  V2InterviewSessionResponse,
  V2InterviewSessionState,
  V2InterviewTurn,
} from '@/types'

const MAX_RESUME_BYTES = 10 * 1024 * 1024
const RESUME_EXTENSIONS = new Set(['pdf', 'docx'])
const RESUME_MIME_TYPES = new Set([
  'application/pdf',
  'application/x-pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
])

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

function getQuestion(turn?: V2InterviewTurn | null): V2InterviewQuestion | null {
  if (!turn || typeof turn.question === 'string') return null
  return turn.question
}

function questionText(turn?: V2InterviewTurn | null): string {
  if (!turn) return ''
  return typeof turn.question === 'string' ? turn.question : turn.question.question
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
  const [candidateId, setCandidateId] = useState('')
  const [candidateProfile, setCandidateProfile] = useState<CandidateProfile | null>(null)
  const [profileConfidence, setProfileConfidence] = useState(0)
  const interviewMode = mode
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState<string | null>(null)
  const [language, setLanguage] = useState<InterviewLanguage>(preferences.language)
  const [experienceLevel, setExperienceLevel] = useState<ExperienceLevel>(preferences.experienceLevel)
  const [interviewStyle, setInterviewStyle] = useState<InterviewStyle>(preferences.interviewStyle)
  const [durationMinutes, setDurationMinutes] = useState(preferences.durationMinutes)
  const [questionCount, setQuestionCount] = useState(preferences.questionCount)
  const [objective, setObjective] = useState(preferences.objective)
  const [sessionId, setSessionId] = useState(routeSessionId ?? '')
  const [state, setState] = useState<V2InterviewSessionState | null>(null)
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [starting, setStarting] = useState(false)
  const [showPreparationScreen, setShowPreparationScreen] = useState(false)
  const [preparationStatus, setPreparationStatus] = useState<
    'idle' | 'preparing' | 'ready'
  >('idle')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

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
        if (!cancelled) setError(err instanceof Error ? err.message : 'Failed to load interview')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [routeSessionId])

  const progress = useMemo(() => {
    if (!state) return { current: 0, total: questionCount, pct: 0 }
    const total = state.interview_config.question_count || questionCount
    const current = Math.min(
      total,
      state.completed_turns.length + (state.current_turn ? 1 : 0)
    )
    return { current, total, pct: total ? Math.round((current / total) * 100) : 0 }
  }, [questionCount, state])

  const currentQuestion = getQuestion(state?.current_turn)
  const isFinished = Boolean(state && !state.current_turn)
  const interviewStartData = useMemo(() => ({
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
  }), [
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
    if (!candidateProfile || !interviewStartData.candidate_id || state) return

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
  }, [candidateProfile, interviewStartData, state])

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
    setCandidateId('')
    setCandidateProfile(null)
    setProfileConfidence(0)

    if (!file) {
      setSelectedFile(null)
      return
    }

    const validationError = validateResumeFile(file)
    if (validationError) {
      setSelectedFile(null)
      setUploadError(validationError)
      event.target.value = ''
      return
    }

    setSelectedFile(file)
  }

  const uploadSelectedResume = async () => {
    if (!selectedFile || uploading || candidateProfile) return
    setUploading(true)
    setError(null)
    setUploadError(null)
    setCandidateId('')
    setCandidateProfile(null)
    setProfileConfidence(0)
    try {
      const response = await api.uploadResume(selectedFile)
      setCandidateId(response.candidate_id)
      setCandidateProfile(response.profile)
      setProfileConfidence(response.confidence_score)
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : 'Resume analysis failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  const startInterview = async (event: FormEvent) => {
    event.preventDefault()
    if (!candidateId.trim()) return
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
      setError(err instanceof Error ? err.message : 'Failed to start interview')
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
    setError(null)
    try {
      const response: V2InterviewSessionResponse = await api.submitV2InterviewAnswer(sessionId, text)
      setState(response.state)
      setAnswer('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit answer')
    } finally {
      setSubmitting(false)
    }
  }

  if (showPreparationScreen && candidateProfile && !state) {
    return (
      <InterviewPreparationScreen
        candidateName={candidateProfile.name}
        mode={interviewMode}
        experienceLevel={experienceLevel}
        questionCount={questionCount}
        preparationReady={preparationStatus === 'ready'}
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
                  disabled={!selectedFile || uploading || loading || Boolean(candidateProfile)}
                  className="w-full md:w-auto"
                >
                  {uploading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : candidateProfile ? (
                    <CheckCircle2 className="h-4 w-4" />
                  ) : (
                    <Upload className="h-4 w-4" />
                  )}
                  {uploading ? 'Analyzing...' : candidateProfile ? 'Analyzed' : 'Upload and Analyze'}
                </Button>
              </div>

              {selectedFile && (
                <div className="flex min-w-0 items-center gap-2 rounded-lg border border-border bg-surface-raised px-3 py-2.5">
                  <FileText className="h-4 w-4 shrink-0 text-accent" />
                  <span className="min-w-0 flex-1 truncate text-sm text-text-primary">{selectedFile.name}</span>
                  <span className="shrink-0 text-xs text-text-faint">{formatFileSize(selectedFile.size)}</span>
                </div>
              )}

              <div id="resume-upload-status" aria-live="polite" aria-atomic="true">
                {uploading ? (
                  <p className="text-sm text-text-muted">Uploading and extracting the candidate profile...</p>
                ) : candidateProfile ? (
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

          {candidateProfile && (
            <CandidateProfilePreview profile={candidateProfile} confidenceScore={profileConfidence} />
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
                      value={durationMinutes}
                      onChange={(event) => setDurationMinutes(Number(event.target.value) || 30)}
                      disabled={loading || uploading}
                    />
                  </div>
                  <div>
                    <Label htmlFor="interview-question-count">Question Count</Label>
                    <Input
                      id="interview-question-count"
                      type="number"
                      min={1}
                      value={questionCount}
                      onChange={(event) => setQuestionCount(Number(event.target.value) || 10)}
                      disabled={loading || uploading}
                    />
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
                    disabled={loading || uploading || !candidateId}
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
                    {candidateProfile?.name ?? 'CV required'}
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
                  <span className="font-medium text-text-primary">{questionCount}</span>
                </div>
                <div className="flex justify-between gap-3">
                  <span>Minutes</span>
                  <span className="font-medium text-text-primary">{durationMinutes}</span>
                </div>
              </div>
            </div>
          </form>
        </div>
      ) : (
        <div className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_360px]">
          <section className="space-y-5">
            <div className="rounded-lg border border-border bg-surface p-5">
              <div className="mb-4 flex items-center justify-between gap-4">
                <div>
                  <div className="text-xs font-medium uppercase text-text-faint">Progress</div>
                  <div className="mt-1 text-sm text-text-muted">
                    Question {progress.current} of {progress.total}
                  </div>
                </div>
                <Badge variant={currentQuestion?.difficulty === 'hard' ? 'warning' : 'accent'}>
                  {currentQuestion?.difficulty ?? 'done'}
                </Badge>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-surface-raised">
                <div className="h-full bg-accent transition-[width] duration-300" style={{ width: `${progress.pct}%` }} />
              </div>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>{isFinished ? 'Interview Complete' : currentQuestion?.topic || state.current_turn?.topic}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-5">
                {isFinished ? (
                  <div className="flex items-start gap-3 rounded-lg border border-success/30 bg-success/10 p-4">
                    <CheckCircle2 className="mt-0.5 h-5 w-5 text-success" />
                    <div>
                      <div className="text-sm font-semibold text-text-primary">All current questions are complete.</div>
                      <div className="mt-1 text-sm text-text-muted">
                        Completed turns: {state.completed_turns.length}
                      </div>
                      <div className="mt-4 flex flex-wrap gap-2">
                        <Button type="button" onClick={() => navigate(`/text-interview/${sessionId}/report`)}>
                          <FileText className="h-4 w-4" />
                          View Final Report
                        </Button>
                        <Button type="button" variant="secondary" onClick={() => navigate('/interview-history')}>
                          <History className="h-4 w-4" />
                          Back to History
                        </Button>
                      </div>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="rounded-lg border border-border bg-surface-raised p-5">
                      <div className="mb-3 flex items-center gap-2 text-xs font-medium uppercase text-text-faint">
                        <MessageSquareText className="h-4 w-4 text-accent" />
                        Current Question
                      </div>
                      <p className="text-base leading-7 text-text-primary">{questionText(state.current_turn)}</p>
                    </div>

                    {currentQuestion?.expected_answer_points?.length ? (
                      <div>
                        <div className="mb-2 text-xs font-medium uppercase text-text-faint">Expected Signals</div>
                        <div className="flex flex-wrap gap-2">
                          {currentQuestion.expected_answer_points.map((point) => (
                            <Badge key={point} variant="default">{point}</Badge>
                          ))}
                        </div>
                      </div>
                    ) : null}

                    <form onSubmit={submitAnswer} className="space-y-3">
                      <div>
                        <Label htmlFor="interview-answer">Answer</Label>
                        <Textarea
                          id="interview-answer"
                          rows={8}
                          value={answer}
                          onChange={(event) => setAnswer(event.target.value)}
                          disabled={submitting}
                          placeholder="Type your answer..."
                        />
                      </div>
                      <div className="flex justify-end">
                        <Button type="submit" disabled={submitting || !answer.trim()}>
                          {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                          Submit Answer
                        </Button>
                      </div>
                    </form>
                  </>
                )}
              </CardContent>
            </Card>
          </section>

          <aside className="space-y-5">
            <div className="rounded-lg border border-border bg-surface p-5">
              <div className="text-sm font-semibold text-text-primary">
                {state.candidate_profile.name}
              </div>
              <div className="mt-1 text-xs text-text-muted">
                {state.candidate_profile.specialization || 'Candidate'}
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                {state.candidate_profile.skills.slice(0, 8).map((skill) => (
                  <Badge key={skill} variant="accent">{skill}</Badge>
                ))}
              </div>
            </div>

            <div className="rounded-lg border border-border bg-surface p-5">
              <div className="mb-3 text-sm font-semibold text-text-primary">Completed Turns</div>
              <div className="space-y-3">
                {state.completed_turns.length === 0 ? (
                  <div className="text-sm text-text-muted">No completed turns yet.</div>
                ) : (
                  state.completed_turns.map((turn, index) => (
                    <div key={`${turn.turn_id}-${index}`} className="rounded-lg border border-border bg-surface-raised p-3">
                      <div className="mb-1 flex items-center justify-between gap-2">
                        <span className="truncate text-xs font-medium text-text-primary">{turn.topic || `Turn ${index + 1}`}</span>
                        <Badge variant="success">{turn.evaluation?.overall_score ?? 0}/10</Badge>
                      </div>
                      {turn.evaluation?.feedback && (
                        <p className="line-clamp-3 text-xs leading-5 text-text-muted">{turn.evaluation.feedback}</p>
                      )}
                    </div>
                  ))
                )}
              </div>
            </div>
          </aside>
        </div>
      )}
    </div>
  )
}

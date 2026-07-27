import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Button, ButtonLink } from '@/components/ui/Button'
import {
  InterviewReadinessSummary,
  profileTargetForFieldPath,
} from '@/components/candidate-profile/InterviewReadinessSummary'
import { ApiError, api } from '@/lib/api'
import type {
  CandidateEducation,
  CandidateExperience,
  CandidateProject,
  InterviewReadiness,
  PersistedCandidateProfile,
  SkillEvidence,
} from '@/types'

type LoadState =
  | { phase: 'loading' }
  | {
      phase: 'loaded'
      profile: PersistedCandidateProfile
      readiness: InterviewReadiness
      etag: string
    }
  | { phase: 'not-found' }
  | { phase: 'authentication-required' }
  | { phase: 'error'; message: string }

const profileSections = [
  { id: 'identity-current-role', label: 'Identity and current role' },
  { id: 'skills-evidence', label: 'Skills and skill evidence' },
  { id: 'projects', label: 'Projects' },
  { id: 'work-experience', label: 'Work experience' },
  { id: 'education', label: 'Education' },
] as const

function present(value: string | number | null | undefined, fallback = 'Not provided') {
  if (value === null || value === undefined || value === '') return fallback
  return String(value)
}

function ReadOnlyValue({
  label,
  value,
  targetId,
}: {
  label: string
  value: string | number | null | undefined
  targetId?: string
}) {
  return (
    <div id={targetId} tabIndex={targetId ? -1 : undefined}>
      <dt className="text-xs font-semibold text-text-muted">{label}</dt>
      <dd className="mt-2 text-sm leading-6 text-text-primary">{present(value)}</dd>
    </div>
  )
}

function Section({
  id,
  title,
  children,
}: {
  id: string
  title: string
  children: React.ReactNode
}) {
  const headingId = `${id}-heading`
  return (
    <section
      id={id}
      tabIndex={-1}
      aria-labelledby={headingId}
      className="scroll-mt-8 border-b border-border py-8 first:pt-6"
    >
      <h2
        id={headingId}
        className="font-display text-xl font-semibold tracking-tight-display text-text-primary"
      >
        {title}
      </h2>
      <div className="mt-4">{children}</div>
    </section>
  )
}

function SkillEvidenceList({ evidence }: { evidence: SkillEvidence[] }) {
  if (!evidence.length) {
    return (
      <p className="text-sm leading-6 text-text-muted">
        No skill evidence is saved.
      </p>
    )
  }
  return (
    <div className="mt-6 border-t border-border">
      {evidence.map((item, index) => (
        <div
          key={`${item.skill}-${index}`}
          id={profileTargetForFieldPath(`skill_evidence.${index}`)}
          tabIndex={-1}
          className="grid gap-2 border-b border-border py-4 sm:grid-cols-[160px_minmax(0,1fr)]"
        >
          <div
            id={profileTargetForFieldPath(`skill_evidence.${index}.skill`)}
            tabIndex={-1}
          >
            <p className="text-xs font-semibold text-text-muted">Skill</p>
            <p className="mt-2 text-sm text-text-primary">{item.skill}</p>
          </div>
          <div
            id={profileTargetForFieldPath(`skill_evidence.${index}.evidence`)}
            tabIndex={-1}
          >
            <p className="text-xs font-semibold text-text-muted">Evidence</p>
            {item.evidence.length ? (
              <ul className="mt-2 space-y-2 text-sm leading-6 text-text-primary">
                {item.evidence.map((entry, evidenceIndex) => (
                  <li key={`${entry}-${evidenceIndex}`}>{entry}</li>
                ))}
              </ul>
            ) : (
              <p className="mt-2 text-sm text-text-muted">No evidence text is saved.</p>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

function ProjectsList({ projects }: { projects: CandidateProject[] }) {
  if (!projects.length) {
    return (
      <p className="text-sm leading-6 text-text-muted">
        No projects are saved. Projects are optional when other interviewable
        evidence is present.
      </p>
    )
  }
  return (
    <div className="border-t border-border">
      {projects.map((project, index) => (
        <article
          key={`${project.name}-${index}`}
          id={profileTargetForFieldPath(`projects.${index}`)}
          tabIndex={-1}
          className="border-b border-border py-4"
        >
          <h3 className="text-sm font-semibold text-text-primary">
            {present(project.name, 'Untitled project')}
          </h3>
          {project.description && (
            <p className="mt-2 text-sm leading-6 text-text-muted">{project.description}</p>
          )}
          {project.technologies.length > 0 && (
            <p className="mt-2 text-xs text-text-muted">
              Technologies: {project.technologies.join(', ')}
            </p>
          )}
          {project.role && (
            <p className="mt-2 text-xs text-text-muted">Role: {project.role}</p>
          )}
        </article>
      ))}
    </div>
  )
}

function ExperiencesList({ experiences }: { experiences: CandidateExperience[] }) {
  if (!experiences.length) {
    return (
      <p className="text-sm leading-6 text-text-muted">
        No work experience is saved. Students and interns can still prepare from
        skills, projects, or education.
      </p>
    )
  }
  return (
    <div className="border-t border-border">
      {experiences.map((experience, index) => (
        <article
          key={`${experience.company}-${experience.title}-${index}`}
          id={profileTargetForFieldPath(`experiences.${index}`)}
          tabIndex={-1}
          className="border-b border-border py-4"
        >
          <h3 className="text-sm font-semibold text-text-primary">
            {present(experience.title, 'Role not provided')}
          </h3>
          <p className="mt-2 text-sm text-text-muted">
            {present(experience.company, 'Company not provided')}
          </p>
          {(experience.start_date || experience.end_date) && (
            <p className="mt-2 text-xs text-text-muted">
              {present(experience.start_date, 'Start date not provided')} to{' '}
              {present(experience.end_date, 'Present')}
            </p>
          )}
          {experience.description && (
            <p className="mt-2 text-sm leading-6 text-text-muted">
              {experience.description}
            </p>
          )}
          {experience.technologies.length > 0 && (
            <p className="mt-2 text-xs text-text-muted">
              Technologies: {experience.technologies.join(', ')}
            </p>
          )}
        </article>
      ))}
    </div>
  )
}

function StructuredEducationList({
  education,
}: {
  education: CandidateEducation[]
}) {
  if (!education.length) {
    return <p className="text-sm leading-6 text-text-muted">No education is saved.</p>
  }
  return (
    <div className="border-t border-border">
      {education.map((entry, index) => (
        <article
          key={`${entry.institution}-${entry.degree ?? ''}-${index}`}
          id={profileTargetForFieldPath(`education.${index}`)}
          tabIndex={-1}
          className="border-b border-border py-4"
        >
          <h3 className="text-sm font-semibold text-text-primary">
            {present(entry.institution, 'Institution not provided')}
          </h3>
          <p className="mt-2 text-sm text-text-muted">
            {[entry.degree, entry.field_of_study].filter(Boolean).join(', ') ||
              'Degree and field not provided'}
          </p>
          {(entry.start_date || entry.end_date) && (
            <p className="mt-2 text-xs text-text-muted">
              {present(entry.start_date, 'Start date not provided')} to{' '}
              {present(entry.end_date, 'End date not provided')}
            </p>
          )}
        </article>
      ))}
    </div>
  )
}

function EducationContent({
  education,
}: {
  education: PersistedCandidateProfile['education']
}) {
  if (typeof education === 'string') {
    return (
      <div className="border-l-2 border-info bg-info/10 px-4 py-4">
        <p className="text-sm font-semibold text-text-primary">
          Legacy education
        </p>
        <p className="mt-2 text-sm leading-6 text-text-primary">{education}</p>
        <p className="mt-2 text-xs leading-5 text-text-muted">
          This original education text remains unchanged until you explicitly
          replace it in a later correction.
        </p>
      </div>
    )
  }
  return <StructuredEducationList education={education ?? []} />
}

function ProfileWorkspace({
  profile,
  readiness,
}: {
  profile: PersistedCandidateProfile
  readiness: InterviewReadiness
}) {
  return (
    <div className="grid gap-8 lg:grid-cols-[240px_minmax(0,1fr)]">
      <aside
        className="lg:sticky lg:top-8 lg:self-start"
        aria-label="Interview readiness and Candidate Profile navigation"
      >
        <InterviewReadinessSummary readiness={readiness} />
        <nav
          aria-label="Profile sections"
          className="mt-6 hidden border-y border-border py-4 lg:block"
        >
          {profileSections.map((section, index) => (
            <a
              key={section.id}
              href={`#${section.id}`}
              className="block border-b border-border py-4 text-sm text-text-muted last:border-b-0 hover:text-accent focus:text-accent"
            >
              {index + 1}. {section.label}
            </a>
          ))}
        </nav>
      </aside>

      <div className="min-w-0 border-t border-border">
        <Section id="identity-current-role" title="Identity and current role">
          <dl className="grid gap-4 sm:grid-cols-2">
            <ReadOnlyValue
              label="Full name"
              value={profile.name}
              targetId="profile-field-name"
            />
            <ReadOnlyValue
              label="Years of experience"
              value={profile.years_experience}
              targetId="profile-field-years_experience"
            />
            <ReadOnlyValue label="Recent role" value={profile.recent_role} />
            <ReadOnlyValue label="Specialization" value={profile.specialization} />
          </dl>
        </Section>

        <Section id="skills-evidence" title="Skills and skill evidence">
          <dl>
            <ReadOnlyValue
              label="Skills"
              value={profile.skills.length ? profile.skills.join(', ') : undefined}
              targetId="profile-field-skills"
            />
          </dl>
          <SkillEvidenceList evidence={profile.skill_evidence} />
        </Section>

        <Section id="projects" title="Projects">
          <ProjectsList projects={profile.projects} />
        </Section>

        <Section id="work-experience" title="Work experience">
          <ExperiencesList experiences={profile.experiences} />
        </Section>

        <Section id="education" title="Education">
          <EducationContent education={profile.education} />
        </Section>
      </div>
    </div>
  )
}

export function CandidateProfilePage() {
  const { candidateId } = useParams()
  const [loadState, setLoadState] = useState<LoadState>({ phase: 'loading' })

  const loadProfile = async () => {
    if (!candidateId) {
      setLoadState({ phase: 'not-found' })
      return
    }
    setLoadState({ phase: 'loading' })
    try {
      const response = await api.getCandidateProfile(candidateId)
      setLoadState({
        phase: 'loaded',
        profile: response.profile,
        readiness: response.readiness,
        etag: response.etag,
      })
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) {
        setLoadState({ phase: 'not-found' })
      } else if (error instanceof ApiError && error.status === 401) {
        setLoadState({ phase: 'authentication-required' })
      } else {
        setLoadState({
          phase: 'error',
          message:
            error instanceof Error
              ? error.message
              : 'Candidate Profile could not be loaded.',
        })
      }
    }
  }

  useEffect(() => {
    void loadProfile()
  }, [candidateId])

  if (loadState.phase === 'loading') {
    return (
      <div className="mx-auto max-w-6xl" role="status" aria-live="polite">
        <h1 className="font-display text-3xl font-semibold tracking-tight-display text-text-primary">
          Loading Candidate Profile
        </h1>
        <div className="mt-8 grid gap-8 lg:grid-cols-[240px_minmax(0,1fr)]" aria-hidden="true">
          <div className="h-32 rounded-lg bg-surface-raised" />
          <div className="space-y-6 border-t border-border pt-6">
            <div className="h-6 w-56 rounded-lg bg-surface-raised" />
            <div className="h-20 rounded-lg bg-surface-raised" />
            <div className="h-6 w-48 rounded-lg bg-surface-raised" />
            <div className="h-20 rounded-lg bg-surface-raised" />
          </div>
        </div>
      </div>
    )
  }

  if (loadState.phase !== 'loaded') {
    const authenticationRequired = loadState.phase === 'authentication-required'
    const notFound = loadState.phase === 'not-found'
    return (
      <div className="mx-auto max-w-2xl py-8">
        <h1 className="font-display text-3xl font-semibold tracking-tight-display text-text-primary">
          {authenticationRequired
            ? 'Sign in to continue'
            : notFound
              ? 'Candidate Profile not found'
              : 'Candidate Profile unavailable'}
        </h1>
        <p role="status" className="mt-2 max-w-xl text-sm leading-6 text-text-muted">
          {authenticationRequired
            ? 'Your session expired before the saved profile could be loaded.'
            : notFound
              ? 'Upload a resume to create a Candidate Profile you can review.'
              : loadState.message}
        </p>
        <div className="mt-6 flex flex-wrap gap-4">
          {authenticationRequired ? (
            <ButtonLink
              to="/login"
              treatment="restrained"
              className="h-12 px-4"
            >
              Sign in again
            </ButtonLink>
          ) : notFound ? (
            <ButtonLink
              to="/text-interview"
              treatment="restrained"
              className="h-12 px-4"
            >
              Choose resume
            </ButtonLink>
          ) : (
            <Button
              treatment="restrained"
              className="h-12 px-4"
              onClick={() => void loadProfile()}
            >
              Try again
            </Button>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-6xl">
      <header className="mb-8">
        <p className="text-sm font-medium text-text-muted">
          Saved profile
        </p>
        <h1 className="mt-2 font-display text-3xl font-semibold tracking-tight-display text-text-primary">
          Candidate Profile
        </h1>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-text-muted">
          Review the information saved from your resume. This persisted profile
          is available whenever you return.
        </p>
        <p className="mt-2 text-xs text-text-muted">
          Profile version {loadState.profile.profile_version}
        </p>
      </header>
      <ProfileWorkspace
        profile={loadState.profile}
        readiness={loadState.readiness}
      />
    </div>
  )
}

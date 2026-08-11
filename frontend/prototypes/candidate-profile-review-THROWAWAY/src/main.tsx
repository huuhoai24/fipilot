/**
 * THROWAWAY PROTOTYPE
 *
 * Candidate Profile Review design exploration only.
 * Uses deterministic local data, calls no backend, and is not mounted by the
 * production router.
 */
import React, { useEffect, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './prototype.css'

type Variant = 'A' | 'B' | 'C'

type Scenario =
  | 'complete'
  | 'partial'
  | 'incomplete'
  | 'ready'
  | 'dirty'
  | 'saving'
  | 'saved'
  | 'validation'
  | 'stale'
  | 'save-failure'
  | 'replacement-selected'
  | 'replacement-processing'
  | 'replacement-rejected'
  | 'upload-unavailable'
  | 'authentication-required'
  | 'legacy-education'
  | 'structured-education'

type SectionKey = 'identity' | 'skills' | 'projects' | 'experience' | 'education'

type CandidateProfile = {
  name: string
  years_experience: string
  recent_role: string
  specialization: string
  skills: string[]
  skill_evidence: Array<{
    evidence_id: string
    skill: string
    text: string
    source: string
    user_corrected: boolean
  }>
  projects: Array<{ name: string; description: string }>
  experiences: Array<{ role: string; company: string; description: string }>
  education: Array<{ institution: string; degree: string; field: string }>
  legacyEducation?: string
  profile_version: number
}

type ScenarioDefinition = {
  label: string
  eyebrow: string
  title: string
  tone: 'neutral' | 'info' | 'warning' | 'danger' | 'success'
  message: string
  profile: 'complete' | 'incomplete' | 'legacy'
  dirty?: boolean
  saving?: boolean
  ready?: boolean
}

const sections: Array<{ key: SectionKey; label: string; shortLabel: string }> = [
  { key: 'identity', label: 'Identity and current role', shortLabel: 'Identity' },
  { key: 'skills', label: 'Skills and skill evidence', shortLabel: 'Skills' },
  { key: 'projects', label: 'Projects', shortLabel: 'Projects' },
  { key: 'experience', label: 'Work experience', shortLabel: 'Experience' },
  { key: 'education', label: 'Education', shortLabel: 'Education' },
]

const completeProfile: CandidateProfile = {
  name: 'Nguyễn Minh Anh',
  years_experience: '1.5',
  recent_role: 'Backend Engineering Intern',
  specialization: 'Backend systems',
  skills: ['Python', 'FastAPI', 'PostgreSQL', 'Docker'],
  skill_evidence: [
    {
      evidence_id: 'evidence-58d57213',
      skill: 'FastAPI',
      text: 'Built typed REST endpoints and authentication for a campus interview practice service.',
      source: 'Resume, Campus Interview Practice API',
      user_corrected: false,
    },
    {
      evidence_id: 'evidence-80a204aa',
      skill: 'PostgreSQL',
      text: 'Designed the interview, candidate, and scoring tables used by the practice service.',
      source: 'Resume, Campus Interview Practice API',
      user_corrected: true,
    },
  ],
  projects: [
    {
      name: 'Campus Interview Practice API',
      description:
        'A FastAPI and PostgreSQL service that generates structured interview sessions for university students.',
    },
  ],
  experiences: [
    {
      role: 'Backend Engineering Intern',
      company: 'FPT Software',
      description:
        'Added API tests, investigated production logs, and documented service handoff steps for the platform team.',
    },
  ],
  education: [
    {
      institution: 'Ho Chi Minh City University of Technology',
      degree: 'Bachelor of Engineering',
      field: 'Computer Science',
    },
  ],
  profile_version: 7,
}

const incompleteProfile: CandidateProfile = {
  ...completeProfile,
  name: 'Candidate',
  skills: [],
  skill_evidence: [],
  projects: [{ name: '', description: '' }],
  experiences: [],
  education: [],
  profile_version: 3,
}

const legacyProfile: CandidateProfile = {
  ...completeProfile,
  education: [],
  legacyEducation:
    'B.Eng. Computer Science, Ho Chi Minh City University of Technology, expected 2026.',
  profile_version: 5,
}

const scenarioDefinitions: Record<Scenario, ScenarioDefinition> = {
  complete: {
    label: 'Accepted complete extraction',
    eyebrow: 'Resume accepted',
    title: 'Your resume was extracted',
    tone: 'success',
    message: 'Review the saved profile before starting an interview.',
    profile: 'complete',
    ready: true,
  },
  partial: {
    label: 'Partial Extraction',
    eyebrow: 'Resume partially extracted',
    title: 'Some resume content may be missing',
    tone: 'info',
    message:
      'Review every section and add anything the extraction missed. Saving a valid review acknowledges this warning.',
    profile: 'incomplete',
  },
  incomplete: {
    label: 'Incomplete saved profile',
    eyebrow: 'Saved profile',
    title: 'Complete two requirements before interviewing',
    tone: 'warning',
    message: 'Add your name, one skill, and supporting evidence. You can save valid partial corrections.',
    profile: 'incomplete',
  },
  ready: {
    label: 'Interview Ready saved profile',
    eyebrow: 'Saved profile',
    title: 'Your profile is interview ready',
    tone: 'success',
    message: 'A new interview will use profile version 7.',
    profile: 'complete',
    ready: true,
  },
  dirty: {
    label: 'Unsaved corrections',
    eyebrow: 'Unsaved corrections',
    title: 'Save before starting an interview',
    tone: 'warning',
    message: 'Your local edits are visible here but have not been saved to your Candidate Profile.',
    profile: 'complete',
    dirty: true,
    ready: true,
  },
  saving: {
    label: 'Saving corrections',
    eyebrow: 'Saving corrections',
    title: 'Updating your Candidate Profile',
    tone: 'neutral',
    message: 'Keep this page open. Interview actions will return after the save completes.',
    profile: 'complete',
    dirty: true,
    saving: true,
    ready: true,
  },
  saved: {
    label: 'Successful save',
    eyebrow: 'Corrections saved',
    title: 'Profile version 8 is interview ready',
    tone: 'success',
    message: 'Your next interview will reload this saved profile.',
    profile: 'complete',
    ready: true,
  },
  validation: {
    label: 'Field validation failure',
    eyebrow: 'Check your corrections',
    title: 'Two fields need attention',
    tone: 'danger',
    message: 'Correct the highlighted fields, then save again.',
    profile: 'incomplete',
    dirty: true,
  },
  stale: {
    label: 'Stale Profile Version conflict',
    eyebrow: 'Save conflict',
    title: 'Your profile changed in another session',
    tone: 'warning',
    message: 'Your current edits have not been discarded.',
    profile: 'complete',
    dirty: true,
    ready: true,
  },
  'save-failure': {
    label: 'Save server failure',
    eyebrow: 'Corrections not saved',
    title: 'We could not update your profile',
    tone: 'danger',
    message: 'Your edits remain on this page. Try saving again when the service is available.',
    profile: 'complete',
    dirty: true,
    ready: true,
  },
  'replacement-selected': {
    label: 'Replacement Upload selected',
    eyebrow: 'Replacement selected',
    title: 'minh-anh-resume-2026.pdf',
    tone: 'neutral',
    message: '8.2 MB PDF. Your currently saved profile remains available until replacement completes.',
    profile: 'complete',
    ready: true,
  },
  'replacement-processing': {
    label: 'Replacement Upload processing',
    eyebrow: 'Extracting replacement',
    title: 'Your saved profile is unchanged',
    tone: 'info',
    message: 'You may start an interview now using saved profile version 7.',
    profile: 'complete',
    ready: true,
  },
  'replacement-rejected': {
    label: 'Replacement Upload rejected',
    eyebrow: 'Replacement not accepted',
    title: 'This document has no extractable text',
    tone: 'warning',
    message: 'Choose a PDF or DOCX that contains selectable text. Your saved profile was not changed.',
    profile: 'complete',
    ready: true,
  },
  'upload-unavailable': {
    label: 'Upload temporarily unavailable',
    eyebrow: 'Upload interrupted',
    title: 'Resume upload is temporarily unavailable',
    tone: 'danger',
    message: 'Your selected file remains available on this page. Your saved profile was not changed.',
    profile: 'complete',
    ready: true,
  },
  'authentication-required': {
    label: 'Authentication required',
    eyebrow: 'Sign-in required',
    title: 'Sign in again to continue',
    tone: 'warning',
    message: 'Your session expired before the request completed. The saved profile was not changed.',
    profile: 'complete',
    ready: true,
  },
  'legacy-education': {
    label: 'Legacy education',
    eyebrow: 'Saved profile',
    title: 'Review legacy education',
    tone: 'info',
    message: 'The original education text remains readable until you explicitly replace it.',
    profile: 'legacy',
    ready: true,
  },
  'structured-education': {
    label: 'Structured education',
    eyebrow: 'Saved profile',
    title: 'Structured education supports interview readiness',
    tone: 'success',
    message: 'Institution and degree or field provide interviewable evidence.',
    profile: 'complete',
    ready: true,
  },
}

function readQuery(): { variant: Variant; scenario: Scenario } {
  const params = new URLSearchParams(window.location.search)
  const requestedVariant = params.get('variant')
  const requestedScenario = params.get('state')
  return {
    variant: requestedVariant === 'A' || requestedVariant === 'C' ? requestedVariant : 'B',
    scenario:
      requestedScenario && requestedScenario in scenarioDefinitions
        ? (requestedScenario as Scenario)
        : 'ready',
  }
}

function App() {
  const initial = useMemo(readQuery, [])
  const [variant, setVariant] = useState<Variant>(initial.variant)
  const [scenario, setScenario] = useState<Scenario>(initial.scenario)
  const [activeSection, setActiveSection] = useState<SectionKey>('identity')
  const definition = scenarioDefinitions[scenario]
  const profile =
    definition.profile === 'incomplete'
      ? incompleteProfile
      : definition.profile === 'legacy'
        ? legacyProfile
        : completeProfile

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    params.set('variant', variant)
    params.set('state', scenario)
    window.history.replaceState(null, '', `${window.location.pathname}?${params.toString()}`)
  }, [variant, scenario])

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement | null
      if (
        target?.matches('input, textarea, select, button') ||
        target?.isContentEditable ||
        event.altKey ||
        event.ctrlKey ||
        event.metaKey
      ) {
        return
      }
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return
      const order: Variant[] = ['A', 'B', 'C']
      const delta = event.key === 'ArrowRight' ? 1 : -1
      const next = (order.indexOf(variant) + delta + order.length) % order.length
      setVariant(order[next])
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [variant])

  const sharedProps = {
    profile,
    scenario,
    definition,
    activeSection,
    onSectionChange: setActiveSection,
    onScenarioChange: setScenario,
  }

  return (
    <div className="prototype-shell">
      <PrototypeHeader variant={variant} />
      {variant === 'A' ? (
        <GuidedReview {...sharedProps} />
      ) : variant === 'B' ? (
        <ProfessionalWorkspace {...sharedProps} />
      ) : (
        <ProgressiveReview {...sharedProps} />
      )}
      <PrototypeSwitcher
        variant={variant}
        scenario={scenario}
        onVariantChange={setVariant}
        onScenarioChange={setScenario}
      />
    </div>
  )
}

type DirectionProps = {
  profile: CandidateProfile
  scenario: Scenario
  definition: ScenarioDefinition
  activeSection: SectionKey
  onSectionChange: (section: SectionKey) => void
  onScenarioChange: (scenario: Scenario) => void
}

function PrototypeHeader({ variant }: { variant: Variant }) {
  const names = {
    A: 'Guided Review',
    B: 'Professional Workspace',
    C: 'Progressive Review',
  }
  return (
    <header className="product-header" data-component="ProductHeader">
      <a className="brand" href="#main">
        InterviewOS
      </a>
      <div className="header-context">
        <span className="throwaway-label">Throwaway prototype</span>
        <span aria-hidden="true">/</span>
        <span>Direction {variant}: {names[variant]}</span>
      </div>
      <button className="text-button" type="button">Sign out</button>
    </header>
  )
}

function GuidedReview(props: DirectionProps) {
  const stageIndex = sections.findIndex((section) => section.key === props.activeSection)
  const nextSection = sections[stageIndex + 1]
  return (
    <main id="main" className="guided-layout" data-direction="A">
      <PageIntroduction
        kicker="Candidate Profile"
        title="Review what we extracted"
        description="Confirm each section so your interview questions reflect your experience."
      />
      <StatusNotice definition={props.definition} scenario={props.scenario} />
      <ReadinessSummary profile={props.profile} definition={props.definition} compact />
      <nav className="guided-steps" aria-label="Profile review steps" data-component="GuidedSteps">
        {sections.map((section, index) => (
          <button
            key={section.key}
            className={section.key === props.activeSection ? 'step is-active' : 'step'}
            type="button"
            onClick={() => props.onSectionChange(section.key)}
          >
            <span>{index + 1}</span>
            {section.shortLabel}
          </button>
        ))}
      </nav>
      <section className="guided-stage" data-component="GuidedStage">
        <div className="stage-heading">
          <p>Step {stageIndex + 1} of {sections.length}</p>
          <h2>{sections[stageIndex].label}</h2>
        </div>
        <ProfileSection
          section={props.activeSection}
          profile={props.profile}
          scenario={props.scenario}
          onDirty={() => props.onScenarioChange('dirty')}
          standalone
        />
        <div className="stage-actions">
          {stageIndex > 0 && (
            <button
              className="button secondary"
              type="button"
              onClick={() => props.onSectionChange(sections[stageIndex - 1].key)}
            >
              Back
            </button>
          )}
          <span />
          {nextSection ? (
            <button
              className="button primary"
              type="button"
              onClick={() => props.onSectionChange(nextSection.key)}
            >
              Continue to {nextSection.shortLabel.toLowerCase()}
            </button>
          ) : (
            <PrimaryWorkflowAction
              scenario={props.scenario}
              definition={props.definition}
              onScenarioChange={props.onScenarioChange}
            />
          )}
        </div>
      </section>
    </main>
  )
}

function ProfessionalWorkspace(props: DirectionProps) {
  return (
    <main id="main" className="workspace-page" data-direction="B">
      <PageIntroduction
        kicker="Candidate Profile"
        title="Review your saved profile"
        description="Correct the details used to prepare interview questions. Changes apply to future interviews only."
      />
      <div className="workspace-mobile-readiness">
        <ReadinessSummary profile={props.profile} definition={props.definition} compact />
      </div>
      <div className="workspace-grid">
        <aside className="readiness-rail" data-component="ReadinessRail">
          <ReadinessSummary profile={props.profile} definition={props.definition} />
          <SectionNavigation
            profile={props.profile}
            onSectionChange={props.onSectionChange}
          />
          <UploadControl
            scenario={props.scenario}
            onScenarioChange={props.onScenarioChange}
            compact
          />
        </aside>
        <div className="editor-column">
          <StatusNotice definition={props.definition} scenario={props.scenario} />
          <div className="profile-editor" data-component="CandidateProfileEditor">
            {sections.map((section) => (
              <ProfileSection
                key={section.key}
                section={section.key}
                profile={props.profile}
                scenario={props.scenario}
                onDirty={() => props.onScenarioChange('dirty')}
              />
            ))}
          </div>
          <ActionArea
            scenario={props.scenario}
            definition={props.definition}
            onScenarioChange={props.onScenarioChange}
          />
        </div>
      </div>
    </main>
  )
}

function ProgressiveReview(props: DirectionProps) {
  const unresolved = getReadinessIssues(props.profile)
  return (
    <main id="main" className="progressive-layout" data-direction="C">
      <PageIntroduction
        kicker="Candidate Profile"
        title="Finish the details that matter"
        description="Open unresolved sections first. Completed details stay available when you need them."
      />
      <StatusNotice definition={props.definition} scenario={props.scenario} />
      <ReadinessSummary profile={props.profile} definition={props.definition} />
      <div className="progressive-sections" data-component="ProgressiveSections">
        {sections.map((section) => {
          const needsAttention = sectionHasIssue(section.key, unresolved)
          return (
            <details key={section.key} open={needsAttention || section.key === 'identity'}>
              <summary>
                <span>
                  <strong>{section.label}</strong>
                  <small>{needsAttention ? 'Needs attention' : 'Saved'}</small>
                </span>
                <span className="summary-affordance">Open section</span>
              </summary>
              <ProfileSection
                section={section.key}
                profile={props.profile}
                scenario={props.scenario}
                onDirty={() => props.onScenarioChange('dirty')}
                standalone
              />
            </details>
          )
        })}
      </div>
      <ActionArea
        scenario={props.scenario}
        definition={props.definition}
        onScenarioChange={props.onScenarioChange}
      />
    </main>
  )
}

function PageIntroduction({
  kicker,
  title,
  description,
}: {
  kicker: string
  title: string
  description: string
}) {
  return (
    <div className="page-introduction" data-component="PageIntroduction">
      <p>{kicker}</p>
      <h1>{title}</h1>
      <span>{description}</span>
    </div>
  )
}

function StatusNotice({
  definition,
  scenario,
}: {
  definition: ScenarioDefinition
  scenario: Scenario
}) {
  return (
    <section
      className={`status-notice tone-${definition.tone} scenario-${scenario}`}
      aria-live={definition.tone === 'danger' ? 'assertive' : 'polite'}
      data-component="StatusNotice"
    >
      <div>
        <p>{definition.eyebrow}</p>
        <h2>{definition.title}</h2>
        <span>{definition.message}</span>
      </div>
      <StatusAction scenario={scenario} />
    </section>
  )
}

function StatusAction({ scenario }: { scenario: Scenario }) {
  if (scenario === 'stale') {
    return (
      <div className="inline-actions">
        <button className="button primary" type="button">Reload latest profile</button>
        <button className="button quiet" type="button">Continue reviewing my local edits</button>
      </div>
    )
  }
  if (scenario === 'save-failure' || scenario === 'upload-unavailable') {
    return <button className="button primary" type="button">Try again</button>
  }
  if (scenario === 'replacement-rejected') {
    return <button className="button primary" type="button">Choose another file</button>
  }
  if (scenario === 'authentication-required') {
    return <button className="button primary" type="button">Sign in again</button>
  }
  if (scenario === 'replacement-selected') {
    return <button className="button primary" type="button">Upload replacement</button>
  }
  return null
}

function ReadinessSummary({
  profile,
  definition,
  compact = false,
}: {
  profile: CandidateProfile
  definition: ScenarioDefinition
  compact?: boolean
}) {
  const issues = getReadinessIssues(profile)
  const isReady = definition.ready && issues.length === 0
  return (
    <section
      className={compact ? 'readiness-summary is-compact' : 'readiness-summary'}
      aria-labelledby={compact ? 'readiness-compact-title' : 'readiness-title'}
      data-component="ReadinessSummary"
    >
      <p className="section-kicker">Interview Readiness</p>
      <h2 id={compact ? 'readiness-compact-title' : 'readiness-title'}>
        {isReady ? 'Ready to interview' : `${issues.length} requirements unresolved`}
      </h2>
      {isReady ? (
        <p className="supporting-copy">
          Name, skills, and interviewable evidence are saved.
        </p>
      ) : (
        <ul className="issue-list">
          {issues.map((issue) => (
            <li key={issue.code}>
              <a href={`#${issue.fieldId}`}>{issue.message}</a>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

function SectionNavigation({
  profile,
  onSectionChange,
}: {
  profile: CandidateProfile
  onSectionChange: (section: SectionKey) => void
}) {
  const issues = getReadinessIssues(profile)
  return (
    <nav className="section-navigation" aria-label="Candidate Profile sections">
      {sections.map((section, index) => {
        const issue = sectionHasIssue(section.key, issues)
        return (
          <a
            key={section.key}
            href={`#section-${section.key}`}
            onClick={() => onSectionChange(section.key)}
          >
            <span>{index + 1}. {section.label}</span>
            <small>{issue ? 'Needs attention' : 'Saved'}</small>
          </a>
        )
      })}
    </nav>
  )
}

function ProfileSection({
  section,
  profile,
  scenario,
  onDirty,
  standalone = false,
}: {
  section: SectionKey
  profile: CandidateProfile
  scenario: Scenario
  onDirty: () => void
  standalone?: boolean
}) {
  const className = standalone ? 'profile-section is-standalone' : 'profile-section'
  const sectionName = sections.find((item) => item.key === section)?.label
  return (
    <section
      id={`section-${section}`}
      className={className}
      data-component={`ProfileSection:${section}`}
    >
      {!standalone && (
        <div className="profile-section-heading">
          <h2>{sectionName}</h2>
        </div>
      )}
      {section === 'identity' && (
        <IdentityFields profile={profile} scenario={scenario} onDirty={onDirty} />
      )}
      {section === 'skills' && (
        <SkillsFields profile={profile} scenario={scenario} onDirty={onDirty} />
      )}
      {section === 'projects' && <ProjectsFields profile={profile} onDirty={onDirty} />}
      {section === 'experience' && (
        <ExperienceFields profile={profile} onDirty={onDirty} />
      )}
      {section === 'education' && (
        <EducationFields profile={profile} onDirty={onDirty} />
      )}
    </section>
  )
}

function IdentityFields({
  profile,
  scenario,
  onDirty,
}: {
  profile: CandidateProfile
  scenario: Scenario
  onDirty: () => void
}) {
  const invalidName = scenario === 'validation' || profile.name === 'Candidate'
  return (
    <div className="field-grid">
      <Field
        id="profile-name"
        label="Full name"
        defaultValue={profile.name}
        error={invalidName ? 'Enter your name instead of the extraction fallback “Candidate”.' : undefined}
        onDirty={onDirty}
        required
      />
      <Field
        id="profile-years"
        label="Years of experience"
        defaultValue={profile.years_experience}
        error={scenario === 'validation' ? 'Enter zero or a positive number.' : undefined}
        inputMode="decimal"
        onDirty={onDirty}
      />
      <Field
        id="profile-role"
        label="Recent role"
        defaultValue={profile.recent_role}
        onDirty={onDirty}
      />
      <Field
        id="profile-specialization"
        label="Specialization"
        defaultValue={profile.specialization}
        onDirty={onDirty}
      />
    </div>
  )
}

function SkillsFields({
  profile,
  scenario,
  onDirty,
}: {
  profile: CandidateProfile
  scenario: Scenario
  onDirty: () => void
}) {
  return (
    <div className="nested-editor">
      <div className="field-block">
        <label htmlFor="profile-skills">Skills</label>
        <input
          id="profile-skills"
          defaultValue={profile.skills.join(', ')}
          aria-describedby={profile.skills.length ? 'profile-skills-help' : 'profile-skills-error'}
          aria-invalid={!profile.skills.length}
          onChange={onDirty}
        />
        {profile.skills.length ? (
          <span id="profile-skills-help" className="field-help">
            Separate skills with commas. Duplicate skills are normalized when saved.
          </span>
        ) : (
          <span id="profile-skills-error" className="field-error">
            Add at least one skill before starting an interview.
          </span>
        )}
      </div>
      <div className="nested-heading">
        <div>
          <h3>Skill evidence</h3>
          <p>Show where you applied a skill so interview questions stay grounded.</p>
        </div>
        <button className="button secondary small" type="button">Add evidence</button>
      </div>
      {profile.skill_evidence.length ? (
        profile.skill_evidence.map((evidence, index) => (
          <div className="evidence-row" key={evidence.evidence_id} data-component="SkillEvidenceRow">
            <span className="row-number">{index + 1}</span>
            <div className="field-block">
              <label htmlFor={`${evidence.evidence_id}-skill`}>Skill</label>
              <select
                id={`${evidence.evidence_id}-skill`}
                defaultValue={evidence.skill}
                onChange={onDirty}
              >
                {profile.skills.map((skill) => <option key={skill}>{skill}</option>)}
              </select>
            </div>
            <div className="field-block evidence-text">
              <label htmlFor={`${evidence.evidence_id}-text`}>Evidence</label>
              <textarea
                id={`${evidence.evidence_id}-text`}
                defaultValue={evidence.text}
                rows={2}
                onChange={onDirty}
              />
              <span className="field-help">
                {evidence.user_corrected ? 'Corrected by you. ' : ''}
                Source: {evidence.source}
              </span>
            </div>
            <button className="text-button remove-button" type="button">Remove</button>
          </div>
        ))
      ) : (
        <div className="empty-inline" id="profile-evidence">
          <p>No skill evidence is saved.</p>
          <button className="button secondary small" type="button">Add skill evidence</button>
        </div>
      )}
      {scenario === 'validation' && (
        <p className="section-error" role="alert">
          Evidence must reference a skill that is present in Skills.
        </p>
      )}
    </div>
  )
}

function ProjectsFields({
  profile,
  onDirty,
}: {
  profile: CandidateProfile
  onDirty: () => void
}) {
  return (
    <NestedList
      emptyMessage="No projects are saved. Projects are optional when other interviewable evidence is present."
      addLabel="Add project"
      hasItems={profile.projects.some((project) => project.name || project.description)}
    >
      {profile.projects
        .filter((project) => project.name || project.description)
        .map((project, index) => (
          <div className="nested-row two-fields" key={`${project.name}-${index}`} data-component="ProjectRow">
            <Field id={`project-${index}-name`} label="Project name" defaultValue={project.name} onDirty={onDirty} />
            <TextAreaField
              id={`project-${index}-description`}
              label="Description"
              defaultValue={project.description}
              onDirty={onDirty}
            />
            <button className="text-button remove-button" type="button">Remove</button>
          </div>
        ))}
    </NestedList>
  )
}

function ExperienceFields({
  profile,
  onDirty,
}: {
  profile: CandidateProfile
  onDirty: () => void
}) {
  return (
    <NestedList
      emptyMessage="No work experience is saved. Students and interns can continue with education or project evidence."
      addLabel="Add experience"
      hasItems={profile.experiences.length > 0}
    >
      {profile.experiences.map((experience, index) => (
        <div className="nested-row experience-fields" key={`${experience.company}-${index}`} data-component="ExperienceRow">
          <Field id={`experience-${index}-role`} label="Role" defaultValue={experience.role} onDirty={onDirty} />
          <Field id={`experience-${index}-company`} label="Company" defaultValue={experience.company} onDirty={onDirty} />
          <TextAreaField
            id={`experience-${index}-description`}
            label="Description"
            defaultValue={experience.description}
            onDirty={onDirty}
          />
          <button className="text-button remove-button" type="button">Remove</button>
        </div>
      ))}
    </NestedList>
  )
}

function EducationFields({
  profile,
  onDirty,
}: {
  profile: CandidateProfile
  onDirty: () => void
}) {
  if (profile.legacyEducation) {
    return (
      <div className="legacy-education" data-component="LegacyEducation">
        <div>
          <p className="section-kicker">Original legacy education</p>
          <p>{profile.legacyEducation}</p>
          <span>This text will remain unchanged unless you replace it with structured education.</span>
        </div>
        <button className="button secondary" type="button">Replace with structured education</button>
      </div>
    )
  }
  return (
    <NestedList
      emptyMessage="No structured education is saved."
      addLabel="Add education"
      hasItems={profile.education.length > 0}
    >
      {profile.education.map((education, index) => (
        <div className="nested-row education-fields" key={`${education.institution}-${index}`} data-component="EducationRow">
          <Field
            id={`education-${index}-institution`}
            label="Institution"
            defaultValue={education.institution}
            onDirty={onDirty}
            required
          />
          <Field
            id={`education-${index}-degree`}
            label="Degree"
            defaultValue={education.degree}
            onDirty={onDirty}
          />
          <Field
            id={`education-${index}-field`}
            label="Field of study"
            defaultValue={education.field}
            onDirty={onDirty}
          />
          <button className="text-button remove-button" type="button">Remove</button>
        </div>
      ))}
    </NestedList>
  )
}

function NestedList({
  hasItems,
  emptyMessage,
  addLabel,
  children,
}: {
  hasItems: boolean
  emptyMessage: string
  addLabel: string
  children: React.ReactNode
}) {
  return (
    <div className="nested-editor">
      <div className="nested-heading">
        <p>{hasItems ? 'Saved entries can be corrected, reordered, or removed.' : emptyMessage}</p>
        <button className="button secondary small" type="button">{addLabel}</button>
      </div>
      {hasItems ? children : <div className="empty-inline"><p>{emptyMessage}</p></div>}
    </div>
  )
}

function Field({
  id,
  label,
  defaultValue,
  error,
  required,
  inputMode,
  onDirty,
}: {
  id: string
  label: string
  defaultValue: string
  error?: string
  required?: boolean
  inputMode?: React.HTMLAttributes<HTMLInputElement>['inputMode']
  onDirty: () => void
}) {
  const descriptionId = error ? `${id}-error` : undefined
  return (
    <div className="field-block">
      <label htmlFor={id}>{label}{required ? ' *' : ''}</label>
      <input
        id={id}
        defaultValue={defaultValue}
        aria-invalid={Boolean(error)}
        aria-describedby={descriptionId}
        inputMode={inputMode}
        onChange={onDirty}
      />
      {error && <span className="field-error" id={descriptionId}>{error}</span>}
    </div>
  )
}

function TextAreaField({
  id,
  label,
  defaultValue,
  onDirty,
}: {
  id: string
  label: string
  defaultValue: string
  onDirty: () => void
}) {
  return (
    <div className="field-block">
      <label htmlFor={id}>{label}</label>
      <textarea id={id} defaultValue={defaultValue} rows={2} onChange={onDirty} />
    </div>
  )
}

function UploadControl({
  scenario,
  onScenarioChange,
  compact = false,
}: {
  scenario: Scenario
  onScenarioChange: (scenario: Scenario) => void
  compact?: boolean
}) {
  const isProcessing = scenario === 'replacement-processing'
  return (
    <section className={compact ? 'upload-control is-compact' : 'upload-control'} data-component="ReplacementUpload">
      <p className="section-kicker">Resume source</p>
      <h2>{isProcessing ? 'Replacement processing' : 'minh-anh-resume.pdf'}</h2>
      <span>{isProcessing ? 'Saved profile version 7 remains active.' : 'Uploaded 18 Jul 2026'}</span>
      <div className="upload-actions">
        <button
          className="button secondary small"
          type="button"
          onClick={() => onScenarioChange('replacement-selected')}
        >
          Choose resume
        </button>
        {(scenario === 'replacement-selected' || scenario === 'replacement-rejected') && (
          <button className="text-button" type="button">Choose another file</button>
        )}
      </div>
    </section>
  )
}

function ActionArea({
  scenario,
  definition,
  onScenarioChange,
}: {
  scenario: Scenario
  definition: ScenarioDefinition
  onScenarioChange: (scenario: Scenario) => void
}) {
  const issues = getReadinessIssues(
    definition.profile === 'incomplete' ? incompleteProfile : definition.profile === 'legacy' ? legacyProfile : completeProfile,
  )
  const canInterview = Boolean(definition.ready && !definition.dirty && !definition.saving && issues.length === 0)
  const displayedVersion =
    scenario === 'saved' ? 8 : definition.profile === 'incomplete' ? 3 : definition.profile === 'legacy' ? 5 : 7
  return (
    <section className="action-area" aria-label="Profile and interview actions" data-component="ActionArea">
      <div className="action-status">
        <strong>{definition.dirty ? 'Unsaved corrections' : 'Saved Candidate Profile'}</strong>
        <span>
          {definition.dirty
            ? 'Save to make these corrections available to future interviews.'
            : `Profile version ${displayedVersion}`}
        </span>
      </div>
      <div className="workflow-actions">
        <PrimaryWorkflowAction
          scenario={scenario}
          definition={definition}
          onScenarioChange={onScenarioChange}
        />
        <div className="interview-actions">
          <button className="button primary" type="button" disabled={!canInterview}>
            Start text interview
          </button>
          <button className="button secondary" type="button" disabled={!canInterview}>
            Start speech interview
          </button>
        </div>
      </div>
    </section>
  )
}

function PrimaryWorkflowAction({
  scenario,
  definition,
  onScenarioChange,
}: {
  scenario: Scenario
  definition: ScenarioDefinition
  onScenarioChange: (scenario: Scenario) => void
}) {
  if (scenario === 'stale') {
    return null
  }
  if (definition.dirty || scenario === 'save-failure') {
    return (
      <button
        className="button primary"
        type="button"
        disabled={definition.saving}
        onClick={() => {
          onScenarioChange('saving')
          window.setTimeout(() => onScenarioChange('saved'), 700)
        }}
      >
        {definition.saving ? 'Saving corrections' : 'Save corrections'}
      </button>
    )
  }
  if (!definition.ready) {
    return <a className="button primary" href="#profile-name">Complete missing details</a>
  }
  return null
}

function PrototypeSwitcher({
  variant,
  scenario,
  onVariantChange,
  onScenarioChange,
}: {
  variant: Variant
  scenario: Scenario
  onVariantChange: (variant: Variant) => void
  onScenarioChange: (scenario: Scenario) => void
}) {
  const order: Variant[] = ['A', 'B', 'C']
  const move = (delta: number) => {
    const next = (order.indexOf(variant) + delta + order.length) % order.length
    onVariantChange(order[next])
  }
  return (
    <aside className="prototype-switcher" aria-label="Throwaway prototype controls" data-component="PrototypeSwitcher">
      <button type="button" onClick={() => move(-1)} aria-label="Previous direction">Previous</button>
      <div className="variant-buttons">
        {order.map((item) => (
          <button
            key={item}
            type="button"
            className={item === variant ? 'is-active' : ''}
            aria-pressed={item === variant}
            onClick={() => onVariantChange(item)}
          >
            {item}
          </button>
        ))}
      </div>
      <label>
        Scenario
        <select value={scenario} onChange={(event) => onScenarioChange(event.target.value as Scenario)}>
          {Object.entries(scenarioDefinitions).map(([value, item]) => (
            <option value={value} key={value}>{item.label}</option>
          ))}
        </select>
      </label>
      <button type="button" onClick={() => move(1)} aria-label="Next direction">Next</button>
    </aside>
  )
}

type ReadinessIssue = {
  code: string
  message: string
  fieldId: string
  section: SectionKey
}

function getReadinessIssues(profile: CandidateProfile): ReadinessIssue[] {
  const issues: ReadinessIssue[] = []
  if (!profile.name.trim()) {
    issues.push({ code: 'missing_name', message: 'Add your name', fieldId: 'profile-name', section: 'identity' })
  } else if (profile.name.trim() === 'Candidate') {
    issues.push({
      code: 'fallback_name',
      message: 'Replace the fallback name “Candidate”',
      fieldId: 'profile-name',
      section: 'identity',
    })
  }
  if (!profile.skills.length) {
    issues.push({ code: 'missing_skills', message: 'Add at least one skill', fieldId: 'profile-skills', section: 'skills' })
  }
  const hasEvidence =
    profile.skill_evidence.some((item) => item.text.trim()) ||
    profile.projects.some((item) => item.name.trim() || item.description.trim()) ||
    profile.experiences.some((item) => item.role.trim() || item.company.trim() || item.description.trim()) ||
    profile.education.some(
      (item) => item.institution.trim() && (item.degree.trim() || item.field.trim()),
    )
  if (!hasEvidence) {
    issues.push({
      code: 'missing_interviewable_evidence',
      message: 'Add skill, project, work, or education evidence',
      fieldId: 'profile-evidence',
      section: 'skills',
    })
  }
  return issues
}

function sectionHasIssue(section: SectionKey, issues: ReadinessIssue[]) {
  return issues.some((issue) => issue.section === section)
}

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

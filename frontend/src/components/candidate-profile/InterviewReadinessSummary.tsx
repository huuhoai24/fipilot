import React from 'react'
import type { InterviewReadiness, ProfileIssue } from '@/types'

const issueCopy: Record<string, string> = {
  missing_name: 'Add your full name.',
  fallback_name: 'Replace “Candidate” with your full name.',
  missing_skills: 'Add at least one skill.',
  missing_interviewable_evidence:
    'Add skill evidence, a project, work experience, or qualifying education.',
  invalid_years_experience: 'Enter zero or a positive number.',
  empty_nested_entry: 'Complete or remove this entry.',
  evidence_skill_not_found:
    'Choose a skill that is present in your skills list.',
  empty_skill: 'Remove or correct the empty skill.',
}

const fieldTargets: Record<string, string> = {
  name: 'profile-field-name',
  years_experience: 'profile-field-years_experience',
  skills: 'profile-field-skills',
  skill_evidence: 'skills-evidence',
  projects: 'projects',
  experiences: 'work-experience',
  education: 'education',
}

export function profileTargetForFieldPath(fieldPath: string): string {
  if (fieldPath.includes('.')) {
    return `profile-field-${fieldPath.replace(/\./g, '-')}`
  }
  return fieldTargets[fieldPath] ?? 'identity-current-role'
}

function targetForIssue(issue: ProfileIssue): string {
  if (issue.field_path) {
    return profileTargetForFieldPath(issue.field_path)
  }
  if (issue.code === 'missing_interviewable_evidence') return 'skills-evidence'
  return 'identity-current-role'
}

function focusIssueTarget(
  event: React.MouseEvent<HTMLAnchorElement>,
  targetId: string,
) {
  const target = document.getElementById(targetId)
  if (!target) return
  event.preventDefault()
  target.focus()
}

export function InterviewReadinessSummary({
  readiness,
}: {
  readiness: InterviewReadiness
}) {
  if (readiness.is_ready) {
    return (
      <section
        aria-labelledby="interview-readiness-heading"
        className="border-b border-border pb-4"
      >
        <h2
          id="interview-readiness-heading"
          className="text-base font-semibold text-text-primary"
        >
          Interview ready
        </h2>
        <p className="mt-2 text-sm leading-6 text-text-muted">
          Your saved profile contains the minimum information needed for an
          interview.
        </p>
      </section>
    )
  }

  return (
    <section
      aria-labelledby="interview-readiness-heading"
      className="border-l-2 border-warning pl-4"
    >
      <h2
        id="interview-readiness-heading"
        className="text-base font-semibold text-text-primary"
      >
        Complete your profile
      </h2>
      <p className="mt-2 text-sm leading-6 text-text-muted">
        Your saved profile needs the following information before an interview
        can start.
      </p>
      <ul className="mt-2 border-t border-border">
        {readiness.issues.map((issue, index) => {
          const targetId = targetForIssue(issue)
          return (
            <li key={`${issue.code}-${issue.field_path ?? index}`}>
              <a
                href={`#${targetId}`}
                onClick={(event) => focusIssueTarget(event, targetId)}
                className="inline-flex min-h-11 items-center border-b border-border py-2 text-sm leading-6 text-accent hover:text-accent-hover"
              >
                {issueCopy[issue.code] ?? 'Review this profile requirement.'}
              </a>
            </li>
          )
        })}
      </ul>
    </section>
  )
}

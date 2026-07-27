import React from 'react'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { afterEach, describe, expect, it } from 'vitest'
import { InterviewReadinessSummary } from '@/components/candidate-profile/InterviewReadinessSummary'

afterEach(cleanup)

describe('InterviewReadinessSummary', () => {
  it('lists every backend issue and focuses its visible profile target', () => {
    render(
      <>
        <InterviewReadinessSummary
          readiness={{
            is_ready: false,
            issues: [
              {
                code: 'fallback_name',
                origin: 'interview_readiness',
                field_path: 'name',
              },
              {
                code: 'missing_skills',
                origin: 'interview_readiness',
                field_path: 'skills',
              },
              {
                code: 'missing_interviewable_evidence',
                origin: 'interview_readiness',
                field_path: 'skill_evidence',
              },
            ],
          }}
        />
        <div id="profile-field-name" tabIndex={-1}>Saved name</div>
        <div id="profile-field-skills" tabIndex={-1}>Saved skills</div>
        <section id="skills-evidence" tabIndex={-1}>Saved evidence</section>
      </>,
    )

    expect(
      screen.getByRole('heading', { name: 'Complete your profile' }),
    ).toBeInTheDocument()
    const issueLinks = screen.getAllByRole('link')
    expect(issueLinks.map((link) => link.textContent)).toEqual([
      'Replace “Candidate” with your full name.',
      'Add at least one skill.',
      'Add skill evidence, a project, work experience, or qualifying education.',
    ])

    fireEvent.click(issueLinks[1])

    expect(document.activeElement).toBe(
      document.getElementById('profile-field-skills'),
    )
  })

  it('keeps routine ready confirmation restrained and non-actionable', () => {
    render(
      <InterviewReadinessSummary
        readiness={{ is_ready: true, issues: [] }}
      />,
    )

    expect(
      screen.getByRole('heading', { name: 'Interview ready' }),
    ).toBeInTheDocument()
    expect(screen.queryByRole('link')).not.toBeInTheDocument()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it('focuses the exact nested entry named by a validity issue', () => {
    render(
      <>
        <InterviewReadinessSummary
          readiness={{
            is_ready: false,
            issues: [
              {
                code: 'evidence_skill_not_found',
                origin: 'profile_validity',
                field_path: 'skill_evidence.0.skill',
              },
            ],
          }}
        />
        <div id="profile-field-skill_evidence-0-skill" tabIndex={-1}>
          Saved evidence skill
        </div>
      </>,
    )

    fireEvent.click(
      screen.getByRole('link', {
        name: 'Choose a skill that is present in your skills list.',
      }),
    )

    expect(document.activeElement).toBe(
      document.getElementById('profile-field-skill_evidence-0-skill'),
    )
  })
})

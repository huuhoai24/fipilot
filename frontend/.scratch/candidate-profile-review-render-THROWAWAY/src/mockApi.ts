// THROWAWAY deterministic boundary for rendering the production page.
export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message)
  }
}

export const api = {
  getCandidateProfile: async () => ({
    etag: '"1"',
    profile: {
      candidate_id: 'candidate-review-7',
      profile_version: 1,
      name: 'Candidate',
      years_experience: 1.5,
      recent_role: 'Backend Engineering Intern',
      specialization: 'Backend systems',
      skills: ['Python', 'FastAPI', 'PostgreSQL', 'Docker'],
      skill_evidence: [
        {
          skill: 'Rust',
          evidence: [
            'Built typed REST endpoints and authentication for a campus interview practice service.',
          ],
          source_section: 'Projects',
        },
        {
          skill: 'PostgreSQL',
          evidence: [
            'Designed the interview, candidate, and scoring tables used by the practice service.',
          ],
          source_section: 'Projects',
        },
      ],
      projects: [
        {
          name: 'Campus Interview Practice API',
          description:
            'A FastAPI and PostgreSQL service that creates structured interview sessions for university students.',
          technologies: ['Python', 'FastAPI', 'PostgreSQL'],
          role: 'Backend developer',
        },
      ],
      experiences: [
        {
          company: 'FPT Software',
          title: 'Backend Engineering Intern',
          start_date: '2025-06',
          end_date: '2025-09',
          description:
            'Added API tests, investigated production logs, and documented service handoff steps.',
          technologies: ['Python', 'Docker'],
        },
      ],
      education: [
        {
          institution: 'Ho Chi Minh City University of Technology',
          degree: 'Bachelor of Engineering',
          field_of_study: 'Computer Science',
          start_date: '2022',
          end_date: '2026',
        },
      ],
      confidence: 0.82,
      confidence_score: 0.82,
      extraction_method: 'resume',
    },
    readiness: {
      is_ready: false,
      issues: [
        {
          code: 'fallback_name',
          origin: 'interview_readiness' as const,
          field_path: 'name',
        },
        {
          code: 'evidence_skill_not_found',
          origin: 'profile_validity' as const,
          field_path: 'skill_evidence.0.skill',
        },
      ],
    },
  }),
}

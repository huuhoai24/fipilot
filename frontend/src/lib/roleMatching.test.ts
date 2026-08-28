import { describe, expect, it } from 'vitest'
import { calculateRoleMatches, INTERVIEW_ROLES } from '@/lib/roleMatching'
import type { CandidateProfile } from '@/types'

describe('calculateRoleMatches', () => {
  it('returns empty list for null or undefined profile', () => {
    expect(calculateRoleMatches(null)).toEqual([])
    expect(calculateRoleMatches(undefined)).toEqual([])
  })

  it('uses AI-generated role_matches when available, returns top 6 sorted descending with 0% padding', () => {
    const profile: CandidateProfile = {
      name: 'Vo Quang Trieu',
      skills: ['LangGraph', 'RAG', 'PyTorch', 'FastAPI'],
      skill_evidence: [],
      projects: [],
      experiences: [],
      confidence: 0.95,
      confidence_score: 0.95,
      role_matches: [
        {
          role_id: 'ai-engineer',
          title: 'AI Engineer',
          score: 65,
          matched_skills: ['LangGraph', 'RAG', 'PyTorch'],
          relevant_experience_count: 2,
          summary: '3 matched skills · 2 relevant experiences',
        },
        {
          role_id: 'backend-developer',
          title: 'Backend Developer',
          score: 35,
          matched_skills: ['FastAPI'],
          relevant_experience_count: 1,
          summary: '1 matched skills · 1 relevant experiences',
        },
      ],
    }

    const matches = calculateRoleMatches(profile)
    expect(matches).toHaveLength(6)

    // First role is AI Engineer (65%)
    expect(matches[0].title).toBe('AI Engineer')
    expect(matches[0].score).toBe(65)
    expect(matches[0].matchedSkills).toEqual(['LangGraph', 'RAG', 'PyTorch'])

    // Second role is Backend Developer (35%)
    expect(matches[1].title).toBe('Backend Developer')
    expect(matches[1].score).toBe(35)
    expect(matches[1].matchedSkills).toEqual(['FastAPI'])

    // The remaining 4 roles are padded with 0% and empty matchedSkills
    for (let i = 2; i < 6; i++) {
      expect(matches[i].score).toBe(0)
      expect(matches[i].matchedSkills).toEqual([])
      expect(matches[i].summary).toBe('')
    }
  })

  it('correctly maps 10 Knowledge domains and returns 6 roles in fallback mode without AI role_matches', () => {
    const profile: CandidateProfile = {
      name: 'Vo Quang Trieu',
      skills: ['LangGraph', 'RAG', 'PyTorch', 'Playwright', 'FastAPI', 'Docker', 'Git'],
      skill_evidence: [],
      projects: [
        {
          name: 'AI System',
          description: 'Built RAG agent with PyTorch and LangGraph',
          technologies: ['LangGraph', 'RAG', 'PyTorch'],
        },
        {
          name: 'Test Automation',
          description: 'Automated test suite using Playwright',
          technologies: ['Playwright'],
        },
      ],
      experiences: [],
      confidence: 0.9,
      confidence_score: 0.9,
    }

    const matches = calculateRoleMatches(profile)
    expect(matches).toHaveLength(6)

    // Top match should be AI Engineer
    expect(matches[0].title).toBe('AI Engineer')
    expect(matches[0].matchedSkills).toContain('LangGraph')
    expect(matches[0].matchedSkills).toContain('RAG')
    expect(matches[0].matchedSkills).toContain('PyTorch')
    expect(matches[0].matchedSkills).not.toContain('Playwright')

    // Tester / QA / QC or Software Engineer matches Playwright
    const qaMatch = matches.find((m) => m.title === 'Tester / QA / QC' || m.title === 'Software Engineer')
    expect(qaMatch).toBeDefined()

    // Unmatched roles in the 6 returned have 0% and empty matchedSkills
    const zeroMatches = matches.filter((m) => m.score === 0)
    for (const zm of zeroMatches) {
      expect(zm.matchedSkills).toEqual([])
      expect(zm.summary).toBe('')
    }
  })

  it('contains all 10 standard roles from Knowledge/Domains in INTERVIEW_ROLES', () => {
    expect(INTERVIEW_ROLES).toHaveLength(10)
    const titles = INTERVIEW_ROLES.map((r) => r.title)
    expect(titles).toContain('AI Engineer')
    expect(titles).toContain('Backend Developer')
    expect(titles).toContain('Business Analyst')
    expect(titles).toContain('Data Engineer')
    expect(titles).toContain('Data Scientist')
    expect(titles).toContain('DevOps Engineer')
    expect(titles).toContain('Full Stack Developer')
    expect(titles).toContain('Software Engineer')
    expect(titles).toContain('Tester / QA / QC')
    expect(titles).toContain('Web Developer')
  })
})

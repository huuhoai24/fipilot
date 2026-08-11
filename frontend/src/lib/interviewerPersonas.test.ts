import { describe, expect, it } from 'vitest'
import { resolveInterviewerPersona } from '@/lib/interviewerPersonas'

describe('resolveInterviewerPersona', () => {
  it('selects the technical AI persona for a technical interview', () => {
    expect(resolveInterviewerPersona('technical')).toMatchObject({
      id: 'technical',
      name: 'Sarah Nguyen',
      role: 'Technical Interviewer',
      specialization: 'Technical knowledge, projects, and system design',
    })
  })

  it('selects the behavioral AI persona for a behavioral interview', () => {
    expect(resolveInterviewerPersona('behavioral')).toMatchObject({
      id: 'behavioral',
      name: 'Alex Chen',
      role: 'Behavioral Interviewer',
      specialization: 'Teamwork, conflict, leadership, and STAR-style questions',
    })
  })

  it('selects the HR AI persona when a structured HR style is available', () => {
    expect(resolveInterviewerPersona('hr')).toMatchObject({
      id: 'hr',
      name: 'Mia Tran',
      role: 'HR Interviewer',
      specialization: 'Background, motivation, career goals, and culture fit',
    })
  })

  it('selects the English-practice AI persona when that structured style is available', () => {
    expect(resolveInterviewerPersona('english')).toMatchObject({
      id: 'english',
      name: 'Emma Lee',
      role: 'English Interviewer',
      specialization: 'Professional English interview practice',
    })
  })

  it('falls back safely when the interview style has no persona mapping', () => {
    expect(resolveInterviewerPersona('mixed')).toMatchObject({
      id: 'default',
      name: 'FiPilot Interviewer',
      role: 'AI Virtual Interviewer',
    })
    expect(resolveInterviewerPersona('future-style')).toMatchObject({
      id: 'default',
      name: 'FiPilot Interviewer',
    })
    expect(resolveInterviewerPersona(undefined)).toMatchObject({
      id: 'default',
      name: 'FiPilot Interviewer',
    })
  })
})

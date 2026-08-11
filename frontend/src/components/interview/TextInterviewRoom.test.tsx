import React from 'react'
import { cleanup, render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { TextInterviewRoom } from '@/components/interview/TextInterviewRoom'
import { resolveInterviewerPersona } from '@/lib/interviewerPersonas'
import type { V2InterviewSessionState, V2InterviewTurn } from '@/types'

const openingTurn: V2InterviewTurn = {
  turn_id: 'turn-opening',
  question: 'Hi Trieu, nice to meet you. To start, could you briefly introduce yourself?',
  status: 'created',
  question_type: 'opening',
  difficulty: 'easy',
  topic: 'Introduction',
  expected_signal: [],
}

const firstTechnicalTurn: V2InterviewTurn = {
  turn_id: 'turn-1',
  question: 'Could you walk me through the agent workflow in your project?',
  status: 'created',
  question_type: 'project_deep_dive',
  difficulty: 'medium',
  topic: 'Agent workflow',
  expected_signal: ['Private expected signal'],
}

function sessionState(
  overrides: Partial<V2InterviewSessionState>,
): V2InterviewSessionState {
  return {
    candidate_profile: {
      name: 'Trieu Vo',
      skills: ['LangGraph'],
      skill_evidence: [],
      projects: [],
      experiences: [],
      confidence: 0.94,
      confidence_score: 0.94,
    },
    interview_config: {
      mode: 'text',
      language: 'en',
      experience_level: 'senior',
      duration_minutes: 30,
      interview_style: 'technical',
      question_count: 4,
      objective: 'Assess practical engineering experience',
    },
    interview_plan: {
      duration_minutes: 30,
      rounds: [],
      coverage_goals: [],
      risk_areas: [],
      planner_summary: '',
    },
    phase: 'interviewing',
    current_turn: firstTechnicalTurn,
    completed_turns: [],
    current_question_index: 0,
    ...overrides,
  }
}

function renderRoom(
  state: V2InterviewSessionState,
  options: { pendingAnswer?: string | null; submitting?: boolean } = {},
) {
  return render(
    <TextInterviewRoom
      state={state}
      persona={resolveInterviewerPersona(state.interview_config.interview_style)}
      progress={{ current: 1, total: 4 }}
      answer=""
      pendingAnswer={options.pendingAnswer ?? null}
      submitting={options.submitting ?? false}
      error={null}
      onAnswerChange={vi.fn()}
      onSubmit={vi.fn()}
      onViewReport={vi.fn()}
      onBackToHistory={vi.fn()}
    />,
  )
}

afterEach(cleanup)

describe('TextInterviewRoom conversation phases', () => {
  it('renders the selected fictional AI persona throughout the active room', () => {
    renderRoom(
      sessionState({}),
      { pendingAnswer: 'My submitted answer', submitting: true },
    )

    expect(screen.getByRole('heading', { level: 1, name: 'Sarah Nguyen' })).toBeInTheDocument()
    expect(screen.getByText('AI Virtual Interviewer')).toBeInTheDocument()
    expect(screen.getByText('Technical Interviewer')).toBeInTheDocument()
    expect(screen.getByText('Technical knowledge, projects, and system design')).toBeInTheDocument()
    expect(screen.getByText('Sarah Nguyen is preparing the next question...')).toBeInTheDocument()
    expect(screen.queryByText('FiPilot interviewer is preparing the next question...')).not.toBeInTheDocument()
  })

  it('starts with the persisted opening and keeps the planned question hidden', () => {
    renderRoom(sessionState({
      phase: 'opening',
      current_turn: openingTurn,
      pending_turn: firstTechnicalTurn,
    }))

    expect(screen.getByText(/Hi Trieu, nice to meet you/)).toBeInTheDocument()
    expect(screen.getAllByText('Sarah Nguyen')).toHaveLength(2)
    expect(screen.getAllByText('Opening')).toHaveLength(2)
    expect(screen.queryByText(firstTechnicalTurn.question as string)).not.toBeInTheDocument()
  })

  it('presents an existing follow-up as normal interviewer dialogue', () => {
    const answeredOpening = {
      ...openingTurn,
      status: 'answered' as const,
      answer: 'I build agentic systems for production workflows.',
      candidate_answer: 'I build agentic systems for production workflows.',
    }
    const answeredTechnical = {
      ...firstTechnicalTurn,
      status: 'evaluated' as const,
      answer: 'We used LangGraph to coordinate the agents.',
      candidate_answer: 'We used LangGraph to coordinate the agents.',
    }
    const followUp: V2InterviewTurn = {
      ...firstTechnicalTurn,
      turn_id: 'turn-2',
      question: 'How did you manage shared state between the agents?',
      question_type: 'follow_up',
    }

    renderRoom(sessionState({
      opening_turn: answeredOpening,
      completed_turns: [answeredTechnical],
      current_turn: followUp,
    }))

    expect(screen.getByText('How did you manage shared state between the agents?')).toBeInTheDocument()
    expect(screen.getByText("I'd like to explore that a little further.")).toBeInTheDocument()
    expect(screen.queryByText(/follow-up question/i)).not.toBeInTheDocument()
  })

  it('closes naturally before offering the existing report action', () => {
    const evaluatedTurn: V2InterviewTurn = {
      ...firstTechnicalTurn,
      status: 'evaluated',
      answer: 'We isolated each agent and persisted shared state.',
      candidate_answer: 'We isolated each agent and persisted shared state.',
      evaluation: {
        turn_id: 'turn-1',
        overall_score: 8,
        technical_score: 8,
        communication_score: 8,
        correctness_score: 8,
        strengths: ['Private strength'],
        weaknesses: ['Private weakness'],
        missing_concepts: [],
        follow_up_needed: false,
        feedback: 'Private evaluator feedback',
      },
    }

    renderRoom(sessionState({
      phase: 'closing',
      current_turn: null,
      completed_turns: [evaluatedTurn],
    }))

    expect(screen.getByText(/That's all the questions I have for today/)).toBeInTheDocument()
    expect(screen.getByText(/Your interview is now complete/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'View report' })).toBeInTheDocument()
    expect(screen.queryByText('Private evaluator feedback')).not.toBeInTheDocument()
    expect(screen.queryByText('Private strength')).not.toBeInTheDocument()
    expect(screen.queryByText('Private weakness')).not.toBeInTheDocument()
  })
})

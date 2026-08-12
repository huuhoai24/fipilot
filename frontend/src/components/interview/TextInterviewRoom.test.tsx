import React, { act } from 'react'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
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
  options: {
    answer?: string
    sessionId?: string
    onSubmit?: (event: React.FormEvent<HTMLFormElement>) => void
    pendingAnswer?: string | null
    submitting?: boolean
    startedAt?: string | null
  } = {},
) {
  return render(
    <TextInterviewRoom
      state={state}
      sessionId={options.sessionId}
      persona={resolveInterviewerPersona(state.interview_config.interview_style)}
      progress={{ current: 1, total: 4 }}
      answer={options.answer ?? ''}
      pendingAnswer={options.pendingAnswer ?? null}
      submitting={options.submitting ?? false}
      startedAt={options.startedAt ?? null}
      error={null}
      onAnswerChange={vi.fn()}
      onSubmit={options.onSubmit ?? vi.fn()}
      onViewReport={vi.fn()}
      onBackToHistory={vi.fn()}
    />,
  )
}

afterEach(cleanup)

describe('TextInterviewRoom conversation phases', () => {
  it('offers microphone input without replacing the text composer', () => {
    renderRoom(sessionState({}), { sessionId: 'session-42' })

    expect(screen.getByRole('button', { name: 'Start recording' })).toBeEnabled()
    expect(screen.getByLabelText('Your answer')).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Submit answer' })).toBeDisabled()
  })

  it('keeps the composer compact, grows with its content, and scrolls after the height cap', () => {
    function ComposerHarness() {
      const [answer, setAnswer] = React.useState('')
      return (
        <TextInterviewRoom
          state={sessionState({})}
          persona={resolveInterviewerPersona('technical')}
          progress={{ current: 1, total: 4 }}
          answer={answer}
          pendingAnswer={null}
          submitting={false}
          startedAt={null}
          error={null}
          onAnswerChange={setAnswer}
          onSubmit={vi.fn()}
          onViewReport={vi.fn()}
          onBackToHistory={vi.fn()}
        />
      )
    }

    render(<ComposerHarness />)
    const composer = screen.getByLabelText('Your answer')
    let contentHeight = 72
    Object.defineProperty(composer, 'scrollHeight', {
      configurable: true,
      get: () => contentHeight,
    })

    expect(composer).toHaveAttribute('rows', '2')
    fireEvent.change(composer, { target: { value: 'Short answer' } })
    expect(composer).toHaveStyle({ height: '72px', overflowY: 'hidden' })

    contentHeight = 220
    fireEvent.change(composer, { target: { value: 'A much longer answer\n'.repeat(12) } })
    expect(composer).toHaveStyle({ height: '144px', overflowY: 'auto' })

    contentHeight = 96
    fireEvent.change(composer, { target: { value: 'A shorter answer again' } })
    expect(composer).toHaveStyle({ height: '96px', overflowY: 'hidden' })
  })

  it('derives elapsed time from the persisted session start without resetting on rerender', () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-08-11T03:01:30Z'))

    try {
      const view = renderRoom(sessionState({}), {
        startedAt: '2026-08-11T03:00:00Z',
      })

      expect(screen.getByLabelText('Elapsed interview time')).toHaveTextContent('00:01:30')

      act(() => vi.advanceTimersByTime(1_000))
      expect(screen.getByLabelText('Elapsed interview time')).toHaveTextContent('00:01:31')

      view.rerender(
        <TextInterviewRoom
          state={sessionState({})}
          persona={resolveInterviewerPersona('technical')}
          progress={{ current: 1, total: 4 }}
          answer="Draft answer"
          pendingAnswer={null}
          submitting={false}
          startedAt="2026-08-11T03:00:00Z"
          error={null}
          onAnswerChange={vi.fn()}
          onSubmit={vi.fn()}
          onViewReport={vi.fn()}
          onBackToHistory={vi.fn()}
        />,
      )
      expect(screen.getByLabelText('Elapsed interview time')).toHaveTextContent('00:01:31')
    } finally {
      vi.useRealTimers()
    }
  })

  it('keeps Enter multiline and submits only with Ctrl or Command plus Enter', () => {
    const onSubmit = vi.fn((event) => event.preventDefault())
    renderRoom(sessionState({}), { answer: 'A complete answer', onSubmit })
    const composer = screen.getByLabelText('Your answer')

    fireEvent.keyDown(composer, { key: 'Enter' })
    expect(onSubmit).not.toHaveBeenCalled()

    fireEvent.keyDown(composer, { key: 'Enter', ctrlKey: true })
    expect(onSubmit).toHaveBeenCalledOnce()
  })

  it('does not submit an empty answer', () => {
    const onSubmit = vi.fn((event) => event.preventDefault())
    renderRoom(sessionState({}), { answer: '   ', onSubmit })
    const composer = screen.getByLabelText('Your answer')

    expect(screen.getByRole('button', { name: 'Submit answer' })).toBeDisabled()
    fireEvent.keyDown(composer, { key: 'Enter', metaKey: true })
    expect(onSubmit).not.toHaveBeenCalled()
  })

  it('does not force-scroll to a new question while the candidate is reading older messages', () => {
    const scrollIntoView = vi.fn()
    Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', {
      configurable: true,
      value: scrollIntoView,
    })
    Object.defineProperty(document.documentElement, 'scrollHeight', {
      configurable: true,
      value: 2400,
    })
    Object.defineProperty(window, 'innerHeight', {
      configurable: true,
      value: 700,
    })
    Object.defineProperty(window, 'scrollY', {
      configurable: true,
      value: 0,
    })

    const view = renderRoom(sessionState({}))
    expect(scrollIntoView).toHaveBeenCalledOnce()
    window.dispatchEvent(new Event('scroll'))

    const nextState = sessionState({
      current_turn: {
        ...firstTechnicalTurn,
        turn_id: 'turn-2',
        question: 'How did you validate the workflow?',
      },
      current_question_index: 1,
    })
    view.rerender(
      <TextInterviewRoom
        state={nextState}
        persona={resolveInterviewerPersona('technical')}
        progress={{ current: 2, total: 4 }}
        answer=""
        pendingAnswer={null}
        submitting={false}
        error={null}
        onAnswerChange={vi.fn()}
        onSubmit={vi.fn()}
        onViewReport={vi.fn()}
        onBackToHistory={vi.fn()}
      />,
    )

    expect(scrollIntoView).toHaveBeenCalledOnce()
  })

  it('renders the selected fictional AI persona throughout the active room', () => {
    renderRoom(
      sessionState({}),
      { pendingAnswer: 'My submitted answer', submitting: true },
    )

    expect(screen.getByRole('heading', { level: 1, name: 'Sarah Nguyen' })).toBeInTheDocument()
    expect(screen.getByText('AI Virtual Interviewer')).toBeInTheDocument()
    expect(screen.getByText('Technical Interviewer')).toBeInTheDocument()
    expect(screen.queryByText('Technical knowledge, projects, and system design')).not.toBeInTheDocument()
    expect(screen.queryByText(/explore your technical decisions/i)).not.toBeInTheDocument()
    expect(screen.getByText('Sarah Nguyen is preparing the next question...')).toBeInTheDocument()
    expect(screen.queryByText('FiPilot interviewer is preparing the next question...')).not.toBeInTheDocument()
  })

  it('keeps visual form labels quiet while preserving accessible conversation and composer names', () => {
    renderRoom(sessionState({}), { pendingAnswer: 'A candidate response' })

    expect(screen.getByRole('heading', { level: 2, name: 'Conversation' })).toHaveClass('sr-only')
    expect(screen.getByText('Your answer')).toHaveClass('sr-only')
    expect(screen.getByLabelText('Your answer')).toHaveAttribute('placeholder', 'Type your answer...')

    const currentQuestion = screen.getByRole('article', {
      name: 'Current question from Sarah Nguyen',
    })
    const candidateResponse = screen.getByRole('article', {
      name: 'Response from Trieu Vo',
    })

    expect(currentQuestion).toHaveAttribute('aria-current', 'true')
    expect(currentQuestion.closest('li')).toHaveClass('w-full', 'sm:w-[78%]')
    expect(candidateResponse.closest('li')).toHaveClass('ml-auto', 'w-full', 'sm:w-[78%]')
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
    expect(screen.getAllByText('Complete')).toHaveLength(2)
    expect(screen.queryByText(/Question \d+ of \d+/)).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'View report' })).toBeInTheDocument()
    expect(screen.queryByText('Private evaluator feedback')).not.toBeInTheDocument()
    expect(screen.queryByText('Private strength')).not.toBeInTheDocument()
    expect(screen.queryByText('Private weakness')).not.toBeInTheDocument()
  })
})

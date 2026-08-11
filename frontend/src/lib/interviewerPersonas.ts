export type InterviewerPersonaId =
  | 'default'
  | 'technical'
  | 'hr'
  | 'behavioral'
  | 'english'

export interface InterviewerPersonaAvatar {
  /** Optional path for a local, fictional asset. Initials remain the safe fallback. */
  src?: string
  initials: string
}

export interface InterviewerPersona {
  id: InterviewerPersonaId
  name: string
  role: string
  specialization?: string
  avatar: InterviewerPersonaAvatar
  shortDescription: string
}

export const AI_INTERVIEWER_LABEL = 'AI Virtual Interviewer'

const DEFAULT_PERSONA: InterviewerPersona = {
  id: 'default',
  name: 'FiPilot Interviewer',
  role: AI_INTERVIEWER_LABEL,
  specialization: 'Guided interview practice',
  avatar: { initials: 'FI' },
  shortDescription: 'I’ll guide you through this interview one question at a time.',
}

export const INTERVIEWER_PERSONAS: Readonly<Record<InterviewerPersonaId, InterviewerPersona>> = {
  default: DEFAULT_PERSONA,
  technical: {
    id: 'technical',
    name: 'Sarah Nguyen',
    role: 'Technical Interviewer',
    specialization: 'Technical knowledge, projects, and system design',
    avatar: { initials: 'SN' },
    shortDescription: 'I’ll explore your technical decisions, project experience, and system-design thinking.',
  },
  hr: {
    id: 'hr',
    name: 'Mia Tran',
    role: 'HR Interviewer',
    specialization: 'Background, motivation, career goals, and culture fit',
    avatar: { initials: 'MT' },
    shortDescription: 'I’ll guide a professional conversation about your background, motivation, and career direction.',
  },
  behavioral: {
    id: 'behavioral',
    name: 'Alex Chen',
    role: 'Behavioral Interviewer',
    specialization: 'Teamwork, conflict, leadership, and STAR-style questions',
    avatar: { initials: 'AC' },
    shortDescription: 'I’ll help you explain how you worked with others, handled challenges, and led through change.',
  },
  english: {
    id: 'english',
    name: 'Emma Lee',
    role: 'English Interviewer',
    specialization: 'Professional English interview practice',
    avatar: { initials: 'EL' },
    shortDescription: 'I’ll help you practice clear, confident answers in a professional English interview.',
  },
}

export function resolveInterviewerPersona(interviewStyle: string | null | undefined): InterviewerPersona {
  const persona = INTERVIEWER_PERSONAS[interviewStyle?.trim().toLowerCase() as InterviewerPersonaId]
  return persona ?? DEFAULT_PERSONA
}

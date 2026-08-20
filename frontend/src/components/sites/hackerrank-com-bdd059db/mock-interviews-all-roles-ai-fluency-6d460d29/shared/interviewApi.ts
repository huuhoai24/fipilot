import type { ResumeProfile } from "./resumeApi";
import { getAnonymousClientId } from "./clientIdentity";

export interface InterviewSetup {
  clientId: string;
  sessionId: string;
  resumeId: string | null;
  role: string;
  level: string;
  customDescription: string;
  workExperience: Array<Record<string, unknown>>;
}

export interface InterviewQuestion {
  company: string;
  question: string;
  project: string;
  project_context: Record<string, unknown>;
  rubric: {
    evaluation_goal: string;
    critical_points: string[];
    met: string;
    partially_met: string;
    not_met: string;
  };
  topic: string;
}

export interface AnswerEvaluation {
  score: number;
  status: "MET" | "PARTIALLY_MET" | "NOT_MET" | "NOT_ASSESSED";
  evidence_quote: string;
  justification: string;
  should_follow_up: boolean;
  next_direction: string;
  matched_points: string[];
  missing_points: string[];
  technical_errors: string[];
}

export interface InterviewTurn {
  question: InterviewQuestion;
  answer: string;
  timestamp: string;
}

export interface ReportAssessment {
  turn_index: number;
  evaluation_goal: string;
  raw_score: number;
  status: "MET" | "PARTIALLY_MET" | "NOT_MET" | "NOT_ASSESSED";
  rationale: string;
  evidence: Array<{ timestamp: string; quote: string }>;
}

export interface InterviewReport {
  assessments: ReportAssessment[];
  solutions_summary: string;
  overall_assessment: string;
  recommendations: string;
  normalized_score: number;
  coverage_ratio: number;
}

interface InterviewQuestionResult {
  questions: InterviewQuestion[];
}

interface NextInterviewQuestionResult {
  decision: AnswerEvaluation;
  follow_up_count: number;
  question: InterviewQuestion;
}

export const INTERVIEW_SETUP_STORAGE_KEY = "interview_setup";
const INTERVIEW_QUESTIONS_STORAGE_KEY = "interview_questions";
let preparedQuestions: Promise<InterviewQuestionResult> | null = null;

function turnsStorageKey(sessionId: string) {
  return `interview_turns:${sessionId}`;
}

function reportStorageKey(sessionId: string) {
  return `interview_report:${sessionId}`;
}

export function createInterviewSetup(
  sessionId: string,
  resumeId: string | null,
  role: string,
  level: string,
  customDescription: string,
  profile: ResumeProfile,
): InterviewSetup {
  return {
    clientId: getAnonymousClientId(),
    sessionId,
    resumeId,
    role,
    level,
    customDescription,
    workExperience: profile.workExperience ?? [],
  };
}

export function saveInterviewSetup(setup: InterviewSetup) {
  sessionStorage.setItem(INTERVIEW_SETUP_STORAGE_KEY, JSON.stringify(setup));
  sessionStorage.removeItem(INTERVIEW_QUESTIONS_STORAGE_KEY);
  preparedQuestions = null;
}

export function loadInterviewSetup(): InterviewSetup | null {
  const rawSetup = sessionStorage.getItem(INTERVIEW_SETUP_STORAGE_KEY);
  if (rawSetup === null) return null;
  try {
    const setup = JSON.parse(rawSetup) as Partial<InterviewSetup>;
    if (!setup.role || !setup.level || !Array.isArray(setup.workExperience)) return null;
    return {
      clientId: setup.clientId ?? getAnonymousClientId(),
      sessionId: setup.sessionId ?? `mock-${crypto.randomUUID()}`,
      resumeId: setup.resumeId ?? null,
      role: setup.role,
      level: setup.level,
      customDescription: setup.customDescription ?? "",
      workExperience: setup.workExperience,
    };
  } catch {
    return null;
  }
}

async function requestInterviewQuestions(setup: InterviewSetup) {
  const response = await fetch("/api/interview/questions", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      client_id: setup.clientId,
      session_id: setup.sessionId,
      resume_id: setup.resumeId,
      role: setup.role,
      level: setup.level,
      custom_description: setup.customDescription,
      work_experience: setup.workExperience,
      count: 1,
    }),
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(body?.detail ?? `Question generation failed (HTTP ${response.status})`);
  }
  return response.json() as Promise<InterviewQuestionResult>;
}

export function prepareInterviewQuestions(setup: InterviewSetup) {
  preparedQuestions = requestInterviewQuestions(setup).then((result) => {
    sessionStorage.setItem(INTERVIEW_QUESTIONS_STORAGE_KEY, JSON.stringify(result));
    return result;
  });
  return preparedQuestions;
}

export function getPreparedInterviewQuestions() {
  if (preparedQuestions !== null) return preparedQuestions;
  const cachedQuestions = sessionStorage.getItem(INTERVIEW_QUESTIONS_STORAGE_KEY);
  if (cachedQuestions !== null) {
    try {
      const cached = JSON.parse(cachedQuestions) as InterviewQuestionResult;
      if (!cached.questions[0]?.rubric || !cached.questions[0]?.project_context) {
        throw new Error("Cached interview question uses the old schema");
      }
      preparedQuestions = Promise.resolve(cached);
      return preparedQuestions;
    } catch {
      sessionStorage.removeItem(INTERVIEW_QUESTIONS_STORAGE_KEY);
    }
  }
  const setup = loadInterviewSetup();
  if (setup === null) return Promise.reject(new Error("Interview setup is missing"));
  return prepareInterviewQuestions(setup);
}

export async function requestNextInterviewQuestion(
  currentQuestion: InterviewQuestion,
  answer: string,
  followUpCount: number,
  usedProjectNames: string[],
) {
  const setup = loadInterviewSetup();
  if (setup === null) throw new Error("Interview setup is missing");
  const response = await fetch("/api/interview/next", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      client_id: setup.clientId,
      session_id: setup.sessionId,
      resume_id: setup.resumeId,
      role: setup.role,
      level: setup.level,
      custom_description: setup.customDescription,
      work_experience: setup.workExperience,
      current_question: currentQuestion,
      current_project: currentQuestion.project_context,
      answer,
      follow_up_count: followUpCount,
      used_project_names: usedProjectNames,
    }),
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(body?.detail ?? `Next question failed (HTTP ${response.status})`);
  }
  return response.json() as Promise<NextInterviewQuestionResult>;
}

export function saveInterviewTurn(
  sessionId: string,
  question: InterviewQuestion,
  answer: string,
) {
  const turns = loadInterviewTurns(sessionId);
  turns.push({ question, answer, timestamp: new Date().toISOString() });
  sessionStorage.setItem(turnsStorageKey(sessionId), JSON.stringify(turns));
}

export function loadInterviewTurns(sessionId: string): InterviewTurn[] {
  const rawTurns = sessionStorage.getItem(turnsStorageKey(sessionId));
  if (rawTurns === null) return [];
  try {
    return JSON.parse(rawTurns) as InterviewTurn[];
  } catch {
    return [];
  }
}

export async function createInterviewReport(sessionId: string) {
  const setup = loadInterviewSetup();
  if (setup === null) throw new Error("Interview setup is missing");
  const response = await fetch("/api/interview/report", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      client_id: setup.clientId,
      session_id: sessionId,
      role: setup.role,
      level: setup.level,
      turns: loadInterviewTurns(sessionId),
    }),
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(body?.detail ?? `Report generation failed (HTTP ${response.status})`);
  }
  const report = await response.json() as InterviewReport;
  sessionStorage.setItem(reportStorageKey(sessionId), JSON.stringify(report));
  return report;
}

export function loadInterviewReport(sessionId: string): InterviewReport | null {
  const rawReport = sessionStorage.getItem(reportStorageKey(sessionId));
  if (rawReport === null) return null;
  try {
    return JSON.parse(rawReport) as InterviewReport;
  } catch {
    return null;
  }
}

export async function fetchPersistedInterview(sessionId: string) {
  const response = await fetch(
    `/api/interview/${encodeURIComponent(sessionId)}?client_id=${encodeURIComponent(getAnonymousClientId())}`,
    { cache: "no-store" },
  );
  if (!response.ok) return null;
  const result = await response.json() as {
    report: InterviewReport | null;
    turns: InterviewTurn[];
  };
  sessionStorage.setItem(turnsStorageKey(sessionId), JSON.stringify(result.turns));
  if (result.report !== null) {
    sessionStorage.setItem(reportStorageKey(sessionId), JSON.stringify(result.report));
  }
  return result;
}

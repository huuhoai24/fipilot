import { focusResumeForRole, type ResumeExperience, type ResumeProfile } from "./resumeApi";
import { getAnonymousClientId } from "./clientIdentity";

export interface InterviewSetup {
  clientId: string;
  sessionId: string;
  resumeId: string | null;
  role: string;
  level: string;
  customDescription: string;
  workExperience: ResumeExperience[];
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
  raw_llm_score: number;
  validated_score: number;
  final_score: number;
  score_scale: 10;
  score_correction_reason: string;
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
  raw_score: number | null;
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
  score_scale: 10;
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
const INTERVIEW_SETUP_STORAGE_PREFIX = `${INTERVIEW_SETUP_STORAGE_KEY}:`;
const INTERVIEW_QUESTIONS_STORAGE_PREFIX = "interview_questions:";
const INTERVIEW_TURNS_STORAGE_PREFIX = "interview_turns:";
const INTERVIEW_REPORT_STORAGE_PREFIX = "interview_report:";
const preparedQuestions = new Map<string, Promise<InterviewQuestionResult>>();
const nextQuestionRequests = new Map<string, Promise<NextInterviewQuestionResult>>();

function setupStorageKey(sessionId: string) {
  return `${INTERVIEW_SETUP_STORAGE_PREFIX}${sessionId}`;
}

function questionsStorageKey(sessionId: string) {
  return `${INTERVIEW_QUESTIONS_STORAGE_PREFIX}${sessionId}`;
}

function turnsStorageKey(sessionId: string) {
  return `${INTERVIEW_TURNS_STORAGE_PREFIX}${sessionId}`;
}

function reportStorageKey(sessionId: string) {
  return `${INTERVIEW_REPORT_STORAGE_PREFIX}${sessionId}`;
}

export function createInterviewSetup(
  sessionId: string,
  resumeId: string | null,
  role: string,
  level: string,
  customDescription: string,
  profile: ResumeProfile,
  roleId?: string,
): InterviewSetup {
  const focusedProfile = roleId === undefined ? profile : focusResumeForRole(profile, roleId);
  return {
    clientId: getAnonymousClientId(),
    sessionId,
    resumeId,
    role,
    level,
    customDescription,
    workExperience: focusedProfile.workExperience ?? [],
  };
}

export function saveInterviewSetup(setup: InterviewSetup) {
  sessionStorage.setItem(INTERVIEW_SETUP_STORAGE_KEY, setup.sessionId);
  sessionStorage.setItem(setupStorageKey(setup.sessionId), JSON.stringify(setup));
  sessionStorage.removeItem(questionsStorageKey(setup.sessionId));
  preparedQuestions.delete(setup.sessionId);
  nextQuestionRequests.delete(setup.sessionId);
}

export function loadInterviewSetup(sessionId?: string): InterviewSetup | null {
  const selectedSessionId = sessionId ?? sessionStorage.getItem(INTERVIEW_SETUP_STORAGE_KEY);
  if (selectedSessionId === null) return null;
  const rawSetup = sessionStorage.getItem(setupStorageKey(selectedSessionId));
  if (rawSetup === null) return null;
  try {
    const setup = JSON.parse(rawSetup) as Partial<InterviewSetup>;
    if (
      !setup.clientId
      || setup.sessionId !== selectedSessionId
      || !setup.role
      || !setup.level
      || !Array.isArray(setup.workExperience)
    ) return null;
    return {
      clientId: setup.clientId,
      sessionId: selectedSessionId,
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
  const existingRequest = preparedQuestions.get(setup.sessionId);
  if (existingRequest !== undefined) return existingRequest;
  const request = requestInterviewQuestions(setup).then((result) => {
    sessionStorage.setItem(questionsStorageKey(setup.sessionId), JSON.stringify(result));
    return result;
  }).catch((error: unknown) => {
    if (preparedQuestions.get(setup.sessionId) === request) {
      preparedQuestions.delete(setup.sessionId);
    }
    throw error;
  });
  preparedQuestions.set(setup.sessionId, request);
  return request;
}

export function getPreparedInterviewQuestions(sessionId: string) {
  const prepared = preparedQuestions.get(sessionId);
  if (prepared !== undefined) return prepared;
  const cachedQuestions = sessionStorage.getItem(questionsStorageKey(sessionId));
  if (cachedQuestions !== null) {
    try {
      const cached = JSON.parse(cachedQuestions) as InterviewQuestionResult;
      if (!cached.questions[0]?.rubric || !cached.questions[0]?.project_context) {
        throw new Error("Cached interview question uses the old schema");
      }
      const cachedRequest = Promise.resolve(cached);
      preparedQuestions.set(sessionId, cachedRequest);
      return cachedRequest;
    } catch {
      sessionStorage.removeItem(questionsStorageKey(sessionId));
    }
  }
  const setup = loadInterviewSetup(sessionId);
  if (setup === null) return Promise.reject(new Error("Interview setup is missing"));
  return prepareInterviewQuestions(setup);
}

export async function requestNextInterviewQuestion(
  sessionId: string,
  currentQuestion: InterviewQuestion,
  answer: string,
  followUpCount: number,
  usedProjectNames: string[],
  usedQuestionTexts: string[] = [],
) {
  const existingRequest = nextQuestionRequests.get(sessionId);
  if (existingRequest !== undefined) return existingRequest;
  const setup = loadInterviewSetup(sessionId);
  if (setup === null) throw new Error("Interview setup is missing");
  const request = (async () => {
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
        used_question_texts: usedQuestionTexts,
      }),
    });
    if (!response.ok) {
      const body = (await response.json().catch(() => null)) as { detail?: string } | null;
      throw new Error(body?.detail ?? `Next question failed (HTTP ${response.status})`);
    }
    return response.json() as Promise<NextInterviewQuestionResult>;
  })();
  nextQuestionRequests.set(sessionId, request);
  try {
    return await request;
  } finally {
    if (nextQuestionRequests.get(sessionId) === request) {
      nextQuestionRequests.delete(sessionId);
    }
  }
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
  const setup = loadInterviewSetup(sessionId);
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

export function clearInterviewState() {
  const keysToRemove: string[] = [];
  for (let index = 0; index < sessionStorage.length; index += 1) {
    const key = sessionStorage.key(index);
    if (key !== null && (
      key === INTERVIEW_SETUP_STORAGE_KEY
      || key.startsWith(INTERVIEW_SETUP_STORAGE_PREFIX)
      || key.startsWith(INTERVIEW_QUESTIONS_STORAGE_PREFIX)
      || key.startsWith(INTERVIEW_TURNS_STORAGE_PREFIX)
      || key.startsWith(INTERVIEW_REPORT_STORAGE_PREFIX)
    )) {
      keysToRemove.push(key);
    }
  }
  keysToRemove.forEach((key) => sessionStorage.removeItem(key));
  preparedQuestions.clear();
  nextQuestionRequests.clear();
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

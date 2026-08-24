import { afterAll, beforeEach, describe, expect, it, vi } from "vitest";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

import {
  clearResumeAnalysis,
  loadResumeAnalysis,
  summarizeResumeExtraction,
  type ResumeProfile,
} from "../../src/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/shared/resumeApi";
import {
  createInterviewReport,
  loadInterviewSetup,
  prepareInterviewQuestions,
  requestNextInterviewQuestion,
  saveInterviewSetup,
  saveInterviewTurn,
  loadInterviewTurns,
  type InterviewQuestion,
  type InterviewSetup,
} from "../../src/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/shared/interviewApi";
import { fetchLatestResume } from "../../src/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/shared/resumeApi";
import { loginUser } from "../../src/lib/auth";

type Status = "PASS" | "FAIL" | "PARTIAL" | "BLOCKED" | "NOT TESTED" | "NOT EVALUATED";
interface Result {
  test_id: string;
  agent: string;
  scenario: string;
  expected: string;
  actual: unknown;
  status: Status;
  severity: string;
}

const results: Result[] = [];

function record(result: Result) {
  results.push(result);
}

const question: InterviewQuestion = {
  company: "Portfolio",
  project: "Portfolio",
  project_context: { name: "Portfolio", jobDescription: "Built React screens" },
  question: "How did you structure this React project?",
  topic: "React",
  rubric: {
    evaluation_goal: "Assess React structure",
    critical_points: ["Boundaries"],
    met: "Explains boundaries",
    partially_met: "Names boundaries",
    not_met: "No mechanism",
  },
};

function setup(sessionId: string, role: string, clientId: string): InterviewSetup {
  return {
    clientId,
    sessionId,
    resumeId: null,
    role,
    level: "Junior",
    customDescription: "",
    workExperience: [{
      type: "Project",
      name: role === "Web Developer" ? "Portfolio" : "Payments",
      position: "",
      jobDescription: role === "Web Developer" ? "React CSS" : "Spring Kafka",
    }],
  };
}

function jsonResponse(body: unknown, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as Response;
}

describe.sequential("FiPilot frontend robustness evidence", () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
    vi.restoreAllMocks();
    vi.stubGlobal("crypto", { randomUUID: () => "00000000-0000-4000-8000-000000000001" });
  });

  it("READY-001 accepts complete resume evidence", () => {
    const summary = summarizeResumeExtraction({
      skills: ["FastAPI"],
      workExperience: [{ type: "Work", name: "API team", position: "Developer", jobDescription: "Built APIs" }],
    });
    expect(summary.canContinue).toBe(true);
    expect(summary.isComplete).toBe(true);
    record({ test_id: "READY-001", agent: "summarizeResumeExtraction", scenario: "Complete resume evidence", expected: "Ready and complete", actual: summary, status: "PASS", severity: "" });
  });

  it("READY-002 allows a student project", () => {
    const summary = summarizeResumeExtraction({
      skills: ["Python"],
      workExperience: [{ type: "Project", name: "University project", position: "", jobDescription: "Built a Python application" }],
    });
    expect(summary.canContinue).toBe(true);
    record({ test_id: "READY-002", agent: "summarizeResumeExtraction", scenario: "Fresher with project only", expected: "Do not reject merely for lacking employment", actual: summary, status: "PASS", severity: "" });
  });

  it("READY-003 has no education-only readiness path", () => {
    const summary = summarizeResumeExtraction({ education: [{ institution: "Synthetic University" }] });
    expect(summary.canContinue).toBe(false);
    record({ test_id: "READY-003", agent: "summarizeResumeExtraction", scenario: "Education only", expected: "Explicit policy/reason from a shared readiness contract", actual: summary, status: "PARTIAL", severity: "MEDIUM" });
  });

  it("READY-004 contains wrong entry types without crashing", () => {
    const profile = { workExperience: [null, "noise", 123] } as unknown as ResumeProfile;
    const summary = summarizeResumeExtraction(profile);
    expect(summary.canContinue).toBe(false);
    expect(summary.issues.length).toBeGreaterThan(0);
    record({ test_id: "READY-004", agent: "summarizeResumeExtraction", scenario: "Wrong workExperience entry types", expected: "No crash and not ready", actual: summary, status: "PASS", severity: "" });
  });

  it("UX-001 coalesces duplicate first-question requests", async () => {
    let calls = 0;
    vi.stubGlobal("fetch", vi.fn(async () => {
      calls += 1;
      return jsonResponse({ questions: [question] });
    }));
    const value = setup("session-a", "Web Developer", "client-a");
    saveInterviewSetup(value);
    await Promise.all([prepareInterviewQuestions(value), prepareInterviewQuestions(value)]);
    expect(calls).toBe(1);
    record({ test_id: "UX-001", agent: "prepareInterviewQuestions", scenario: "Rapid double-click/start", expected: "One in-flight request per setup", actual: { fetch_calls: calls }, status: "PASS", severity: "HIGH" });
  });

  it("UX-REG failed first-question request allows a legitimate retry", async () => {
    let calls = 0;
    vi.stubGlobal("fetch", vi.fn(async () => {
      calls += 1;
      return calls === 1
        ? jsonResponse({ detail: "temporary failure" }, 503)
        : jsonResponse({ questions: [question] });
    }));
    const value = setup("session-retry", "Web Developer", "client-retry");
    saveInterviewSetup(value);

    await expect(prepareInterviewQuestions(value)).rejects.toThrow("temporary failure");
    await expect(prepareInterviewQuestions(value)).resolves.toEqual({ questions: [question] });

    expect(calls).toBe(2);
  });

  it("UX-REG rapid submit coalesces one next-question request", async () => {
    let calls = 0;
    vi.stubGlobal("fetch", vi.fn(async () => {
      calls += 1;
      return jsonResponse({
        decision: { score: 2, status: "PARTIALLY_MET", evidence_quote: "answer", justification: "partial", should_follow_up: false, next_direction: "", matched_points: [], missing_points: [], technical_errors: [] },
        follow_up_count: 0,
        question,
      });
    }));
    saveInterviewSetup(setup("session-submit", "Web Developer", "client-submit"));

    await Promise.all([
      requestNextInterviewQuestion("session-submit", question, "answer", 0, []),
      requestNextInterviewQuestion("session-submit", question, "answer", 0, []),
    ]);

    expect(calls).toBe(1);
  });

  it("UX-REG next-question coalescing remains isolated by session", async () => {
    const sessionIds: string[] = [];
    vi.stubGlobal("fetch", vi.fn(async (_url: string, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body)) as { session_id: string };
      sessionIds.push(body.session_id);
      return jsonResponse({
        decision: { score: 2, status: "PARTIALLY_MET", evidence_quote: "answer", justification: "partial", should_follow_up: false, next_direction: "", matched_points: [], missing_points: [], technical_errors: [] },
        follow_up_count: 0,
        question,
      });
    }));
    saveInterviewSetup(setup("session-a", "Web Developer", "client-a"));
    saveInterviewSetup(setup("session-b", "Backend Developer", "client-b"));

    await Promise.all([
      requestNextInterviewQuestion("session-a", question, "answer a", 0, []),
      requestNextInterviewQuestion("session-b", question, "answer b", 0, []),
    ]);

    expect(sessionIds.sort()).toEqual(["session-a", "session-b"]);
  });

  it("UX-REG failed next-question request allows a legitimate retry", async () => {
    let calls = 0;
    vi.stubGlobal("fetch", vi.fn(async () => {
      calls += 1;
      if (calls === 1) return jsonResponse({ detail: "temporary next failure" }, 503);
      return jsonResponse({
        decision: { score: 2, status: "PARTIALLY_MET", evidence_quote: "answer", justification: "partial", should_follow_up: false, next_direction: "", matched_points: [], missing_points: [], technical_errors: [] },
        follow_up_count: 0,
        question,
      });
    }));
    saveInterviewSetup(setup("session-next-retry", "Web Developer", "client-next-retry"));

    await expect(
      requestNextInterviewQuestion("session-next-retry", question, "answer", 0, []),
    ).rejects.toThrow("temporary next failure");
    await expect(
      requestNextInterviewQuestion("session-next-retry", question, "answer", 0, []),
    ).resolves.toMatchObject({ question });

    expect(calls).toBe(2);
  });

  it("STATE-03 question generation uses the requested session profile", async () => {
    let requestBody: Record<string, unknown> = {};
    vi.stubGlobal("fetch", vi.fn(async (_url: string, init?: RequestInit) => {
      requestBody = JSON.parse(String(init?.body)) as Record<string, unknown>;
      return jsonResponse({
        decision: { score: 2, status: "PARTIALLY_MET", evidence_quote: "answer", justification: "partial", should_follow_up: false, next_direction: "", matched_points: [], missing_points: [], technical_errors: [] },
        follow_up_count: 0,
        question,
      });
    }));
    saveInterviewSetup(setup("session-a", "Web Developer", "client-a"));
    saveInterviewSetup(setup("session-b", "Backend Developer", "client-b"));
    await requestNextInterviewQuestion("session-a", question, "answer", 0, []);
    expect(requestBody).toMatchObject({
      session_id: "session-a",
      client_id: "client-a",
      role: "Web Developer",
    });
    expect(requestBody.work_experience).toEqual(setup("session-a", "Web Developer", "client-a").workExperience);
    record({ test_id: "STATE-03", agent: "requestNextInterviewQuestion", scenario: "Two interviews open rapidly", expected: "Session A request uses only A setup", actual: requestBody, status: "PASS", severity: "CRITICAL" });
  });

  it("STATE-04 report uses the requested interview setup and transcript", async () => {
    let requestBody: Record<string, unknown> = {};
    vi.stubGlobal("fetch", vi.fn(async (_url: string, init?: RequestInit) => {
      requestBody = JSON.parse(String(init?.body)) as Record<string, unknown>;
      return jsonResponse({ assessments: [], solutions_summary: "", overall_assessment: "", recommendations: "", normalized_score: 0, coverage_ratio: 0 });
    }));
    saveInterviewSetup(setup("session-a", "Web Developer", "client-a"));
    saveInterviewTurn("session-a", question, "answer a");
    saveInterviewSetup(setup("session-b", "Backend Developer", "client-b"));
    await createInterviewReport("session-a");
    expect(requestBody).toMatchObject({
      session_id: "session-a",
      client_id: "client-a",
      role: "Web Developer",
    });
    expect(requestBody.turns).toEqual(loadInterviewTurns("session-a"));
    record({ test_id: "STATE-04", agent: "createInterviewReport", scenario: "Generate report for A after starting B", expected: "Session A report uses only A setup and turns", actual: requestBody, status: "PASS", severity: "CRITICAL" });
  });

  it("STATE-02 keeps two active session setups and transcripts independent", () => {
    const sessionA = setup("session-a", "Web Developer", "client-a");
    const sessionB = setup("session-b", "Backend Developer", "client-b");
    saveInterviewSetup(sessionA);
    saveInterviewSetup(sessionB);
    saveInterviewTurn("session-a", question, "answer a");
    saveInterviewTurn("session-b", question, "answer b");
    const a = loadInterviewTurns("session-a");
    const b = loadInterviewTurns("session-b");
    expect(loadInterviewSetup("session-a")).toEqual(sessionA);
    expect(loadInterviewSetup("session-b")).toEqual(sessionB);
    expect(a[0]?.answer).toBe("answer a");
    expect(b[0]?.answer).toBe("answer b");
    record({ test_id: "STATE-02", agent: "interview storage", scenario: "Two sessions active independently", expected: "No setup or turn leakage", actual: { a, b }, status: "PASS", severity: "CRITICAL" });
  });

  it("UX-002 distinguishes latest-resume API errors from an empty result", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => jsonResponse({ detail: "Database unavailable" }, 503)));
    let actual = "";
    try {
      await fetchLatestResume();
    } catch (error) {
      actual = error instanceof Error ? error.message : String(error);
    }
    expect(actual).toBe("Database unavailable");
    record({ test_id: "UX-002", agent: "fetchLatestResume", scenario: "Backend 503", expected: "Distinguish service failure from no saved resume", actual, status: "PASS", severity: "" });
  });

  it("UX-003 clears malformed cached resume JSON", () => {
    localStorage.setItem("resume_analysis", "{broken");
    const value = loadResumeAnalysis();
    expect(value).toBeNull();
    expect(localStorage.getItem("resume_analysis")).toBeNull();
    record({ test_id: "UX-003", agent: "loadResumeAnalysis", scenario: "Malformed local cache", expected: "Clear corrupt cache without crash", actual: value, status: "PASS", severity: "" });
  });

  it("STATE-01 Candidate A state is removed when Candidate B logs in", async () => {
    const candidateBId = "00000000-0000-4000-8000-000000000002";
    localStorage.setItem("fipilot_auth_user", JSON.stringify({ id: "00000000-0000-4000-8000-000000000001", name: "Candidate A", email: "a@example.test" }));
    localStorage.setItem("fipilot_client_id", "00000000-0000-4000-8000-000000000001");
    localStorage.setItem("resume_analysis", JSON.stringify({ filename: "candidate-a.pdf", profile: { skills: ["Kafka"] } }));
    saveInterviewSetup(setup("session-a", "Backend Developer", "00000000-0000-4000-8000-000000000001"));
    saveInterviewTurn("session-a", question, "candidate a answer");
    vi.stubGlobal("fetch", vi.fn(async () => jsonResponse({ id: candidateBId, name: "Candidate B", email: "b@example.test" })));
    await loginUser("b@example.test", "password123");
    const candidateBState = {
      clientId: localStorage.getItem("fipilot_client_id"),
      resume: loadResumeAnalysis(),
      setupA: loadInterviewSetup("session-a"),
      turnsA: loadInterviewTurns("session-a"),
    };
    expect(candidateBState).toEqual({ clientId: candidateBId, resume: null, setupA: null, turnsA: [] });
    record({ test_id: "STATE-01", agent: "loginUser", scenario: "Candidate A then Candidate B", expected: "Candidate B receives its own client identity and no A resume/interview state", actual: candidateBState, status: "PASS", severity: "CRITICAL" });
    clearResumeAnalysis();
  });
});

afterAll(() => {
  const output = resolve(process.cwd(), "../evaluation/agent_robustness/frontend_results.json");
  mkdirSync(dirname(output), { recursive: true });
  const statuses: Status[] = ["PASS", "FAIL", "PARTIAL", "BLOCKED", "NOT TESTED", "NOT EVALUATED"];
  const summary = Object.fromEntries(statuses.map((status) => [status, results.filter((result) => result.status === status).length]));
  writeFileSync(output, JSON.stringify({ summary, results }, null, 2), "utf8");
});

import re

file_path = "../frontend/src/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/shared/interviewApi.ts"

with open(file_path, "r") as f:
    content = f.read()

new_func = """export async function requestNextInterviewQuestion(
  currentQuestion: InterviewQuestion,
  answer: string,
  followUpCount: number,
  usedProjectNames: string[],
) {
  const setup = loadInterviewSetup();
  if (setup === null) throw new Error("Interview setup is missing");
  
  // Try to load session state from sessionStorage (saved during prepare/start or previous turn)
  let sessionStateStr = sessionStorage.getItem(`session_state:${setup.sessionId}`);
  let sessionState = sessionStateStr ? JSON.parse(sessionStateStr) : {
      session_id: setup.sessionId,
      status: "in_progress",
      current_round_id: 1,
      turn_count: 1,
      follow_up_count: followUpCount
  };
  
  // Map currentQuestion back to QuestionGenerationResult for backend
  const v2CurrentQuestion = {
    question_text: currentQuestion.question,
    expected_key_points: currentQuestion.rubric?.critical_points || []
  };

  const response = await fetch("/api/v2/interview/next", {
    method: "POST",
    headers: { "content-type": "application/json", "X-User-ID": setup.clientId },
    body: JSON.stringify({
      session_id: setup.sessionId,
      session_state: sessionState,
      current_question: v2CurrentQuestion,
      answer: answer,
      follow_up_count: followUpCount,
    }),
  });
  
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(body?.detail ?? `Next question failed (HTTP ${response.status})`);
  }
  
  const data = await response.json();
  
  // Save new session state
  sessionStorage.setItem(`session_state:${setup.sessionId}`, JSON.stringify(data.session_state));
  
  // Map Evaluator Result to AnswerEvaluation for frontend UI
  const missingPoints = data.evaluation.evaluations.filter((e: any) => e.status !== "MET").map((e: any) => e.key_point);
  const matchedPoints = data.evaluation.evaluations.filter((e: any) => e.status === "MET").map((e: any) => e.key_point);
  
  const decisionDecision = {
    score: matchedPoints.length * 10,
    status: missingPoints.length === 0 ? "MET" : (matchedPoints.length > 0 ? "PARTIALLY_MET" : "NOT_MET"),
    evidence_quote: data.evaluation.evaluations[0]?.evidence || "",
    justification: data.evaluation.overall_assessment,
    should_follow_up: data.decision === "FOLLOW_UP",
    next_direction: data.decision,
    matched_points: matchedPoints,
    missing_points: missingPoints,
    technical_errors: []
  };
  
  let nextQuestion = null;
  if (data.question) {
    nextQuestion = {
      company: "V2 Session",
      question: data.question.question_text,
      project: "V2 Generated",
      project_context: {},
      rubric: {
        evaluation_goal: "Technical Evaluation",
        critical_points: data.question.expected_key_points,
        met: "Candidate met all key points",
        partially_met: "Candidate met some key points",
        not_met: "Candidate failed to mention key points"
      },
      topic: data.round_info?.topic || "Follow Up"
    };
  }

  return {
    decision: decisionDecision,
    follow_up_count: data.session_state.follow_up_count,
    question: nextQuestion || currentQuestion // Fallback if interview ended
  };
}"""

content = re.sub(r'export async function requestNextInterviewQuestion\([\s\S]*?return response\.json\(\) as Promise<NextInterviewQuestionResult>;\n\}', new_func, content)

with open(file_path, "w") as f:
    f.write(content)

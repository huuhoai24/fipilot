import re

file_path = "../frontend/src/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/shared/interviewApi.ts"

with open(file_path, "r") as f:
    content = f.read()

new_func = """async function requestInterviewQuestions(setup: InterviewSetup) {
  // 1. V2 Prepare Interview
  const prepareResponse = await fetch("/api/v2/interview/prepare", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      candidate_id: setup.resumeId,
      config: {
        role: setup.role,
        level: setup.level,
        duration_minutes: 30
      }
    }),
  });
  
  if (!prepareResponse.ok) {
    const body = (await prepareResponse.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(body?.detail ?? `Prepare failed (HTTP ${prepareResponse.status})`);
  }
  
  const prepareData = await prepareResponse.json();
  const sessionId = prepareData.session_id;
  
  // Save the new session ID so subsequent turns use it
  setup.sessionId = sessionId;
  saveInterviewSetup(setup);
  
  // 2. V2 Start Interview
  const startResponse = await fetch("/api/v2/interview/start", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId
    }),
  });
  
  if (!startResponse.ok) {
    const body = (await startResponse.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(body?.detail ?? `Start failed (HTTP ${startResponse.status})`);
  }
  
  const startData = await startResponse.json();
  
  // 3. Map V2 response back to V1 InterviewQuestion format for the Frontend
  return {
    questions: [
      {
        company: "V2 Session",
        question: startData.question.question_text,
        project: "V2 Generated",
        project_context: {},
        rubric: {
          evaluation_goal: "Technical Evaluation",
          critical_points: startData.question.expected_key_points,
          met: "Candidate met all key points",
          partially_met: "Candidate met some key points",
          not_met: "Candidate failed to mention key points"
        },
        topic: startData.round_info.topic
      }
    ]
  };
}"""

content = re.sub(r'async function requestInterviewQuestions\(setup: InterviewSetup\) \{[\s\S]*?return response\.json\(\) as Promise<InterviewQuestionResult>;\n\}', new_func, content)

with open(file_path, "w") as f:
    f.write(content)

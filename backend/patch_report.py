import re

file_path = "../frontend/src/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/shared/interviewApi.ts"

with open(file_path, "r") as f:
    content = f.read()

# Update createInterviewReport function
old_func = """export async function createInterviewReport(sessionId: string) {
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
  });"""

new_func = """export async function createInterviewReport(sessionId: string) {
  const setup = loadInterviewSetup();
  if (setup === null) throw new Error("Interview setup is missing");
  const response = await fetch("/api/v2/interview/report", {
    method: "POST",
    headers: { "content-type": "application/json", "X-User-ID": setup.clientId },
    body: JSON.stringify({
      session_id: sessionId,
    }),
  });"""

content = content.replace(old_func, new_func)

with open(file_path, "w") as f:
    f.write(content)

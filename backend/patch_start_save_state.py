import re

file_path = "../frontend/src/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/shared/interviewApi.ts"
with open(file_path, "r") as f:
    content = f.read()

# Replace the save
old_save = """  const startData = await startResponse.json();
  
  // 3. Map V2 response back to V1 InterviewQuestion format for the Frontend"""

new_save = """  const startData = await startResponse.json();
  
  sessionStorage.setItem(`session_state:${setup.sessionId}`, JSON.stringify(startData.session_state));
  
  // 3. Map V2 response back to V1 InterviewQuestion format for the Frontend"""

content = content.replace(old_save, new_save)
with open(file_path, "w") as f:
    f.write(content)

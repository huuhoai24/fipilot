import re

file_path = "../frontend/src/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/shared/interviewApi.ts"

with open(file_path, "r") as f:
    content = f.read()

# Update the prepare request payload
old_payload = """    body: JSON.stringify({
      candidate_id: setup.resumeId,
      config: {
        role: setup.role,
        level: setup.level,
        duration_minutes: 30
      }
    }),"""

new_payload = """    body: JSON.stringify({
      candidate_id: setup.resumeId,
      custom_description: setup.customDescription,
      config: {
        role: setup.role,
        level: setup.level,
        duration_minutes: 30
      }
    }),"""

content = content.replace(old_payload, new_payload)

with open(file_path, "w") as f:
    f.write(content)

import re

file_path = "../frontend/src/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/shared/interviewApi.ts"
with open(file_path, "r") as f:
    content = f.read()

# Replace the prepare fetch headers
old_prep = """  const prepareResponse = await fetch("/api/v2/interview/prepare", {
    method: "POST",
    headers: { "content-type": "application/json" },"""

new_prep = """  const prepareResponse = await fetch("/api/v2/interview/prepare", {
    method: "POST",
    headers: { "content-type": "application/json", "X-User-ID": setup.clientId },"""
content = content.replace(old_prep, new_prep)

# Replace the start fetch headers
old_start = """  const startResponse = await fetch("/api/v2/interview/start", {
    method: "POST",
    headers: { "content-type": "application/json" },"""

new_start = """  const startResponse = await fetch("/api/v2/interview/start", {
    method: "POST",
    headers: { "content-type": "application/json", "X-User-ID": setup.clientId },"""
content = content.replace(old_start, new_start)

with open(file_path, "w") as f:
    f.write(content)

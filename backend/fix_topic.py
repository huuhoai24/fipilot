import re
file_path = "gateway/api/interview.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace('topic = turn.question.get("topic") if turn.question else "N/A"', 'topic = turn.question.get("topic") or "Technical Evaluation" if turn.question else "Technical Evaluation"')
with open(file_path, "w") as f:
    f.write(content)

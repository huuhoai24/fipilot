import json

notebook_path = '/home/hoai/user/resource/fipilot/backend/notebooks/04_pipeline_poc.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "def evaluate_answer(question: str, expected_points: List[str], candidate_answer: str) -> AnswerEvaluationResult:" in source:
            new_source = source.replace(
                "Return ONLY a valid JSON object matching the requested schema.",
                """Return ONLY a valid JSON object matching exactly this schema:
    {
      "evaluations": [
        {
          "key_point": "string (the expected key point)",
          "status": "MET" | "PARTIAL" | "MISSING",
          "evidence": "string (direct quote) or null",
          "reasoning": "string (why you gave this status)"
        }
      ],
      "overall_assessment": "string (short summary)"
    }
    Do NOT return markdown formatting."""
            )
            
            lines = [line + '\n' for line in new_source.split('\n')]
            if lines:
                lines[-1] = lines[-1][:-1]
            cell['source'] = lines
            break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated to fix JSON schema.")

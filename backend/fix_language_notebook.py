import json

notebook_path = '/home/hoai/user/resource/fipilot/backend/notebooks/04_pipeline_poc.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "def generate_first_question(profile: CandidateProfile, first_round: InterviewRound) -> QuestionGenerationResult:" in source:
            new_source = source.replace(
                "4. Base the context of the question on the candidate's actual experience if possible.",
                "4. Base the context of the question on the candidate's actual experience if possible.\\n    5. The question_text and expected_key_points MUST be written in VIETNAMESE."
            )
            # Reconstruct the source array
            lines = [line + '\n' for line in new_source.split('\n')]
            if lines:
                lines[-1] = lines[-1][:-1]
            cell['source'] = lines
            break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated to require Vietnamese language.")

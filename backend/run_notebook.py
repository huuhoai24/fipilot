import json

with open('/home/hoai/user/resource/fipilot/backend/notebooks/04_pipeline_poc.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

code = ""
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        code += "".join(cell['source']) + "\n\n"

with open('run_poc.py', 'w', encoding='utf-8') as f:
    f.write(code)

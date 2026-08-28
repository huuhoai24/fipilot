import json

notebook_path = '/home/hoai/user/resource/fipilot/backend/notebooks/04_pipeline_poc.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        
        # Sửa trong Cell 9
        if "status_color = \"✅\" if ev.status == \"MET\" else (\"⚠️\" if ev.status == \"PARTIAL\" else \"❌\")" in source:
            new_source = source.replace(
                "status_color = \"✅\" if ev.status == \"MET\" else (\"⚠️\" if ev.status == \"PARTIAL\" else \"❌\")\n        print(f\"{status_color} [{ev.status}] Tiêu chí: {ev.key_point}\")",
                "status_map = {\"MET\": \"[3 - Met]\", \"PARTIAL\": \"[2 - Partially Met]\", \"MISSING\": \"[1 - Not Met]\"}\n        status_display = status_map.get(ev.status, \"[0 - Not Assessed]\")\n        print(f\"{status_display} Tiêu chí: {ev.key_point}\")"
            )
            # Dành cho Cell 10
            new_source = new_source.replace(
                "status_color = \"✅\" if ev.status == \"MET\" else (\"⚠️\" if ev.status == \"PARTIAL\" else \"❌\")\n        print(f\"  {idx}. {ev.key_point} {status_color}\")",
                "status_map = {\"MET\": \"[3 - Met]\", \"PARTIAL\": \"[2 - Partially Met]\", \"MISSING\": \"[1 - Not Met]\"}\n        status_display = status_map.get(ev.status, \"[0 - Not Assessed]\")\n        print(f\"  {idx}. {ev.key_point} {status_display}\")"
            )
            
            lines = [line + '\n' for line in new_source.split('\n')]
            if lines:
                lines[-1] = lines[-1][:-1]
            cell['source'] = lines

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated to use Chakra scoring labels instead of emojis.")

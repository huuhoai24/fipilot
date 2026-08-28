import json

notebook_path = '/home/hoai/user/resource/fipilot/backend/notebooks/04_pipeline_poc.ipynb'
knowledge_path = '/home/hoai/user/resource/fipilot/backend/Knowledge/Levels/AI_Engineer/Middle.md'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open(knowledge_path, 'r', encoding='utf-8') as f:
    knowledge_content = f.read()

# Escape quotes and curly braces for python format string injection
safe_knowledge = knowledge_content.replace("{", "{{").replace("}", "}}").replace('"', '\\"')

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        
        # Inject into generate_followup_question
        if "def generate_followup_question(" in source:
            new_source = source.replace(
                "You are an adaptive AI interviewer.",
                f"You are an adaptive AI interviewer for a Middle-level AI Engineer.\\n    Here is the Knowledge Base and Evaluation Focus for this level:\\n    \\n    {safe_knowledge}\\n\\n    You must enforce these standards."
            )
            
            lines = [line + '\n' for line in new_source.split('\n')]
            if lines:
                lines[-1] = lines[-1][:-1]
            cell['source'] = lines
            
        # Update mock answer to trigger the Middle level evaluation
        if "mock_candidate_answer =" in source:
            new_source = source.replace(
                "mock_candidate_answer = \"Tôi nghĩ ngôn ngữ này khá dễ dùng và có nhiều thư viện hỗ trợ. Trong các dự án của tôi, tôi thường dùng nó để xử lý dữ liệu và viết vài script tự động hoá cơ bản.\"",
                "mock_candidate_answer = \"Trong dự án phân tích hóa đơn, tôi đã sử dụng YOLOv12 thay vì YOLOv8 cũ vì kiến trúc mới của nó cho kết quả nhận diện Layout nhanh hơn hẳn.\""
            )
            lines = [line + '\n' for line in new_source.split('\n')]
            if lines:
                lines[-1] = lines[-1][:-1]
            cell['source'] = lines

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated with RAG Knowledge Base injection.")

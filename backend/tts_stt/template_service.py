import os
import re

class TemplateService:
    def __init__(self, templates_dir: str = "../Template"):
        # Đường dẫn tới folder Template
        self.templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), templates_dir))

    def get_all_templates(self):
        templates = []
        if not os.path.exists(self.templates_dir):
            print(f"Template directory not found: {self.templates_dir}")
            return templates

        for filename in os.listdir(self.templates_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(self.templates_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Lấy Title (dòng # đầu tiên)
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = title_match.group(1).strip() if title_match else filename.replace('.md', '')
                    
                    # Đếm số lượng câu hỏi (ví dụ: đếm các block bắt đầu bằng "Câu hỏi:" hoặc "- **Câu")
                    # Một cách đơn giản hơn là giả định theo spec mock (vì chưa biết format thực tế của md)
                    # Hoặc đếm "## Câu"
                    questions = re.findall(r'(?:^##\s+Câu|^Câu hỏi:|\-\s+\*\*Câu)', content, re.MULTILINE)
                    question_count = len(questions) if len(questions) > 0 else 10
                    
                    templates.append({
                        "template_id": filename,
                        "title": title,
                        "question_count": question_count,
                        "role_target": filename.split('_')[0].replace(' ', ''), # Ví dụ: AI_Engineer_lv1.md -> AI
                    })
                except Exception as e:
                    print(f"Error reading template {filename}: {e}")
                    
        return templates

    def match_templates(self, role_fit: str, inferred_level: int):
        all_templates = self.get_all_templates()
        
        # Sắp xếp các template dựa trên độ phù hợp với role_fit và level
        # role_fit là chuỗi trả về từ LLM (e.g. "AI Engineer", "Backend Developer")
        matched = []
        role_keyword = role_fit.split(' ')[0].lower() # e.g., 'ai', 'backend', 'data'
        
        for t in all_templates:
            score = 0.5 # Điểm cơ bản
            filename = t["template_id"].lower()
            
            # Match role
            if role_keyword in filename:
                score += 0.3
            
            # Match level
            level_str = f"lv{inferred_level}"
            if level_str in filename:
                score += 0.15
                
            matched.append({
                "template_id": t["template_id"],
                "title": t["title"],
                "score": score,
                "question_count": t["question_count"],
                "difficulty_mix": {"easy": 4, "medium": 4, "hard": 2}, # Mock
                "duration_minutes": 45 # Mock
            })
            
        # Sort by score descending
        matched.sort(key=lambda x: x["score"], reverse=True)
        return matched[:5]

    def get_template_questions(self, template_id: str):
        if not template_id:
            return []
        if not template_id.endswith(".md"):
            template_id += ".md"
            
        file_path = os.path.join(self.templates_dir, template_id)
        if not os.path.exists(file_path):
            print(f"Template file not found: {file_path}")
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            blocks = re.split(r'^###\s+Câu\s+\d+', content, flags=re.MULTILINE)
            questions = []
            for i, block in enumerate(blocks[1:], start=1):
                difficulty_match = re.search(r'\*\s*\*\*Độ khó:\*\*\s*(.+)$', block, re.MULTILINE)
                question_match = re.search(r'\*\s*\*\*Câu hỏi:\*\*\s*(.+)$', block, re.MULTILINE)
                
                difficulty = difficulty_match.group(1).strip() if difficulty_match else ""
                question_text = question_match.group(1).strip() if question_match else ""
                
                answer_text = ""
                ans_pos = block.find("**Đáp án mẫu:**")
                if ans_pos != -1:
                    ans_content = block[ans_pos + 15:].strip()
                    if ans_content.startswith(':'):
                        ans_content = ans_content[1:].strip()
                    ans_content = re.sub(r'\n---\n.*', '', ans_content, flags=re.DOTALL)
                    answer_text = ans_content.strip()
                
                if question_text:
                    questions.append({
                        "id": i,
                        "difficulty": difficulty,
                        "question": question_text,
                        "answer": answer_text
                    })
            return questions
        except Exception as e:
            print(f"Error parsing template questions: {e}")
            return []

template_service = TemplateService()

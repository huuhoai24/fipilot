import os
import re


class TemplateService:
    def __init__(self, templates_dir: str = "../Template"):
        self.templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), templates_dir))

    def get_all_templates(self):
        templates = []
        if not os.path.exists(self.templates_dir):
            print(f"Template directory not found: {self.templates_dir}")
            return templates

        for filename in os.listdir(self.templates_dir):
            if not filename.endswith(".md"):
                continue

            file_path = os.path.join(self.templates_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else filename.replace(".md", "")
                questions = self.get_template_questions(filename)

                templates.append(
                    {
                        "template_id": filename,
                        "title": title,
                        "question_count": len(questions) or 10,
                        "role_target": self._role_from_filename(filename),
                        "level": self._level_from_filename(filename),
                        "difficulty_mix": self._difficulty_mix(questions),
                        "tags": self._extract_tags(content, filename),
                    }
                )
            except Exception as e:
                print(f"Error reading template {filename}: {e}")

        return templates

    def match_templates(self, role_fit: str, inferred_level: int, skills=None, target_role: str = None):
        all_templates = self.get_all_templates()
        role_query = self._normalize_text(target_role or role_fit or "")
        skill_terms = {self._normalize_text(s) for s in (skills or []) if s}

        matched = []
        for template in all_templates:
            role_score = self._role_similarity(role_query, template["role_target"])
            level_score = self._level_similarity(inferred_level, template.get("level"))
            tag_score = self._tag_similarity(skill_terms, template.get("tags", []))
            score = (0.50 * role_score) + (0.30 * level_score) + (0.20 * tag_score)

            matched.append(
                {
                    "template_id": template["template_id"],
                    "title": template["title"],
                    "score": round(max(0.0, min(score, 1.0)), 3),
                    "question_count": template["question_count"],
                    "difficulty_mix": template["difficulty_mix"],
                    "duration_minutes": max(20, template["question_count"] * 4),
                    "matched_role": template["role_target"],
                    "matched_level": template.get("level"),
                    "matched_skills": sorted(skill_terms.intersection(template.get("tags", [])))[:8],
                }
            )

        matched.sort(key=lambda item: item["score"], reverse=True)
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
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            blocks = re.split(r"^###\s+C[^\n]*\d+", content, flags=re.MULTILINE | re.IGNORECASE)
            questions = []
            for index, block in enumerate(blocks[1:], start=1):
                difficulty = self._find_markdown_field(block, ["Do kho", "Difficulty", "khó", "kho"])
                question_text = self._find_markdown_field(block, ["Cau hoi", "Question", "hỏi", "hoi"])
                answer_text = self._find_answer(block)

                if question_text:
                    questions.append(
                        {
                            "id": index,
                            "difficulty": difficulty,
                            "question": question_text,
                            "answer": answer_text,
                            "tags": sorted(self._extract_tags(f"{question_text}\n{answer_text}", template_id)),
                        }
                    )
            return questions
        except Exception as e:
            print(f"Error parsing template questions: {e}")
            return []

    def _find_markdown_field(self, block: str, labels):
        for line in block.splitlines():
            normalized = self._strip_accents(line).lower()
            if not any(label.lower() in normalized for label in labels):
                continue
            if ":" in line:
                return line.split(":", 1)[1].replace("**", "").strip()
        return ""

    def _find_answer(self, block: str):
        lines = block.splitlines()
        answer_lines = []
        collecting = False
        for line in lines:
            normalized = self._strip_accents(line).lower()
            if "dap an" in normalized or "sample answer" in normalized:
                collecting = True
                answer_lines.append(line.split(":", 1)[1].strip() if ":" in line else "")
                continue
            if collecting:
                if line.startswith("### ") or line.strip() == "---":
                    break
                answer_lines.append(line)
        return "\n".join(answer_lines).replace("**", "").strip()

    def _role_from_filename(self, filename: str) -> str:
        base = filename.rsplit(".", 1)[0]
        base = re.sub(r"_lv\d+$", "", base, flags=re.IGNORECASE)
        return base.replace("_", " ").strip()

    def _level_from_filename(self, filename: str):
        match = re.search(r"lv(\d+)", filename, re.IGNORECASE)
        return int(match.group(1)) if match else None

    def _normalize_text(self, text: str) -> str:
        normalized = re.sub(r"[^a-z0-9]+", " ", self._strip_accents(str(text)).lower()).strip()
        replacements = {
            "artificial intelligence": "ai",
            "machine learning": "ml",
            "quality assurance": "qa",
            "full stack": "fullstack",
            "front end": "frontend",
            "back end": "backend",
        }
        for source, target in replacements.items():
            normalized = re.sub(rf"\b{re.escape(source)}\b", target, normalized)
        return re.sub(r"\s+", " ", normalized).strip()

    def _strip_accents(self, text: str) -> str:
        import unicodedata

        stripped = "".join(
            char for char in unicodedata.normalize("NFKD", text) if not unicodedata.combining(char)
        )
        return stripped.replace("đ", "d").replace("Đ", "D")

    def _tokenize(self, text: str):
        return set(self._normalize_text(text).split())

    def _role_similarity(self, query: str, template_role: str) -> float:
        q_tokens = self._tokenize(query)
        t_tokens = self._tokenize(template_role)
        if not q_tokens or not t_tokens:
            return 0.4

        normalized_template = self._normalize_text(template_role)
        if normalized_template in query or query in normalized_template:
            return 1.0

        overlap = len(q_tokens & t_tokens) / max(len(q_tokens | t_tokens), 1)
        return max(0.2, overlap)

    def _level_similarity(self, inferred_level, template_level) -> float:
        try:
            inferred = int(inferred_level)
            template = int(template_level)
        except (TypeError, ValueError):
            return 0.5

        distance = abs(inferred - template)
        if distance == 0:
            return 1.0
        if distance == 1:
            return 0.65
        return 0.25

    def _tag_similarity(self, skill_terms, template_tags) -> float:
        if not skill_terms:
            return 0.5
        tags = set(template_tags or [])
        if not tags:
            return 0.3
        return min(1.0, len(skill_terms & tags) / max(min(len(skill_terms), 8), 1))

    def _extract_tags(self, content: str, filename: str):
        seed = self._tokenize(self._role_from_filename(filename))
        common = {
            "python",
            "java",
            "javascript",
            "typescript",
            "react",
            "node",
            "sql",
            "database",
            "api",
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "gcp",
            "linux",
            "git",
            "oop",
            "solid",
            "testing",
            "etl",
            "spark",
            "airflow",
            "machine",
            "learning",
            "llm",
            "rag",
            "nlp",
            "data",
            "backend",
            "frontend",
            "devops",
            "cloud",
            "security",
            "analytics",
        }
        return sorted((self._tokenize(content) & common) | seed)

    def _difficulty_mix(self, questions):
        mix = {"easy": 0, "medium": 0, "hard": 0}
        for question in questions:
            difficulty = self._normalize_text(question.get("difficulty", ""))
            if "kho" in difficulty or "hard" in difficulty:
                mix["hard"] += 1
            elif "trung" in difficulty or "medium" in difficulty:
                mix["medium"] += 1
            else:
                mix["easy"] += 1
        return mix


template_service = TemplateService()

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

        for file_path in self._iter_folder_template_files():
            template_id = self._template_id_from_path(file_path)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else template_id.replace(".md", "")
                questions = self.get_template_questions(template_id)

                templates.append(
                    {
                        "template_id": template_id,
                        "title": title,
                        "question_count": len(questions) or 10,
                        "role_target": self._role_from_template_id(template_id),
                        "level": self._level_from_template_id(template_id),
                        "difficulty_mix": self._difficulty_mix(questions),
                        "tags": self._extract_tags(content, template_id),
                    }
                )
            except Exception as e:
                print(f"Error reading template {template_id}: {e}")

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
        deduped = []
        seen_groups = set()
        for item in matched:
            group_key = (self._normalize_text(item.get("matched_role", "")), item.get("matched_level"))
            if group_key in seen_groups:
                continue
            seen_groups.add(group_key)
            deduped.append(item)
            if len(deduped) >= 5:
                break
        return deduped

    def get_template_questions(self, template_id: str):
        if not template_id:
            return []
        if not template_id.endswith(".md"):
            template_id += ".md"

        file_path = os.path.abspath(os.path.join(self.templates_dir, template_id.replace("\\", os.sep).replace("/", os.sep)))
        if not self._is_inside_templates_dir(file_path):
            print(f"Template path outside directory rejected: {template_id}")
            return []
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

    def _iter_folder_template_files(self):
        for root, _dirs, files in os.walk(self.templates_dir):
            if os.path.abspath(root) == self.templates_dir:
                continue
            for filename in files:
                if filename.lower().endswith(".md") and filename.lower() != "readme.md":
                    yield os.path.join(root, filename)

    def _template_id_from_path(self, file_path: str) -> str:
        return os.path.relpath(file_path, self.templates_dir).replace(os.sep, "/")

    def _is_inside_templates_dir(self, file_path: str) -> bool:
        try:
            return os.path.commonpath([self.templates_dir, file_path]) == self.templates_dir
        except ValueError:
            return False

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
            if "dap an" in normalized or "sample answer" in normalized or "expected_key_points" in normalized:
                collecting = True
                answer_lines.append(line.split(":", 1)[1].strip() if ":" in line else "")
                continue
            if collecting:
                if line.startswith("### ") or line.strip() == "---":
                    break
                answer_lines.append(line)
        answer = "\n".join(answer_lines).replace("**", "").strip()
        if answer:
            return self._compact_expected_key_points(answer)
        return ""

    def _compact_expected_key_points(self, text: str):
        lines = []
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            normalized = self._strip_accents(line).lower()
            if normalized.startswith("id:") or normalized.startswith("- id:") or normalized.startswith("keypoint_weight:"):
                continue
            if normalized.startswith("content:"):
                lines.append("- " + line.split(":", 1)[1].strip())
                continue
            if normalized.startswith("description:"):
                lines.append("  " + line.split(":", 1)[1].strip())
                continue
            lines.append(line)
        return "\n".join(lines).strip()

    def _role_from_filename(self, filename: str) -> str:
        base = os.path.basename(filename).rsplit(".", 1)[0]
        base = re.sub(r"_lv\d+$", "", base, flags=re.IGNORECASE)
        return base.replace("_", " ").strip()

    def _level_from_filename(self, filename: str):
        match = re.search(r"(?:lv|level[_/-]?)(\d+)", filename, re.IGNORECASE)
        return int(match.group(1)) if match else None

    def _role_from_template_id(self, template_id: str) -> str:
        parts = template_id.replace("\\", "/").split("/")
        if len(parts) > 1:
            return parts[0].replace("_", " ").strip()
        return self._role_from_filename(template_id)

    def _level_from_template_id(self, template_id: str):
        return self._level_from_filename(template_id)

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

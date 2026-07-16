import calendar
import math
import re
from datetime import date
from difflib import SequenceMatcher

import docx
import pypdf


CURRENT_YEAR = date.today().year


SKILL_TAXONOMY = {
    "Python": ["python", "py"],
    "Java": ["java", "spring boot", "spring"],
    "JavaScript": ["javascript", "js", "ecmascript"],
    "TypeScript": ["typescript", "ts"],
    "React": ["react", "reactjs", "react.js", "next.js", "nextjs"],
    "Vue": ["vue", "vue.js", "nuxt"],
    "Angular": ["angular"],
    "Node.js": ["node.js", "nodejs", "node", "express", "nestjs"],
    "C#": ["c#", ".net", "asp.net"],
    "Go": ["golang", "go developer"],
    "PHP": ["php", "laravel"],
    "SQL": ["sql", "mysql", "postgresql", "postgres", "mssql", "oracle"],
    "NoSQL": ["mongodb", "mongo", "redis", "cassandra", "dynamodb"],
    "API": ["api", "rest", "restful", "graphql", "grpc"],
    "Docker": ["docker", "container"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud"],
    "Linux": ["linux", "ubuntu", "bash", "shell"],
    "Git": ["git", "github", "gitlab", "bitbucket"],
    "CI/CD": ["ci/cd", "cicd", "jenkins", "github actions", "gitlab ci"],
    "Testing": ["testing", "unit test", "integration test", "pytest", "jest", "selenium", "cypress"],
    "QA Automation": ["qa automation", "automation test", "automated testing", "selenium", "cypress", "playwright"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3", "sass", "scss", "tailwind", "bootstrap"],
    "Machine Learning": ["machine learning", "ml", "scikit-learn", "sklearn"],
    "Deep Learning": ["deep learning", "neural network", "tensorflow", "pytorch", "keras"],
    "LLM": ["llm", "large language model", "openai", "ollama", "langchain", "llamaindex"],
    "RAG": ["rag", "retrieval augmented generation", "vector database", "embedding", "faiss", "qdrant", "pinecone"],
    "NLP": ["nlp", "natural language processing", "spacy", "nltk"],
    "MLOps": ["mlops", "model serving", "mlflow", "kubeflow", "airflow"],
    "Data Engineering": ["data engineering", "etl", "elt", "data pipeline", "data warehouse"],
    "Spark": ["spark", "pyspark", "databricks"],
    "Airflow": ["airflow", "dag"],
    "Kafka": ["kafka", "streaming"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Business Analysis": ["business analyst", "business analysis", "brd", "user story", "use case", "bpmn"],
    "Security": ["security", "cybersecurity", "penetration testing", "pentest", "owasp", "siem"],
}


ROLE_PROFILES = {
    "Backend Developer": {
        "title": ["backend", "back-end", "server side", "api developer"],
        "skills": ["Python", "Java", "Node.js", "C#", "Go", "PHP", "SQL", "NoSQL", "API", "Docker", "Git"],
    },
    "Frontend Developer": {
        "title": ["frontend", "front-end", "web ui", "ui developer"],
        "skills": ["JavaScript", "TypeScript", "React", "Vue", "Angular", "HTML", "CSS", "Testing", "Git"],
    },
    "Fullstack Developer": {
        "title": ["fullstack", "full-stack", "full stack"],
        "skills": ["JavaScript", "TypeScript", "React", "Node.js", "Python", "Java", "SQL", "API", "Docker"],
    },
    "Web Developer": {
        "title": ["web developer", "website developer"],
        "skills": ["JavaScript", "TypeScript", "React", "Vue", "HTML", "CSS", "Node.js", "PHP", "SQL"],
    },
    "Software Engineer": {
        "title": ["software engineer", "software developer", "developer", "programmer"],
        "skills": ["Python", "Java", "JavaScript", "TypeScript", "SQL", "API", "Git", "Testing", "Docker"],
    },
    "AI Engineer": {
        "title": ["ai engineer", "machine learning engineer", "ml engineer", "nlp engineer"],
        "skills": ["Python", "Machine Learning", "Deep Learning", "LLM", "RAG", "NLP", "MLOps", "SQL"],
    },
    "Data Scientist": {
        "title": ["data scientist", "machine learning scientist"],
        "skills": ["Python", "SQL", "Machine Learning", "Deep Learning", "NLP", "Power BI", "Tableau"],
    },
    "Data Engineer": {
        "title": ["data engineer", "etl developer", "big data engineer"],
        "skills": ["Python", "SQL", "Data Engineering", "Spark", "Airflow", "Kafka", "AWS", "GCP", "Azure"],
    },
    "DevOps Engineer": {
        "title": ["devops", "site reliability", "sre", "cloud engineer"],
        "skills": ["Docker", "Kubernetes", "AWS", "Azure", "GCP", "Linux", "CI/CD", "Git"],
    },
    "Cloud Engineer": {
        "title": ["cloud engineer", "cloud architect"],
        "skills": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Linux", "CI/CD"],
    },
    "Tester": {
        "title": ["tester", "qa", "quality assurance", "test engineer"],
        "skills": ["Testing", "QA Automation", "SQL", "API", "Selenium", "Git"],
    },
    "Business Analyst": {
        "title": ["business analyst", "product analyst"],
        "skills": ["Business Analysis", "SQL", "Power BI", "Tableau", "API"],
    },
    "Cybersecurity Analyst": {
        "title": ["cybersecurity", "security analyst", "soc analyst"],
        "skills": ["Security", "Linux", "Python", "SQL", "AWS"],
    },
}


SECTION_ALIASES = {
    "summary": ["summary", "professional summary", "profile", "objective", "about me", "career objective"],
    "skills": ["skills", "technical skills", "technologies", "tools", "tech stack", "competencies", "software"],
    "experience": [
        "experience",
        "work experience",
        "working experience",
        "working experience highlights",
        "professional experience",
        "employment",
        "work history",
    ],
    "projects": ["projects", "personal projects", "academic projects", "portfolio", "project and practice"],
    "education": [
        "education",
        "education certificate",
        "education and certificate",
        "educational background",
        "academic background",
        "qualification",
        "qualifications",
    ],
    "certifications": ["certifications", "certificates", "certificate and award", "licenses"],
    "hobbies": ["hobbies", "interests"],
}


TABLE_LABELS = {
    "project name",
    "duration",
    "position",
    "positions",
    "role",
    "title",
    "general information",
    "description",
    "project scope",
    "technology used",
    "technologies used",
    "team size",
    "customer",
    "client",
    "responsibilities",
}


ROLE_TITLE_TERMS = {
    "engineer",
    "developer",
    "analyst",
    "tester",
    "qa",
    "devops",
    "scientist",
    "architect",
    "manager",
    "lead",
    "specialist",
    "consultant",
    "administrator",
}


GENERIC_ROLE_ALIASES = {"developer", "engineer", "analyst", "tester", "programmer"}


MONTHS = {
    name.lower(): index for index, name in enumerate(calendar.month_name) if name
}
MONTHS.update({name.lower(): index for index, name in enumerate(calendar.month_abbr) if name})


class CVExtractor:
    def extract_text(self, file_path: str, filename: str) -> str:
        text = ""
        ext = filename.split(".")[-1].lower()
        try:
            if ext == "pdf":
                with open(file_path, "rb") as f:
                    reader = pypdf.PdfReader(f)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            elif ext in ["docx", "doc"]:
                document = docx.Document(file_path)
                for para in document.paragraphs:
                    if para.text.strip():
                        text += para.text + "\n"
                for table in document.tables:
                    for row in table.rows:
                        cells = self._dedupe_cells([cell.text.strip() for cell in row.cells if cell.text.strip()])
                        if cells:
                            text += " | ".join(cells) + "\n"
        except Exception as e:
            print(f"Error parsing CV: {e}")
        return self._normalize_whitespace(text)

    async def parse_cv(self, text: str) -> dict:
        return self.parse_cv_sync(text)

    def parse_cv_sync(self, text: str) -> dict:
        normalized_text = self._normalize_whitespace(text)
        sections = self._split_sections(normalized_text)
        skills = self._extract_skills(normalized_text, sections)
        recent_role = self._extract_recent_role(normalized_text, sections)
        years_experience = self._estimate_years_experience(normalized_text, sections)
        role_fit, role_confidence = self._infer_role(normalized_text, recent_role, skills)
        inferred_level = self._infer_level(years_experience, recent_role, normalized_text)

        confidence_parts = [
            0.2 if self._extract_candidate_name(normalized_text) != "Candidate" else 0.0,
            min(len(skills) / 8, 1.0) * 0.3,
            min(years_experience / 3, 1.0) * 0.2 if years_experience else 0.05,
            role_confidence * 0.3,
        ]

        return {
            "candidate_name": self._extract_candidate_name(normalized_text),
            "years_experience": years_experience,
            "skills": skills or ["Not Found"],
            "education": self._extract_education(sections),
            "recent_role": recent_role,
            "inferred_level": inferred_level,
            "role_fit": role_fit,
            "confidence": round(min(sum(confidence_parts), 0.98), 2),
            "extraction_method": "rule_based",
        }

    def _normalize_whitespace(self, text: str) -> str:
        text = text.replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _split_sections(self, text: str) -> dict:
        sections = {"raw": text}
        current = "header"
        sections[current] = []

        heading_map = {}
        for section, aliases in SECTION_ALIASES.items():
            for alias in aliases:
                heading_map[self._clean_heading(alias)] = section

        for raw_line in text.splitlines():
            line = raw_line.strip(" :-|").strip()
            if not line:
                continue
            cells = self._split_table_cells(line)
            if cells and self._clean_heading(cells[0]) == "project name":
                current = "projects"
                sections.setdefault(current, []).append(line)
                continue
            cleaned = self._clean_heading(line)
            if cleaned in heading_map or self._looks_like_heading(cleaned, heading_map):
                closest = cleaned if cleaned in heading_map else self._closest_heading(cleaned, heading_map)
                current = heading_map[closest]
                sections.setdefault(current, [])
                continue
            sections.setdefault(current, []).append(line)

        return {
            key: "\n".join(value) if isinstance(value, list) else value
            for key, value in sections.items()
        }

    def _clean_heading(self, text: str) -> str:
        text = self._strip_accents(text).lower()
        text = re.sub(r"[^a-z0-9 ]+", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def _looks_like_heading(self, cleaned: str, heading_map: dict) -> bool:
        if len(cleaned.split()) > 4:
            return False
        return any(SequenceMatcher(None, cleaned, heading).ratio() >= 0.88 for heading in heading_map)

    def _closest_heading(self, cleaned: str, heading_map: dict) -> str:
        return max(heading_map, key=lambda heading: SequenceMatcher(None, cleaned, heading).ratio())

    def _extract_candidate_name(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines()[:12] if line.strip()]
        for line in lines:
            if self._is_contact_line(line) or self._is_probably_title(line):
                continue
            if self._is_table_noise_line(line):
                continue
            line = re.sub(r"\s*[-|]\s*(resume|cv|curriculum vitae)\s*$", "", line, flags=re.I)
            cleaned = re.sub(r"[^A-Za-zÀ-ỹ .'-]", "", line).strip()
            words = cleaned.split()
            if 2 <= len(words) <= 5:
                return " ".join(word.capitalize() if word.isupper() else word for word in words)
        return "Candidate"

    def _is_contact_line(self, line: str) -> bool:
        return bool(re.search(r"@|https?://|linkedin|github|phone|mobile|\+?\d[\d\s().-]{7,}", line, re.I))

    def _is_probably_title(self, line: str) -> bool:
        normalized = self._clean_heading(line)
        return any(term in normalized.split() for term in ROLE_TITLE_TERMS) and len(normalized.split()) <= 7

    def _extract_skills(self, text: str, sections: dict) -> list:
        search_text = "\n".join(
            [
                sections.get("skills", ""),
                sections.get("summary", ""),
                sections.get("experience", ""),
                sections.get("projects", ""),
                text,
            ]
        ).lower()

        found = []
        for canonical, aliases in SKILL_TAXONOMY.items():
            for alias in aliases:
                pattern = r"(?<![a-z0-9])" + re.escape(alias.lower()) + r"(?![a-z0-9])"
                if re.search(pattern, search_text):
                    found.append(canonical)
                    break
        return sorted(set(found))

    def _extract_recent_role(self, text: str, sections: dict) -> str:
        experience = sections.get("experience", "")
        projects = sections.get("projects", "")
        role_source = "\n".join(part for part in [experience, projects] if part.strip()) or text
        candidates = []

        for line in role_source.splitlines()[:120]:
            candidate = self._role_from_position_row(line)
            if candidate:
                candidates.append(candidate)

        for line in role_source.splitlines()[:60]:
            if self._is_contact_line(line) or self._is_table_noise_line(line) or self._is_section_heading(line):
                continue
            for cell in self._split_table_cells(line):
                if self._looks_like_role_value(cell):
                    candidates.append(cell.strip(" -*•|"))

        if candidates:
            return self._clean_role_line(candidates[0])[:140]

        header_lines = [line.strip() for line in text.splitlines()[:10] if line.strip()]
        for line in header_lines:
            if self._is_probably_title(line) and not self._is_section_heading(line):
                return self._clean_role_line(line)[:140]
        return "Not Found"

    def _clean_role_line(self, line: str) -> str:
        return re.sub(r"^\s*(position|title|role|current role)\s*:\s*", "", line, flags=re.I).strip()

    def _role_from_position_row(self, line: str) -> str:
        cells = self._split_table_cells(line)
        if len(cells) < 2:
            return ""
        label = self._clean_heading(cells[0])
        if label not in {"position", "positions", "role", "title", "current role"}:
            return ""
        for cell in cells[1:]:
            if self._looks_like_role_value(cell):
                return cell.strip()
        return ""

    def _split_table_cells(self, line: str) -> list:
        cells = [cell.strip() for cell in line.split("|")] if "|" in line else [line.strip()]
        return self._dedupe_cells(cells)

    def _dedupe_cells(self, cells: list) -> list:
        deduped = []
        seen = set()
        for cell in cells:
            normalized = self._clean_heading(cell)
            if not normalized or normalized in seen:
                continue
            deduped.append(cell)
            seen.add(normalized)
        return deduped

    def _is_table_noise_line(self, line: str) -> bool:
        normalized = self._clean_heading(line)
        if not normalized:
            return True
        cells = [self._clean_heading(cell) for cell in self._split_table_cells(line)]
        if len(cells) >= 2 and cells[0] in TABLE_LABELS:
            return True
        label_hits = sum(1 for cell in cells if cell in TABLE_LABELS)
        return label_hits >= 2

    def _looks_like_role_value(self, text: str) -> bool:
        normalized = self._clean_heading(self._clean_role_line(text))
        words = normalized.split()
        if not words or len(words) > 8:
            return False
        if normalized in TABLE_LABELS:
            return False
        if any(term in words for term in ROLE_TITLE_TERMS):
            return True
        return any(
            re.search(rf"(?<![a-z0-9]){re.escape(self._clean_heading(title))}(?![a-z0-9])", normalized)
            for profile in ROLE_PROFILES.values()
            for title in profile["title"]
        )

    def _is_section_heading(self, line: str) -> bool:
        normalized = self._clean_heading(line)
        return any(normalized == self._clean_heading(alias) for aliases in SECTION_ALIASES.values() for alias in aliases)

    def _role_terms(self) -> set:
        terms = set()
        for profile in ROLE_PROFILES.values():
            for title in profile["title"]:
                terms.update(self._clean_heading(title).split())
        return terms | ROLE_TITLE_TERMS

    def _estimate_years_experience(self, text: str, sections: dict) -> float:
        explicit = self._extract_explicit_years(text)
        experience_text = "\n".join(
            part for part in [sections.get("experience", ""), sections.get("projects", "")] if part.strip()
        )
        ranges = self._extract_date_ranges(experience_text)
        months = self._merge_ranges_in_months(ranges)

        if months:
            range_years = round(months / 12, 1)
            return max(range_years, explicit or 0.0)
        if explicit:
            return explicit
        return 0.0

    def _extract_explicit_years(self, text: str) -> float:
        patterns = [
            r"(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)\s+(?:of\s+)?experience",
            r"experience\s*:?\s*(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)",
        ]
        values = []
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.I):
                values.append(float(match.group(1)))
        return max(values) if values else 0.0

    def _extract_date_ranges(self, text: str) -> list:
        date_token = (
            r"(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+)?"
            r"(?:20\d{2}|19\d{2})"
            r"|(?:0?[1-9]|1[0-2])[/.-](?:20\d{2}|19\d{2})"
        )
        range_pattern = re.compile(
            rf"({date_token})\s*(?:-|–|—|to|until)\s*((?:present|current|now)|{date_token})",
            re.I,
        )
        ranges = []
        for match in range_pattern.finditer(text):
            start = self._parse_date_token(match.group(1))
            end = self._parse_date_token(match.group(2), end=True)
            if start and end and start <= end:
                ranges.append((start, end))
        return ranges

    def _parse_date_token(self, token: str, end: bool = False):
        token = token.strip().lower().replace(".", "")
        if token in {"present", "current", "now"}:
            today = date.today()
            return today.year * 12 + today.month

        month_year = re.search(r"([a-z]+)\s+(19\d{2}|20\d{2})", token)
        if month_year:
            month = MONTHS.get(month_year.group(1)[:3], 1)
            return int(month_year.group(2)) * 12 + month

        numeric = re.search(r"(0?[1-9]|1[0-2])[/.-](19\d{2}|20\d{2})", token)
        if numeric:
            return int(numeric.group(2)) * 12 + int(numeric.group(1))

        year = re.search(r"(19\d{2}|20\d{2})", token)
        if year:
            return int(year.group(1)) * 12 + (12 if end else 1)
        return None

    def _merge_ranges_in_months(self, ranges: list) -> int:
        if not ranges:
            return 0
        ranges = sorted(ranges)
        merged = []
        for start, end in ranges:
            if not merged or start > merged[-1][1] + 1:
                merged.append([start, end])
            else:
                merged[-1][1] = max(merged[-1][1], end)
        return sum(end - start + 1 for start, end in merged)

    def _infer_role(self, text: str, recent_role: str, skills: list) -> tuple[str, float]:
        skill_set = set(skills)
        title_text = self._clean_heading(recent_role)
        full_text = self._clean_heading(text[:2500])
        scored = []

        for role, profile in ROLE_PROFILES.items():
            profile_skills = set(profile["skills"])
            skill_score = len(skill_set & profile_skills) / max(math.sqrt(len(profile_skills)), 1)
            title_score = 0.0
            for title in profile["title"]:
                cleaned_title = self._clean_heading(title)
                if cleaned_title in title_text:
                    title_score = max(title_score, 0.5 if cleaned_title in GENERIC_ROLE_ALIASES else 2.0)
                elif cleaned_title in full_text:
                    title_score = max(title_score, 0.25 if cleaned_title in GENERIC_ROLE_ALIASES else 1.0)
            scored.append((role, skill_score + title_score))

        scored.sort(key=lambda item: item[1], reverse=True)
        best_role, best_score = scored[0]
        second_score = scored[1][1] if len(scored) > 1 else 0.0
        confidence = min(1.0, (best_score - second_score + 1.0) / 3.0)
        return best_role, round(confidence, 2)

    def _infer_level(self, years: float, recent_role: str, text: str) -> int:
        role_text = self._clean_heading(f"{recent_role} {text[:1000]}")
        if any(term in role_text for term in ["principal", "staff", "architect", "head of", "director"]):
            return 4
        if any(term in role_text for term in ["lead", "manager", "senior"]) and years >= 3:
            return 3
        if years >= 8:
            return 4
        if years >= 5:
            return 3
        if years >= 2:
            return 2
        return 1

    def _extract_education(self, sections: dict) -> str:
        education = sections.get("education", "").strip()
        if not education:
            return "Not Found"
        lines = [line.strip(" -*•") for line in education.splitlines() if line.strip()]
        return " | ".join(lines[:3])[:240] if lines else "Not Found"

    def _strip_accents(self, text: str) -> str:
        import unicodedata

        stripped = "".join(
            char for char in unicodedata.normalize("NFKD", text) if not unicodedata.combining(char)
        )
        return stripped.replace("đ", "d").replace("Đ", "D")


cv_extractor = CVExtractor()

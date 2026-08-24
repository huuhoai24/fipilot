# AI CV Processing Flow

This document details the complete flow of the resume classification and extraction process, from input, through the LLM prompt instructions, to the output structure.

---

## 1. Input Contract

The input to the CV Lab Agent is a JSON payload defined by the `CVInput` Pydantic model:

* **Field:** `resume_text` (String) - The raw text of the uploaded CV/resume.
* **Pre-processing:** The agent limits the raw resume text to the first **12,000 characters** to prevent context window bloat and control latency. This text is serialized as a JSON string (`untrusted_document`) and injected into the prompt.

---

## 2. LLM Processing & Prompt Logic

The LLM receives the prompt consisting of a `SYSTEM_INSTRUCTION` (defining the persona and constraints) and a structured prompt template containing classification and quality instructions.

### A. System Instruction
Instructs the model to act as a precise resume classification and extraction engine, treat the document as untrusted data, extract only facts from the text, and respond in JSON only.

### B. Classification Logic (The 10 Supported Domains)
The LLM evaluates whether the CV belongs to the **10 Supported Technology Domains**:
1. AI Engineer
2. Backend Developer
3. Business Analyst
4. Data Engineer
5. Data Scientist
6. DevOps Engineer
7. Full Stack Developer
8. Software Engineer
9. Tester / QA / QC
10. Web Developer

Based on this, the LLM classifies the `document_type` into one of the following:
* **`resume`**: The document is a valid resume primarily presenting qualifications for one of the 10 supported technology domains.
* **`marginal_resume`**: The document is a resume/CV but is only **slightly suitable / tech-adjacent** (e.g. Digital Marketing, Product Manager, UI/UX Designer, Graphic Design inside software/web projects, Sales in Tech, or other roles that interact closely with tech but are not core IT/software engineering roles).
* **`other`**: Resumes in completely non-IT or unsupported domains (e.g. Nursing, Cooking, general non-tech roles with no IT involvement), or if the document is ambiguous.
* **`portfolio` / `job_description` / `academic_report` / `project_report` / `research_paper` / `certificate`**: Documents that are not resumes.

### C. Missing Section Headings Handling
The prompt instructs the LLM to handle documents where section headings (such as `"SKILLS"`, `"WORK EXPERIENCE"`, `"PROJECTS"`, `"EDUCATION"`) are omitted, merged, or misplaced:
* The LLM identifies skills, work experience, projects, and education based on **text patterns and semantic context**:
  * Lists of technologies indicate skills.
  * Chronological roles with companies, titles, and dates indicate work experience.
  * Project names and descriptions with candidate roles indicate projects.
  * Degree names and institutions indicate education.
* Information is extracted even if the respective heading is entirely missing.

### D. Professional Experience Calculation
To ensure precise estimation of the candidate's professional seniority:
* The LLM is provided with a **temporal reference** of the current month and year (e.g. `August 2026`).
* The LLM must calculate `years_experience` based **ONLY on professional work experience**. Education/university durations (even if tech-related or capstone projects) are strictly excluded from the calculation.
* For ongoing jobs (e.g., `"2022-present"`), the LLM calculates duration dynamically relative to the injected current date.

---

## 3. Output Schema & Processing

### A. Raw LLM Output Schema (`ResumeExtractionResult`)
The LLM outputs a structured JSON object satisfying the `ResumeExtractionResult` schema:
* `document_type` (String Literal)
* `classification_confidence` (Float)
* `closest_domains` (List of strings) - closest matching supported domains for marginal CVs
* `match_percentage` (Integer) - estimated match percentage (0 to 100)
* `name` (String)
* `years_experience` (Float)
* `recent_role` (String)
* `skills` (List of strings)
* `skill_evidence` (List of objects: `skill`, `evidence`, `source_section`)
* `projects` (List of project objects)
* `experiences` (List of experience objects) - ongoing experiences will have their `end_date` set to `"present"`.
* `education` (List of education objects)
* `specialization` (String)
* `confidence_score` (Float)

### B. Agent-Level Validation & Rejection Logic
After parsing the LLM response, the agent validates the results:
1. **Fully Suitable (`document_type == "resume"`)**:
   - The agent normalizes and parses the fields into `CandidateProfile`.
2. **Slightly Suitable (`document_type == "marginal_resume"`)**:
   - The agent raises `MarginalResumeDocumentError` (defined in `exceptions.py`, inheriting from `NonResumeDocumentError`), which constructs the `safe_message` dynamically using `closest_domains` and `match_percentage` extracted by the LLM:
     `"Rất tiếc, CV của bạn ít phù hợp với 10 ngành nghề thuộc khối Công nghệ & Kỹ thuật phần mềm hiện đang được hỗ trợ của hệ thống (AI Engineer, Backend Developer, Business Analyst, Data Engineer, Data Scientist, DevOps Engineer, Full Stack Developer, Software Engineer, Tester/QA/QC, Web Developer)."`
     `"Hệ thống nhận định CV của bạn có thể thuộc domain: <closest_domains> với mức độ phù hợp khoảng <match_percentage>%."`
     `"Bạn có muốn tiếp tục không?"`
3. **Invalid or Unrelated (`document_type != "resume"`)**:
   - The agent raises `NonResumeDocumentError` (defined in `exceptions.py`), which defaults to the error code `not_a_resume` and the standard platform message:
     `"Nền tảng hiện tại chỉ hỗ trợ phỏng vấn cho 10 ngành nghề thuộc khối Công nghệ & Kỹ thuật phần mềm (AI Engineer, Backend Developer, Business Analyst, Data Engineer, Data Scientist, DevOps Engineer, Full Stack Developer, Software Engineer, Tester/QA/QC, Web Developer). CV của bạn không thuộc các ngành được hỗ trợ hoặc không phải là một CV hợp lệ."`

### C. Final Output Schema (`CandidateProfile`)
For validated resumes, the agent converts the output to `CandidateProfile`:
* Standardizes skills, filters up to 30 high-value skills, and selects up to 8 skill evidence items.
* Caps projects and experiences to at most 6 items.

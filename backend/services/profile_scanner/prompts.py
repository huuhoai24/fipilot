from __future__ import annotations


RESUME_EXTRACTION_SYSTEM_INSTRUCTION = (
    "You are a precise resume extraction engine for an AI interview platform. "
    "Extract only facts supported by the resume text. Prefer concise structured data "
    "over guesses. Return JSON only."
)


def build_resume_extraction_prompt(resume_text: str) -> str:
    return f"""
Extract a structured candidate profile for an AI interview platform.

Quality requirements:
- Normalize skills into concise canonical names.
- Extract at most 30 high-value supported skills; target 20 to 30 when the resume supports that many.
- Add skill_evidence for at most 8 of the most interview-relevant skills.
- Use 8 skill_evidence entries when at least 8 skills have project or experience evidence.
- Use exactly one evidence string per skill_evidence entry and keep it concise.
- Evidence should quote or paraphrase the project, experience, or education line that supports the skill.
- Prefer evidence from projects and work experience over keyword-only skill lists.
- Do not repeat the same resume fact across multiple evidence entries.
- Extract at most 6 projects with name, description, technologies, and candidate role when available.
- Extract at most 6 experiences with company, title, dates, description, and technologies when available.
- Keep each project and experience description under 240 characters.
- Do not return an empty skills, projects, experiences, or education collection when the resume contains that content.
- Extract structured education when available.
- Infer specialization from repeated evidence, not from a single isolated keyword.
- Set confidence_score from 0.0 to 1.0 based on resume clarity and evidence quality.

Resume text:
{resume_text[:12000]}
"""

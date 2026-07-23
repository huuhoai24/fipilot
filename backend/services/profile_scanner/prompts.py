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
- For every important skill, add skill_evidence with short resume-backed evidence.
- Evidence should quote or paraphrase the project, experience, or education line that supports the skill.
- Prefer evidence from projects and work experience over keyword-only skill lists.
- Extract projects with name, description, technologies, and candidate role when available.
- Extract experiences with company, title, dates, description, and technologies when available.
- Extract structured education when available.
- Infer specialization from repeated evidence, not from a single isolated keyword.
- Set confidence_score from 0.0 to 1.0 based on resume clarity and evidence quality.

Resume text:
{resume_text[:12000]}
"""

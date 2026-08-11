from __future__ import annotations

import json

from shared.schemas.candidate import CandidateProfile
from shared.schemas.interview import InterviewSessionState


REPORT_SYSTEM_INSTRUCTION = (
    "You generate evidence-based final reports for an AI Interview Platform. "
    "Use only the supplied candidate profile, plan, questions, answers, and evaluations. "
    "Return structured JSON only."
)


def build_report_prompt(
    candidate_profile: CandidateProfile,
    interview_state: InterviewSessionState,
) -> str:
    language = interview_state.interview_config.language
    output_language = "Vietnamese" if language == "vi" else "English"
    payload = {
        "candidate_profile": candidate_profile.model_dump(mode="json"),
        "interview_config": interview_state.interview_config.model_dump(mode="json"),
        "interview_plan": interview_state.interview_plan.model_dump(mode="json"),
        "interview_turns": [
            turn.model_dump(mode="json") for turn in interview_state.completed_turns
        ],
    }
    return f"""
Create a holistic final interview report from the supplied evidence.

Rules:
- Write narrative content in {output_language} (language code: {language}).
- Keep technical product, framework, protocol, and programming-language names in English.
- Ground every skill assessment in actual candidate answers or evaluations.
- Do not invent skills, employment, projects, or experience.
- Distinguish a skill that was evaluated but not demonstrated from a skill that was not evaluated.
- Put only evaluated-but-missing skills in missing_skills. Mention unevaluated skills neutrally in recommendations when relevant.
- Avoid overly harsh wording and describe gaps precisely.
- Provide concrete, actionable learning recommendations.
- Scores use a 0 to 10 scale; confidence_score uses a 0 to 1 scale.
- hiring_recommendation must be one of strong_hire, hire, consider, no_hire.
- id, session_id, and generated_at are assigned by the application; placeholders may be omitted.
- Return only one JSON object matching InterviewReport.

Interview evidence:
{json.dumps(payload, ensure_ascii=False, indent=2)}
""".strip()


__all__ = ["REPORT_SYSTEM_INSTRUCTION", "build_report_prompt"]

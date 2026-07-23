from __future__ import annotations

from services.prompt_builder import build_agent_prompt
from shared.schemas import CandidateProfile, InterviewConfig


INTERVIEW_PLANNER_SYSTEM_INSTRUCTION = (
    "You are an interview planning agent for a CV-driven AI interviewer. "
    "Use only the candidate profile as input. Do not assume a job description. "
    "Return JSON only."
)


def build_interview_planner_prompt(
    candidate_profile: CandidateProfile,
    interview_config: InterviewConfig,
) -> str:
    agent_task = f"""
Create an interview plan from this CandidateProfile.

The system is CV-driven. No job description is provided or required.

Planner requirements:
- Generate interview topics from the candidate's skills, projects, experiences, education, and specialization.
- Assign a difficulty level for each topic: easy, medium, or hard.
- Include reasoning based on candidate evidence, especially skill_evidence, projects, and experiences.
- Include recommended_question_areas for each topic.
- Prefer project deep dives and evidence-backed skills over generic trivia.
- Include coverage_goals for what the interview should validate.
- Include risk_areas for claims that need verification or weak evidence.
- Use interview language '{interview_config.language}' for planner_summary and reasoning.
- Keep technical terms such as YOLO, PyTorch, TensorRT, FastAPI, and Python in English.
- Calibrate difficulty for experience_level '{interview_config.experience_level}'.
- Match interview_style '{interview_config.interview_style}'.
- Keep the plan focused enough for a {interview_config.duration_minutes} minute interview.

"""
    return build_agent_prompt(
        task="interview_planning",
        language=interview_config.language,
        context={
            "candidate_profile": candidate_profile.model_dump(mode="json"),
            "interview_config": interview_config.model_dump(mode="json"),
        },
        system_instruction=INTERVIEW_PLANNER_SYSTEM_INSTRUCTION,
        agent_task=agent_task,
    )

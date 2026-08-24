from __future__ import annotations

import json

from ai_lab.ai_planner.schemas import PlannerInput


SYSTEM_INSTRUCTION = (
    "You are an interview planning agent for a CV-driven AI interviewer. "
    "Use only the candidate profile as input. Do not assume a job description. "
    "Return JSON only."
)


def _language_instruction(language: str) -> str:
    if language == "vi":
        return (
            "The interview language is Vietnamese.\n\nRules:\n"
            "- Ask questions in Vietnamese.\n- Provide feedback in Vietnamese.\n"
            "- Keep technical terms such as YOLO, PyTorch, TensorRT, FastAPI in English.\n"
            "- Do not translate programming concepts."
        )
    return (
        "The interview language is English.\n\nRules:\n"
        "- Ask questions in English.\n- Provide feedback in English.\n"
        "- Keep technical terms unchanged."
    )


def build_prompt(input_data: PlannerInput) -> str:
    config = input_data.interview_config
    agent_task = f"""
Create an interview plan from this CandidateProfile.

The system is CV-driven. No job description is provided or required.

Planner requirements:
- Generate interview topics from the candidate's skills, projects, experiences, education, and specialization.
- Assign a difficulty level for each topic: easy, medium, or hard.
- Include reasoning based on candidate evidence, especially skill_evidence, projects, and experiences.
- Keep each objective and reasoning field to one concise sentence.
- Include 3 to 5 short phrases in recommended_question_areas for each topic; use directions, not fully written questions.
- Keep each recommended question area under 100 characters.
- Prefer project deep dives and evidence-backed skills over generic trivia.
- Use curated_knowledge only to choose relevant topic depth and question direction; candidate evidence remains authoritative.
- Do not plan broad definition questions such as "What is Machine Learning?" when the profile contains specific evidence.
- For evidence-backed topics, plan questions about mechanisms, implementation decisions, trade-offs, debugging, measurement, or failure cases.
- Do not repeat candidate summaries already present in CandidateProfile.
- Use interview language '{config.language}' for objectives and reasoning.
- Keep technical terms such as YOLO, PyTorch, TensorRT, FastAPI, and Python in English.
- Calibrate difficulty for experience_level '{config.experience_level}'.
- Match interview_style '{config.interview_style}'.
- Allocate question_budget for each round such that the sum of question_budget across all rounds exactly equals question_count ({config.question_count}).
- Total planned questions across all rounds must be exactly {config.question_count}.
- Keep the plan focused enough for a {config.duration_minutes} minute interview.
""".strip()
    context = {
        "candidate_profile": input_data.candidate_profile.model_dump(mode="json"),
        "interview_config": config.model_dump(mode="json"),
        "curated_knowledge": input_data.knowledge_topics,
    }
    sections = [
        ("System instruction", SYSTEM_INSTRUCTION),
        ("Language instruction", _language_instruction(config.language)),
        ("Task", "interview_planning"),
        ("Agent task", agent_task),
        ("Context", json.dumps(context, ensure_ascii=False)),
    ]
    return "\n\n".join(f"{title}:\n{body}" for title, body in sections)

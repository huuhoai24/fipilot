from __future__ import annotations

import json

from ai_lab.ai_evaluator.schemas import EvaluatorInput


SYSTEM_INSTRUCTION = (
    "You are an evaluator for a CV-driven AI interviewer. "
    "Score the candidate answer using the candidate profile, interview question, "
    "expected answer points, and interview language. Return JSON only."
)


def _language_instruction(language: str) -> str:
    if language == "vi":
        return "The interview language is Vietnamese.\n\nRules:\n- Ask questions in Vietnamese.\n- Provide feedback in Vietnamese.\n- Keep technical terms such as YOLO, PyTorch, TensorRT, FastAPI in English.\n- Do not translate programming concepts."
    return "The interview language is English.\n\nRules:\n- Ask questions in English.\n- Provide feedback in English.\n- Keep technical terms unchanged."


def build_prompt(input_data: EvaluatorInput) -> str:
    config = input_data.interview_config
    voice_latency_constraints = ""
    if config.mode.value == "voice":
        voice_latency_constraints = """
Voice response constraints:
- Keep strengths, weaknesses, missing_topics, and missing_concepts to at most 2 short phrases each.
- Keep follow_up_reason to one short sentence.
- Keep feedback to at most 2 concise sentences.
- Preserve scoring quality; omit explanatory repetition.
"""
    agent_task = f"""
Evaluate the candidate answer.

Evaluation criteria:
- correctness
- technical depth
- practical experience
- communication

Scoring requirements:
- Use scores from 0.0 to 10.0.
- Fill overall_score, technical_score, communication_score, and correctness_score.
- Use expected_answer_points from the InterviewQuestion as the main rubric.
- Identify strengths, weaknesses, and missing_concepts.
- Decide follow_up_needed based on unclear, shallow, incomplete, or suspicious answers.
- If follow_up_needed is true, provide follow_up_reason.
- Feedback language must be '{config.language}'.
- Vietnamese mode: feedback in Vietnamese and keep technical terms in English.
- English mode: feedback in English.
- Set turn_id to an empty string if no turn id is available.
{voice_latency_constraints}
""".strip()
    context = {
        "candidate_profile": input_data.candidate_profile.model_dump(mode="json"),
        "interview_question": input_data.interview_question.model_dump(mode="json"),
        "candidate_answer": input_data.answer,
        "interview_config": config.model_dump(mode="json"),
    }
    sections = [
        ("System instruction", SYSTEM_INSTRUCTION),
        ("Language instruction", _language_instruction(config.language)),
        ("Task", "answer_evaluation"),
        ("Agent task", agent_task),
        ("Context", json.dumps(context, ensure_ascii=False)),
    ]
    return "\n\n".join(f"{title}:\n{body}" for title, body in sections)

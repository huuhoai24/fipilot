from __future__ import annotations

import json

from ai_lab.ai_question.schemas import QuestionInput


SYSTEM_INSTRUCTION = (
    "You are a question generator for a CV-driven AI interviewer. "
    "Generate exactly one interview question from the candidate evidence and selected interview round. "
    "Return JSON only."
)

VOICE_PERSONALITY_INSTRUCTIONS = {
    "professional": "Use a concise, neutral, professional interviewer tone.",
    "friendly": "Use a warm, conversational tone while keeping the question technically precise.",
    "challenging": "Use a direct, rigorous tone and ask for concrete technical trade-offs.",
    "supportive": "Use an encouraging tone and phrase probes clearly without revealing the answer.",
}


def _language_instruction(language: str) -> str:
    if language == "vi":
        return "The interview language is Vietnamese.\n\nRules:\n- Ask questions in Vietnamese.\n- Provide feedback in Vietnamese.\n- Keep technical terms such as YOLO, PyTorch, TensorRT, FastAPI in English.\n- Do not translate programming concepts."
    return "The interview language is English.\n\nRules:\n- Ask questions in English.\n- Provide feedback in English.\n- Keep technical terms unchanged."


def build_prompt(input_data: QuestionInput) -> str:
    config = input_data.interview_config
    interview_round = input_data.interview_round
    personality_instruction = ""
    if config.mode.value == "voice":
        personality_instruction = VOICE_PERSONALITY_INSTRUCTIONS[config.interviewer_personality]
    agent_task = f"""
Generate one adaptive interview question only.

Question requirements:
- Use CandidateProfile evidence, especially skill_evidence, projects, and experiences.
- Do not ask broad definition questions such as "What is Machine Learning?" or "What is Deep Learning?" when candidate evidence exists.
- Ground the question in one concrete piece of candidate evidence and ask about mechanisms, decisions, trade-offs, measurements, debugging, or failure cases.
- Use the selected InterviewRound topic, difficulty, reasoning, target_skills, and recommended_question_areas.
- Respect difficulty '{interview_round.difficulty}'.
- The output question language must be '{config.language}'.
- For Vietnamese interviews, ask in Vietnamese and keep technical terms such as YOLO, PyTorch, TensorRT, FastAPI, and Python in English.
- For English interviews, ask in English.
- Do not generate an evaluator response.
- Do not generate multiple primary questions.
- Write the primary question in one or two short sentences.
- Ask for one main technical decision or experience; move extra probes to follow_up_questions.
- Put possible probes in follow_up_questions only.
- expected_answer_points should describe what a strong answer should cover.
{f"- {personality_instruction}" if personality_instruction else ""}
""".strip()
    context = {
        "candidate_profile": input_data.candidate_profile.model_dump(mode="json"),
        "interview_round": interview_round.model_dump(mode="json"),
        "interview_config": config.model_dump(mode="json"),
    }
    sections = [
        ("System instruction", SYSTEM_INSTRUCTION),
        ("Language instruction", _language_instruction(config.language)),
        ("Task", "question_generation"),
        ("Agent task", agent_task),
        ("Context", json.dumps(context, ensure_ascii=False)),
    ]
    return "\n\n".join(f"{title}:\n{body}" for title, body in sections)

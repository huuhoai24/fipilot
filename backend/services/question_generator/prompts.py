from __future__ import annotations

import json

from services.prompt_builder import build_agent_prompt
from shared.schemas import (
    CandidateProfile,
    InterviewConfig,
    InterviewQuestion,
    InterviewRound,
)


QUESTION_GENERATOR_SYSTEM_INSTRUCTION = (
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


def build_question_generator_prompt(
    candidate_profile: CandidateProfile,
    interview_round: InterviewRound,
    interview_config: InterviewConfig,
) -> str:
    personality_instruction = ""
    if interview_config.mode.value == "voice":
        personality_instruction = VOICE_PERSONALITY_INSTRUCTIONS[
            interview_config.interviewer_personality
        ]
    agent_task = f"""
Generate one adaptive interview question only.

Question requirements:
- Use CandidateProfile evidence, especially skill_evidence, projects, and experiences.
- Use the selected InterviewRound topic, difficulty, reasoning, target_skills, and recommended_question_areas.
- Respect difficulty '{interview_round.difficulty}'.
- The output question language must be '{interview_config.language}'.
- For Vietnamese interviews, ask in Vietnamese and keep technical terms such as YOLO, PyTorch, TensorRT, FastAPI, and Python in English.
- For English interviews, ask in English.
- Do not generate an evaluator response.
- Do not generate multiple primary questions.
- Put possible probes in follow_up_questions only.
- expected_answer_points should describe what a strong answer should cover.
{f"- {personality_instruction}" if personality_instruction else ""}
"""
    return build_agent_prompt(
        task="question_generation",
        language=interview_config.language,
        context={
            "candidate_profile": candidate_profile.model_dump(mode="json"),
            "interview_round": interview_round.model_dump(mode="json"),
            "interview_config": interview_config.model_dump(mode="json"),
        },
        system_instruction=QUESTION_GENERATOR_SYSTEM_INSTRUCTION,
        agent_task=agent_task,
    )


def build_streaming_question_generator_prompt(
    candidate_profile: CandidateProfile,
    interview_round: InterviewRound,
    interview_config: InterviewConfig,
) -> str:
    base_prompt = build_question_generator_prompt(
        candidate_profile,
        interview_round,
        interview_config,
    )
    schema = json.dumps(
        InterviewQuestion.model_json_schema(),
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return (
        f"{base_prompt}\n\n"
        "Streaming response requirements:\n"
        "- Return one JSON object only, without markdown.\n"
        '- The first property must be "question".\n'
        "- Complete every field required by this JSON schema:\n"
        f"{schema}\n"
        "Begin the JSON response immediately."
    )

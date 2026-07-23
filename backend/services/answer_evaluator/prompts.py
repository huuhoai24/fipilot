from __future__ import annotations

from services.prompt_builder import build_agent_prompt
from shared.schemas import CandidateProfile, InterviewConfig, InterviewQuestion


EVALUATOR_SYSTEM_INSTRUCTION = (
    "You are an evaluator for a CV-driven AI interviewer. "
    "Score the candidate answer using the candidate profile, interview question, "
    "expected answer points, and interview language. Return JSON only."
)


def build_evaluator_prompt(
    candidate_profile: CandidateProfile,
    interview_question: InterviewQuestion,
    answer: str,
    interview_config: InterviewConfig,
) -> str:
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
- Feedback language must be '{interview_config.language}'.
- Vietnamese mode: feedback in Vietnamese and keep technical terms in English.
- English mode: feedback in English.
- Set turn_id to an empty string if no turn id is available.
"""
    return build_agent_prompt(
        task="answer_evaluation",
        language=interview_config.language,
        context={
            "candidate_profile": candidate_profile.model_dump(mode="json"),
            "interview_question": interview_question.model_dump(mode="json"),
            "candidate_answer": answer,
            "interview_config": interview_config.model_dump(mode="json"),
        },
        system_instruction=EVALUATOR_SYSTEM_INSTRUCTION,
        agent_task=agent_task,
    )

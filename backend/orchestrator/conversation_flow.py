from __future__ import annotations

from shared.schemas import (
    InterviewMode,
    InterviewQuestion,
    InterviewSessionState,
    InterviewTurn,
)


def begin_text_conversation(state: InterviewSessionState) -> InterviewSessionState:
    """Add a persisted opening exchange without replacing the planned first question."""
    if (
        state.interview_config.mode != InterviewMode.TEXT
        or state.phase != "interviewing"
        or state.current_turn is None
    ):
        return state

    opening_question = InterviewQuestion(
        question=_opening_text(state),
        language=state.interview_config.language,
        topic="Introduction",
        difficulty="easy",
        expected_answer_points=[],
        follow_up_questions=[],
    )
    opening_turn = InterviewTurn(
        turn_id="turn-opening",
        question=opening_question,
        question_type="opening",
        difficulty="easy",
        topic="Introduction",
        expected_signal=[],
    )
    return state.model_copy(
        update={
            "phase": "opening",
            "current_turn": opening_turn,
            "pending_turn": state.current_turn,
        }
    )


def answer_opening(
    state: InterviewSessionState,
    answer: str,
) -> InterviewSessionState | None:
    """Persist the introduction answer and reveal the existing first planned turn."""
    if state.phase != "opening" or state.current_turn is None:
        return None

    answered_opening = state.current_turn.model_copy(
        update={
            "answer": answer,
            "candidate_answer": answer,
            "status": "answered",
        }
    )
    return state.model_copy(
        update={
            "phase": "interviewing",
            "opening_turn": answered_opening,
            "current_turn": state.pending_turn,
            "pending_turn": None,
        }
    )


def enter_closing_if_finished(state: InterviewSessionState) -> InterviewSessionState:
    if (
        state.interview_config.mode == InterviewMode.TEXT
        and state.phase == "interviewing"
        and state.current_turn is None
    ):
        return state.model_copy(update={"phase": "closing"})
    return state


def _opening_text(state: InterviewSessionState) -> str:
    name = state.candidate_profile.name.strip()
    style = state.interview_config.interview_style

    if state.interview_config.language == "vi":
        greeting = f"Chào {name}, rất vui được gặp bạn." if name else "Chào bạn, rất vui được gặp bạn."
        style_label = {
            "technical": "kỹ thuật",
            "behavioral": "hành vi",
            "mixed": "kết hợp kỹ thuật và hành vi",
        }[style]
        return (
            f"{greeting}\n\n"
            f"Hôm nay tôi sẽ thực hiện buổi phỏng vấn {style_label} với bạn. "
            "Chúng ta sẽ trao đổi về kinh nghiệm, các dự án trong CV và một vài chủ đề liên quan.\n\n"
            "Để bắt đầu, bạn có thể giới thiệu ngắn gọn về bản thân không?"
        )

    greeting = f"Hi {name}, nice to meet you." if name else "Hello, nice to meet you."
    style_label = {
        "technical": "technical",
        "behavioral": "behavioral",
        "mixed": "technical and behavioral",
    }[style]
    return (
        f"{greeting}\n\n"
        f"I'll be conducting your {style_label} interview today. "
        "We'll talk about your background, projects from your CV, and a few relevant topics.\n\n"
        "To start, could you briefly introduce yourself?"
    )


__all__ = [
    "answer_opening",
    "begin_text_conversation",
    "enter_closing_if_finished",
]

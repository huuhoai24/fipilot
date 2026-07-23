from __future__ import annotations

from shared.schemas import AnswerEvaluation, InterviewDecision, InterviewQuestion, InterviewSessionState


class InterviewDecisionService:
    def decide(
        self,
        evaluation: AnswerEvaluation,
        current_question: InterviewQuestion,
        session_state: InterviewSessionState,
    ) -> InterviewDecision:
        if evaluation.follow_up_needed:
            return InterviewDecision(
                action="follow_up",
                reason=evaluation.follow_up_reason or "Evaluation requires a follow-up question.",
                next_topic=current_question.topic,
            )

        score = evaluation.overall_score or evaluation.scores.overall_score
        if score >= 8:
            return InterviewDecision(
                action="increase_difficulty",
                reason="Candidate answer scored 8 or higher.",
                next_topic=current_question.topic,
                difficulty_change="increase",
            )

        return InterviewDecision(
            action="next_question",
            reason="Candidate answer does not require follow-up and is below the difficulty increase threshold.",
            next_topic=self._next_topic(session_state),
        )

    @staticmethod
    def _next_topic(session_state: InterviewSessionState) -> str | None:
        next_index = session_state.current_question_index + 1
        if next_index < len(session_state.interview_plan.rounds):
            return session_state.interview_plan.rounds[next_index].topic
        return None

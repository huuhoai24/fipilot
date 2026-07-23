from __future__ import annotations

from shared.schemas import (
    AnswerEvaluation,
    InterviewMemoryState,
    InterviewQuestion,
    InterviewRound,
)


class InterviewMemoryService:
    """Builds bounded interview context from structured evaluation output."""

    max_items = 20

    def update(
        self,
        memory: InterviewMemoryState,
        *,
        question: InterviewQuestion,
        interview_round: InterviewRound,
        evaluation: AnswerEvaluation,
    ) -> InterviewMemoryState:
        covered = interview_round.target_skills or [question.topic]
        follow_up = [
            evaluation.follow_up_reason,
            *evaluation.missing_topics,
            *evaluation.missing_concepts,
        ]
        return InterviewMemoryState(
            previous_topics=self._merge(memory.previous_topics, [question.topic]),
            covered_skills=self._merge(memory.covered_skills, covered),
            weaknesses=self._merge(
                memory.weaknesses,
                [
                    *evaluation.weaknesses,
                    *evaluation.missing_topics,
                    *evaluation.missing_concepts,
                ],
            ),
            follow_up_points=self._merge(
                memory.follow_up_points,
                [item for item in follow_up if item],
            ),
        )

    def apply_to_round(
        self,
        interview_round: InterviewRound,
        memory: InterviewMemoryState,
    ) -> InterviewRound:
        memory_context = [
            *(f"Unresolved: {item}" for item in memory.follow_up_points[-5:]),
            *(f"Weakness: {item}" for item in memory.weaknesses[-5:]),
        ]
        previous = ", ".join(memory.previous_topics[-5:])
        reasoning = interview_round.reasoning
        if previous:
            reasoning = (
                f"{reasoning} Previously covered topics: {previous}."
            ).strip()
        return interview_round.model_copy(
            update={
                "reasoning": reasoning,
                "recommended_question_areas": self._merge(
                    interview_round.recommended_question_areas,
                    memory_context,
                ),
            }
        )

    def _merge(self, existing: list[str], additions: list[str]) -> list[str]:
        merged: list[str] = []
        seen: set[str] = set()
        for raw_value in [*existing, *additions]:
            value = raw_value.strip()
            key = value.casefold()
            if not value or key in seen:
                continue
            seen.add(key)
            merged.append(value)
        return merged[-self.max_items :]

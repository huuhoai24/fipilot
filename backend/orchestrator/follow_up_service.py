from __future__ import annotations

import re

from shared.schemas import AnswerEvaluation


class FollowUpSelectionService:
    """Ranks existing probes against structured evaluator feedback."""

    _token_pattern = re.compile(r"[a-zA-Z0-9+#.-]+")

    def select(
        self,
        candidates: list[str],
        evaluation: AnswerEvaluation,
    ) -> str:
        if not candidates:
            raise ValueError("At least one follow-up candidate is required.")
        feedback = " ".join(
            value
            for value in [
                evaluation.follow_up_reason or "",
                *evaluation.weaknesses,
                *evaluation.missing_topics,
                *evaluation.missing_concepts,
            ]
            if value
        )
        feedback_tokens = self._tokens(feedback)
        ranked = [
            (
                len(self._tokens(candidate) & feedback_tokens),
                -index,
                candidate,
            )
            for index, candidate in enumerate(candidates)
        ]
        return max(ranked)[2]

    def _tokens(self, text: str) -> set[str]:
        return {
            token.casefold()
            for token in self._token_pattern.findall(text)
            if len(token) > 2
        }

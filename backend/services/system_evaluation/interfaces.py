from __future__ import annotations

from typing import Protocol

from infrastructure.speech.stt.base import StreamingSTTFactory
from infrastructure.speech.tts.base import StreamingTTS
from services.system_evaluation.schemas import QuestionQualityScore
from shared.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    InterviewConfig,
    InterviewQuestion,
    InterviewRound,
)


class ProfileExtractor(Protocol):
    async def extract_profile(self, resume_text: str) -> CandidateProfile: ...


class QuestionGenerator(Protocol):
    async def generate_question(
        self,
        candidate_profile: CandidateProfile,
        interview_round: InterviewRound,
        interview_config: InterviewConfig,
    ) -> InterviewQuestion: ...


class AnswerEvaluator(Protocol):
    async def evaluate_answer(
        self,
        candidate_profile: CandidateProfile,
        interview_question: InterviewQuestion,
        answer: str,
        interview_config: InterviewConfig,
    ) -> AnswerEvaluation: ...


class QuestionQualityJudge(Protocol):
    async def score_question(
        self,
        candidate_profile: CandidateProfile,
        interview_round: InterviewRound,
        interview_config: InterviewConfig,
        generated_question: InterviewQuestion,
    ) -> QuestionQualityScore: ...


__all__ = [
    "AnswerEvaluator",
    "ProfileExtractor",
    "QuestionGenerator",
    "QuestionQualityJudge",
    "StreamingSTTFactory",
    "StreamingTTS",
]

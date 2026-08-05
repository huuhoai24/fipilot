from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from shared.schemas import CandidateProfile, InterviewConfig, InterviewQuestion, InterviewRound


@dataclass(frozen=True)
class CVEvaluationCase:
    case_id: str
    resume_text: str = field(repr=False)
    expected_skills: tuple[str, ...] = ()
    expected_profile_fields: dict[str, Any] = field(default_factory=dict, repr=False)
    document_processing_ms: float = 0.0


@dataclass(frozen=True)
class STTEvaluationCase:
    case_id: str
    audio_chunks: tuple[bytes, ...] = field(repr=False)
    reference_text: str = field(repr=False)
    category: Literal["vi", "en", "mixed_technical"] = "vi"


@dataclass(frozen=True)
class TTSEvaluationCase:
    case_id: str
    text: str = field(repr=False)


@dataclass(frozen=True)
class QuestionEvaluationCase:
    case_id: str
    candidate_profile: CandidateProfile = field(repr=False)
    interview_round: InterviewRound = field(repr=False)
    interview_config: InterviewConfig = field(repr=False)


@dataclass(frozen=True)
class EvaluatorEvaluationCase:
    case_id: str
    candidate_profile: CandidateProfile = field(repr=False)
    interview_question: InterviewQuestion = field(repr=False)
    candidate_answer: str = field(repr=False)
    interview_config: InterviewConfig = field(repr=False)
    human_score: float


@dataclass(frozen=True)
class VoiceTurnObservation:
    total_latency_ms: float | None
    success: bool


@dataclass(frozen=True)
class EvaluationDataset:
    name: str = "system-evaluation"
    cv_cases: tuple[CVEvaluationCase, ...] = ()
    stt_cases: tuple[STTEvaluationCase, ...] = ()
    tts_cases: tuple[TTSEvaluationCase, ...] = ()
    question_cases: tuple[QuestionEvaluationCase, ...] = ()
    evaluator_cases: tuple[EvaluatorEvaluationCase, ...] = ()
    voice_turns: tuple[VoiceTurnObservation, ...] = ()

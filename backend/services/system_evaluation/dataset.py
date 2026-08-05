from __future__ import annotations

import json
import time
import wave
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from services.system_evaluation.cases import (
    CVEvaluationCase,
    EvaluationDataset,
    EvaluatorEvaluationCase,
    QuestionEvaluationCase,
    STTEvaluationCase,
    TTSEvaluationCase,
    VoiceTurnObservation,
)
from shared.schemas import CandidateProfile, InterviewConfig, InterviewQuestion, InterviewRound


class _ManifestModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CVCaseManifest(_ManifestModel):
    case_id: str
    resume_path: str
    expected_skills: list[str] = Field(default_factory=list)
    expected_profile_fields: dict[str, Any] = Field(default_factory=dict)


class STTCaseManifest(_ManifestModel):
    case_id: str
    audio_path: str
    reference_text_path: str
    category: Literal["vi", "en", "mixed_technical"]
    chunk_duration_ms: int = Field(default=100, ge=20, le=1000)


class TTSCaseManifest(_ManifestModel):
    case_id: str
    text: str


class QuestionCaseManifest(_ManifestModel):
    case_id: str
    candidate_profile: CandidateProfile
    interview_round: InterviewRound
    interview_config: InterviewConfig


class EvaluatorCaseManifest(_ManifestModel):
    case_id: str
    candidate_profile: CandidateProfile
    interview_question: InterviewQuestion
    candidate_answer: str
    interview_config: InterviewConfig
    human_score: float = Field(ge=0.0, le=10.0)


class VoiceTurnManifest(_ManifestModel):
    success: bool
    total_latency_ms: float | None = Field(default=None, ge=0.0)


class EvaluationManifest(_ManifestModel):
    dataset_name: str = "system-evaluation"
    cv_cases: list[CVCaseManifest] = Field(default_factory=list)
    stt_cases: list[STTCaseManifest] = Field(default_factory=list)
    tts_cases: list[TTSCaseManifest] = Field(default_factory=list)
    question_cases: list[QuestionCaseManifest] = Field(default_factory=list)
    evaluator_cases: list[EvaluatorCaseManifest] = Field(default_factory=list)
    voice_turns: list[VoiceTurnManifest] = Field(default_factory=list)


def load_evaluation_dataset(manifest_path: str | Path, document_service) -> EvaluationDataset:
    path = Path(manifest_path).resolve()
    manifest = EvaluationManifest.model_validate_json(path.read_text(encoding="utf-8"))
    base_directory = path.parent

    cv_cases: list[CVEvaluationCase] = []
    for case in manifest.cv_cases:
        resume_path = _resolve_path(base_directory, case.resume_path)
        started = time.perf_counter()
        if resume_path.suffix.lower() == ".txt":
            resume_text = resume_path.read_text(encoding="utf-8")
        else:
            resume_text = document_service.extract_text(
                str(resume_path),
                resume_path.name,
            )
        cv_cases.append(
            CVEvaluationCase(
                case_id=case.case_id,
                resume_text=resume_text,
                expected_skills=tuple(case.expected_skills),
                expected_profile_fields=case.expected_profile_fields,
                document_processing_ms=(time.perf_counter() - started) * 1000,
            )
        )

    stt_cases = [
        _load_stt_case(base_directory, case)
        for case in manifest.stt_cases
    ]
    return EvaluationDataset(
        name=manifest.dataset_name,
        cv_cases=tuple(cv_cases),
        stt_cases=tuple(stt_cases),
        tts_cases=tuple(
            TTSEvaluationCase(case_id=case.case_id, text=case.text)
            for case in manifest.tts_cases
        ),
        question_cases=tuple(
            QuestionEvaluationCase(
                case_id=case.case_id,
                candidate_profile=case.candidate_profile,
                interview_round=case.interview_round,
                interview_config=case.interview_config,
            )
            for case in manifest.question_cases
        ),
        evaluator_cases=tuple(
            EvaluatorEvaluationCase(
                case_id=case.case_id,
                candidate_profile=case.candidate_profile,
                interview_question=case.interview_question,
                candidate_answer=case.candidate_answer,
                interview_config=case.interview_config,
                human_score=case.human_score,
            )
            for case in manifest.evaluator_cases
        ),
        voice_turns=tuple(
            VoiceTurnObservation(
                success=turn.success,
                total_latency_ms=turn.total_latency_ms,
            )
            for turn in manifest.voice_turns
        ),
    )


def _load_stt_case(base_directory: Path, case: STTCaseManifest) -> STTEvaluationCase:
    audio_path = _resolve_path(base_directory, case.audio_path)
    reference_path = _resolve_path(base_directory, case.reference_text_path)
    with wave.open(str(audio_path), "rb") as audio:
        if (
            audio.getnchannels() != 1
            or audio.getsampwidth() != 2
            or audio.getframerate() != 16_000
            or audio.getcomptype() != "NONE"
        ):
            raise ValueError(
                "STT fixtures must be mono, uncompressed PCM16 WAV at 16 kHz."
            )
        pcm = audio.readframes(audio.getnframes())
    chunk_size = max(2, 16_000 * 2 * case.chunk_duration_ms // 1000)
    chunks = tuple(
        pcm[offset : offset + chunk_size]
        for offset in range(0, len(pcm), chunk_size)
        if pcm[offset : offset + chunk_size]
    )
    return STTEvaluationCase(
        case_id=case.case_id,
        audio_chunks=chunks,
        reference_text=reference_path.read_text(encoding="utf-8").strip(),
        category=case.category,
    )


def _resolve_path(base_directory: Path, relative_path: str) -> Path:
    path = (base_directory / relative_path).resolve()
    if not path.is_file():
        raise ValueError("Evaluation fixture file was not found.")
    return path

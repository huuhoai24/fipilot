from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


BenchmarkStatus = Literal["completed", "partial", "no_data"]
DatasetValidationStatus = Literal["valid", "partial", "invalid"]


class DatasetSectionValidation(BaseModel):
    total_samples: int = Field(default=0, ge=0)
    valid_samples: int = Field(default=0, ge=0)
    invalid_samples: int = Field(default=0, ge=0)
    skipped_samples: int = Field(default=0, ge=0)
    issue_counts: dict[str, int] = Field(default_factory=dict)


class DatasetValidationSummary(BaseModel):
    schema_version: str = "1.0"
    status: DatasetValidationStatus = "valid"
    invalid_files: int = Field(default=0, ge=0)
    skipped_samples: int = Field(default=0, ge=0)
    missing_annotations: int = Field(default=0, ge=0)
    duplicate_ids: int = Field(default=0, ge=0)
    sections: dict[str, DatasetSectionValidation] = Field(default_factory=dict)
    issue_counts: dict[str, int] = Field(default_factory=dict)
    cv_parsing_failures_by_format: dict[str, int] = Field(
        default_factory=lambda: {"pdf": 0, "docx": 0}
    )
    aggregate_only: bool = True


class BenchmarkDatasetSummary(BaseModel):
    total_cv_samples: int = Field(default=0, ge=0)
    valid_cv_samples: int = Field(default=0, ge=0)
    invalid_cv_samples: int = Field(default=0, ge=0)
    total_speech_samples: int = Field(default=0, ge=0)
    valid_speech_samples: int = Field(default=0, ge=0)
    invalid_speech_samples: int = Field(default=0, ge=0)
    language_distribution: dict[str, int] = Field(default_factory=dict)
    average_audio_duration_seconds: float | None = Field(default=None, ge=0.0)
    average_transcript_length_words: float | None = Field(default=None, ge=0.0)
    synthetic_sections: list[str] = Field(default_factory=list)


class CVAccuracyMetrics(BaseModel):
    status: BenchmarkStatus = "no_data"
    sample_count: int = Field(default=0, ge=0)
    failure_count: int = Field(default=0, ge=0)
    skill_precision: float | None = Field(default=None, ge=0.0, le=1.0)
    skill_recall: float | None = Field(default=None, ge=0.0, le=1.0)
    skill_f1: float | None = Field(default=None, ge=0.0, le=1.0)
    profile_field_accuracy: float | None = Field(default=None, ge=0.0, le=1.0)
    processing_latency_ms: float | None = Field(default=None, ge=0.0)


class STTCategoryMetrics(BaseModel):
    sample_count: int = Field(default=0, ge=0)
    wer: float | None = Field(default=None, ge=0.0)
    cer: float | None = Field(default=None, ge=0.0)
    latency_ms: float | None = Field(default=None, ge=0.0)


class STTMetrics(BaseModel):
    status: BenchmarkStatus = "no_data"
    sample_count: int = Field(default=0, ge=0)
    failure_count: int = Field(default=0, ge=0)
    wer: float | None = Field(default=None, ge=0.0)
    cer: float | None = Field(default=None, ge=0.0)
    latency_ms: float | None = Field(default=None, ge=0.0)
    by_category: dict[str, STTCategoryMetrics] = Field(default_factory=dict)


class TTSMetrics(BaseModel):
    status: BenchmarkStatus = "no_data"
    sample_count: int = Field(default=0, ge=0)
    failure_count: int = Field(default=0, ge=0)
    first_audio_ms: float | None = Field(default=None, ge=0.0)
    generation_duration_ms: float | None = Field(default=None, ge=0.0)
    generated_audio_duration_ms: float | None = Field(default=None, ge=0.0)
    real_time_factor: float | None = Field(default=None, ge=0.0)


class QuestionQualityScore(BaseModel):
    relevance_score: float = Field(ge=0.0, le=1.0)
    difficulty_alignment: float = Field(ge=0.0, le=1.0)
    cv_alignment: float = Field(ge=0.0, le=1.0)


class QuestionGeneratorMetrics(BaseModel):
    status: BenchmarkStatus = "no_data"
    sample_count: int = Field(default=0, ge=0)
    failure_count: int = Field(default=0, ge=0)
    relevance_score: float | None = Field(default=None, ge=0.0, le=1.0)
    difficulty_alignment: float | None = Field(default=None, ge=0.0, le=1.0)
    cv_alignment: float | None = Field(default=None, ge=0.0, le=1.0)
    generation_latency_ms: float | None = Field(default=None, ge=0.0)


class EvaluatorMetrics(BaseModel):
    status: BenchmarkStatus = "no_data"
    sample_count: int = Field(default=0, ge=0)
    failure_count: int = Field(default=0, ge=0)
    repetitions: int = Field(default=0, ge=0)
    score_consistency: float | None = Field(default=None, ge=0.0, le=1.0)
    score_mean_absolute_deviation: float | None = Field(default=None, ge=0.0)
    mae_against_human: float | None = Field(default=None, ge=0.0)
    evaluation_latency_ms: float | None = Field(default=None, ge=0.0)


class LLMMetrics(BaseModel):
    question_generator: QuestionGeneratorMetrics = Field(default_factory=QuestionGeneratorMetrics)
    evaluator: EvaluatorMetrics = Field(default_factory=EvaluatorMetrics)


class VoiceTurnMetrics(BaseModel):
    status: BenchmarkStatus = "no_data"
    sample_count: int = Field(default=0, ge=0)
    failure_count: int = Field(default=0, ge=0)
    average_latency_ms: float | None = Field(default=None, ge=0.0)
    p50_latency_ms: float | None = Field(default=None, ge=0.0)
    p95_latency_ms: float | None = Field(default=None, ge=0.0)
    failure_rate: float | None = Field(default=None, ge=0.0, le=1.0)


class SystemEvaluationReport(BaseModel):
    schema_version: str = "2.0"
    dataset_name: str
    status: BenchmarkStatus
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    dataset_summary: BenchmarkDatasetSummary = Field(
        default_factory=BenchmarkDatasetSummary
    )
    dataset_validation: DatasetValidationSummary = Field(
        default_factory=DatasetValidationSummary
    )
    cv_accuracy: CVAccuracyMetrics = Field(default_factory=CVAccuracyMetrics)
    cv_by_format: dict[str, CVAccuracyMetrics] = Field(
        default_factory=lambda: {
            "pdf": CVAccuracyMetrics(),
            "docx": CVAccuracyMetrics(),
        }
    )
    stt: STTMetrics = Field(default_factory=STTMetrics)
    tts: TTSMetrics = Field(default_factory=TTSMetrics)
    llm: LLMMetrics = Field(default_factory=LLMMetrics)
    voice_turn: VoiceTurnMetrics = Field(default_factory=VoiceTurnMetrics)
    limitations: list[str] = Field(default_factory=list)

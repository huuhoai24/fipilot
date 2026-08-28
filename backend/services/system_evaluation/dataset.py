from __future__ import annotations

import audioop
import csv
import hashlib
import json
import time
import wave
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from services.system_evaluation.cases import (
    CVEvaluationCase,
    EvaluationDataset,
    EvaluatorEvaluationCase,
    QuestionEvaluationCase,
    STTEvaluationCase,
    TTSEvaluationCase,
    VoiceTurnObservation,
)
from services.system_evaluation.schemas import (
    BenchmarkDatasetSummary,
    DatasetSectionValidation,
    DatasetValidationSummary,
)
from shared.schemas import CandidateProfile, InterviewConfig, InterviewQuestion, InterviewRound


_SUPPORTED_RESUME_FORMATS = {".pdf", ".docx"}
_TECHNICAL_TERMS = (
    "yolov8",
    "fastapi",
    "kubernetes",
    "pytorch",
    "tensorrt",
    "docker",
)
_VIETNAMESE_CHARACTERS = frozenset(
    "ăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩị"
    "óòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ"
)


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


class _ValidationCollector:
    def __init__(self) -> None:
        self._sections: dict[str, dict[str, Any]] = defaultdict(
            lambda: {
                "total": 0,
                "valid": 0,
                "invalid": 0,
                "skipped": 0,
                "issues": Counter(),
            }
        )
        self._issues: Counter[str] = Counter()
        self.parsing_failures: Counter[str] = Counter()

    def register(self, section: str, count: int = 1) -> None:
        self._sections[section]["total"] += count

    def valid(self, section: str, count: int = 1) -> None:
        self._sections[section]["valid"] += count

    def invalid(self, section: str, *codes: str) -> None:
        self._sections[section]["invalid"] += 1
        self._sections[section]["skipped"] += 1
        for code in sorted(set(codes)):
            self.issue(section, code)

    def issue(self, section: str, code: str, count: int = 1) -> None:
        if count <= 0:
            return
        self._sections[section]["issues"][code] += count
        self._issues[code] += count

    def summary(self) -> DatasetValidationSummary:
        sections = {
            name: DatasetSectionValidation(
                total_samples=values["total"],
                valid_samples=values["valid"],
                invalid_samples=values["invalid"],
                skipped_samples=values["skipped"],
                issue_counts=dict(sorted(values["issues"].items())),
            )
            for name, values in sorted(self._sections.items())
        }
        invalid_files = sum(section.invalid_samples for section in sections.values())
        skipped = sum(section.skipped_samples for section in sections.values())
        has_valid = any(section.valid_samples for section in sections.values())
        if not self._issues:
            status = "valid"
        elif has_valid:
            status = "partial"
        else:
            status = "invalid"
        return DatasetValidationSummary(
            status=status,
            invalid_files=invalid_files,
            skipped_samples=skipped,
            missing_annotations=(
                self._issues["missing_ground_truth"]
                + self._issues["missing_transcript"]
            ),
            duplicate_ids=self._issues["duplicate_id"],
            sections=sections,
            issue_counts=dict(sorted(self._issues.items())),
            cv_parsing_failures_by_format={
                "pdf": self.parsing_failures["pdf"],
                "docx": self.parsing_failures["docx"],
            },
        )


def load_evaluation_dataset(
    dataset_path: str | Path,
    document_service,
) -> EvaluationDataset:
    path = Path(dataset_path).resolve()
    if path.is_dir():
        return _load_directory_dataset(path, document_service)
    return _load_manifest_dataset(path, document_service)


def _load_directory_dataset(root: Path, document_service) -> EvaluationDataset:
    validation = _ValidationCollector()
    cv_cases = _load_cv_directory(root, document_service, validation)
    stt_cases = _load_stt_directory(root, validation)
    tts_cases, tts_synthetic = _load_tts_directory(root, validation)
    question_cases, llm_synthetic = _load_question_directory(root, validation)
    evaluator_cases, evaluator_synthetic = _load_evaluator_directory(root, validation)
    voice_turns, voice_synthetic = _load_voice_directory(root, validation)
    validation_summary = validation.summary()

    cv_section = validation_summary.sections.get("cv", DatasetSectionValidation())
    stt_section = validation_summary.sections.get("stt", DatasetSectionValidation())
    language_distribution = Counter(
        _display_category(case.category) for case in stt_cases
    )
    durations = [case.audio_duration_seconds for case in stt_cases]
    transcript_lengths = [case.transcript_word_count for case in stt_cases]
    synthetic_sections = [
        section
        for section, is_synthetic in (
            ("TTS", tts_synthetic),
            ("LLM question generation", llm_synthetic),
            ("evaluator", evaluator_synthetic),
            ("voice latency", voice_synthetic),
        )
        if is_synthetic
    ]
    summary = BenchmarkDatasetSummary(
        total_cv_samples=cv_section.total_samples,
        valid_cv_samples=cv_section.valid_samples,
        invalid_cv_samples=cv_section.invalid_samples,
        total_speech_samples=stt_section.total_samples,
        valid_speech_samples=stt_section.valid_samples,
        invalid_speech_samples=stt_section.invalid_samples,
        language_distribution=dict(sorted(language_distribution.items())),
        average_audio_duration_seconds=(
            sum(durations) / len(durations) if durations else None
        ),
        average_transcript_length_words=(
            sum(transcript_lengths) / len(transcript_lengths)
            if transcript_lengths
            else None
        ),
        synthetic_sections=synthetic_sections,
    )
    return EvaluationDataset(
        name=root.name,
        cv_cases=tuple(cv_cases),
        stt_cases=tuple(stt_cases),
        tts_cases=tuple(tts_cases),
        question_cases=tuple(question_cases),
        evaluator_cases=tuple(evaluator_cases),
        voice_turns=tuple(voice_turns),
        summary=summary,
        validation=validation_summary,
    )


def _load_cv_directory(
    root: Path,
    document_service,
    validation: _ValidationCollector,
) -> list[CVEvaluationCase]:
    resumes_directory = root / "cv" / "resumes"
    ground_truth_directories = [
        directory
        for directory in (
            root / "cv" / "ground_truth",
            root / "cv" / "ground-truth",
        )
        if directory.is_dir()
    ]
    if not resumes_directory.is_dir():
        validation.issue("cv", "missing_file")
        return []
    if not ground_truth_directories:
        validation.issue("cv", "missing_ground_truth")

    ground_truth_paths = sorted(
        {
            path
            for directory in ground_truth_directories
            for path in directory.rglob("*.json")
        },
        key=lambda path: path.as_posix().casefold(),
    )
    labels_by_stem: dict[str, list[tuple[Path, dict[str, Any]]]] = defaultdict(list)
    label_ids: Counter[str] = Counter()
    for label_path in ground_truth_paths:
        try:
            raw = json.loads(label_path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            validation.issue("cv", "invalid_json")
            continue
        if not isinstance(raw, dict):
            validation.issue("cv", "invalid_metadata")
            continue
        label_id = raw.get("cv_id")
        if not isinstance(label_id, str) or not label_id.strip():
            validation.issue("cv", "invalid_metadata")
            continue
        label_ids[label_id.strip().casefold()] += 1
        labels_by_stem[label_path.stem.casefold()].append((label_path, raw))

    duplicate_label_ids = sum(count - 1 for count in label_ids.values() if count > 1)
    validation.issue("cv", "duplicate_id", duplicate_label_ids)

    resume_paths = sorted(
        (path for path in resumes_directory.iterdir() if path.is_file()),
        key=lambda path: path.name.casefold(),
    )
    resume_stems = {path.stem.casefold() for path in resume_paths}
    orphan_labels = sum(
        len(labels)
        for stem, labels in labels_by_stem.items()
        if stem not in resume_stems
    )
    validation.issue("cv", "broken_file_reference", orphan_labels)

    cases: list[CVEvaluationCase] = []
    for resume_path in resume_paths:
        validation.register("cv")
        suffix = resume_path.suffix.lower()
        if suffix not in _SUPPORTED_RESUME_FORMATS:
            validation.invalid("cv", "unsupported_resume_format")
            continue
        labels = labels_by_stem.get(resume_path.stem.casefold(), [])
        if not labels:
            validation.invalid("cv", "missing_ground_truth")
            continue
        if len(labels) != 1:
            validation.invalid("cv", "duplicate_id", "invalid_metadata")
            continue
        try:
            expected_skills, expected_fields = _convert_ground_truth(labels[0][1])
        except (TypeError, ValueError, ValidationError):
            validation.invalid("cv", "invalid_metadata")
            continue

        started = time.perf_counter()
        try:
            if document_service is None:
                raise RuntimeError("A document service is required for Resume files.")
            resume_text = document_service.extract_text(
                str(resume_path),
                resume_path.name,
            ).strip()
            if not resume_text:
                raise ValueError("Resume extraction produced no text.")
        except Exception:
            document_format = suffix.removeprefix(".")
            validation.parsing_failures[document_format] += 1
            validation.invalid("cv", "parsing_failure")
            continue
        processing_ms = (time.perf_counter() - started) * 1000
        cases.append(
            CVEvaluationCase(
                case_id=_safe_case_id("cv", resume_path.relative_to(root)),
                resume_text=resume_text,
                expected_skills=tuple(expected_skills),
                expected_profile_fields=expected_fields,
                document_processing_ms=processing_ms,
                document_format=suffix.removeprefix("."),  # type: ignore[arg-type]
            )
        )
        validation.valid("cv")
    return cases


def _convert_ground_truth(raw: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    skills = raw.get("skills")
    experiences = raw.get("experiences", raw.get("experience"))
    projects = raw.get("projects")
    education = raw.get("education")
    if not isinstance(skills, list) or not all(isinstance(value, str) for value in skills):
        raise ValueError("Ground truth skills must be a string list.")
    if not isinstance(experiences, list):
        raise ValueError("Ground truth experience must be a list.")
    if not isinstance(projects, list) or not isinstance(education, list):
        raise ValueError("Ground truth projects and education must be lists.")

    converted_experiences = [_convert_experience(value) for value in experiences]
    converted_projects = [_convert_project(value) for value in projects]
    converted_education = [_convert_education(value) for value in education]
    role = raw.get("recent_role", raw.get("role"))
    if not isinstance(role, str) or not role.strip():
        role = next(
            (
                experience["title"]
                for experience in converted_experiences
                if experience["title"]
            ),
            None,
        )
    if not role:
        raise ValueError("Ground truth has no explicit role annotation.")
    return (
        [skill.strip() for skill in skills if skill.strip()],
        {
            "recent_role": role.strip(),
            "experiences": converted_experiences,
            "projects": converted_projects,
            "education": converted_education,
        },
    )


def _convert_experience(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Experience annotation must be an object.")
    description = value.get("description", "")
    if isinstance(description, list):
        description = "\n".join(str(item).strip() for item in description if str(item).strip())
    if not isinstance(description, str):
        raise ValueError("Experience description must be text or a text list.")
    technologies = value.get("technologies", [])
    if not isinstance(technologies, list):
        technologies = []
    return {
        "company": str(value.get("company", "")).strip(),
        "title": str(value.get("title", value.get("position", ""))).strip(),
        "start_date": _optional_text(value.get("start_date")),
        "end_date": _optional_text(value.get("end_date")),
        "description": description,
        "technologies": [str(item).strip() for item in technologies if str(item).strip()],
    }


def _convert_project(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Project annotation must be an object.")
    technologies = value.get("technologies", [])
    if not isinstance(technologies, list):
        raise ValueError("Project technologies must be a list.")
    return {
        "name": str(value.get("name", "")).strip(),
        "description": str(value.get("description", "")).strip(),
        "technologies": [str(item).strip() for item in technologies if str(item).strip()],
        "role": _optional_text(value.get("role")),
    }


def _convert_education(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Education annotation must be an object.")
    return {
        "institution": str(value.get("institution", value.get("school", ""))).strip(),
        "degree": _optional_text(value.get("degree")),
        "field_of_study": _optional_text(
            value.get("field_of_study", value.get("major"))
        ),
        "start_date": _optional_text(value.get("start_date")),
        "end_date": _optional_text(value.get("end_date")),
    }


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _load_stt_directory(
    root: Path,
    validation: _ValidationCollector,
) -> list[STTEvaluationCase]:
    stt_directory = root / "stt"
    audio_directory = stt_directory / "audio"
    metadata_path = stt_directory / "metadata.csv"
    if not metadata_path.is_file():
        validation.issue("stt", "missing_file")
        if audio_directory.is_dir():
            for path in audio_directory.rglob("*"):
                if not path.is_file():
                    continue
                validation.register("stt")
                validation.invalid("stt", "missing_transcript")
        return []
    try:
        with metadata_path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            rows = list(reader)
            fieldnames = set(reader.fieldnames or [])
    except (OSError, UnicodeError, csv.Error):
        validation.register("stt")
        validation.invalid("stt", "invalid_metadata")
        return []
    if not {"filename", "text"}.issubset(fieldnames):
        validation.register("stt", len(rows) or 1)
        for _ in range(len(rows) or 1):
            validation.invalid("stt", "invalid_metadata")
        return []

    filenames = [(row.get("filename") or "").strip().casefold() for row in rows]
    duplicate_names = Counter(name for name in filenames if name)
    validation.issue(
        "stt",
        "duplicate_id",
        sum(count - 1 for count in duplicate_names.values() if count > 1),
    )
    referenced_audio: set[Path] = set()
    cases: list[STTEvaluationCase] = []
    for row, normalized_filename in zip(rows, filenames, strict=True):
        validation.register("stt")
        problems: list[str] = []
        filename = (row.get("filename") or "").strip()
        transcript = (row.get("text") or "").strip()
        if not filename:
            problems.append("invalid_metadata")
        if not transcript:
            problems.append("empty_transcript")
        if normalized_filename and duplicate_names[normalized_filename] > 1:
            problems.append("duplicate_id")
        duration_value = (row.get("duration") or "").strip()
        if duration_value:
            try:
                if float(duration_value) < 0:
                    raise ValueError
            except ValueError:
                problems.append("invalid_metadata")

        audio_path: Path | None = None
        if filename:
            try:
                audio_path = _resolve_under(audio_directory, filename)
            except ValueError:
                problems.append("broken_file_reference")
            else:
                if not audio_path.is_file():
                    problems.append("broken_file_reference")
                else:
                    referenced_audio.add(audio_path)
                    if audio_path.suffix.lower() != ".wav":
                        problems.append("unsupported_audio_format")

        audio_chunks: tuple[bytes, ...] = ()
        audio_duration = 0.0
        if audio_path is not None and audio_path.is_file() and not problems:
            try:
                audio_chunks, audio_duration = _read_wav_chunks(audio_path)
            except wave.Error:
                problems.append("broken_audio_file")
            except ValueError:
                problems.append("unsupported_audio_format")
            except OSError:
                problems.append("broken_file_reference")
        if problems:
            validation.invalid("stt", *problems)
            continue
        category = _classify_transcript(transcript, row.get("language"))
        cases.append(
            STTEvaluationCase(
                case_id=_safe_case_id("stt", Path(filename)),
                audio_chunks=audio_chunks,
                reference_text=transcript,
                category=category,
                audio_duration_seconds=audio_duration,
                transcript_word_count=len(transcript.split()),
            )
        )
        validation.valid("stt")

    if audio_directory.is_dir():
        for audio_path in sorted(
            (path.resolve() for path in audio_directory.rglob("*") if path.is_file()),
            key=lambda path: path.as_posix().casefold(),
        ):
            if audio_path not in referenced_audio:
                validation.register("stt")
                validation.invalid("stt", "missing_transcript")
    return cases


def _read_wav_chunks(
    audio_path: Path,
    *,
    chunk_duration_ms: int = 100,
) -> tuple[tuple[bytes, ...], float]:
    with wave.open(str(audio_path), "rb") as audio:
        channels = audio.getnchannels()
        sample_width = audio.getsampwidth()
        sample_rate = audio.getframerate()
        compression = audio.getcomptype()
        frame_count = audio.getnframes()
        pcm = audio.readframes(frame_count)
    if channels != 1 or sample_width != 2 or compression != "NONE":
        raise ValueError("Only mono uncompressed PCM16 WAV is supported.")
    if sample_rate < 8_000 or sample_rate > 48_000:
        raise ValueError("WAV sample rate is outside the supported range.")
    if sample_rate != 16_000:
        pcm, _ = audioop.ratecv(pcm, 2, 1, sample_rate, 16_000, None)
    chunk_size = max(2, 16_000 * 2 * chunk_duration_ms // 1000)
    chunks = tuple(
        pcm[offset : offset + chunk_size]
        for offset in range(0, len(pcm), chunk_size)
        if pcm[offset : offset + chunk_size]
    )
    return chunks, frame_count / sample_rate


def _classify_transcript(text: str, metadata_language: str | None) -> Literal[
    "vi", "en", "mixed_technical"
]:
    folded = text.casefold()
    if any(term in folded for term in _TECHNICAL_TERMS):
        return "mixed_technical"
    language = (metadata_language or "").strip().casefold()
    if language.startswith("vi"):
        return "vi"
    if language.startswith("en"):
        return "en"
    return "vi" if any(character in _VIETNAMESE_CHARACTERS for character in folded) else "en"


def _display_category(category: str) -> str:
    return {
        "vi": "Vietnamese",
        "en": "English",
        "mixed_technical": "Mixed technical",
    }.get(category, category)


def _load_tts_directory(
    root: Path,
    validation: _ValidationCollector,
) -> tuple[list[TTSEvaluationCase], bool]:
    rows, synthetic = _read_case_file(root / "tts" / "cases.json", "tts", validation)
    cases: list[TTSEvaluationCase] = []
    ids = _duplicate_ids(rows)
    validation.issue("tts", "duplicate_id", ids[1])
    for index, row in enumerate(rows):
        validation.register("tts")
        case_id = row.get("case_id")
        text = row.get("text")
        problems = []
        if not isinstance(case_id, str) or not case_id.strip():
            problems.append("invalid_metadata")
        elif ids[0][case_id.strip().casefold()] > 1:
            problems.append("duplicate_id")
        if not isinstance(text, str) or not text.strip():
            problems.append("invalid_metadata")
        if problems:
            validation.invalid("tts", *problems)
            continue
        cases.append(TTSEvaluationCase(case_id=case_id, text=text.strip()))
        validation.valid("tts")
    return cases, synthetic


def _load_question_directory(
    root: Path,
    validation: _ValidationCollector,
) -> tuple[list[QuestionEvaluationCase], bool]:
    rows, synthetic = _read_case_file(
        root / "llm" / "interview_cases.json", "llm", validation
    )
    cases: list[QuestionEvaluationCase] = []
    ids = _duplicate_ids(rows)
    validation.issue("llm", "duplicate_id", ids[1])
    difficulty_by_level = {
        "intern": "easy",
        "junior": "easy",
        "middle": "medium",
        "senior": "hard",
    }
    for row in rows:
        validation.register("llm")
        try:
            case_id = _required_id(row, ids[0])
            profile = CandidateProfile.model_validate(row.get("candidate_profile"))
            topics = row.get("expected_topics")
            if not isinstance(topics, list) or not topics or not all(
                isinstance(topic, str) and topic.strip() for topic in topics
            ):
                raise ValueError
            expected_level = row.get("expected_level")
            if expected_level not in difficulty_by_level:
                raise ValueError
            question_text = row.get("generated_question")
            if not isinstance(question_text, str) or not question_text.strip():
                raise ValueError
            language = row.get("language", "en")
            config = InterviewConfig(
                mode="text",
                language=language,
                experience_level=expected_level,
            )
            difficulty = difficulty_by_level[expected_level]
            interview_round = InterviewRound(
                round_id=case_id,
                topic=topics[0].strip(),
                objective="Assess the expected benchmark topics.",
                difficulty=difficulty,
                recommended_question_areas=[topic.strip() for topic in topics],
                target_skills=[topic.strip() for topic in topics],
            )
            generated_question = InterviewQuestion(
                question=question_text.strip(),
                language=language,
                topic=topics[0].strip(),
                difficulty=difficulty,
            )
        except (TypeError, ValueError, ValidationError):
            validation.invalid("llm", "invalid_metadata")
            continue
        cases.append(
            QuestionEvaluationCase(
                case_id=case_id,
                candidate_profile=profile,
                interview_round=interview_round,
                interview_config=config,
                generated_question=generated_question,
            )
        )
        validation.valid("llm")
    return cases, synthetic


def _load_evaluator_directory(
    root: Path,
    validation: _ValidationCollector,
) -> tuple[list[EvaluatorEvaluationCase], bool]:
    rows, synthetic = _read_case_file(
        root / "evaluator" / "human_labels.json", "evaluator", validation
    )
    cases: list[EvaluatorEvaluationCase] = []
    ids = _duplicate_ids(rows)
    validation.issue("evaluator", "duplicate_id", ids[1])
    for row in rows:
        validation.register("evaluator")
        try:
            case_id = _required_id(row, ids[0])
            question_text = row.get("question")
            answer = row.get("candidate_answer")
            feedback_category = row.get("human_feedback_category")
            score = float(row.get("human_score"))
            if not isinstance(question_text, str) or not question_text.strip():
                raise ValueError
            if not isinstance(answer, str) or not answer.strip():
                raise ValueError
            if not isinstance(feedback_category, str) or not feedback_category.strip():
                raise ValueError
            if not 0.0 <= score <= 10.0:
                raise ValueError
            expected_points = row.get("expected_answer_points", [])
            if not isinstance(expected_points, list) or not all(
                isinstance(point, str) for point in expected_points
            ):
                raise ValueError
            topic = str(row.get("topic", "Technical fundamentals")).strip()
            difficulty = row.get("difficulty", "medium")
            language = row.get("language", "en")
            profile = CandidateProfile(
                name="Candidate",
                skills=[topic] if topic else [],
            )
            question = InterviewQuestion(
                question=question_text.strip(),
                language=language,
                topic=topic,
                difficulty=difficulty,
                expected_answer_points=expected_points,
            )
            config = InterviewConfig(
                mode="text",
                language=language,
                experience_level=row.get("expected_level", "middle"),
            )
        except (TypeError, ValueError, ValidationError):
            validation.invalid("evaluator", "invalid_metadata")
            continue
        cases.append(
            EvaluatorEvaluationCase(
                case_id=case_id,
                candidate_profile=profile,
                interview_question=question,
                candidate_answer=answer.strip(),
                interview_config=config,
                human_score=score,
                human_feedback_category=feedback_category.strip(),
            )
        )
        validation.valid("evaluator")
    return cases, synthetic


def _load_voice_directory(
    root: Path,
    validation: _ValidationCollector,
) -> tuple[list[VoiceTurnObservation], bool]:
    rows, synthetic = _read_case_file(
        root / "voice" / "latency_samples.json", "voice", validation
    )
    observations: list[VoiceTurnObservation] = []
    ids = _duplicate_ids(rows)
    validation.issue("voice", "duplicate_id", ids[1])
    timestamp_fields = (
        "speech_end_time",
        "stt_final_time",
        "evaluation_start",
        "question_first_token",
        "tts_first_audio",
    )
    for row in rows:
        validation.register("voice")
        try:
            _required_id(row, ids[0])
            success = row.get("success", True)
            if not isinstance(success, bool):
                raise ValueError
            if not success:
                observation = VoiceTurnObservation(total_latency_ms=None, success=False)
            elif row.get("total_latency_ms") is not None:
                latency_ms = float(row["total_latency_ms"])
                if latency_ms < 0:
                    raise ValueError
                observation = VoiceTurnObservation(
                    total_latency_ms=latency_ms,
                    success=True,
                )
            else:
                timestamps = [_parse_timestamp(row.get(field)) for field in timestamp_fields]
                if any(
                    later < earlier
                    for earlier, later in zip(timestamps, timestamps[1:], strict=False)
                ):
                    raise ValueError
                observation = VoiceTurnObservation(
                    total_latency_ms=(timestamps[-1] - timestamps[0]) * 1000,
                    success=True,
                )
        except (TypeError, ValueError):
            validation.invalid("voice", "invalid_metadata")
            continue
        observations.append(observation)
        validation.valid("voice")
    return observations, synthetic


def _read_case_file(
    path: Path,
    section: str,
    validation: _ValidationCollector,
) -> tuple[list[dict[str, Any]], bool]:
    if not path.is_file():
        validation.issue(section, "missing_file")
        return [], False
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        validation.register(section)
        validation.invalid(section, "invalid_json")
        return [], False
    synthetic = False
    if isinstance(payload, dict):
        synthetic = bool(payload.get("synthetic", False))
        payload = payload.get("cases", payload.get("samples"))
    if not isinstance(payload, list):
        validation.register(section)
        validation.invalid(section, "invalid_metadata")
        return [], synthetic
    rows: list[dict[str, Any]] = []
    invalid_rows = 0
    for value in payload:
        if isinstance(value, dict):
            rows.append(value)
        else:
            invalid_rows += 1
    for _ in range(invalid_rows):
        validation.register(section)
        validation.invalid(section, "invalid_metadata")
    return rows, synthetic


def _duplicate_ids(rows: list[dict[str, Any]]) -> tuple[Counter[str], int]:
    ids = Counter(
        str(row.get("case_id", "")).strip().casefold()
        for row in rows
        if str(row.get("case_id", "")).strip()
    )
    return ids, sum(count - 1 for count in ids.values() if count > 1)


def _required_id(row: dict[str, Any], ids: Counter[str]) -> str:
    case_id = row.get("case_id")
    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError("case_id is required")
    if ids[case_id.strip().casefold()] > 1:
        raise ValueError("case_id is duplicated")
    return case_id.strip()


def _parse_timestamp(value: Any) -> float:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str) and value.strip():
        normalized = value.strip().replace("Z", "+00:00")
        return datetime.fromisoformat(normalized).timestamp()
    raise ValueError("A timestamp is required.")


def _safe_case_id(namespace: str, path: Path) -> str:
    digest = hashlib.sha256(path.as_posix().casefold().encode("utf-8")).hexdigest()[:16]
    return f"{namespace}-{digest}"


def _resolve_under(base_directory: Path, relative_path: str) -> Path:
    base = base_directory.resolve()
    path = (base / relative_path).resolve()
    if path != base and base not in path.parents:
        raise ValueError("Evaluation fixture path escapes its dataset directory.")
    return path


def _load_manifest_dataset(path: Path, document_service) -> EvaluationDataset:
    manifest = EvaluationManifest.model_validate_json(path.read_text(encoding="utf-8"))
    base_directory = path.parent

    cv_cases: list[CVEvaluationCase] = []
    for case in manifest.cv_cases:
        resume_path = _resolve_file(base_directory, case.resume_path)
        started = time.perf_counter()
        if resume_path.suffix.lower() == ".txt":
            resume_text = resume_path.read_text(encoding="utf-8")
        else:
            resume_text = document_service.extract_text(
                str(resume_path),
                resume_path.name,
            )
        suffix = resume_path.suffix.lower().removeprefix(".")
        cv_cases.append(
            CVEvaluationCase(
                case_id=case.case_id,
                resume_text=resume_text,
                expected_skills=tuple(case.expected_skills),
                expected_profile_fields=case.expected_profile_fields,
                document_processing_ms=(time.perf_counter() - started) * 1000,
                document_format=suffix if suffix in {"pdf", "docx", "txt"} else "txt",
            )
        )

    stt_cases = [_load_manifest_stt_case(base_directory, case) for case in manifest.stt_cases]
    validation = DatasetValidationSummary(
        sections={
            "cv": DatasetSectionValidation(
                total_samples=len(cv_cases), valid_samples=len(cv_cases)
            ),
            "stt": DatasetSectionValidation(
                total_samples=len(stt_cases), valid_samples=len(stt_cases)
            ),
        }
    )
    summary = BenchmarkDatasetSummary(
        total_cv_samples=len(cv_cases),
        valid_cv_samples=len(cv_cases),
        total_speech_samples=len(stt_cases),
        valid_speech_samples=len(stt_cases),
        language_distribution=dict(
            Counter(_display_category(case.category) for case in stt_cases)
        ),
        average_audio_duration_seconds=(
            sum(case.audio_duration_seconds for case in stt_cases) / len(stt_cases)
            if stt_cases
            else None
        ),
        average_transcript_length_words=(
            sum(case.transcript_word_count for case in stt_cases) / len(stt_cases)
            if stt_cases
            else None
        ),
    )
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
        summary=summary,
        validation=validation,
    )


def _load_manifest_stt_case(
    base_directory: Path,
    case: STTCaseManifest,
) -> STTEvaluationCase:
    audio_path = _resolve_file(base_directory, case.audio_path)
    reference_path = _resolve_file(base_directory, case.reference_text_path)
    chunks, duration = _read_wav_chunks(
        audio_path,
        chunk_duration_ms=case.chunk_duration_ms,
    )
    reference_text = reference_path.read_text(encoding="utf-8").strip()
    return STTEvaluationCase(
        case_id=case.case_id,
        audio_chunks=chunks,
        reference_text=reference_text,
        category=case.category,
        audio_duration_seconds=duration,
        transcript_word_count=len(reference_text.split()),
    )


def _resolve_file(base_directory: Path, relative_path: str) -> Path:
    path = _resolve_under(base_directory, relative_path)
    if not path.is_file():
        raise ValueError("Evaluation fixture file was not found.")
    return path

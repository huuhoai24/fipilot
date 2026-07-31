"""Central dependency construction for gateway routes and services."""

from __future__ import annotations

from functools import lru_cache

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.settings import Settings, get_settings
from database import get_db
from shared.schemas import CurrentUser


_bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache
def get_app_settings() -> Settings:
    return get_settings()


def get_sqlite_repository(db: Session, settings: Settings | None = None):
    from infrastructure.repositories.sqlite import SQLiteInterviewRepository

    active_settings = settings or get_app_settings()
    return SQLiteInterviewRepository(
        db,
        auth_enabled=active_settings.auth_enabled,
        dev_user_id=active_settings.auth_dev_user_id,
    )


@lru_cache
def get_firestore_repository(
    project: str,
    database: str,
    users_collection: str,
    candidates_collection: str,
    interviews_collection: str,
):
    from google.cloud import firestore
    from infrastructure.repositories.firestore import FirestoreRepository

    client = firestore.Client(project=project, database=database)
    return FirestoreRepository(
        client,
        users_collection=users_collection,
        candidates_collection=candidates_collection,
        interviews_collection=interviews_collection,
    )


def build_interview_repository(
    settings: Settings,
    *,
    db: Session | None = None,
    firestore_client=None,
):
    if settings.repository_backend == "sqlite":
        if db is None:
            raise RuntimeError("A database session is required for the SQLite repository")
        return get_sqlite_repository(db, settings)

    from infrastructure.repositories.firestore import FirestoreRepository

    if firestore_client is not None:
        return FirestoreRepository(
            firestore_client,
            users_collection=settings.firestore_users_collection,
            candidates_collection=settings.firestore_candidates_collection,
            interviews_collection=settings.firestore_interviews_collection,
        )
    if not settings.google_cloud_project:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is required for Firestore")
    return get_firestore_repository(
        settings.google_cloud_project,
        settings.firestore_database,
        settings.firestore_users_collection,
        settings.firestore_candidates_collection,
        settings.firestore_interviews_collection,
    )


def get_interview_repository(
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_app_settings),
):
    return build_interview_repository(settings, db=db)


@lru_cache
def get_llm_service():
    from infrastructure.llm.vertex_gemini import VertexGeminiService

    return VertexGeminiService(settings=get_app_settings())


@lru_cache
def get_resume_llm_service():
    from infrastructure.llm.vertex_gemini import RetryConfig, VertexGeminiService

    settings = get_app_settings()
    resume_settings = settings.model_copy(
        update={
            "google_cloud": settings.google_cloud.model_copy(
                update={"location": settings.gemini_resume_location}
            ),
            "llm_routing": settings.llm_routing.model_copy(
                update={"simple_model": settings.gemini_resume_model}
            ),
        }
    )
    return VertexGeminiService(
        settings=resume_settings,
        retry_config=RetryConfig(max_attempts=1),
    )


@lru_cache
def get_question_streaming_service():
    from services.question_generator.streaming_service import (
        QuestionStreamingService,
    )

    return QuestionStreamingService(llm_service=get_llm_service())


@lru_cache
def get_streaming_tts_service():
    settings = get_app_settings()
    if settings.speech_service_url:
        from infrastructure.speech.remote import RemoteStreamingTTS

        return RemoteStreamingTTS(
            service_url=settings.speech_service_url,
            service_token=settings.speech_service_token,
        )

    from infrastructure.speech.tts.vieneu import VieneuStreamingTTS

    return VieneuStreamingTTS(
        mode=settings.tts_mode,
        device=settings.tts_device,
        voice=settings.tts_voice,
        sample_rate=settings.tts_sample_rate,
        frame_duration_ms=settings.tts_frame_duration_ms,
    )


@lru_cache
def get_question_speech_streamer_factory():
    from services.voice_session.question_speech import (
        QuestionSpeechStreamerFactory,
    )

    settings = get_app_settings()
    return QuestionSpeechStreamerFactory(
        tts_service=get_streaming_tts_service(),
        queue_size=settings.tts_queue_size,
        chunk_min_words=settings.tts_chunk_min_words,
        chunk_max_chars=settings.tts_chunk_max_chars,
    )


@lru_cache
def get_auth_service():
    from infrastructure.auth import FirebaseAuthService

    return FirebaseAuthService(settings=get_app_settings())


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    settings: Settings = Depends(get_app_settings),
    auth_service=Depends(get_auth_service),
) -> CurrentUser:
    if not settings.auth_enabled:
        return CurrentUser(
            uid=settings.auth_dev_user_id,
            name="Local Development User",
            email_verified=False,
            claims={"auth_provider": "development"},
        )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Bearer authentication is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return auth_service.verify_id_token(credentials.credentials)
    except Exception as error:
        from core.exceptions import AuthenticationError

        if not isinstance(error, AuthenticationError):
            raise
        raise HTTPException(
            status_code=401,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        ) from error


def get_document_service():
    from infrastructure.documents import DocumentService

    return DocumentService()


@lru_cache
def get_audio_pipeline_factory():
    settings = get_app_settings()
    if settings.speech_service_url:
        from infrastructure.speech.remote import RemoteAudioPipelineFactory

        return RemoteAudioPipelineFactory(
            service_url=settings.speech_service_url,
            service_token=settings.speech_service_token,
            queue_size=settings.stt_audio_queue_size,
        )

    from infrastructure.speech.stt.faster_whisper import FasterWhisperSTTFactory
    from services.voice_session.audio_pipeline import (
        AudioPipelineFactory,
        SileroVADFactory,
    )

    return AudioPipelineFactory(
        stt_factory=FasterWhisperSTTFactory(
            model_name=settings.stt_model,
            device=settings.stt_device,
            compute_type=settings.stt_compute_type,
            language=settings.stt_language,
            partial_interval_ms=settings.stt_partial_interval_ms,
            vocabulary_profile=settings.stt_vocabulary_profile,
            custom_hotwords=settings.stt_hotwords,
            partial_max_audio_ms=settings.stt_partial_max_audio_ms,
            final_beam_size=settings.stt_final_beam_size,
        ),
        vad_factory=SileroVADFactory(
            threshold=settings.vad_threshold,
            min_silence_ms=settings.vad_min_silence_ms,
            speech_pad_ms=settings.vad_speech_pad_ms,
        ),
        queue_size=settings.stt_audio_queue_size,
    )


@lru_cache
def get_voice_session_manager():
    from services.voice_session.manager import VoiceSessionManager

    settings = get_app_settings()
    return VoiceSessionManager(
        max_chunk_bytes=settings.max_voice_chunk_bytes,
        max_session_bytes=settings.max_voice_session_bytes,
        pipeline_factory=get_audio_pipeline_factory(),
    )


def get_resume_agent():
    from services.profile_scanner.agent import ResumeAgent

    return ResumeAgent(llm_service=get_resume_llm_service())


def get_profile_scanner_service():
    from services.profile_scanner.service import ProfileScannerService

    return ProfileScannerService(agent=get_resume_agent())


def get_interview_planner_agent():
    from services.interview_planner.agent import InterviewPlannerAgent

    return InterviewPlannerAgent(llm_service=get_llm_service())


def get_question_generator_agent():
    from services.question_generator.agent import QuestionGeneratorAgent

    return QuestionGeneratorAgent(llm_service=get_llm_service())


def get_evaluator_agent():
    from services.answer_evaluator.agent import EvaluatorAgent

    return EvaluatorAgent(
        llm_service=get_llm_service(),
        task_type=get_app_settings().evaluator_task_type,
    )


def get_decision_service():
    from orchestrator.decision_service import InterviewDecisionService

    return InterviewDecisionService()


def get_interview_orchestrator():
    from orchestrator.interview_orchestrator import InterviewOrchestrator
    from orchestrator.memory_service import InterviewMemoryService
    from orchestrator.follow_up_service import FollowUpSelectionService

    return InterviewOrchestrator(
        planner_agent=get_interview_planner_agent(),
        question_generator_agent=get_question_generator_agent(),
        evaluator_agent=get_evaluator_agent(),
        decision_service=get_decision_service(),
        memory_service=InterviewMemoryService(),
        follow_up_service=FollowUpSelectionService(),
    )


@lru_cache
def get_interview_preparation_cache():
    from services.interview_preparation import InterviewPreparationCache

    settings = get_app_settings()
    return InterviewPreparationCache(
        ttl_seconds=settings.interview_preparation_ttl_seconds,
        max_entries=settings.interview_preparation_max_entries,
    )


def get_voice_answer_submission_service(
    repository=Depends(get_interview_repository),
    orchestrator=Depends(get_interview_orchestrator),
):
    from services.voice_session.answer_service import VoiceAnswerSubmissionService

    return VoiceAnswerSubmissionService(
        repository=repository,
        orchestrator=orchestrator,
    )


@lru_cache
def get_report_generator_agent():
    from services.report_generator.agent import ReportGeneratorAgent

    return ReportGeneratorAgent(llm_service=get_llm_service())


def get_report_service(repository=Depends(get_interview_repository)):
    from services.report_generator.service import ReportService

    return ReportService(agent=get_report_generator_agent(), repository=repository)

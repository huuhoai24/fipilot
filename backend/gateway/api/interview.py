from __future__ import annotations

from datetime import datetime, timezone
import time

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core.dependencies import (
    get_current_user,
    get_interview_orchestrator,
    get_interview_preparation_cache,
    get_interview_repository,
)
from core.logging import get_logger
from core.performance import log_duration, timed_stage
from infrastructure.repositories import (
    InterviewSessionRecord,
    SQLiteInterviewRepository,
)
from orchestrator.interview_orchestrator import InterviewOrchestrator
from services.interview_preparation import InterviewPreparationCache
from shared.schemas import (
    CurrentUser,
    InterviewConfig,
    InterviewPlan,
    InterviewSessionState,
    InterviewStatus,
    PersistedCandidateProfile,
)
from orchestrator.conversation_flow import (
    answer_opening,
    begin_text_conversation,
    enter_closing_if_finished,
)


router = APIRouter(prefix="/api/v2/interview", tags=["v2-interview"])
logger = get_logger(__name__)


class InterviewStartRequest(BaseModel):
    candidate_id: str
    interview_config: InterviewConfig


class InterviewAnswerRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=12000)


class InterviewSessionResponse(BaseModel):
    session_id: str
    started_at: datetime | None = None
    state: InterviewSessionState


class InterviewPreparationResponse(BaseModel):
    status: str = "ready"
    profile_version: int


@router.post("/prepare", response_model=InterviewPreparationResponse)
async def prepare_interview(
    request: InterviewStartRequest,
    repository: SQLiteInterviewRepository = Depends(get_interview_repository),
    orchestrator: InterviewOrchestrator = Depends(get_interview_orchestrator),
    preparation_cache: InterviewPreparationCache = Depends(
        get_interview_preparation_cache
    ),
    current_user: CurrentUser = Depends(get_current_user),
) -> InterviewPreparationResponse:
    total_started_at = time.perf_counter()
    with timed_stage(
        logger,
        "interview.load_candidate",
        stage="prepare_candidate_load",
    ):
        candidate_profile = repository.get_candidate_profile(
            request.candidate_id,
            user_id=current_user.uid,
        )
    if candidate_profile is None:
        raise HTTPException(status_code=404, detail="Candidate profile not found.")

    key = preparation_cache.key_for(
        current_user.uid,
        candidate_profile,
        request.interview_config,
    )
    with timed_stage(logger, "interview.preparation", stage="prepare_request"):
        await _get_or_create_blueprint(
            repository,
            orchestrator,
            preparation_cache,
            key,
            candidate_profile,
            request.interview_config,
            current_user.uid,
        )
    log_duration(logger, "interview.total_prepare", total_started_at)
    return InterviewPreparationResponse(
        profile_version=candidate_profile.profile_version,
    )


@router.post("/start", response_model=InterviewSessionResponse)
async def start_interview(
    request: InterviewStartRequest,
    repository: SQLiteInterviewRepository = Depends(get_interview_repository),
    orchestrator: InterviewOrchestrator = Depends(get_interview_orchestrator),
    preparation_cache: InterviewPreparationCache = Depends(
        get_interview_preparation_cache
    ),
    current_user: CurrentUser = Depends(get_current_user),
) -> InterviewSessionResponse:
    total_started_at = time.perf_counter()
    with timed_stage(
        logger,
        "interview.load_candidate",
        stage="start_candidate_load",
    ):
        candidate_profile = repository.get_candidate_profile(
            request.candidate_id, user_id=current_user.uid
        )
    if candidate_profile is None:
        raise HTTPException(status_code=404, detail="Candidate profile not found.")

    key = preparation_cache.key_for(
        current_user.uid,
        candidate_profile,
        request.interview_config,
    )
    with timed_stage(logger, "interview.preparation", stage="start_request"):
        interview_plan = await _get_or_create_blueprint(
            repository,
            orchestrator,
            preparation_cache,
            key,
            candidate_profile,
            request.interview_config,
            current_user.uid,
        )
    with timed_stage(logger, "interview.question_generation", stage="session_first_question"):
        state = await orchestrator.start_interview(
            candidate_profile,
            request.interview_config,
            interview_plan=interview_plan,
        )
    state = begin_text_conversation(state)
    with timed_stage(logger, "interview.persistence", stage="session_create"):
        session = repository.create_session(
            request.candidate_id,
            role=candidate_profile.specialization,
            level=request.interview_config.experience_level,
            language=request.interview_config.language,
            user_id=current_user.uid,
        )
        _save_state(repository, session.session_id, state, current_user.uid)

        if state.current_turn is not None:
            repository.save_turn(
                session.session_id, state.current_turn, user_id=current_user.uid
            )

    log_duration(
        logger,
        "interview.total_start",
        total_started_at,
        session_id=session.session_id,
    )
    return InterviewSessionResponse(
        session_id=session.session_id,
        started_at=_utc_timestamp(session.started_at),
        state=state,
    )


import asyncio

_session_locks: dict[str, asyncio.Lock] = {}


def _get_session_lock(session_id: str) -> asyncio.Lock:
    if session_id not in _session_locks:
        _session_locks[session_id] = asyncio.Lock()
    return _session_locks[session_id]


@router.post("/{session_id}/answer", response_model=InterviewSessionResponse)
async def submit_answer(
    session_id: str,
    request: InterviewAnswerRequest,
    repository: SQLiteInterviewRepository = Depends(get_interview_repository),
    orchestrator: InterviewOrchestrator = Depends(get_interview_orchestrator),
    current_user: CurrentUser = Depends(get_current_user),
) -> InterviewSessionResponse:
    total_started_at = time.perf_counter()
    async with _get_session_lock(session_id):
        with timed_stage(
            logger,
            "answer.load_session",
            stage="session_state_load",
            session_id=session_id,
        ):
            session = _load_session(repository, session_id, current_user.uid)
            state = _state_from_session(session)

        # If already answered or closed by a concurrent click, return current state
        if state.current_turn is None or state.phase == "closing":
            return InterviewSessionResponse(
                session_id=session_id,
                started_at=_utc_timestamp(session.started_at),
                state=state,
            )

        with timed_stage(
            logger,
            "answer.orchestration",
            stage="evaluation_and_next_question",
            session_id=session_id,
        ):
            updated_state = answer_opening(state, request.answer)
            if updated_state is None:
                updated_state = await orchestrator.submit_answer(state, request.answer)
                updated_state = enter_closing_if_finished(updated_state)
        with timed_stage(
            logger,
            "answer.persistence",
            stage="session_state_save",
            session_id=session_id,
        ):
            _save_state(repository, session_id, updated_state, current_user.uid)

            if updated_state.current_turn is not None:
                repository.save_turn(
                    session_id, updated_state.current_turn, user_id=current_user.uid
                )

        log_duration(
            logger,
            "answer.total",
            total_started_at,
            session_id=session_id,
        )

        return InterviewSessionResponse(
            session_id=session_id,
            started_at=_utc_timestamp(session.started_at),
            state=updated_state,
        )


@router.get("/{session_id}", response_model=InterviewSessionResponse)
async def get_interview_session(
    session_id: str,
    repository: SQLiteInterviewRepository = Depends(get_interview_repository),
    current_user: CurrentUser = Depends(get_current_user),
) -> InterviewSessionResponse:
    session = _load_session(repository, session_id, current_user.uid)
    return InterviewSessionResponse(
        session_id=session_id,
        started_at=_utc_timestamp(session.started_at),
        state=_state_from_session(session),
    )


@router.post("/{session_id}/end", response_model=InterviewSessionResponse)
async def end_interview_session(
    session_id: str,
    repository: SQLiteInterviewRepository = Depends(get_interview_repository),
    current_user: CurrentUser = Depends(get_current_user),
) -> InterviewSessionResponse:
    session = _load_session(repository, session_id, current_user.uid)
    state = _state_from_session(session)
    ended_state = state.model_copy(
        update={
            "phase": "closing",
            "current_turn": None,
            "pending_turn": None,
        }
    )
    _save_state(repository, session_id, ended_state, current_user.uid)
    return InterviewSessionResponse(
        session_id=session_id,
        started_at=_utc_timestamp(session.started_at),
        state=ended_state,
    )


def _save_state(
    repository: SQLiteInterviewRepository,
    session_id: str,
    state: InterviewSessionState,
    user_id: str,
) -> None:
    repository.update_session_state(
        session_id,
        "INTERVIEWING" if state.current_turn is not None else "ENDED",
        state.model_dump(mode="json"),
        status=(
            InterviewStatus.IN_PROGRESS.value
            if state.current_turn is not None
            else InterviewStatus.COMPLETED.value
        ),
        user_id=user_id,
    )


async def _get_or_create_blueprint(
    repository: SQLiteInterviewRepository,
    orchestrator: InterviewOrchestrator,
    preparation_cache: InterviewPreparationCache,
    artifact_key: str,
    candidate_profile: PersistedCandidateProfile,
    interview_config: InterviewConfig,
    user_id: str,
) -> InterviewPlan:
    async def load_or_create() -> InterviewPlan:
        persistent_started_at = time.perf_counter()
        plan = repository.get_interview_blueprint(
            candidate_profile.candidate_id,
            artifact_key,
            user_id=user_id,
        )
        log_duration(
            logger,
            "interview.blueprint_store",
            persistent_started_at,
            status="hit" if plan is not None else "miss",
            stage="persistent_blueprint",
            cache_hit=plan is not None,
        )
        if plan is not None:
            return plan

        plan = await orchestrator.create_plan(candidate_profile, interview_config)
        with timed_stage(
            logger,
            "interview.blueprint_persistence",
            stage="persistent_blueprint_save",
        ):
            repository.save_interview_blueprint(
                candidate_profile.candidate_id,
                artifact_key,
                plan,
                user_id=user_id,
            )
        return plan

    return await preparation_cache.get_or_create(artifact_key, load_or_create)


def _load_session(
    repository: SQLiteInterviewRepository,
    session_id: str,
    user_id: str,
) -> InterviewSessionRecord:
    session = repository.get_session(session_id, user_id=user_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Interview session not found.")
    if not session.state_payload:
        raise HTTPException(status_code=404, detail="Interview session state not found.")
    return session


def _state_from_session(session: InterviewSessionRecord) -> InterviewSessionState:
    return InterviewSessionState.model_validate(session.state_payload)


def _utc_timestamp(value: datetime | None) -> datetime | None:
    if value is None or value.tzinfo is not None:
        return value
    return value.replace(tzinfo=timezone.utc)

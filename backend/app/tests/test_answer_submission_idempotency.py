from __future__ import annotations

import asyncio
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import models
from database import Base
from infrastructure.repositories.sqlite import SQLiteInterviewRepository
from services.interview_answer_service import (
    InterviewAnswerSubmissionError,
    InterviewAnswerSubmissionService,
)
from shared.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    InterviewConfig,
    InterviewMode,
    InterviewPlan,
    InterviewQuestion,
    InterviewRound,
    InterviewSessionState,
    InterviewTurn,
)


def make_turn(turn_id: str, round_id: str = "round-1") -> InterviewTurn:
    return InterviewTurn(
        turn_id=turn_id,
        round_id=round_id,
        question=InterviewQuestion(
            question=f"Question for {turn_id}",
            language="en",
            topic="Reliability",
            difficulty="medium",
        ),
        topic="Reliability",
        difficulty="medium",
    )


def make_state(*, current_turn: InterviewTurn | None = None) -> InterviewSessionState:
    return InterviewSessionState(
        candidate_profile=CandidateProfile(name="Candidate", skills=["Python"]),
        interview_config=InterviewConfig(
            mode="voice",
            language="en",
            experience_level="middle",
            question_count=2,
        ),
        interview_plan=InterviewPlan(
            rounds=[
                InterviewRound(round_id="round-1", topic="Reliability"),
                InterviewRound(round_id="round-2", topic="Testing"),
            ]
        ),
        current_turn=current_turn or make_turn("turn-1"),
    )


class BlockingOrchestrator:
    def __init__(self) -> None:
        self.calls = 0
        self.started = asyncio.Event()
        self.release = asyncio.Event()

    async def submit_answer(self, state, answer, **_kwargs):
        self.calls += 1
        self.started.set()
        await self.release.wait()
        turn = state.current_turn.model_copy(
            update={
                "answer": answer,
                "candidate_answer": answer,
                "status": "evaluated",
                "evaluation": AnswerEvaluation(
                    turn_id=state.current_turn.turn_id,
                    overall_score=8.0,
                    feedback="Good answer.",
                ),
            }
        )
        return state.model_copy(
            update={
                "current_turn": None,
                "completed_turns": [*state.completed_turns, turn],
                "current_question_index": state.current_question_index + 1,
            }
        )


class ImmediateOrchestrator(BlockingOrchestrator):
    def __init__(self) -> None:
        super().__init__()
        self.release.set()


class AnswerSubmissionIdempotencyTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=engine)
        self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        self.repository = SQLiteInterviewRepository(self.db)
        candidate = self.repository.create_candidate("Candidate", user_id="user-1")
        session = self.repository.create_session(
            candidate.candidate_id, user_id="user-1"
        )
        self.session_id = session.session_id
        self.persist(make_state())

    def tearDown(self) -> None:
        self.db.close()

    def persist(self, state: InterviewSessionState) -> None:
        self.repository.update_session_state(
            self.session_id,
            "INTERVIEWING" if state.current_turn else "ENDED",
            state.model_dump(mode="json"),
            status="in_progress" if state.current_turn else "completed",
            user_id="user-1",
        )

    async def test_concurrent_duplicate_is_claimed_once_before_evaluator(self) -> None:
        orchestrator = BlockingOrchestrator()
        service = InterviewAnswerSubmissionService(
            repository=self.repository, orchestrator=orchestrator
        )
        first_task = asyncio.create_task(
            service.submit_answer(
                self.session_id,
                "user-1",
                "turn-1",
                "Use an idempotency claim.",
                expected_mode=InterviewMode.VOICE,
            )
        )
        await orchestrator.started.wait()

        with self.assertRaises(InterviewAnswerSubmissionError) as duplicate_error:
            await service.submit_answer(
                self.session_id,
                "user-1",
                "turn-1",
                "Use an idempotency claim.",
                expected_mode=InterviewMode.VOICE,
            )
        self.assertEqual(
            duplicate_error.exception.code, "answer_submission_in_progress"
        )
        self.assertEqual(orchestrator.calls, 1)

        orchestrator.release.set()
        first = await first_task
        state_after_first = first.state.model_dump(mode="json")
        self.assertEqual(len(first.state.completed_turns), 1)
        self.assertIsNotNone(first.state.completed_turns[0].evaluation)
        self.assertIsNone(first.state.current_turn)
        counts_after_first = (
            self.db.query(models.AnswerSubmission).count(),
            self.db.query(models.Message).count(),
            self.db.query(models.Evaluation).count(),
        )
        replay = await service.submit_answer(
            self.session_id,
            "user-1",
            "turn-1",
            "Use an idempotency claim.",
            expected_mode=InterviewMode.VOICE,
        )

        self.assertTrue(replay.replayed)
        self.assertEqual(replay.state.model_dump(mode="json"), state_after_first)
        self.assertEqual(orchestrator.calls, 1)
        self.assertEqual(
            (
                self.db.query(models.AnswerSubmission).count(),
                self.db.query(models.Message).count(),
                self.db.query(models.Evaluation).count(),
            ),
            counts_after_first,
        )

    async def test_different_answer_for_completed_turn_conflicts(self) -> None:
        orchestrator = ImmediateOrchestrator()
        service = InterviewAnswerSubmissionService(
            repository=self.repository, orchestrator=orchestrator
        )
        await service.submit_answer(
            self.session_id,
            "user-1",
            "turn-1",
            "First answer.",
            expected_mode=InterviewMode.VOICE,
        )

        with self.assertRaises(InterviewAnswerSubmissionError) as conflict:
            await service.submit_answer(
                self.session_id,
                "user-1",
                "turn-1",
                "Changed answer.",
                expected_mode=InterviewMode.VOICE,
            )

        self.assertEqual(conflict.exception.code, "answer_already_submitted")
        self.assertEqual(orchestrator.calls, 1)
        self.assertEqual(self.db.query(models.AnswerSubmission).count(), 1)

    async def test_stale_and_future_turns_are_rejected_without_claim(self) -> None:
        stale = make_turn("turn-previous").model_copy(
            update={"answer": "Already answered", "status": "evaluated"}
        )
        state = make_state(current_turn=make_turn("turn-current", "round-2"))
        self.persist(state.model_copy(update={"completed_turns": [stale]}))
        orchestrator = ImmediateOrchestrator()
        service = InterviewAnswerSubmissionService(
            repository=self.repository, orchestrator=orchestrator
        )

        for turn_id, expected_code in (
            ("turn-previous", "stale_interview_turn"),
            ("turn-future", "invalid_interview_turn"),
        ):
            with self.assertRaises(InterviewAnswerSubmissionError) as error:
                await service.submit_answer(
                    self.session_id,
                    "user-1",
                    turn_id,
                    "Should not be evaluated.",
                    expected_mode=InterviewMode.VOICE,
                )
            self.assertEqual(error.exception.code, expected_code)

        self.assertEqual(orchestrator.calls, 0)
        self.assertEqual(self.db.query(models.AnswerSubmission).count(), 0)

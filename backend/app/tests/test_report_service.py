from __future__ import annotations

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.exceptions import ConflictError
from database import Base
from infrastructure.repositories.sqlite import SQLiteInterviewRepository
from services.report_generator.schemas import InterviewReport
from services.report_generator.service import ReportService
from shared.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    InterviewConfig,
    InterviewPlan,
    InterviewQuestion,
    InterviewRound,
    InterviewSessionState,
    InterviewTurn,
)


def interview_state(
    profile: CandidateProfile, *, completed: bool, mode: str = "text"
) -> InterviewSessionState:
    config = InterviewConfig(
        mode=mode,
        language="en",
        experience_level="middle",
        question_count=1,
    )
    question = InterviewQuestion(
        question="Explain FastAPI dependency injection.",
        language="en",
        topic="FastAPI",
        difficulty="medium",
    )
    turn = InterviewTurn(
        turn_id="turn-1",
        question=question,
        topic="FastAPI",
    )
    completed_turns = []
    current_turn = turn
    if completed:
        completed_turns = [
            turn.model_copy(
                update={
                    "answer": "I inject services with Depends.",
                    "candidate_answer": "I inject services with Depends.",
                    "status": "evaluated",
                    "evaluation": AnswerEvaluation(turn_id="turn-1", overall_score=8.0),
                }
            )
        ]
        current_turn = None
    return InterviewSessionState(
        candidate_profile=profile,
        interview_config=config,
        interview_plan=InterviewPlan(
            rounds=[InterviewRound(round_id="round-1", topic="FastAPI")]
        ),
        current_turn=current_turn,
        completed_turns=completed_turns,
        current_question_index=1 if completed else 0,
    )


class MockReportAgent:
    def __init__(self):
        self.calls = 0

    async def generate_report(self, candidate_profile, state):
        self.calls += 1
        return InterviewReport(
            id="report-1",
            overall_score=8.0,
            technical_score=8.0,
            communication_score=8.0,
            correctness_score=8.0,
            summary="Good evidence.",
            hiring_recommendation="hire",
            confidence_score=0.9,
        )


class ReportServiceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        self.repository = SQLiteInterviewRepository(self.db)
        candidate = self.repository.create_candidate("Tran Thi B")
        self.profile = CandidateProfile(
            candidate_id=candidate.candidate_id,
            name="Tran Thi B",
            skills=["Python", "FastAPI"],
        )
        self.repository.save_candidate_profile(candidate.candidate_id, self.profile)
        self.candidate_id = candidate.candidate_id

    def tearDown(self):
        self.db.close()

    def create_session(self, *, completed: bool, mode: str = "text"):
        session = self.repository.create_session(
            self.candidate_id, level="middle", language="en"
        )
        state = interview_state(self.profile, completed=completed, mode=mode)
        self.repository.update_session_state(
            session.session_id,
            "ENDED" if completed else "INTERVIEWING",
            state.model_dump(mode="json"),
            status="completed" if completed else "in_progress",
        )
        return session

    async def test_generate_completed_session_and_save_report(self):
        session = self.create_session(completed=True)
        agent = MockReportAgent()
        service = ReportService(agent=agent, repository=self.repository)

        report = await service.generate_for_session(session.session_id)

        self.assertEqual(report.session_id, session.session_id)
        self.assertEqual(self.repository.get_interview_report(session.session_id), report)
        saved_session = self.repository.get_session(session.session_id)
        self.assertEqual(saved_session.status, "report_generated")
        self.assertEqual(saved_session.report_id, report.id)

    async def test_reject_active_session(self):
        session = self.create_session(completed=False)
        service = ReportService(agent=MockReportAgent(), repository=self.repository)

        with self.assertRaises(ConflictError):
            await service.generate_for_session(session.session_id)

    async def test_report_generation_is_idempotent(self):
        session = self.create_session(completed=True)
        agent = MockReportAgent()
        service = ReportService(agent=agent, repository=self.repository)

        first = await service.generate_for_session(session.session_id)
        second = await service.generate_for_session(session.session_id)

        self.assertEqual(first, second)
        self.assertEqual(agent.calls, 1)

    async def test_sqlite_history_and_pagination(self):
        completed_session = self.create_session(completed=True)
        await ReportService(
            agent=MockReportAgent(), repository=self.repository
        ).generate_for_session(completed_session.session_id)
        voice_session = self.create_session(completed=False, mode="voice")

        first_page = self.repository.list_interview_sessions(None, limit=1, offset=0)
        second_page = self.repository.list_interview_sessions(None, limit=1, offset=1)

        self.assertEqual(self.repository.count_interview_sessions(), 2)
        self.assertEqual(len(first_page), 1)
        self.assertEqual(len(second_page), 1)
        self.assertNotEqual(first_page[0].session_id, second_page[0].session_id)
        report_summary = next(
            item for item in [*first_page, *second_page] if item.status == "report_generated"
        )
        self.assertEqual(report_summary.overall_score, 8.0)
        self.assertEqual(report_summary.answered_question_count, 1)
        voice_summary = next(
            item
            for item in [*first_page, *second_page]
            if item.session_id == voice_session.session_id
        )
        self.assertEqual(voice_summary.mode, "voice")


if __name__ == "__main__":
    unittest.main()

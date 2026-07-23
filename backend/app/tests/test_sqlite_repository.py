import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
from database import Base
from app.repositories import SQLiteInterviewRepository
from app.schemas import AnswerEvaluation, CandidateProfile, EvaluationScore, FinalReport, InterviewTurn


class SQLiteInterviewRepositoryTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        self.repository = SQLiteInterviewRepository(self.db)

    def tearDown(self):
        self.db.close()

    def test_create_candidate(self):
        candidate = self.repository.create_candidate("Nguyen Van A")

        self.assertEqual(candidate.name, "Nguyen Van A")
        self.assertIsNotNone(self.repository.get_candidate(candidate.candidate_id))

    def test_save_profile(self):
        candidate = self.repository.create_candidate("Candidate")
        profile = CandidateProfile(
            name="Tran Thi B",
            skills=["Python", "FastAPI"],
            specialization="AI Interview",
            confidence_score=0.87,
        )

        saved_profile = self.repository.update_candidate_profile(candidate.candidate_id, profile)
        saved_candidate = self.repository.get_candidate(candidate.candidate_id)

        self.assertEqual(saved_profile, profile)
        self.assertEqual(saved_candidate.name, "Tran Thi B")
        self.assertEqual(saved_candidate.profile.specialization, "AI Interview")

    def test_candidate_profile_persists_across_repository_instances(self):
        candidate = self.repository.create_candidate("Candidate")
        profile = CandidateProfile(
            name="Tran Thi B",
            skills=["Python", "FastAPI"],
            specialization="AI Interview",
            confidence_score=0.87,
        )

        self.repository.save_candidate_profile(candidate.candidate_id, profile)
        another_repository = SQLiteInterviewRepository(self.db)
        saved_profile = another_repository.get_candidate_profile(candidate.candidate_id)
        saved_candidate = another_repository.get_candidate(candidate.candidate_id)

        self.assertEqual(saved_profile, profile)
        self.assertEqual(saved_candidate.profile, profile)

    def test_candidate_resume_text_persists_across_repository_instances(self):
        candidate = self.repository.create_candidate("Candidate")
        resume_text = "Tran Thi B\nAI Engineer\nPython FastAPI"

        self.repository.save_candidate_resume_text(candidate.candidate_id, resume_text)
        another_repository = SQLiteInterviewRepository(self.db)
        saved_candidate = another_repository.get_candidate(candidate.candidate_id)
        saved_resume_text = another_repository.get_candidate_resume_text(candidate.candidate_id)

        self.assertEqual(saved_resume_text, resume_text)
        self.assertEqual(saved_candidate.raw_resume_text, resume_text)

    def test_create_session(self):
        candidate = self.repository.create_candidate("Nguyen Van A")

        session = self.repository.create_session(
            candidate.candidate_id,
            role="Backend Developer",
            level="Junior",
            language="vi",
        )

        self.assertEqual(session.candidate_id, candidate.candidate_id)
        self.assertEqual(session.role, "Backend Developer")
        self.assertEqual(session.level, "Junior")
        self.assertEqual(session.language, "vi")

    def test_save_interview_turn(self):
        candidate = self.repository.create_candidate("Nguyen Van A")
        session = self.repository.create_session(candidate.candidate_id)
        turn = InterviewTurn(
            turn_id="turn-1",
            question="Explain dependency injection.",
            topic="Backend",
            candidate_answer="It passes dependencies from outside the class.",
        )

        saved_turn = self.repository.save_turn(session.session_id, turn)
        turns = self.repository.get_turns(session.session_id)

        self.assertEqual(saved_turn, turn)
        self.assertEqual(turns, [turn])

    def test_save_evaluation(self):
        candidate = self.repository.create_candidate("Nguyen Van A")
        session = self.repository.create_session(candidate.candidate_id)
        turn = InterviewTurn(
            turn_id="turn-1",
            question="Explain dependency injection.",
            topic="Backend",
        )
        self.repository.save_turn(session.session_id, turn)
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            scores=EvaluationScore(overall_score=8.0),
            feedback="Clear and practical.",
        )

        saved_evaluation = self.repository.save_evaluation(session.session_id, evaluation)
        db_evaluation = self.db.query(models.Evaluation).first()

        self.assertEqual(saved_evaluation, evaluation)
        self.assertEqual(db_evaluation.correctness, "Correct")
        self.assertEqual(db_evaluation.score, 8)

    def test_save_report(self):
        candidate = self.repository.create_candidate("Nguyen Van A")
        session = self.repository.create_session(candidate.candidate_id)
        report = FinalReport(
            session_id=session.session_id,
            candidate_id=candidate.candidate_id,
            overall_score=7.5,
            recommendation="hire",
            summary="Good backend fundamentals.",
        )

        saved_report = self.repository.save_report(session.session_id, report)
        loaded_report = self.repository.get_report(session.session_id)

        self.assertEqual(saved_report, report)
        self.assertEqual(loaded_report, report)


if __name__ == "__main__":
    unittest.main()

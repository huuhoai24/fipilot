import unittest

from app.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    InterviewConfig,
    InterviewPlan,
    InterviewQuestion,
    InterviewRound,
    InterviewSessionState,
)
from app.services.interview_decision_service import InterviewDecisionService


def current_question() -> InterviewQuestion:
    return InterviewQuestion(
        question="How would you optimize YOLOv8 inference?",
        language="en",
        topic="YOLO Optimization",
        difficulty="medium",
        reasoning="Candidate has YOLO evidence.",
        expected_answer_points=["profiling", "TensorRT"],
        follow_up_questions=[],
    )


def session_state() -> InterviewSessionState:
    return InterviewSessionState(
        candidate_profile=CandidateProfile(name="Tran Thi B", skills=["YOLOv8"]),
        interview_config=InterviewConfig(language="en", experience_level="middle"),
        interview_plan=InterviewPlan(
            rounds=[
                InterviewRound(round_id="round-1", topic="YOLO Optimization"),
                InterviewRound(round_id="round-2", topic="FastAPI Deployment"),
            ]
        ),
        current_question_index=0,
    )


class InterviewDecisionServiceTests(unittest.TestCase):
    def test_weak_answer_returns_follow_up(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=3.0,
            follow_up_needed=True,
            follow_up_reason="Answer is too vague.",
        )

        decision = InterviewDecisionService().decide(evaluation, current_question(), session_state())

        self.assertEqual(decision.action, "follow_up")
        self.assertEqual(decision.next_topic, "YOLO Optimization")
        self.assertEqual(decision.reason, "Answer is too vague.")

    def test_good_answer_returns_increase_difficulty(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=8.5,
            follow_up_needed=False,
        )

        decision = InterviewDecisionService().decide(evaluation, current_question(), session_state())

        self.assertEqual(decision.action, "increase_difficulty")
        self.assertEqual(decision.next_topic, "YOLO Optimization")
        self.assertEqual(decision.difficulty_change, "increase")

    def test_normal_answer_returns_next_question(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=6.5,
            follow_up_needed=False,
        )

        decision = InterviewDecisionService().decide(evaluation, current_question(), session_state())

        self.assertEqual(decision.action, "next_question")
        self.assertEqual(decision.next_topic, "FastAPI Deployment")
        self.assertIsNone(decision.difficulty_change)


if __name__ == "__main__":
    unittest.main()

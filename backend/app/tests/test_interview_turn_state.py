import unittest

from app.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    EvaluationScore,
    InterviewConfig,
    InterviewPlan,
    InterviewQuestion,
    InterviewRound,
    InterviewSessionState,
    InterviewTurn,
)


class InterviewTurnStateTests(unittest.TestCase):
    def test_create_interview_turn(self):
        question = InterviewQuestion(
            question="Bạn tối ưu YOLOv8 inference pipeline như thế nào?",
            language="vi",
            topic="YOLO Optimization",
            difficulty="hard",
            reasoning="Candidate has YOLOv8 project evidence.",
            expected_answer_points=["latency", "mAP", "TensorRT"],
            follow_up_questions=["Bạn đo latency như thế nào?"],
        )

        turn = InterviewTurn(turn_id="turn-1", question=question)

        self.assertEqual(turn.status, "created")
        self.assertEqual(turn.question.topic, "YOLO Optimization")
        self.assertIsNone(turn.answer)

    def test_update_answer(self):
        turn = InterviewTurn(
            turn_id="turn-1",
            question=InterviewQuestion(
                question="Explain FastAPI dependency injection.",
                language="en",
                topic="FastAPI",
                difficulty="medium",
                reasoning="Candidate lists FastAPI.",
                expected_answer_points=[],
                follow_up_questions=[],
            ),
        )

        answered_turn = turn.model_copy(update={"answer": "It injects dependencies per request.", "status": "answered"})

        self.assertEqual(answered_turn.status, "answered")
        self.assertEqual(answered_turn.answer, "It injects dependencies per request.")

    def test_status_transition_to_evaluated(self):
        turn = InterviewTurn(
            turn_id="turn-1",
            question="Explain FastAPI dependency injection.",
            topic="FastAPI",
        )
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            scores=EvaluationScore(overall_score=8.0),
            feedback="Clear answer.",
        )

        evaluated_turn = turn.model_copy(
            update={
                "answer": "It provides dependencies to route handlers.",
                "status": "evaluated",
                "evaluation": evaluation,
            }
        )

        self.assertEqual(evaluated_turn.status, "evaluated")
        self.assertEqual(evaluated_turn.evaluation.scores.overall_score, 8.0)

    def test_session_state_validation(self):
        candidate_profile = CandidateProfile(
            name="Tran Thi B",
            skills=["Python", "YOLOv8"],
            specialization="Computer Vision",
        )
        config = InterviewConfig(language="vi", experience_level="middle")
        plan = InterviewPlan(
            rounds=[
                InterviewRound(
                    round_id="round-1",
                    topic="YOLO Optimization",
                    difficulty="hard",
                )
            ]
        )
        current_turn = InterviewTurn(
            turn_id="turn-1",
            question=InterviewQuestion(
                question="Bạn tối ưu YOLOv8 như thế nào?",
                language="vi",
                topic="YOLO Optimization",
                difficulty="hard",
                reasoning="Candidate has YOLOv8 project evidence.",
                expected_answer_points=["latency", "accuracy"],
                follow_up_questions=[],
            ),
        )

        state = InterviewSessionState(
            candidate_profile=candidate_profile,
            interview_config=config,
            interview_plan=plan,
            current_turn=current_turn,
            current_question_index=0,
        )

        self.assertEqual(state.candidate_profile.name, "Tran Thi B")
        self.assertEqual(state.interview_config.language, "vi")
        self.assertEqual(state.interview_plan.rounds[0].topic, "YOLO Optimization")
        self.assertEqual(state.current_turn.turn_id, "turn-1")
        self.assertEqual(state.completed_turns, [])


if __name__ == "__main__":
    unittest.main()

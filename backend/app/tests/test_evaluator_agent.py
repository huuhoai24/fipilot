import unittest

from pydantic import ValidationError

from app.agents.evaluator_agent import EvaluatorAgent
from app.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    InterviewConfig,
    InterviewQuestion,
    InterviewTurn,
)


class MockLLMService:
    def __init__(self, evaluation: AnswerEvaluation):
        self.evaluation = evaluation
        self.prompt = ""
        self.output_schema = None
        self.kwargs = {}

    async def generate_json(self, prompt, output_schema, **kwargs):
        self.prompt = prompt
        self.output_schema = output_schema
        self.kwargs = kwargs
        return self.evaluation


def candidate_profile() -> CandidateProfile:
    return CandidateProfile(
        name="Tran Thi B",
        skills=["Python", "YOLOv8", "FastAPI"],
        specialization="Computer Vision",
    )


def interview_question(language: str = "en") -> InterviewQuestion:
    return InterviewQuestion(
        question="How would you optimize a YOLOv8 inference pipeline?",
        language=language,
        topic="YOLO Optimization",
        difficulty="hard",
        reasoning="Candidate has YOLOv8 project evidence.",
        expected_answer_points=["profiling", "TensorRT", "mAP and latency trade-off"],
        follow_up_questions=["How would you validate accuracy after optimization?"],
    )


class EvaluatorAgentTests(unittest.IsolatedAsyncioTestCase):
    async def test_vietnamese_evaluation(self):
        expected = AnswerEvaluation(
            turn_id="",
            overall_score=8.0,
            technical_score=8.5,
            communication_score=7.5,
            correctness_score=8.0,
            strengths=["Nêu được TensorRT và latency"],
            weaknesses=["Chưa nói rõ cách đo mAP"],
            missing_concepts=["accuracy regression test"],
            follow_up_needed=True,
            follow_up_reason="Cần làm rõ cách validate mAP sau optimization",
            feedback="Câu trả lời tốt, nhưng cần giải thích rõ hơn về mAP.",
        )
        llm_service = MockLLMService(expected)
        agent = EvaluatorAgent(llm_service=llm_service)

        result = await agent.evaluate_answer(
            candidate_profile(),
            interview_question(language="vi"),
            "Em dùng TensorRT và đo latency.",
            InterviewConfig(language="vi", experience_level="middle"),
        )

        self.assertTrue(result.follow_up_needed)
        self.assertIn("mAP", result.feedback)
        self.assertIn("The interview language is Vietnamese.", llm_service.prompt)
        self.assertIn("expected_answer_points", llm_service.prompt)
        self.assertEqual(llm_service.output_schema, AnswerEvaluation)

    async def test_english_evaluation(self):
        expected = AnswerEvaluation(
            turn_id="",
            overall_score=9.0,
            technical_score=9.0,
            communication_score=8.5,
            correctness_score=9.0,
            strengths=["Explains profiling and TensorRT clearly"],
            weaknesses=[],
            missing_concepts=[],
            follow_up_needed=False,
            feedback="Strong answer with practical validation details.",
        )
        llm_service = MockLLMService(expected)
        agent = EvaluatorAgent(llm_service=llm_service)

        result = await agent.evaluate_answer(
            candidate_profile(),
            interview_question(language="en"),
            "I would profile first, export to TensorRT, then compare mAP and latency.",
            InterviewConfig(language="en", experience_level="middle"),
        )

        self.assertFalse(result.follow_up_needed)
        self.assertEqual(result.overall_score, 9.0)
        self.assertIn("The interview language is English.", llm_service.prompt)
        self.assertIn('"language": "en"', llm_service.prompt)

    async def test_follow_up_needed_true(self):
        expected = AnswerEvaluation(
            turn_id="",
            overall_score=4.0,
            technical_score=4.0,
            communication_score=5.0,
            correctness_score=3.5,
            weaknesses=["Answer is too vague"],
            missing_concepts=["profiling", "accuracy validation"],
            follow_up_needed=True,
            follow_up_reason="Answer lacks concrete optimization and validation steps.",
            feedback="Please clarify the actual optimization pipeline.",
        )
        result = await EvaluatorAgent(MockLLMService(expected)).evaluate_answer(
            candidate_profile(),
            interview_question(),
            "I make it faster.",
            InterviewConfig(language="en", experience_level="middle"),
        )

        self.assertTrue(result.follow_up_needed)
        self.assertEqual(result.follow_up_reason, "Answer lacks concrete optimization and validation steps.")

    async def test_follow_up_needed_false(self):
        expected = AnswerEvaluation(
            turn_id="",
            overall_score=8.5,
            technical_score=8.5,
            communication_score=8.0,
            correctness_score=8.5,
            strengths=["Covers profiling and validation"],
            follow_up_needed=False,
            feedback="Complete enough to move to the next topic.",
        )
        result = await EvaluatorAgent(MockLLMService(expected)).evaluate_answer(
            candidate_profile(),
            interview_question(),
            "I profile bottlenecks, optimize with TensorRT, and compare mAP and latency.",
            InterviewConfig(language="en", experience_level="middle"),
        )

        self.assertFalse(result.follow_up_needed)

    async def test_high_quality_answer(self):
        expected = AnswerEvaluation(
            turn_id="",
            overall_score=9.2,
            technical_score=9.5,
            communication_score=8.8,
            correctness_score=9.3,
            strengths=["Connects profiling, TensorRT, and mAP validation"],
            weaknesses=[],
            missing_concepts=[],
            follow_up_needed=False,
            feedback="High-quality answer with clear technical and practical evidence.",
        )

        result = await EvaluatorAgent(MockLLMService(expected)).evaluate_answer(
            candidate_profile(),
            interview_question(),
            "I would profile the pipeline, convert to TensorRT, compare latency and mAP, and run regression tests.",
            InterviewConfig(language="en", experience_level="middle"),
        )

        self.assertGreaterEqual(result.overall_score, 9.0)
        self.assertFalse(result.follow_up_needed)
        self.assertEqual(result.weaknesses, [])

    async def test_weak_answer(self):
        expected = AnswerEvaluation(
            turn_id="",
            overall_score=3.0,
            technical_score=2.5,
            communication_score=4.0,
            correctness_score=2.0,
            strengths=[],
            weaknesses=["Does not address expected answer points"],
            missing_concepts=["profiling", "TensorRT", "mAP and latency trade-off"],
            follow_up_needed=True,
            follow_up_reason="Candidate answer is too shallow to evaluate practical experience.",
            feedback="Weak answer; it needs concrete optimization and validation details.",
        )

        result = await EvaluatorAgent(MockLLMService(expected)).evaluate_answer(
            candidate_profile(),
            interview_question(),
            "Just make it faster.",
            InterviewConfig(language="en", experience_level="middle"),
        )

        self.assertLessEqual(result.overall_score, 3.0)
        self.assertTrue(result.follow_up_needed)
        self.assertIn("TensorRT", result.missing_concepts)

    def test_schema_validation_and_turn_transition(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=7.0,
            technical_score=7.0,
            communication_score=7.5,
            correctness_score=7.0,
            feedback="Solid answer.",
        )
        turn = InterviewTurn(turn_id="turn-1", question=interview_question())

        evaluated_turn = turn.with_evaluation(evaluation)

        self.assertEqual(evaluated_turn.status, "evaluated")
        self.assertEqual(evaluated_turn.evaluation.overall_score, 7.0)

        with self.assertRaises(ValidationError):
            AnswerEvaluation(turn_id="turn-1", overall_score=11.0)


if __name__ == "__main__":
    unittest.main()

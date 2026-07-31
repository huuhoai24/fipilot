import unittest

from pydantic import ValidationError

from app.agents.question_generator_agent import QuestionGeneratorAgent
from app.schemas import CandidateProfile, InterviewConfig, InterviewQuestion, InterviewRound


class MockLLMService:
    def __init__(self, question: InterviewQuestion):
        self.question = question
        self.prompt = ""
        self.output_schema = None
        self.kwargs = {}

    async def generate_json(self, prompt, output_schema, **kwargs):
        self.prompt = prompt
        self.output_schema = output_schema
        self.kwargs = kwargs
        return self.question


def candidate_profile() -> CandidateProfile:
    return CandidateProfile(
        name="Tran Thi B",
        skills=["Python", "YOLOv8", "FastAPI"],
        skill_evidence=[
            {
                "skill": "YOLOv8",
                "evidence": ["Optimized YOLOv8 object detection pipeline."],
                "source_section": "Projects",
            }
        ],
        specialization="Computer Vision",
    )


def interview_round() -> InterviewRound:
    return InterviewRound(
        round_id="round-1",
        topic="YOLO Optimization",
        difficulty="hard",
        reasoning="Candidate has YOLOv8 project evidence.",
        recommended_question_areas=["model optimization", "object detection pipeline"],
        target_skills=["YOLOv8", "PyTorch"],
    )


class QuestionGeneratorAgentTests(unittest.IsolatedAsyncioTestCase):
    async def test_vietnamese_question_generation(self):
        expected_question = InterviewQuestion(
            question="Bạn tối ưu YOLOv8 như thế nào để giảm latency mà vẫn giữ mAP ổn định?",
            language="vi",
            topic="YOLO Optimization",
            difficulty="hard",
            reasoning="Ứng viên có evidence về YOLOv8 optimization.",
            expected_answer_points=["latency", "mAP", "TensorRT hoặc quantization"],
            follow_up_questions=["Bạn đo trade-off latency và accuracy ra sao?"],
        )
        llm_service = MockLLMService(expected_question)
        agent = QuestionGeneratorAgent(llm_service=llm_service)

        question = await agent.generate_question(
            candidate_profile(),
            interview_round(),
            InterviewConfig(language="vi", experience_level="middle"),
        )

        self.assertEqual(question.language, "vi")
        self.assertIn("YOLOv8", question.question)
        self.assertIn("The interview language is Vietnamese.", llm_service.prompt)
        self.assertIn("keep technical terms", llm_service.prompt.lower())
        self.assertIn("one or two short sentences", llm_service.prompt.lower())
        self.assertEqual(llm_service.output_schema, InterviewQuestion)
        self.assertEqual(llm_service.kwargs["task_type"], "simple")
        self.assertEqual(llm_service.kwargs["thinking_budget"], 0)

    async def test_english_question_generation(self):
        expected_question = InterviewQuestion(
            question="How would you optimize a YOLOv8 inference pipeline for lower latency?",
            language="en",
            topic="YOLO Optimization",
            difficulty="hard",
            reasoning="Candidate has YOLOv8 project evidence.",
            expected_answer_points=["profiling", "batch size", "TensorRT"],
            follow_up_questions=["How would you validate accuracy after optimization?"],
        )
        llm_service = MockLLMService(expected_question)
        agent = QuestionGeneratorAgent(llm_service=llm_service)

        question = await agent.generate_question(
            candidate_profile(),
            interview_round(),
            InterviewConfig(language="en", experience_level="middle"),
        )

        self.assertEqual(question.language, "en")
        self.assertIn("How would you", question.question)
        self.assertIn("The interview language is English.", llm_service.prompt)
        self.assertIn('"language": "en"', llm_service.prompt)

    async def test_voice_question_uses_configured_interviewer_personality(self):
        expected_question = InterviewQuestion(
            question="Which latency and accuracy trade-offs did you measure?",
            language="en",
            topic="YOLO Optimization",
            difficulty="hard",
        )
        voice_llm = MockLLMService(expected_question)
        voice_agent = QuestionGeneratorAgent(llm_service=voice_llm)
        await voice_agent.generate_question(
            candidate_profile(),
            interview_round(),
            InterviewConfig(
                mode="voice",
                language="en",
                experience_level="middle",
                interviewer_personality="challenging",
            ),
        )
        self.assertIn("direct, rigorous tone", voice_llm.prompt)

        text_llm = MockLLMService(expected_question)
        text_agent = QuestionGeneratorAgent(llm_service=text_llm)
        await text_agent.generate_question(
            candidate_profile(),
            interview_round(),
            InterviewConfig(
                mode="text",
                language="en",
                experience_level="middle",
                interviewer_personality="challenging",
            ),
        )
        self.assertNotIn("direct, rigorous tone", text_llm.prompt)

    def test_interview_question_schema_validation(self):
        question = InterviewQuestion(
            question="Explain FastAPI dependency injection.",
            language="en",
            topic="FastAPI",
            difficulty="medium",
            reasoning="Candidate lists FastAPI.",
            expected_answer_points=["dependency injection", "testing", "request lifecycle"],
            follow_up_questions=["How do you override dependencies in tests?"],
        )

        self.assertEqual(question.topic, "FastAPI")
        self.assertEqual(question.expected_answer_points[0], "dependency injection")

        with self.assertRaises(ValidationError):
            InterviewQuestion(
                question="Bonjour?",
                language="fr",
                topic="FastAPI",
                difficulty="medium",
                reasoning="Invalid language.",
                expected_answer_points=[],
                follow_up_questions=[],
            )


if __name__ == "__main__":
    unittest.main()

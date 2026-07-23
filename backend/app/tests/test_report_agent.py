from __future__ import annotations

import unittest

from pydantic import ValidationError

from services.report_generator.agent import ReportGeneratorAgent
from services.report_generator.prompts import build_report_prompt
from services.report_generator.schemas import InterviewReport
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


def completed_state(language: str, answer: str) -> InterviewSessionState:
    profile = CandidateProfile(name="Tran Thi B", skills=["Python", "FastAPI"])
    config = InterviewConfig(language=language, experience_level="middle")
    question = InterviewQuestion(
        question="Explain dependency injection.",
        language=language,
        topic="FastAPI",
        difficulty="medium",
    )
    evaluation = AnswerEvaluation(
        turn_id="turn-1",
        overall_score=8.0,
        technical_score=8.5,
        communication_score=7.5,
        correctness_score=8.0,
        feedback="Clear evidence.",
    )
    turn = InterviewTurn(
        turn_id="turn-1",
        question=question,
        answer=answer,
        candidate_answer=answer,
        status="evaluated",
        evaluation=evaluation,
        topic="FastAPI",
    )
    return InterviewSessionState(
        candidate_profile=profile,
        interview_config=config,
        interview_plan=InterviewPlan(
            rounds=[InterviewRound(round_id="round-1", topic="FastAPI")]
        ),
        current_turn=None,
        completed_turns=[turn],
        current_question_index=1,
    )


def report_result() -> InterviewReport:
    return InterviewReport(
        overall_score=8.0,
        technical_score=8.5,
        communication_score=7.5,
        correctness_score=8.0,
        summary="Evidence-based summary.",
        hiring_recommendation="hire",
        confidence_score=0.9,
    )


class MockLLMService:
    def __init__(self):
        self.calls = []

    async def generate_json(self, prompt, output_schema, **kwargs):
        self.calls.append((prompt, output_schema, kwargs))
        return report_result()


class ReportAgentTests(unittest.IsolatedAsyncioTestCase):
    def test_report_score_validation(self):
        with self.assertRaises(ValidationError):
            InterviewReport(
                overall_score=11,
                technical_score=8,
                communication_score=8,
                correctness_score=8,
                summary="Invalid score.",
                hiring_recommendation="hire",
                confidence_score=0.8,
            )
        with self.assertRaises(ValidationError):
            InterviewReport(
                overall_score=8,
                technical_score=8,
                communication_score=8,
                correctness_score=8,
                summary="Invalid confidence.",
                hiring_recommendation="hire",
                confidence_score=1.2,
            )

    def test_vietnamese_report_prompt_contains_all_evidence(self):
        state = completed_state("vi", "Tôi dùng Depends để truyền dependency.")
        prompt = build_report_prompt(state.candidate_profile, state)

        self.assertIn("Vietnamese", prompt)
        self.assertIn("Tôi dùng Depends", prompt)
        self.assertIn("answer_evaluations", prompt)
        self.assertIn("not evaluated", prompt)

    def test_english_report_prompt_contains_all_evidence(self):
        state = completed_state("en", "I use Depends to inject a service.")
        prompt = build_report_prompt(state.candidate_profile, state)

        self.assertIn("English", prompt)
        self.assertIn("I use Depends", prompt)
        self.assertIn("interview_plan", prompt)

    async def test_agent_uses_complex_structured_output(self):
        llm = MockLLMService()
        state = completed_state("en", "I use Depends to inject a service.")
        agent = ReportGeneratorAgent(llm_service=llm)

        report = await agent.generate_report(state.candidate_profile, state)

        self.assertIsInstance(report, InterviewReport)
        self.assertTrue(report.id)
        self.assertEqual(report.session_id, "")
        self.assertIs(llm.calls[0][1], InterviewReport)
        self.assertEqual(llm.calls[0][2]["task_type"], "complex")


if __name__ == "__main__":
    unittest.main()

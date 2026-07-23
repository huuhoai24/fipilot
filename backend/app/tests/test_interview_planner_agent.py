import unittest

from app.agents.interview_planner_agent import InterviewPlannerAgent
from app.schemas import CandidateProfile, InterviewConfig, InterviewPlan, InterviewRound


class MockLLMService:
    def __init__(self):
        self.prompt = ""
        self.output_schema = None
        self.kwargs = {}

    async def generate_json(self, prompt, output_schema, **kwargs):
        self.prompt = prompt
        self.output_schema = output_schema
        self.kwargs = kwargs
        return InterviewPlan(
            rounds=[
                InterviewRound(
                    round_id="round-1",
                    topic="Computer Vision APIs",
                    objective="Validate practical FastAPI and model-serving depth.",
                    difficulty="hard",
                    reasoning="Candidate lists FastAPI and evidence from an AI interview project.",
                    recommended_question_areas=[
                        "API design",
                        "model serving",
                        "evaluation tradeoffs",
                    ],
                    target_skills=["FastAPI", "Python"],
                    question_budget=3,
                    weight=0.4,
                )
            ],
            coverage_goals=["Validate evidence-backed FastAPI experience."],
            risk_areas=["Confirm whether model-serving work was production-grade."],
            planner_summary="Plan prioritizes project-backed AI interview experience.",
        )


class InterviewPlannerAgentTests(unittest.IsolatedAsyncioTestCase):
    async def test_create_plan_uses_candidate_profile_evidence(self):
        llm_service = MockLLMService()
        agent = InterviewPlannerAgent(llm_service=llm_service)
        candidate_profile = CandidateProfile(
            name="Tran Thi B",
            skills=["Python", "FastAPI"],
            skill_evidence=[
                {
                    "skill": "FastAPI",
                    "evidence": ["Built an AI interview platform."],
                    "source_section": "Projects",
                }
            ],
            specialization="AI Interview",
        )

        config = InterviewConfig(language="vi", experience_level="junior")

        plan = await agent.create_plan(candidate_profile, config)

        self.assertEqual(llm_service.output_schema, InterviewPlan)
        self.assertIn("No job description", llm_service.prompt)
        self.assertIn("skill_evidence", llm_service.prompt)
        self.assertIn("The interview language is Vietnamese.", llm_service.prompt)
        self.assertIn('"language": "vi"', llm_service.prompt)
        self.assertEqual(llm_service.kwargs["system_instruction"].startswith("You are an interview planning agent"), True)
        self.assertEqual(plan.rounds[0].topic, "Computer Vision APIs")
        self.assertEqual(plan.rounds[0].difficulty, "hard")
        self.assertIn("API design", plan.rounds[0].recommended_question_areas)
        self.assertIn("Candidate lists FastAPI", plan.rounds[0].reasoning)

    async def test_create_plan_uses_english_output_mode(self):
        llm_service = MockLLMService()
        agent = InterviewPlannerAgent(llm_service=llm_service)
        candidate_profile = CandidateProfile(name="Tran Thi B", skills=["Python"])
        config = InterviewConfig(language="en", experience_level="senior", interview_style="mixed")

        await agent.create_plan(candidate_profile, config)

        self.assertIn("The interview language is English.", llm_service.prompt)
        self.assertIn('"language": "en"', llm_service.prompt)
        self.assertIn('"experience_level": "senior"', llm_service.prompt)
        self.assertIn('"interview_style": "mixed"', llm_service.prompt)


if __name__ == "__main__":
    unittest.main()

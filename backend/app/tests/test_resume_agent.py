import unittest

from app.agents.resume_agent import ResumeAgent
from app.schemas import CandidateProfile


class MockLLMService:
    def __init__(self):
        self.prompt = ""
        self.output_schema = None

    async def generate_json(self, prompt, output_schema, **kwargs):
        self.prompt = prompt
        self.output_schema = output_schema
        return CandidateProfile(
            name="Tran Thi B",
            skills=["Python"],
            skill_evidence=[
                {
                    "skill": "Python",
                    "evidence": ["Built an AI interview platform."],
                    "source_section": "Projects",
                }
            ],
            confidence_score=0.9,
        )


class ResumeAgentTests(unittest.IsolatedAsyncioTestCase):
    async def test_extract_profile_requests_skill_evidence(self):
        llm_service = MockLLMService()
        agent = ResumeAgent(llm_service=llm_service)

        profile = await agent.extract_profile("Python project: Built an AI interview platform.")

        self.assertEqual(profile.skill_evidence[0].skill, "Python")
        self.assertIn("skill_evidence", llm_service.prompt)
        self.assertEqual(llm_service.output_schema, CandidateProfile)


if __name__ == "__main__":
    unittest.main()

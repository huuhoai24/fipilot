import unittest

from app.agents.resume_agent import ResumeAgent
from app.schemas import CandidateProfile
from services.profile_scanner.exceptions import NonResumeDocumentError
from services.profile_scanner.schemas import ResumeExtractionResult


class MockLLMService:
    def __init__(self):
        self.prompt = ""
        self.output_schema = None
        self.kwargs = {}

    async def generate_json(self, prompt, output_schema, **kwargs):
        self.prompt = prompt
        self.output_schema = output_schema
        self.kwargs = kwargs
        return ResumeExtractionResult(
            document_type="resume",
            classification_confidence=0.98,
            name="Tran Thi B",
            skills=["Python"],
            skill_evidence=[
                {
                    "skill": "Python",
                    "evidence": "Built an AI interview platform.",
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
        self.assertIn("at most 30", llm_service.prompt)
        self.assertIn("at most 8", llm_service.prompt)
        self.assertIn("one evidence string", llm_service.prompt)
        self.assertIn("240 characters", llm_service.prompt)
        self.assertIn("Do not return an empty", llm_service.prompt)
        self.assertIn("target 20 to 30", llm_service.prompt)
        self.assertIn("untrusted", llm_service.prompt.lower())
        self.assertIn("capstone reports", llm_service.prompt)
        self.assertIn("10 supported technology domains", llm_service.prompt)
        self.assertIn("Backend Developer", llm_service.prompt)
        self.assertEqual(llm_service.output_schema, ResumeExtractionResult)
        self.assertEqual(llm_service.kwargs["task_type"], "simple")
        self.assertEqual(llm_service.kwargs["thinking_budget"], 0)

    async def test_rejects_project_report_instead_of_creating_profile(self):
        class ProjectReportLLM(MockLLMService):
            async def generate_json(self, prompt, output_schema, **kwargs):
                self.prompt = prompt
                return ResumeExtractionResult(
                    document_type="project_report",
                    classification_confidence=0.99,
                    name="Capstone Team",
                    skills=["FastAPI", "React", "Gemini"],
                    projects=[
                        {
                            "name": "AI Interview Platform",
                            "description": "Capstone implementation report.",
                        }
                    ],
                    confidence_score=0.9,
                )

        agent = ResumeAgent(llm_service=ProjectReportLLM())

        with self.assertRaises(NonResumeDocumentError):
            await agent.extract_profile(
                "CAPSTONE PROJECT REPORT\nTable of contents\nSystem architecture"
            )

    def test_extraction_prioritizes_skills_with_evidence_within_limit(self):
        extraction = ResumeExtractionResult(
            document_type="resume",
            classification_confidence=0.95,
            skills=[f"Skill {index}" for index in range(35)],
            skill_evidence=[
                {
                    "skill": "Skill 34",
                    "evidence": "Used Skill 34 in a production project.",
                }
            ],
        )

        profile = extraction.to_candidate_profile()

        self.assertEqual(len(profile.skills), 30)
        self.assertIn("Skill 34", profile.skills)
        self.assertEqual(profile.skill_evidence[0].skill, "Skill 34")


if __name__ == "__main__":
    unittest.main()

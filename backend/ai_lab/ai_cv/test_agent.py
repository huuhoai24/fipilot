import unittest

from ai_lab.ai_cv.agent import CVLabAgent
from ai_lab.ai_cv.exceptions import NonResumeDocumentError, MarginalResumeDocumentError
from ai_lab.ai_cv.schemas import CVInput, ResumeExtractionResult, CandidateProfile


class MockLLMService:
    def __init__(self, document_type="resume", classification_confidence=0.98, closest_domains=None, match_percentage=None):
        self.document_type = document_type
        self.classification_confidence = classification_confidence
        self.closest_domains = closest_domains if closest_domains is not None else []
        self.match_percentage = match_percentage
        self.prompt = ""
        self.output_schema = None
        self.kwargs = {}

    async def generate_json(self, prompt, output_schema, **kwargs):
        self.prompt = prompt
        self.output_schema = output_schema
        self.kwargs = kwargs
        return ResumeExtractionResult(
            document_type=self.document_type,
            classification_confidence=self.classification_confidence,
            closest_domains=self.closest_domains,
            match_percentage=self.match_percentage,
            name="Test Candidate",
            skills=["Python"],
            skill_evidence=[],
            confidence_score=0.9,
        )


class CVLabAgentTests(unittest.IsolatedAsyncioTestCase):
    async def test_resume_passes_normally(self):
        llm = MockLLMService(document_type="resume", classification_confidence=0.9)
        agent = CVLabAgent(llm)
        input_data = CVInput(resume_text="Some resume text")
        
        profile = await agent.run(input_data)
        self.assertIsInstance(profile, CandidateProfile)
        self.assertEqual(profile.name, "Test Candidate")

    async def test_marginal_resume_raises_marginal_error(self):
        llm = MockLLMService(
            document_type="marginal_resume",
            classification_confidence=0.9,
            closest_domains=["Web Developer", "Backend Developer"],
            match_percentage=45,
        )
        agent = CVLabAgent(llm)
        input_data = CVInput(resume_text="Some resume text")
        
        with self.assertRaises(MarginalResumeDocumentError) as context:
            await agent.run(input_data)
            
        self.assertEqual(context.exception.code, "marginal_resume")
        self.assertIn("Hệ thống nhận định CV của bạn có thể thuộc domain: Web Developer, Backend Developer với mức độ phù hợp khoảng 45%.", context.exception.safe_message)
        self.assertIn("Bạn có muốn tiếp tục không?", context.exception.safe_message)

    async def test_unsupported_resume_raises_standard_error(self):
        llm = MockLLMService(document_type="other", classification_confidence=0.9)
        agent = CVLabAgent(llm)
        input_data = CVInput(resume_text="Some resume text")
        
        with self.assertRaises(NonResumeDocumentError) as context:
            await agent.run(input_data)
            
        self.assertEqual(context.exception.code, "not_a_resume")
        self.assertIn(
            "Nền tảng hiện tại chỉ hỗ trợ phỏng vấn cho 10 ngành nghề thuộc khối Công nghệ & Kỹ thuật phần mềm",
            context.exception.safe_message
        )

    async def test_low_confidence_raises_standard_error(self):
        llm = MockLLMService(document_type="resume", classification_confidence=0.5)
        agent = CVLabAgent(llm)
        input_data = CVInput(resume_text="Some resume text")
        
        with self.assertRaises(NonResumeDocumentError) as context:
            await agent.run(input_data)
            
        self.assertEqual(context.exception.code, "not_a_resume")
        self.assertIn(
            "Nền tảng hiện tại chỉ hỗ trợ phỏng vấn cho 10 ngành nghề thuộc khối Công nghệ & Kỹ thuật phần mềm",
            context.exception.safe_message
        )


if __name__ == "__main__":
    unittest.main()

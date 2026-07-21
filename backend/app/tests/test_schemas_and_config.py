import unittest

from app.config.settings import Settings
from app.schemas import (
    AnswerSubmission,
    CandidateProfile,
    EvaluationScore,
    InterviewGraphState,
    InterviewPlan,
    InterviewRound,
)


class V2FoundationTests(unittest.TestCase):
    def test_settings_defaults(self):
        settings = Settings(app_env="test")
        self.assertEqual(settings.application.app_env, "test")
        self.assertEqual(settings.app_env, "test")
        self.assertFalse(settings.debug)
        self.assertEqual(settings.gemini_simple_model, "gemini-2.5-flash")
        self.assertEqual(settings.llm_routing.complex_model, "gemini-2.5-pro")
        self.assertEqual(settings.database_url, "sqlite:///./interview_app.db")
        self.assertGreater(settings.max_resume_bytes, 0)

    def test_settings_groups_accept_required_field_names(self):
        settings = Settings(
            APP_ENV="test",
            DEBUG=True,
            GOOGLE_CLOUD_PROJECT="sample-project",
            GOOGLE_CLOUD_LOCATION="asia-southeast1",
            GEMINI_SIMPLE_MODEL="gemini-flash-test",
            GEMINI_COMPLEX_MODEL="gemini-pro-test",
            DATABASE_URL="sqlite:///./test.db",
            LOG_LEVEL="DEBUG",
        )

        self.assertEqual(settings.application.app_env, "test")
        self.assertTrue(settings.application.debug)
        self.assertEqual(settings.google_cloud.project, "sample-project")
        self.assertEqual(settings.google_cloud.location, "asia-southeast1")
        self.assertEqual(settings.llm_routing.simple_model, "gemini-flash-test")
        self.assertEqual(settings.llm_routing.complex_model, "gemini-pro-test")
        self.assertEqual(settings.database.url, "sqlite:///./test.db")
        self.assertEqual(settings.log_level, "DEBUG")

    def test_candidate_profile_defaults(self):
        profile = CandidateProfile(skills=["Python", "RAG"], confidence=0.8)
        self.assertEqual(profile.name, "Candidate")
        self.assertEqual(profile.skills, ["Python", "RAG"])
        self.assertEqual(profile.confidence, 0.8)

    def test_interview_plan_schema(self):
        plan = InterviewPlan(
            rounds=[
                InterviewRound(
                    round_id="round-1",
                    topic="Machine Learning",
                    difficulty="medium",
                    weight=0.5,
                )
            ]
        )
        self.assertEqual(plan.rounds[0].topic, "Machine Learning")

    def test_answer_submission_validation(self):
        submission = AnswerSubmission(turn_id="turn-1", answer="A concise answer")
        self.assertEqual(submission.turn_id, "turn-1")

    def test_score_bounds(self):
        score = EvaluationScore(overall_score=7.5)
        self.assertEqual(score.overall_score, 7.5)

    def test_graph_state_defaults(self):
        state = InterviewGraphState(language="vi")
        self.assertEqual(state.status, "draft")
        self.assertEqual(state.history, [])
        self.assertEqual(state.memory.covered_topics, [])


if __name__ == "__main__":
    unittest.main()

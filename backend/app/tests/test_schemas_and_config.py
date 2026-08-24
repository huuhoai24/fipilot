import unittest

from app.config.settings import Settings
from app.schemas import (
    AnswerSubmission,
    AnswerEvaluation,
    CandidateEducation,
    CandidateExperience,
    CandidateProfile,
    EvaluationScore,
    InterviewConfig,
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
        self.assertEqual(settings.gemini_resume_model, "gemini-2.5-flash-lite")
        self.assertEqual(settings.gemini_resume_location, "global")
        self.assertEqual(settings.database_url, "sqlite:///./interview_app.db")
        self.assertGreater(settings.max_resume_bytes, 0)
        self.assertEqual(settings.stt_model, "large-v3")
        self.assertEqual(settings.stt_device, "cpu")
        self.assertEqual(settings.stt_compute_type, "int8")
        self.assertEqual(settings.stt_language, "vi")
        self.assertEqual(settings.stt_vocabulary_profile, "auto")
        self.assertEqual(settings.stt_hotwords, [])
        self.assertEqual(settings.stt_final_beam_size, 5)
        self.assertEqual(settings.tts_mode, "v3turbo")
        self.assertEqual(settings.tts_device, "auto")
        self.assertEqual(settings.tts_sample_rate, 24000)
        self.assertEqual(settings.interview_preparation_ttl_seconds, 300)
        self.assertEqual(settings.interview_preparation_max_entries, 128)

    def test_settings_groups_accept_required_field_names(self):
        settings = Settings(
            APP_ENV="test",
            DEBUG=True,
            GOOGLE_CLOUD_PROJECT="sample-project",
            GOOGLE_CLOUD_LOCATION="asia-southeast1",
            GEMINI_SIMPLE_MODEL="gemini-flash-test",
            GEMINI_COMPLEX_MODEL="gemini-pro-test",
            GEMINI_RESUME_MODEL="gemini-resume-test",
            GEMINI_RESUME_LOCATION="asia-southeast1",
            DATABASE_URL="sqlite:///./test.db",
            LOG_LEVEL="DEBUG",
            STT_MODEL="small",
            STT_DEVICE="cuda",
            STT_COMPUTE_TYPE="float16",
            STT_LANGUAGE="en",
            STT_VOCABULARY_PROFILE="backend",
            STT_HOTWORDS="FastAPI,Kubernetes",
            TTS_MODE="v3turbo",
            TTS_DEVICE="cpu",
            TTS_VOICE="interviewer",
            TTS_SAMPLE_RATE=24000,
            SPEECH_SERVICE_TOKEN="internal-secret",
            SPEECH_SERVICE_URL="https://speech.internal",
            SPEECH_BENCHMARK_MODE=True,
            SPEECH_PREWARM_MODELS=True,
            INTERVIEW_PREPARATION_TTL_SECONDS=600,
            INTERVIEW_PREPARATION_MAX_ENTRIES=64,
        )

        self.assertEqual(settings.application.app_env, "test")
        self.assertTrue(settings.application.debug)
        self.assertEqual(settings.google_cloud.project, "sample-project")
        self.assertEqual(settings.google_cloud.location, "asia-southeast1")
        self.assertEqual(settings.llm_routing.simple_model, "gemini-flash-test")
        self.assertEqual(settings.llm_routing.complex_model, "gemini-pro-test")
        self.assertEqual(settings.gemini_resume_model, "gemini-resume-test")
        self.assertEqual(settings.gemini_resume_location, "asia-southeast1")
        self.assertEqual(settings.database.url, "sqlite:///./test.db")
        self.assertEqual(settings.log_level, "DEBUG")
        self.assertEqual(settings.stt_model, "small")
        self.assertEqual(settings.stt_device, "cuda")
        self.assertEqual(settings.stt_compute_type, "float16")
        self.assertEqual(settings.stt_language, "en")
        self.assertEqual(settings.stt_vocabulary_profile, "backend")
        self.assertEqual(settings.stt_hotwords, ["FastAPI", "Kubernetes"])
        self.assertEqual(settings.tts_mode, "v3turbo")
        self.assertEqual(settings.tts_device, "cpu")
        self.assertEqual(settings.tts_voice, "interviewer")
        self.assertEqual(settings.tts_sample_rate, 24000)
        self.assertEqual(settings.speech_service_token, "internal-secret")
        self.assertTrue(settings.speech_benchmark_mode)
        self.assertTrue(settings.speech_prewarm_models)
        self.assertEqual(settings.interview_preparation_ttl_seconds, 600)
        self.assertEqual(settings.interview_preparation_max_entries, 64)
        self.assertEqual(
            settings.speech_service_url,
            "https://speech.internal",
        )

    def test_tts_prewarm_is_disabled_by_default_and_can_be_enabled(self):
        self.assertFalse(Settings(APP_ENV="test").tts_prewarm)
        enabled = Settings(APP_ENV="test", TTS_PREWARM=True)
        self.assertTrue(enabled.tts_prewarm)
        self.assertEqual(enabled.tts_mode, "v3turbo")
        self.assertEqual(enabled.tts_device, "auto")
        self.assertIsNone(enabled.tts_voice)
        self.assertEqual(enabled.tts_sample_rate, 24000)

    def test_auth_and_cors_settings(self):
        settings = Settings(
            APP_ENV="production",
            AUTH_ENABLED=True,
            AUTH_PROVIDER="firebase",
            GOOGLE_CLOUD_PROJECT="fallback-project",
            AUTH_DEV_USER_ID="developer-user",
            CORS_ALLOWED_ORIGINS="https://interview.example.com",
        )

        self.assertTrue(settings.auth_enabled)
        self.assertEqual(settings.auth_provider, "firebase")
        self.assertEqual(settings.firebase_project_id, "fallback-project")
        self.assertEqual(settings.auth_dev_user_id, "developer-user")
        self.assertEqual(settings.cors_allowed_origins, ["https://interview.example.com"])

    def test_candidate_profile_defaults(self):
        profile = CandidateProfile(skills=["Python", "FastAPI"], confidence=0.8)
        self.assertEqual(profile.name, "Candidate")
        self.assertEqual(profile.skills, ["Python", "FastAPI"])
        self.assertEqual(profile.skill_evidence, [])
        self.assertEqual(profile.projects, [])
        self.assertEqual(profile.experiences, [])
        self.assertIsNone(profile.education)
        self.assertIsNone(profile.specialization)
        self.assertEqual(profile.confidence, 0.8)
        self.assertEqual(profile.confidence_score, 0.8)

    def test_candidate_profile_accepts_ai_interview_fields(self):
        profile = CandidateProfile(
            projects=[
                {
                    "name": "CV Interview Assistant",
                    "description": "Built a resume-driven interview flow.",
                    "technologies": ["Python", "FastAPI"],
                    "role": "Backend Developer",
                }
            ],
            experiences=[
                {
                    "company": "Acme AI",
                    "title": "AI Engineer",
                    "start_date": "2023",
                    "end_date": "Present",
                    "description": "Built LLM interview evaluation services.",
                    "technologies": ["Python", "Pydantic"],
                }
            ],
            education=[
                {
                    "institution": "HCMC University of Technology",
                    "degree": "Bachelor",
                    "field_of_study": "Computer Science",
                }
            ],
            specialization="AI interview systems",
            skill_evidence=[
                {
                    "skill": "Python",
                    "evidence": ["Built LLM interview evaluation services."],
                    "source_section": "Experience",
                }
            ],
            confidence_score=0.91,
        )

        self.assertEqual(profile.projects[0].name, "CV Interview Assistant")
        self.assertEqual(profile.skill_evidence[0].skill, "Python")
        self.assertEqual(profile.skill_evidence[0].source_section, "Experience")
        self.assertIsInstance(profile.experiences[0], CandidateExperience)
        self.assertEqual(profile.experiences[0].company, "Acme AI")
        self.assertIsInstance(profile.education[0], CandidateEducation)
        self.assertEqual(profile.education[0].field_of_study, "Computer Science")
        self.assertEqual(profile.specialization, "AI interview systems")
        self.assertEqual(profile.confidence, 0.91)
        self.assertEqual(profile.confidence_score, 0.91)

    def test_candidate_profile_keeps_legacy_education_string(self):
        profile = CandidateProfile(education="Bachelor of Computer Science")
        self.assertEqual(profile.education, "Bachelor of Computer Science")

    def test_interview_plan_schema(self):
        plan = InterviewPlan(
            rounds=[
                InterviewRound(
                    round_id="round-1",
                    topic="Machine Learning",
                    difficulty="medium",
                    reasoning="Candidate has ML project evidence.",
                    recommended_question_areas=["model evaluation", "feature engineering"],
                    weight=0.5,
                )
            ]
        )
        self.assertEqual(plan.rounds[0].topic, "Machine Learning")
        self.assertEqual(plan.rounds[0].reasoning, "Candidate has ML project evidence.")
        self.assertEqual(plan.rounds[0].recommended_question_areas, ["model evaluation", "feature engineering"])

    def test_interview_config_defaults(self):
        config = InterviewConfig(experience_level="junior")
        self.assertEqual(config.language, "vi")
        self.assertEqual(config.duration_minutes, 30)
        self.assertEqual(config.interview_style, "technical")
        self.assertEqual(config.question_count, 10)
        self.assertEqual(config.objective, "Evaluate technical knowledge and practical experience")
        self.assertEqual(config.interviewer_personality, "professional")

    def test_answer_submission_validation(self):
        submission = AnswerSubmission(turn_id="turn-1", answer="A concise answer")
        self.assertEqual(submission.turn_id, "turn-1")

    def test_score_bounds(self):
        score = EvaluationScore(overall_score=7.5)
        self.assertEqual(score.overall_score, 7.5)

    def test_answer_evaluation_adaptive_fields(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=8.0,
            technical_score=8.5,
            communication_score=7.5,
            correctness_score=8.0,
            strengths=["Clear FastAPI explanation"],
            weaknesses=["Limited scaling details"],
            missing_concepts=["dependency override testing"],
            follow_up_needed=True,
            follow_up_reason="Probe testing depth",
            feedback="Good practical answer.",
        )

        self.assertEqual(evaluation.overall_score, 8.0)
        self.assertEqual(evaluation.technical_score, 8.5)
        self.assertEqual(evaluation.communication_score, 7.5)
        self.assertEqual(evaluation.correctness_score, 8.0)
        self.assertEqual(evaluation.missing_concepts, ["dependency override testing"])
        self.assertTrue(evaluation.follow_up_needed)
        self.assertEqual(evaluation.follow_up_reason, "Probe testing depth")
        self.assertEqual(evaluation.feedback, "Good practical answer.")

    def test_answer_evaluation_keeps_legacy_defaults(self):
        evaluation = AnswerEvaluation(turn_id="turn-1")
        self.assertEqual(evaluation.scores.overall_score, 0.0)
        self.assertEqual(evaluation.overall_score, 0.0)
        self.assertEqual(evaluation.technical_score, 0.0)
        self.assertEqual(evaluation.communication_score, 0.0)
        self.assertEqual(evaluation.correctness_score, 0.0)
        self.assertEqual(evaluation.strengths, [])
        self.assertEqual(evaluation.weaknesses, [])
        self.assertEqual(evaluation.missing_concepts, [])
        self.assertFalse(evaluation.follow_up_needed)
        self.assertIsNone(evaluation.follow_up_reason)


class SettingsDefaultConsistencyTests(unittest.TestCase):
    """Every setting is declared twice: once as a model field default and once as
    the fallback in Settings.__init__'s os.getenv call. They silently drifted
    (stt_model said large-v3-turbo on the model and medium in __init__), so the
    running service used a value nobody had chosen. This pins them together.
    """

    def test_speech_defaults_match_the_model_fields(self):
        from core.settings import Settings, SpeechSettings

        settings = Settings()
        for field_name, field in SpeechSettings.model_fields.items():
            if field.default_factory is not None:
                continue
            with self.subTest(field=field_name):
                self.assertEqual(
                    getattr(settings.speech, field_name),
                    field.default,
                    f"SpeechSettings.{field_name} default disagrees with the "
                    f"fallback used in Settings.__init__",
                )

    def test_llm_routing_defaults_match_the_model_fields(self):
        from core.settings import LLMRoutingSettings, Settings

        settings = Settings()
        for field_name, field in LLMRoutingSettings.model_fields.items():
            if field.default_factory is not None:
                continue
            with self.subTest(field=field_name):
                self.assertEqual(
                    getattr(settings.llm_routing, field_name),
                    field.default,
                )


if __name__ == "__main__":
    unittest.main()

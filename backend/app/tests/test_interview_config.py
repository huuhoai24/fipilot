import unittest

from pydantic import ValidationError

from app.schemas import InterviewConfig, InterviewMode


class InterviewConfigTests(unittest.TestCase):
    def test_default_language(self):
        config = InterviewConfig(experience_level="junior")

        self.assertEqual(config.language, "vi")
        self.assertEqual(config.mode, InterviewMode.TEXT)
        self.assertEqual(config.duration_minutes, 30)
        self.assertEqual(config.interview_style, "technical")
        self.assertEqual(config.question_count, 10)
        self.assertEqual(config.objective, "Evaluate technical knowledge and practical experience")

    def test_invalid_language(self):
        with self.assertRaises(ValidationError):
            InterviewConfig(language="fr", experience_level="junior")

    def test_schema_validation(self):
        config = InterviewConfig(
            language="en",
            experience_level="senior",
            duration_minutes=45,
            interview_style="mixed",
            question_count=12,
            objective="Validate CV-backed computer vision experience",
        )

        self.assertEqual(config.language, "en")
        self.assertEqual(config.experience_level, "senior")
        self.assertEqual(config.duration_minutes, 45)
        self.assertEqual(config.interview_style, "mixed")
        self.assertEqual(config.question_count, 12)
        self.assertEqual(config.objective, "Validate CV-backed computer vision experience")

    def test_interview_modes(self):
        voice_config = InterviewConfig(mode="voice", experience_level="middle")

        self.assertEqual(voice_config.mode, InterviewMode.VOICE)
        self.assertEqual(voice_config.model_dump(mode="json")["mode"], "voice")
        with self.assertRaises(ValidationError):
            InterviewConfig(mode="video", experience_level="middle")


if __name__ == "__main__":
    unittest.main()

import unittest

from app.services.language_service import get_language_instruction


class LanguageServiceTests(unittest.TestCase):
    def test_vietnamese_instruction(self):
        instruction = get_language_instruction("vi")

        self.assertIn("The interview language is Vietnamese.", instruction)
        self.assertIn("Ask questions in Vietnamese.", instruction)
        self.assertIn("Keep technical terms", instruction)
        self.assertIn("FastAPI", instruction)

    def test_english_instruction(self):
        instruction = get_language_instruction("en")

        self.assertIn("The interview language is English.", instruction)
        self.assertIn("Ask questions in English.", instruction)
        self.assertIn("Keep technical terms unchanged.", instruction)


if __name__ == "__main__":
    unittest.main()

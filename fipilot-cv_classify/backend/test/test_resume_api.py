import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from api import main as api_main


class StubExtractor:
    def __init__(self, result=None, error: Exception | None = None):
        self.result = result
        self.error = error

    def pipeline(self, _path):
        if self.error is not None:
            raise self.error
        return self.result


class ResumeUploadApiTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(api_main.app)

    def test_corrupt_pdf_is_rejected_without_leaking_temporary_path(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(
            tempfile, "tempdir", directory
        ):
            response = self.client.post(
                "/api/v1/resume/upload",
                files={"file": ("broken.pdf", b"%PDF-corrupt", "application/pdf")},
            )

            self.assertEqual(response.status_code, 422)
            self.assertEqual(
                response.json(),
                {"detail": "The uploaded PDF is malformed or corrupted"},
            )
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_empty_and_invalid_pdf_bytes_are_rejected_before_extraction(self):
        for filename, content in (("empty.pdf", b""), ("invalid.pdf", b"not a pdf")):
            with self.subTest(filename=filename):
                response = self.client.post(
                    "/api/v1/resume/upload",
                    files={"file": (filename, content, "application/pdf")},
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.json(),
                    {"detail": "The uploaded file is not a valid PDF"},
                )

    def test_docx_remains_explicitly_unsupported(self):
        response = self.client.post(
            "/api/v1/resume/upload",
            files={
                "file": (
                    "broken.docx",
                    b"not a docx",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Only PDF files are supported"})

    def test_extractor_failure_returns_controlled_service_error(self):
        extractor = StubExtractor(error=RuntimeError("internal provider secret"))

        with patch("api.main.get_extractor", return_value=extractor):
            response = self.client.post(
                "/api/v1/resume/upload",
                files={"file": ("candidate.pdf", b"%PDF-valid", "application/pdf")},
            )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json(), {"detail": "Resume extraction failed"})
        self.assertNotIn("internal provider secret", response.text)

    def test_valid_pdf_returns_extracted_resume(self):
        profile = {
            "skills": ["Python"],
            "workExperience": [
                {
                    "type": "Project",
                    "name": "Minimal project",
                    "position": "",
                    "jobDescription": "Built a small Python application.",
                }
            ],
            "roleMatches": [],
        }
        extractor = StubExtractor(result=json.dumps(profile))

        with patch("api.main.get_extractor", return_value=extractor):
            response = self.client.post(
                "/api/v1/resume/upload",
                files={"file": ("candidate.pdf", b"%PDF-valid", "application/pdf")},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["profile"], profile)


if __name__ == "__main__":
    unittest.main()

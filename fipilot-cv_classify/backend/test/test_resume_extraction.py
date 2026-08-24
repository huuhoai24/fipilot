import json
import tempfile
import unittest
from pathlib import Path

import pymupdf

from fipilot.pdf_text_extractor import extract_indexed_text_from_pdf
from fipilot.resume_extraction import ResumeExtract


class FakeLLM:
    def __init__(self, response=None):
        self.calls = []
        self.response = response or {
            "skills": ["Python", "FastAPI", "PostgreSQL"],
            "workExperience": [
                {
                    "type": "Work",
                    "name": "FiPilot",
                    "position": "Backend Engineer",
                    "description_refer_index_range": [1, 2],
                }
            ]
        }

    def extract_info(self, text_content, extract_types, resume_id):
        self.calls.append(
            {
                "text_content": text_content,
                "extract_types": extract_types,
                "resume_id": resume_id,
            }
        )
        return self.response


def write_pdf(path: Path, pages: list[list[str]]) -> None:
    document = pymupdf.open()
    for lines in pages:
        page = document.new_page()
        for index, line in enumerate(lines):
            page.insert_text((72, 72 + index * 24), line)
    document.save(path)
    document.close()


class PdfTextExtractorTest(unittest.TestCase):
    def test_extracts_indexed_nonblank_lines_in_page_order(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.pdf"
            write_pdf(path, [["Candidate Name", "FiPilot"], ["Built interview API"]])

            text, index_map = extract_indexed_text_from_pdf(path)

        self.assertEqual(
            index_map,
            {
                0: "Candidate Name",
                1: "FiPilot",
                2: "Built interview API",
            },
        )
        self.assertEqual(
            text,
            "[0]: Candidate Name\n[1]: FiPilot\n[2]: Built interview API",
        )

    def test_rejects_pdf_without_a_text_layer(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scanned.pdf"
            write_pdf(path, [[]])

            with self.assertRaisesRegex(ValueError, "No text layer found"):
                extract_indexed_text_from_pdf(path)


class ResumeExtractTest(unittest.TestCase):
    def test_pipeline_deduplicates_canonically_equivalent_unicode_skills(self):
        fake_llm = FakeLLM(
            {
                "skills": ["Café", "Cafe\u0301", "PYTHON", "python"],
                "workExperience": [
                    {
                        "type": "Project",
                        "name": "Unicode profile",
                        "position": "",
                        "description_refer_index_range": [0, 0],
                    }
                ],
            }
        )

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.pdf"
            write_pdf(path, [["Unicode profile"]])

            result = json.loads(ResumeExtract(llm_client=fake_llm).pipeline(path))

        self.assertEqual(result["skills"], ["Café", "PYTHON"])

    def test_pipeline_bounds_oversized_context_and_preserves_head_tail_evidence(self):
        filler = [f"Filler evidence {index} " + ("x" * 90) for index in range(800)]
        lines = ["Skills: Python FastAPI", *filler, "Senior Backend Engineer led API delivery"]
        last_index = len(lines) - 1
        fake_llm = FakeLLM(
            {
                "skills": ["Python", "FastAPI"],
                "workExperience": [
                    {
                        "type": "Work",
                        "name": "API delivery",
                        "position": "Senior Backend Engineer",
                        "description_refer_index_range": [last_index, last_index],
                    }
                ],
            }
        )

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "oversized.pdf"
            write_pdf(path, [lines[index:index + 8] for index in range(0, len(lines), 8)])

            result = json.loads(ResumeExtract(llm_client=fake_llm).pipeline(path))

        llm_context = fake_llm.calls[0]["text_content"]
        self.assertLessEqual(len(llm_context), 50_000)
        self.assertIn("Skills: Python FastAPI", llm_context)
        self.assertIn("Senior Backend Engineer led API delivery", llm_context)
        self.assertEqual(
            result["workExperience"][0]["jobDescription"],
            "Senior Backend Engineer led API delivery",
        )

    def test_pipeline_uses_pdf_text_and_resolves_description_evidence(self):
        fake_llm = FakeLLM()
        extractor = ResumeExtract(llm_client=fake_llm)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.pdf"
            write_pdf(
                path,
                [["Candidate Name", "FiPilot", "Built interview API"]],
            )

            result = json.loads(extractor.pipeline(path))

        self.assertEqual(len(fake_llm.calls), 1)
        self.assertEqual(fake_llm.calls[0]["extract_types"], ["work_experience"])
        self.assertIn("[2]: Built interview API", fake_llm.calls[0]["text_content"])
        self.assertEqual(
            result["workExperience"][0]["jobDescription"],
            "FiPilot Built interview API",
        )
        self.assertEqual(result["skills"], ["Python", "FastAPI", "PostgreSQL"])
        self.assertEqual(result["roleMatches"][0]["id"], "backend-developer")
        self.assertEqual(sum(match["score"] for match in result["roleMatches"]), 100)
        self.assertNotIn(
            "description_refer_index_range",
            result["workExperience"][0],
        )

    def test_pipeline_rejects_an_evidence_range_outside_the_resume(self):
        fake_llm = FakeLLM(
            {
                "workExperience": [
                    {
                        "type": "Project",
                        "name": "FiPilot",
                        "position": "",
                        "description_refer_index_range": [0, 99],
                    }
                ]
            }
        )

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.pdf"
            write_pdf(path, [["FiPilot", "Built interview API"]])

            with self.assertRaisesRegex(ValueError, "invalid evidence index range"):
                ResumeExtract(llm_client=fake_llm).pipeline(path)

    def test_pipeline_rejects_a_resume_without_interviewable_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.pdf"
            write_pdf(path, [["Candidate Name"]])

            with self.assertRaisesRegex(ValueError, "No work or project evidence"):
                ResumeExtract(
                    llm_client=FakeLLM({"workExperience": []})
                ).pipeline(path)


if __name__ == "__main__":
    unittest.main()

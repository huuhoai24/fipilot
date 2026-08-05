import json
import tempfile
import unittest
from pathlib import Path

from services.interview_knowledge.local import LocalKnowledgeRetriever
from shared.schemas import CandidateProfile, InterviewConfig


class LocalKnowledgeRetrieverTests(unittest.TestCase):
    def test_retrieves_candidate_specific_topics_and_level_guidance(self):
        catalog = {
            "version": 1,
            "domains": {
                "AI_Engineer": [
                    {
                        "title": "TensorRT",
                        "path": ["AI Deployment", "Model Serving Runtimes"],
                        "anchors": ["FP16 and INT8 optimization", "latency and accuracy trade-offs"],
                    },
                    {
                        "title": "Linear Regression",
                        "path": ["Machine Learning", "Regression"],
                        "anchors": ["least squares"],
                    },
                ]
            },
            "levels": {
                "AI_Engineer": {
                    "Junior": [
                        "Explain operating mechanisms.",
                        "Compare accuracy, speed, and complexity trade-offs.",
                    ]
                }
            },
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            catalog_path = Path(temp_dir) / "catalog.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            retriever = LocalKnowledgeRetriever(catalog_path=catalog_path, topic_limit=2)

            topics = retriever.retrieve_topics(
                CandidateProfile(
                    name="Candidate",
                    recent_role="AI Engineer",
                    specialization="Computer Vision",
                    skills=["YOLOv8", "TensorRT"],
                    skill_evidence=[
                        {
                            "skill": "TensorRT",
                            "evidence": ["Converted a YOLOv8 model to TensorRT with FP16."],
                            "source_section": "Projects",
                        }
                    ],
                ),
                InterviewConfig(language="vi", experience_level="junior"),
            )

        joined = "\n".join(topics)
        self.assertIn("Domain: AI Engineer", joined)
        self.assertIn("TensorRT", joined)
        self.assertIn("operating mechanisms", joined)
        self.assertNotIn("Linear Regression", joined)


if __name__ == "__main__":
    unittest.main()

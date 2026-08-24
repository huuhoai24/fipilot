import unittest

from fipilot.role_matching import ROLE_TAXONOMY, infer_candidate_role, match_resume_roles


class RoleMatchingTest(unittest.TestCase):
    def test_role_fix_01_frontend_tasks_dominate_conflicting_backend_title(self):
        inference = infer_candidate_role(
            skills=[],
            work_experience=[
                {
                    "type": "Work",
                    "name": "Web app",
                    "position": "Backend Developer",
                    "jobDescription": "Implemented React UI, CSS, accessibility and browser state.",
                }
            ],
        )

        self.assertEqual(inference["title_role"], "Backend Developer")
        self.assertEqual(inference["task_role"], "Web Developer")
        self.assertEqual(inference["effective_role"], "Web Developer")
        self.assertTrue(inference["conflict"])

    def test_role_fix_02_ai_tasks_dominate_conflicting_data_engineer_title(self):
        inference = infer_candidate_role(
            skills=[],
            work_experience=[
                {
                    "type": "Work",
                    "name": "ML pipeline",
                    "position": "Data Engineer",
                    "jobDescription": "Trained neural models with PyTorch and computer vision evaluation.",
                }
            ],
        )

        self.assertEqual(inference["title_role"], "Data Engineer")
        self.assertEqual(inference["task_role"], "AI Engineer")
        self.assertEqual(inference["effective_role"], "AI Engineer")
        self.assertTrue(inference["conflict"])

    def test_role_fix_03_absent_role_evidence_remains_unknown(self):
        inference = infer_candidate_role(
            skills=[],
            work_experience=[
                {
                    "type": "Project",
                    "name": "Tool",
                    "position": "Enginer",
                    "jobDescription": "Improved an internal workflow.",
                }
            ],
        )

        self.assertEqual(inference["effective_role"], "Unknown")
        self.assertEqual(inference["confidence"], "none")
        self.assertFalse(inference["conflict"])

    def test_catalog_covers_the_ten_knowledge_domains(self):
        expected_roles = {
            "AI Engineer",
            "Backend Developer",
            "Business Analyst",
            "Data Engineer",
            "Data Scientist",
            "DevOps Engineer",
            "Full Stack Developer",
            "Software Engineer",
            "Tester QA QC",
            "Web Developer",
        }

        self.assertEqual(len(ROLE_TAXONOMY), 10)
        self.assertEqual({role["title"] for role in ROLE_TAXONOMY}, expected_roles)

    def test_each_knowledge_role_can_be_matched_from_distinct_resume_evidence(self):
        cases = {
            "ai-engineer": ("AI Engineer", "PyTorch"),
            "backend-developer": ("Backend Developer", "FastAPI"),
            "business-analyst": ("Business Analyst", "BPMN"),
            "data-engineer": ("Data Engineer", "Apache Airflow"),
            "data-scientist": ("Data Scientist", "Hypothesis Testing"),
            "devops-engineer": ("DevOps Engineer", "Terraform"),
            "full-stack-developer": ("Full Stack Developer", "MERN"),
            "software-engineer": ("Software Engineer", "Data Structures"),
            "tester-qa-qc": ("QA Engineer", "Selenium"),
            "web-developer": ("Web Developer", "WordPress"),
        }

        for expected_id, (position, skill) in cases.items():
            with self.subTest(role=expected_id):
                matches = match_resume_roles(
                    skills=[skill],
                    work_experience=[
                        {
                            "type": "Work",
                            "name": f"{position} delivery",
                            "position": position,
                            "jobDescription": f"Applied {skill} in production.",
                        }
                    ],
                )

                match = next(item for item in matches if item["id"] == expected_id)
                self.assertEqual(match["relevantExperienceIndexes"], [0])

    def test_returns_normalized_role_evidence_shares(self):
        matches = match_resume_roles(
            skills=[
                "Python", "PyTorch", "TensorFlow", "Machine Learning",
                "Computer Vision", "FastAPI", "PostgreSQL",
            ],
            work_experience=[
                {
                    "type": "Project",
                    "name": "Vision assistant",
                    "position": "AI Engineer",
                    "jobDescription": (
                        "Trained PyTorch and TensorFlow deep learning computer vision models, "
                        "then deployed model inference behind a FastAPI service."
                    ),
                },
                {
                    "type": "Work",
                    "name": "Platform team",
                    "position": "Backend Engineer",
                    "jobDescription": "Built REST APIs with FastAPI and PostgreSQL.",
                },
            ],
        )

        self.assertGreaterEqual(len(matches), 2)
        self.assertEqual(sum(match["score"] for match in matches), 100)
        self.assertEqual(matches[0]["id"], "ai-engineer")
        backend = next(match for match in matches if match["id"] == "backend-developer")
        self.assertIn("FastAPI", backend["matchedSkills"])
        self.assertEqual(backend["relevantExperienceIndexes"], [0, 1])

    def test_excludes_roles_without_resume_evidence(self):
        matches = match_resume_roles(
            skills=["React", "TypeScript", "CSS"],
            work_experience=[
                {
                    "type": "Project",
                    "name": "Candidate portal",
                    "position": "Frontend Developer",
                    "jobDescription": "Built accessible React screens with TypeScript and CSS.",
                }
            ],
        )

        self.assertEqual(matches[0]["id"], "web-developer")
        self.assertNotIn("ai-engineer", {match["id"] for match in matches})
        self.assertNotIn("backend-developer", {match["id"] for match in matches})

    def test_returns_empty_list_when_no_role_signal_exists(self):
        self.assertEqual(
            match_resume_roles(
                skills=[],
                work_experience=[
                    {
                        "type": "Work",
                        "name": "Community club",
                        "position": "Volunteer",
                        "jobDescription": "Organized weekly member events.",
                    }
                ],
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()

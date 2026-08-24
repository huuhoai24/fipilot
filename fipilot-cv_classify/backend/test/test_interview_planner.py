import unittest

from fipilot.interview_planner import create_interview_plan


class FakeRetriever:
    def __init__(self):
        self.calls = []

    def __call__(self, query: str, role: str, top_k: int):
        self.calls.append({"query": query, "role": role, "top_k": top_k})
        return [
            {
                "source": "Domains/Backend Developer/Database/PostgreSQL.md",
                "path": "Domains/Backend Developer/Database/PostgreSQL.md",
                "content": "# PostgreSQL\nTransactions, rollback, isolation, and indexes.",
                "score": 0.82,
                "method": "lexical",
            }
        ]


class InterviewPlannerTest(unittest.TestCase):
    def test_flow_reg_empty_null_and_missing_experience_produce_no_rounds(self):
        empty = create_interview_plan(
            work_experience=[],
            role="Backend Developer",
            level="Senior",
            retrieve=lambda *_args: [],
        )
        null = create_interview_plan(
            work_experience=None,
            role="Backend Developer",
            level="Senior",
            retrieve=lambda *_args: [],
        )
        missing = create_interview_plan(
            role="Backend Developer",
            level="Senior",
            retrieve=lambda *_args: [],
        )
        malformed = create_interview_plan(
            work_experience=[{}],
            role="Backend Developer",
            level="Senior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(empty["rounds"], [])
        self.assertEqual(null["rounds"], [])
        self.assertEqual(missing["rounds"], [])
        self.assertEqual(malformed["rounds"], [])

    def test_flow_reg_student_project_remains_interviewable(self):
        plan = create_interview_plan(
            work_experience=[
                {
                    "type": "Project",
                    "name": "University capstone",
                    "position": "",
                    "jobDescription": "Built a Python scheduling application.",
                }
            ],
            role="Backend Developer",
            level="Junior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(len(plan["rounds"]), 1)
        self.assertEqual(plan["rounds"][0]["evidence_index"], 0)
        self.assertEqual(plan["rounds"][0]["difficulty"], "medium")

    def test_plan_reg_01_react_fresher_is_not_treated_as_senior_data_engineer(self):
        plan = create_interview_plan(
            work_experience=[
                {
                    "type": "Project",
                    "name": "React portfolio",
                    "position": "Frontend Developer",
                    "jobDescription": "Built React and CSS screens.",
                }
            ],
            role="Data Engineer",
            level="Senior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(plan["rounds"][0]["role"], "Web Developer")
        self.assertEqual(plan["rounds"][0]["level"], "Junior")
        self.assertEqual(plan["rounds"][0]["difficulty"], "medium")
        self.assertIn("mismatch", plan["rounds"][0]["reasoning"].casefold())
        self.assertIn("without assuming Data Engineer experience", plan["rounds"][0]["objective"])

    def test_builds_traceable_rounds_from_role_focused_resume_and_rag(self):
        retriever = FakeRetriever()
        plan = create_interview_plan(
            work_experience=[
                {
                    "type": "Work",
                    "name": "Platform API",
                    "position": "Backend Engineer",
                    "jobDescription": "Built FastAPI endpoints with PostgreSQL transactions.",
                }
            ],
            role="Backend Developer",
            level="Junior",
            retrieve=retriever,
        )

        self.assertEqual(plan["role"], "Backend Developer")
        self.assertEqual(plan["rounds"][0]["round_id"], "round-1")
        self.assertEqual(plan["rounds"][0]["evidence_index"], 0)
        self.assertEqual(plan["rounds"][0]["topic"], "PostgreSQL")
        self.assertEqual(plan["rounds"][0]["difficulty"], "medium")
        self.assertEqual(
            plan["rounds"][0]["knowledge"][0]["source"],
            "Domains/Backend Developer/Database/PostgreSQL.md",
        )
        self.assertIn("Backend Developer", retriever.calls[0]["query"])
        self.assertIn("FastAPI endpoints", retriever.calls[0]["query"])
        self.assertEqual(retriever.calls[0]["top_k"], 3)

    def test_plan_keeps_resume_evidence_when_rag_has_no_match(self):
        plan = create_interview_plan(
            work_experience=[
                {
                    "type": "Project",
                    "name": "Internal gateway",
                    "position": "",
                    "jobDescription": "Implemented a custom request routing mechanism.",
                }
            ],
            role="Backend Developer",
            level="Junior",
            retrieve=lambda *_args, **_kwargs: [],
        )

        self.assertEqual(plan["rounds"][0]["topic"], "Internal gateway")
        self.assertEqual(plan["rounds"][0]["difficulty"], "medium")
        self.assertEqual(plan["rounds"][0]["knowledge"], [])

    def test_plan_reg_02_senior_backend_evidence_is_not_downgraded_for_missing_name(self):
        plan = create_interview_plan(
            work_experience=[
                {
                    "type": "Work",
                    "name": "",
                    "position": "Senior Backend Engineer",
                    "jobDescription": "Led FastAPI and PostgreSQL platform delivery.",
                }
            ],
            role="Backend Developer",
            level="Senior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(plan["rounds"][0]["role"], "Backend Developer")
        self.assertEqual(plan["rounds"][0]["level"], "Senior")
        self.assertEqual(plan["rounds"][0]["difficulty"], "hard")
        self.assertNotIn("mismatch", plan["rounds"][0]["reasoning"].casefold())

    def test_plan_reg_03_cv_and_target_job_role_mismatch_is_explicit(self):
        plan = create_interview_plan(
            work_experience=[
                {
                    "type": "Work",
                    "name": "Web product",
                    "position": "Frontend Developer",
                    "jobDescription": "Built accessible React user interfaces.",
                }
            ],
            role="Backend Developer",
            level="Senior",
            job_description="Senior backend role building Python APIs.",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(plan["rounds"][0]["role"], "Web Developer")
        self.assertEqual(plan["rounds"][0]["level"], "Junior")
        self.assertEqual(plan["rounds"][0]["difficulty"], "medium")
        self.assertIn("role mismatch", plan["rounds"][0]["reasoning"].casefold())
        self.assertIn("without assuming Backend Developer experience", plan["rounds"][0]["objective"])

    def test_role_fix_04_project_only_candidate_is_entry_level(self):
        plan = create_interview_plan(
            work_experience=[
                {
                    "type": "Project",
                    "name": "Portfolio",
                    "position": "Frontend Developer",
                    "jobDescription": "Built React screens.",
                }
            ],
            role="Web Developer",
            level="Senior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(plan["candidate_level"], "Entry")
        self.assertEqual(plan["target_level"], "Senior")
        self.assertEqual(plan["rounds"][0]["candidate_level"], "Entry")

    def test_role_fix_05_requested_senior_does_not_become_candidate_level(self):
        plan = create_interview_plan(
            work_experience=[
                {
                    "type": "Project",
                    "name": "Tool",
                    "position": "Enginer",
                    "jobDescription": "Improved an internal workflow.",
                }
            ],
            role="Data Engineer",
            level="Senior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(plan["candidate_role"], "Unknown")
        self.assertNotEqual(plan["candidate_level"], "Senior")
        self.assertEqual(plan["target_role"], "Data Engineer")
        self.assertEqual(plan["target_level"], "Senior")

    def test_role_fix_06_project_scope_remains_project(self):
        plan = create_interview_plan(
            work_experience=[
                {"type": "Project", "name": "Tool", "position": "", "jobDescription": "Built a utility."}
            ],
            role="Software Engineer",
            level="Junior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(plan["rounds"][0]["candidate_scope"], "Project")

    def test_role_fix_07_prototype_scope_remains_prototype(self):
        plan = create_interview_plan(
            work_experience=[
                {"type": "Project", "name": "Search", "position": "", "jobDescription": "Built a local prototype."}
            ],
            role="Software Engineer",
            level="Junior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(plan["rounds"][0]["candidate_scope"], "Prototype")

    def test_role_fix_08_academic_project_scope_remains_academic(self):
        plan = create_interview_plan(
            work_experience=[
                {"type": "Project", "name": "Capstone", "position": "Student", "jobDescription": "Built a university coursework project."}
            ],
            role="Software Engineer",
            level="Junior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(plan["rounds"][0]["candidate_scope"], "Academic")


if __name__ == "__main__":
    unittest.main()

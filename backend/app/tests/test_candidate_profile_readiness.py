from __future__ import annotations

import unittest

from services.candidate_profile.readiness import evaluate_interview_readiness
from shared.schemas import CandidateProfile


class CandidateProfileReadinessTests(unittest.TestCase):
    def test_returns_every_missing_minimum_requirement(self) -> None:
        readiness = evaluate_interview_readiness(
            CandidateProfile(
                name="Candidate",
                skills=[],
                skill_evidence=[],
                projects=[],
                experiences=[],
                education=None,
            )
        )

        self.assertFalse(readiness.is_ready)
        self.assertEqual(
            [issue.model_dump(exclude_none=True) for issue in readiness.issues],
            [
                {
                    "code": "fallback_name",
                    "origin": "interview_readiness",
                    "field_path": "name",
                },
                {
                    "code": "missing_skills",
                    "origin": "interview_readiness",
                    "field_path": "skills",
                },
                {
                    "code": "missing_interviewable_evidence",
                    "origin": "interview_readiness",
                    "field_path": "skill_evidence",
                },
            ],
        )

    def test_every_approved_evidence_source_can_make_profile_ready(self) -> None:
        evidence_profiles = {
            "skill evidence": CandidateProfile(
                name="Nguyen An",
                skills=["Python"],
                skill_evidence=[
                    {
                        "skill": "Python",
                        "evidence": ["Built an authenticated interview API."],
                    }
                ],
            ),
            "project": CandidateProfile(
                name="Nguyen An",
                skills=["Python"],
                projects=[{"name": "Interview practice API"}],
            ),
            "experience": CandidateProfile(
                name="Nguyen An",
                skills=["Python"],
                experiences=[{"title": "Backend Engineering Intern"}],
            ),
            "education degree": CandidateProfile(
                name="Nguyen An",
                skills=["Python"],
                education=[
                    {
                        "institution": "HCMC University of Technology",
                        "degree": "Bachelor of Engineering",
                    }
                ],
            ),
            "education field": CandidateProfile(
                name="Nguyen An",
                skills=["Python"],
                education=[
                    {
                        "institution": "HCMC University of Technology",
                        "field_of_study": "Computer Science",
                    }
                ],
            ),
        }

        for evidence_kind, profile in evidence_profiles.items():
            with self.subTest(evidence_kind=evidence_kind):
                readiness = evaluate_interview_readiness(profile)
                self.assertTrue(readiness.is_ready)
                self.assertEqual(readiness.issues, [])

    def test_profile_validity_issues_remain_distinct_from_readiness_issues(self) -> None:
        readiness = evaluate_interview_readiness(
            CandidateProfile(
                name="Nguyen An",
                years_experience=-0.5,
                skills=["Python"],
                skill_evidence=[
                    {
                        "skill": "Rust",
                        "evidence": ["Built a command-line tool."],
                    }
                ],
                projects=[{}],
                experiences=[{}],
                education=[{}],
            )
        )

        self.assertFalse(readiness.is_ready)
        self.assertEqual(
            [issue.model_dump(exclude_none=True) for issue in readiness.issues],
            [
                {
                    "code": "invalid_years_experience",
                    "origin": "profile_validity",
                    "field_path": "years_experience",
                },
                {
                    "code": "evidence_skill_not_found",
                    "origin": "profile_validity",
                    "field_path": "skill_evidence.0.skill",
                },
                {
                    "code": "empty_nested_entry",
                    "origin": "profile_validity",
                    "field_path": "projects.0",
                },
                {
                    "code": "empty_nested_entry",
                    "origin": "profile_validity",
                    "field_path": "experiences.0",
                },
                {
                    "code": "empty_nested_entry",
                    "origin": "profile_validity",
                    "field_path": "education.0",
                },
            ],
        )

    def test_uses_nfkc_and_unicode_whitespace_for_readiness(self) -> None:
        readiness = evaluate_interview_readiness(
            CandidateProfile(
                name="  ＣＡＮＤＩＤＡＴＥ  ",
                skills=["\u00a0Ｐｙｔｈｏｎ\t"],
                projects=[{"description": "  Built an API.  "}],
            )
        )

        self.assertFalse(readiness.is_ready)
        self.assertEqual(
            [issue.code for issue in readiness.issues],
            ["fallback_name"],
        )

    def test_legacy_or_incomplete_education_does_not_supply_evidence(self) -> None:
        education_values = [
            "Bachelor of Computer Science",
            [{"degree": "Bachelor of Engineering"}],
            [{"institution": "HCMC University of Technology"}],
        ]

        for education in education_values:
            with self.subTest(education=education):
                readiness = evaluate_interview_readiness(
                    CandidateProfile(
                        name="Nguyen An",
                        skills=["Python"],
                        education=education,
                    )
                )
                self.assertFalse(readiness.is_ready)
                self.assertEqual(
                    [issue.code for issue in readiness.issues],
                    ["missing_interviewable_evidence"],
                )

    def test_issues_follow_the_approved_profile_section_order(self) -> None:
        readiness = evaluate_interview_readiness(
            CandidateProfile(
                name="Nguyen An",
                skills=["Python"],
                projects=[{}],
                experiences=[{}],
                education=[{}],
            )
        )

        self.assertEqual(
            [
                (issue.code, issue.field_path)
                for issue in readiness.issues
            ],
            [
                ("missing_interviewable_evidence", "skill_evidence"),
                ("empty_nested_entry", "projects.0"),
                ("empty_nested_entry", "experiences.0"),
                ("empty_nested_entry", "education.0"),
            ],
        )


if __name__ == "__main__":
    unittest.main()

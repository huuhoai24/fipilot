import json
import unittest

from pydantic import ValidationError

from fipilot.interview_engine import evaluate_answer, generate_question, generate_report


class FakeLLM:
    def __init__(self, *responses: dict):
        self.responses = iter(responses)

    def generate_text(self, *_args, **_kwargs) -> str:
        return json.dumps(next(self.responses), ensure_ascii=False)


class CapturingLLM(FakeLLM):
    def __init__(self, *responses: dict):
        super().__init__(*responses)
        self.calls = []

    def generate_text(self, system_prompt, user_prompt, **kwargs) -> str:
        self.calls.append({"system_prompt": system_prompt, "user_prompt": user_prompt})
        return super().generate_text(system_prompt, user_prompt, **kwargs)


QUESTION = {
    "company": "FiPilot",
    "project": "FiPilot",
    "topic": "Cache consistency",
    "question": "Bạn xử lý dữ liệu cache cũ như thế nào?",
    "rubric": {
        "evaluation_goal": "Đánh giá cách xử lý cache consistency",
        "critical_points": ["Nhận diện stale data", "Có chiến lược invalidation"],
        "met": "Giải thích đúng cơ chế và trade-off.",
        "partially_met": "Đúng hướng nhưng thiếu cơ chế hoặc trade-off.",
        "not_met": "Không nhận diện stale data hoặc trả lời sai.",
    },
}

ASSUMED_EXPERIENCE_QUESTION = {
    "company": "Candidate profile",
    "topic": "Kubernetes",
    "question": "How did you use Kubernetes in production?",
    "rubric": {
        "evaluation_goal": "Assess Kubernetes production operations",
        "critical_points": ["Deployment", "Observability", "Failure recovery"],
        "met": "Explains mechanisms and trade-offs.",
        "partially_met": "Explains some mechanisms.",
        "not_met": "Cannot explain Kubernetes operations.",
    },
}


class InterviewEngineTest(unittest.TestCase):
    def test_eval_lang_01_english_rubric_accepts_correct_vietnamese_answer(self):
        answer = (
            "Mỗi lần thử lại dùng cùng một mã yêu cầu. Dịch vụ kiểm tra kết quả đã lưu "
            "nên không thực hiện tác dụng phụ lần thứ hai."
        )
        question = {
            "company": "Synthetic",
            "topic": "Safe operation retries",
            "question": "How does the service safely process a retried operation?",
            "rubric": {
                "evaluation_goal": "Explain safe retry behavior",
                "critical_points": [
                    "Reuse a stable request identity",
                    "Return a previously stored result",
                    "Prevent duplicate side effects",
                ],
                "met": "Explains how a stable identity makes retries safe.",
                "partially_met": "Explains only one part of retry safety.",
                "not_met": "Describes unsafe or unrelated behavior.",
            },
        }
        llm = CapturingLLM(
            {
                "score": 3,
                "evidence_quote": answer,
                "justification": "Câu trả lời tiếng Việt diễn đạt đầy đủ technical meaning.",
                "should_follow_up": False,
                "next_direction": "",
                "matched_points": question["rubric"]["critical_points"],
                "missing_points": [],
                "technical_errors": [],
            }
        )

        result = evaluate_answer(llm, question, answer)

        self.assertEqual(result["status"], "MET")
        self.assertIn('"semantic_evidence_policy"', llm.calls[0]["user_prompt"])
        self.assertIn('"criterion_id": "CP-1"', llm.calls[0]["user_prompt"])
        self.assertIn("silently normalize the rubric and answer into language-neutral technical claims", llm.calls[0]["system_prompt"])

    def test_eval_lang_02_mixed_language_correct_answer_is_met(self):
        answer = (
            "Client reuse cùng request identity; service trả saved result khi retry "
            "nên không tạo side effect lần hai."
        )
        question = {
            "topic": "Safe operation retries",
            "question": "Explain how retried operations remain safe.",
            "rubric": {
                "evaluation_goal": "Explain safe retry behavior",
                "critical_points": ["Stable identity", "Stored result", "No duplicate effect"],
                "met": "Connects stable identity to safe repeated execution.",
                "partially_met": "Explains only one mechanism.",
                "not_met": "Incorrect or unrelated explanation.",
            },
        }
        result = evaluate_answer(
            FakeLLM(
                {
                    "score": 3,
                    "evidence_quote": answer,
                    "justification": "Mixed-language answer is technically complete.",
                    "should_follow_up": False,
                    "next_direction": "",
                    "matched_points": question["rubric"]["critical_points"],
                    "missing_points": [],
                    "technical_errors": [],
                }
            ),
            question,
            answer,
        )

        self.assertEqual((result["score"], result["status"]), (8, "MET"))

    def test_eval_lang_03_correct_concept_without_shared_rubric_keywords_is_met(self):
        answer = "Khi thao tác lỗi, khối cuối cùng luôn đóng tài nguyên nên không bị rò rỉ."
        question = {
            "topic": "Resource safety",
            "question": "How are resources released after an unsuccessful operation?",
            "rubric": {
                "evaluation_goal": "Explain guaranteed resource cleanup",
                "critical_points": ["Cleanup executes on failure", "Open handles are released"],
                "met": "Explains unconditional cleanup after failure.",
                "partially_met": "Mentions cleanup without failure behavior.",
                "not_met": "Leaves resources open or is unrelated.",
            },
        }
        result = evaluate_answer(
            FakeLLM(
                {
                    "score": 3,
                    "evidence_quote": answer,
                    "justification": "Different terminology expresses the complete mechanism.",
                    "should_follow_up": False,
                    "next_direction": "",
                    "matched_points": question["rubric"]["critical_points"],
                    "missing_points": [],
                    "technical_errors": [],
                }
            ),
            question,
            answer,
        )

        self.assertEqual(result["status"], "MET")

    def test_eval_lang_04_rubric_keywords_with_wrong_explanation_stay_low(self):
        answer = "Transaction rollback means committing every partial change after an error."
        question = {
            "topic": "Failure atomicity",
            "question": "What does transaction rollback accomplish?",
            "rubric": {
                "evaluation_goal": "Explain failure atomicity",
                "critical_points": ["Rollback discards partial changes", "State remains consistent"],
                "met": "Correctly explains atomic failure behavior.",
                "partially_met": "Recognizes rollback but lacks the effect.",
                "not_met": "Claims partial changes are committed.",
            },
        }
        result = evaluate_answer(
            FakeLLM(
                {
                    "score": 2,
                    "evidence_quote": answer,
                    "justification": "The keywords are present but the mechanism is wrong.",
                    "should_follow_up": False,
                    "next_direction": "",
                    "matched_points": [],
                    "missing_points": question["rubric"]["critical_points"],
                    "technical_errors": ["Incorrectly says rollback commits partial changes."],
                }
            ),
            question,
            answer,
        )

        self.assertEqual((result["score"], result["status"]), (2, "NOT_MET"))
        self.assertTrue(result["technical_errors"])

    def test_eval_lang_05_long_unrelated_terminology_stays_low(self):
        answer = ("monitoring metrics tracing schema queue compiler rendering " * 40).strip()
        question = {
            "topic": "Failure atomicity",
            "question": "How are partial writes prevented after failure?",
            "rubric": {
                "evaluation_goal": "Explain atomic failure handling",
                "critical_points": ["Discard partial writes", "Preserve prior state"],
                "met": "Explains the failure mechanism and its effect.",
                "partially_met": "Mentions one relevant mechanism.",
                "not_met": "Keyword listing or unrelated answer.",
            },
        }
        result = evaluate_answer(
            FakeLLM(
                {
                    "score": 1,
                    "evidence_quote": "monitoring metrics tracing",
                    "justification": "Long answer contains no relevant technical explanation.",
                    "should_follow_up": False,
                    "next_direction": "",
                    "matched_points": [],
                    "missing_points": question["rubric"]["critical_points"],
                    "technical_errors": [],
                }
            ),
            question,
            answer,
        )

        self.assertEqual((result["score"], result["status"]), (1, "NOT_MET"))

    def test_eval_lang_06_same_meaning_different_terminology_is_equivalent(self):
        first_answer = "After failure, the finalizer closes every open handle."
        second_answer = "Nếu xử lý thất bại, bước kết thúc vẫn giải phóng toàn bộ tài nguyên đang mở."
        question = {
            "topic": "Resource safety",
            "question": "How does cleanup remain reliable after failure?",
            "rubric": {
                "evaluation_goal": "Explain reliable resource cleanup",
                "critical_points": ["Cleanup runs after failure", "Resources are released"],
                "met": "Explains guaranteed cleanup and release.",
                "partially_met": "Mentions cleanup without guarantee.",
                "not_met": "Incorrect or unrelated behavior.",
            },
        }
        llm = FakeLLM(
            {
                "score": 3,
                "evidence_quote": first_answer,
                "justification": "Complete explanation.",
                "should_follow_up": False,
                "next_direction": "",
                "matched_points": question["rubric"]["critical_points"],
                "missing_points": [],
                "technical_errors": [],
            },
            {
                "score": 3,
                "evidence_quote": second_answer,
                "justification": "Cùng một technical meaning.",
                "should_follow_up": False,
                "next_direction": "",
                "matched_points": question["rubric"]["critical_points"],
                "missing_points": [],
                "technical_errors": [],
            },
        )

        first = evaluate_answer(llm, question, first_answer)
        second = evaluate_answer(llm, question, second_answer)

        self.assertEqual(
            (first["score"], first["status"]),
            (second["score"], second["status"]),
        )

    def test_score10_03_full_coverage_without_errors_reaches_strong_range(self):
        answer = "A stable operation identity returns the prior result and avoids repeated effects."
        question = {
            "topic": "Safe retries",
            "question": "How are retried operations kept safe?",
            "rubric": {
                "evaluation_goal": "Explain safe retry behavior",
                "critical_points": [
                    "Stable operation identity",
                    "Prior result is reused",
                    "Repeated side effects are prevented",
                ],
                "met": "Explains the complete safe-retry mechanism.",
                "partially_met": "Explains only part of the mechanism.",
                "not_met": "Incorrect or unrelated explanation.",
            },
        }
        result = evaluate_answer(
            FakeLLM(
                {
                    "score": 4,
                    "evidence_quote": answer,
                    "justification": "All canonical criteria are supported.",
                    "should_follow_up": True,
                    "next_direction": "Add more detail.",
                    "matched_points": question["rubric"]["critical_points"],
                    "missing_points": [],
                    "technical_errors": [],
                }
            ),
            question,
            answer,
        )

        self.assertEqual(result["raw_llm_score"], 4)
        self.assertEqual(
            (result["score"], result["validated_score"], result["final_score"]),
            (8, 8, 8),
        )
        self.assertEqual(result["score_scale"], 10)
        self.assertEqual(result["status"], "MET")
        self.assertIn("strong range", result["score_correction_reason"])

    def test_score10_04_full_coverage_with_technical_error_is_not_maximum(self):
        answer = "The mechanism is described, but one stated consequence is technically wrong."
        question = self._score_consistency_question()
        result = evaluate_answer(
            FakeLLM(
                self._score_consistency_response(
                    score=10,
                    answer=answer,
                    matched=question["rubric"]["critical_points"],
                    missing=[],
                    errors=["One consequence contradicts the mechanism."],
                )
            ),
            question,
            answer,
        )

        self.assertEqual((result["raw_llm_score"], result["score"]), (10, 7))
        self.assertEqual(result["status"], "MET")

    def test_score10_05_two_of_three_criteria_can_remain_partial(self):
        answer = "The answer supports two of the three required mechanisms."
        question = self._score_consistency_question()
        result = evaluate_answer(
            FakeLLM(
                self._score_consistency_response(
                    score=6,
                    answer=answer,
                    matched=question["rubric"]["critical_points"][:2],
                    missing=question["rubric"]["critical_points"][2:],
                    errors=[],
                )
            ),
            question,
            answer,
        )

        self.assertEqual((result["raw_llm_score"], result["score"]), (6, 6))
        self.assertEqual(result["score_correction_reason"], "")

    def test_score10_06_zero_of_three_criteria_remains_low(self):
        answer = "I do not know how this mechanism works."
        question = self._score_consistency_question()
        result = evaluate_answer(
            FakeLLM(
                self._score_consistency_response(
                    score=2,
                    answer=answer,
                    matched=[],
                    missing=question["rubric"]["critical_points"],
                    errors=[],
                )
            ),
            question,
            answer,
        )

        self.assertEqual((result["raw_llm_score"], result["score"]), (2, 2))
        self.assertEqual(result["status"], "NOT_MET")

    def test_score_consist_05_keywords_with_technical_error_remain_low(self):
        answer = "Identity stored result side effects, but repetition always creates extra effects."
        question = self._score_consistency_question()
        result = evaluate_answer(
            FakeLLM(
                self._score_consistency_response(
                    score=2,
                    answer=answer,
                    matched=[],
                    missing=question["rubric"]["critical_points"],
                    errors=["Claims repeated execution creates the effect again."],
                )
            ),
            question,
            answer,
        )

        self.assertEqual((result["raw_llm_score"], result["score"]), (2, 2))
        self.assertTrue(result["technical_errors"])

    def test_score_consist_06_consistent_raw_score_is_not_changed(self):
        answer = "One identity reuses the prior result, preventing repeated effects."
        question = self._score_consistency_question()
        result = evaluate_answer(
            FakeLLM(
                self._score_consistency_response(
                    score=9,
                    answer=answer,
                    matched=question["rubric"]["critical_points"],
                    missing=[],
                    errors=[],
                )
            ),
            question,
            answer,
        )

        self.assertEqual((result["raw_llm_score"], result["score"]), (9, 9))
        self.assertEqual(result["score_correction_reason"], "")

    def test_score10_01_negative_score_is_rejected(self):
        question = self._score_consistency_question()
        with self.assertRaises(ValidationError):
            evaluate_answer(
                FakeLLM(
                    self._score_consistency_response(
                        score=-1,
                        answer="invalid negative score",
                        matched=[],
                        missing=question["rubric"]["critical_points"],
                        errors=[],
                    )
                ),
                question,
                "invalid negative score",
            )

    def test_score10_02_score_above_ten_is_rejected(self):
        question = self._score_consistency_question()
        with self.assertRaises(ValidationError):
            evaluate_answer(
                FakeLLM(
                    self._score_consistency_response(
                        score=11,
                        answer="invalid oversized score",
                        matched=question["rubric"]["critical_points"],
                        missing=[],
                        errors=[],
                    )
                ),
                question,
                "invalid oversized score",
            )

    @staticmethod
    def _score_consistency_question():
        return {
            "topic": "Safe repeated operations",
            "question": "How is a repeated operation kept safe?",
            "rubric": {
                "evaluation_goal": "Explain safe repeated operations",
                "critical_points": [
                    "Stable operation identity",
                    "Prior result is reused",
                    "Repeated side effects are prevented",
                ],
                "met": "Explains the complete mechanism.",
                "partially_met": "Explains part of the mechanism.",
                "not_met": "Incorrect, unknown, or unrelated explanation.",
            },
        }

    @staticmethod
    def _score_consistency_response(*, score, answer, matched, missing, errors):
        return {
            "score": score,
            "evidence_quote": answer,
            "justification": "Structured evidence for score consistency validation.",
            "should_follow_up": 4 <= score <= 7,
            "next_direction": "Clarify the missing criterion." if 4 <= score <= 7 else "",
            "matched_points": matched,
            "missing_points": missing,
            "technical_errors": errors,
        }

    def test_qgen_reg_duplicate_history_is_retried_and_not_accepted(self):
        duplicate = {
            "company": "Portfolio",
            "topic": "React rendering",
            "question": "How did you reduce React re-renders in this project?",
            "rubric": QUESTION["rubric"],
        }
        replacement = {
            "company": "Portfolio",
            "topic": "Accessibility",
            "question": "How did you verify keyboard accessibility in this project?",
            "rubric": QUESTION["rubric"],
        }

        result = generate_question(
            FakeLLM(duplicate, replacement),
            {
                "type": "Project",
                "name": "Portfolio",
                "position": "Frontend Developer",
                "jobDescription": "Built React screens and accessibility checks.",
            },
            "Web Developer",
            "Junior",
            [],
            previous_questions=[duplicate["question"]],
        )

        self.assertEqual(result["question"], replacement["question"])
        self.assertNotEqual(result["question"], duplicate["question"])

    def test_qgen_reg_semantic_duplicate_is_rejected_after_bounded_retry(self):
        previous = "How did you reduce React re-renders in this project?"
        semantic_duplicate = {
            "company": "Portfolio",
            "topic": "React rendering",
            "question": "In this project, how did you reduce React re-renders?",
            "rubric": QUESTION["rubric"],
        }

        with self.assertRaisesRegex(ValueError, "duplicate interview question"):
            generate_question(
                FakeLLM(semantic_duplicate, semantic_duplicate),
                {
                    "type": "Project",
                    "name": "Portfolio",
                    "position": "Frontend Developer",
                    "jobDescription": "Built React screens.",
                },
                "Web Developer",
                "Junior",
                [],
                previous_questions=[previous],
            )

    @staticmethod
    def _qsem_question(topic, text):
        return {
            "company": "Candidate evidence",
            "topic": topic,
            "question": text,
            "rubric": QUESTION["rubric"],
        }

    def _qsem_generate(self, project, bad, good, *, role="Backend Developer", level="Junior", hits=None, interview_round=None):
        return generate_question(
            FakeLLM(bad, good),
            project,
            role,
            level,
            hits or [],
            interview_round=interview_round,
        )

    def test_qsem_01_personal_project_rejects_production_premise(self):
        bad = self._qsem_question("Redis", "How did you operate Redis in production?")
        good = self._qsem_question("Redis", "How did you use Redis in your personal project?")
        result = self._qsem_generate(
            {"type": "Project", "name": "Personal cache", "position": "", "jobDescription": "Built a personal project using Redis."},
            bad,
            good,
        )
        self.assertEqual(result["question"], good["question"])

    def test_qsem_02_jd_only_technology_requires_hypothetical_form(self):
        bad = self._qsem_question("Kubernetes", "How did you deploy Kubernetes?")
        good = self._qsem_question("Kubernetes", "How would you approach Kubernetes deployment?")
        result = self._qsem_generate(
            {"type": "Project", "name": "HTTP API", "position": "Student", "jobDescription": "Built a Python HTTP API."},
            bad,
            good,
            hits=[{"source": "TargetJD.md", "content": "Kubernetes deployment and operations", "score": 0.9}],
        )
        self.assertEqual(result["question"], good["question"])

    def test_qsem_03_familiarity_does_not_become_implementation(self):
        bad = self._qsem_question("Kafka", "How did you optimize Kafka consumers?")
        good = self._qsem_question("Kafka", "What do you know about diagnosing consumer lag in Kafka?")
        result = self._qsem_generate(
            {"type": "Project", "name": "Learning notes", "position": "", "jobDescription": "Familiar with Kafka concepts."},
            bad,
            good,
        )
        self.assertEqual(result["question"], good["question"])

    def test_qsem_04_prototype_does_not_become_deployed_production(self):
        bad = self._qsem_question("RAG", "How did you monitor the deployed RAG system in production?")
        good = self._qsem_question("RAG", "How did you evaluate the RAG prototype?")
        result = self._qsem_generate(
            {"type": "Project", "name": "RAG prototype", "position": "", "jobDescription": "Built an experimental RAG prototype."},
            bad,
            good,
        )
        self.assertEqual(result["question"], good["question"])

    def test_qsem_05_contribution_does_not_become_architecture_ownership(self):
        bad = self._qsem_question("Backend", "How did you architect the entire backend?")
        good = self._qsem_question("Backend", "What part of the backend did you contribute to?")
        result = self._qsem_generate(
            {"type": "Work", "name": "Product team", "position": "Developer", "jobDescription": "Contributed to backend endpoint implementation."},
            bad,
            good,
        )
        self.assertEqual(result["question"], good["question"])

    def test_qsem_06_team_project_does_not_imply_leadership(self):
        bad = self._qsem_question("Team delivery", "How did you lead the team and manage engineers?")
        good = self._qsem_question("Team delivery", "How did you collaborate with the team on this project?")
        result = self._qsem_generate(
            {"type": "Project", "name": "Team project", "position": "Developer", "jobDescription": "Worked with a team to build a course project."},
            bad,
            good,
        )
        self.assertEqual(result["question"], good["question"])

    def test_qsem_07_missing_duration_rejects_invented_years(self):
        bad = self._qsem_question("API design", "During your 3 years building APIs, how did you optimize them?")
        good = self._qsem_question("API design", "How did you design the APIs described in this work?")
        result = self._qsem_generate(
            {"type": "Work", "name": "API team", "position": "Developer", "jobDescription": "Built and tested HTTP APIs."},
            bad,
            good,
        )
        self.assertEqual(result["question"], good["question"])

    def test_qsem_08_role_mismatch_does_not_rewrite_historical_role(self):
        bad = self._qsem_question("AI Engineer role", "In your previous AI Engineer role, how did you deploy models?")
        good = self._qsem_question("Transferable skills", "How would you apply your frontend experience to an AI engineering role?")
        result = self._qsem_generate(
            {"type": "Work", "name": "Web team", "position": "Frontend Intern", "jobDescription": "Built React user interfaces."},
            bad,
            good,
            role="AI Engineer",
            interview_round={"reasoning": "Role mismatch: resume evidence aligns with Web Developer, while the target role is AI Engineer."},
        )
        self.assertEqual(result["question"], good["question"])

    def test_qsem_09_strong_production_evidence_allows_production_question(self):
        valid = self._qsem_question("Production deployment", "How did you deploy and monitor this service in production?")
        result = generate_question(
            FakeLLM(valid),
            {"type": "Work", "name": "Platform", "position": "Backend Engineer", "jobDescription": "Deployed the service to production and monitored live traffic."},
            "Backend Developer",
            "Senior",
            [],
        )
        self.assertEqual(result["question"], valid["question"])

    def test_qsem_10_explicit_technology_production_evidence_remains_valid(self):
        valid = self._qsem_question("Kubernetes", "How did you operate Kubernetes in production?")
        result = generate_question(
            FakeLLM(valid),
            {"type": "Work", "name": "Platform", "position": "DevOps Engineer", "jobDescription": "Deployed Kubernetes to production and monitored the cluster."},
            "DevOps Engineer",
            "Senior",
            [],
        )
        self.assertEqual(result["question"], valid["question"])

    @staticmethod
    def _eval_claim_question(topic, text):
        return {
            "company": "Candidate evidence",
            "topic": topic,
            "question": text,
            "rubric": {
                "evaluation_goal": "Evaluate the supported technical claim",
                "critical_points": ["Supported mechanism", "Supported scope"],
                "met": "Correct mechanism and scope.",
                "partially_met": "Some supported evidence.",
                "not_met": "Incorrect or missing supported evidence.",
            },
        }

    def _eval_claim(self, question_value, answer, context, *, errors=None):
        return evaluate_answer(
            FakeLLM(
                {
                    "score": 2,
                    "evidence_quote": answer,
                    "justification": "The answer did not satisfy the assumed experience.",
                    "should_follow_up": False,
                    "next_direction": "",
                    "matched_points": [],
                    "missing_points": question_value["rubric"]["critical_points"],
                    "technical_errors": errors or [],
                }
            ),
            question_value,
            answer,
            candidate_context=context,
        )

    def test_eval_claim_01_project_scope_correction_is_not_penalized(self):
        result = self._eval_claim(
            self._eval_claim_question("Redis", "How did you operate Redis in production?"),
            "I only used Redis in a university project, not in production.",
            {"type": "Project", "name": "University cache", "jobDescription": "Used Redis in a university project."},
        )
        self.assertEqual((result["status"], result["score"]), ("NOT_ASSESSED", 0))

    def test_eval_claim_02_familiarity_correction_is_not_implementation_failure(self):
        result = self._eval_claim(
            self._eval_claim_question("Kafka", "How did you optimize Kafka consumers in production?"),
            "I learned Kafka concepts but haven't implemented it in production.",
            {"skills": ["Familiar with Kafka"], "jobDescription": "Studied Kafka concepts."},
        )
        self.assertEqual((result["status"], result["score"]), ("NOT_ASSESSED", 0))

    def test_eval_claim_03_old_cv_claim_is_not_used_against_current_snapshot(self):
        result = self._eval_claim(
            self._eval_claim_question("Java", "How did you optimize the Java service from your experience?"),
            "That was from an older version of my CV; I no longer list Java as current experience.",
            {"skills": ["Python"], "jobDescription": "Built the current Python service."},
        )
        self.assertEqual((result["status"], result["score"]), ("NOT_ASSESSED", 0))

    def test_eval_claim_04_grounded_production_wrong_answer_remains_low(self):
        result = self._eval_claim(
            self._eval_claim_question("Redis", "How did you operate Redis in production?"),
            "Redis persistence guarantees that stale cache entries can never occur.",
            {"type": "Work", "jobDescription": "Deployed Redis to production and monitored cache health."},
            errors=["Incorrectly claims persistence prevents stale cache entries."],
        )
        self.assertEqual((result["status"], result["score"]), ("NOT_MET", 2))
        self.assertTrue(result["technical_errors"])

    def test_eval_claim_05_valid_knowledge_question_i_do_not_know_remains_low(self):
        result = self._eval_claim(
            self._eval_claim_question("Kubernetes", "How would you approach using Kubernetes?"),
            "I don't know how I would approach it.",
            {"type": "Project", "jobDescription": "Built a Docker-based local service."},
        )
        self.assertEqual((result["status"], result["score"]), ("NOT_MET", 2))

    def test_eval_claim_06_contribution_correction_is_not_ownership_failure(self):
        result = self._eval_claim(
            self._eval_claim_question("Backend", "How did you architect the entire backend?"),
            "I only contributed to endpoint implementation; I did not architect the backend.",
            {"type": "Work", "jobDescription": "Contributed to backend endpoint implementation."},
        )
        self.assertEqual((result["status"], result["score"]), ("NOT_ASSESSED", 0))

    def test_eval_claim_07_team_membership_correction_is_not_leadership_failure(self):
        result = self._eval_claim(
            self._eval_claim_question("Team delivery", "How did you lead the team and manage engineers?"),
            "I was a team member, not the lead, and I did not manage engineers.",
            {"type": "Project", "jobDescription": "Worked with a team on a university project."},
        )
        self.assertEqual((result["status"], result["score"]), ("NOT_ASSESSED", 0))

    def test_eval_claim_08_prototype_correction_is_not_deployment_failure(self):
        result = self._eval_claim(
            self._eval_claim_question("Search", "How did you monitor the deployed search system in production?"),
            "It was only a prototype; I did not deploy or operate it in production.",
            {"type": "Project", "jobDescription": "Built an experimental search prototype."},
        )
        self.assertEqual((result["status"], result["score"]), ("NOT_ASSESSED", 0))

    def test_eval_claim_09_unknown_duration_correction_is_not_penalized(self):
        result = self._eval_claim(
            self._eval_claim_question("API", "During your 3 years building APIs, how did you optimize them?"),
            "I do not have three years of API experience; the dates were not listed.",
            {"type": "Work", "jobDescription": "Built and tested HTTP APIs."},
        )
        self.assertEqual((result["status"], result["score"]), ("NOT_ASSESSED", 0))

    def test_eval_claim_10_incorrect_correction_does_not_override_authoritative_evidence(self):
        result = self._eval_claim(
            self._eval_claim_question("Redis", "How did you operate Redis in production?"),
            "I never used Redis.",
            {"type": "Work", "jobDescription": "Deployed Redis to production and monitored cache health."},
        )
        self.assertEqual((result["status"], result["score"]), ("NOT_MET", 2))

    @staticmethod
    def _report_claim_evaluation(answer, *, score, status, justification):
        return {
            "score": score,
            "raw_llm_score": score,
            "validated_score": score,
            "final_score": score,
            "score_scale": 10,
            "score_correction_reason": "",
            "status": status,
            "evidence_quote": "" if status == "NOT_ASSESSED" else answer,
            "justification": justification,
            "should_follow_up": False,
            "next_direction": "",
            "matched_points": [],
            "missing_points": [],
            "technical_errors": [],
        }

    def _report_claim_result(
        self,
        *,
        context,
        question_text,
        topic,
        answer,
        model_rationale,
        evaluation=None,
        role="Backend Developer",
    ):
        timestamp = "2026-08-24T10:00:00+07:00"
        question_value = self._eval_claim_question(topic, question_text)
        question_value["project_context"] = context
        turn = {
            "question": question_value,
            "answer": answer,
            "timestamp": timestamp,
        }
        if evaluation is not None:
            turn["evaluation"] = evaluation
        model_score = evaluation["final_score"] if evaluation is not None else 8
        return generate_report(
            FakeLLM(
                {
                    "assessments": [
                        {
                            "turn_index": 0,
                            "raw_score": model_score,
                            "rationale": model_rationale,
                            "evidence": [{"timestamp": timestamp, "quote": answer}],
                        }
                    ],
                    "solutions_summary": model_rationale,
                    "overall_assessment": model_rationale,
                    "recommendations": model_rationale,
                }
            ),
            role,
            "Junior",
            [turn],
        )

    def test_report_claim_01_projects_do_not_become_professional_experience(self):
        report = self._report_claim_result(
            context={"type": "Project", "name": "Course API", "jobDescription": "Built a Python API for a university project."},
            question_text="How did you structure the course API?",
            topic="Python API",
            answer="I separated routing from persistence in the university project.",
            model_rationale="The candidate demonstrated strong professional industry experience.",
        )
        self.assertNotIn("professional industry experience", report["assessments"][0]["rationale"].casefold())

    def test_report_claim_02_unknown_duration_does_not_become_years(self):
        report = self._report_claim_result(
            context={"type": "Work", "name": "API", "position": "Developer", "jobDescription": "Built Python APIs; dates are not supplied."},
            question_text="How did you handle API failures?",
            topic="API failures",
            answer="I used rollback and returned a controlled error.",
            model_rationale="The candidate demonstrated three years of API experience.",
        )
        self.assertNotIn("three years", report["assessments"][0]["rationale"].casefold())

    def test_report_claim_03_prototype_does_not_become_production_deployment(self):
        report = self._report_claim_result(
            context={"type": "Project", "name": "Search prototype", "jobDescription": "Built a local experimental prototype."},
            question_text="How did you evaluate the prototype?",
            topic="Search prototype",
            answer="I measured retrieval quality on a local test set.",
            model_rationale="The candidate successfully deployed and operated the system in production.",
        )
        self.assertNotIn("deployed and operated", report["assessments"][0]["rationale"].casefold())

    def test_report_claim_04_contribution_does_not_become_ownership(self):
        report = self._report_claim_result(
            context={"type": "Work", "name": "API", "jobDescription": "Contributed to endpoint implementation."},
            question_text="What endpoint work did you contribute?",
            topic="API contribution",
            answer="I implemented two endpoints and their tests.",
            model_rationale="The candidate architected and owned the entire backend.",
        )
        self.assertNotIn("owned the entire", report["assessments"][0]["rationale"].casefold())

    def test_report_claim_05_team_membership_does_not_become_leadership(self):
        report = self._report_claim_result(
            context={"type": "Project", "name": "Capstone", "jobDescription": "Worked as a member of a university project team."},
            question_text="How did the team collaborate?",
            topic="Team collaboration",
            answer="I coordinated my API changes with two classmates.",
            model_rationale="The candidate led the team and managed engineers.",
        )
        self.assertNotIn("led the team", report["assessments"][0]["rationale"].casefold())

    def test_report_claim_06_not_assessed_is_not_a_weakness(self):
        answer = "I only used Redis in a personal project, not in production."
        report = self._report_claim_result(
            context={"type": "Project", "name": "Cache demo", "jobDescription": "Built a local Redis prototype."},
            question_text="How did you operate Redis in production?",
            topic="Redis",
            answer=answer,
            model_rationale="The candidate failed Redis production operations.",
            evaluation=self._report_claim_evaluation(
                answer,
                score=0,
                status="NOT_ASSESSED",
                justification="The unsupported production premise was corrected.",
            ),
        )
        self.assertEqual(report["assessments"][0]["status"], "NOT_ASSESSED")
        self.assertIsNone(report["assessments"][0]["raw_score"])
        self.assertNotIn("failed", json.dumps(report).casefold())

    def test_report_claim_07_removed_skill_is_not_restored(self):
        answer = "That was old CV evidence; I no longer claim Java experience."
        report = self._report_claim_result(
            context={"type": "Project", "name": "Current API", "jobDescription": "Built the current Python API."},
            question_text="How did you optimize Java in production?",
            topic="Java",
            answer=answer,
            model_rationale="Java is a major candidate weakness.",
            evaluation=self._report_claim_evaluation(
                answer,
                score=0,
                status="NOT_ASSESSED",
                justification="The stale Java premise was corrected.",
            ),
        )
        self.assertNotIn("java is a major candidate weakness", json.dumps(report).casefold())

    def test_report_claim_08_grounded_strength_is_retained(self):
        answer = "I used transaction boundaries and rollback for failed writes."
        evaluation = self._report_claim_evaluation(
            answer,
            score=9,
            status="MET",
            justification="Strong grounded transaction handling evidence.",
        )
        report = self._report_claim_result(
            context={"type": "Work", "name": "Payments API", "jobDescription": "Built transaction handling and rollback for a production API."},
            question_text="How did you handle failed database writes?",
            topic="Transactions",
            answer=answer,
            model_rationale="Strong grounded transaction handling evidence.",
            evaluation=evaluation,
        )
        self.assertEqual(report["assessments"][0]["status"], "MET")
        self.assertIn("strong grounded transaction", report["assessments"][0]["rationale"].casefold())

    def test_report_claim_09_grounded_low_score_can_remain_a_weakness(self):
        answer = "Rollback means committing all partial writes after failure."
        evaluation = self._report_claim_evaluation(
            answer,
            score=2,
            status="NOT_MET",
            justification="The grounded rollback explanation is technically incorrect.",
        )
        report = self._report_claim_result(
            context={"type": "Work", "name": "Payments API", "jobDescription": "Implemented database transactions and rollback."},
            question_text="How does rollback handle failed writes?",
            topic="Transactions",
            answer=answer,
            model_rationale="The grounded rollback explanation is technically incorrect.",
            evaluation=evaluation,
        )
        self.assertEqual(report["assessments"][0]["status"], "NOT_MET")
        self.assertIn("technically incorrect", report["assessments"][0]["rationale"].casefold())

    def test_report_claim_10_historical_snapshot_keeps_its_supported_claim(self):
        answer = "I implemented Java transaction handling in the historical service."
        evaluation = self._report_claim_evaluation(
            answer,
            score=9,
            status="MET",
            justification="Strong Java transaction evidence from the historical interview.",
        )
        report = self._report_claim_result(
            context={"type": "Work", "name": "Historical service", "position": "Java Developer", "jobDescription": "Built a Java service with transaction handling."},
            question_text="How did you implement Java transaction handling?",
            topic="Java transactions",
            answer=answer,
            model_rationale="Strong Java transaction evidence from the historical interview.",
            evaluation=evaluation,
        )
        self.assertEqual(report["assessments"][0]["status"], "MET")
        self.assertIn("java transaction", report["assessments"][0]["rationale"].casefold())

    def _generate_report_for_scores(self, scores, overall_assessment="Assessment"):
        turns = [
            {
                "question": QUESTION,
                "answer": f"answer {index}",
                "timestamp": f"2026-08-19T10:00:0{index}+07:00",
            }
            for index in range(len(scores))
        ]
        if not scores:
            return generate_report(FakeLLM(), "AI Engineer", "Junior", turns)

        assessments = []
        for index, score in enumerate(scores):
            evidence = [{"timestamp": turns[index]["timestamp"], "quote": f"answer {index}"}]
            assessments.append(
                {
                    "turn_index": index,
                    "raw_score": score,
                    "rationale": "Regression score fixture.",
                    "evidence": evidence,
                }
            )
        llm = FakeLLM(
            {
                "assessments": assessments,
                "solutions_summary": "Summary",
                "overall_assessment": overall_assessment,
                "recommendations": "Recommendation",
            }
        )
        return generate_report(llm, "AI Engineer", "Junior", turns)

    def test_question_prompt_combines_selected_role_with_matching_resume_evidence(self):
        llm = CapturingLLM(
            {
                "company": "Platform API",
                "topic": "Database consistency",
                "question": "Bạn bảo đảm transaction nhất quán trong API này như thế nào?",
                "rubric": {
                    "evaluation_goal": "Đánh giá transaction handling",
                    "critical_points": ["Transaction boundary", "Rollback"],
                    "met": "Giải thích đúng boundary và rollback.",
                    "partially_met": "Nêu một cơ chế nhưng thiếu trade-off.",
                    "not_met": "Không giải thích được transaction.",
                },
            }
        )

        generate_question(
            llm,
            {
                "type": "Work",
                "name": "Platform API",
                "position": "Backend Engineer",
                "jobDescription": "Built FastAPI services backed by PostgreSQL.",
            },
            "Backend Developer",
            "Junior",
            [
                {
                    "source": "Domains/Backend Developer/Database/PostgreSQL.md",
                    "content": "Transactions require explicit boundaries and rollback handling.",
                    "score": 0.82,
                    "method": "lexical",
                }
            ],
            interview_round={
                "round_id": "round-1",
                "topic": "PostgreSQL",
                "difficulty": "medium",
                "objective": "Validate transaction handling.",
                "reasoning": "The resume claims PostgreSQL API experience.",
            },
        )

        prompt = llm.calls[0]["user_prompt"]
        self.assertIn("Target role: Backend Developer", prompt)
        self.assertIn("FastAPI services backed by PostgreSQL", prompt)
        self.assertIn("Selected interview round", prompt)
        self.assertIn("Validate transaction handling", prompt)
        self.assertIn("PostgreSQL.md", prompt)
        self.assertIn("explicit boundaries and rollback", prompt)
        self.assertIn("reference guidance, not a candidate claim", prompt)
        self.assertNotIn("PyTorch", prompt)

    def test_evaluate_answer_uses_saved_rubric_and_exact_evidence(self):
        llm = FakeLLM(
            {
                "score": 5,
                "evidence_quote": "Tôi xóa cache",
                "justification": "Có invalidation nhưng thiếu trade-off.",
                "should_follow_up": True,
                "next_direction": "Làm rõ trade-off của invalidation.",
                "matched_points": ["Có chiến lược invalidation"],
                "missing_points": ["Nhận diện stale data"],
                "technical_errors": [],
            }
        )

        result = evaluate_answer(
            llm,
            QUESTION,
            "Tôi xóa cache sau khi cập nhật database.",
        )

        self.assertEqual(result["score"], 5)
        self.assertEqual(result["status"], "PARTIALLY_MET")
        self.assertEqual(result["evidence_quote"], "Tôi xóa cache")
        self.assertTrue(result["should_follow_up"])

    def test_evaluate_answer_rejects_invented_evidence(self):
        llm = FakeLLM(
            {
                "score": 10,
                "evidence_quote": "Trích dẫn không tồn tại",
                "justification": "Đạt yêu cầu.",
                "should_follow_up": True,
                "next_direction": "Hỏi thêm.",
                "matched_points": [],
                "missing_points": [],
                "technical_errors": [],
            }
        )

        result = evaluate_answer(llm, QUESTION, "Tôi sử dụng TTL.")

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["status"], "NOT_ASSESSED")
        self.assertEqual(result["evidence_quote"], "")
        self.assertFalse(result["should_follow_up"])

    def test_eval_reg_01_unsupported_question_premise_does_not_penalize_denial(self):
        answer = "I have not used Kubernetes directly, but I have worked with Docker."
        llm = FakeLLM(
            {
                "score": 2,
                "evidence_quote": "I have not used Kubernetes directly",
                "justification": "Candidate did not explain Kubernetes operations.",
                "should_follow_up": True,
                "next_direction": "Explain Kubernetes operations.",
                "matched_points": [],
                "missing_points": ["Deployment"],
                "technical_errors": [],
            }
        )

        result = evaluate_answer(
            llm,
            ASSUMED_EXPERIENCE_QUESTION,
            answer,
            candidate_context={
                "position": "Backend Developer",
                "jobDescription": "Built and ran containerized services with Docker.",
            },
        )

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["status"], "NOT_ASSESSED")
        self.assertEqual(result["evidence_quote"], "")
        self.assertFalse(result["should_follow_up"])
        self.assertEqual(result["technical_errors"], [])
        self.assertIn("premise", result["justification"].casefold())

    def test_eval_reg_02_grounded_experience_with_wrong_answer_still_scores_low(self):
        answer = "Kubernetes is only a container runtime and has no orchestration features."
        result = evaluate_answer(
            FakeLLM(
                {
                    "score": 2,
                    "evidence_quote": answer,
                    "justification": "The answer is technically incorrect.",
                    "should_follow_up": False,
                    "next_direction": "",
                    "matched_points": [],
                    "missing_points": ["Deployment", "Observability", "Failure recovery"],
                    "technical_errors": ["Incorrectly denies orchestration features."],
                }
            ),
            ASSUMED_EXPERIENCE_QUESTION,
            answer,
            candidate_context={
                "position": "DevOps Engineer",
                "jobDescription": "Operated Kubernetes production deployments and monitoring.",
            },
        )

        self.assertEqual(result["score"], 2)
        self.assertEqual(result["status"], "NOT_MET")
        self.assertTrue(result["technical_errors"])

    def test_eval_reg_03_i_do_not_know_still_scores_low_for_grounded_question(self):
        answer = "I don't know how Kubernetes deployment and recovery work."
        result = evaluate_answer(
            FakeLLM(
                {
                    "score": 2,
                    "evidence_quote": answer,
                    "justification": "The grounded question was not answered.",
                    "should_follow_up": False,
                    "next_direction": "",
                    "matched_points": [],
                    "missing_points": ["Deployment", "Failure recovery"],
                    "technical_errors": [],
                }
            ),
            ASSUMED_EXPERIENCE_QUESTION,
            answer,
            candidate_context={
                "position": "DevOps Engineer",
                "jobDescription": "Used Kubernetes for production deployment and recovery.",
            },
        )

        self.assertEqual(result["score"], 2)
        self.assertEqual(result["status"], "NOT_MET")

    def test_eval_reg_semantically_equivalent_evidence_is_required_by_prompt(self):
        answer = (
            "Redis giup giam database load vi frequently accessed data duoc giu trong "
            "memory, nhung can invalidation de tranh stale data."
        )
        question = {
            "company": "Synthetic",
            "project": "Synthetic",
            "topic": "Giai thich co che cache",
            "question": "Tai sao cache co the giam tai cho database?",
            "rubric": {
                "evaluation_goal": "Giai thich co che cache",
                "critical_points": [
                    "Du lieu truy cap thuong xuyen o bo nho nhanh",
                    "Giam truy van lap lai vao database",
                    "Nhan biet stale data/invalidation",
                ],
                "met": "Giai thich co che, tac dong len database, va mot trade-off consistency.",
                "partially_met": "Dung co che nhung thieu mot critical point.",
                "not_met": "Lac de hoac giai thich sai.",
            },
        }
        llm = CapturingLLM(
            {
                "score": 8,
                "evidence_quote": answer,
                "justification": "Câu trả lời diễn đạt đủ các ý bằng wording tương đương.",
                "should_follow_up": False,
                "next_direction": "",
                "matched_points": question["rubric"]["critical_points"],
                "missing_points": [],
                "technical_errors": [],
            }
        )

        result = evaluate_answer(llm, question, answer)

        self.assertEqual(result["score"], 8)
        prompt = llm.calls[0]["system_prompt"]
        self.assertIn("semantically equivalent evidence", prompt)
        self.assertIn("Do not require the candidate to repeat a rubric label", prompt)
        self.assertIn("Do not count the same concept as both matched and missing", prompt)

    def test_generate_report_validates_each_turn_evidence_and_score(self):
        timestamp = "2026-08-19T10:00:00+07:00"
        turns = [
            {
                "question": QUESTION,
                "answer": "Tôi xóa cache sau khi cập nhật database.",
                "timestamp": timestamp,
            }
        ]
        llm = FakeLLM(
            {
                "assessments": [
                    {
                        "turn_index": 0,
                        "raw_score": 5,
                        "rationale": "Đúng hướng nhưng thiếu trade-off.",
                        "evidence": [
                            {"timestamp": timestamp, "quote": "Tôi xóa cache"}
                        ],
                    }
                ],
                "solutions_summary": "Ứng viên sử dụng cache invalidation.",
                "overall_assessment": "Có nền tảng nhưng cần giải thích sâu hơn.",
                "recommendations": "Kiểm tra thêm failure cases.",
            }
        )

        report = generate_report(llm, "AI Engineer", "Junior", turns)

        self.assertEqual(report["normalized_score"], 5.0)
        self.assertEqual(report["coverage_ratio"], 1.0)
        self.assertEqual(report["assessments"][0]["status"], "PARTIALLY_MET")
        self.assertEqual(
            report["assessments"][0]["evaluation_goal"],
            QUESTION["rubric"]["evaluation_goal"],
        )

    def test_report_reg_high_scores_replace_strongly_negative_conclusion(self):
        timestamp = "2026-08-19T10:00:00+07:00"
        turns = [
            {"question": QUESTION, "answer": "correct mechanism", "timestamp": timestamp}
        ]
        report = generate_report(
            FakeLLM(
                {
                    "assessments": [
                        {
                            "turn_index": 0,
                            "raw_score": 10,
                            "rationale": "Meets the rubric.",
                            "evidence": [{"timestamp": timestamp, "quote": "correct mechanism"}],
                        }
                    ],
                    "solutions_summary": "No technical knowledge was demonstrated.",
                    "overall_assessment": "The candidate failed every assessed area.",
                    "recommendations": "Restart from the basics.",
                }
            ),
            "Backend Developer",
            "Senior",
            turns,
        )

        self.assertEqual(report["normalized_score"], 10.0)
        self.assertIn("met all assessed rubric goals", report["overall_assessment"].casefold())
        self.assertNotIn("failed every", report["overall_assessment"].casefold())

    def test_report_reg_low_scores_replace_strong_hire_conclusion(self):
        report = self._generate_report_for_scores(
            [2, 2],
            overall_assessment="Strong Hire with excellent evidence in every area.",
        )

        self.assertIn("did not meet", report["overall_assessment"].casefold())
        self.assertNotIn("strong hire", report["overall_assessment"].casefold())

    def test_report_reg_mixed_scores_produce_balanced_narrative(self):
        report = self._generate_report_for_scores(
            [9, 5, 2],
            overall_assessment="Uniform performance.",
        )

        self.assertIn("mixed results", report["overall_assessment"].casefold())
        self.assertIn("1 met", report["solutions_summary"].casefold())
        self.assertIn("1 partially met", report["solutions_summary"].casefold())
        self.assertIn("1 not met", report["solutions_summary"].casefold())

    def test_report_reg_missing_evaluation_is_handled_safely(self):
        timestamp = "2026-08-19T10:00:00+07:00"
        turns = [
            {"question": QUESTION, "answer": "correct", "timestamp": timestamp},
            {"question": QUESTION, "answer": "second answer", "timestamp": timestamp + "-2"},
        ]
        report = generate_report(
            FakeLLM(
                {
                    "assessments": [
                        {
                            "turn_index": 0,
                            "raw_score": 10,
                            "rationale": "Meets the rubric.",
                            "evidence": [{"timestamp": timestamp, "quote": "correct"}],
                        }
                    ],
                    "solutions_summary": "All complete.",
                    "overall_assessment": "Strong conclusion.",
                    "recommendations": "None.",
                }
            ),
            "Backend Developer",
            "Junior",
            turns,
        )

        self.assertEqual(len(report["assessments"]), 2)
        self.assertIsNone(report["assessments"][1]["raw_score"])
        self.assertEqual(report["assessments"][1]["status"], "NOT_ASSESSED")
        self.assertEqual(report["normalized_score"], 10.0)
        self.assertEqual(report["coverage_ratio"], 0.5)
        self.assertIn("1 rubric goal(s) remained not assessed", report["overall_assessment"])

    def test_score10_07_partial_components_do_not_become_ten(self):
        report = self._generate_report_for_scores([6, 0, 0])

        self.assertEqual(report["normalized_score"], 2.0)
        self.assertLess(report["normalized_score"], 10.0)

    def test_score10_09_all_zero_scores_produce_minimum(self):
        report = self._generate_report_for_scores([0, 0, 0])

        self.assertEqual(report["normalized_score"], 0.0)
        self.assertEqual(report["coverage_ratio"], 1.0)

    def test_score10_08_all_maximum_components_produce_ten(self):
        report = self._generate_report_for_scores([10, 10, 10])

        self.assertEqual(report["normalized_score"], 10.0)

    def test_score10_empty_scores_do_not_produce_a_fake_high_score(self):
        report = self._generate_report_for_scores([])

        self.assertEqual(report["normalized_score"], 0.0)

    def test_score10_10_normalized_score_is_monotonic(self):
        low = self._generate_report_for_scores([4, 0, 0])["normalized_score"]
        medium = self._generate_report_for_scores([4, 6, 0])["normalized_score"]
        high = self._generate_report_for_scores([4, 6, 8])["normalized_score"]

        self.assertLess(low, medium)
        self.assertLess(medium, high)
        self.assertTrue(all(0.0 <= score <= 10.0 for score in (low, medium, high)))

    def test_score10_report_averages_strong_and_mixed_components(self):
        self.assertEqual(
            self._generate_report_for_scores([8, 9, 10])["normalized_score"],
            9.0,
        )
        self.assertEqual(
            self._generate_report_for_scores([4, 6, 8])["normalized_score"],
            6.0,
        )


if __name__ == "__main__":
    unittest.main()

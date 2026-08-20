import json
import unittest

from fipilot.interview_engine import evaluate_answer, generate_report


class FakeLLM:
    def __init__(self, *responses: dict):
        self.responses = iter(responses)

    def generate_text(self, *_args, **_kwargs) -> str:
        return json.dumps(next(self.responses), ensure_ascii=False)


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


class InterviewEngineTest(unittest.TestCase):
    def test_evaluate_answer_uses_saved_rubric_and_exact_evidence(self):
        llm = FakeLLM(
            {
                "score": 2,
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

        self.assertEqual(result["score"], 2)
        self.assertEqual(result["status"], "PARTIALLY_MET")
        self.assertEqual(result["evidence_quote"], "Tôi xóa cache")
        self.assertTrue(result["should_follow_up"])

    def test_evaluate_answer_rejects_invented_evidence(self):
        llm = FakeLLM(
            {
                "score": 3,
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
                        "raw_score": 2,
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

        self.assertEqual(report["normalized_score"], 3.33)
        self.assertEqual(report["coverage_ratio"], 1.0)
        self.assertEqual(report["assessments"][0]["status"], "PARTIALLY_MET")
        self.assertEqual(
            report["assessments"][0]["evaluation_goal"],
            QUESTION["rubric"]["evaluation_goal"],
        )


if __name__ == "__main__":
    unittest.main()

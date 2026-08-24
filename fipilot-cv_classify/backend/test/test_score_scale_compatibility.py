import unittest

from fipilot.persistence import normalize_report_score_scale


class ScoreScaleCompatibilityTest(unittest.TestCase):
    def test_historical_report_is_converted_to_score_ten_at_read_boundary(self):
        report = normalize_report_score_scale(
            {
                "normalized_score": 4.25,
                "assessments": [
                    {"turn_index": 0, "raw_score": 3},
                    {"turn_index": 1, "raw_score": 2},
                    {"turn_index": 2, "raw_score": 0},
                ],
            }
        )

        self.assertEqual(report["normalized_score"], 8.5)
        self.assertEqual(
            [item["raw_score"] for item in report["assessments"]],
            [10.0, 6.67, 0.0],
        )
        self.assertEqual(report["score_scale"], 10)

    def test_current_score_ten_report_is_not_rescaled(self):
        report = normalize_report_score_scale(
            {
                "normalized_score": 8.5,
                "score_scale": 10,
                "assessments": [{"turn_index": 0, "raw_score": 8}],
            }
        )

        self.assertEqual(report["normalized_score"], 8.5)
        self.assertEqual(report["assessments"][0]["raw_score"], 8)
        self.assertEqual(report["score_scale"], 10)


if __name__ == "__main__":
    unittest.main()

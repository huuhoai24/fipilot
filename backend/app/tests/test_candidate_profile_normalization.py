from __future__ import annotations

import unittest

from services.candidate_profile.normalization import (
    normalize_profile_text,
    normalized_comparison_key,
)


class CandidateProfileNormalizationTests(unittest.TestCase):
    def test_normalizes_nfkc_and_unicode_whitespace_without_losing_copy(self) -> None:
        self.assertEqual(
            normalize_profile_text(" \u00a0Nguye\u0302\u0303n\t Minh\nAnh  "),
            "Nguyễn Minh Anh",
        )
        self.assertEqual(
            normalize_profile_text("  Built APIs: auth, scoring; reports.  "),
            "Built APIs: auth, scoring; reports.",
        )

    def test_comparison_key_casefolds_normalized_skill_text(self) -> None:
        self.assertEqual(
            normalized_comparison_key("\u00a0Ｐｙｔｈｏｎ\t"),
            normalized_comparison_key("python"),
        )
        self.assertEqual(normalized_comparison_key(" \t\n "), "")


if __name__ == "__main__":
    unittest.main()

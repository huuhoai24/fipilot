from __future__ import annotations

import asyncio
import unittest

from services.interview_preparation import InterviewPreparationCache
from shared.schemas import (
    CandidateProfile,
    InterviewConfig,
    InterviewPlan,
    InterviewSessionState,
    PersistedCandidateProfile,
)


def prepared_state() -> InterviewSessionState:
    return InterviewSessionState(
        candidate_profile=CandidateProfile(
            candidate_id="candidate-1",
            name="Candidate",
            skills=["Python"],
        ),
        interview_config=InterviewConfig(
            language="en",
            experience_level="junior",
        ),
        interview_plan=InterviewPlan(),
        current_turn=None,
    )


class InterviewPreparationCacheTests(unittest.IsolatedAsyncioTestCase):
    async def test_concurrent_requests_share_one_preparation(self):
        cache = InterviewPreparationCache(ttl_seconds=300, max_entries=8)
        started = asyncio.Event()
        release = asyncio.Event()
        calls = 0

        async def factory() -> InterviewSessionState:
            nonlocal calls
            calls += 1
            started.set()
            await release.wait()
            return prepared_state()

        first = asyncio.create_task(cache.get_or_create("same-key", factory))
        await started.wait()
        second = asyncio.create_task(cache.get_or_create("same-key", factory))
        release.set()
        first_state, second_state = await asyncio.gather(first, second)

        self.assertEqual(calls, 1)
        self.assertEqual(first_state, second_state)
        self.assertIsNot(first_state, second_state)

    def test_key_changes_with_profile_version_and_configuration(self):
        cache = InterviewPreparationCache()
        profile = PersistedCandidateProfile(
            candidate_id="candidate-1",
            profile_version=1,
            name="Candidate",
            skills=["Python"],
        )
        config = InterviewConfig(language="en", experience_level="junior")

        baseline = cache.key_for("user-1", profile, config)
        changed_profile = cache.key_for(
            "user-1",
            profile.model_copy(update={"profile_version": 2}),
            config,
        )
        changed_config = cache.key_for(
            "user-1",
            profile,
            config.model_copy(update={"experience_level": "senior"}),
        )

        self.assertNotEqual(baseline, changed_profile)
        self.assertNotEqual(baseline, changed_config)


if __name__ == "__main__":
    unittest.main()

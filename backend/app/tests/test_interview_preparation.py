from __future__ import annotations

import asyncio
import unittest

from services.interview_preparation import InterviewPreparationCache
from shared.schemas import (
    InterviewConfig,
    InterviewPlan,
    PersistedCandidateProfile,
)


def prepared_plan() -> InterviewPlan:
    return InterviewPlan()


class InterviewPreparationCacheTests(unittest.IsolatedAsyncioTestCase):
    async def test_reports_cache_miss_then_ready_hit_without_logging_the_key(self):
        cache = InterviewPreparationCache(ttl_seconds=300, max_entries=8)

        async def factory() -> InterviewPlan:
            return prepared_plan()

        with self.assertLogs("services.interview_preparation.service", level="INFO") as logs:
            await cache.get_or_create("private-user-and-profile-key", factory)
            await cache.get_or_create("private-user-and-profile-key", factory)

        records = [record for record in logs.records if record.event == "interview.preparation_cache"]
        self.assertEqual([record.cache_hit for record in records], [False, True])
        self.assertEqual([record.status for record in records], ["miss", "ready_hit"])
        self.assertTrue(all(not hasattr(record, "cache_key") for record in records))

    async def test_concurrent_requests_share_one_preparation(self):
        cache = InterviewPreparationCache(ttl_seconds=300, max_entries=8)
        started = asyncio.Event()
        release = asyncio.Event()
        calls = 0

        async def factory() -> InterviewPlan:
            nonlocal calls
            calls += 1
            started.set()
            await release.wait()
            return prepared_plan()

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
        changed_owner = cache.key_for("user-2", profile, config)

        self.assertNotEqual(baseline, changed_profile)
        self.assertNotEqual(baseline, changed_config)
        self.assertNotEqual(baseline, changed_owner)
        self.assertNotIn("user-1", baseline)
        self.assertNotIn("candidate-1", baseline)


if __name__ == "__main__":
    unittest.main()

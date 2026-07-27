from __future__ import annotations

import unittest

from services.question_generator.streaming_service import (
    QuestionStreamingError,
    QuestionStreamingService,
)
from shared.schemas import (
    CandidateProfile,
    InterviewConfig,
    InterviewQuestion,
    InterviewRound,
)


class MockStreamingLLM:
    def __init__(self, chunks: list[str]) -> None:
        self.chunks = chunks
        self.calls: list[tuple[str, dict]] = []

    async def stream_text(self, prompt: str, **kwargs):
        self.calls.append((prompt, kwargs))
        for chunk in self.chunks:
            yield chunk


class QuestionStreamingServiceTests(unittest.IsolatedAsyncioTestCase):
    def inputs(self):
        return (
            CandidateProfile(name="Candidate", skills=["YOLOv8"]),
            InterviewRound(
                round_id="round-2",
                topic="Computer Vision",
                difficulty="medium",
            ),
            InterviewConfig(
                mode="voice",
                language="en",
                experience_level="junior",
            ),
        )

    async def test_streams_question_field_and_validates_final_schema(self):
        llm = MockStreamingLLM(
            [
                '{"question":"Can you explain',
                ' YOLO architecture?","language":"en",',
                '"topic":"Computer Vision","difficulty":"medium",',
                '"reasoning":"Relevant experience",',
                '"expected_answer_points":["backbone","head"],',
                '"follow_up_questions":[]}',
            ]
        )
        service = QuestionStreamingService(llm_service=llm)
        deltas: list[str] = []

        question = await service.generate_question(
            *self.inputs(),
            delta_publisher=lambda text: self._collect(deltas, text),
        )

        self.assertEqual(
            deltas,
            ["Can you explain", " YOLO architecture?"],
        )
        self.assertEqual(question.question, "".join(deltas))
        self.assertEqual(question.topic, "Computer Vision")
        self.assertIn('"question"', llm.calls[0][0])
        # The voice path deliberately uses the fast model: the candidate is
        # waiting in silence while this runs.
        self.assertEqual(llm.calls[0][1]["task_type"], "simple")
        # No response schema is requested. Schema-constrained generation makes
        # Gemini buffer the whole object and emit it as one chunk, which removes
        # the incremental streaming this service exists to provide.
        self.assertNotIn("output_schema", llm.calls[0][1])

    async def test_rejects_incomplete_streamed_json(self):
        service = QuestionStreamingService(
            llm_service=MockStreamingLLM(
                ['{"question":"Incomplete question']
            )
        )

        with self.assertRaises(QuestionStreamingError):
            await service.generate_question(
                *self.inputs(),
                delta_publisher=lambda text: self._collect([], text),
            )

    @staticmethod
    async def _collect(target: list[str], text: str) -> None:
        target.append(text)


if __name__ == "__main__":
    unittest.main()

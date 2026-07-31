import asyncio
import unittest

from app.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    InterviewConfig,
    InterviewDecision,
    InterviewPlan,
    InterviewQuestion,
    InterviewRound,
)
from app.services.interview_orchestrator import InterviewOrchestrator


class MockPlannerAgent:
    async def create_plan(self, candidate_profile, interview_config):
        return InterviewPlan(
            rounds=[
                InterviewRound(
                    round_id="round-1",
                    topic="YOLO Optimization",
                    difficulty="medium",
                ),
                InterviewRound(
                    round_id="round-2",
                    topic="FastAPI Deployment",
                    difficulty="medium",
                ),
            ]
        )


class MockQuestionGeneratorAgent:
    def __init__(self):
        self.calls = []

    async def generate_question(self, candidate_profile, interview_round, interview_config):
        self.calls.append(interview_round)
        return InterviewQuestion(
            question=f"Explain {interview_round.topic}.",
            language=interview_config.language,
            topic=interview_round.topic,
            difficulty=interview_round.difficulty,
            reasoning=f"Generated from {interview_round.topic}.",
            expected_answer_points=["practical detail"],
            follow_up_questions=[f"Clarify your {interview_round.topic} experience."],
        )


class MockEvaluatorAgent:
    def __init__(self, evaluation):
        self.evaluation = evaluation
        self.answers = []

    async def evaluate_answer(self, candidate_profile, interview_question, answer, interview_config):
        self.answers.append(answer)
        return self.evaluation


class MockDecisionService:
    def __init__(self, action):
        self.action = action

    def decide(self, evaluation, current_question, session_state):
        return InterviewDecision(action=self.action, reason=f"{self.action} decision", next_topic=current_question.topic)


def candidate_profile() -> CandidateProfile:
    return CandidateProfile(name="Tran Thi B", skills=["YOLOv8", "FastAPI"])


def interview_config() -> InterviewConfig:
    return InterviewConfig(language="en", experience_level="middle")


def orchestrator(evaluation, action, question_agent=None) -> InterviewOrchestrator:
    return InterviewOrchestrator(
        planner_agent=MockPlannerAgent(),
        question_generator_agent=question_agent or MockQuestionGeneratorAgent(),
        evaluator_agent=MockEvaluatorAgent(evaluation),
        decision_service=MockDecisionService(action),
    )


class InterviewTurnIdentityTests(unittest.IsolatedAsyncioTestCase):
    """turn_id used to be topic+difficulty, which collided across a whole round.

    Repositories look turns up by this id, so a collision pointed evaluations at
    the wrong row, and every turn of a live interview shared one id.
    """

    async def test_turn_ids_are_unique_across_a_follow_up_chain(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=3.0,
            follow_up_needed=True,
            follow_up_reason="Answer is too vague.",
        )
        service = orchestrator(evaluation, "follow_up")
        state = await service.start_interview(candidate_profile(), interview_config())

        seen = [state.current_turn.turn_id]
        for _ in range(3):
            state = await service.submit_answer(state, "Still vague.")
            if state.current_turn is None:
                break
            seen.append(state.current_turn.turn_id)

        self.assertGreaterEqual(len(seen), 3)
        self.assertEqual(len(seen), len(set(seen)), f"duplicate turn ids: {seen}")

    async def test_a_canned_follow_up_probe_is_never_reused(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=3.0,
            follow_up_needed=True,
            follow_up_reason="Answer is too vague.",
        )
        service = orchestrator(evaluation, "follow_up")
        state = await service.start_interview(candidate_profile(), interview_config())
        probe = state.current_turn.question.follow_up_questions[0]

        first = await service.submit_answer(state, "Still vague.")
        second = await service.submit_answer(first, "Still vague.")

        self.assertEqual(first.current_turn.question.question, probe)
        # The used probe is consumed, so the next follow-up cannot be the same one.
        self.assertNotIn(probe, first.current_turn.question.follow_up_questions)
        self.assertNotEqual(second.current_turn.question.question, probe)

    async def test_regenerated_follow_up_is_told_what_was_already_asked(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=3.0,
            follow_up_needed=True,
            follow_up_reason="Answer is too vague.",
        )
        question_agent = MockQuestionGeneratorAgent()
        service = orchestrator(evaluation, "follow_up", question_agent=question_agent)
        state = await service.start_interview(candidate_profile(), interview_config())

        # First answer consumes the canned probe; the second has to regenerate.
        state = await service.submit_answer(state, "Still vague.")
        await service.submit_answer(state, "Still vague.")

        regenerated_round = question_agent.calls[-1]
        avoid = [
            area
            for area in regenerated_round.recommended_question_areas
            if area.startswith("Do not ask again:")
        ]
        self.assertTrue(avoid, regenerated_round.recommended_question_areas)
        self.assertTrue(
            any("Explain YOLO Optimization." in area for area in avoid),
            avoid,
        )


class InterviewOrchestratorTests(unittest.IsolatedAsyncioTestCase):
    async def test_start_interview_creates_first_question(self):
        question_agent = MockQuestionGeneratorAgent()
        service = InterviewOrchestrator(
            planner_agent=MockPlannerAgent(),
            question_generator_agent=question_agent,
            evaluator_agent=MockEvaluatorAgent(AnswerEvaluation(turn_id="turn-1")),
            decision_service=MockDecisionService("next_question"),
        )

        state = await service.start_interview(candidate_profile(), interview_config())

        self.assertEqual(state.current_question_index, 0)
        self.assertEqual(state.interview_plan.rounds[0].topic, "YOLO Optimization")
        self.assertEqual(state.current_turn.question.topic, "YOLO Optimization")
        self.assertEqual(question_agent.calls[0].round_id, "round-1")

    async def test_submit_answer_updates_turn(self):
        evaluation = AnswerEvaluation(turn_id="turn-1", overall_score=6.5, follow_up_needed=False)
        service = orchestrator(evaluation, "next_question")
        state = await service.start_interview(candidate_profile(), interview_config())

        updated_state = await service.submit_answer(state, "I use profiling and TensorRT.")

        self.assertEqual(updated_state.completed_turns[0].answer, "I use profiling and TensorRT.")
        self.assertEqual(updated_state.completed_turns[0].status, "evaluated")
        self.assertEqual(updated_state.completed_turns[0].evaluation.overall_score, 6.5)

    async def test_text_evaluation_and_next_topic_question_run_concurrently(self):
        evaluator_started = asyncio.Event()
        question_started = asyncio.Event()

        class ConcurrentEvaluatorAgent(MockEvaluatorAgent):
            async def evaluate_answer(
                self,
                candidate_profile,
                interview_question,
                answer,
                interview_config,
            ):
                evaluator_started.set()
                await question_started.wait()
                return self.evaluation

        class ConcurrentQuestionGeneratorAgent(MockQuestionGeneratorAgent):
            async def generate_question(
                self,
                candidate_profile,
                interview_round,
                interview_config,
            ):
                if interview_round.round_id == "round-2":
                    question_started.set()
                    await evaluator_started.wait()
                return await super().generate_question(
                    candidate_profile,
                    interview_round,
                    interview_config,
                )

        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=6.5,
            follow_up_needed=False,
        )
        service = InterviewOrchestrator(
            planner_agent=MockPlannerAgent(),
            question_generator_agent=ConcurrentQuestionGeneratorAgent(),
            evaluator_agent=ConcurrentEvaluatorAgent(evaluation),
            decision_service=MockDecisionService("next_question"),
        )
        state = await service.start_interview(candidate_profile(), interview_config())

        updated_state = await asyncio.wait_for(
            service.submit_answer(state, "I use profiling and TensorRT."),
            timeout=0.2,
        )

        self.assertTrue(evaluator_started.is_set())
        self.assertTrue(question_started.is_set())
        self.assertEqual(updated_state.current_turn.question.topic, "FastAPI Deployment")

    async def test_weak_answer_triggers_follow_up(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=3.0,
            follow_up_needed=True,
            follow_up_reason="Answer is too vague.",
        )
        service = orchestrator(evaluation, "follow_up")
        state = await service.start_interview(candidate_profile(), interview_config())

        updated_state = await service.submit_answer(state, "I make it faster.")

        self.assertEqual(updated_state.current_question_index, 0)
        self.assertEqual(updated_state.current_turn.question_type, "follow_up")
        self.assertIn("Clarify your YOLO Optimization", updated_state.current_turn.question.question)

    async def test_strong_answer_increases_difficulty(self):
        question_agent = MockQuestionGeneratorAgent()
        evaluation = AnswerEvaluation(turn_id="turn-1", overall_score=9.0, follow_up_needed=False)
        service = orchestrator(evaluation, "increase_difficulty", question_agent=question_agent)
        state = await service.start_interview(candidate_profile(), interview_config())

        updated_state = await service.submit_answer(
            state,
            "I profile bottlenecks, export to TensorRT, and compare mAP and latency.",
        )

        self.assertEqual(updated_state.current_question_index, 0)
        self.assertEqual(updated_state.current_turn.question.difficulty, "hard")
        self.assertEqual(question_agent.calls[-1].difficulty, "hard")

    async def test_question_count_finishes_before_adaptive_follow_up(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=3.0,
            follow_up_needed=True,
            follow_up_reason="Answer is too vague.",
        )
        service = orchestrator(evaluation, "follow_up")
        config = interview_config().model_copy(update={"question_count": 1})
        state = await service.start_interview(candidate_profile(), config)

        updated_state = await service.submit_answer(state, "I make it faster.")

        self.assertIsNone(updated_state.current_turn)
        self.assertEqual(len(updated_state.completed_turns), 1)

    async def test_voice_memory_is_persisted_and_applied_to_next_question(self):
        question_agent = MockQuestionGeneratorAgent()
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=5.0,
            weaknesses=["Limited latency analysis"],
            missing_concepts=["load testing"],
            follow_up_reason="Probe production validation.",
        )
        service = orchestrator(
            evaluation,
            "next_question",
            question_agent=question_agent,
        )
        config = InterviewConfig(
            mode="voice",
            language="en",
            experience_level="middle",
        )
        state = await service.start_interview(candidate_profile(), config)

        updated_state = await service.submit_answer(
            state,
            "I profile endpoints before deployment.",
        )

        self.assertEqual(updated_state.memory.previous_topics, ["YOLO Optimization"])
        self.assertIn("YOLO Optimization", updated_state.memory.covered_skills)
        self.assertIn("Limited latency analysis", updated_state.memory.weaknesses)
        self.assertIn("load testing", updated_state.memory.follow_up_points)
        generated_round = question_agent.calls[-1]
        self.assertIn(
            "Weakness: Limited latency analysis",
            generated_round.recommended_question_areas,
        )
        restored = type(updated_state).model_validate(
            updated_state.model_dump(mode="json")
        )
        self.assertEqual(restored.memory, updated_state.memory)

    async def test_voice_follow_up_prefers_evaluator_feedback_match(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            overall_score=4.0,
            weaknesses=["No load testing evidence"],
            missing_concepts=["concurrent traffic"],
            follow_up_needed=True,
            follow_up_reason="Probe load testing under concurrent traffic.",
        )
        service = orchestrator(evaluation, "follow_up")
        state = await service.start_interview(
            candidate_profile(),
            InterviewConfig(
                mode="voice",
                language="en",
                experience_level="middle",
            ),
        )
        state.current_turn.question = state.current_turn.question.model_copy(
            update={
                "follow_up_questions": [
                    "Which database schema did you choose?",
                    "How did you load test concurrent traffic?",
                ]
            }
        )

        updated_state = await service.submit_answer(
            state,
            "I deployed the endpoint.",
        )

        self.assertEqual(
            updated_state.current_turn.question.question,
            "How did you load test concurrent traffic?",
        )

    async def test_text_interview_does_not_accumulate_voice_memory(self):
        evaluation = AnswerEvaluation(
            turn_id="turn-1",
            weaknesses=["Do not feed this into text mode"],
        )
        service = orchestrator(evaluation, "next_question")
        state = await service.start_interview(candidate_profile(), interview_config())

        updated_state = await service.submit_answer(state, "Text answer")

        self.assertEqual(updated_state.memory.previous_topics, [])
        self.assertEqual(updated_state.memory.weaknesses, [])


if __name__ == "__main__":
    unittest.main()

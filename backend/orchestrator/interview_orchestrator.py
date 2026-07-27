from __future__ import annotations

from collections.abc import Awaitable, Callable

from services.answer_evaluator.agent import EvaluatorAgent
from services.interview_planner.agent import InterviewPlannerAgent
from services.question_generator.agent import QuestionGeneratorAgent
from shared.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    InterviewConfig,
    InterviewMemoryState,
    InterviewMode,
    InterviewPlan,
    InterviewQuestion,
    InterviewRound,
    InterviewSessionState,
    InterviewTurn,
)
from orchestrator.decision_service import InterviewDecisionService
from orchestrator.memory_service import InterviewMemoryService
from orchestrator.follow_up_service import FollowUpSelectionService


QuestionProvider = Callable[
    [CandidateProfile, InterviewRound, InterviewConfig],
    Awaitable[InterviewQuestion],
]


class InterviewOrchestrator:
    def __init__(
        self,
        planner_agent: InterviewPlannerAgent | None = None,
        question_generator_agent: QuestionGeneratorAgent | None = None,
        evaluator_agent: EvaluatorAgent | None = None,
        decision_service: InterviewDecisionService | None = None,
        memory_service: InterviewMemoryService | None = None,
        follow_up_service: FollowUpSelectionService | None = None,
    ):
        self.planner_agent = planner_agent
        self.question_generator_agent = question_generator_agent
        self.evaluator_agent = evaluator_agent
        self.decision_service = decision_service
        self.memory_service = memory_service or InterviewMemoryService()
        self.follow_up_service = follow_up_service or FollowUpSelectionService()

    async def start_interview(
        self,
        candidate_profile: CandidateProfile,
        interview_config: InterviewConfig,
    ) -> InterviewSessionState:
        interview_plan = await self.planner_agent.create_plan(candidate_profile, interview_config)
        first_round = self._get_round_or_finish(interview_plan, 0)
        first_question = await self.question_generator_agent.generate_question(
            candidate_profile,
            first_round,
            interview_config,
        )

        return InterviewSessionState(
            candidate_profile=candidate_profile,
            interview_config=interview_config,
            interview_plan=interview_plan,
            current_turn=self._create_turn(first_question, first_round, turn_number=1),
            completed_turns=[],
            current_question_index=0,
        )

    async def submit_answer(
        self,
        session_state: InterviewSessionState,
        answer: str,
        *,
        question_provider: QuestionProvider | None = None,
    ) -> InterviewSessionState:
        if session_state.current_turn is None:
            return session_state
        if not isinstance(session_state.current_turn.question, InterviewQuestion):
            return session_state

        answered_turn = session_state.current_turn.model_copy(
            update={
                "answer": answer,
                "candidate_answer": answer,
                "status": "answered",
            }
        )
        evaluation = await self.evaluator_agent.evaluate_answer(
            session_state.candidate_profile,
            answered_turn.question,
            answer,
            session_state.interview_config,
        )
        evaluated_turn = answered_turn.with_evaluation(evaluation)
        completed_turns = [*session_state.completed_turns, evaluated_turn]
        memory = session_state.memory
        if session_state.interview_config.mode == InterviewMode.VOICE:
            current_round = self._current_round(session_state)
            memory = self.memory_service.update(
                memory,
                question=answered_turn.question,
                interview_round=current_round,
                evaluation=evaluation,
            )

        if len(completed_turns) >= session_state.interview_config.question_count:
            return session_state.model_copy(
                update={
                    "current_turn": None,
                    "completed_turns": completed_turns,
                    "memory": memory,
                }
            )

        decision = self.decision_service.decide(evaluation, answered_turn.question, session_state)

        if decision.action == "finish":
            return session_state.model_copy(
                update={
                    "current_turn": None,
                    "completed_turns": completed_turns,
                    "memory": memory,
                }
            )
        if decision.action == "follow_up":
            next_turn = await self._build_follow_up_turn(
                session_state,
                answered_turn.question,
                memory=memory,
                evaluation=evaluation,
                question_provider=question_provider,
                turn_number=len(completed_turns) + 1,
            )
            return session_state.model_copy(
                update={
                    "current_turn": next_turn,
                    "completed_turns": completed_turns,
                    "memory": memory,
                }
            )
        if decision.action == "increase_difficulty":
            current_round = self._round_with_increased_difficulty(session_state)
            current_round = self._round_with_memory(
                session_state,
                current_round,
                memory,
            )
            next_question = await self._generate_question(
                session_state.candidate_profile,
                current_round,
                session_state.interview_config,
                question_provider=question_provider,
            )
            return session_state.model_copy(
                update={
                    "current_turn": self._create_turn(
                        next_question,
                        current_round,
                        turn_number=len(completed_turns) + 1,
                    ),
                    "completed_turns": completed_turns,
                    "memory": memory,
                }
            )

        next_index = session_state.current_question_index + 1
        if next_index >= len(session_state.interview_plan.rounds):
            return session_state.model_copy(
                update={
                    "current_turn": None,
                    "completed_turns": completed_turns,
                    "current_question_index": next_index,
                    "memory": memory,
                }
            )

        next_round = session_state.interview_plan.rounds[next_index]
        next_round = self._round_with_memory(session_state, next_round, memory)
        next_question = await self._generate_question(
            session_state.candidate_profile,
            next_round,
            session_state.interview_config,
            question_provider=question_provider,
        )
        return session_state.model_copy(
            update={
                "current_turn": self._create_turn(
                    next_question,
                    next_round,
                    turn_number=len(completed_turns) + 1,
                ),
                "completed_turns": completed_turns,
                "current_question_index": next_index,
                "memory": memory,
            }
        )

    async def _build_follow_up_turn(
        self,
        session_state: InterviewSessionState,
        current_question: InterviewQuestion,
        *,
        memory: InterviewMemoryState,
        evaluation: AnswerEvaluation,
        question_provider: QuestionProvider | None = None,
        turn_number: int,
    ) -> InterviewTurn:
        asked = self._asked_questions(session_state)
        remaining = [
            probe
            for probe in current_question.follow_up_questions
            if probe.strip() and probe.strip() not in asked
        ]
        if remaining:
            follow_up = remaining[0]
            if session_state.interview_config.mode == InterviewMode.VOICE:
                follow_up = self.follow_up_service.select(remaining, evaluation)
            follow_up_question = current_question.model_copy(
                update={
                    "question": follow_up,
                    "reasoning": "Follow-up requested by evaluation decision.",
                    # Drop the probe we just used. Carrying the full list forward
                    # meant the same follow-up got re-selected every turn and the
                    # candidate was asked one question over and over.
                    "follow_up_questions": [
                        probe for probe in remaining if probe != follow_up
                    ],
                }
            )
            return self._create_turn(
                follow_up_question,
                question_type="follow_up",
                turn_number=turn_number,
            )

        current_round = session_state.interview_plan.rounds[session_state.current_question_index]
        current_round = self._round_with_memory(
            session_state,
            current_round,
            memory,
        )
        current_round = self._round_avoiding_asked(current_round, asked)
        generated_question = await self._generate_question(
            session_state.candidate_profile,
            current_round,
            session_state.interview_config,
            question_provider=question_provider,
        )
        return self._create_turn(
            generated_question,
            current_round,
            question_type="follow_up",
            turn_number=turn_number,
        )

    @staticmethod
    def _round_avoiding_asked(
        interview_round: InterviewRound,
        asked: set[str],
    ) -> InterviewRound:
        """Tell the generator which questions were already asked.

        Without this the follow-up path regenerated from an unchanged round and
        produced the same question again, so a candidate could be asked one
        question several times in a row.
        """
        if not asked:
            return interview_round
        avoid = [f"Do not ask again: {question}" for question in sorted(asked)[-5:]]
        return interview_round.model_copy(
            update={
                "recommended_question_areas": [
                    *interview_round.recommended_question_areas,
                    *avoid,
                ]
            }
        )

    @staticmethod
    def _asked_questions(session_state: InterviewSessionState) -> set[str]:
        asked: set[str] = set()
        turns = [*session_state.completed_turns]
        if session_state.current_turn is not None:
            turns.append(session_state.current_turn)
        for turn in turns:
            question = turn.question
            text = question if isinstance(question, str) else question.question
            if text and text.strip():
                asked.add(text.strip())
        return asked

    async def _generate_question(
        self,
        candidate_profile: CandidateProfile,
        interview_round: InterviewRound,
        interview_config: InterviewConfig,
        *,
        question_provider: QuestionProvider | None,
    ) -> InterviewQuestion:
        if question_provider is not None:
            return await question_provider(
                candidate_profile,
                interview_round,
                interview_config,
            )
        return await self.question_generator_agent.generate_question(
            candidate_profile,
            interview_round,
            interview_config,
        )

    def _round_with_increased_difficulty(self, session_state: InterviewSessionState) -> InterviewRound:
        current_round = session_state.interview_plan.rounds[session_state.current_question_index]
        next_difficulty = {
            "easy": "medium",
            "medium": "hard",
            "hard": "hard",
        }[current_round.difficulty]
        return current_round.model_copy(update={"difficulty": next_difficulty})

    @staticmethod
    def _current_round(session_state: InterviewSessionState) -> InterviewRound:
        index = min(
            session_state.current_question_index,
            max(0, len(session_state.interview_plan.rounds) - 1),
        )
        if not session_state.interview_plan.rounds:
            return InterviewRound(
                round_id="round-1",
                topic=(
                    session_state.current_turn.topic
                    if session_state.current_turn is not None
                    else "General"
                ),
            )
        return session_state.interview_plan.rounds[index]

    def _round_with_memory(
        self,
        session_state: InterviewSessionState,
        interview_round: InterviewRound,
        memory: InterviewMemoryState,
    ) -> InterviewRound:
        if session_state.interview_config.mode != InterviewMode.VOICE:
            return interview_round
        return self.memory_service.apply_to_round(interview_round, memory)

    @staticmethod
    def _get_round_or_finish(interview_plan: InterviewPlan, index: int) -> InterviewRound:
        if not interview_plan.rounds:
            return InterviewRound(round_id="round-1", topic="General CV Deep Dive")
        return interview_plan.rounds[index]

    @staticmethod
    def _create_turn(
        question: InterviewQuestion,
        interview_round: InterviewRound | None = None,
        *,
        question_type: str = "conceptual",
        turn_number: int = 1,
    ) -> InterviewTurn:
        # turn_number keeps this unique. Deriving the id from topic + difficulty
        # alone collided across every turn of a round (follow-ups reuse both),
        # and repositories look turns up by this id.
        slug = question.topic.lower().replace(" ", "-") or "general"
        return InterviewTurn(
            turn_id=f"turn-{turn_number}-{slug}-{question.difficulty}",
            round_id=interview_round.round_id if interview_round is not None else None,
            question=question,
            question_type=question_type,
            difficulty=question.difficulty,
            topic=question.topic,
            expected_signal=question.expected_answer_points,
        )

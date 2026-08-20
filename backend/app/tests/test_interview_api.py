import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.routes.interview import get_interview_orchestrator, router
from core.dependencies import get_current_user, get_interview_preparation_cache
from app.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    CurrentUser,
    InterviewConfig,
    InterviewPlan,
    InterviewQuestion,
    InterviewRound,
    InterviewSessionState,
    InterviewTurn,
)
from database import Base, get_db
from app.repositories import SQLiteInterviewRepository
from orchestrator.decision_service import InterviewDecisionService
from orchestrator.interview_orchestrator import InterviewOrchestrator
from services.answer_evaluator.agent import EvaluatorAgent
from services.interview_planner.agent import InterviewPlannerAgent
from services.interview_preparation import InterviewPreparationCache
from services.question_generator.agent import QuestionGeneratorAgent


class SessionFreshnessLLM:
    def __init__(self):
        self.plan_requests = 0
        self.question_requests = 0

    async def generate_json(self, prompt, output_schema, **kwargs):
        if output_schema is InterviewPlan:
            self.plan_requests += 1
            return InterviewPlan(
                rounds=[
                    InterviewRound(
                        round_id="round-1",
                        topic="YOLO Optimization",
                        difficulty="medium",
                        target_skills=["YOLOv8"],
                    )
                ]
            )
        if output_schema is InterviewQuestion:
            self.question_requests += 1
            return InterviewQuestion(
                question=f"Fresh session question {self.question_requests}",
                language="en",
                topic="YOLO Optimization",
                difficulty="medium",
                follow_up_questions=[
                    f"Fresh follow-up for session question {self.question_requests}"
                ],
            )
        if output_schema is AnswerEvaluation:
            return AnswerEvaluation(
                turn_id="",
                overall_score=4.0,
                feedback="The answer needs one session-specific follow-up.",
                follow_up_needed=True,
                follow_up_reason="Clarify the candidate's actual answer.",
            )
        raise AssertionError(f"Unexpected schema: {output_schema}")


class MockInterviewOrchestrator:
    def __init__(self):
        self.start_calls = 0
        self.plan_calls = 0
        self.submit_calls = 0

    async def create_plan(self, candidate_profile, interview_config):
        self.plan_calls += 1
        return InterviewPlan(
            rounds=[
                InterviewRound(
                    round_id="round-1",
                    topic="YOLO Optimization",
                    difficulty="medium",
                )
            ]
        )

    async def start_interview(
        self,
        candidate_profile,
        interview_config,
        *,
        interview_plan=None,
    ):
        self.start_calls += 1
        question = InterviewQuestion(
            question="How would you optimize YOLOv8 inference?",
            language=interview_config.language,
            topic="YOLO Optimization",
            difficulty="medium",
            reasoning="Candidate has YOLO evidence.",
            expected_answer_points=["profiling", "TensorRT"],
            follow_up_questions=["How do you validate mAP after optimization?"],
        )
        plan = interview_plan or await self.create_plan(candidate_profile, interview_config)
        return InterviewSessionState(
            candidate_profile=candidate_profile,
            interview_config=interview_config,
            interview_plan=plan,
            current_turn=InterviewTurn(
                turn_id="turn-1",
                round_id="round-1",
                question=question,
                difficulty=question.difficulty,
                topic=question.topic,
            ),
        )

    async def submit_answer(self, session_state, answer):
        self.submit_calls += 1
        evaluated_turn = session_state.current_turn.model_copy(
            update={
                "answer": answer,
                "candidate_answer": answer,
                "status": "evaluated",
                "evaluation": AnswerEvaluation(
                    turn_id=session_state.current_turn.turn_id,
                    overall_score=8.0,
                    feedback="Good answer.",
                ),
            }
        )
        return session_state.model_copy(
            update={
                "current_turn": None,
                "completed_turns": [*session_state.completed_turns, evaluated_turn],
                "current_question_index": 1,
            }
        )


class InterviewApiTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=engine)
        self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        self.app = FastAPI()
        self.app.include_router(router)

        def override_get_db():
            yield self.db

        self.app.dependency_overrides[get_db] = override_get_db
        self.orchestrator = MockInterviewOrchestrator()
        self.app.dependency_overrides[get_interview_orchestrator] = lambda: self.orchestrator
        self.preparation_cache = InterviewPreparationCache()
        self.app.dependency_overrides[get_interview_preparation_cache] = lambda: self.preparation_cache
        self.app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid="user-1")
        self.client = TestClient(self.app)

        repository = SQLiteInterviewRepository(self.db)
        self.candidate = repository.create_candidate("Tran Thi B", user_id="user-1")
        repository.save_candidate_profile(
            self.candidate.candidate_id,
            CandidateProfile(
                name="Tran Thi B",
                skills=["YOLOv8", "FastAPI"],
                specialization="Computer Vision",
            ),
            user_id="user-1",
        )

    def tearDown(self):
        self.app.dependency_overrides.clear()
        self.db.close()

    def test_start_interview(self):
        with self.assertLogs("gateway.api.interview", level="INFO") as logs:
            response = self.client.post(
                "/api/v2/interview/start",
                json={
                    "candidate_id": self.candidate.candidate_id,
                    "interview_config": {
                        "language": "en",
                        "experience_level": "middle",
                        "duration_minutes": 30,
                        "interview_style": "technical",
                    },
                },
            )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["state"]["phase"], "opening")
        self.assertEqual(body["state"]["current_turn"]["question"]["topic"], "Introduction")
        self.assertIn("Tran Thi B", body["state"]["current_turn"]["question"]["question"])
        self.assertIn(
            "briefly introduce yourself",
            body["state"]["current_turn"]["question"]["question"],
        )
        self.assertEqual(
            body["state"]["pending_turn"]["question"]["topic"],
            "YOLO Optimization",
        )
        self.assertEqual(body["state"]["interview_config"]["language"], "en")
        self.assertEqual(body["state"]["interview_config"]["mode"], "text")
        self.assertTrue(body["session_id"])
        self.assertTrue(body["started_at"])
        self.assertTrue(body["started_at"].endswith(("Z", "+00:00")))
        events = {record.event for record in logs.records}
        self.assertTrue(
            {
                "interview.load_candidate",
                "interview.preparation",
                "interview.persistence",
                "interview.total_start",
            }.issubset(events)
        )
        repository = SQLiteInterviewRepository(self.db)
        self.assertEqual(
            repository.get_session(body["session_id"], user_id="user-1").status,
            "in_progress",
        )

    def test_start_voice_mode_is_persisted_without_changing_endpoint(self):
        response = self.client.post(
            "/api/v2/interview/start",
            json={
                "candidate_id": self.candidate.candidate_id,
                "interview_config": {
                    "mode": "voice",
                    "language": "en",
                    "experience_level": "middle",
                },
            },
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["state"]["interview_config"]["mode"], "voice")
        repository = SQLiteInterviewRepository(self.db)
        session = repository.get_session(body["session_id"], user_id="user-1")
        self.assertEqual(session.state_payload["interview_config"]["mode"], "voice")

    def test_prepared_interview_is_reused_by_start(self):
        payload = {
            "candidate_id": self.candidate.candidate_id,
            "interview_config": {
                "mode": "text",
                "language": "en",
                "experience_level": "middle",
            },
        }

        prepare_response = self.client.post(
            "/api/v2/interview/prepare",
            json=payload,
        )
        start_response = self.client.post(
            "/api/v2/interview/start",
            json=payload,
        )

        self.assertEqual(prepare_response.status_code, 200)
        self.assertEqual(prepare_response.json()["status"], "ready")
        self.assertEqual(start_response.status_code, 200)
        self.assertEqual(self.orchestrator.start_calls, 1)
        self.assertEqual(self.orchestrator.plan_calls, 1)

    def test_persisted_blueprint_never_replays_questions_across_sessions(self):
        llm = SessionFreshnessLLM()
        orchestrator = InterviewOrchestrator(
            planner_agent=InterviewPlannerAgent(llm),
            question_generator_agent=QuestionGeneratorAgent(llm),
            evaluator_agent=EvaluatorAgent(llm, task_type="simple"),
            decision_service=InterviewDecisionService(),
        )
        self.app.dependency_overrides[get_interview_orchestrator] = lambda: orchestrator
        cache = InterviewPreparationCache()
        self.app.dependency_overrides[get_interview_preparation_cache] = lambda: cache
        payload = {
            "candidate_id": self.candidate.candidate_id,
            "interview_config": {
                "mode": "text",
                "language": "en",
                "experience_level": "middle",
            },
        }

        prepared = self.client.post("/api/v2/interview/prepare", json=payload)
        cache = InterviewPreparationCache()  # simulate another process/restart
        first = self.client.post("/api/v2/interview/start", json=payload)
        cache = InterviewPreparationCache()  # force persistent reuse again
        second = self.client.post("/api/v2/interview/start", json=payload)

        self.assertEqual(prepared.status_code, 200)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertNotEqual(first.json()["session_id"], second.json()["session_id"])
        first_question = first.json()["state"]["pending_turn"]["question"]["question"]
        second_question = second.json()["state"]["pending_turn"]["question"]["question"]
        self.assertNotEqual(first_question, second_question)
        self.assertEqual(llm.plan_requests, 1)
        self.assertEqual(llm.question_requests, 2)

        follow_ups = []
        for response, answer in (
            (first, "I optimized the first pipeline."),
            (second, "I optimized the second pipeline differently."),
        ):
            session_id = response.json()["session_id"]
            opening_turn_id = response.json()["state"]["current_turn"]["turn_id"]
            opening = self.client.post(
                f"/api/v2/interview/{session_id}/answer",
                json={
                    "turn_id": opening_turn_id,
                    "answer": "I build computer vision systems.",
                },
            )
            technical = self.client.post(
                f"/api/v2/interview/{session_id}/answer",
                json={
                    "turn_id": opening.json()["state"]["current_turn"]["turn_id"],
                    "answer": answer,
                },
            )
            self.assertEqual(opening.status_code, 200)
            self.assertEqual(technical.status_code, 200)
            follow_ups.append(
                technical.json()["state"]["current_turn"]["question"]["question"]
            )
        self.assertNotEqual(follow_ups[0], follow_ups[1])

    def test_opening_answer_reveals_first_question_and_final_answer_enters_closing(self):
        start_response = self.client.post(
            "/api/v2/interview/start",
            json={
                "candidate_id": self.candidate.candidate_id,
                "interview_config": {"language": "en", "experience_level": "middle"},
            },
        )
        session_id = start_response.json()["session_id"]
        opening_turn_id = start_response.json()["state"]["current_turn"]["turn_id"]

        opening_response = self.client.post(
            f"/api/v2/interview/{session_id}/answer",
            json={
                "turn_id": opening_turn_id,
                "answer": "I build and optimize computer vision systems.",
            },
        )

        self.assertEqual(opening_response.status_code, 200)
        opening_body = opening_response.json()
        self.assertEqual(opening_body["state"]["phase"], "interviewing")
        self.assertEqual(
            opening_body["state"]["opening_turn"]["answer"],
            "I build and optimize computer vision systems.",
        )
        self.assertIsNone(opening_body["state"]["opening_turn"]["evaluation"])
        self.assertEqual(
            opening_body["state"]["current_turn"]["question"]["topic"],
            "YOLO Optimization",
        )
        self.assertEqual(opening_body["state"]["completed_turns"], [])

        with self.assertLogs("gateway.api.interview", level="INFO") as logs:
            final_response = self.client.post(
                f"/api/v2/interview/{session_id}/answer",
                json={
                    "turn_id": opening_body["state"]["current_turn"]["turn_id"],
                    "answer": "I profile bottlenecks and export to TensorRT.",
                },
            )

        self.assertEqual(final_response.status_code, 200)
        body = final_response.json()
        self.assertEqual(body["state"]["phase"], "closing")
        self.assertIsNone(body["state"]["current_turn"])
        self.assertEqual(body["state"]["completed_turns"][0]["status"], "evaluated")
        self.assertEqual(
            body["state"]["completed_turns"][0]["answer"],
            "I profile bottlenecks and export to TensorRT.",
        )
        repository = SQLiteInterviewRepository(self.db)
        self.assertEqual(
            repository.get_session(session_id, user_id="user-1").status,
            "completed",
        )
        self.assertIn("answer.total", {record.event for record in logs.records})

    def test_exact_answer_replay_returns_current_state_without_second_evaluation(self):
        started = self.client.post(
            "/api/v2/interview/start",
            json={
                "candidate_id": self.candidate.candidate_id,
                "interview_config": {
                    "language": "en",
                    "experience_level": "middle",
                    "question_count": 1,
                },
            },
        )
        session_id = started.json()["session_id"]
        opening_turn_id = started.json()["state"]["current_turn"]["turn_id"]
        opening = self.client.post(
            f"/api/v2/interview/{session_id}/answer",
            json={"turn_id": opening_turn_id, "answer": "I build CV systems."},
        )
        technical_turn_id = opening.json()["state"]["current_turn"]["turn_id"]
        payload = {
            "turn_id": technical_turn_id,
            "answer": "I profile bottlenecks and validate the optimized model.",
        }

        first = self.client.post(
            f"/api/v2/interview/{session_id}/answer", json=payload
        )
        replay = self.client.post(
            f"/api/v2/interview/{session_id}/answer", json=payload
        )

        self.assertEqual(first.status_code, 200)
        self.assertEqual(replay.status_code, 200)
        self.assertFalse(first.json()["answer_replayed"])
        self.assertTrue(replay.json()["answer_replayed"])
        self.assertEqual(replay.json()["state"], first.json()["state"])
        self.assertEqual(self.orchestrator.submit_calls, 1)
        repository = SQLiteInterviewRepository(self.db)
        self.assertEqual(len(repository.get_turns(session_id, user_id="user-1")), 2)

    def test_get_interview_session(self):
        start_response = self.client.post(
            "/api/v2/interview/start",
            json={
                "candidate_id": self.candidate.candidate_id,
                "interview_config": {"language": "vi", "experience_level": "junior"},
            },
        )
        session_id = start_response.json()["session_id"]

        response = self.client.get(f"/api/v2/interview/{session_id}")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["session_id"], session_id)
        self.assertEqual(body["started_at"], start_response.json()["started_at"])
        self.assertEqual(body["state"]["candidate_profile"]["name"], "Tran Thi B")
        self.assertEqual(body["state"]["phase"], "opening")
        self.assertEqual(
            body["state"]["pending_turn"]["question"]["topic"],
            "YOLO Optimization",
        )


if __name__ == "__main__":
    unittest.main()

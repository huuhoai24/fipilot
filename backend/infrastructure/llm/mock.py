from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Any, TypeVar

from pydantic import BaseModel

from infrastructure.llm.base import BaseLLMService, LLMTaskType
from services.profile_scanner.schemas import ExtractedSkillEvidence, ResumeExtractionResult
from shared.schemas.candidate import (
    CandidateEducation,
    CandidateExperience,
    CandidateProject,
)
from shared.schemas.evaluation import AnswerEvaluation, EvaluationScore
from shared.schemas.interview import (
    InterviewPlan,
    InterviewQuestion,
    InterviewRound,
)
from shared.schemas.report import FinalReport, TopicScore

SchemaT = TypeVar("SchemaT", bound=BaseModel)


class MockLLMService(BaseLLMService):
    """Mock LLM provider for local offline development and testing."""

    def route_model(self, task_type: LLMTaskType = "simple", model: str | None = None) -> str:
        return "mock-model"

    async def generate_text(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        task_type: LLMTaskType = "simple",
        model: str | None = None,
        temperature: float = 0.2,
        timeout_seconds: float | None = None,
    ) -> str:
        return "Chào bạn, hãy chia sẻ về kinh nghiệm của bạn với React và FastAPI."

    async def stream_text(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        task_type: LLMTaskType = "simple",
        model: str | None = None,
        temperature: float = 0.2,
        timeout_seconds: float | None = None,
        output_schema: type[BaseModel] | None = None,
    ) -> AsyncIterator[str]:
        chunks = [
            "Chào bạn, ",
            "chúng ta hãy bắt đầu ",
            "với câu hỏi đầu tiên: ",
            "Bạn hãy chia sẻ về kinh nghiệm ",
            "làm việc thực tế với React và TypeScript ",
            "trong các dự án gần đây của bạn.",
        ]
        for chunk in chunks:
            await asyncio.sleep(0.05)
            yield chunk

    async def generate_json(
        self,
        prompt: str,
        output_schema: type[SchemaT],
        *,
        system_instruction: str | None = None,
        task_type: LLMTaskType = "complex",
        model: str | None = None,
        temperature: float = 0.1,
        timeout_seconds: float | None = None,
        thinking_budget: int | None = None,
        operation: str | None = None,
    ) -> SchemaT:
        schema_name = getattr(output_schema, "__name__", str(output_schema))

        if "ResumeExtractionResult" in schema_name:
            return ResumeExtractionResult(
                document_type="resume",
                classification_confidence=0.95,
                name="Nguyễn Hữu Hoài",
                years_experience=2.5,
                recent_role="Fullstack / Frontend Developer",
                skills=["React", "TypeScript", "Python", "FastAPI", "Tailwind CSS", "Node.js", "SQL"],
                skill_evidence=[
                    ExtractedSkillEvidence(
                        skill="React",
                        evidence="Xây dựng giao diện ứng dụng web tương tác với React và TypeScript",
                        source_section="Projects",
                    ),
                    ExtractedSkillEvidence(
                        skill="FastAPI",
                        evidence="Phát triển REST API và WebSocket backend hiệu năng cao",
                        source_section="Projects",
                    ),
                    ExtractedSkillEvidence(
                        skill="Python",
                        evidence="Lập trình backend và xử lý dữ liệu với Python",
                        source_section="Work Experience",
                    ),
                ],
                projects=[
                    CandidateProject(
                        name="AI Interview Platform",
                        description="Hệ thống phỏng vấn AI với phân tích CV và đánh giá câu trả lời trực tiếp.",
                        technologies=["React", "FastAPI", "TypeScript", "Python"],
                        role="Fullstack Developer",
                    )
                ],
                experiences=[
                    CandidateExperience(
                        company="Technology Corp",
                        title="Software Engineer",
                        start_date="2023-01-01",
                        end_date="Present",
                        description="Phát triển và tối ưu hóa hệ thống web fullstack.",
                        technologies=["React", "Python", "FastAPI"],
                    )
                ],
                education=[
                    CandidateEducation(
                        institution="University of Technology",
                        degree="Bachelor",
                        field_of_study="Computer Science",
                        start_date="2019-09-01",
                        end_date="2023-06-30",
                    )
                ],
                specialization="Fullstack Web Development",
                confidence_score=0.95,
            )  # type: ignore

        if "InterviewPlan" in schema_name:
            return InterviewPlan(
                duration_minutes=30,
                rounds=[
                    InterviewRound(
                        round_id="round-1",
                        topic="Frontend & React Architecture",
                        objective="Đánh giá kiến thức React, tối ưu hiệu năng và quản lý state.",
                        difficulty="medium",
                        reasoning="Ứng viên có kinh nghiệm với React và TypeScript.",
                        recommended_question_areas=["React Hooks", "State Management", "Performance Optimization"],
                        target_skills=["React", "TypeScript"],
                        question_budget=2,
                        weight=0.5,
                    ),
                    InterviewRound(
                        round_id="round-2",
                        topic="Backend API & System Design",
                        objective="Đánh giá thiết kế REST API, WebSocket và xử lý bất đồng bộ.",
                        difficulty="medium",
                        reasoning="Ứng viên đã xây dựng backend với FastAPI và Python.",
                        recommended_question_areas=["FastAPI", "AsyncIO", "API Security"],
                        target_skills=["FastAPI", "Python"],
                        question_budget=2,
                        weight=0.5,
                    ),
                ],
                coverage_goals=["Kiểm tra kỹ năng giải quyết vấn đề thực tế trong dự án."],
                risk_areas=["Đào sâu cách xử lý lỗi và scaling hệ thống."],
                planner_summary="Kế hoạch phỏng vấn cân đối giữa Frontend và Backend thực chiến.",
            )  # type: ignore

        if "InterviewQuestion" in schema_name:
            return InterviewQuestion(
                question="Bạn hãy giải thích cách quản lý state và tối ưu hóa số lần re-render trong một ứng dụng React lớn?",
                language="vi",
                topic="Frontend & React Architecture",
                difficulty="medium",
                reasoning="Đánh giá kỹ năng tối ưu hiệu năng ứng dụng React thực tế.",
                expected_answer_points=[
                    "Sử dụng useMemo, useCallback hợp lý",
                    "Chia nhỏ component và cấu trúc state phân tầng",
                    "Sử dụng thư viện state quản lý tập trung (Zustand, Redux)",
                ],
                follow_up_questions=[
                    "Bạn đã từng dùng React DevTools Profiler để tìm nguyên nhân gây lag chưa?",
                ],
            )  # type: ignore

        if "AnswerEvaluation" in schema_name:
            return AnswerEvaluation(
                turn_id="turn-mock",
                scores=EvaluationScore(
                    technical_score=8.5,
                    depth_score=8.0,
                    communication_score=9.0,
                    engineering_mindset_score=8.5,
                    overall_score=8.5,
                ),
                overall_score=8.5,
                technical_score=8.5,
                communication_score=9.0,
                correctness_score=8.5,
                strengths=[
                    "Nắm chắc khái niệm và cơ chế hoạt động của React",
                    "Giao tiếp mạch lạc, cấu trúc câu trả lời rõ ràng",
                ],
                weaknesses=[
                    "Có thể bổ sung thêm ví dụ cụ thể về benchmark hiệu năng trước và sau khi tối ưu",
                ],
                missing_topics=[],
                missing_concepts=[],
                feedback="Câu trả lời rất tốt, thể hiện kinh nghiệm thực tiễn và tư duy kỹ thuật tốt.",
                follow_up_needed=False,
            )  # type: ignore

        if "FinalReport" in schema_name or "InterviewReport" in schema_name:
            return FinalReport(
                session_id="mock-session",
                overall_score=8.5,
                recommendation="hire",
                summary="Ứng viên thể hiện năng lực chuyên môn xuất sắc, tư duy giải quyết vấn đề tốt và giao tiếp tự tin.",
                strengths=[
                    "Kỹ năng React và TypeScript vững vàng",
                    "Hiểu biết tốt về kiến trúc REST API và Backend",
                    "Thái độ chuyên nghiệp, trả lời đúng trọng tâm",
                ],
                weaknesses=[
                    "Cần tiếp tục trau dồi thêm về distributed systems và cloud deployment",
                ],
                topic_scores=[
                    TopicScore(
                        topic="Frontend & React Architecture",
                        score=8.5,
                        evidence=["Giải thích rõ ràng cơ chế render và state management"],
                    ),
                    TopicScore(
                        topic="Backend API & System Design",
                        score=8.5,
                        evidence=["Nắm vững kiến trúc async và thiết kế API"],
                    ),
                ],
                learning_plan=[
                    "Nghiên cứu sâu hơn về Server-Side Rendering (SSR) và Next.js",
                    "Thực hành thiết kế hệ thống Microservices quy mô lớn",
                ],
            )  # type: ignore

        try:
            return output_schema()
        except Exception:
            return None  # type: ignore

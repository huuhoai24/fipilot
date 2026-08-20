import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import func, select

from fipilot.database import database_session
from fipilot.models import InterviewReport, InterviewSession, InterviewTurn, Resume

logger = logging.getLogger(__name__)


def save_resume(client_id: uuid.UUID | None, filename: str, profile: dict[str, Any]) -> str | None:
    if client_id is None:
        return None
    with database_session() as db:
        if db is None:
            return None
        resume = Resume(client_id=client_id, filename=filename, profile=profile)
        db.add(resume)
        db.flush()
        return str(resume.id)


def save_interview_session(
    *,
    session_id: str | None,
    client_id: uuid.UUID | None,
    resume_id: uuid.UUID | None,
    role: str,
    level: str,
    custom_description: str,
    work_experience: list[dict[str, Any]],
) -> None:
    if session_id is None or client_id is None:
        return
    with database_session() as db:
        if db is None:
            return
        interview = db.get(InterviewSession, session_id)
        if interview is None:
            interview = InterviewSession(
                id=session_id,
                client_id=client_id,
                resume_id=resume_id,
                role=role,
                level=level,
                custom_description=custom_description,
                work_experience=work_experience,
            )
            db.add(interview)
            return
        if interview.client_id != client_id:
            raise ValueError("Interview session belongs to another client")
        interview.resume_id = resume_id
        interview.role = role
        interview.level = level
        interview.custom_description = custom_description
        interview.work_experience = work_experience


def save_interview_turn(
    *,
    session_id: str | None,
    client_id: uuid.UUID | None,
    question: dict[str, Any],
    answer: str,
    evaluation: dict[str, Any],
) -> None:
    if session_id is None or client_id is None:
        return
    with database_session() as db:
        if db is None:
            return
        interview = db.get(InterviewSession, session_id)
        if interview is None or interview.client_id != client_id:
            raise ValueError("Interview session was not found for this client")
        next_sequence = db.scalar(
            select(func.coalesce(func.max(InterviewTurn.sequence), 0) + 1).where(
                InterviewTurn.session_id == session_id
            )
        )
        db.add(
            InterviewTurn(
                session_id=session_id,
                sequence=int(next_sequence or 1),
                question=question,
                answer=answer,
                evaluation=evaluation,
            )
        )
        interview.status = "in_progress"


def save_interview_report(
    *, session_id: str | None, client_id: uuid.UUID | None, content: dict[str, Any]
) -> None:
    if session_id is None or client_id is None:
        return
    with database_session() as db:
        if db is None:
            return
        interview = db.get(InterviewSession, session_id)
        if interview is None or interview.client_id != client_id:
            raise ValueError("Interview session was not found for this client")
        report = db.scalar(
            select(InterviewReport).where(InterviewReport.session_id == session_id)
        )
        if report is None:
            db.add(InterviewReport(session_id=session_id, content=content))
        else:
            report.content = content
        interview.status = "completed"
        interview.completed_at = datetime.now(timezone.utc)


def get_latest_resume(client_id: uuid.UUID) -> dict[str, Any] | None:
    with database_session() as db:
        if db is None:
            return None
        resume = db.scalar(
            select(Resume)
            .where(Resume.client_id == client_id)
            .order_by(Resume.created_at.desc())
            .limit(1)
        )
        if resume is None:
            return None
        return {"id": str(resume.id), "filename": resume.filename, "profile": resume.profile}


def get_interview_result(session_id: str, client_id: uuid.UUID) -> dict[str, Any] | None:
    with database_session() as db:
        if db is None:
            return None
        interview = db.get(InterviewSession, session_id)
        if interview is None or interview.client_id != client_id:
            return None
        report = db.scalar(
            select(InterviewReport).where(InterviewReport.session_id == session_id)
        )
        turns = db.scalars(
            select(InterviewTurn)
            .where(InterviewTurn.session_id == session_id)
            .order_by(InterviewTurn.sequence)
        ).all()
        return {
            "report": report.content if report is not None else None,
            "turns": [
                {
                    "question": turn.question,
                    "answer": turn.answer,
                    "timestamp": turn.created_at.isoformat(),
                }
                for turn in turns
            ],
        }


def list_interview_sessions(client_id: uuid.UUID) -> list[dict[str, Any]]:
    with database_session() as db:
        if db is None:
            return []
        sessions = db.scalars(
            select(InterviewSession)
            .where(InterviewSession.client_id == client_id)
            .order_by(InterviewSession.created_at.desc())
        ).all()
        results: list[dict[str, Any]] = []
        for session in sessions:
            report = db.scalar(
                select(InterviewReport).where(InterviewReport.session_id == session.id)
            )
            results.append(
                {
                    "session_id": session.id,
                    "role": session.role,
                    "level": session.level,
                    "status": session.status,
                    "created_at": session.created_at.isoformat(),
                    "completed_at": session.completed_at.isoformat()
                    if session.completed_at is not None
                    else None,
                    "normalized_score": report.content.get("normalized_score")
                    if report is not None
                    else None,
                }
            )
        return results

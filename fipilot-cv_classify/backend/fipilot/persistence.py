import logging
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import func, select

from fipilot.database import database_session
from fipilot.models import InterviewReport, InterviewSession, InterviewTurn, Resume

logger = logging.getLogger(__name__)


def candidate_profile_context(
    profile: dict[str, Any] | None,
    *,
    fallback_work_experience: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    snapshot = deepcopy(profile) if isinstance(profile, dict) else {}
    work_experience = snapshot.get("workExperience")
    if not isinstance(work_experience, list):
        work_experience = list(fallback_work_experience or [])
    skills = snapshot.get("skills")
    if not isinstance(skills, list):
        skills = []
    skill_evidence = snapshot.get("skillEvidence")
    if not isinstance(skill_evidence, list):
        skill_evidence = []
    education = snapshot.get("education")
    if not isinstance(education, list):
        education = []
    snapshot["workExperience"] = deepcopy(work_experience)
    snapshot["skills"] = deepcopy(skills)
    snapshot["skillEvidence"] = deepcopy(skill_evidence)
    snapshot["education"] = deepcopy(education)
    return {
        "candidate_profile": snapshot,
        "work_experience": deepcopy(work_experience),
        "skills": deepcopy(skills),
        "skill_evidence": deepcopy(skill_evidence),
        "education": deepcopy(education),
    }


def normalize_report_score_scale(content: dict[str, Any]) -> dict[str, Any]:
    report = deepcopy(content)
    if report.get("score_scale") == 10:
        return report

    normalized_score = report.get("normalized_score")
    if isinstance(normalized_score, (int, float)) and not isinstance(normalized_score, bool):
        report["normalized_score"] = round(max(0.0, min(10.0, normalized_score * 2)), 2)
    for assessment in report.get("assessments") or []:
        raw_score = assessment.get("raw_score")
        if isinstance(raw_score, (int, float)) and not isinstance(raw_score, bool):
            assessment["raw_score"] = round(max(0.0, min(10.0, raw_score * 10 / 3)), 2)
    report["score_scale"] = 10
    return report


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


def get_owned_resume_profile(
    resume_id: uuid.UUID,
    client_id: uuid.UUID,
) -> dict[str, Any]:
    with database_session() as db:
        if db is None:
            raise RuntimeError("Resume persistence is unavailable")
        resume = db.get(Resume, resume_id)
        if resume is None or resume.client_id != client_id:
            raise ValueError("Resume was not found for this client")
        return deepcopy(resume.profile)


def get_interview_session_context(
    session_id: str,
    client_id: uuid.UUID,
) -> dict[str, Any] | None:
    with database_session() as db:
        if db is None:
            return None
        interview = db.get(InterviewSession, session_id)
        if interview is None:
            return None
        if interview.client_id != client_id:
            raise ValueError("Interview session belongs to another client")
        return {
            "resume_id": interview.resume_id,
            "role": interview.role,
            "level": interview.level,
            "custom_description": interview.custom_description,
        } | candidate_profile_context(
            getattr(interview, "candidate_profile", None),
            fallback_work_experience=interview.work_experience,
        )


def get_interview_report_source(
    session_id: str,
    client_id: uuid.UUID,
) -> dict[str, Any] | None:
    with database_session() as db:
        if db is None:
            return None
        interview = db.get(InterviewSession, session_id)
        if interview is None:
            return None
        if interview.client_id != client_id:
            raise ValueError("Interview session belongs to another client")
        turns = db.scalars(
            select(InterviewTurn)
            .where(InterviewTurn.session_id == session_id)
            .order_by(InterviewTurn.sequence)
        ).all()
        profile_snapshot = getattr(interview, "candidate_profile", None)
        candidate_context = (
            deepcopy(profile_snapshot)
            if isinstance(profile_snapshot, dict) and profile_snapshot
            else deepcopy(interview.work_experience)
        )
        return {
            "role": interview.role,
            "level": interview.level,
            "candidate_context": candidate_context,
            "turns": [
                {
                    "question": deepcopy(turn.question),
                    "answer": turn.answer,
                    "timestamp": turn.created_at.isoformat(),
                    "evaluation": deepcopy(turn.evaluation),
                }
                for turn in turns
            ],
        }


def save_interview_session(
    *,
    session_id: str | None,
    client_id: uuid.UUID | None,
    resume_id: uuid.UUID | None,
    role: str,
    level: str,
    custom_description: str,
    work_experience: list[dict[str, Any]],
    candidate_profile: dict[str, Any] | None = None,
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
                candidate_profile=candidate_profile_context(
                    candidate_profile,
                    fallback_work_experience=work_experience,
                )["candidate_profile"],
            )
            db.add(interview)
            return
        if interview.client_id != client_id:
            raise ValueError("Interview session belongs to another client")


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
            "report": normalize_report_score_scale(report.content)
            if report is not None
            else None,
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
            normalized_report = (
                normalize_report_score_scale(report.content)
                if report is not None
                else None
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
                    "normalized_score": normalized_report.get("normalized_score")
                    if normalized_report is not None
                    else None,
                    "score_scale": 10,
                }
            )
        return results

import json
import logging
import os
import random
import tempfile
import time
from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path
from uuid import UUID

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field

load_dotenv()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Loading the resume extraction model")
    get_extractor()
    logger.info("Resume extraction model is ready")
    yield


app = FastAPI(title="FiPilot Resume API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_AUDIO_SIZE = 20 * 1024 * 1024

_extractor = None
_question_llm = None


class SpeechRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2_000)


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=8, max_length=200)


class LoginRequest(BaseModel):
    identifier: str = Field(min_length=1, max_length=320)
    password: str = Field(min_length=1, max_length=200)


class InterviewQuestionRequest(BaseModel):
    client_id: UUID | None = None
    session_id: str | None = Field(default=None, min_length=1, max_length=100)
    resume_id: UUID | None = None
    role: str = Field(min_length=1, max_length=200)
    level: str = Field(min_length=1, max_length=50)
    work_experience: list[dict] = Field(min_length=1, max_length=20)
    custom_description: str = Field(default="", max_length=10_000)
    count: int = Field(default=1, ge=1, le=1)


class InterviewNextRequest(BaseModel):
    client_id: UUID | None = None
    session_id: str | None = Field(default=None, min_length=1, max_length=100)
    resume_id: UUID | None = None
    role: str = Field(min_length=1, max_length=200)
    level: str = Field(min_length=1, max_length=50)
    work_experience: list[dict] = Field(min_length=1, max_length=20)
    custom_description: str = Field(default="", max_length=10_000)
    current_question: dict
    current_project: dict
    answer: str = Field(min_length=1, max_length=20_000)
    follow_up_count: int = Field(default=0, ge=0, le=2)
    used_project_names: list[str] = Field(default_factory=list, max_length=20)


class InterviewTurnRequest(BaseModel):
    question: dict
    answer: str = Field(max_length=20_000)
    timestamp: str = Field(min_length=1, max_length=100)


class InterviewReportRequest(BaseModel):
    client_id: UUID | None = None
    session_id: str | None = Field(default=None, min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=200)
    level: str = Field(min_length=1, max_length=50)
    turns: list[InterviewTurnRequest] = Field(default_factory=list, max_length=30)


def get_extractor():
    global _extractor
    if _extractor is None:
        from fipilot.resume_extraction import ResumeExtract

        _extractor = ResumeExtract()
    return _extractor


def get_question_llm():
    global _question_llm
    if _question_llm is None:
        from fipilot.model.llm_client import LLMClient

        _question_llm = LLMClient()
    return _question_llm


@lru_cache(maxsize=100)
def search_domain_hits(description: str, role: str) -> tuple[dict, ...]:
    try:
        from fipilot.knowledge_index import search_domain

        return tuple(search_domain(description, role, top_k=3))
    except Exception:
        logger.warning("Domain knowledge lookup failed; continuing with resume context", exc_info=True)
        return ()


def get_domain_hits(project: dict, role: str) -> list[dict]:
    description = str(project.get("jobDescription", "")).strip()
    return list(search_domain_hits(description, role)) if description else []


def choose_project(work_experience: list[dict], used_project_names: list[str] | None = None) -> dict:
    used_names = set(used_project_names or [])
    candidates = [
        project
        for project in work_experience
        if str(project.get("name", "")).strip() not in used_names
    ]
    return random.choice(candidates or work_experience)


@app.get("/health")
def health():
    from fipilot.database import database_url

    return {"status": "ok", "database_configured": database_url() is not None}


def persist(action, /, **kwargs) -> None:
    try:
        action(**kwargs)
    except Exception:
        logger.exception("Database persistence failed during %s", action.__name__)


def auth_user_payload(user) -> dict[str, str]:
    return {"id": str(user.id), "name": user.full_name, "email": user.email}


def set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="fipilot_session",
        value=token,
        max_age=30 * 24 * 60 * 60,
        httponly=True,
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        samesite="lax",
        path="/",
    )


@app.post("/api/v1/auth/register")
def register(request: RegisterRequest):
    try:
        from fipilot.auth import create_session, create_user

        user = create_user(request.email, request.full_name, request.password)
        token = create_session(user.id)
        response = Response(content=json.dumps(auth_user_payload(user)), media_type="application/json")
        set_auth_cookie(response, token)
        return response
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except Exception as error:
        logger.exception("Registration failed")
        raise HTTPException(status_code=503, detail="Authentication service is unavailable") from error


@app.post("/api/v1/auth/login")
def login(request: LoginRequest):
    try:
        from fipilot.auth import authenticate, create_session

        user = authenticate(request.identifier, request.password)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        token = create_session(user.id)
        response = Response(content=json.dumps(auth_user_payload(user)), media_type="application/json")
        set_auth_cookie(response, token)
        return response
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Login failed")
        raise HTTPException(status_code=503, detail="Authentication service is unavailable") from error


@app.get("/api/v1/auth/me")
def current_user(request: Request):
    try:
        from fipilot.auth import get_user_from_token

        user = get_user_from_token(request.cookies.get("fipilot_session"))
    except Exception as error:
        logger.exception("Could not load current user")
        raise HTTPException(status_code=503, detail="Authentication service is unavailable") from error
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return auth_user_payload(user)


@app.post("/api/v1/auth/logout")
def logout(request: Request):
    try:
        from fipilot.auth import revoke_token

        revoke_token(request.cookies.get("fipilot_session"))
    except Exception:
        logger.exception("Logout persistence failed")
    response = Response(content=json.dumps({"ok": True}), media_type="application/json")
    response.delete_cookie("fipilot_session", path="/")
    return response


@app.post("/api/v1/speech")
def synthesize_speech(request: SpeechRequest):
    try:
        from fipilot.tts import synthesize_speech as create_audio

        audio = create_audio(request.text)
        return Response(content=audio, media_type="audio/wav")
    except Exception as error:
        logger.exception("Speech synthesis failed")
        raise HTTPException(status_code=502, detail="Speech synthesis failed") from error


@app.post("/api/v1/speech/recognize")
async def recognize_speech(audio: UploadFile = File(...)):
    content = await audio.read()
    if not content:
        raise HTTPException(status_code=400, detail="The recording is empty")
    if len(content) > MAX_AUDIO_SIZE:
        raise HTTPException(status_code=413, detail="The recording is too large")
    try:
        from fipilot.stt import recognize_vietnamese

        transcript = recognize_vietnamese(content)
        if not transcript:
            raise HTTPException(
                status_code=422,
                detail="Không nhận diện được giọng nói trong bản ghi âm",
            )
        return {"text": transcript, "locale": "vi-VN"}
    except HTTPException:
        raise
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        logger.exception("Speech recognition failed")
        raise HTTPException(status_code=502, detail="Speech recognition failed") from error


@app.post("/api/v1/interview/questions")
def generate_interview_questions(request: InterviewQuestionRequest):
    try:
        from fipilot.interview_engine import generate_question
        from fipilot.persistence import save_interview_session

        persist(
            save_interview_session,
            session_id=request.session_id,
            client_id=request.client_id,
            resume_id=request.resume_id,
            role=request.role,
            level=request.level,
            custom_description=request.custom_description,
            work_experience=request.work_experience,
        )

        project = choose_project(request.work_experience)
        question = generate_question(
            get_question_llm(),
            project,
            request.role,
            request.level,
            get_domain_hits(project, request.role),
        )
        question["project"] = str(project.get("name", question["company"])).strip()
        question["project_context"] = project
        return {"questions": [question]}
    except Exception as error:
        logger.exception("Interview question generation failed")
        raise HTTPException(
            status_code=502,
            detail="Interview question generation failed",
        ) from error


@app.post("/api/v1/interview/next")
def generate_next_interview_question(request: InterviewNextRequest):
    try:
        from fipilot.interview_engine import (
            evaluate_answer,
            generate_followup,
            generate_question,
        )
        from fipilot.persistence import save_interview_session, save_interview_turn

        llm = get_question_llm()
        decision = evaluate_answer(llm, request.current_question, request.answer)
        persist(
            save_interview_session,
            session_id=request.session_id,
            client_id=request.client_id,
            resume_id=request.resume_id,
            role=request.role,
            level=request.level,
            custom_description=request.custom_description,
            work_experience=request.work_experience,
        )
        persist(
            save_interview_turn,
            session_id=request.session_id,
            client_id=request.client_id,
            question=request.current_question,
            answer=request.answer,
            evaluation=decision,
        )
        should_follow_up = decision["should_follow_up"] and request.follow_up_count < 2

        if should_follow_up:
            project = request.current_project
            next_question = generate_followup(
                llm,
                project,
                request.role,
                request.level,
                get_domain_hits(project, request.role),
                request.current_question,
                request.answer,
                decision["next_direction"],
            )
            follow_up_count = request.follow_up_count + 1
        else:
            project = choose_project(request.work_experience, request.used_project_names)
            next_question = generate_question(
                llm,
                project,
                request.role,
                request.level,
                get_domain_hits(project, request.role),
            )
            follow_up_count = 0

        next_question["project"] = str(project.get("name", next_question["company"])).strip()
        next_question["project_context"] = project
        return {
            "decision": decision,
            "follow_up_count": follow_up_count,
            "question": next_question,
        }
    except Exception as error:
        logger.exception("Next interview question generation failed")
        raise HTTPException(
            status_code=502,
            detail="Next interview question generation failed",
        ) from error


@app.post("/api/v1/interview/report")
def generate_interview_report(request: InterviewReportRequest):
    try:
        from fipilot.interview_engine import generate_report
        from fipilot.persistence import save_interview_report

        report = generate_report(
            get_question_llm(),
            request.role,
            request.level,
            [turn.model_dump() for turn in request.turns],
        )
        persist(
            save_interview_report,
            session_id=request.session_id,
            client_id=request.client_id,
            content=report,
        )
        return report
    except Exception as error:
        logger.exception("Interview report generation failed")
        raise HTTPException(
            status_code=502,
            detail="Interview report generation failed",
        ) from error


@app.post("/api/v1/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    client_id: UUID | None = Form(default=None),
):
    started_at = time.perf_counter()
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File exceeds 10 MB limit")
    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400, detail="The uploaded file is not a valid PDF"
        )

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)

        extraction_started_at = time.perf_counter()
        result = get_extractor().pipeline(tmp_path)
        logger.info(
            "Resume extraction completed for %s in %.2f seconds",
            filename,
            time.perf_counter() - extraction_started_at,
        )
        payload = json.loads(result)
        resume_id = None
        try:
            from fipilot.persistence import save_resume

            resume_id = save_resume(client_id, filename, payload)
        except Exception:
            logger.exception("Database persistence failed during resume upload")
        return {"id": resume_id, "filename": filename, "profile": payload}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {e}")
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
        logger.info(
            "Resume upload request completed for %s in %.2f seconds",
            filename,
            time.perf_counter() - started_at,
        )


@app.get("/api/v1/resumes/latest")
def latest_resume(client_id: UUID):
    try:
        from fipilot.persistence import get_latest_resume

        resume = get_latest_resume(client_id)
    except Exception as error:
        logger.exception("Could not load the latest resume")
        raise HTTPException(status_code=503, detail="Database is unavailable") from error
    if resume is None:
        raise HTTPException(status_code=404, detail="No saved resume was found")
    return resume


@app.get("/api/v1/interview/{session_id}")
def interview_result(session_id: str, client_id: UUID):
    try:
        from fipilot.persistence import get_interview_result

        result = get_interview_result(session_id, client_id)
    except Exception as error:
        logger.exception("Could not load interview %s", session_id)
        raise HTTPException(status_code=503, detail="Database is unavailable") from error
    if result is None:
        raise HTTPException(status_code=404, detail="Interview was not found")
    return result


@app.get("/api/v1/interviews")
def interview_history(client_id: UUID):
    try:
        from fipilot.persistence import list_interview_sessions

        return {"interviews": list_interview_sessions(client_id)}
    except Exception as error:
        logger.exception("Could not load interview history")
        raise HTTPException(status_code=503, detail="Database is unavailable") from error

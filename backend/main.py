from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, Depends, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from database import engine, Base, get_db, SessionLocal
import crud
import models
from tts_service import tts_service
from ai_services import ai_services
from cv_parser import cv_extractor
from template_service import template_service
from rag_service import rag_service
from transcript_corrector import transcript_corrector
import json
import os
import re
import tempfile
import shutil
import zipfile
import unicodedata
import asyncio

import pypdf

MAX_CV_BYTES = 10 * 1024 * 1024
ALLOWED_CV_EXTENSIONS = {"pdf", "docx"}
MAX_CV_PAGES = 10
MIN_TEMPLATE_MATCH_SCORE = 0.5
MAX_WS_QUEUE_SIZE = 3
MAX_AUDIO_PAYLOAD_BYTES = 25 * 1024 * 1024
MAX_TEXT_ANSWER_CHARS = 12000

# Initialize database
def migrate_db():
    import sqlite3
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "interview_app.db"))
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(sessions)")
            columns = [info[1] for info in cursor.fetchall()]
            if "template_id" not in columns:
                print("Migrating database: adding template_id column to sessions table...")
                cursor.execute("ALTER TABLE sessions ADD COLUMN template_id VARCHAR")
                conn.commit()
            session_columns_to_add = {
                "current_question_id": "INTEGER DEFAULT 0",
                "follow_up_count": "INTEGER DEFAULT 0",
                "completed_question_ids": "TEXT DEFAULT '[]'",
                "state": "VARCHAR DEFAULT 'GREETING'",
                "question_plan_json": "TEXT",
                "proctoring_events_json": "TEXT DEFAULT '[]'",
            }
            for column_name, column_type in session_columns_to_add.items():
                if column_name not in columns:
                    print(f"Migrating database: adding {column_name} column to sessions table...")
                    cursor.execute(f"ALTER TABLE sessions ADD COLUMN {column_name} {column_type}")
                    conn.commit()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='evaluations'")
            if cursor.fetchone():
                cursor.execute("PRAGMA table_info(evaluations)")
                eval_columns = [info[1] for info in cursor.fetchall()]
                if "rubric_json" not in eval_columns:
                    print("Migrating database: adding rubric_json column to evaluations table...")
                    cursor.execute("ALTER TABLE evaluations ADD COLUMN rubric_json TEXT")
                    conn.commit()
            conn.close()
        except Exception as e:
            print(f"Migration error: {e}")

migrate_db()
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    if os.environ.get("LOCAL_STT_PRELOAD", "true").lower() in {"1", "true", "yes"} and getattr(ai_services, "stt_provider", "") == "local":
        async def preload_local_stt():
            try:
                await asyncio.to_thread(ai_services._get_local_whisper_model)
                print("Local STT model preloaded and kept in memory.")
            except Exception as preload_error:
                print(f"Local STT preload failed: {preload_error}")

        asyncio.create_task(preload_local_stt())
    if os.environ.get("LOCAL_TTS_PRELOAD", "true").lower() in {"1", "true", "yes"} and getattr(tts_service, "provider", "") == "local":
        async def preload_local_tts():
            try:
                await tts_service.preload()
                print("Local VieNeu-TTS preloaded and kept in memory.")
            except Exception as preload_error:
                print(f"Local VieNeu-TTS preload failed: {preload_error}")

        asyncio.create_task(preload_local_tts())
    yield
    print("Application shutdown")

app = FastAPI(title="AI Interview Chatbot", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from pydantic import BaseModel, Field

class SessionCreate(BaseModel):
    name: str
    role: str
    level: str
    language: str = "vi"
    template_id: str = None
    skills: list[str] = Field(default_factory=list)
    recent_role: str | None = None
    years_experience: float | None = None
    education: str | None = None

class TemplateMatchRequest(BaseModel):
    role_fit: str = "Software Engineer"
    inferred_level: int = 1
    skills: list[str] = Field(default_factory=list)
    target_role: str | None = None

class ProctoringEventCreate(BaseModel):
    event_type: str
    reason: str | None = None
    occurred_at: str | None = None
    visible: bool | None = None
    focus_state: str | None = None

def get_completed_ids(session):
    try:
        return set(json.loads(session.completed_question_ids or "[]"))
    except Exception:
        return set()

def set_completed_ids(session, completed_ids):
    session.completed_question_ids = json.dumps(sorted({int(item) for item in completed_ids}))

def get_proctoring_events(session):
    try:
        events = json.loads(session.proctoring_events_json or "[]")
        return events if isinstance(events, list) else []
    except Exception:
        return []

def get_proctoring_summary(session):
    events = get_proctoring_events(session)
    tab_switch_count = sum(1 for event in events if event.get("event_type") == "tab_hidden")
    window_blur_count = sum(1 for event in events if event.get("event_type") == "window_blur")
    return {
        "tab_switch_count": tab_switch_count,
        "window_blur_count": window_blur_count,
        "total_events": len(events),
        "events": events[-100:],
    }

def ensure_valid_template(template_id: str):
    if not template_id:
        raise HTTPException(status_code=400, detail="Vui lòng chọn bộ câu hỏi phỏng vấn trước khi bắt đầu.")
    questions = template_service.get_template_questions(template_id)
    if len(questions) < 3:
        raise HTTPException(status_code=400, detail="Template đã chọn không hợp lệ hoặc có quá ít câu hỏi.")
    missing_answers = [q["id"] for q in questions if not q.get("answer")]
    if missing_answers:
        raise HTTPException(
            status_code=400,
            detail=f"Template đang thiếu đáp án mẫu ở các câu: {missing_answers[:5]}",
        )
    return questions

def get_session_questions(session):
    if session and session.question_plan_json:
        try:
            questions = json.loads(session.question_plan_json)
            if isinstance(questions, list) and len(questions) >= 3:
                return questions
        except Exception as e:
            print(f"Invalid question_plan_json for session {getattr(session, 'id', None)}: {e}")
    return template_service.get_template_questions(session.template_id) if session and session.template_id else []

def build_interview_speech_context(db: Session, session):
    try:
        template_questions = get_session_questions(session)
        history = crud.get_session_messages(db, session.id, limit=80)
        return rag_service.build_session_context(session, template_questions=template_questions, history=history)
    except Exception as error:
        print(f"Could not build interview speech context: {error}")
        return {"glossary": [], "retrieved_context": ""}

async def transcribe_interview_audio(audio_bytes: bytes, session, db: Session):
    speech_context = build_interview_speech_context(db, session)
    raw_text = await ai_services.stt(
        audio_bytes,
        session.language,
        glossary=speech_context.get("glossary", []),
    )
    corrected_text = await transcript_corrector.correct(
        raw_text,
        role=session.role,
        level=session.level,
        glossary=speech_context.get("glossary", []),
        retrieved_context=speech_context.get("retrieved_context", ""),
        llm_chat=ai_services._core_llm_chat,
    )
    if corrected_text != raw_text:
        print(f"Transcript corrected: {raw_text} -> {corrected_text}")
    return corrected_text, raw_text

async def prepare_adaptive_question_plan_background(
    session_id: int,
    profile_context: dict,
    template_questions: list,
    role: str,
    level: str,
):
    try:
        question_plan = await ai_services.generate_adaptive_question_plan(
            profile=profile_context,
            template_questions=template_questions,
            role=role,
            level=level,
        )
        if not question_plan:
            return

        db = SessionLocal()
        try:
            session = db.query(models.Session).filter(models.Session.id == session_id).first()
            if not session or session.current_question_id > 0 or session.status != "CHITCHAT":
                return
            session.question_plan_json = json.dumps(question_plan, ensure_ascii=False)
            db.commit()
            print(f"Adaptive question plan prepared for session {session_id}")
        finally:
            db.close()
    except Exception as e:
        print(f"Adaptive question plan background failed for session {session_id}: {e}")

def is_likely_english_resume(text: str):
    if not text or len(text.strip()) < 300:
        return False
    sample = text[:5000]
    letters = [char for char in sample if char.isalpha()]
    if not letters:
        return False
    ascii_letters = [char for char in letters if ord(char) < 128]
    ascii_ratio = len(ascii_letters) / max(len(letters), 1)
    vietnamese_markers = set("ăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ")
    marker_count = sum(1 for char in sample.lower() if char in vietnamese_markers)
    return ascii_ratio >= 0.92 and marker_count < 8

def validate_cv_upload(file: UploadFile):
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_CV_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ CV tiếng Anh dạng PDF hoặc DOCX.")
    size = getattr(file, "size", None)
    if size and size > MAX_CV_BYTES:
        raise HTTPException(status_code=413, detail="CV quá lớn. Vui lòng upload file dưới 10MB.")

def detect_cv_file_type(file_path: str):
    try:
        with open(file_path, "rb") as file:
            header = file.read(8)
        if header.startswith(b"%PDF-"):
            return "pdf"
        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path) as archive:
                names = set(archive.namelist())
            if "word/document.xml" in names:
                return "docx"
    except Exception:
        return None
    return None

def validate_cv_file_content(file_path: str, expected_ext: str):
    actual_ext = detect_cv_file_type(file_path)
    if actual_ext != expected_ext:
        raise HTTPException(
            status_code=400,
            detail="Nội dung file không khớp với phần mở rộng. Vui lòng upload CV tiếng Anh PDF hoặc DOCX thật.",
        )

    if actual_ext == "pdf":
        try:
            with open(file_path, "rb") as file:
                reader = pypdf.PdfReader(file, strict=False)
                if reader.is_encrypted:
                    raise HTTPException(status_code=422, detail="Không hỗ trợ PDF có mã hóa hoặc đặt mật khẩu.")
                page_count = len(reader.pages)
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=422, detail="File PDF không hợp lệ hoặc đã bị lỗi.")

        if page_count == 0:
            raise HTTPException(status_code=422, detail="PDF không có trang nào.")
        if page_count > MAX_CV_PAGES:
            raise HTTPException(status_code=422, detail=f"CV PDF không nên vượt quá {MAX_CV_PAGES} trang.")

def cv_error(code: str, message: str, status_code: int = 422):
    raise HTTPException(status_code=status_code, detail={"code": code, "message": message})

def cv_profile_quality(profile: dict):
    skills = profile.get("skills") if isinstance(profile.get("skills"), list) else []
    skill_count = len([skill for skill in skills if str(skill).strip() and str(skill).lower() != "not found"])
    score = 0
    if profile.get("candidate_name") and profile.get("candidate_name") != "Candidate":
        score += 2
    if profile.get("role_fit"):
        score += 2
    if profile.get("recent_role") and profile.get("recent_role") != "Not Found":
        score += 1
    if profile.get("education") and profile.get("education") != "Not Found":
        score += 1
    score += min(skill_count, 10)
    return score

def choose_best_cv_profile(workflow_profile: dict, llm_profile: dict | None):
    if not llm_profile:
        return workflow_profile, "workflow"
    workflow_score = cv_profile_quality(workflow_profile)
    llm_score = cv_profile_quality(llm_profile)
    if workflow_score >= llm_score + 3:
        merged = {**llm_profile, **workflow_profile}
        merged["confidence"] = max(float(workflow_profile.get("confidence", 0) or 0), float(llm_profile.get("confidence", 0) or 0))
        merged["extraction_method"] = "hybrid:workflow_preferred"
        return merged, "hybrid"
    if llm_score >= workflow_score:
        merged = {**workflow_profile, **llm_profile}
        merged["extraction_method"] = llm_profile.get("extraction_method", "llm")
        return merged, "llm"
    merged = {**llm_profile, **workflow_profile}
    merged["extraction_method"] = "hybrid:workflow"
    return merged, "hybrid"

def is_likely_resume_text(text: str):
    normalized = (text or "").lower()
    lines = [line.strip() for line in normalized.splitlines() if line.strip()]
    words = re.findall(r"[a-z][a-z0-9+#.\-]{1,}", normalized)
    if len(words) < 80:
        return False

    section_patterns = [
        r"\bsummary\b",
        r"\bprofile\b",
        r"\bobjective\b",
        r"\bskills?\b",
        r"\btechnical skills?\b",
        r"\bexperience\b",
        r"\bwork experience\b",
        r"\bemployment\b",
        r"\bprojects?\b",
        r"\beducation\b",
        r"\bcertifications?\b",
    ]
    section_hits = sum(1 for pattern in section_patterns if re.search(pattern, normalized))
    contact_hits = bool(re.search(r"[\w.+-]+@[\w.-]+\.[a-z]{2,}", normalized, re.I))
    contact_hits = contact_hits or bool(re.search(r"\+?\d[\d\s().-]{8,}", normalized))
    contact_hits = contact_hits or any(token in normalized for token in ["linkedin", "github", "portfolio"])

    role_terms = [
        "engineer",
        "developer",
        "analyst",
        "tester",
        "qa",
        "devops",
        "scientist",
        "architect",
        "administrator",
        "manager",
        "intern",
    ]
    skill_terms = [
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "node",
        "sql",
        "api",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "git",
        "testing",
        "machine learning",
        "data",
        "backend",
        "frontend",
    ]
    role_hits = sum(1 for term in role_terms if re.search(rf"\b{re.escape(term)}\b", normalized))
    skill_hits = sum(1 for term in skill_terms if re.search(rf"\b{re.escape(term)}\b", normalized))
    date_hits = len(re.findall(r"\b(?:19|20)\d{2}\b|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b", normalized))

    signal_score = section_hits + min(role_hits, 2) + min(skill_hits, 4) + min(date_hits, 2)
    if contact_hits:
        signal_score += 2
    if len(lines) >= 8:
        signal_score += 1

    return section_hits >= 2 and signal_score >= 7 and (contact_hits or role_hits > 0 or skill_hits >= 3)

@app.post("/api/sessions")
async def create_new_session(
    session_data: SessionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    template_questions = ensure_valid_template(session_data.template_id)
    profile_context = {
        "candidate_name": session_data.name,
        "role_fit": session_data.role,
        "recent_role": session_data.recent_role,
        "years_experience": session_data.years_experience,
        "skills": session_data.skills or [],
        "education": session_data.education,
    }
    question_plan = ai_services.generate_contextual_question_plan(
        profile=profile_context,
        template_questions=template_questions,
        role=session_data.role,
    ) or template_questions

    new_session = models.Session(
        candidate_name=session_data.name,
        role=session_data.role, 
        level=session_data.level, 
        language="vi",
        status="CHITCHAT",
        template_id=session_data.template_id,
        current_question_id=0,
        follow_up_count=0,
        completed_question_ids="[]",
        state="GREETING",
        question_plan_json=json.dumps(question_plan, ensure_ascii=False),
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    background_tasks.add_task(
        prepare_adaptive_question_plan_background,
        new_session.id,
        profile_context,
        template_questions,
        session_data.role,
        session_data.level,
    )
    return {"session_id": new_session.id}

@app.get("/api/sessions/{session_id}")
async def get_session_detail(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = crud.get_session_messages(db, session_id, limit=500)
    return {
        "id": session.id,
        "candidate_name": session.candidate_name,
        "role": session.role,
        "level": session.level,
        "language": session.language,
        "status": session.status,
        "state": session.state,
        "template_id": session.template_id,
        "has_question_plan": bool(session.question_plan_json),
        "current_question_id": session.current_question_id,
        "follow_up_count": session.follow_up_count,
        "completed_question_ids": sorted(get_completed_ids(session)),
        "question_count": session.question_count,
        "proctoring": get_proctoring_summary(session),
        "created_at": session.created_at.isoformat() if session.created_at else None,
        "messages": [
            {
                "id": msg.id,
                "sender": "AI" if msg.role == "ai" else (session.candidate_name.split(" ")[0] if session.candidate_name else "You"),
                "role": msg.role,
                "text": msg.content,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in messages
        ],
    }

@app.post("/api/sessions/{session_id}/end")
async def end_session(session_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        return {"status": "failed", "message": "Session not found"}

    session.status = "ENDED"
    session.state = "ENDING"
    db.commit()
    schedule_report_generation(background_tasks, session_id)
    return {"status": "success", "message": "Interview ended. Report is being generated."}

@app.get("/api/sessions/{session_id}/report")
async def get_session_report(session_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.report_data:
        report = json.loads(session.report_data)
        report["proctoring"] = get_proctoring_summary(session)
        return {"status": "success", "report": report}
    if session.status == "ENDED":
        schedule_report_generation(background_tasks, session_id)
    return {
        "status": "processing" if session.status == "ENDED" else "not_ready",
        "message": "Report is being generated or the interview is not completed yet.",
    }

@app.get("/api/sessions")
async def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(models.Session).order_by(models.Session.created_at.desc()).all()
    result = []
    for s in sessions:
        report = {}
        if s.report_data:
            report = json.loads(s.report_data)
        
        result.append({
            "id": s.id,
            "candidate_name": s.candidate_name,
            "role": s.role,
            "level": s.level,
            "status": s.status.lower(),
            "started_at": s.created_at.isoformat(),
            "overall_score": report.get("overall_score", 0) if report else 0,
            "interviewer_email": "admin2026@gmail.com"
        })
    return result

@app.post("/api/sessions/{session_id}/proctoring-events")
async def record_proctoring_event(session_id: int, event: ProctoringEventCreate, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status == "ENDED":
        return {"status": "ignored", "proctoring": get_proctoring_summary(session)}

    allowed_events = {"tab_hidden", "window_blur"}
    event_type = event.event_type if event.event_type in allowed_events else "window_blur"
    events = get_proctoring_events(session)
    events.append({
        "event_type": event_type,
        "reason": (event.reason or "").strip()[:160],
        "occurred_at": event.occurred_at,
        "visible": event.visible,
        "focus_state": event.focus_state,
    })
    session.proctoring_events_json = json.dumps(events[-250:], ensure_ascii=False)
    db.commit()
    db.refresh(session)
    return {"status": "success", "proctoring": get_proctoring_summary(session)}

@app.get("/api/templates")
async def get_templates():
    return {"status": "success", "templates": template_service.get_all_templates()}

@app.post("/api/templates/match")
async def match_templates(request: TemplateMatchRequest):
    matches = template_service.match_templates(
        role_fit=request.role_fit,
        inferred_level=request.inferred_level,
        skills=request.skills,
        target_role=request.target_role or request.role_fit,
    )
    return {"status": "success", "matches": matches}

@app.get("/api/templates/{template_id}/validate")
async def validate_template(template_id: str):
    questions = template_service.get_template_questions(template_id)
    issues = []
    if len(questions) < 3:
        issues.append("Template must contain at least 3 parsed questions.")
    for question in questions:
        if not question.get("question"):
            issues.append(f"Question {question.get('id')} is missing question text.")
        if not question.get("answer"):
            issues.append(f"Question {question.get('id')} is missing sample answer.")
        if not question.get("difficulty"):
            issues.append(f"Question {question.get('id')} is missing difficulty.")
    return {
        "status": "success" if not issues else "failed",
        "valid": not issues,
        "question_count": len(questions),
        "issues": issues,
    }

@app.post("/api/cv/extract")
async def extract_cv(file: UploadFile = File(...), parser_mode: str = Form("workflow")):
    validate_cv_upload(file)
    ext = file.filename.split('.')[-1].lower() if '.' in file.filename else 'pdf'
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
        
    try:
        if os.path.getsize(tmp_path) > MAX_CV_BYTES:
            raise HTTPException(status_code=413, detail="CV quá lớn. Vui lòng upload file dưới 10MB.")

        validate_cv_file_content(tmp_path, ext)
        text = cv_extractor.extract_text(tmp_path, file.filename)
        if not text or len(text.strip()) < 300:
            raise HTTPException(
                status_code=422,
                detail="Không đọc được nội dung CV. Vui lòng upload CV tiếng Anh dạng PDF/DOCX có text thật.",
            )
        if not is_likely_resume_text(text):
            raise HTTPException(
                status_code=422,
                detail="File upload không giống CV. Vui lòng upload CV tiếng Anh có thông tin liên hệ, kỹ năng, học vấn, kinh nghiệm hoặc dự án.",
            )
        if not is_likely_english_resume(text):
            raise HTTPException(
                status_code=422,
                detail="Hiện chỉ hỗ trợ detect CV tiếng Anh. Vui lòng upload resume tiếng Anh.",
            )

        normalized_mode = (parser_mode or "workflow").lower()
        if normalized_mode not in {"workflow", "llm"}:
            raise HTTPException(status_code=400, detail="parser_mode must be workflow or llm.")

        llm_warning = None
        workflow_profile = await cv_extractor.parse_cv(text)
        selected_parser = "workflow"
        if normalized_mode == "llm":
            try:
                llm_profile = await cv_extractor.parse_cv_with_llm(text)
                profile, selected_parser = choose_best_cv_profile(workflow_profile, llm_profile)
            except Exception as e:
                print(f"LLM CV extraction failed, falling back to workflow: {e}")
                profile = workflow_profile
                llm_warning = "LLM Gemma khong phan tich duoc CV, he thong da fallback sang workflow nhanh."
        else:
            profile = workflow_profile
        
        role_fit = profile.get("role_fit", "Software Engineer")
        inferred_level = profile.get("inferred_level", 1)
        matches = template_service.match_templates(
            role_fit=role_fit,
            inferred_level=inferred_level,
            skills=profile.get("skills", []),
            target_role=profile.get("recent_role"),
        )
        
        if normalized_mode == "workflow":
            profile["confidence"] = 0.92
        if matches and matches[0]["score"] < MIN_TEMPLATE_MATCH_SCORE:
            profile["template_warning"] = "No strong template match was found. Please choose a template manually."
        if llm_warning:
            profile["parser_warning"] = llm_warning
        
        return {
            "status": "success",
            "profile": profile,
            "matches": matches,
            "parser_mode": normalized_mode,
            "selected_parser": selected_parser,
        }
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def clean_words(text: str):
    import re
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)

KEYWORD_HINT_ALIASES = {
    "hoc co giam sat": "Học có giám sát",
    "hoc khong giam sat": "Học không giám sát",
    "hoc ban giam sat": "Học bán giám sát",
    "hoc tang cuong": "Học tăng cường",
    "du lieu gan nhan": "Dữ liệu gán nhãn",
    "du lieu khong gan nhan": "Dữ liệu không gán nhãn",
    "nhan du lieu": "Nhãn dữ liệu",
    "phan loai": "Phân loại",
    "hoi quy": "Hồi quy",
    "phan cum": "Phân cụm",
    "giam chieu du lieu": "Giảm chiều dữ liệu",
    "mo hinh": "Mô hình",
    "huan luyen": "Huấn luyện",
    "tap huan luyen": "Tập huấn luyện",
    "tap kiem tra": "Tập kiểm tra",
    "tap xac thuc": "Tập xác thực",
    "danh gia mo hinh": "Đánh giá mô hình",
    "do chinh xac": "Độ chính xác",
    "do phu hop": "Độ phù hợp",
    "qua khop": "Quá khớp",
    "thieu khop": "Thiếu khớp",
    "ham mat mat": "Hàm mất mát",
    "toi uu hoa": "Tối ưu hóa",
    "gradient descent": "Gradient descent",
    "cay quyet dinh": "Cây quyết định",
    "rung ngau nhien": "Rừng ngẫu nhiên",
    "mang no ron": "Mạng nơ-ron",
    "mang neural": "Mạng nơ-ron",
    "logic mo": "Logic mờ",
    "he chuyen gia": "Hệ chuyên gia",
    "tra cuu co so du lieu": "Tra cứu cơ sở dữ liệu",
    "co so du lieu": "Cơ sở dữ liệu",
    "tien xu ly du lieu": "Tiền xử lý dữ liệu",
    "trich chon dac trung": "Trích chọn đặc trưng",
    "dac trung": "Đặc trưng",
}

def normalize_keyword_key(text: str):
    normalized = unicodedata.normalize("NFD", (text or "").strip().lower())
    normalized = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    normalized = normalized.replace("đ", "d")
    normalized = re.sub(r"[^a-z0-9+#.\-\s]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()

def canonicalize_keyword_hint(keyword: str):
    normalized = normalize_keyword_key(keyword)
    return KEYWORD_HINT_ALIASES.get(normalized, (keyword or "").strip())

def normalize_keyword_hints(keywords, limit: int = 8):
    seen = set()
    normalized_keywords = []
    for keyword in keywords or []:
        canonical = canonicalize_keyword_hint(str(keyword))
        key = normalize_keyword_key(canonical)
        if not canonical or not key or key in seen:
            continue
        seen.add(key)
        normalized_keywords.append(canonical)
        if len(normalized_keywords) >= limit:
            break
    return normalized_keywords

def extract_keyword_hints(text: str, limit: int = 8):
    import re
    stop_words = {
        "the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
        "you", "your", "can", "will", "have", "has", "had", "cua", "va", "la",
        "mot", "cac", "cho", "khi", "trong", "bang", "duoc", "khong", "nhung",
    }
    normalized_text = normalize_keyword_key(text)
    seen = []
    for alias, canonical in KEYWORD_HINT_ALIASES.items():
        if alias in normalized_text and canonical not in seen:
            seen.append(canonical)
            if len(seen) >= limit:
                return seen

    words = re.findall(r"[A-Za-zÀ-ỹ][A-Za-zÀ-ỹ0-9+#.\-]{2,}", text or "")
    for word in words:
        normalized = word.strip(".,:;()[]{}").lower()
        normalized_key = normalize_keyword_key(normalized)
        if normalized_key in stop_words or len(normalized_key) < 3:
            continue
        keyword = canonicalize_keyword_hint(normalized)
        if normalize_keyword_key(keyword) not in {normalize_keyword_key(item) for item in seen}:
            seen.append(keyword)
    return seen[:limit]

def match_question(ai_text: str, template_questions: list):
    ai_text_lower = ai_text.lower()
    for q in template_questions:
        if f"câu {q['id']}" in ai_text_lower:
            return q
        if f"cau {q['id']}" in ai_text_lower:
            return q
        q_words = clean_words(q["question"])
        ai_words = clean_words(ai_text)
        if q_words:
            overlap = len(q_words & ai_words) / len(q_words)
            if overlap > 0.4:
                return q
    return None

def get_segments(history, template_questions):
    segments = []
    current_segment = None
    last_ai_message = None
    
    for msg in history:
        if msg.role == "ai":
            matched_q = match_question(msg.content, template_questions)
            if matched_q:
                if current_segment:
                    segments.append(current_segment)
                current_segment = {
                    "question_id": matched_q["id"],
                    "topic": matched_q.get("topic", ""),
                    "difficulty": matched_q.get("difficulty", ""),
                    "template_question": matched_q["question"],
                    "sample_answer": matched_q.get("expected_answer") or matched_q.get("answer", ""),
                    "expected_answer": matched_q.get("expected_answer") or matched_q.get("answer", ""),
                    "score_rule": matched_q.get("score_rule", {}),
                    "source_context": matched_q.get("source_context", {}),
                    "expected_keywords": (
                        matched_q.get("score_rule", {}).get("expected_keywords")
                        if isinstance(matched_q.get("score_rule"), dict)
                        else None
                    ) or extract_keyword_hints(matched_q.get("expected_answer") or matched_q.get("answer", "")),
                    "initial_answer": "",
                    "follow_ups": []
                }
                last_ai_message = {"type": "standard", "content": msg.content}
            else:
                if current_segment:
                    last_ai_message = {"type": "follow_up", "content": msg.content}
        elif msg.role == "user":
            if current_segment:
                if last_ai_message and last_ai_message["type"] == "standard":
                    current_segment["initial_answer"] = msg.content
                elif last_ai_message and last_ai_message["type"] == "follow_up":
                    current_segment["follow_ups"].append({
                        "question": last_ai_message["content"],
                        "answer": msg.content
                    })
    if current_segment:
        segments.append(current_segment)
    return segments

def build_current_segment_from_latest_answer(history, current_question: dict):
    if not history or not current_question:
        return None
    last_user = next((msg for msg in reversed(history) if msg.role == "user" and (msg.content or "").strip()), None)
    if not last_user:
        return None
    last_ai = next((msg for msg in reversed(history) if msg.role == "ai" and (msg.content or "").strip()), None)
    if last_ai and getattr(last_ai, "id", 0) > getattr(last_user, "id", 0):
        return None
    return {
        "question_id": current_question["id"],
        "topic": current_question.get("topic", ""),
        "difficulty": current_question.get("difficulty", ""),
        "template_question": current_question.get("question", ""),
        "sample_answer": current_question.get("expected_answer") or current_question.get("answer", ""),
        "expected_answer": current_question.get("expected_answer") or current_question.get("answer", ""),
        "score_rule": current_question.get("score_rule", {}),
        "source_context": current_question.get("source_context", {}),
        "expected_keywords": (
            current_question.get("score_rule", {}).get("expected_keywords")
            if isinstance(current_question.get("score_rule"), dict)
            else None
        ) or extract_keyword_hints(current_question.get("expected_answer") or current_question.get("answer", "")),
        "initial_answer": last_user.content,
        "follow_ups": [],
    }

def normalize_difficulty(value: str):
    text = (value or "").lower()
    if "hard" in text or "kh" in text:
        return "hard"
    if "medium" in text or "trung" in text:
        return "medium"
    return "easy"

def is_non_answer(text: str):
    normalized = (text or "").lower()
    skip_phrases = [
        "khong biet",
        "không biết",
        "bo qua",
        "bỏ qua",
        "chiu",
        "chịu",
        "di tiep",
        "đi tiếp",
        "sang cau",
        "sang câu",
    ]
    return any(phrase in normalized for phrase in skip_phrases)

def is_unclear_transcript(text: str):
    normalized = (text or "").strip().lower()
    if not normalized:
        return True
    unclear_phrases = [
        "xin lỗi, tôi không nghe rõ",
        "xin loi, toi khong nghe ro",
        "không nghe rõ",
        "khong nghe ro",
        "i could not hear",
        "could not understand",
    ]
    return any(phrase in normalized for phrase in unclear_phrases)

def is_low_information_answer(text: str):
    normalized = (text or "").strip().lower()
    if not normalized:
        return True
    normalized_plain = re.sub(r"[^a-z0-9A-ZÀ-ỹ\s]+", " ", normalized)
    words = [word for word in normalized_plain.split() if word.strip()]
    if len(words) <= 2:
        return True
    low_signal_phrases = [
        "khong biet",
        "khong tra loi",
        "khong nghe ro",
        "bo qua",
        "chiu",
        "im lang",
        "no answer",
        "skip",
        "silence",
        "i do not know",
        "i don't know",
    ]
    return any(phrase in normalized for phrase in low_signal_phrases)

def normalize_answer_signal(text: str):
    normalized = (text or "").strip().lower()
    normalized = unicodedata.normalize("NFD", normalized)
    normalized = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    normalized = normalized.replace("đ", "d")
    normalized = re.sub(r"[^a-z0-9\s]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()

def is_non_answer(text: str):
    normalized = normalize_answer_signal(text)
    skip_phrases = [
        "khong biet",
        "khong tra loi",
        "bo qua",
        "chiu",
        "di tiep",
        "sang cau",
        "sang cau khac",
        "bat dau",
        "bat dau di",
        "tiep tuc",
        "skip",
        "next question",
    ]
    return any(phrase in normalized for phrase in skip_phrases)

def is_unclear_transcript(text: str):
    normalized = normalize_answer_signal(text)
    if not normalized:
        return True
    unclear_phrases = [
        "xin loi toi khong nghe ro",
        "khong nghe ro",
        "minh chua nghe ro",
        "toi chua nghe ro",
        "khong ro",
        "khong noi gi",
        "chua noi gi",
        "im lang",
        "no speech",
        "no answer",
        "silence",
        "i could not hear",
        "could not understand",
    ]
    return any(phrase in normalized for phrase in unclear_phrases)

def is_low_information_answer(text: str):
    normalized = normalize_answer_signal(text)
    if not normalized:
        return True
    words = [word for word in normalized.split() if word.strip()]
    filler_words = {"a", "ah", "uh", "um", "uhm", "ok", "okay", "vang", "da", "co", "khong", "roi"}
    meaningful_words = [word for word in words if word not in filler_words]
    if len(meaningful_words) <= 2:
        return True
    low_signal_phrases = [
        "khong biet",
        "khong tra loi",
        "khong nghe ro",
        "khong noi gi",
        "chua noi gi",
        "bo qua",
        "chiu",
        "im lang",
        "bat dau",
        "bat dau di",
        "no answer",
        "skip",
        "silence",
        "i do not know",
        "i dont know",
    ]
    return any(phrase in normalized for phrase in low_signal_phrases)

def is_meaningful_answer(text: str):
    return not is_unclear_transcript(text) and not is_non_answer(text) and not is_low_information_answer(text)

def should_retry_answer(text: str):
    if is_unclear_transcript(text):
        return True
    if is_non_answer(text):
        return False
    return is_low_information_answer(text)

def classify_chitchat_reply(text: str):
    normalized = normalize_answer_signal(text)
    if not normalized:
        return "unclear"

    refusal_phrases = [
        "toi khong quan tam",
        "khong quan tam",
        "khong muon",
        "toi khong muon",
        "khong phong van",
        "khong can",
        "huy",
        "thoat",
        "dung lai",
        "stop",
        "cancel",
    ]
    if any(phrase in normalized for phrase in refusal_phrases):
        return "refusal"

    not_ready_phrases = [
        "chua san sang",
        "doi chut",
        "cho chut",
        "de sau",
        "lat nua",
        "tam dung",
    ]
    if any(phrase in normalized for phrase in not_ready_phrases):
        return "not_ready"

    start_phrases = [
        "bat dau",
        "san sang",
        "ready",
        "ok",
        "duoc",
        "tiep tuc",
        "vao phong van",
    ]
    if any(phrase in normalized for phrase in start_phrases):
        return "start"

    words = normalized.split()
    intro_signals = [
        "toi la",
        "minh la",
        "em la",
        "kinh nghiem",
        "du an",
        "project",
        "developer",
        "engineer",
        "python",
        "javascript",
        "ai",
        "machine learning",
    ]
    if len(words) >= 6 or any(signal in normalized for signal in intro_signals):
        return "start"
    return "unclear"

def render_chitchat_intent_response(intent: str, name: str, role: str):
    candidate_name = (name or "bạn").strip()
    role_text = (role or "vị trí này").strip()
    if intent == "refusal":
        return (
            f"Mình hiểu, {candidate_name}. Nếu bạn chưa quan tâm đến buổi luyện phỏng vấn cho vị trí {role_text} "
            "thì mình sẽ chưa bắt đầu phần kỹ thuật. Khi nào bạn muốn luyện tiếp, hãy nhắn rằng bạn đã sẵn sàng."
        )
    if intent == "not_ready":
        return (
            f"Không sao, {candidate_name}. Mình sẽ chờ. Khi bạn sẵn sàng, hãy nhắn hoặc nói ngắn gọn "
            "\"bắt đầu\" để mình vào phần phỏng vấn."
        )
    return (
        "Mình chưa rõ bạn muốn bắt đầu phỏng vấn hay muốn trao đổi thêm. "
        "Bạn có thể giới thiệu ngắn về bản thân, hoặc nói \"bắt đầu\" khi đã sẵn sàng."
    )

def should_ask_follow_up(segment: dict, max_follow_ups: int = 1):
    answer = (segment.get("initial_answer") or "").strip()
    if not answer or is_non_answer(answer):
        return False
    if len(segment.get("follow_ups", [])) >= max_follow_ups:
        return False
    word_count = len(answer.split())
    return word_count < 35

def should_ask_follow_up_from_evaluation(eval_result: dict, session) -> bool:
    if session.follow_up_count >= 1:
        return False
    score = int(eval_result.get("score", 0) or 0)
    correctness = eval_result.get("correctness") or ("Wrong" if score <= 3 else "Partial")
    if correctness == "Wrong" or score <= 3:
        return False
    if correctness == "Partial":
        return True
    rubric = eval_result.get("rubric", {}) if isinstance(eval_result.get("rubric"), dict) else {}
    depth = int(rubric.get("depth", score) or score)
    relevance = int(rubric.get("relevance", score) or score)
    return score < 8 or depth < 7 or relevance < 7

def has_three_consecutive_wrong(db: Session, session_id: int):
    evals = db.query(models.Evaluation).filter(
        models.Evaluation.session_id == session_id
    ).order_by(models.Evaluation.id.desc()).limit(3).all()
    return len(evals) == 3 and all(e.correctness == "Wrong" for e in evals)

def render_template_question(question: dict, name: str, total_questions: int):
    question_text = (question.get("question") or "").strip()
    question_id = int(question.get("id") or 1)
    difficulty = normalize_difficulty(question.get("difficulty", ""))
    candidate_name = (name or "").strip()
    name_phrase = f" {candidate_name}" if candidate_name else ""
    if question_id <= 1 and question.get("source") in {"adaptive", "contextual_fallback"}:
        return f"Cảm ơn{name_phrase}. Mình bắt đầu bằng một câu theo kinh nghiệm và kỹ năng của bạn nhé: {question_text}"

    if question_id <= 1:
        return f"Cảm ơn{name_phrase}. Mình bắt đầu bằng một câu nền tảng nhé: {question_text}"
    if difficulty == "hard":
        return f"Bây giờ mình muốn đưa bạn vào một tình huống khó hơn một chút: {question_text}"
    if difficulty == "medium":
        return f"Mình muốn đi sâu hơn một chút ở phần này: {question_text}"
    return f"Mình hỏi tiếp một ý nền tảng khác nhé: {question_text}"

def render_next_question_with_feedback(eval_payload: dict, question: dict, total_questions: int):
    score = int(eval_payload.get("score", 0) or 0)
    correctness = eval_payload.get("correctness") or ("Wrong" if score <= 3 else "Partial")
    next_question = render_template_question(question, "", total_questions)

    if correctness == "Wrong" or score <= 3:
        return (
            "Mình hiểu ý bạn. Phần này mình sẽ ghi nhận lại để góp ý kỹ hơn sau buổi phỏng vấn. "
            "Giờ mình chuyển sang một ý khác nhé.\n\n"
            f"{next_question}"
        )
    if correctness == "Partial" or score < 8:
        return (
            "Cảm ơn bạn, mình đã ghi nhận phần trả lời này. "
            "Mình muốn nối tiếp bằng một chủ đề liên quan nhé.\n\n"
            f"{next_question}"
        )
    return next_question

def render_non_answer_transition(question: dict, total_questions: int):
    next_question = render_template_question(question, "", total_questions)
    return (
        "Mình ghi nhận là bạn chưa biết phần này, nên mình sẽ chuyển sang câu tiếp theo. "
        "Sau buổi phỏng vấn mình sẽ gợi ý keyword để bạn ôn lại nhé.\n\n"
        f"{next_question}"
    )

def render_interview_greeting(session):
    candidate_name = session.candidate_name or "bạn"
    role = session.role or "vị trí này"
    return (
        f"Chào {candidate_name}, tôi là Alex, interviewer AI của buổi phỏng vấn hôm nay. "
        f"Bạn đang luyện phỏng vấn cho vị trí {role}. "
        "Buổi phỏng vấn sẽ đi theo bộ câu hỏi đã chọn, có thể có một câu hỏi phụ ngắn nếu câu trả lời cần làm rõ. "
        "Trước khi vào phần kỹ thuật, bạn hãy giới thiệu ngắn gọn về bản thân và lý do bạn quan tâm đến vị trí này nhé."
    )

async def next_interview_turn(db: Session, session, history, template_questions):
    total_questions = len(template_questions)

    if total_questions == 0:
        return {
            "text": None,
            "status": session.status,
            "completed_segment": None,
            "ended": False,
        }

    completed_ids = get_completed_ids(session)

    if session.current_question_id <= 0:
        first_question = template_questions[0]
        session.current_question_id = first_question["id"]
        session.follow_up_count = 0
        session.state = "ASKING"
        return {
            "text": render_template_question(first_question, session.candidate_name, total_questions),
            "status": "INTERVIEWING",
            "completed_segment": None,
            "ended": False,
        }

    segments = get_segments(history, template_questions)
    current_segment = next(
        (segment for segment in reversed(segments) if int(segment["question_id"]) == int(session.current_question_id)),
        None,
    )
    current_question = template_questions[session.current_question_id - 1]

    if not current_segment or not current_segment.get("initial_answer"):
        current_segment = build_current_segment_from_latest_answer(history, current_question)
        if not current_segment or not current_segment.get("initial_answer"):
            return {
                "text": render_template_question(current_question, session.candidate_name, total_questions),
                "status": "INTERVIEWING",
                "completed_segment": None,
                "ended": False,
            }

    completed_segment = current_segment

    if is_non_answer(completed_segment.get("initial_answer", "")):
        await ensure_segment_evaluated(db, session.id, completed_segment, session.level, session.role)
        completed_ids.add(int(session.current_question_id))
        set_completed_ids(session, completed_ids)
        session.follow_up_count = 0

        if has_three_consecutive_wrong(db, session.id):
            session.state = "EARLY_STOPPED"
            return {
                "text": "Buổi phỏng vấn tạm dừng tại đây vì bạn đang gặp khó khăn với nhiều câu liên tiếp. AI sẽ tổng hợp báo cáo và gợi ý keyword để bạn ôn tập.",
                "status": "ENDED",
                "completed_segment": completed_segment,
                "ended": True,
            }

        if int(session.current_question_id) >= total_questions:
            session.state = "COMPLETED"
            return {
                "text": "Cảm ơn bạn. Buổi phỏng vấn đã hoàn tất, AI đang tổng hợp báo cáo đánh giá cho bạn.",
                "status": "ENDED",
                "completed_segment": completed_segment,
                "ended": True,
            }

        next_question = template_questions[int(session.current_question_id)]
        session.current_question_id = next_question["id"]
        session.state = "ASKING"
        return {
            "text": render_non_answer_transition(next_question, total_questions),
            "status": "INTERVIEWING",
            "completed_segment": completed_segment,
            "ended": False,
        }

    eval_record = await ensure_segment_evaluated(db, session.id, completed_segment, session.level, session.role)
    eval_payload = {}
    if eval_record and eval_record.rubric_json:
        try:
            eval_payload = json.loads(eval_record.rubric_json)
        except Exception:
            eval_payload = {}

    if should_ask_follow_up_from_evaluation(eval_payload, session):
        session.follow_up_count += 1
        session.state = "FOLLOW_UP"
        follow_up = await ai_services.generate_follow_up_question(
            completed_segment,
            session.level,
            session.role,
            session.language,
        )
        return {
            "text": follow_up,
            "status": "INTERVIEWING",
            "completed_segment": None,
            "ended": False,
        }

    completed_ids.add(int(session.current_question_id))
    set_completed_ids(session, completed_ids)
    session.follow_up_count = 0

    if has_three_consecutive_wrong(db, session.id):
        session.state = "EARLY_STOPPED"
        return {
            "text": "Buổi phỏng vấn tạm dừng tại đây vì bạn đang gặp khó khăn với nhiều câu liên tiếp. AI sẽ tổng hợp báo cáo và gợi ý keyword để bạn ôn tập.",
            "status": "ENDED",
            "completed_segment": completed_segment,
            "ended": True,
        }

    if int(session.current_question_id) >= total_questions:
        session.state = "COMPLETED"
        return {
            "text": "Cảm ơn bạn. Buổi phỏng vấn đã hoàn tất, AI đang tổng hợp báo cáo đánh giá cho bạn.",
            "status": "ENDED",
            "completed_segment": completed_segment,
            "ended": True,
        }

    next_question = template_questions[int(session.current_question_id)]
    session.current_question_id = next_question["id"]
    session.state = "ASKING"
    return {
        "text": render_next_question_with_feedback(eval_payload, next_question, total_questions),
        "status": "INTERVIEWING",
        "completed_segment": completed_segment,
        "ended": False,
    }

def build_per_question_payload(db: Session, session_id: int, template_questions: list):
    evaluations = db.query(models.Evaluation).filter(models.Evaluation.session_id == session_id).all()
    question_map = {int(q["id"]): q for q in template_questions}
    payload = []

    for evaluation in evaluations:
        question_id = int(evaluation.question_id)
        template_question = question_map.get(question_id, {})
        rubric = {}
        if evaluation.rubric_json:
            try:
                rubric = json.loads(evaluation.rubric_json)
            except Exception:
                rubric = {}

        keyword_hints = rubric.get("keyword_hints") or extract_keyword_hints(template_question.get("answer", ""))

        payload.append({
            "question_id": str(question_id),
            "question_text": template_question.get("question", ""),
            "topic": template_question.get("topic", ""),
            "difficulty": normalize_difficulty(template_question.get("difficulty", "")),
            "score": evaluation.score,
            "correctness": evaluation.correctness,
            "explanation": evaluation.explanation,
            "expected_answer": template_question.get("expected_answer") or template_question.get("answer", ""),
            "score_rule": template_question.get("score_rule", {}),
            "rubric": rubric.get("rubric", {}),
            "issues": rubric.get("issues", []),
            "suggestion": rubric.get("suggestion", ""),
            "keyword_hints": normalize_keyword_hints(keyword_hints),
            "evidence": rubric.get("evidence", []),
        })

    payload.sort(key=lambda item: int(item["question_id"]))
    return payload

async def ensure_segment_evaluated(db: Session, session_id: int, segment: dict, level: str, role: str):
    existing = db.query(models.Evaluation).filter(
        models.Evaluation.session_id == session_id,
        models.Evaluation.question_id == segment["question_id"],
    ).first()
    if not segment.get("initial_answer"):
        return existing
    if not is_meaningful_answer(segment.get("initial_answer", "")):
        eval_result = {
            "correctness": "Wrong",
            "score": 0,
            "explanation": "Ứng viên không cung cấp câu trả lời hợp lệ cho câu hỏi này.",
            "rubric": {
                "technical_accuracy": 0,
                "depth": 0,
                "clarity": 0,
                "relevance": 0,
            },
            "issues": ["Không có câu trả lời hợp lệ."],
            "suggestion": "Hãy trả lời trực tiếp vào câu hỏi; nếu chưa chắc, hãy nêu cách hiểu và giả định của bạn.",
            "keyword_hints": segment.get("expected_keywords", []),
            "evidence": [],
        }
        if existing:
            existing.correctness = eval_result["correctness"]
            existing.score = eval_result["score"]
            existing.explanation = eval_result["explanation"]
            existing.rubric_json = json.dumps(eval_result, ensure_ascii=False)
            db.commit()
            db.refresh(existing)
            return existing
        return crud.create_evaluation(
            db=db,
            session_id=session_id,
            question_id=segment["question_id"],
            answer_id=0,
            correctness=eval_result["correctness"],
            score=eval_result["score"],
            explanation=eval_result["explanation"],
            rubric_json=json.dumps(eval_result, ensure_ascii=False),
        )

    has_follow_ups = bool(segment.get("follow_ups"))
    if existing and not has_follow_ups:
        return existing

    eval_result = await ai_services.evaluate_segment(segment, level, role)
    if existing:
        existing.correctness = eval_result["correctness"]
        existing.score = eval_result["score"]
        existing.explanation = eval_result["explanation"]
        existing.rubric_json = json.dumps(eval_result, ensure_ascii=False)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        return crud.create_evaluation(
            db=db,
            session_id=session_id,
            question_id=segment["question_id"],
            answer_id=0,
            correctness=eval_result["correctness"],
            score=eval_result["score"],
            explanation=eval_result["explanation"],
            rubric_json=json.dumps(eval_result, ensure_ascii=False),
        )

async def finalize_session_report(db: Session, session_id: int):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        return None

    history = crud.get_session_messages(db, session_id)
    template_questions = get_session_questions(session)
    per_question = build_per_question_payload(db, session_id, template_questions)
    meaningful_user_answers = [msg for msg in history if msg.role == "user" and is_meaningful_answer(msg.content)]

    if not meaningful_user_answers:
        report = {
            "overall_score": 0,
            "max_score": 10,
            "strengths": ["Chưa có dữ liệu phỏng vấn."],
            "weaknesses": ["Ứng viên chưa cung cấp câu trả lời nào."],
            "final_feedback": "Phiên phỏng vấn không có câu trả lời hợp lệ từ ứng viên nên điểm tổng là 0.",
            "score_by_difficulty": {"easy": 0, "medium": 0, "hard": 0},
            "per_question": per_question,
            "skill_breakdown": [],
            "improvement_plan": ["Hay doi AI hoi xong cau mo dau/cau hoi ky thuat, sau do tra loi ro rang vao dung cau hoi."],
            "hire_recommendation": "reject",
        }
    else:
        report = await ai_services.evaluate_overall_session(
            history,
            session.role,
            session.level,
            session.language,
            per_question=per_question,
        )

    report["proctoring"] = get_proctoring_summary(session)
    session.report_data = json.dumps(report, ensure_ascii=False)
    session.status = "ENDED"
    db.commit()
    return report

report_generation_sessions = set()

def schedule_report_generation(background_tasks: BackgroundTasks, session_id: int):
    if session_id in report_generation_sessions:
        return
    report_generation_sessions.add(session_id)
    background_tasks.add_task(generate_report_background_task, session_id)

async def generate_report_background_task(session_id: int):
    db = SessionLocal()
    try:
        session = db.query(models.Session).filter(models.Session.id == session_id).first()
        if not session:
            return
        if session.report_data:
            return

        history = crud.get_session_messages(db, session_id)
        if session.template_id and history:
            try:
                template_questions = get_session_questions(session)
                segments = get_segments(history, template_questions)
                for segment in segments:
                    if segment.get("initial_answer"):
                        await ensure_segment_evaluated(db, session_id, segment, session.level, session.role)
                session.question_count = db.query(models.Evaluation).filter(models.Evaluation.session_id == session_id).count()
                db.commit()
            except Exception as e:
                print(f"Error evaluating remaining segments during report generation: {e}")

        await finalize_session_report(db, session_id)
    except Exception as e:
        print(f"Report generation background failed for session {session_id}: {e}")
    finally:
        report_generation_sessions.discard(session_id)
        db.close()

active_connections = {}
session_start_locks = {}

async def synthesize_ai_audio(text: str, language: str):
    try:
        return await tts_service.synthesize(text, language=language)
    except Exception as tts_error:
        print(f"TTS error: {tts_error}")
        raise

async def evaluate_segment_background_task(session_id: int, segment: dict, level: str, role: str):
    db = SessionLocal()
    try:
        await ensure_segment_evaluated(db, session_id, segment, level, role)
        
        # Check early stopping condition
        evals = db.query(models.Evaluation).filter(models.Evaluation.session_id == session_id).order_by(models.Evaluation.id.desc()).limit(3).all()
        if len(evals) == 3 and all(e.correctness == "Wrong" for e in evals):
            await finalize_session_report(db, session_id)
            
            # Gửi thông báo kết thúc sớm tới WebSocket nếu đang hoạt động
            if session_id in active_connections:
                ws = active_connections[session_id]
                try:
                    closing_text = "Buổi phỏng vấn tạm dừng tại đây. AI đang phân tích kết quả và chuyển hướng bạn đến trang báo cáo."
                    await ws.send_json({"text": closing_text, "status": "ENDED"})
                    await ws.close()
                except Exception as ws_err:
                    print(f"Error sending early stopping notification: {ws_err}")
    finally:
        db.close()

async def ai_processing_task(websocket: WebSocket, queue: asyncio.Queue, session_id: int, background_tasks: BackgroundTasks, db: Session, session: models.Session):
    while True:
        try:
            db.refresh(session)
            # Lấy dữ liệu âm thanh hoặc văn bản từ hàng đợi (nếu không có thì chờ)
            input_data = await queue.get()
            
            if input_data == b"START_INTERVIEW":
                user_text = ""
                # Skip STT and saving user message for the initial trigger
            elif isinstance(input_data, dict) and input_data.get("type") == "text":
                user_text = input_data.get("content", "")
                
                # Gửi text về frontend
                await websocket.send_json({"sender": session.candidate_name.split(" ")[0] if session.candidate_name else "You", "text": user_text})
                
                # Lưu log user
                crud.create_message(db, session_id, "user", user_text)
            else:
                # STT
                user_text, raw_text = await transcribe_interview_audio(input_data, session, db)
                
                # Gửi text về frontend
                await websocket.send_json({"sender": session.candidate_name.split(" ")[0] if session.candidate_name else "You", "text": user_text})
                
                # Lưu log user
                crud.create_message(db, session_id, "user", user_text)
            
            # Khởi tạo history và gọi LLM
            history = crud.get_session_messages(db, session_id)
            
            # Transition status from CHITCHAT to INTERVIEWING once user responds to the greeting
            if session.status == "CHITCHAT":
                user_msgs = [msg for msg in history if msg.role == "user"]
                if len(user_msgs) > 0:
                    session.status = "INTERVIEWING"
                    db.commit()
                    db.refresh(session)
            
            ai_text = await ai_services.generate_interview_response(
                history=history,
                status=session.status,
                role=session.role,
                level=session.level,
                name=session.candidate_name,
                language=session.language,
                template_id=session.template_id
            )
            
            # Lưu log ai
            crud.create_message(db, session_id, "ai", ai_text)
            
            # Async Evaluation & Ending Condition
            if session.status == "INTERVIEWING" and session.template_id:
                try:
                    from template_service import template_service
                    template_questions = get_session_questions(session)
                    
                    full_history = crud.get_session_messages(db, session_id)
                    segments = get_segments(full_history, template_questions)
                    
                    existing_evals = db.query(models.Evaluation).filter(models.Evaluation.session_id == session_id).all()
                    evaluated_q_ids = {e.question_id for e in existing_evals}
                    
                    for idx, seg in enumerate(segments):
                        if idx < len(segments) - 1 and seg["initial_answer"] and seg["question_id"] not in evaluated_q_ids:
                            background_tasks.add_task(
                                evaluate_segment_background_task,
                                session_id=session_id,
                                segment=seg,
                                level=session.level,
                                role=session.role
                            )
                            evaluated_q_ids.add(seg["question_id"])
                            
                    if segments:
                        last_seg = segments[-1]
                        if last_seg["question_id"] == len(template_questions) and last_seg["initial_answer"]:
                            if "?" not in ai_text:
                                if last_seg["question_id"] not in evaluated_q_ids:
                                    background_tasks.add_task(
                                        evaluate_segment_background_task,
                                        session_id=session_id,
                                        segment=last_seg,
                                        level=session.level,
                                        role=session.role
                                    )
                                    evaluated_q_ids.add(last_seg["question_id"])
                                session.status = "ENDED"
                                
                    session.question_count = len(evaluated_q_ids)
                    db.commit()
                except Exception as e:
                    print(f"Error in segment evaluation task: {e}")
            
            # Synthesize Audio (TTS)
            audio_response = await synthesize_ai_audio(ai_text, session.language)
            
            # Gửi kết quả về frontend
            await websocket.send_json({"text": ai_text, "status": session.status})
            await websocket.send_bytes(audio_response)
            
            # Đánh dấu đã xử lý xong task này trong queue
            queue.task_done()
            
        except WebSocketDisconnect:
            break
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error in ai_processing_task: {e}")
            queue.task_done()

async def ai_processing_task_v2(websocket: WebSocket, queue: asyncio.Queue, session_id: int, background_tasks: BackgroundTasks, db: Session, session: models.Session):
    while True:
        got_queue_item = False
        try:
            db.refresh(session)
            input_data = await queue.get()
            got_queue_item = True

            if input_data == b"START_INTERVIEW":
                pass
            elif isinstance(input_data, dict) and input_data.get("type") == "text":
                user_text = input_data.get("content", "")
                if not (session.status == "CHITCHAT" and classify_chitchat_reply(user_text) == "start") and should_retry_answer(user_text):
                    user_message = crud.create_message(db, session_id, "user", user_text)
                    await websocket.send_json({
                        "message_id": user_message.id,
                        "sender": session.candidate_name.split(" ")[0] if session.candidate_name else "You",
                        "text": user_text,
                    })
                    await websocket.send_json({
                        "sender": "AI",
                        "text": "Câu trả lời của bạn đang quá ngắn hoặc chưa rõ ý. Bạn vui lòng trả lời đầy đủ hơn trước khi mình chấm câu này nhé.",
                        "status": session.status,
                        "has_audio": False,
                        "retry_answer": True,
                    })
                    queue.task_done()
                    got_queue_item = False
                    continue
                user_message = crud.create_message(db, session_id, "user", user_text)
                user_payload = {
                    "message_id": user_message.id,
                    "sender": session.candidate_name.split(" ")[0] if session.candidate_name else "You",
                    "text": user_text,
                }
                await websocket.send_json(user_payload)
            else:
                user_text, raw_text = await transcribe_interview_audio(input_data, session, db)
                if is_unclear_transcript(user_text):
                    await websocket.send_json({
                        "sender": "AI",
                        "text": "Mình chưa nghe rõ phần trả lời của bạn. Bạn nói lại chậm hơn một chút hoặc nhập câu trả lời bằng chữ nhé.",
                        "status": session.status,
                        "has_audio": False,
                        "retry_answer": True,
                    })
                    queue.task_done()
                    got_queue_item = False
                    continue

                if not (session.status == "CHITCHAT" and classify_chitchat_reply(user_text) == "start") and should_retry_answer(user_text):
                    user_message = crud.create_message(db, session_id, "user", user_text)
                    await websocket.send_json({
                        "message_id": user_message.id,
                        "sender": session.candidate_name.split(" ")[0] if session.candidate_name else "You",
                        "text": user_text,
                    })
                    await websocket.send_json({
                        "sender": "AI",
                        "text": "Câu trả lời của bạn đang quá ngắn hoặc chưa có đủ thông tin để chấm. Bạn vui lòng trả lời cụ thể hơn nhé.",
                        "status": session.status,
                        "has_audio": False,
                        "retry_answer": True,
                    })
                    queue.task_done()
                    got_queue_item = False
                    continue

                user_message = crud.create_message(db, session_id, "user", user_text)
                user_payload = {
                    "message_id": user_message.id,
                    "sender": session.candidate_name.split(" ")[0] if session.candidate_name else "You",
                    "text": user_text,
                }
                if raw_text != user_text:
                    user_payload["raw_transcript"] = raw_text
                await websocket.send_json(user_payload)

            if input_data == b"START_INTERVIEW":
                start_lock = session_start_locks.setdefault(session_id, asyncio.Lock())
                async with start_lock:
                    db.refresh(session)
                    history = crud.get_session_messages(db, session_id)
                    if history or (session.state or "GREETING") not in {"GREETING", "GREETING_SENT"}:
                        queue.task_done()
                        got_queue_item = False
                        continue
                    session.state = "GREETING_SENT"
                    db.commit()
                    db.refresh(session)
                    ai_text = render_interview_greeting(session)
            else:
                history = crud.get_session_messages(db, session_id)

            if input_data != b"START_INTERVIEW" and session.template_id:
                if session.status == "CHITCHAT":
                    intent = classify_chitchat_reply(user_text)
                    if intent != "start":
                        ai_text = render_chitchat_intent_response(intent, session.candidate_name, session.role)
                        session.state = "GREETING_SENT"
                        db.commit()
                        db.refresh(session)
                        ai_message = crud.create_message(db, session_id, "ai", ai_text)
                        audio_response = await synthesize_ai_audio(ai_text, session.language)
                        await websocket.send_json({
                            "message_id": ai_message.id,
                            "sender": "AI",
                            "text": ai_text,
                            "status": session.status,
                            "has_audio": audio_response is not None,
                        })
                        if audio_response is not None:
                            await websocket.send_bytes(audio_response)
                        queue.task_done()
                        got_queue_item = False
                        continue
                    session.status = "INTERVIEWING"
                    db.commit()
                    db.refresh(session)

                template_questions = get_session_questions(session)
                turn = await next_interview_turn(db, session, history, template_questions)
                ai_text = turn["text"] or await ai_services.generate_interview_response(
                    history=history,
                    status=session.status,
                    role=session.role,
                    level=session.level,
                    name=session.candidate_name,
                    language=session.language,
                    template_id=session.template_id,
                )

                session.status = turn["status"]
                session.question_count = db.query(models.Evaluation).filter(models.Evaluation.session_id == session_id).count()

                if turn.get("ended"):
                    db.commit()
                    db.refresh(session)
                    schedule_report_generation(background_tasks, session_id)
                else:
                    db.commit()
                    db.refresh(session)
            elif input_data != b"START_INTERVIEW":
                if session.status == "CHITCHAT":
                    user_msgs = [msg for msg in history if msg.role == "user"]
                    if user_msgs:
                        intent = classify_chitchat_reply(user_text)
                        if intent != "start":
                            ai_text = render_chitchat_intent_response(intent, session.candidate_name, session.role)
                            session.state = "GREETING_SENT"
                            db.commit()
                            db.refresh(session)
                            ai_message = crud.create_message(db, session_id, "ai", ai_text)
                            audio_response = await synthesize_ai_audio(ai_text, session.language)
                            await websocket.send_json({
                                "message_id": ai_message.id,
                                "sender": "AI",
                                "text": ai_text,
                                "status": session.status,
                                "has_audio": audio_response is not None,
                            })
                            if audio_response is not None:
                                await websocket.send_bytes(audio_response)
                            queue.task_done()
                            got_queue_item = False
                            continue
                        session.status = "INTERVIEWING"
                        db.commit()
                        db.refresh(session)

                ai_text = await ai_services.generate_interview_response(
                    history=history,
                    status=session.status,
                    role=session.role,
                    level=session.level,
                    name=session.candidate_name,
                    language=session.language,
                    template_id=session.template_id,
                )

            ai_message = crud.create_message(db, session_id, "ai", ai_text)

            audio_response = await synthesize_ai_audio(ai_text, session.language)
            await websocket.send_json({
                "message_id": ai_message.id,
                "sender": "AI",
                "text": ai_text,
                "status": session.status,
                "has_audio": audio_response is not None,
            })
            if audio_response is not None:
                await websocket.send_bytes(audio_response)
            queue.task_done()
            got_queue_item = False

        except WebSocketDisconnect:
            break
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error in ai_processing_task_v2: {e}")
            try:
                await websocket.send_json({
                    "sender": "AI",
                    "text": "Mình gặp lỗi khi xử lý câu trả lời vừa rồi. Bạn thử trả lời lại hoặc bấm nói lại giúp mình nhé.",
                    "status": session.status,
                    "has_audio": False,
                    "retry_answer": True,
                })
            except Exception:
                pass
            if got_queue_item:
                queue.task_done()


@app.websocket("/ws/interview/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    await websocket.accept()
    
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        await websocket.close(code=1008)
        return

    if session_id in active_connections:
        try:
            await active_connections[session_id].close(code=4000)
        except Exception:
            pass
    active_connections[session_id] = websocket

    if session.status == "ENDED":
        await websocket.send_json({"text": "Phiên phỏng vấn đã kết thúc. Báo cáo đang sẵn sàng.", "status": "ENDED"})
        await websocket.close()
        active_connections.pop(session_id, None)
        return

    # Khởi tạo Hàng đợi
    if not session.template_id:
        await websocket.send_json({
            "sender": "system",
            "text": "Phiên phỏng vấn này chưa có template câu hỏi. Vui lòng tạo phiên mới và chọn template trước khi bắt đầu.",
            "status": "CONFIG_ERROR",
        })
        await websocket.close(code=1008)
        active_connections.pop(session_id, None)
        return

    audio_queue = asyncio.Queue()
    
    # Chạy luồng Consumer (AI) ngầm
    ai_task = asyncio.create_task(ai_processing_task_v2(websocket, audio_queue, session_id, background_tasks, db, session))

    # Trigger AI greeting if this is the start of the interview (no history)
    history = crud.get_session_messages(db, session_id)
    if not history:
        await audio_queue.put(b"START_INTERVIEW")

    try:
        while True:
            # Luồng Producer: Luôn lắng nghe websocket, không bị block bởi xử lý AI
            message = await websocket.receive()
            if "bytes" in message and message["bytes"]:
                if audio_queue.qsize() >= MAX_WS_QUEUE_SIZE:
                    await websocket.send_json({"sender": "system", "text": "Hệ thống đang xử lý câu trả lời trước đó, vui lòng chờ một chút."})
                    continue
                if len(message["bytes"]) > MAX_AUDIO_PAYLOAD_BYTES:
                    await websocket.send_json({"sender": "system", "text": "Audio quá lớn để xử lý. Vui lòng gửi câu trả lời ngắn hơn hoặc dùng ô nhập text."})
                    continue
                await audio_queue.put(message["bytes"])
            elif "text" in message and message["text"]:
                text_content = message["text"]
                if audio_queue.qsize() >= MAX_WS_QUEUE_SIZE:
                    await websocket.send_json({"sender": "system", "text": "Hệ thống đang xử lý câu trả lời trước đó, vui lòng chờ một chút."})
                    continue
                try:
                    import json
                    parsed = json.loads(text_content)
                    if isinstance(parsed, dict) and "text" in parsed:
                        if audio_queue.qsize() >= MAX_WS_QUEUE_SIZE:
                            await websocket.send_json({"sender": "system", "text": "Hệ thống đang xử lý câu trả lời trước đó, vui lòng chờ một chút."})
                            continue
                        await audio_queue.put({"type": "text", "content": str(parsed["text"])[:MAX_TEXT_ANSWER_CHARS]})
                    else:
                        await audio_queue.put({"type": "text", "content": text_content[:MAX_TEXT_ANSWER_CHARS]})
                except Exception:
                    await audio_queue.put({"type": "text", "content": text_content[:MAX_TEXT_ANSWER_CHARS]})
            elif message.get("type") == "websocket.disconnect":
                print(f"Client {session_id} disconnected via event")
                break

    except WebSocketDisconnect:
        print(f"Client {session_id} disconnected")
    finally:
        if active_connections.get(session_id) is websocket:
            active_connections.pop(session_id, None)
        # Khi client ngắt kết nối, dọn dẹp luồng xử lý AI
        ai_task.cancel()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, Depends, UploadFile, File
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
import json
import os

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
            conn.close()
        except Exception as e:
            print(f"Migration error: {e}")

migrate_db()
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
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
from pydantic import BaseModel

class SessionCreate(BaseModel):
    name: str
    role: str
    level: str
    language: str = "vi"
    template_id: str = None

@app.post("/api/sessions")
async def create_new_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    new_session = models.Session(
        candidate_name=session_data.name,
        role=session_data.role, 
        level=session_data.level, 
        language=session_data.language,
        status="CHITCHAT",
        template_id=session_data.template_id
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"session_id": new_session.id}

@app.post("/api/sessions/{session_id}/end")
async def end_session(session_id: int, db: Session = Depends(get_db)):
    crud.update_session_status(db, session_id, "ENDED")
    # Tự động tạo kết quả đánh giá tổng quát
    history = crud.get_session_messages(db, session_id)
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    
    if session and history:
        # Evaluate any remaining segments
        if session.template_id:
            try:
                from template_service import template_service
                template_questions = template_service.get_template_questions(session.template_id)
                segments = get_segments(history, template_questions)
                
                existing_evals = db.query(models.Evaluation).filter(models.Evaluation.session_id == session_id).all()
                evaluated_q_ids = {e.question_id for e in existing_evals}
                
                for seg in segments:
                    if seg["question_id"] not in evaluated_q_ids and seg["initial_answer"]:
                        eval_result = await ai_services.evaluate_segment(seg, session.level, session.role)
                        crud.create_evaluation(
                            db=db,
                            session_id=session_id,
                            question_id=seg["question_id"],
                            answer_id=0,
                            correctness=eval_result["correctness"],
                            score=eval_result["score"],
                            explanation=eval_result["explanation"]
                        )
                
                # Refresh session question_count
                session.question_count = db.query(models.Evaluation).filter(models.Evaluation.session_id == session_id).count()
                db.commit()
            except Exception as e:
                print(f"Error evaluating remaining segments during end_session: {e}")
                
        user_messages = [msg for msg in history if msg.role == "user"]
        if len(user_messages) == 0:
            report = {
                "overall_score": 0,
                "strengths": ["Không có dữ liệu đánh giá (No data available)."],
                "weaknesses": ["Không có dữ liệu đánh giá (No data available)."],
                "final_feedback": "Phiên phỏng vấn kết thúc quá sớm. Ứng viên chưa cung cấp bất kỳ câu trả lời nào để AI có thể đưa ra nhận xét."
            }
        else:
            report = await ai_services.evaluate_overall_session(history, session.role, session.level, session.language)
            
        session.report_data = json.dumps(report)
        db.commit()
        return {"status": "success", "report": report}
    return {"status": "failed", "message": "Session not found or empty"}

@app.get("/api/sessions/{session_id}/report")
async def get_session_report(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if session and session.report_data:
        return {"status": "success", "report": json.loads(session.report_data)}
    return {"status": "failed", "message": "Report not found"}

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

@app.post("/api/cv/extract")
async def extract_cv(file: UploadFile = File(...)):
    # Save file temporarily
    ext = file.filename.split('.')[-1].lower() if '.' in file.filename else 'pdf'
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
        
    try:
        text = cv_extractor.extract_text(tmp_path, file.filename)
        profile = await cv_extractor.parse_cv(text)
        
        role_fit = profile.get("role_fit", "Software Engineer")
        inferred_level = profile.get("inferred_level", 1)
        matches = template_service.match_templates(role_fit, inferred_level)
        
        profile["confidence"] = 0.92
        
        return {
            "status": "success",
            "profile": profile,
            "matches": matches
        }
    finally:
        os.remove(tmp_path)

def clean_words(text: str):
    import re
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)

def match_question(ai_text: str, template_questions: list):
    ai_text_lower = ai_text.lower()
    for q in template_questions:
        if f"câu {q['id']}" in ai_text_lower:
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
                    "template_question": matched_q["question"],
                    "sample_answer": matched_q["answer"],
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

active_connections = {}

async def evaluate_segment_background_task(session_id: int, segment: dict, level: str, role: str):
    db = SessionLocal()
    try:
        eval_result = await ai_services.evaluate_segment(segment, level, role)
        
        crud.create_evaluation(
            db=db,
            session_id=session_id,
            question_id=segment["question_id"],
            answer_id=0,
            correctness=eval_result["correctness"],
            score=eval_result["score"],
            explanation=eval_result["explanation"]
        )
        
        # Check early stopping condition
        evals = db.query(models.Evaluation).filter(models.Evaluation.session_id == session_id).order_by(models.Evaluation.id.desc()).limit(3).all()
        if len(evals) == 3 and all(e.correctness == "Wrong" for e in evals):
            crud.update_session_status(db, session_id, "ENDED")
            # Tự động tạo kết quả đánh giá tổng quát
            history = crud.get_session_messages(db, session_id)
            session = db.query(models.Session).filter(models.Session.id == session_id).first()
            if session and history:
                report = await ai_services.evaluate_overall_session(history, session.role, session.level, session.language)
                session.report_data = json.dumps(report)
                db.commit()
            
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

import asyncio

async def ai_processing_task(websocket: WebSocket, queue: asyncio.Queue, session_id: int, background_tasks: BackgroundTasks, db: Session, session: models.Session):
    while True:
        try:
            db.refresh(session)
            # Lấy dữ liệu âm thanh từ hàng đợi (nếu không có thì chờ)
            audio_bytes = await queue.get()
            
            if audio_bytes == b"START_INTERVIEW":
                user_text = ""
                # Skip STT and saving user message for the initial trigger
            else:
                # STT
                user_text = await ai_services.stt(audio_bytes, session.language)
                
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
                    template_questions = template_service.get_template_questions(session.template_id)
                    
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
            audio_response = await tts_service.synthesize(ai_text, language=session.language)
            
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


@app.websocket("/ws/interview/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    await websocket.accept()
    
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        await websocket.close(code=1008)
        return

    active_connections[session_id] = websocket

    # Khởi tạo Hàng đợi
    audio_queue = asyncio.Queue()
    
    # Chạy luồng Consumer (AI) ngầm
    ai_task = asyncio.create_task(ai_processing_task(websocket, audio_queue, session_id, background_tasks, db, session))

    # Trigger AI greeting if this is the start of the interview (no history)
    history = crud.get_session_messages(db, session_id)
    if not history:
        await audio_queue.put(b"START_INTERVIEW")

    try:
        while True:
            # Luồng Producer: Luôn lắng nghe websocket, không bị block bởi xử lý AI
            message = await websocket.receive()
            if "bytes" in message and message["bytes"]:
                await audio_queue.put(message["bytes"])
            elif "text" in message and message["text"]:
                print("Received text instead of audio bytes. Ignoring.")
            elif message.get("type") == "websocket.disconnect":
                print(f"Client {session_id} disconnected via event")
                break

    except WebSocketDisconnect:
        print(f"Client {session_id} disconnected")
    finally:
        active_connections.pop(session_id, None)
        # Khi client ngắt kết nối, dọn dẹp luồng xử lý AI
        ai_task.cancel()

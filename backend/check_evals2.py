import os
import json
from dotenv import load_dotenv
load_dotenv()
from fipilot.database import database_session
from fipilot.models import InterviewTurn, InterviewSession
from sqlalchemy import select

with database_session() as db:
    session = db.scalars(select(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(1)).first()
    turns = db.scalars(select(InterviewTurn).where(InterviewTurn.session_id == session.id).order_by(InterviewTurn.sequence)).all()
    for t in turns:
        print(f"Seq {t.sequence}: {json.dumps(t.evaluation, ensure_ascii=False)}")

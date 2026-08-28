import os
from dotenv import load_dotenv
load_dotenv()

from fipilot.database import database_session
from fipilot.models import InterviewTurn, InterviewSession
from sqlalchemy import select

with database_session() as db:
    stmt = select(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(1)
    session = db.scalars(stmt).first()
    
    turns = db.scalars(select(InterviewTurn).where(InterviewTurn.session_id == session.id).order_by(InterviewTurn.sequence)).all()
    for t in turns:
        print(f"Seq {t.sequence}: Has Eval? {t.evaluation is not None}")

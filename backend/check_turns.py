import os
from dotenv import load_dotenv
load_dotenv()

from fipilot.database import database_session
from fipilot.models import InterviewTurn, InterviewSession
from sqlalchemy import select

with database_session() as db:
    stmt = select(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(1)
    session = db.scalars(stmt).first()
    print("Latest Session ID:", session.id)
    
    turns = db.scalars(select(InterviewTurn).where(InterviewTurn.session_id == session.id).order_by(InterviewTurn.sequence)).all()
    print(f"Number of turns for this session: {len(turns)}")
    for t in turns:
        print(f"Turn {t.sequence}: {t.answer}")

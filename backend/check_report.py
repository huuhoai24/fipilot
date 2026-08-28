import os
from dotenv import load_dotenv
load_dotenv()

from fipilot.database import database_session
from fipilot.models import InterviewReport, InterviewSession
from sqlalchemy import select
import json

with database_session() as db:
    stmt = select(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(1)
    session = db.scalars(stmt).first()
    print("Session ID:", session.id)
    
    report = db.scalar(select(InterviewReport).where(InterviewReport.session_id == session.id))
    if report:
        print("Report found!")
        print(json.dumps(report.content, indent=2, ensure_ascii=False))
    else:
        print("No report found for this session!")

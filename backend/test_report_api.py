import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

from fipilot.database import database_session
from fipilot.models import InterviewSession
from sqlalchemy import select

with database_session() as db:
    stmt = select(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(1)
    session = db.scalars(stmt).first()
    client_id = str(session.client_id)
    session_id = session.id

response = requests.post("http://127.0.0.1:8000/api/v2/interview/report", json={"session_id": session_id}, headers={"X-User-ID": client_id})
data = response.json()
print("Assessments count:", len(data.get("assessments", [])))
for idx, a in enumerate(data.get("assessments", [])):
    print(f"Assessment {idx}: {a.get('rationale')} (Turn {a.get('turn_index')})")

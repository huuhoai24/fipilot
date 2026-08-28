import os
from dotenv import load_dotenv
load_dotenv()
from fipilot.database import database_session
from fipilot.models import Resume
from sqlalchemy import select
import requests

with database_session() as db:
    stmt = select(Resume).order_by(Resume.created_at.desc()).limit(1)
    resume = db.scalars(stmt).first()

if not resume:
    print("No resumes in DB!")
    exit(1)

resume_id = str(resume.id)
client_id = str(resume.client_id)
print(f"Found Resume: {resume_id}, Client: {client_id}")

headers = {
    "X-User-ID": client_id,
    "Content-Type": "application/json"
}
payload = {
    "candidate_id": resume_id,
    "config": {
        "role": "AI Engineer",
        "level": "Junior",
        "duration_minutes": 30
    }
}

resp = requests.post("http://127.0.0.1:8000/api/v2/interview/prepare", json=payload, headers=headers)
print("Status:", resp.status_code)
print("Body:", resp.text)
